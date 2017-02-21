# -*- coding: utf-8 -*-

from imagine.priors.prior import Prior


class FlatPrior(Prior):
    def __call__(self, cube, ndim, nparams):
        return cube
