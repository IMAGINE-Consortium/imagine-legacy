# -*- coding: utf-8 -*-

import numpy as np

from imagine.likelihoods.likelihood import Likelihood


class SimpleLikelihood(Likelihood):
    def __init__(self, measured_data):
        self.measured_data = measured_data

    def __call__(self, observable):
        shape = observable.shape
        data = self.measured_data.val.get_full_data()
        obs = observable.val.get_full_data()

        quadratic_diff = ((data - obs).conjugate() * (data - obs)).sum()
        quadratic_diff /= np.prod(shape)

        return -quadratic_diff
