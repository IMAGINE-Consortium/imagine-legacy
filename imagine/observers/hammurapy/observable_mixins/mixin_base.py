# -*- coding: utf-8 -*-

from nifty import HPSpace

from imagine.observables import Observable


class MixinBase(object):
    def __init__(self, hammurabi_executable, input_directory='./input',
                 working_directory_base='.', nside=64):
        self.__hpSpace = HPSpace(nside=int(nside))
        super(MixinBase, self).__init__(hammurabi_executable,
                                        input_directory,
                                        working_directory_base,
                                        nside)

    @property
    def __config_dict(self):
        return {'obs_name': '',
                'component_names': [],
                'parameter_dict_update': {},
                }

    def _initialize_observable_dict(self, observable_dict, magnetic_field):
        super(MixinBase, self)._initialize_observable_dict(
                                            observable_dict, magnetic_field)

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
                              local_ensemble_index):
        super(MixinBase, self)._build_parameter_dict(parameter_dict,
                                                     magnetic_field,
                                                     local_ensemble_index)

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
