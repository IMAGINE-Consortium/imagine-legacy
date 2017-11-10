# -*- coding: utf-8 -*-

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
