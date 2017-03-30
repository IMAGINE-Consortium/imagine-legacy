# -*- coding: utf-8 -*-

from mixin_base import MixinBase


class DMMixin(MixinBase):

    @property
    def __config_dict(self):
        return {'obs_name': 'dm',
                'component_names': ['dm'],
                'parameter_dict_update': {'do_dm': 'T'},
                'filename_key': 'obs_DM_file_name',
                }

    def _initialize_observable_dict(self, *args, **kwargs):
        fat_kwargs = kwargs.copy()
        fat_kwargs.update({'config_dict': self.__config_dict})
        self._initialize_observable_dict_helper(*args, **fat_kwargs)
        super(DMMixin, self)._initialize_observable_dict(*args, **kwargs)

    def _build_parameter_dict(self, *args, **kwargs):
        fat_kwargs = kwargs.copy()
        fat_kwargs.update({'config_dict': self.__config_dict})
        self._build_parameter_dict_helper(*args, **fat_kwargs)
        super(DMMixin, self)._build_parameter_dict(*args, **kwargs)

    def _fill_observable_dict(self, *args, **kwargs):
        fat_kwargs = kwargs.copy()
        fat_kwargs.update({'config_dict': self.__config_dict})
        self._fill_observable_dict_helper(*args, **fat_kwargs)
        super(DMMixin, self)._fill_observable_dict(*args, **kwargs)

    def _add_ensemble_mean(self, *args, **kwargs):
        fat_kwargs = kwargs.copy()
        fat_kwargs.update({'config_dict': self.__config_dict})
        self._add_ensemble_mean_helper(*args, **fat_kwargs)
        super(DMMixin, self)._add_ensemble_mean(*args, **kwargs)
