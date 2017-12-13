# -*- coding: utf-8 -*-

import abc

from keepers import Loggable

from nifty import FieldArray


class Likelihood(Loggable, object):
    @abc.abstractmethod
    def __call__(self, observables):
        raise NotImplementedError

    def _strip_data(self, data):
        # if the first element in the domain tuple is a FieldArray we must
        # extract the data
        if isinstance(data.domain[0], FieldArray):
            data = data.val.get_full_data()[0]
        else:
            data = data.val.get_full_data()
        return data
