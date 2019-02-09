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

from mpi4py import MPI
import simplejson as json
import numpy as np

from nifty import Field, FieldArray, RGSpace
from d2o import distributed_data_object

comm = MPI.COMM_WORLD
size = comm.size
rank = comm.rank

class MagneticField(Field):
    
    def __init__(self, parameters={}, domain=None, val=None, dtype=None,
                 distribution_strategy=None, copy=False, random_seed=None):

        super(MagneticField, self).__init__(domain=domain,
                                            val=val,
                                            dtype=dtype,
                                            distribution_strategy=distribution_strategy,
                                            copy=copy)

        assert(len(self.domain) == 3)
        assert(isinstance(self.domain[0], FieldArray))
        assert(isinstance(self.domain[1], RGSpace))
        assert(isinstance(self.domain[2], FieldArray))

        self._parameters = {}
        for p in self.descriptor_lookup:#{
            self._parameters[p] = np.float(parameters[p])
        #}
        casted_random_seed = distributed_data_object(global_shape=(self.shape[0],),
                                                     dtype=np.int,
                                                     distribution_strategy=distribution_strategy)
        if random_seed is None:#{
            random_seed = np.random.randint(np.uint32(-1)/3,
                                            size=self.shape[0])
            random_seed = comm.bcast(random_seed, root=0)
        #}
        casted_random_seed[:] = random_seed
        self.random_seed = casted_random_seed

    @property
    def descriptor_lookup(self):
        return {}

    @property
    def parameters(self):
        return self._parameters

    def set_val(self, new_val=None, copy=False):
        if new_val is not None:#{
            raise RuntimeError("Setting the field values explicitly is not supported by MagneticField.")
        #}
        self._val = self._create_field()

    def _to_hdf5(self, hdf5_group):
        hdf5_group.attrs['_parameters'] = json.dumps(self._parameters)
        ret_dict = super(MagneticField, self)._to_hdf5(hdf5_group=hdf5_group)
        ret_dict['random_seed'] = self.random_seed
        return ret_dict

    @classmethod
    def _from_hdf5(cls, hdf5_group, repository):
        new_field = super(MagneticField, cls)._from_hdf5(hdf5_group=hdf5_group,
                                                         repository=repository)
        new_field._parameters = json.loads(hdf5_group.attrs['_parameters'])
        new_field.random_seed = repository.get('random_seed', hdf5_group)
        return new_field
