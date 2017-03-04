# -*- coding: utf-8 -*-

import os

from nifty import Field, HPSpace


class DustMixin(object):
    def _initialize_observable_dict(self, observable_dict, magnetic_field):
        ensemble_space = magnetic_field.domain[0]
        hpSpace = HPSpace(nside=self.nside)

        for name in ['dust_I', 'dust_Q', 'dust_U']:
            observable_dict[name] = Field(domain=(ensemble_space, hpSpace),
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

        observable_dict['dust_I'].val.data[local_ensemble_index, :] = dust_I
        observable_dict['dust_Q'].val.data[local_ensemble_index, :] = dust_Q
        observable_dict['dust_U'].val.data[local_ensemble_index, :] = dust_U

        super(DustMixin, self)._fill_observable_dict(observable_dict,
                                                     working_directory,
                                                     local_ensemble_index)
