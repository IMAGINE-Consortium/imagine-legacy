# -*- coding: utf-8 -*-

import os

from imagine.magnetic_fields.galmag_field import GalMagField


class GalMagMixin(object):
    def __init__(self, hammurabi_executable, conf_directory='./confs',
                 working_directory_base='.', nside=128,
                 analytic_ensemble_mean=False):
        self.__parameter_dict = {'B_field_type': '6'}
        super(GalMagMixin, self).__init__(hammurabi_executable,
                                          conf_directory,
                                          working_directory_base,
                                          nside,
                                          analytic_ensemble_mean)

    @property
    def magnetic_field_class(self):
        return GalMagField

    def _build_parameter_dict(self, parameter_dict, magnetic_field,
                              working_directory, local_ensemble_index):
        parameter_dict.update(self.__parameter_dict)

        parameter_dict.update(magnetic_field.parameters)

        # write the field array to disk
        array_file_name = os.path.join(working_directory, 'b_field.arr')
        field_array = magnetic_field.val.get_full_data()
        # hammurabi reads the array like B[z,y,x]
        # field_array = field_array.transpose((1, 2, 3, 0))
        field_array.tofile(array_file_name)

        super(GalMagMixin, self)._build_parameter_dict(parameter_dict,
                                                       magnetic_field,
                                                       working_directory,
                                                       local_ensemble_index)
