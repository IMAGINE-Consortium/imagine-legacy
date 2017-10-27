# -*- coding: utf-8 -*-

from imagine.magnetic_fields.wmap3yr_magnetic_field import WMAP3yrMagneticField


class WMAP3yrMixin(object):
    __parameter_dict = {('./Galaxy/MagneticField/Regular', 'type'): 'WMAP',
                        ('./Galaxy/MagneticField/Random', 'cue'): '1',
                        ('./Galaxy/MagneticField/Random', 'type'): 'Anisoglob',
                        }

    @property
    def magnetic_field_class(self):
        return WMAP3yrMagneticField

    def _build_parameter_dict(self, parameter_dict, magnetic_field,
                              local_ensemble_index):
        parameter_dict.update(self.__parameter_dict)

        super(WMAP3yrMixin, self)._build_parameter_dict(parameter_dict,
                                                        magnetic_field,
                                                        local_ensemble_index)
