# -*- coding: utf-8 -*-

from imagine.magnetic_fields.jaffe13_magnetic_field import Jaffe13MagneticField


class Jaffe13Mixin(object):
    def __init__(self, hammurabi_executable, conf_directory='./confs',
                 working_directory_base='.', nside=128):
        self.__parameter_dict = {'B_field_type': '10',
                                 'B_field_do_random': 'T',
                                 'B_analytic_beta': '0',
                                 'B_field_RMS_uG': '3.5',
                                 'B_field_interp': 'T',
                                 'use_B_analytic': 'F',
                                 'B_ran_mem_lim': '4',

                                 'bb_molr_aniso': 'T',
                                 'bb_ord_interarm': 'T',
                                 'bb_scale_coh_amps': 'T',
                                 'bb_scale_rms_amps': 'F',
                                 'bb_swap_cr0': 'T',  # SWAPS cr0 for 1/(1+cr0) for sampling
                                 }
        super(Jaffe13Mixin, self).__init__(hammurabi_executable,
                                           conf_directory,
                                           working_directory_base,
                                           nside)

    @property
    def magnetic_field_class(self):
        return Jaffe13MagneticField

    def _build_parameter_dict(self, parameter_dict, magnetic_field,
                              working_directory, local_ensemble_index):
        parameter_dict.update(self.__parameter_dict)

        parameter_dict.update(magnetic_field.parameters)

        super(Jaffe13Mixin, self)._build_parameter_dict(parameter_dict,
                                                        magnetic_field,
                                                        working_directory,
                                                        local_ensemble_index)
