# -*- coding: utf-8 -*-

import abc

from keepers import Loggable


class Prior(Loggable, object):
    @abc.abstractmethod
    def __call__(self, parameters):
        raise NotImplemented
