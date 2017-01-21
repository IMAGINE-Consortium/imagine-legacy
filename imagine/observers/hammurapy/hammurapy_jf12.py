# -*- coding: utf-8 -*-

from hammurapy_base import HammurapyBase


class HammurapyJF12(HammurapyBase):

    @property
    def valid_magnetic_field_descriptor(self):
        d = super(HammurapyJF12, self).valid_magnetic_field_descriptor
        d += ['JF12']
        return d
