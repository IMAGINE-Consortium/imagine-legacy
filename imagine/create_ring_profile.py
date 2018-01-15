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
import healpy as hp


def create_ring_profile(input_map):
    input_map = np.abs(input_map)
    npix = input_map.shape[0]
    nside = hp.npix2nside(npix)

    rings = hp.pix2ring(nside, np.arange(npix)) - 1

    mask = np.ones([npix])
    mask[np.isnan(input_map)] = 0
    rho = np.bincount(rings, weights=mask)
    averages = np.bincount(rings, weights=np.nan_to_num(input_map))/rho
    # set profile for empty rings to 1
    averages[np.isnan(averages)] = 1

    result = averages[rings]

    return result
