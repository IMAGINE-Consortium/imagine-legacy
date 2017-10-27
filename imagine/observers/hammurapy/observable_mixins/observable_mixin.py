# -*- coding: utf-8 -*-

import abc
import os

import healpy

from keepers import Loggable


class ObservableMixin(Loggable, object):
    @abc.abstractproperty
    def obs_name(self):
        raise NotImplementedError

    @abc.abstractproperty
    def component_names(self):
        raise NotImplementedError

    def update_parameter_xml(self):
        raise NotImplementedError

    def fill_observable_dict(self, observable_dict, working_directory,
                             local_ensemble_index, nside):
        self.logger.debug('Reading %s-map.' % self.obs_name)
        map_list = self._read_fits_file(path=working_directory,
                                        name=self.obs_name + '.fits',
                                        nside=nside)

        for i, map_component in enumerate(map_list):
            temp_obs = observable_dict[self.component_names[i]]
            temp_obs.val.data[local_ensemble_index] = map_component

    def _read_fits_file(self, path, name, nside):
        map_path = os.path.join(path, name)
        result_list = []
        i = 0
        while True:
            try:
                loaded_map = healpy.read_map(map_path, verbose=False,
                                             field=i)
                # loaded_map = healpy.ud_grade(loaded_map, nside_out=nside)
                result_list += [loaded_map]
                i += 1
            except IndexError:
                break
        return result_list
