# -*- coding: utf-8 -*-

import numpy as np
import healpy as hp


def create_ring_profile(input_map):
    input_map = np.abs(input_map)
    npix = input_map.shape[0]
    nside = hp.npix2nside(npix)

    rings = hp.pix2ring(nside, np.arange(npix))

    rho = np.bincount(rings)[1:]
    averages = np.bincount(rings, weights=input_map)[1:]/rho

    result = averages[rings]

    return result
