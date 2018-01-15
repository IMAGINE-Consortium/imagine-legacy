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

import xml.etree.ElementTree as et

from .observable_mixin import ObservableMixin


class SyncMixin(ObservableMixin):
    def __init__(self, frequency='23'):
        self.frequency = str(frequency)

    @property
    def obs_name(self):
        return 'sync_' + self.frequency

    @property
    def component_names(self):
        return ['sync_I_' + self.frequency,
                'sync_Q_' + self.frequency,
                'sync_U_' + self.frequency]

    def update_parameter_xml(self, root):
        element = et.Element('Sync', {'cue': '1',
                                      'freq': self.frequency,
                                      'filename': self.obs_name+'.fits'})
        output = root.find('Obsout')
        output.append(element)
