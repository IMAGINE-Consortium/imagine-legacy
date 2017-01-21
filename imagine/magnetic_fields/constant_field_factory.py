# -*- coding: utf-8 -*-

import numpy as np

from magnetic_field_factory import MagneticFieldFactory


class ConstantFieldFactory(MagneticFieldFactory):
    @property
    def descriptor(self):
        return 'CONSTANT_FIELD'

    @staticmethod
    def _create_array(self):
        result_array = np.empty(tuple(self.resolution) + (3,))
        result_array[:, :, :] = [self.parameters['b_x'],
                                 self.parameters['b_y'],
                                 self.parameters['b_z']]
        return result_array

    def _initialize_parameter_defaults(self):
        self._parameter_defaults = {'b_x': 0,
                                    'b_y': 0,
                                    'b_z': 0}

    def _initialize_variable_to_parameter_mappings(self):
        self._variable_to_parameter_mappings = {'b_x': [-np.inf, 0, np.inf],
                                                'b_y': [-np.inf, 0, np.inf],
                                                'b_z': [-np.inf, 0, np.inf]}
