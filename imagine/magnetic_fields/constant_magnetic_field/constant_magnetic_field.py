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
