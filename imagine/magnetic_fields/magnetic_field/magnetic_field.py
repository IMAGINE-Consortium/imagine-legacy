# -*- coding: utf-8 -*-

import simplejson as json

import numpy as np

from nifty import Field, FieldArray, RGSpace


class MagneticField(Field):
    def __init__(self, parameters={}, domain=None, val=None, dtype=None,
                 distribution_strategy=None, copy=False, random_seed=None):

        super(MagneticField, self).__init__(
                                domain=domain,
                                val=val,
                                dtype=dtype,
                                distribution_strategy=distribution_strategy,
                                copy=copy)

        assert(len(self.domain) == 3)
        assert(isinstance(self.domain[0], FieldArray))
        assert(isinstance(self.domain[1], RGSpace))
        assert(isinstance(self.domain[2], FieldArray))

        self._parameters = {}
        for p in self.parameter_list:
            self._parameters[p] = np.float(parameters[p])

        casted_random_seed = np.empty(self.shape[0], dtype=np.int)
        if random_seed is None:
            random_seed = np.random.randint(np.uint32(-1)/3,
                                            size=self.shape[0])
        casted_random_seed[:] = random_seed
        self.random_seed = tuple(casted_random_seed)

    @property
    def parameter_list(self):
        return []

    @property
    def parameters(self):
        return self._parameters

    def set_val(self, new_val=None, copy=False):
        if new_val is not None:
            raise RuntimeError("Setting the field values explicitly is not "
                               "supported by MagneticField.")
        self._val = self._create_field()

    def _to_hdf5(self, hdf5_group):
        hdf5_group.attrs['_parameters'] = json.dumps(self._parameters)
        hdf5_group.create_dataset('random_seed', data=self.random_seed)
        return super(MagneticField, self)._to_hdf5(hdf5_group=hdf5_group)

    @classmethod
    def _from_hdf5(cls, hdf5_group, repository):
        new_field = super(MagneticField, cls)._from_hdf5(hdf5_group=hdf5_group,
                                                         repository=repository)
        new_field._parameters = json.loads(hdf5_group.attrs['_parameters'])
        new_field.random_seed = tuple(hdf5_group['random_seed'])
        return new_field
