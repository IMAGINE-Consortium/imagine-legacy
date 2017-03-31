# -*- coding: utf-8 -*-

import os

import numpy as np

from mpi4py import MPI

from d2o import distributed_data_object

from nifty import HPSpace

from imagine.observables import Observable


class MixinBase(object):
    def __init__(self, hammurabi_executable, conf_directory='./confs',
                 working_directory_base='.', nside=128,
                 analytic_ensemble_mean=False):
        self.__hpSpace = HPSpace(nside=int(nside))
        super(MixinBase, self).__init__(hammurabi_executable,
                                        conf_directory,
                                        working_directory_base,
                                        nside,
                                        analytic_ensemble_mean)

    @property
    def __config_dict(self):
        return {'obs_name': '',
                'component_names': [],
                'parameter_dict_update': {},
                'filename_key': '',
                }

    def _initialize_observable_dict(self, observable_dict, magnetic_field):
        super(MixinBase, self)._initialize_observable_dict(observable_dict,
                                                           magnetic_field)

    def _initialize_observable_dict_helper(self, observable_dict,
                                           magnetic_field, config_dict):
        component_names = config_dict['component_names']

        ensemble_space = magnetic_field.domain[0]
        for component in component_names:
            # It is important to initialize the Observables with an explicit
            # value. Otherwise the d2o will not instantaneuosly be created
            # (c.f. lazy object creation).
            observable_dict[component] = Observable(
                                    val=0,
                                    domain=(ensemble_space, self.__hpSpace),
                                    distribution_strategy='equal')

    def _build_parameter_dict(self, parameter_dict, magnetic_field,
                              working_directory, local_ensemble_index):
        super(MixinBase, self)._build_parameter_dict(parameter_dict,
                                                     magnetic_field,
                                                     working_directory,
                                                     local_ensemble_index)

    def _build_parameter_dict_helper(self, parameter_dict, magnetic_field,
                                     working_directory, local_ensemble_index,
                                     config_dict):
        obs_name = config_dict['obs_name']
        parameter_dict_update = config_dict['parameter_dict_update']
        filename_key = config_dict['filename_key']

        obs_file_name = os.path.join(working_directory, obs_name + '.fits')
        parameter_dict[filename_key] = obs_file_name
        parameter_dict.update(parameter_dict_update)

    def _fill_observable_dict(self, observable_dict, working_directory,
                              local_ensemble_index):
        super(MixinBase, self)._fill_observable_dict(observable_dict,
                                                     working_directory,
                                                     local_ensemble_index)

    def _fill_observable_dict_helper(self, observable_dict, working_directory,
                                     local_ensemble_index, config_dict):
        obs_name = config_dict['obs_name']
        component_names = config_dict['component_names']

        self.logger.debug('Reading %s-map.' % obs_name)
        map_list = self._read_fits_file(path=working_directory,
                                        name=obs_name + '.fits',
                                        nside=self.nside)

        for i, map_component in enumerate(map_list):
            temp_obs = observable_dict[component_names[i]]
            temp_obs.val.data[local_ensemble_index] = map_component

    def _add_ensemble_mean(self, observable_dict, working_directory):
        super(MixinBase, self)._add_ensemble_mean(observable_dict,
                                                  working_directory)

    def _add_ensemble_mean_helper(self, observable_dict, working_directory,
                                  config_dict):

        obs_name = config_dict['obs_name']
        component_names = config_dict['component_names']

        dummy_obs_field = observable_dict[component_names[0]]
        comm = dummy_obs_field.val.comm
        rank = comm.rank
        size = comm.size

        if rank + 1 == size:
            self.logger.debug('Reading %s-ensemble-mean.' % obs_name)
            mean_list = self._read_fits_file(path=working_directory,
                                             name=obs_name + '.fits',
                                             nside=self.nside)

        else:
            mean_list = []
            for component in component_names:
                mean_list += [np.empty(dummy_obs_field.domain[1].shape,
                                       dtype=np.float64)]

        for i, component in enumerate(component_names):
            comm.Bcast([mean_list[i], MPI.DOUBLE], root=size-1)

            obs_field = observable_dict[component]
            # at the moment the code is hardwired to np.float64
            assert(obs_field.dtype == np.float64)

            # put the array into a d2o
            mean_obj = distributed_data_object(global_data=mean_list[i],
                                               dtype=np.float64,
                                               distribution_strategy='not',
                                               comm=comm,
                                               copy=False,
                                               )
            obs_field._ensemble_mean = mean_obj
