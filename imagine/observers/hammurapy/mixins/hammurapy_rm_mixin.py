# -*- coding: utf-8 -*-

import os

from nifty import Field, HPSpace


class HammurapyRMMixin(object):
    def _initialize_observable_dict(self, observable_dict, magnetic_field):
        ensemble_space = magnetic_field.domain[0]
        hp128 = HPSpace(nside=128)

        observable_dict['rm'] = Field(domain=(ensemble_space, hp128),
                                      distribution_strategy='equal')
        super(HammurapyRMMixin, self)._initialize_observable_dict(
                                                             observable_dict,
                                                             magnetic_field)

    def _build_parameter_dict(self, parameter_dict, magnetic_field,
                              working_directory, local_ensemble_index):
        obs_RM_file_name = os.path.join(working_directory, 'rm.fits')
        parameter_dict['do_rm'] = 'T'
        parameter_dict['obs_RM_file_name'] = obs_RM_file_name
        super(HammurapyRMMixin, self)._build_parameter_dict(
                                                        parameter_dict,
                                                        magnetic_field,
                                                        working_directory,
                                                        local_ensemble_index)

    def _fill_observable_dict(self, observable_dict, working_directory,
                              local_ensemble_index):
        self.logger.debug('Reading RM-map.')
        [rm_map] = self._read_fits_file(working_directory, 'rm.fits')

        rm_field = observable_dict['rm']
        rm_field.val.data[local_ensemble_index] = rm_map

        super(HammurapyRMMixin, self)._fill_observable_dict(
                                                        observable_dict,
                                                        working_directory,
                                                        local_ensemble_index)
