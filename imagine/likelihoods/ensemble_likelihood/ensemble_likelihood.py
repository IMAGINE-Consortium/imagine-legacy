# -*- coding: utf-8 -*-

import numpy as np

from nifty import FieldArray, Field

from imagine.likelihoods.likelihood import Likelihood


class EnsembleLikelihood(Likelihood):
    def __init__(self, observable_name,  measured_data,
                 data_covariance, profile=None):
        self.observable_name = observable_name
        self.measured_data = self._strip_data(measured_data)
        if isinstance(data_covariance, Field):
            data_covariance = data_covariance.val.get_full_data()
        self.data_covariance = data_covariance

    def __call__(self, observable):
        field = observable[self.observable_name]
        return self._process_simple_field(field,
                                          self.measured_data,
                                          self.data_covariance)

    def _process_simple_field(self, observable, measured_data,
                              data_covariance):
        # https://en.wikipedia.org/wiki/Sherman%E2%80%93Morrison_formula#Generalization
        # B = A^{-1} + U U^dagger
        # A = data_covariance
        # B^{-1} c = (A_inv -
        #             A_inv U (I_k + U^dagger A_inv U)^{-1} U^dagger A_inv) c
        data_covariance = data_covariance.copy()
        k = observable.shape[0]
        n = observable.shape[1]

        obs_val = observable.val.get_full_data()
        obs_mean = observable.ensemble_mean().val.get_full_data()

        U = obs_val - obs_mean
        U *= np.sqrt(n)
        # compute quantities for OAS estimator
        mu = np.vdot(U, U)/k/n
        alpha = (np.einsum(U, [0, 1], U, [2, 1])**2).sum()
        alpha /= k**2

        numerator = (1 - 2./n)*alpha + (mu*n)**2
        denominator = (k + 1 - 2./n) * (alpha - ((mu*n)**2)/n)

        if denominator == 0:
            rho = 1
        else:
            rho = np.min([1, numerator/denominator])
        self.logger.debug("rho: %f = %f / %f" % (rho, numerator, denominator))

        # rescale U half/half
        V = U * np.sqrt(1-rho) / np.sqrt(k)

        self.logger.info(('data_cov', np.mean(data_covariance),
                          'rho*mu', rho*mu,
                          'rho', rho,
                          'mu', mu,
                          'alpha', alpha))
        B = data_covariance + rho*mu

        V_B = V/B

        # build middle-matrix (kxk)
        middle = (np.eye(k) +
                  np.einsum(V.conjugate(), [0, 1],
                            V_B, [2, 1]))
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
        V_B_c = np.einsum(c, [1], V_B, [0, 1])

        first_summand_val = c/B
        second_summand_val = np.einsum(middle, [0, 1], V_B_c, [1])
        second_summand_val = np.einsum(V_B, [0, 1],
                                       second_summand_val, [0])
#        # second_summand_val *= -1
#        second_summand = first_summand.copy_empty()
#        second_summand.val = second_summand_val

        result_1 = np.vdot(c, first_summand_val)
        result_2 = -np.vdot(c, second_summand_val)

        # compute regularizing determinant of the covariance
        # det(A + UV^T) =  det(A) det(I + V^T A^-1 U)
        log_det_1 = np.sum(np.log(B))
        (sign, log_det_2) = np.linalg.slogdet(middle)
        if sign < 0:
            self.logger.error("Negative determinant of covariance!")

        result = -0.5*(result_1 + result_2 + log_det_1 + log_det_2)

        self.logger.info("Calculated (%s): -(%g + %g + %g + %g) = %g" %
                         (self.observable_name,
                          result_1, result_2, log_det_1, log_det_2, result))
#        result_array[i] = result
#        total_result = result_array.mean()

        return result
