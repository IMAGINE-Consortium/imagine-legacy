# -*- coding: utf-8 -*-

import numpy as np

from keepers import Loggable

from likelihoods import Likelihood
from observers import Observer
from priors import Prior


class Pipeline(Loggable, object):
    def __init__(self, observer, likelihood, prior,
                 parameters=[], ensemble_size=1):
        self.logger.debug("Setting up pipeline.")
        self.observer = observer
        self.likelihood = likelihood
        self.prior = prior
        self.parameters = parameters
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
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        """
        parameters is either a list of the parameter-names, or a list of lists
        containing [parameter-name, min, max, mean]
        """
        new_parameters = []
        for p in parameters:
            if isinstance(p, list):
                new_parameters += [[str(p[0]), p[1], p[2], p[3]]]
            else:
                new_parameters += [[str(p), None, None, None]]
        self.logger.debug("Setting parameters to %s." % str(new_parameters))
        self._parameters = new_parameters

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

    @staticmethod
    def carrier_mapper(x, a=-np.inf, b=np.inf, m=0):
        """
        Maps x from [-inf, inf] into the interval [a, b], where x=0 -> m
        """

        if a == -np.inf and b == np.inf and m == 0:
            return x

        x = np.float(x)
        a = np.float(a)
        b = np.float(b)
        if m is None:
            if a == -np.inf and b == np.inf:
                m = 0
            else:
                m = a + (b-a)/2.
        else:
            m = np.float(m)

        # map x from [-inf, inf] to [0, 1]
        y = np.arctan(x)/np.pi + 0.5
        # compute where m would lie in [0, 1]
        n = (m - a)/(b - a)
        # strech y, such that x=0 -> n
        y = y**np.emath.logn(0.5, n)
        # strech y to the interval [a,b]
        y = y*(b-a) + a
        return y

    def __call__(self, parameter_list):
        parameter_dict = {}
        for (i, p) in enumerate(self.parameters):
            parameter_dict[p[0]] = self.carrier_mapper(parameter_list[i],
                                                       a=p[1],
                                                       b=p[2],
                                                       m=p[3])












