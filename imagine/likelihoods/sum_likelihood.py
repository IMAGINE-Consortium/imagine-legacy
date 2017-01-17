# -*- coding: utf-8 -*-

from likelihood import Likelihood


class SumLikelihood(Likelihood):
    def __init__(self, likelihoods):
        self.likelihoods = []
        for likelihood in likelihoods:
            assert isinstance(likelihood, Likelihood)
            self.likelihoods += [likelihood]

    def __call__(self, observables):
        likelihood = 0
        for current_likelihood in self.likelihoods:
            likelihood += current_likelihood(observables)

        return likelihood
