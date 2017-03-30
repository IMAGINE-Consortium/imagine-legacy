# -*- coding: utf-8 -*-

from mixin_base import MixinBase


class RMMixin(MixinBase):

    @property
    def __config_dict(self):
        return {'obs_name': 'rm',
                'component_names': ['rm'],
                'parameter_dict_update': {'do_rm': 'T'},
                'filename_key': 'obs_RM_file_name',
                }

    def _initialize_observable_dict(self, *args, **kwargs):
        fat_kwargs = kwargs.copy()
        fat_kwargs.update({'config_dict': self.__config_dict})
        self._initialize_observable_dict_helper(*args, **fat_kwargs)
        super(RMMixin, self)._initialize_observable_dict(*args, **kwargs)

    def _build_parameter_dict(self, *args, **kwargs):
        fat_kwargs = kwargs.copy()
        fat_kwargs.update({'config_dict': self.__config_dict})
        self._build_parameter_dict_helper(*args, **fat_kwargs)
        super(RMMixin, self)._build_parameter_dict(*args, **kwargs)

    def _fill_observable_dict(self, *args, **kwargs):
        fat_kwargs = kwargs.copy()
        fat_kwargs.update({'config_dict': self.__config_dict})
        self._fill_observable_dict_helper(*args, **fat_kwargs)
        super(RMMixin, self)._fill_observable_dict(*args, **kwargs)

    def _add_ensemble_mean(self, *args, **kwargs):
        fat_kwargs = kwargs.copy()
        fat_kwargs.update({'config_dict': self.__config_dict})
        self._add_ensemble_mean_helper(*args, **fat_kwargs)
        super(RMMixin, self)._add_ensemble_mean(*args, **kwargs)
