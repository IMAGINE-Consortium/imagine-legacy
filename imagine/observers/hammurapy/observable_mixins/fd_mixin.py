# -*- coding: utf-8 -*-

from mixin_base import MixinBase


class FDMixin(MixinBase):

    @property
    def __config_dict(self):
        return {'obs_name': 'fd',
                'component_names': ['fd'],
                'parameter_dict_update': {('./Output/Faraday', 'cue'): '1'},
                }

    def _initialize_observable_dict(self, observable_dict, magnetic_field):
        self._initialize_observable_dict_helper(observable_dict,
                                                magnetic_field,
                                                self.__config_dict)
        super(FDMixin, self)._initialize_observable_dict(
                                            observable_dict, magnetic_field)

    def _build_parameter_dict(self, parameter_dict, magnetic_field,
                              local_ensemble_index):
        parameter_dict.update(self.__config_dict['parameter_dict_update'])
        super(FDMixin, self)._build_parameter_dict(parameter_dict,
                                                   magnetic_field,
                                                   local_ensemble_index)

    def _fill_observable_dict(self, observable_dict, working_directory,
                              local_ensemble_index):
        self._fill_observable_dict_helper(observable_dict,
                                          working_directory,
                                          local_ensemble_index,
                                          self.__config_dict)
        super(FDMixin, self)._fill_observable_dict(observable_dict,
                                                   working_directory,
                                                   local_ensemble_index)
