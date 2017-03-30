# -*- coding: utf-8 -*-

from imagine.magnetic_fields.magnetic_field.magnetic_field_factory \
    import MagneticFieldFactory

from jf12_magnetic_field import JF12MagneticField


class JF12MagneticFieldFactory(MagneticFieldFactory):
    @property
    def magnetic_field_class(self):
        return JF12MagneticField

    @property
    def _initial_parameter_defaults(self):
        defaults = {'b51_ran_b1': 10.8,
                    'b51_ran_b2': 6.96,
                    'b51_ran_b3': 9.59,
                    'b51_ran_b4': 6.96,
                    'b51_ran_b5': 1.96,
                    'b51_ran_b6': 16.34,
                    'b51_ran_b7': 37.29,
                    'b51_ran_b8': 10.35,
                    'b51_coh_b1': 0.1,
                    'b51_coh_b2': 3.,
                    'b51_coh_b3': -0.9,
                    'b51_coh_b4': -0.8,
                    'b51_coh_b5': -2.,
                    'b51_coh_b6': -4.2,
                    'b51_coh_b7': 0.,
                    'b51_z0_spiral': 0.61,
                    'b51_z0_smooth': 2.84,
                    'b51_r0_smooth': 10.97,
                    'b51_b0_smooth': 4.68,
                    'b51_b0_x': 4.6,
                    'b51_Xtheta': 49.,
                    'b51_r0_x': 2.9,
                    'b51_h_disk': 0.4,
                    'b51_Bn': 1.4,
                    'b51_Bs': -1.1,
                    'b51_z0_halo': 5.3,
                    'b51_b_ring': 0.1,
                    'b51_b0_interior': 7.63,
                    'b51_shift': 0.,
                    'B_analytic_beta': 1.36}
        return defaults

    @property
    def _initial_variable_to_parameter_mappings(self):
        return self._generate_variable_to_parameter_mapping_defaults(n=3)

    def _generate_variable_to_parameter_mapping_defaults(self, n):
        defaults = {
           'b51_ran_b1': self._interval(10.8, 2.33, n),  # b_1, 1210.7820
           'b51_ran_b2': self._interval(6.96, 1.58, n),  # b_2, 1210.7820
           'b51_ran_b3': self._interval(9.59, 1.10, n),  # b_3, 1210.7820
           'b51_ran_b4': self._interval(6.96, 0.87, n),  # b_4 1210.7820
           'b51_ran_b5': self._interval(1.96, 1.32, n),  # b_5, 1210.7820
           'b51_ran_b6': self._interval(16.34, 2.53, n),  # b_6, 1210.7820
           'b51_ran_b7': self._interval(37.29, 2.39, n),  # b_7, 1210.7820
           'b51_ran_b8': self._interval(10.35, 4.43, n),  # b_8, 1210.7820
           'b51_b0_interior': self._interval(7.63, 1.39, n),  # b_int, 1210.7820
           'b51_z0_spiral': self._positive_interval(0.61, 0.04, n), # z_0^disk, 1210.7820
           'b51_b0_smooth': self._interval(4.68, 1.39, n),  # B_0, 1210.7820
           'b51_r0_smooth': self._positive_interval(10.97, 3.80, n),  # r_0, 1210.7820
           'b51_z0_smooth': self._positive_interval(2.84, 1.30, n),  # z_0, 1210.7820
            # beta is missing (1210.7820)

           'b51_coh_b1': self._interval(0.1, 1.8, n),  # b_1, 1204.3662
           'b51_coh_b2': self._interval(3.0, 0.6, n),  # b_2, 1204.3662
           'b51_coh_b3': self._interval(-0.9, 0.8, n),  # b_3, 1204.3662
           'b51_coh_b4': self._interval(-0.8, 0.3, n),  # b_4, 1204.3662
           'b51_coh_b5': self._interval(-2.0, 0.1, n),  # b_5, 1204.3662
           'b51_coh_b6': self._interval(-4.2, 0.5, n),  # b_6, 1204.3662
           'b51_coh_b7': self._interval(0.0, 1.8, n),  # b_7, 1204.3662
           'b51_b_ring': self._interval(0.1, 0.1, n),  # b_ring, 1204.3662
           'b51_h_disk': self._positive_interval(0.4, 0.03, n),  # b_disk, 1204.3662
           # w_disk is missing, 1204.3662
           # B_n_disk is missing, 1204.3662
           'b51_Bs': self._interval(-1.1, 0.1, n),  # B_s, 1204.3662
           # r_n is missing, 1204.3662
           # r_s is missing, 1204.3662
           # w_h is missing, 1204.3662
           'b51_z0_halo': self._positive_interval(5.3, 1.6, n),  # z_0, 1204.3662
           'b51_b0_x': self._interval(4.6, 0.3, n),  # B_X, 1204.3662
           'b51_Xtheta': self._positive_interval(49., 1., n),  # Theta_X^0, 1204.3662
           # r_x^c is missing, 1204.3662
           'b51_r0_x': self._positive_interval(2.9, 0.1, n),  # r_x, 1204.3662
           # gamma is missing (1204.3662)
           'b51_shift': [-2, 0, 2],
           'B_analytic_beta': self._interval(1.36, 0.4, n),
            }
        return defaults
