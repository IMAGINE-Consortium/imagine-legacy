# -*- coding: utf-8 -*-

import os

from nifty import Field, HPSpace


class DMMixin(object):
    def _initialize_observable_dict(self, observable_dict, magnetic_field):
        ensemble_space = magnetic_field.domain[0]
        hpSpace = HPSpace(nside=self.nside)

        observable_dict['dm'] = Field(domain=(ensemble_space, hpSpace),
                                      distribution_strategy='equal')
        super(DMMixin, self)._initialize_observable_dict(observable_dict,
                                                         magnetic_field)

    def _build_parameter_dict(self, parameter_dict, magnetic_field,
                              working_directory, local_ensemble_index):
        obs_DM_file_name = os.path.join(working_directory, 'dm.fits')
        parameter_dict['do_dm'] = 'T'
        parameter_dict['obs_DM_file_name'] = obs_DM_file_name
        super(DMMixin, self)._build_parameter_dict(parameter_dict,
                                                   magnetic_field,
                                                   working_directory,
                                                   local_ensemble_index)

    def _fill_observable_dict(self, observable_dict, working_directory,
                              local_ensemble_index):
        self.logger.debug('Reading DM-map.')
        [dm_map] = self._read_fits_file(path=working_directory,
                                        name='dm.fits',
                                        nside=self.nside)

        dm_field = observable_dict['dm']
        dm_field.val.data[local_ensemble_index] = dm_map

        super(DMMixin, self)._fill_observable_dict(observable_dict,
                                                   working_directory,
                                                   local_ensemble_index)
