# -*- coding: utf-8 -*-

from imagine.magnetic_fields.jf12_magnetic_field import JF12MagneticField

from hammurapy_base import HammurapyBase


class HammurapyJF12(HammurapyBase):

    @property
    def valid_magnetic_field_descriptor(self):
        return JF12MagneticField
