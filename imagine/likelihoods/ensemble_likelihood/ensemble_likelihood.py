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

        # divide out profile
        obs_val /= profile
        obs_mean /= profile
        measured_data = measured_data / profile

        u_val = obs_val - obs_mean
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

            # assuming that A == A^dagger, this can be shortend
            # a_c = A.inverse_times(c)
            # u_a_c = a_c.dot(U, spaces=1)
            # u_a_c = u_a_c.conjugate()

            # and: double conjugate shouldn't make a difference
            # u_a_c = c.conjugate().dot(a_u, spaces=1).conjugate()

            # Pure NIFTy is
            # u_a_c = c.dot(a_u, spaces=1)
            # u_a_c_val = u_a_c.val.get_full_data()
            c_weighted_val = c.weight().val.get_full_data()
            u_a_c_val = np.einsum(c_weighted_val, [1], a_u_val, [0, 1])

            first_summand = A.inverse_times(c)
            second_summand_val = np.einsum(middle, [0, 1], u_a_c_val, [1])
            second_summand_val = np.einsum(a_u_val, [0, 1],
                                           second_summand_val, [0])
            second_summand_val *= -1
            second_summand = first_summand.copy_empty()
            second_summand.val = second_summand_val

            result_1 = -c.dot(first_summand)
            result_2 = -c.dot(second_summand)
            result = result_1 + result_2
            self.logger.debug("Calculated %i of %i: %f + %f = %f" %
                              (i, k, result_1, result_2, result))
            result_array[i] = result

        total_result = result_array.mean()
        normalization = measured_data.dot(measured_data)
        normalized_total_result = total_result / normalization
        self.logger.info("Applied normalization for total result: "
                         "%f / %f = %f" %
                         (total_result,
                          normalization,
                          normalized_total_result))

        return normalized_total_result
