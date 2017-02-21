# -*- coding: utf-8 -*-

import abc

from keepers import Loggable


class Prior(Loggable, object):
    @abc.abstractmethod
    def __call__(self, cube, ndim, nparams):
        raise NotImplemented
