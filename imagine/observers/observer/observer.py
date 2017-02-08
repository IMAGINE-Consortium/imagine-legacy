# -*- coding: utf-8 -*-

from keepers import Loggable


class Observer(Loggable, object):
    def observe(magnetic_field):
        raise NotImplementedError
