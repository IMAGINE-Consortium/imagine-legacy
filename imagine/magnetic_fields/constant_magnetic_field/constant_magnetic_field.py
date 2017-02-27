# -*- coding: utf-8 -*-

from imagine.magnetic_fields.magnetic_field import MagneticField


class ConstantMagneticField(MagneticField):
    @property
    def parameter_list(self):
        parameter_list = ['b_x', 'b_y', 'b_z']
        return parameter_list

    def _create_field(self):
        val = self.cast(None)
        val[:, :, :, :, 0] = self.parameters['b_x']
        val[:, :, :, :, 1] = self.parameters['b_y']
        val[:, :, :, :, 2] = self.parameters['b_z']
        return val
