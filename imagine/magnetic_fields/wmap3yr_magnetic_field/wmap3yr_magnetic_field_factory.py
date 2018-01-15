# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright(C) 2013-2017 Max-Planck-Society
#
# IMAGINE is being developed at the Max-Planck-Institut fuer Astrophysik
# and financially supported by the Studienstiftung des deutschen Volkes.

from imagine.magnetic_fields.magnetic_field.magnetic_field_factory \
    import MagneticFieldFactory

from wmap3yr_magnetic_field import WMAP3yrMagneticField


class WMAP3yrMagneticFieldFactory(MagneticFieldFactory):
    @property
    def magnetic_field_class(self):
        return WMAP3yrMagneticField

    @property
    def _initial_parameter_defaults(self):
        defaults = {'b0': 6.0,
                    'psi0': 27.0,
                    'psi1': 0.9,
                    'chi0': 25.0,
                    'random_rms': 2.0,
                    'random_rho': 0.5,
                    'random_a0': 1.7}
        return defaults

    @property
    def _initial_variable_to_parameter_mappings(self):
        return self._generate_variable_to_parameter_mapping_defaults(n=3)

    def _generate_variable_to_parameter_mapping_defaults(self, n):
        defaults = {
            'b0': self._positive_interval(6.0, 1.9, n),  # b0 astro-ph/0603450
            'psi0': self._positive_interval(27.0, 7.0, n),  # psi0 astro-ph/0603450
            'psi1': self._positive_interval(0.9, 5.0, n),  # psi1 astro-ph/0603450
            'chi0': self._positive_interval(25, 8.0, n),  # xsi0 astro-ph/0603450
            'random_rms': self._positive_interval(2.0, 0.6, n),
            'random_rho': self._positive_interval(0.5, 0.166, n),
            'random_a0': self._positive_interval(1.7, 0.5, n)
        }
        return defaults
