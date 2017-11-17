# -*- coding: utf-8 -*-

from imagine.likelihoods.likelihood import Likelihood


class SimpleLikelihood(Likelihood):
    def __init__(self, measured_data, data_covariance_operator=None):
        self.measured_data = measured_data
        self.data_covariance_operator = data_covariance_operator

    def __call__(self, observable):
        data = self.measured_data.val.get_full_data()
        obs_mean = observable.ensemble_mean().val.get_full_data()

        diff = data - obs_mean
        if self.data_covariance_operator is not None:
            right = self.data_covariance_operator.inverse_times(diff)
        else:
            right = diff
        return -0.5 * diff.conjugate().vdot(right)
