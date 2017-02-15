# -*- coding: utf-8 -*-

import os

from nifty import Field, HPSpace, FieldArray


class DustMixin(object):
    def _initialize_observable_dict(self, observable_dict, magnetic_field):
        ensemble_space = magnetic_field.domain[0]
        hpSpace = HPSpace(nside=self.nside)
        fieldArray = FieldArray((3,))

        observable_dict['dust'] = Field(domain=(ensemble_space, hpSpace,
                                                fieldArray),
                                        distribution_strategy='equal')
        super(DustMixin, self)._initialize_observable_dict(observable_dict,
                                                           magnetic_field)

    def _build_parameter_dict(self, parameter_dict, magnetic_field,
                              working_directory, local_ensemble_index):
        obs_dust_file_name = os.path.join(working_directory, 'IQU_dust.fits')
        parameter_dict['do_dust'] = 'T'
        parameter_dict['obs_dust_file_name'] = obs_dust_file_name
        super(DustMixin, self)._build_parameter_dict(parameter_dict,
                                                     magnetic_field,
                                                     working_directory,
                                                     local_ensemble_index)

    def _fill_observable_dict(self, observable_dict, working_directory,
                              local_ensemble_index):
        self.logger.debug('Reading Dust-map.')
        [dust_I, dust_Q, dust_U] = self._read_fits_file(path=working_directory,
                                                        name='IQU_dust.fits',
                                                        nside=self.nside)

        dust_field = observable_dict['dust']
        dust_field.val.data[local_ensemble_index, :, 0] = dust_I
        dust_field.val.data[local_ensemble_index, :, 1] = dust_Q
        dust_field.val.data[local_ensemble_index, :, 2] = dust_U

        super(DustMixin, self)._fill_observable_dict(observable_dict,
                                                     working_directory,
                                                     local_ensemble_index)
