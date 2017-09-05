# -*- coding: utf-8 -*-

from imagine.magnetic_fields.magnetic_field.magnetic_field_factory \
    import MagneticFieldFactory

from wmap3yr_magnetic_field import WMAP3yrMagneticField


class WMAP3yrMagneticFieldFactory(MagneticFieldFactory):
    @property
    def magnetic_field_class(self):
        return WMAP3yrMagneticField

    @property
    def _initial_parameter_defaults(self):
        defaults = {
		'B_field_b0': 6,
		'B_field_psi0_deg': 27,
		'B_field_psi1_deg': 0.9,
		'B_field_xsi0_deg': 25
		}
        return defaults

    @property
    def _initial_variable_to_parameter_mappings(self):
        return self._generate_variable_to_parameter_mapping_defaults(n=3)

    def _generate_variable_to_parameter_mapping_defaults(self, n):
        defaults = {
		'B_field_b0': self._positive_interval(6.0, 2.0, n), # b0
		'B_field_psi0': self._positive_interval(27.0, 5.0, n), #psi0
		'B_field_psi1': self._positive_interval(0.9, 5.0, n), #psi1
		'B_field_xsi0': self._positive_interval(25, 5.0, n), #xsi0 
            }
        return defaults
