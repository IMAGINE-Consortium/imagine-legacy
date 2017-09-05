# -*- coding: utf-8 -*-

import abc
import os
import tempfile
import subprocess

import healpy
import numpy as np

from d2o import distributed_data_object

from imagine.observers.observer import Observer
from imagine.magnetic_fields.magnetic_field import MagneticField


class Hammurapy(Observer):
    def __init__(self, hammurabi_executable, conf_directory='./confs',
                 working_directory_base='.', nside=128,
                 analytic_ensemble_mean=False):
        self.hammurabi_executable = os.path.abspath(hammurabi_executable)
        self.conf_directory = os.path.abspath(conf_directory)
        self.working_directory_base = os.path.abspath(working_directory_base)

        self.analytic_ensemble_mean = bool(analytic_ensemble_mean)

        self.nside = int(nside)

        self.last_call_log = ""

        sync_template_fname = os.path.join(self.conf_directory,
                                           'IQU_sync.fits')
        dust_template_fname = os.path.join(self.conf_directory,
                                           'IQU_dust.fits')

        self.basic_parameters = {'B_ran_mem_lim': '6',
                                 'obs_shell_index_numb': '1',
                                 'total_shell_numb': '3',
                                 'vec_size_R': '500',
                                 'max_radius': '30',
                                 'max_z': '15',
                                 'B_field_transform_lon': '-999',
                                 'B_field_transform_lat': '-999',
                                 'TE_grid_filename': 'negrid_n400.bin',
                                 'TE_nx': '400',
                                 'TE_ny': '400',
                                 'TE_nz': '80',
                                 'TE_interp': 'F',
                                 'do_sync_emission': 'F',
                                 'do_rm': 'F',
                                 'do_dm': 'F',
                                 'do_dust': 'F',
                                 'do_tau': 'F',
                                 'do_ff': 'F',
                                 'obs_freq_GHz': '23',
                                 'sync_template_fname': sync_template_fname,
                                 'dust_template_fname': dust_template_fname
                                 }

    @abc.abstractproperty
    def magnetic_field_class(self):
        return MagneticField

    def _make_temp_folder(self):
        prefix = os.path.join(self.working_directory_base, 'temp_hammurabi_')
        return tempfile.mkdtemp(prefix=prefix)

    def _remove_folder(self, path):
        # Try multiple times in order to overcome 'Directory not empty' errors
        # Hopefully open file handles get closed in the meantime
        n = 0
        while n < 10:
            temp_process = subprocess.Popen(['rm', '-rf', path],
                                            stderr=subprocess.PIPE)
            # wait until process is finished
            errlog = temp_process.communicate()[1]
            # check if there were some errors
            if errlog == '':
                break
        else:
            self.logger.warning('Could not delete %s' % path)

    def _read_fits_file(self, path, name, nside):
        map_path = os.path.join(path, name)
        result_list = []
        i = 0
        while True:
            try:
                loaded_map = healpy.read_map(map_path, verbose=False,
                                             field=i)
                loaded_map = healpy.ud_grade(loaded_map, nside_out=nside)
                result_list += [loaded_map]
                i += 1
            except IndexError:
                break
        return result_list

    def _call_hammurabi(self, path):
        parameters_file_path = os.path.join(path, 'parameters.txt')
        temp_process = subprocess.Popen([self.hammurabi_executable,
                                         parameters_file_path],
                                        stdout=subprocess.PIPE,
                                        cwd=self.conf_directory)
        self.last_call_log = temp_process.communicate()[0]

    def _initialize_observable_dict(self, observable_dict, magnetic_field):
        pass

    def _build_parameter_dict(self, parameter_dict, magnetic_field,
                              working_directory, local_ensemble_index):
        grid_space = magnetic_field.domain[1]
        lx, ly, lz = np.array(grid_space.shape)*np.array(grid_space.distances)
        nx, ny, nz = grid_space.shape
        if local_ensemble_index is not None:
            random_seed = magnetic_field.random_seed[local_ensemble_index]
            parameter_dict.update({'B_field_seed': random_seed})

        parameter_dict.update({'B_field_lx': lx,
                               'B_field_ly': ly,
                               'B_field_lz': lz,
                               'B_field_nx': nx,
                               'B_field_ny': ny,
                               'B_field_nz': nz,
                               })
        parameter_dict.update({'obs_NSIDE': self.nside})

    def _write_parameter_dict(self, parameter_dict, working_directory):
        parameters_string = ''
        for item in parameter_dict:
            parameters_string += item + '=' + str(parameter_dict[item]) + '\n'

        parameters_file_path = os.path.join(working_directory,
                                            'parameters.txt')
        with open(parameters_file_path, 'wb') as config_file:
            config_file.write(parameters_string)

    def _fill_observable_dict(self, observable_dict, working_directory,
                              ensemble_index):
        return observable_dict

    def _add_ensemble_mean(self, observable_dict, working_directory):
        pass

    def __call__(self, magnetic_field):

        if not isinstance(magnetic_field, self.magnetic_field_class):
            raise ValueError("Given magnetic field is not a subclass of" +
                             " %s" % str(self.magnetic_field_class))

        observable_dict = {}
        self._initialize_observable_dict(observable_dict=observable_dict,
                                         magnetic_field=magnetic_field)

        # iterate over ensemble and put result into result_observable
        # get the local shape by creating a dummy d2o
        ensemble_number = magnetic_field.shape[0]
        dummy = distributed_data_object(global_shape=(ensemble_number,),
                                        distribution_strategy='equal',
                                        dtype=np.float)

        local_length = dummy.distributor.local_length
        for local_ensemble_index in xrange(local_length):
            self.logger.debug("Processing local_ensemble_index %i." %
                              local_ensemble_index)
            # create a temporary folder
            working_directory = self._make_temp_folder()

            # create dictionary for parameter file
            parameter_dict = self.basic_parameters.copy()

            # set the parameters for a numerical run
            parameter_dict['B_field_interp'] = 'T'
            parameter_dict['use_B_analytic'] = 'F'

            self._build_parameter_dict(
                                    parameter_dict=parameter_dict,
                                    magnetic_field=magnetic_field,
                                    working_directory=working_directory,
                                    local_ensemble_index=local_ensemble_index)

            self._write_parameter_dict(parameter_dict=parameter_dict,
                                       working_directory=working_directory)

            # call hammurabi
            self._call_hammurabi(working_directory)

            # if hammurabi failed, _fill_observable_dict will fail
            try:
                self._fill_observable_dict(observable_dict,
                                           working_directory,
                                           local_ensemble_index)
            except:
                self.logger.critical("Hammurabi failed! Last call log:\n" +
                                     self.last_call_log)
                raise
            finally:
                self._remove_folder(working_directory)

        if self.analytic_ensemble_mean:
            # compute ensemble_mean on last node and add it to the observables
            rank = dummy.comm.rank
            size = dummy.comm.size

            if rank + 1 == size:
                self.logger.debug("Processing ensemble mean.")
                # create a temporary folder
                working_directory = self._make_temp_folder()

                # create dictionary for parameter file
                parameter_dict = self.basic_parameters.copy()

                # set the parameters for an analytic run
                parameter_dict['use_B_analytic'] = 'T'

                self._build_parameter_dict(
                                        parameter_dict=parameter_dict,
                                        magnetic_field=magnetic_field,
                                        working_directory=working_directory,
                                        local_ensemble_index=None)

                self._write_parameter_dict(parameter_dict=parameter_dict,
                                           working_directory=working_directory)

                # call hammurabi
                self._call_hammurabi(working_directory)

                # if hammurabi failed, _add_ensemble_mean will fail
                try:
                    self._add_ensemble_mean(observable_dict, working_directory)
                except:
                    self.logger.critical("Hammurabi failed! Last call log:\n" +
                                         self.last_call_log)
                    raise
                finally:
                    self._remove_folder(working_directory)
            else:
                working_directory = None
                self._add_ensemble_mean(observable_dict, working_directory)

        return observable_dict
