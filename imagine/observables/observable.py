# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright(C) 2013-2017 Max-Planck-Society
#
# IMAGINE is being developed at the Max-Planck-Institut fuer Astrophysik
# and financially supported by the Studienstiftung des deutschen Volkes.

from nifty import Field, FieldArray

class Observable(Field):
    def __init__(self, domain=None, val=None, dtype=None,
                 distribution_strategy=None, copy=False):

        super(Observable, self).__init__(domain=domain,
                                         val=val,
                                         dtype=dtype,
                                         distribution_strategy=distribution_strategy,
                                         copy=copy)
        assert(len(self.domain) == 2)
        assert(isinstance(self.domain[0], FieldArray))

    def ensemble_mean(self):
        try:
            self._ensemble_mean
        except(AttributeError):
            self._ensemble_mean = self.mean(spaces=0)
        finally:
            return self._ensemble_mean

    def _to_hdf5(self, hdf5_group):
        if hasattr(self, "_ensemble_mean"):
            return_dict = {"ensemble_mean": self._ensemble_mean}
        else:
            return_dict = {}
        return_dict.update(
                   super(Observable, self)._to_hdf5(hdf5_group=hdf5_group))
        return return_dict

    @classmethod
    def _from_hdf5(cls, hdf5_group, repository):
        new_field = super(Observable, cls)._from_hdf5(hdf5_group=hdf5_group,
                                                      repository=repository)
        try:
            observable_mean = repository.get("ensemble_mean", hdf5_group)
            new_field._observable_mean = observable_mean
        except(KeyError):
            pass
        return new_field
