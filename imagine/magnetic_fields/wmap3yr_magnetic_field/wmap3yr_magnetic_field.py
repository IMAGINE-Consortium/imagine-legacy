# -*- coding: utf-8 -*-

from imagine.magnetic_fields.magnetic_field import MagneticField


class WMAP3yrMagneticField(MagneticField):

    @property
    def descriptor_lookup(self):
        lookup = \
            {'b0': ['./Galaxy/MagneticField/Regular/WMAP/b0', 'value'],
             'psi0': ['./Galaxy/MagneticField/Regular/WMAP/psi0', 'value'],
             'psi1': ['./Galaxy/MagneticField/Regular/WMAP/psi1', 'value'],
             'chi0': ['./Galaxy/MagneticField/Regular/WMAP/chi0', 'value'],
             'random_rms': ['./Galaxy/MagneticField/Random/Iso/rms', 'value'],
             'random_rho': ['./Galaxy/MagneticField/Random/Anisoglob/rho',
                            'value']}
        return lookup

    def _create_field(self):
        raise NotImplementedError
