# -*- coding: utf-8 -*-

import os

from nifty import Field, HPSpace, FieldArray


class SyncMixin(object):
    def _initialize_observable_dict(self, observable_dict, magnetic_field):
        ensemble_space = magnetic_field.domain[0]
        hpSpace = HPSpace(nside=self.nside)
        fieldArray = FieldArray((3,))

        observable_dict['sync'] = Field(domain=(ensemble_space, hpSpace,
                                                fieldArray),
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

        sync_field = observable_dict['sync']
        sync_field.val.data[local_ensemble_index, :, 0] = sync_I
        sync_field.val.data[local_ensemble_index, :, 1] = sync_Q
        sync_field.val.data[local_ensemble_index, :, 2] = sync_U

        super(SyncMixin, self)._fill_observable_dict(observable_dict,
                                                     working_directory,
                                                     local_ensemble_index)
