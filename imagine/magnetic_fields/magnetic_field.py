# -*- coding: utf-8 -*-

import types

import numpy as np

from keepers import Loggable


class MagneticField(Loggable, object):
    def __init__(self, box_dimensions, resolution, descriptor,
                 parameters={}, create_array=None):

        self._box_dimensions = np.empty(3)
        self._box_dimensions[:] = box_dimensions
        self._resolution = np.empty(3)
        self._resolution[:] = resolution
        self._descriptor = descriptor

        self._parameters = {}
        for (key, value) in parameters.items():
            self._parameters[str(key)] = np.float(value)

        self._array = None
        if create_array is not None:
            self._create_array = types.MethodType(create_array, self)

    @property
    def parameters(self):
        return self._parameters

    @property
    def box_dimensions(self):
        return self._box_dimensions

    @property
    def resolution(self):
        return self._resolution

    @property
    def descriptor(self):
        return self._descriptor

    @property
    def array(self):
        if self._array is None:
            self._array = self._create_array()
        return self._array

    def _create_array(self):
        raise NotImplementedError
