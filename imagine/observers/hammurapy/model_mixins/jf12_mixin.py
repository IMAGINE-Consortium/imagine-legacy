# -*- coding: utf-8 -*-

from imagine.magnetic_fields.jf12_magnetic_field import JF12MagneticField


class JF12Mixin(object):
    @property
    def magnetic_field_class(self):
        return JF12MagneticField

    def _build_parameter_dict(self, parameter_dict, magnetic_field,
                              working_directory, local_ensemble_index):
        parameter_dict['B_field_type'] = '51'
        parameter_dict.update(magnetic_field.parameters)

        super(JF12Mixin, self)._build_parameter_dict(parameter_dict,
                                                     magnetic_field,
                                                     working_directory,
                                                     local_ensemble_index)
