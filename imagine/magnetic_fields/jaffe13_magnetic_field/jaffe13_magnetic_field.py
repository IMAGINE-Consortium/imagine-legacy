# -*- coding: utf-8 -*-

from imagine.magnetic_fields.magnetic_field import MagneticField


class Jaffe13MagneticField(MagneticField):
    @property
    def parameter_list(self):
        parameter_list = ['B_f_ord', 'B_field_alpha', 'B_field_cutoff',
                          'B_ran_b2', 'B_ran_h_d', 'B_ran_h_d2', 'B_ran_h_r',
                          'B_ran_h_r2', 'b1_Psi_0', 'bb_amps_0', 'bb_amps_1',
                          'bb_amps_2', 'bb_amps_3', 'bb_amps_4', 'bb_bar_a',
                          'bb_bar_boa', 'bb_bar_phi0_deg', 'bb_cr0_coh',
                          'bb_cr0_iso', 'bb_cr0_ord', 'bb_d0_iso', 'bb_d0',
                          'bb_delta_phi_iso_deg', 'bb_delta_phi_ord_deg',
                          'bb_disk_b0', 'bb_disk_h_d', 'bb_halo_b0',
                          'bb_halo_h_d', 'bb_phi0_deg', 'bb_pitch_biso',
                          'bb_pitch', 'bb_r_compconst', 'bb_r_innercut',
                          'bb_r_peak', 'bb_r_peak', 'bb_r_scale',
                          'bb_rmax_arms', 'bb_spiral_cpow', 'bb_spiral_h_d',
                          'bb_spiral_h_d']
        return parameter_list

    def _create_field(self):
        raise NotImplementedError
