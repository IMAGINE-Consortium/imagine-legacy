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


class SimpleLikelihood(Likelihood):
    def __init__(self, observable_name, measured_data, data_covariance=None):
        self.observable_name = observable_name
        self.measured_data = self._strip_data(measured_data)
        if isinstance(data_covariance, Field):
            data_covariance = data_covariance.val.get_full_data()
        self.data_covariance = data_covariance

    def __call__(self, observable):
        data = self.measured_data
        field = observable[self.observable_name]
        obs_mean = field.ensemble_mean().val.get_full_data()

        diff = data - obs_mean
        if self.data_covariance is not None:
            # modified by Jiaxin
            # it is not a good practice to directly inverse matrices
            right = np.linalg.solve (self.data_covariance,diff)
        else:
            right = diff
        return -0.5 * np.vdot(diff, right)
