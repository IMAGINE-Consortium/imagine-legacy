# -*- coding: utf-8 -*-

from mixin_base import MixinBase


class SyncMixin(MixinBase):

    @property
    def __config_dict(self):
        return {'obs_name': 'sync',
                'component_names': ['sync_I', 'sync_Q', 'sync_U'],
                'parameter_dict_update': {'do_sync_emission': 'T'},
                'filename_key': 'obs_file_name',
                }

    def _initialize_observable_dict(self, *args, **kwargs):
        fat_kwargs = kwargs.copy()
        fat_kwargs.update({'config_dict': self.__config_dict})
        self._initialize_observable_dict_helper(*args, **fat_kwargs)
        super(SyncMixin, self)._initialize_observable_dict(*args, **kwargs)

    def _build_parameter_dict(self, *args, **kwargs):
        fat_kwargs = kwargs.copy()
        fat_kwargs.update({'config_dict': self.__config_dict})
        self._build_parameter_dict_helper(*args, **fat_kwargs)
        super(SyncMixin, self)._build_parameter_dict(*args, **kwargs)

    def _fill_observable_dict(self, *args, **kwargs):
        fat_kwargs = kwargs.copy()
        fat_kwargs.update({'config_dict': self.__config_dict})
        self._fill_observable_dict_helper(*args, **fat_kwargs)
        super(SyncMixin, self)._fill_observable_dict(*args, **kwargs)

    def _add_ensemble_mean(self, *args, **kwargs):
        fat_kwargs = kwargs.copy()
        fat_kwargs.update({'config_dict': self.__config_dict})
        self._add_ensemble_mean_helper(*args, **fat_kwargs)
        super(SyncMixin, self)._add_ensemble_mean(*args, **kwargs)
