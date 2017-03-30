# -*- coding: utf-8 -*-

from imagine.magnetic_fields.magnetic_field.magnetic_field_factory \
    import MagneticFieldFactory

from galmag_field import GalMagField


class GalMagFieldFactory(MagneticFieldFactory):
    @property
    def magnetic_field_class(self):
        return GalMagField

    @property
    def _initial_parameter_defaults(self):
        defaults = {'b_x': 0,
                    'b_y': 0,
                    'b_z': 0}
        return defaults

    @property
    def _initial_variable_to_parameter_mappings(self):
        return {'b_x': [-100, 0, 100],
                'b_y': [-100, 0, 100],
                'b_z': [-100, 0, 100]}
