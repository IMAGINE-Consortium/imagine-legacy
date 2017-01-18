# -*- coding: utf-8 -*-

import abc
import numpy as np

from keepers import Loggable

from imagine.carrier_mapper import carrier_mapper

from magnetic_field import MagneticField


class MagneticFieldFactory(Loggable, object):

    def __init__(self, box_dimensions, resolution):
        self.box_dimensions = box_dimensions
        self.resolution = resolution
        self._initialize_parameter_defaults()
        self._initialize_variable_to_parameter_mappings()

    @abc.abstractproperty
    def descriptor(self):
        raise NotImplementedError

    def _initialize_parameter_defaults(self):
        self._parameter_defaults = {}

    def _initialize_variable_to_parameter_mappings(self):
        self._variable_to_parameter_mapping = {}

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

    def generate(self, variables):
        mapped_variables = self._map_variables_to_parameters(variables)
        work_parameters = self.parameter_defaults.copy()
        work_parameters.update(mapped_variables)

        result_magnetic_field = MagneticField(
                                          box_dimensions=self.box_dimensions,
                                          resolution=self.resolution,
                                          descriptor=self.descriptor,
                                          parameters=work_parameters)

        return result_magnetic_field
