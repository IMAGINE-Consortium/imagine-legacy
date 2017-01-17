# -*- coding: utf-8 -*-

import numpy as np

from keepers import Loggable

from likelihoods import Likelihood
from observers import Observer
from priors import Prior

from carrier_mapper import carrier_mapper


class Pipeline(Loggable, object):
    def __init__(self, observer, likelihood, prior, ensemble_size=1,
                 active_parameters=[], parameter_mapping={}):
        self.logger.debug("Setting up pipeline.")
        self.observer = observer
        self.likelihood = likelihood
        self.prior = prior
        self.active_parameters = active_parameters
        self.parameter_mapping = parameter_mapping
        self.ensemble_size = ensemble_size

    @property
    def observer(self):
        return self._observer

    @observer.setter
    def observer(self, observer):
        if not isinstance(observer, Observer):
            raise TypeError("observer must be an instance of Observer-class.")
        self.logger.debug("Setting observer.")
        self._observer = observer

    @property
    def likelihood(self):
        return self._likelihood

    @likelihood.setter
    def likelihood(self, likelihood):
        if not isinstance(likelihood, Likelihood):
            raise TypeError(
                "likelihood must be an instance of likelihood-class.")

    @property
    def prior(self):
        return self._prior

    @prior.setter
    def prior(self, prior):
        if not isinstance(prior, Prior):
            raise TypeError(
                "prior must be an instance of prior-class.")

    @property
    def parameter_mapping(self):
        return self._parameter_mapping

    @parameter_mapping.setter
    def parameter_mapping(self, parameters):
        """
        The parameter-mapping must be a dictionary with
        key: parameter-name
        value: [min, mean, max]
        """
        new_mapping = {}
        for p in parameters:
            new_key = str(p[0])
            new_value = [p[1], p[2], p[3]]
            new_mapping[new_key] = new_value
            self.logger.debug("Setting parameter_mapping %s to %s." %
                              (new_key, new_mapping[new_key]))
        self._parameter_mapping = new_mapping

    @property
    def ensemble_size(self):
        return self._ensemble_size

    @ensemble_size.setter
    def ensemble_size(self, ensemble_size):

        ensemble_size = int(ensemble_size)
        if ensemble_size <= 0:
            raise ValueError("ensemble_size must be positive!")
        self.logger.debug("Setting ensemble size to %i." % ensemble_size)
        self._ensemble_size = ensemble_size

    def _map_parameters(self, parameter_list):
        parameter_dict = {}
        for i, name in enumerate(self.active_parameters):
            if name in self.parameter_mapping:
                mapping = self.parameter_mapping[name]
                mapped_parameter = carrier_mapper(parameter_list[i],
                                                  a=mapping[1],
                                                  m=mapping[2],
                                                  b=mapping[3])
            else:
                mapped_parameter = np.float(parameter_list[i])
            parameter_dict[name] = mapped_parameter
        return parameter_dict

    def __call__(self, parameter_list):
        mapped_parameters = self._map_parameters(parameter_list)
