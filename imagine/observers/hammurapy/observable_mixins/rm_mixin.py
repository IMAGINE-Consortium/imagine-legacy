# -*- coding: utf-8 -*-

import os

from nifty import Field, HPSpace


class RMMixin(object):
    def __init__(self, hammurabi_executable, conf_directory='./confs',
                 working_directory_base='.', nside=128):
        self.__hpSpace = HPSpace(nside=int(nside))
        super(RMMixin, self).__init__(hammurabi_executable,
                                      conf_directory,
                                      working_directory_base,
                                      nside)

    def _initialize_observable_dict(self, observable_dict, magnetic_field):
        ensemble_space = magnetic_field.domain[0]

        observable_dict['rm'] = Field(domain=(ensemble_space, self.__hpSpace),
                                      distribution_strategy='equal')
        super(RMMixin, self)._initialize_observable_dict(observable_dict,
                                                         magnetic_field)

    def _build_parameter_dict(self, parameter_dict, magnetic_field,
                              working_directory, local_ensemble_index):
        obs_RM_file_name = os.path.join(working_directory, 'rm.fits')
        parameter_dict['do_rm'] = 'T'
        parameter_dict['obs_RM_file_name'] = obs_RM_file_name
        super(RMMixin, self)._build_parameter_dict(parameter_dict,
                                                   magnetic_field,
                                                   working_directory,
                                                   local_ensemble_index)

    def _fill_observable_dict(self, observable_dict, working_directory,
                              local_ensemble_index):
        self.logger.debug('Reading RM-map.')
        [rm_map] = self._read_fits_file(path=working_directory,
                                        name='rm.fits',
                                        nside=self.nside)

        rm_field = observable_dict['rm']
        rm_field.val.data[local_ensemble_index] = rm_map

        super(RMMixin, self)._fill_observable_dict(observable_dict,
                                                   working_directory,
                                                   local_ensemble_index)
