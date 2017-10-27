# -*- coding: utf-8 -*-

import xml.etree.ElementTree as et

from .observable_mixin import ObservableMixin


class FDMixin(ObservableMixin):
    @property
    def obs_name(self):
        return 'fd'

    @property
    def component_names(self):
        return ['fd']

    def update_parameter_xml(self, root):
        element = et.Element('Faraday', {'cue': '1',
                                         'filename': self.obs_name+'.fits'})
        output = root.find('Output')
        output.append(element)
