# -*- coding: utf-8 -*-

from imagine.magnetic_fields.magnetic_field import MagneticField


class JF12MagneticField(MagneticField):
    @property
    def parameter_list(self):
        parameter_list = ['b51_ran_b1', 'b51_ran_b2', 'b51_ran_b3',
                          'b51_ran_b4', 'b51_ran_b5', 'b51_ran_b6',
                          'b51_ran_b7', 'b51_ran_b8', 'b51_coh_b1',
                          'b51_coh_b2', 'b51_coh_b3', 'b51_coh_b4',
                          'b51_coh_b5', 'b51_coh_b6', 'b51_coh_b7',
                          'b51_z0_spiral', 'b51_z0_smooth', 'b51_r0_smooth',
                          'b51_b0_smooth', 'b51_b0_x', 'b51_Xtheta',
                          'b51_r0_x', 'b51_h_disk', 'b51_Bn', 'b51_Bs',
                          'b51_z0_halo', 'b51_b_ring', 'b51_b0_interior',
                          'b51_shift', 'B_analytic_beta']
        return parameter_list

    def _create_field(self):
        raise NotImplementedError
