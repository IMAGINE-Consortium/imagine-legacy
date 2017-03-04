# -*- coding: utf-8 -*-

import os

from nifty import Field, HPSpace


class SyncMixin(object):
    def _initialize_observable_dict(self, observable_dict, magnetic_field):
        ensemble_space = magnetic_field.domain[0]
        hpSpace = HPSpace(nside=self.nside)

        for name in ['sync_I', 'sync_Q', 'sync_U']:
            observable_dict[name] = Field(domain=(ensemble_space, hpSpace),
                                          distribution_strategy='equal')

        super(SyncMixin, self)._initialize_observable_dict(observable_dict,
                                                           magnetic_field)

    def _build_parameter_dict(self, parameter_dict, magnetic_field,
                              working_directory, local_ensemble_index):
        obs_sync_file_name = os.path.join(working_directory, 'IQU_sync.fits')
        parameter_dict['do_sync_emission'] = 'T'
        parameter_dict['obs_file_name'] = obs_sync_file_name
        super(SyncMixin, self)._build_parameter_dict(parameter_dict,
                                                     magnetic_field,
                                                     working_directory,
                                                     local_ensemble_index)

    def _fill_observable_dict(self, observable_dict, working_directory,
                              local_ensemble_index):
        self.logger.debug('Reading Sync-map.')
        [sync_I, sync_Q, sync_U] = self._read_fits_file(path=working_directory,
                                                        name='IQU_sync.fits',
                                                        nside=self.nside)

        observable_dict['sync_I'].val.data[local_ensemble_index, :] = sync_I
        observable_dict['sync_Q'].val.data[local_ensemble_index, :] = sync_Q
        observable_dict['sync_U'].val.data[local_ensemble_index, :] = sync_U

        super(SyncMixin, self)._fill_observable_dict(observable_dict,
                                                     working_directory,
                                                     local_ensemble_index)
