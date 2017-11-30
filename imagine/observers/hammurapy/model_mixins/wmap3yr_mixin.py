# -*- coding: utf-8 -*-

from .magnetic_field_model import MagneticFieldModel
from imagine.magnetic_fields.wmap3yr_magnetic_field import WMAP3yrMagneticField


class WMAP3yrMixin(MagneticFieldModel):
    def update_parameter_xml(self, root):
        custom_parameters = [
                ['./MagneticField/Regular', 'type', 'WMAP'],
                ['./MagneticField/Random', 'cue', '1'],
                ['./MagneticField/Random', 'type', 'Global']]
        for parameter in custom_parameters:
            root.find(parameter[0]).set(parameter[1], str(parameter[2]))

    @property
    def magnetic_field_class(self):
        return WMAP3yrMagneticField
