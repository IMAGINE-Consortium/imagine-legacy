# -*- coding: utf-8 -*-

import os

from nifty import Field, HPSpace


class FFMixin(object):
    def __init__(self, hammurabi_executable, conf_directory='./confs',
                 working_directory_base='.', nside=128):
        self.__hpSpace = HPSpace(nside=int(nside))
        super(FFMixin, self).__init__(hammurabi_executable,
                                      conf_directory,
                                      working_directory_base,
                                      nside)
    def _initialize_observable_dict(self, observable_dict, magnetic_field):
        ensemble_space = magnetic_field.domain[0]

        observable_dict['ff'] = Field(domain=(ensemble_space, self.__hpSpace),
                                      distribution_strategy='equal')
        super(FFMixin, self)._initialize_observable_dict(observable_dict,
                                                         magnetic_field)

    def _build_parameter_dict(self, parameter_dict, magnetic_field,
                              working_directory, local_ensemble_index):
        obs_ff_file_name = os.path.join(working_directory, 'free.fits')
        parameter_dict['do_ff'] = 'T'
        parameter_dict['obs_ff_file_name'] = obs_ff_file_name
        super(FFMixin, self)._build_parameter_dict(parameter_dict,
                                                   magnetic_field,
                                                   working_directory,
                                                   local_ensemble_index)

    def _fill_observable_dict(self, observable_dict, working_directory,
                              local_ensemble_index):
        self.logger.debug('Reading FF-map.')
        [ff_map] = self._read_fits_file(path=working_directory,
                                        name='free.fits',
                                        nside=self.nside)

        ff_field = observable_dict['ff']
        ff_field.val.data[local_ensemble_index] = ff_map

        super(FFMixin, self)._fill_observable_dict(observable_dict,
                                                   working_directory,
                                                   local_ensemble_index)
