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

import numpy as np
from imagine.magnetic_fields.magnetic_field.magnetic_field_factory import MagneticFieldFactory
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
        return {'b_x': [-100, 0, 100],
                'b_y': [-100, 0, 100],
                'b_z': [-100, 0, 100]}
