# -*- coding: utf-8 -*-

from imagine.likelihoods.likelihood import Likelihood

class EnsembleLikelihood(Likelihood):
    def __init__(self, measured_data, data_covariance):
        self.measured_data = measured_data
        self.data_covariance = data_covariance

    def __call__(self, observable):
        mean = observable.mean(spaces=0)
