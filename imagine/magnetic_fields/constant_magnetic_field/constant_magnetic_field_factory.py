# -*- coding: utf-8 -*-

import numpy as np

from imagine.magnetic_fields.magnetic_field.magnetic_field_factory \
    import MagneticFieldFactory

from constant_magnetic_field import ConstantMagneticField


class ConstantMagneticFieldFactory(MagneticFieldFactory):
    @property
    def magnetic_field_class(self):
        return ConstantMagneticField

    @property
    def _initial_parameter_defaults(self):
        defaults = {'b_x': 0,
                    'b_y': 0,
                    'b_z': 0}
        return defaults

    @property
    def _initial_variable_to_parameter_mappings(self):
        return {'b_x': [-np.inf, 0, np.inf],
                'b_y': [-np.inf, 0, np.inf],
                'b_z': [-np.inf, 0, np.inf]}
