# -*- coding: utf-8 -*-

import xml.etree.ElementTree as et

from .observable_mixin import ObservableMixin


class DMMixin(ObservableMixin):
    @property
    def obs_name(self):
        return 'dm'

    @property
    def component_names(self):
        return ['dm']

    def update_parameter_xml(self, root):
        element = et.Element('DM', {'cue': '1',
                                    'filename': self.obs_name+'.fits'})
        output = root.find('Output')
        output.append(element)
