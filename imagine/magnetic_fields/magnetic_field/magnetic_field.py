# -*- coding: utf-8 -*-

import numpy as np

from keepers import Loggable


class MagneticField(Loggable, object):
    def __init__(self, box_dimensions, resolution, parameters):

        self._box_dimensions = np.empty(3)
        self._box_dimensions[:] = box_dimensions
        self._box_dimensions = tuple(self._box_dimensions)

        self._resolution = np.empty(3)
        self._resolution[:] = resolution
        self._resolution = tuple(self._resolution)

        self._parameters = {}
        for p in self.parameter_list:
            self._parameters[p] = np.float(parameters[p])

    @property
    def parameter_list(self):
        return []

    @property
    def parameters(self):
        return self._parameters

    @property
    def field(self):
        if self._field is None:
            self._field = self._create_field()
        return self._field

    def _create_field(self):
        raise NotImplementedError

    @property
    def box_dimensions(self):
        return self._box_dimensions

    @property
    def resolution(self):
        return self._resolution

    @property
    def descriptor(self):
        return self._descriptor
