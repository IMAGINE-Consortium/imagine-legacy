# -*- coding: utf-8 -*-

import numpy as np

from nifty import Field
from imagine.likelihoods.likelihood import Likelihood


class SimpleLikelihood(Likelihood):
    def __init__(self, observable_name, measured_data, data_covariance=None):
        self.observable_name = observable_name
        self.measured_data = self._strip_data(measured_data)
        if isinstance(data_covariance, Field):
            data_covariance = data_covariance.val.get_full_data()
        self.data_covariance = data_covariance

    def __call__(self, observable):
        data = self.measured_data
        field = observable[self.observable_name]
        obs_mean = field.ensemble_mean().val.get_full_data()

        diff = data - obs_mean
        if self.data_covariance is not None:
            right = diff/self.data_covariance
        else:
            right = diff
        return -0.5 * np.vdot(diff, right)
