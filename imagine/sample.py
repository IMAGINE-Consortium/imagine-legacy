# -*- coding: utf-8 -*-

import simplejson as json

import numpy as np

from keepers import Loggable,\
                    Versionable

from nifty import Field
from imagine.magnetic_fields import MagneticField


class Sample(Loggable, Versionable, object):
    def __init__(self, variables=None, magnetic_field=None, observables=None,
                 likelihood=None, total_likelihood=None):
        self.variables = variables
        self.magnetic_field = magnetic_field
        self.observables = observables
        self.likelihood = likelihood
        self.total_likelihood = total_likelihood

    @property
    def variables(self):
        return self._variables

    @variables.setter
    def variables(self, variables):
        self._variables = variables

    @property
    def magnetic_field(self):
        return self._magnetic_field

    @magnetic_field.setter
    def magnetic_field(self, magnetic_field):
        if not isinstance(magnetic_field, MagneticField):
            raise TypeError("Input must be a MagneticField instance.")
        self._magnetic_field = magnetic_field

    @property
    def observables(self):
        return self._observables

    @observables.setter
    def observables(self, observables):
        parsed_observables = {}
        if not isinstance(observables, dict):
            raise TypeError("Input must be a dict.")
        for key, value in observables.iteritems():
            if not isinstance(key, str):
                raise TypeError("Observable name must be a string.")
            if not isinstance(value, Field):
                raise TypeError("Observable must be a NIFTy-Field.")
            parsed_observables[key] = value
        self._observables = parsed_observables

    @property
    def likelihood(self):
        return self._likelihood

    @likelihood.setter
    def likelihood(self, likelihood):
        if np.isscalar(likelihood):
            likelihood = (likelihood, )
        else:
            likelihood = tuple(likelihood)
        self._likelihood = likelihood

    @property
    def total_likelihood(self):
        return self._total_likelihood

    @total_likelihood.setter
    def total_likelihood(self, total_likelihood):
        self._total_likelihood = np.float(total_likelihood)

    def _to_hdf5(self, hdf5_group):
        if self._variables is not None:
            hdf5_group.attrs['variables'] = json.dumps(self._variables)

        if self._likelihood is not None:
            hdf5_group['likelihood'] = self._likelihood

        if self._total_likelihood is not None:
            hdf5_group.attrs['total_likelihood'] = self._total_likelihood

        return_dict = {}
        if self._magnetic_field is not None:
            return_dict['magnetic_field'] = self._magnetic_field

        if self._observables is not None:
            hdf5_group.attrs['observable_names'] = \
                            json.dumps(self._observables.keys())
            return_dict.update(self._observables)

        return return_dict

    @classmethod
    def _from_hdf5(cls, hdf5_group, repository):
        new_sample = cls()
        try:
            variables = hdf5_group.attrs['variables']
            new_sample._variables = json.loads(variables)
        except(KeyError):
            pass

        try:
            new_sample._likelihood = tuple(hdf5_group['likelihood'])
        except(KeyError):
            pass

        try:
            new_sample._total_likelihood = hdf5_group.attrs['total_likelihood']
        except(KeyError):
            pass

        try:
            magnetic_field = repository.get('magnetic_field', hdf5_group)
            new_sample._magnetic_field = magnetic_field
        except(KeyError):
            pass

        try:
            observable_names = hdf5_group.attrs['observable_names']
            observable_names = json.loads(observable_names)
        except(KeyError):
            pass
        else:
            observables = {}
            for name in observable_names:
                observables[name] = repository.get(name, hdf5_group)
            new_sample._observables = observables

        return new_sample
