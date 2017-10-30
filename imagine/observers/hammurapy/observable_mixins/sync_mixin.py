# -*- coding: utf-8 -*-

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
        output = root.find('Output')
        output.append(element)
