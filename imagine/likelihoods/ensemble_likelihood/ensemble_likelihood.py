# -*- coding: utf-8 -*-

import numpy as np

from imagine.likelihoods.likelihood import Likelihood
from imagine.create_ring_profile import create_ring_profile


class EnsembleLikelihood(Likelihood):
    def __init__(self, observable_name,  measured_data,
                 data_covariance_operator, profile=None):
        self.observable_name = observable_name
        self.measured_data = measured_data
        self.data_covariance_operator = data_covariance_operator
        if profile is None:
            profile = create_ring_profile(
                            self.measured_data.val.get_full_data())
        self.profile = profile

    def __call__(self, observable):
        field = observable[self.observable_name]
        return self._process_simple_field(field,
                                          self.measured_data,
                                          self.data_covariance_operator,
                                          self.profile)

    def _process_simple_field(self, field, measured_data,
                              data_covariance_operator, profile):
        # https://en.wikipedia.org/wiki/Sherman%E2%80%93Morrison_formula#Generalization
        # B = A^{-1} + U U^dagger
        # A = data_covariance
        # B^{-1} c = (A_inv -
        #             A_inv U (I_k + U^dagger A_inv U)^{-1} U^dagger A_inv) c
        observable = field

        k = observable.shape[0]

        A = data_covariance_operator
        obs_val = observable.val.get_full_data()
        obs_mean = observable.mean(spaces=0).val.get_full_data()

        u_val = observable.val.get_full_data() - obs_mean
        U = observable.copy_empty()
        U.val = u_val
        a_u = A.inverse_times(U, spaces=1)

        # build middle-matrix (kxk)
        a_u_val = a_u.val.get_full_data()
        middle = (np.eye(k) +
                  np.einsum(u_val.conjugate(), [0, 1],
                            a_u_val, [2, 1]))
        middle = np.linalg.inv(middle)
        result_array = np.zeros(k)
        for i in xrange(k):
            c = measured_data - obs_val[i]
            c /= profile

            # assuming that A == A^dagger, this can be shortend
            # a_c = A.inverse_times(c)
            # u_a_c = a_c.dot(U, spaces=1)
            # u_a_c = u_a_c.conjugate()

            # and: double conjugate shouldn't make a difference
            # u_a_c = c.conjugate().dot(a_u, spaces=1).conjugate()
            u_a_c = c.dot(a_u, spaces=1)
            u_a_c_val = u_a_c.val.get_full_data()

            first_summand = A.inverse_times(c)

            second_summand_val = np.einsum(middle, [0, 1], u_a_c_val, [1])
            second_summand_val = np.einsum(a_u_val, [0, 1],
                                           second_summand_val, [0])
            second_summand = first_summand.copy_empty()
            second_summand.val = second_summand_val

            result = c.dot(first_summand - second_summand)
            result_array[i] = result

        return -result_array.mean()
