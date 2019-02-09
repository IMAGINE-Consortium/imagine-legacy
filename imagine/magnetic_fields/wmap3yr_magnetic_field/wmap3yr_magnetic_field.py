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

from imagine.magnetic_fields.magnetic_field import MagneticField

class WMAP3yrMagneticField(MagneticField):

    @property
    def descriptor_lookup(self):
        lookup = {'b0': ['./MagneticField/Regular/WMAP/b0', 'value'],
                  'psi0': ['./MagneticField/Regular/WMAP/psi0', 'value'],
                  'psi1': ['./MagneticField/Regular/WMAP/psi1', 'value'],
                  'chi0': ['./MagneticField/Regular/WMAP/chi0', 'value'],
                  'random_rms': ['./MagneticField/Random/Global/ES/rms', 'value'],
                  'random_rho': ['./MagneticField/Random/Global/ES/rho', 'value'],
                  'random_a0': ['./MagneticField/Random/Global/ES/a0', 'value'],
                  'random_k0': ['./MagneticField/Random/Global/ES/k0', 'value'],
                  'random_r0': ['./MagneticField/Random/Global/ES/r0', 'value'],
                  'random_z0': ['./MagneticField/Random/Global/ES/z0', 'value']
                  }
        return lookup

    def _create_field(self):
        raise NotImplementedError
