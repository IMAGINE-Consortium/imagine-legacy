# -*- coding: utf-8 -*-

import os
import numpy as np

from mpi4py import MPI

from keepers import Loggable

from likelihoods import Likelihood
from magnetic_fields import MagneticFieldFactory
from observers import Observer
from priors import Prior
from imagine.pymultinest import pymultinest

comm = MPI.COMM_WORLD
size = comm.size
rank = comm.rank


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

    def _multinest_likelihood(self, cube, ndim, nparams):
        cube_content = np.empty(ndim)
        for i in xrange(ndim):
            cube_content[i] = cube[i]
        if rank != 0:
            raise RuntimeError("_multinest_likelihood must only be called on "
                               "rank==0.")
        for i in xrange(1, size):
            comm.send(cube_content, dest=i)

        return self._core_likelihood(cube_content)

    def _listen_for_likelihood_calls(self):
        cube = comm.recv(obj=None, source=0)
        self._core_likelihood(cube)

    def _core_likelihood(self, cube):
        # translate cube to variables
        variables = {}
        for i, av in enumerate(self.active_variables):
            variables[av] = cube[i]

        # create magnetic field
        b_field = self.magnetic_field_factory(variables=variables,
                                              ensemble_size=self.ensemle_size)
        # create observables
        observables = self.observer(b_field)

        # add up individual log-likelihood terms
        likelihood = 0
        for like in self.likelihood:
            likelihood += like(observables)

        return likelihood

    def __call__(self, variables):

        if rank == 0:
            # kickstart pymultinest
            if not os.path.exists("chains"):
                os.mkdir("chains")
            pymultinest.run(self._multinest_likelihood,
                            self.prior,
                            len(self.active_variables),
                            verbose=True)
        else:
            # let all other nodes listen for likelihood evaluations
            self._listen_for_likelihood_calls()
