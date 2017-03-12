# -*- coding: utf-8 -*-

import os

from nifty import Field, HPSpace


class TauMixin(object):
    def __init__(self, hammurabi_executable, conf_directory='./confs',
                 working_directory_base='.', nside=128):
        self.__hpSpace = HPSpace(nside=int(nside))
        super(TauMixin, self).__init__(hammurabi_executable,
                                       conf_directory,
                                       working_directory_base,
                                       nside)
    def _initialize_observable_dict(self, observable_dict, magnetic_field):
        ensemble_space = magnetic_field.domain[0]

        observable_dict['tau'] = Field(domain=(ensemble_space, self.__hpSpace),
                                       distribution_strategy='equal')
        super(TauMixin, self)._initialize_observable_dict(observable_dict,
                                                          magnetic_field)

    def _build_parameter_dict(self, parameter_dict, magnetic_field,
                              working_directory, local_ensemble_index):
        obs_tau_file_name = os.path.join(working_directory, 'tau.fits')
        parameter_dict['do_tau'] = 'T'
        parameter_dict['obs_tau_file_name'] = obs_tau_file_name
        super(TauMixin, self)._build_parameter_dict(parameter_dict,
                                                    magnetic_field,
                                                    working_directory,
                                                    local_ensemble_index)

    def _fill_observable_dict(self, observable_dict, working_directory,
                              local_ensemble_index):
        self.logger.debug('Reading Tau-map.')
        [tau_map] = self._read_fits_file(path=working_directory,
                                         name='tau.fits',
                                         nside=self.nside)

        tau_field = observable_dict['tau']
        tau_field.val.data[local_ensemble_index] = tau_map

        super(TauMixin, self)._fill_observable_dict(observable_dict,
                                                    working_directory,
                                                    local_ensemble_index)
