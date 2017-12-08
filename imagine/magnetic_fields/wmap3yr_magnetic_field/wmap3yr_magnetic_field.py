# -*- coding: utf-8 -*-

from imagine.magnetic_fields.magnetic_field import MagneticField


class WMAP3yrMagneticField(MagneticField):

    @property
    def descriptor_lookup(self):
        lookup = \
            {'b0': ['./MagneticField/Regular/WMAP/b0', 'value'],
             'psi0': ['./MagneticField/Regular/WMAP/psi0', 'value'],
             'psi1': ['./MagneticField/Regular/WMAP/psi1', 'value'],
             'chi0': ['./MagneticField/Regular/WMAP/chi0', 'value'],
             'random_rms': ['./MagneticField/Random/Global/rms', 'value'],
             'random_rho': ['./MagneticField/Random/Global/rho', 'value'],
             'random_a0': ['./MagneticField/Random/Global/a0', 'value']
             }
        return lookup

    def _create_field(self):
        raise NotImplementedError
