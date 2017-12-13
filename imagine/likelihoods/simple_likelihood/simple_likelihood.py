# -*- coding: utf-8 -*-

import numpy as np

from nifty import Field
from imagine.likelihoods.likelihood import Likelihood


class SimpleLikelihood(Likelihood):
    def __init__(self, measured_data, data_covariance=None):
        self.measured_data = measured_data
        if isinstance(data_covariance, Field):
            data_covariance = data_covariance.val.get_full_data()
        self.data_covariance = data_covariance

    def __call__(self, observable):
        data = self.measured_data
        obs_mean = observable.ensemble_mean().val.get_full_data()

        diff = data - obs_mean
        if self.data_covariance is not None:
            right = diff/self.data_covariance_operator
        else:
            right = diff
        return -0.5 * np.vdot(diff, right)
