# -*- coding: utf-8 -*-

from keepers import Loggable


class Observer(Loggable, object):
    def __call__(magnetic_field):
        raise NotImplementedError
