# -*- coding: utf-8 -*-

from imagine.magnetic_fields.jf12_magnetic_field import JF12MagneticField


class JF12Mixin(object):
    def __init__(self, hammurabi_executable, conf_directory='./confs',
                 working_directory_base='.', nside=128):
        self.__parameter_dict = {'B_field_type': '7',
                                 'B_field_do_random': 'T',
                                 'B_analytic_beta': '1.36',
                                 'B_field_interp': 'T',
                                 'use_B_analytic': 'F',
                                 'B_ran_mem_lim': '4'}
        super(JF12Mixin, self).__init__(hammurabi_executable,
                                        conf_directory,
                                        working_directory_base,
                                        nside)

    @property
    def magnetic_field_class(self):
        return JF12MagneticField

    def _build_parameter_dict(self, parameter_dict, magnetic_field,
                              working_directory, local_ensemble_index):
        parameter_dict.update(self.__parameter_dict)

        parameter_dict.update(magnetic_field.parameters)

        super(JF12Mixin, self)._build_parameter_dict(parameter_dict,
                                                     magnetic_field,
                                                     working_directory,
                                                     local_ensemble_index)
