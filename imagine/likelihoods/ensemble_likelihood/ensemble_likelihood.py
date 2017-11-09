# -*- coding: utf-8 -*-

import numpy as np

from nifty import DiagonalOperator, FieldArray, Field

from imagine.likelihoods.likelihood import Likelihood
from imagine.create_ring_profile import create_ring_profile


class EnsembleLikelihood(Likelihood):
    def __init__(self, observable_name,  measured_data,
                 data_covariance_operator, profile=None):
        self.observable_name = observable_name
        self.measured_data = self._strip_data(measured_data)
        self.data_covariance_operator = data_covariance_operator
        self.data_covariance_includes_profile = False

        if profile is None:
            profile = create_ring_profile(
                            self.measured_data.val.get_full_data())
        self.profile = profile

    def _strip_data(self, data):
        # if the first element in the domain tuple is a FieldArray we must
        # extract the data
        if isinstance(data.domain[0], FieldArray):
            stripped_data = Field(domain=data.domain[1:],
                                  val=data.val.get_full_data()[0],
                                  distribution_strategy='not')
        return stripped_data

    def __call__(self, observable):
        field = observable[self.observable_name]
        return self._process_simple_field(field,
                                          self.measured_data,
                                          self.data_covariance_operator,
                                          self.profile)

    def _process_simple_field(self, observable, measured_data,
                              data_covariance_operator, profile):
        # https://en.wikipedia.org/wiki/Sherman%E2%80%93Morrison_formula#Generalization
        # B = A^{-1} + U U^dagger
        # A = data_covariance
        # B^{-1} c = (A_inv -
        #             A_inv U (I_k + U^dagger A_inv U)^{-1} U^dagger A_inv) c

        weight = observable.domain[1].weight(1)

        k = observable.shape[0]
        n = observable.shape[1]

        obs_val = observable.val.get_full_data()
        obs_mean = observable.ensemble_mean().val.get_full_data()

        # divide out profile
        obs_val /= profile
        obs_mean /= profile
        measured_data = measured_data / profile

        u_val = obs_val - obs_mean

        # compute quantities for OAS estimator
        mu = np.vdot(u_val, u_val)*weight/k/n
        self.logger.debug("mu: %f" % mu)

        alpha = (np.einsum(u_val, [0, 1], u_val, [2, 1])**2).sum()
        alpha /= k*2
        # correct the volume factor: one factor comes from the internal scalar
        # product and one from the trace
        alpha *= weight**2

        numerator = (1 - 2./n)*alpha + (mu*n)**2
        denominator = (k + 1 - 2./n) * (alpha - ((mu*n)**2)/n)

        if denominator == 0:
            rho = 1
        else:
            rho = np.min([1, numerator/denominator])

        self.logger.debug("rho: %f = %f / %f" % (rho, numerator, denominator))

        # rescale U half/half
        u_val *= np.sqrt(1-rho) / np.sqrt(k)
        U = observable.copy_empty()
        U.val = u_val

        # we assume that data_covariance_operator is a DiagonalOperator
        if not isinstance(data_covariance_operator, DiagonalOperator):
            raise TypeError("data_covariance_operator must be a NIFTY "
                            "DiagonalOperator.")

        A_bare_diagonal = data_covariance_operator.diagonal(bare=True)
        if not self.data_covariance_includes_profile:
            A_bare_diagonal *= (profile**2)
        A_bare_diagonal.val += rho*mu
        A = DiagonalOperator(
                    domain=data_covariance_operator.domain,
                    diagonal=A_bare_diagonal,
                    bare=True, copy=False,
                    default_spaces=data_covariance_operator.default_spaces)

        a_u = A.inverse_times(U, spaces=1)

        # build middle-matrix (kxk)
        a_u_val = a_u.val.get_full_data()
        middle = (np.eye(k) +
                  np.einsum(u_val.conjugate(), [0, 1],
                            a_u_val, [2, 1])*weight)
        middle = np.linalg.inv(middle)
        c = measured_data - obs_mean

        # If the data was incomplete, i.e. contains np.NANs, set those values
        # to zero.
        c = np.nan_to_num(c)

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
        # second_summand_val *= -1
        second_summand = first_summand.copy_empty()
        second_summand.val = second_summand_val

        result_1 = c.vdot(first_summand)
        result_2 = -c.vdot(second_summand)
        result = -(result_1 + result_2)
        self.logger.info("Calculated (%s): -(%f + %f) = %f" %
                         (self.observable_name, result_1, result_2, result))
#        result_array[i] = result
#        total_result = result_array.mean()

        return result
