# -*- coding: utf-8 -*-

from keepers import Loggable

from likelihoods import Likelihood
from magnetic_fields import MagneticFieldFactory
from observers import Observer
from priors import Prior


class Pipeline(Loggable, object):
    """
    The pipeline
    - posses all the building blocks: magnetic_field, observer,
        likelihood and prior.
    - if multiple log-likelihoods and log-priors are given: sum the result
    - coordinates the repeated observation in order to compute an ensemble
    - controls which parameters of the magnetic field are tested
        (active parameters)


    """
    def __init__(self, magnetic_field_factory, observer, likelihood, prior,
                 active_variables=[], ensemble_size=1):
        self.logger.debug("Setting up pipeline.")
        self.magnetic_field_factory = magnetic_field_factory
        self.observer = observer
        self.likelihood = likelihood
        self.prior = prior
        self.active_variables = active_variables
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
        self.logger.debug("Setting likelihood.")
        self._likelihood = ()
        for l in likelihood:
            if not isinstance(l, Likelihood):
                raise TypeError(
                    "likelihood must be an instance of Likelihood-class.")
            self._likelihood += (l,)

    @property
    def prior(self):
        return self._prior

    @prior.setter
    def prior(self, prior):
        self.logger.debug("Setting prior.")
        self._prior = ()
        for p in prior:
            if not isinstance(p, Prior):
                raise TypeError(
                    "prior must be an instance of Prior-class.")
            self._prior += (p,)

    @property
    def magnetic_field_factory(self):
        return self._magnetic_field_factory

    @magnetic_field_factory.setter
    def magnetic_field_factory(self, magnetic_field_factory):
        if not isinstance(magnetic_field_factory, MagneticFieldFactory):
            raise TypeError(
                "magnetic_field_factory must be an instance of the "
                "MagneticFieldFactory-class.")
        self.logger.debug("Setting magnetic_field_factory.")
        self._magnetic_field_factory = magnetic_field_factory

    @property
    def active_variables(self):
        return self._active_variables

    @active_variables.setter
    def active_variables(self, active_variables):
        if not isinstance(active_variables, list):
            raise TypeError(
                    "active_variables must be a list.")
        self.logger.debug("Resetting active_variables to %s" %
                          str(active_variables))
        new_active = []
        for av in active_variables:
            new_active += [str(av)]
        self._active_variables = new_active

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

    def __call__(self, variables):
        pass
