# -*- coding: utf-8 -*-

import abc


class MagneticFieldModel(object):
    def update_parameter_xml(self, root):
        pass

    @abc.abstractproperty
    def magnetic_field_class(self):
        raise NotImplementedError
