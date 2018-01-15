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


def infinity_mapper(x, a=-np.inf, m=0, b=np.inf):
    """
    Maps x from [-inf, inf] into the interval [a, b], where x=0 -> m
    """

    if a == -np.inf and b == np.inf and m == 0:
        return x

    x = np.float(x)
    a = np.float(a)
    b = np.float(b)
    if m is None:
        if a == -np.inf and b == np.inf:
            m = 0
        else:
            m = a + (b-a)/2.
    else:
        m = np.float(m)

    # map x from [-inf, inf] to [0, 1]
    y = np.arctan(x)/np.pi + 0.5
    # compute where m would lie in [0, 1]
    n = (m - a)/(b - a)
    # strech y, such that x=0 -> n
    y = y**np.emath.logn(0.5, n)
    # strech y to the interval [a,b]
    y = y*(b-a) + a
    return y


def unity_mapper(x, a=0, b=1):
    """
    Maps x from [0, 1] into the interval [a, b]
    """
    return x * (b-a) + a
