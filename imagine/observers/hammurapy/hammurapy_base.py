# -*- coding: utf-8 -*-

import abc
import os
import tempfile

import healpy

from nifty import Field, FieldArray, HPSpace

from imagine.magnetic_fields.magnetic_field import MagneticField
from imagine.observers.observer import Observer


class HammurapyBase(Observer):
    def __init__(self, hammurabi_executable, conf_directory='./confs',
                 working_directory='.'):
        self.hammurabi_executable = os.path.abspath(hammurabi_executable)
        self.conf_directory = os.path.abspath(conf_directory)
        self.working_directory = os.path.abspath(working_directory)

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
                                 'do_sync_emission': 'T',
                                 'do_rm': 'T',
                                 'do_dm': 'F',
                                 'do_dust': 'F',
                                 'do_tau': 'F',
                                 'do_ff': 'F'}

    @abc.abstractproperty
    def valid_magnetic_field_descriptor(self):
        return []

    def check_magnetic_field_descriptor(self, magnetic_field):
        for d in self.valid_magnetic_field_descriptor:
            if d not in magnetic_field.descriptor:
                raise TypeError(
                    "Given magnetic field does not match the "
                    "needed descriptor of Hammurapy-Class: "
                    "%s vs. %s" % (str(self.valid_magnetic_field_descriptor),
                                   str(magnetic_field.descriptor)))

    def _make_temp_folder(self):
        prefix = os.path.join(self.working_directory, 'temp_hammurabi_')
        return tempfile.mkdtemp(prefix=prefix)

###########

    def _make_parameter_file(self, working_directory, resolution, dimensions,
                             custom_parameters={}):

        # setup the default parameters
        parameters_dict = {'B_field_lx': dimensions[0],
                           'B_field_ly': dimensions[1],
                           'B_field_lz': dimensions[2],
                           'B_field_nx': int(resolution[0]),
                           'B_field_ny': int(resolution[1]),
                           'B_field_nz': int(resolution[2]),
                           }

        if self.parameters_dict['do_sync_emission'] == 'T':
            obs_sync_file_name = os.path.join(working_directory,
                                              'IQU_sync.fits')
            parameters_dict['obs_file_name'] = obs_sync_file_name

        if self.parameters_dict['do_rm'] == 'T':
            obs_RM_file_name = os.path.join(working_directory, 'rm.fits')
            parameters_dict['obs_RM_file_name'] = obs_RM_file_name

        if self.parameters_dict['do_dm'] == 'T':
            obs_DM_file_name = os.path.join(working_directory,
                                            'dm.fits')
            parameters_dict['obs_DM_file_name'] = obs_DM_file_name

        if self.parameters_dict['do_dust'] == 'T':
            obs_dust_file_name = os.path.join(working_directory,
                                              'IQU_dust.fits')
            parameters_dict['obs_dust_file_name'] = obs_dust_file_name

        if self.parameters_dict['do_tau'] == 'T':
            obs_tau_file_name = os.path.join(working_directory,
                                             'tau.fits')
            parameters_dict['obs_tau_file_name'] = obs_tau_file_name

        if self.parameters_dict['do_ff'] == 'T':
            obs_ff_file_name = os.path.join(working_directory,
                                            'free.fits')
            parameters_dict['obs_ff_file_name'] = obs_ff_file_name

        # ammend the parameters_dict
        parameters_dict.update(self.parameters_dict)

        # add custom parameters
        parameters_dict.update(custom_parameters)

        parameters_string = ''
        for item in parameters_dict:
            parameters_string += item + '=' + str(parameters_dict[item]) + '\n'

        parameters_file_path = os.path.join(working_directory,
                                            'parameters.txt')
        with open(parameters_file_path, 'wb') as config_file:
            config_file.write(parameters_string)




    def _build_observables(self, temp_folder):
        observables = {}
        if self.parameters_dict['do_sync_emission'] == 'T':
            [sync_I, sync_Q, sync_U] = self._read_fits_file(temp_folder,
                                                            'IQU_sync.fits')
            logger.debug('Read the sync_map')
            observables['sync_observable'] = {'sync_I': sync_I,
                                              'sync_Q': sync_Q,
                                              'sync_U': sync_U}

        if self.parameters_dict['do_rm'] == 'T':
            [rm_map] = self._read_fits_file(temp_folder, 'rm.fits')
            logger.debug('Read the rm_map')
            observables['rm_observable'] = {'rm_map': rm_map}

        if self.parameters_dict['do_dm'] == 'T':
            [dm_map] = self._read_fits_file(temp_folder, 'dm.fits')
            logger.debug('Read the dm_map')
            observables['dm_observable'] = {'dm_map': dm_map}

        if self.parameters_dict['do_dust'] == 'T':
            [dust_I, dust_Q, dust_U] = self._read_fits_file(temp_folder,
                                                            'IQU_dust.fits')
            logger.debug('Read the dust_map')
            observables['dust_observable'] = {'dust_I': dust_I,
                                              'dust_Q': dust_Q,
                                              'dust_U': dust_U}

        if self.parameters_dict['do_tau'] == 'T':
            [tau_map] = self._read_fits_file(temp_folder, 'tau.fits')
            logger.debug('Read the tau_map')
            observables['tau_observable'] = {'tau_map': tau_map}

        if self.parameters_dict['do_ff'] == 'T':
            [ff_map] = self._read_fits_file(temp_folder, 'free.fits')
            logger.debug('Read the ff_map')
            observables['ff_observable'] = {'ff_map': ff_map}

        return observables


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
            logger.warning('Could not delete %s', path)