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
        defaults = {'b0': 3.0,
                    'psi0': 27.0,
                    'psi1': 0.9,
                    'chi0': 25.0,
                    'random_rms': 1.0,
                    'random_rho': 0.5,
                    'random_a0': 1.7}
        return defaults

    @property
    def _initial_variable_to_parameter_mappings(self):
        return self._generate_variable_to_parameter_mapping_defaults(n=3)

    def _generate_variable_to_parameter_mapping_defaults(self, n):
        defaults = {
            'b0': self._positive_interval(3.0, 0.8, n),  # b0 astro-ph/0603450
            'psi0': self._positive_interval(27.0, 5.0, n),  # psi0 astro-ph/0603450
            'psi1': self._positive_interval(0.9, 5.0, n),  # psi1 astro-ph/0603450
            'chi0': self._positive_interval(25, 5.0, n),  # xsi0 astro-ph/0603450
            'random_rms': self._positive_interval(1.0, 0.3, n),
            'random_rho': self._positive_interval(0.5, 0.166, n),
            'random_a0': self._positive_interval(1.7, 0.3, n)
        }
        return defaults
