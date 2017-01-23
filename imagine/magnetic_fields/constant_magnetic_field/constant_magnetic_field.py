# -*- coding: utf-8 -*-

import numpy as np

from nifty import RGSpace, Field, FieldArray

from imagine.magnetic_fields.magnetic_field import MagneticField


class ConstantMagneticField(MagneticField):
    @property
    def parameter_list(self):
        parameter_list = ['b_x', 'b_y', 'b_z']
        return parameter_list

    def _create_field(self):
        distances = np.array(self.box_dimensions)/np.array(self.resolution)
        space = RGSpace(shape=self.resolution,
                        distances=distances)
        field_array = FieldArray(shape=(3,), dtype=np.float)

        result_field = Field(domain=space, field_type=field_array)
        result_field.val[:, :, :, 0] = self.parameters['b_x']
        result_field.val[:, :, :, 1] = self.parameters['b_y']
        result_field.val[:, :, :, 2] = self.parameters['b_z']

        return result_field
