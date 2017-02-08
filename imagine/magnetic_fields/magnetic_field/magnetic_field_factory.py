# -*- coding: utf-8 -*-

import numpy as np

from keepers import Loggable

from imagine.carrier_mapper import carrier_mapper

from nifty import FieldArray, RGSpace

from magnetic_field import MagneticField


class MagneticFieldFactory(Loggable, object):

    def __init__(self, box_dimensions, resolution):
        self.box_dimensions = box_dimensions
        self.resolution = resolution
        self._parameter_defaults = self._initial_parameter_defaults
        self._variable_to_parameter_mappings = \
            self._initial_variable_to_parameter_mappings

    @property
    def box_dimensions(self):
        return self._box_dimensions

    @box_dimensions.setter
    def box_dimensions(self, box_dimensions):
        dim = tuple(np.array(box_dimensions, dtype=np.float))
        if len(dim) != 3:
            raise ValueError("Input of box_dimensions must have length three.")
        self._box_dimensions = dim

    @property
    def resolution(self):
        return self._resolution

    @resolution.setter
    def resolution(self, resolution):
        resolution = tuple(np.array(resolution, dtype=np.int))
        if len(resolution) != 3:
            raise ValueError("Input for resolution must have length three.")
        self._resolution = resolution

    @property
    def magnetic_field_class(self):
        return MagneticField

    @property
    def _initial_parameter_defaults(self):
        return {}

    @property
    def _initial_variable_to_parameter_mappings(self):
        return {}

    @staticmethod
    def _interval(mean, sigma, n):
        return [mean-n*sigma, mean, mean+n*sigma]

    @staticmethod
    def _positive_interval(mean, sigma, n):
        return [max(0, mean-n*sigma), mean, mean+n*sigma]

    @property
    def parameter_defaults(self):
        return self._parameter_defaults

    @parameter_defaults.setter
    def parameter_defaults(self, new_defaults):
        self._parameter_defaults.update((str(k), np.float(v))
                                        for k, v in new_defaults.items()
                                        if k in self._parameter_defaults)

    @property
    def variable_to_parameter_mappings(self):
        return self._variable_to_parameter_mappings

    @variable_to_parameter_mappings.setter
    def variable_to_parameter_mappings(self, new_mapping):
        """
        The parameter-mapping must be a dictionary with
        key: parameter-name
        value: [min, mean, max]
        """
        for k, v in new_mapping.items():
            if k in self._variable_to_parameter_mappings:
                key = str(k)
                value = [np.float(v[1]), np.float(v[2]), np.float(v[3])]
                self._variable_to_parameter_mappings.update((key, value))
                self.logger.debug("Updated variable_to_parameter_mapping %s "
                                  "to %s" % (key, str(value)))

    def _map_variables_to_parameters(self, variables):
        parameter_dict = {}
        for variable_name in variables:
            if variable_name in self.variable_to_parameter_mappings:
                mapping = self.variable_to_parameter_mappings[variable_name]
                mapped_variable = carrier_mapper(variables[variable_name],
                                                 a=mapping[0],
                                                 m=mapping[1],
                                                 b=mapping[2])
            else:
                mapped_variable = np.float(variables[variable_name])
            parameter_dict[variable_name] = mapped_variable
        return parameter_dict

    def generate(self, variables={}, ensemble_size=1):
        mapped_variables = self._map_variables_to_parameters(variables)
        work_parameters = self.parameter_defaults.copy()
        work_parameters.update(mapped_variables)

        distances = np.array(self.box_dimensions) / np.array(self.resolution)
        grid_space = RGSpace(shape=self.resolution,
                             distances=distances)
        ensemble = FieldArray(shape=(ensemble_size,))
        vector = FieldArray(shape=(3,))
        domain = (ensemble, grid_space, vector)

        result_magnetic_field = self.magnetic_field_class(
                                                  domain=domain,
                                                  parameters=work_parameters)

        return result_magnetic_field
