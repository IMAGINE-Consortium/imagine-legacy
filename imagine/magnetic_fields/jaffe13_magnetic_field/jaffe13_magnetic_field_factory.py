# -*- coding: utf-8 -*-

from imagine.magnetic_fields.magnetic_field.magnetic_field_factory \
    import MagneticFieldFactory

from jaffe13_magnetic_field import Jaffe13MagneticField


class Jaffe13MagneticFieldFactory(MagneticFieldFactory):
    @property
    def magnetic_field_class(self):
        return Jaffe13MagneticField

    @property
    def _initial_parameter_defaults(self):
        defaults = {'B_f_ord': 0.5,
                    'B_field_RMS_uG': 1.,
                    'B_field_alpha': -2.37,
                    'B_field_cutoff': 5.,
                    'B_ran_b2': 0.1,
                    'B_ran_h_d': 4.,
                    'B_ran_h_d2': 1.,
                    'B_ran_h_r': 15.,
                    'B_ran_h_r2': 15.,
                    'bb_amps_0': 2.,
                    'bb_amps_1': 0.133,
                    'bb_amps_2': -3.78,
                    'bb_amps_3': 0.32,
                    'bb_amps_4': -0.023,
                    'bb_bar_a': 0.,
                    'bb_bar_boa': 1.,
                    'bb_bar_phi0_deg': 45.,
                    'bb_cr0_coh': 0.5,
                    'bb_cr0_iso': 0.3,
                    'bb_cr0_ord': 0.5,
                    'bb_d0_iso': 0.3,
                    'bb_d0': 0.3,
                    'bb_delta_phi_iso_deg': 0.,
                    'bb_delta_phi_ord_deg': 0.,
                    'bb_disk_b0': 0.167,
                    'bb_disk_h_d': 0.1,
                    'bb_halo_b0': 1.38,
                    'bb_halo_h_d': 3.,
                    'bb_phi0_deg': 70.,
                    'bb_pitch_biso': -11.,
                    'bb_pitch': -11.5,
                    'bb_r_compconst': 12.,
                    'bb_r_innercut': 0.5,
                    'bb_r_peak': -1.,
                    'bb_r_scale': 20.,
                    'bb_rmax_arms': 30.,
                    'bb_spiral_cpow': 3.,
                    'bb_spiral_h_d': 0.1,
                    }

        return defaults

    @property
    def _initial_variable_to_parameter_mappings(self):
        return self._generate_variable_to_parameter_mapping_defaults(n=3)

    def _generate_variable_to_parameter_mapping_defaults(self, n):
        defaults = {'B_f_ord': self._interval(0.5, 1, n),
                    'B_field_RMS_uG': self._interval(1., 0.3, n),
                    'B_field_alpha': self._interval(-2.37, 1., n),
                    'B_field_cutoff': self._interval(5., 1., n),
                    'B_ran_b2': self._interval(0.1, 1., n),
                    'B_ran_h_d': self._interval(4., 1., n),
                    'B_ran_h_d2': self._interval(1., 1., n),
                    'B_ran_h_r': self._interval(15., 5., n),
                    'B_ran_h_r2': self._interval(15., 5., n),
                    'bb_amps_0': self._interval(2., 1., n),
                    'bb_amps_1': self._interval(0.133, 1., n),
                    'bb_amps_2': self._interval(-3.78, 1., n),
                    'bb_amps_3': self._interval(0.32, 1., n),
                    'bb_amps_4': self._interval(-0.023, 1., n),
                    'bb_bar_a': self._interval(0., 1., n),
                    'bb_bar_boa': self._interval(1., 1., n),
                    'bb_bar_phi0_deg': self._interval(45., 15., n),
                    'bb_cr0_coh': self._interval(0.5, 1., n),
                    'bb_cr0_iso': self._interval(0.3, 1., n),
                    'bb_cr0_ord': self._interval(0.5, 1., n),
                    'bb_d0_iso': self._interval(0.3, 0.1, n),
                    'bb_d0': self._interval(0.3, 0.1, n),
                    'bb_delta_phi_iso_deg': self._interval(0., 1., n),
                    'bb_delta_phi_ord_deg': self._interval(0., 1., n),
                    'bb_disk_b0': self._interval(0.167, 1., n),
                    'bb_disk_h_d': self._interval(0.1, 1., n),
                    'bb_halo_b0': self._interval(1.38, 1., n),
                    'bb_halo_h_d': self._interval(3., 1., n),
                    'bb_phi0_deg': self._interval(70., 20., n),
                    'bb_pitch_biso': self._interval(-11, 5., n),
                    'bb_pitch': self._interval(-11.5, 5., n),
                    'bb_r_compconst': self._interval(12., 3., n),
                    'bb_r_innercut': self._interval(0.5, 1., n),
                    'bb_r_peak': self._interval(-1., 1., n),
                    'bb_r_scale': self._interval(20., 4., n),
                    'bb_rmax_arms': self._interval(30., 5., n),
                    'bb_spiral_cpow': self._interval(3., 1., n),
                    'bb_spiral_h_d': self._interval(0.1, 1., n),
                    }

        return defaults
