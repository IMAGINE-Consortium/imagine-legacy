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

import abc

from keepers import Loggable

from nifty import FieldArray


class Likelihood(Loggable, object):
    @abc.abstractmethod
    def __call__(self, observables):
        raise NotImplementedError

    def _strip_data(self, data):
        # if the first element in the domain tuple is a FieldArray we must
        # extract the data
        if not hasattr(data, 'domain'):
            return data

        if isinstance(data.domain[0], FieldArray):
            data = data.val.get_full_data()[0]
        else:
            data = data.val.get_full_data()
        return data
