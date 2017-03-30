# -*- coding: utf-8 -*-

from imagine.magnetic_fields.magnetic_field import MagneticField

try:
    import galmag
except ImportError:
    galmag_available = False
else:
    galmag_available = True

class GalMagField(MagneticField):
    def __init__(self, parameters=[], domain=None, val=None, dtype=None,
                 distribution_strategy=None, copy=False, random_seed=None):
        if not galmag_available:
            raise ImportError("GalMag module needed but not available.")

        super(MagneticField, self).__init__(
                                parameters=parameters,
                                domain=domain,
                                val=val,
                                dtype=dtype,
                                distribution_strategy=distribution_strategy,
                                copy=copy,
                                random_seed=random_seed)

    @property
    def parameter_list(self):
        parameter_list = ['b_x', 'b_y', 'b_z']
        return parameter_list

    def _create_field(self):
        grid_domain = self.domain[1]
        box_resolution = grid_domain.shape
        bl = np.array(grid_domain.distances) * box_resolution
        box_limits = [[-bl[0], bl[0]],
                      [-bl[1], bl[1]],
                      [-bl[2], bl[2]]]

        ensemble_size = self.shape[0]
        val = self.cast(None)
        for i in ensemble_size:
            b = galmag.B_field.B_field(box_limits, box_resolution)
            val[i, :, :, :, 0] = b.x
            val[i, :, :, :, 1] = b.y
            val[i, :, :, :, 2] = b.z

        return val
