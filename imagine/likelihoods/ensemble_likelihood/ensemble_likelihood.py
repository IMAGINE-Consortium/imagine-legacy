# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright(C) 2013-2017 Max-Planck-Society
#
# IMAGINE is being developed at the Max-Planck-Institut fuer Astrophysik
# and financially supported by the Studienstiftung des deutschen Volkes.

import numpy as np

from nifty import Field

from imagine.likelihoods.likelihood import Likelihood


class EnsembleLikelihood(Likelihood):
    def __init__(self, observable_name,  measured_data,
                 data_covariance, profile=None):
        self.observable_name = observable_name
        self.measured_data = self._strip_data(measured_data)
        if isinstance(data_covariance, Field):
            data_covariance = data_covariance.val.get_full_data()
        self.data_covariance = data_covariance
        self.use_determinant = True

    def __call__(self, observable):
        field = observable[self.observable_name]
        return self._process_simple_field(field,
                                          self.measured_data,
                                          self.data_covariance)

    def _process_simple_field(self, observable, measured_data,
                              data_covariance):
        # Theo's scheme of inversing matrices now modifined by Jiaxin
        # use numpy.linalg.solve(A,b) to get inv(A)*b
        # thus safely avoid any possible difficulties brought by inversing matrices
        data_covariance = data_covariance.copy()
        k = observable.shape[0]
        n = observable.shape[1]

        obs_val = observable.val.get_full_data()
        obs_mean = observable.ensemble_mean().val.get_full_data()

        U = obs_val - obs_mean
        # OAS calculation modifined by Jiaxin
        # emperical S
        S = np.vdot(U,U)/k
        # trace of S
        TrS = np.trace(S)
        # trace of S^2
        TrS2 = np.trace(np.dot(S,S))
        
        numerator = (1.-2./n)*TrS2 + TrS**2
        denominator = (k+1.-2./n)*(TrS2-(TrS**2)/n)
        
        if denominator == 0:
            rho = 1
        else:
            rho = np.min([1, numerator/denominator])
            
        self.logger.debug("rho: %f = %f / %f" % (rho, numerator, denominator))

        # total covariance
        AC = data_covariance + (1-rho)*S + np.eye(n)*rho*TrS/n
        # obs - mean(sim)
        dc = measured_data - obs_mean
        # If the data was incomplete, i.e. contains np.NANs, set those values
        # to zero.
        dc = np.nan_to_num(dc)
        # calculate likelihood
        (sign_AC, logdet_AC) = np.linalg.slogdet(AC*2.*np.pi)
        result = -0.5*(dc*np.linalg.solve(AC,dc)) - 0.5*sing_AC*logdet_AC
        
        return result
