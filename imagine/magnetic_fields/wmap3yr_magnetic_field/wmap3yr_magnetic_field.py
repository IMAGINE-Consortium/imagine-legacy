# -*- coding: utf-8 -*-

from imagine.magnetic_fields.magnetic_field import MagneticField


class WMAP3yrMagneticField(MagneticField):
    @property
    def parameter_list(self):
        parameter_list = ['B_field_b0',
                          'B_field_psi0_deg',
                          'B_field_psi1_deg',
                          'B_field_xsi0_deg',
                          'B_field_RMS_uG']
        return parameter_list

    def _create_field(self):
        raise NotImplementedError
