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

from .magnetic_field_model import MagneticFieldModel
from imagine.magnetic_fields.wmap3yr_magnetic_field import WMAP3yrMagneticField


class WMAP3yrMixin(MagneticFieldModel):
    def update_parameter_xml(self, root):
        custom_parameters = [
                ['./MagneticField/Regular', 'type', 'WMAP'],
                ['./MagneticField/Random', 'cue', '1'],
                ['./MagneticField/Random', 'type', 'Global']]
        for parameter in custom_parameters:
            root.find(parameter[0]).set(parameter[1], str(parameter[2]))

    @property
    def magnetic_field_class(self):
        return WMAP3yrMagneticField
