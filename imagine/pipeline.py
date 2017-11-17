# -*- coding: utf-8 -*-

import os
import numpy as np

from scipy import optimize

from mpi4py import MPI

from keepers import Loggable

from imagine.likelihoods import Likelihood
from imagine.magnetic_fields import MagneticFieldFactory
from imagine.observers import Observer
from imagine.priors import Prior
from imagine import pymultinest
from imagine.sample import Sample

comm = MPI.COMM_WORLD
size = comm.size
rank = comm.rank

WORK_TAG = 0
DIE_TAG = 1


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
                 active_variables=[], ensemble_size=1,
                 pymultinest_parameters={}, sample_callback=None):
        self.logger.debug("Setting up pipeline.")
        self.magnetic_field_factory = magnetic_field_factory
        self.observer = observer
        self.likelihood = likelihood
        self.prior = prior
        self.active_variables = active_variables
        self.ensemble_size = ensemble_size
        self.likelihood_rescaler = 1.

        # setting defaults for pymultinest
        self.pymultinest_parameters = {'verbose': True,
                                       'n_iter_before_update': 1,
                                       'n_live_points': 100}
        self.pymultinest_parameters.update(pymultinest_parameters)

        self.sample_callback = sample_callback

        self.fixed_random_seed = None

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
        if not (isinstance(likelihood, list) or
                isinstance(likelihood, tuple)):
            likelihood = [likelihood]
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
        if not isinstance(prior, Prior):
            raise TypeError(
                "prior must be an instance of Prior-class.")
        self._prior = prior

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

        # heuristic for minimizers:
        # if a parameter value from outside of the cube is requested, return
        # the worst possible likelihood value
        if np.any(abs(cube_content) > 1.):
            return np.nan_to_num(-np.inf)

        if rank != 0:
            raise RuntimeError("_multinest_likelihood must only be called on "
                               "rank==0.")
        for i in xrange(1, size):
            comm.send(cube_content, dest=i, tag=WORK_TAG)
        self.logger.debug("Sent multinest-cube to nodes with rank > 0.")

        error_count = 0
        while error_count < 5:
            likelihood = self._core_likelihood(cube_content)
            if likelihood < 0:
                break
            else:
                self.logger.error("Positive log-likelihood value encountered!"
                                  "Redoing calculation.")
        return likelihood

    def _listen_for_likelihood_calls(self):
        status = MPI.Status()
        while True:
            cube = comm.recv(source=0, tag=MPI.ANY_TAG, status=status)
            if status == DIE_TAG:
                self.logger.debug("Received DIE_TAG from rank 0.")
                break
            self.logger.debug("Received cube from rank 0.")
            self._core_likelihood(cube)

    def _core_likelihood(self, cube):
        self.logger.debug("Beginning Likelihood-calculation for %s." %
                          str(cube))
        # translate cube to variables
        variables = {}
        for i, av in enumerate(self.active_variables):
            variables[av] = cube[i]

        # create magnetic field
        self.logger.debug("Creating magnetic field.")
        b_field = self.magnetic_field_factory.generate(
                                          variables=variables,
                                          ensemble_size=self.ensemble_size,
                                          random_seed=self.fixed_random_seed)

        # create observables
        self.logger.debug("Creating observables.")
        observables = self.observer(b_field)

        # add up individual log-likelihood terms
        self.logger.debug("Evaluating likelihood(s).")
        likelihood = ()
        total_likelihood = 0
        for like in self.likelihood:
            current_likelihood = like(observables)
            likelihood += (current_likelihood, )
            total_likelihood += current_likelihood

        self.logger.info("Evaluated likelihood: %f for %s" %
                         (total_likelihood, str(cube)))

        if self.sample_callback is not None:
            self.logger.debug("Creating sample-object.")
            sample = Sample(variables=variables,
                            magnetic_field=b_field,
                            observables=observables,
                            likelihood=likelihood,
                            total_likelihood=total_likelihood)
            self.sample_callback(sample)

        return total_likelihood * self.likelihood_rescaler

    def __call__(self):

        if rank == 0:
            # kickstart pymultinest
            self.logger.info("Starting pymultinest.")
            if not os.path.exists("chains"):
                os.mkdir("chains")
            pymultinest.run(self._multinest_likelihood,
                            self.prior,
                            len(self.active_variables),
                            **self.pymultinest_parameters)
            self.logger.info("pymultinest finished.")
            for i in xrange(1, size):
                self.logger.debug("Sending DIE_TAG to rank %i." % i)
                comm.send(None, dest=i, tag=DIE_TAG)
        else:
            # let all other nodes listen for likelihood evaluations
            self._listen_for_likelihood_calls()

    def find_minimum(self, starting_guess=None, method='Nelder-Mead',
                     **kwargs):
        if starting_guess is None:
            starting_guess = np.zeros(len(self.active_variables)) + 0.5

        if rank == 0:
            # kickstart pymultinest
            self.logger.info("Starting minimizer.")
            call_func = lambda z: -self._multinest_likelihood(
                                                 z,
                                                 len(self.active_variables),
                                                 len(self.active_variables))
            minimum = optimize.minimize(fun=call_func,
                                        x0=starting_guess,
                                        method=method,
                                        **kwargs)
            self.logger.info("Minimizer finished.")
            for i in xrange(1, size):
                self.logger.debug("Sending DIE_TAG to rank %i." % i)
                comm.send(None, dest=i, tag=DIE_TAG)
        else:
            minimum = None
            # let all other nodes listen for likelihood evaluations
            self._listen_for_likelihood_calls()
        minimum = comm.bcast(minimum, root=0)
        return minimum
