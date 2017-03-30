# -*- coding: utf-8 -*-


from nifty import Field, FieldArray


class Observable(Field):
    def __init__(self, domain=None, val=None, dtype=None,
                 distribution_strategy=None, copy=False):

        super(Observable, self).__init__(
                                domain=domain,
                                val=val,
                                dtype=dtype,
                                distribution_strategy=distribution_strategy,
                                copy=copy)

        assert(len(self.domain) == 2)
        assert(isinstance(self.domain[0], FieldArray))

    def ensemble_mean(self):
        try:
            self._ensemble_mean
        except(AttributeError):
            self._ensemble_mean = self.mean(spaces=0)
        finally:
            return self._ensemble_mean
