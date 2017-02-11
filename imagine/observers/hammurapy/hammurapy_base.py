# -*- coding: utf-8 -*-

import abc
import os
import tempfile
import subprocess

import healpy
import numpy as np

from d2o import distributed_data_object

from imagine.observers.observer import Observer


class HammurapyBase(Observer):
    def __init__(self, hammurabi_executable, conf_directory='./confs',
                 working_directory_base='.'):
        self.hammurabi_executable = os.path.abspath(hammurabi_executable)
        self.conf_directory = os.path.abspath(conf_directory)
        self.working_directory_base = os.path.abspath(working_directory_base)

        self.last_call_log = ""

        self.basic_parameters = {'obs_shell_index_numb': '1',
                                 'total_shell_numb': '1',
                                 'obs_NSIDE': '128',
                                 'vec_size_R': '100',
                                 'max_radius': '35',
                                 'B_field_transform_lon': '-999',
                                 'B_field_transform_lat': '-999',
                                 'TE_grid_filename': 'negrid_n400.bin',
                                 'TE_nx': '400',
                                 'TE_ny': '400',
                                 'TE_nz': '80',
                                 'B_field_do_random': 'T',
                                 'B_ran_mem_lim': '4',
                                 'do_sync_emission': 'F',
                                 'do_rm': 'F',
                                 'do_dm': 'F',
                                 'do_dust': 'F',
                                 'do_tau': 'F',
                                 'do_ff': 'F',
                                 }

    @abc.abstractproperty
    def valid_magnetic_field_class(self):
        return object

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

    def _read_fits_file(self, path, name):
        map_path = os.path.join(path, name)
        result_list = []
        i = 0
        while True:
            try:
                loaded_map = healpy.read_map(map_path, verbose=False,
                                             field=i)
                loaded_map = healpy.ud_grade(loaded_map, nside_out=128)
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

        parameter_dict.update({'B_field_lx': lx,
                               'B_field_ly': ly,
                               'B_field_lz': lz,
                               'B_field_nx': nx,
                               'B_field_ny': ny,
                               'B_field_nz': nz,
                               })

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

    def __call__(self, magnetic_field):

        observable_dict = {}
        self._initialize_observable_dict(observable_dict=observable_dict,
                                         magnetic_field=magnetic_field)

        # iterate over ensemble and put result into result_observable
        # get the local shape by creating a dummy d2o
        ensemble_number = magnetic_field.shape[0]
        dummy = distributed_data_object(global_shape=(ensemble_number,),
                                        distribution_strategy='equal')

        local_length = dummy.distributor.local_length
        for local_ensemble_index in xrange(local_length):
            # create a temporary folder
            working_directory = self._make_temp_folder()

            # create dictionary for parameter file
            parameter_dict = self.basic_parameters.copy()
            self._build_parameter_dict(
                                    parameter_dict=parameter_dict,
                                    magnetic_field=magnetic_field,
                                    working_directory=working_directory,
                                    local_ensemble_index=local_ensemble_index)

            self._write_parameter_dict(parameter_dict=parameter_dict,
                                       working_directory=working_directory)

            self._call_hammurabi(working_directory)
            self._fill_observable_dict(observable_dict,
                                       working_directory,
                                       local_ensemble_index)
            self._remove_folder(working_directory)

        return observable_dict


###########

#    def _make_parameter_file(self, working_directory, resolution, dimensions,
#                             custom_parameters={}):
#
#        # setup the default parameters
#        parameters_dict = {'B_field_lx': dimensions[0],
#                           'B_field_ly': dimensions[1],
#                           'B_field_lz': dimensions[2],
#                           'B_field_nx': int(resolution[0]),
#                           'B_field_ny': int(resolution[1]),
#                           'B_field_nz': int(resolution[2]),
#                           }
#
#                               {
#                                 'do_sync_emission': 'T',
#                                 'do_rm': 'T',
#                                 'do_dm': 'F',
#                                 'do_dust': 'F',
#                                 'do_tau': 'F',
#                                 'do_ff': 'F'}
#
#        if self.parameters_dict['do_sync_emission'] == 'T':
#            obs_sync_file_name = os.path.join(working_directory,
#                                              'IQU_sync.fits')
#            parameters_dict['obs_file_name'] = obs_sync_file_name
#
#        if self.parameters_dict['do_rm'] == 'T':
#            obs_RM_file_name = os.path.join(working_directory, 'rm.fits')
#            parameters_dict['obs_RM_file_name'] = obs_RM_file_name
#
#        if self.parameters_dict['do_dm'] == 'T':
#            obs_DM_file_name = os.path.join(working_directory,
#                                            'dm.fits')
#            parameters_dict['obs_DM_file_name'] = obs_DM_file_name
#
#        if self.parameters_dict['do_dust'] == 'T':
#            obs_dust_file_name = os.path.join(working_directory,
#                                              'IQU_dust.fits')
#            parameters_dict['obs_dust_file_name'] = obs_dust_file_name
#
#        if self.parameters_dict['do_tau'] == 'T':
#            obs_tau_file_name = os.path.join(working_directory,
#                                             'tau.fits')
#            parameters_dict['obs_tau_file_name'] = obs_tau_file_name
#
#        if self.parameters_dict['do_ff'] == 'T':
#            obs_ff_file_name = os.path.join(working_directory,
#                                            'free.fits')
#            parameters_dict['obs_ff_file_name'] = obs_ff_file_name
#
#        # ammend the parameters_dict
#        parameters_dict.update(self.parameters_dict)
#
#        # add custom parameters
#        parameters_dict.update(custom_parameters)
#
#        parameters_string = ''
#        for item in parameters_dict:
#            parameters_string += item + '=' + str(parameters_dict[item]) + '\n'
#
#        parameters_file_path = os.path.join(working_directory,
#                                            'parameters.txt')
#        with open(parameters_file_path, 'wb') as config_file:
#            config_file.write(parameters_string)
#
#
#
#
#    def _build_observables(self, temp_folder):
#        observables = {}
#        if self.parameters_dict['do_sync_emission'] == 'T':
#            [sync_I, sync_Q, sync_U] = self._read_fits_file(temp_folder,
#                                                            'IQU_sync.fits')
#            logger.debug('Read the sync_map')
#            observables['sync_observable'] = {'sync_I': sync_I,
#                                              'sync_Q': sync_Q,
#                                              'sync_U': sync_U}
#
#        if self.parameters_dict['do_rm'] == 'T':
#            [rm_map] = self._read_fits_file(temp_folder, 'rm.fits')
#            logger.debug('Read the rm_map')
#            observables['rm_observable'] = {'rm_map': rm_map}
#
#        if self.parameters_dict['do_dm'] == 'T':
#            [dm_map] = self._read_fits_file(temp_folder, 'dm.fits')
#            logger.debug('Read the dm_map')
#            observables['dm_observable'] = {'dm_map': dm_map}
#
#        if self.parameters_dict['do_dust'] == 'T':
#            [dust_I, dust_Q, dust_U] = self._read_fits_file(temp_folder,
#                                                            'IQU_dust.fits')
#            logger.debug('Read the dust_map')
#            observables['dust_observable'] = {'dust_I': dust_I,
#                                              'dust_Q': dust_Q,
#                                              'dust_U': dust_U}
#
#        if self.parameters_dict['do_tau'] == 'T':
#            [tau_map] = self._read_fits_file(temp_folder, 'tau.fits')
#            logger.debug('Read the tau_map')
#            observables['tau_observable'] = {'tau_map': tau_map}
#
#        if self.parameters_dict['do_ff'] == 'T':
#            [ff_map] = self._read_fits_file(temp_folder, 'free.fits')
#            logger.debug('Read the ff_map')
#            observables['ff_observable'] = {'ff_map': ff_map}
#
#        return observables
#
#############
#
#        if self.do_sync_emission:
#            result_observable['sync_emission'] = \
#                Field(domain=(ensemble_space, hp128, FieldArray((3,))))
#        if self.do_rm:
#            result_observable['rm'] = Field(domain=(ensemble_space, hp128))
#        if self.do_dm:
#            result_observable['dm'] = Field(domain=(ensemble_space, hp128,))
#        if self.do_dust:
#            result_observable['dust'] = \
#                Field(domain=(ensemble_space, hp128, FieldArray((3,))))
#        if self.do_tau:
#            result_observable['tau'] = Field(domain=(ensemble_space, hp128,))
#        if self.do_ff:
#            result_observable['ff'] = Field(domain=(ensemble_space, hp128,))
