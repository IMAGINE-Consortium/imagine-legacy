# -*- coding: utf-8 -*-

from prior import Prior


class SumPrior(Prior):
    def __init__(self, priors):
        self.priors = []
        for prior in priors:
            assert isinstance(prior, Prior)
            self.priors += [prior]

    def __call__(self, parameters):
        prior = 0
        for current_prior in self.priors:
            prior += current_prior(parameters)
        return prior
