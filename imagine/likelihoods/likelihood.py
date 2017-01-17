# -*- coding: utf-8 -*-

import abc

from keepers import Loggable


class Likelihood(Loggable, object):
    @abc.abstractmethod
    def __call__(self, observables):
        raise NotImplementedError
