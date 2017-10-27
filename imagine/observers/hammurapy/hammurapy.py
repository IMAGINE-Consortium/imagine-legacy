# -*- coding: utf-8 -*-

import os
import tempfile
import subprocess
import xml.etree.ElementTree as et

import numpy as np

from d2o import distributed_data_object

from nifty import HPSpace

from imagine.observers.observer import Observer
from .observable_mixins import ObservableMixin
from .model_mixins import MagneticFieldModel
from imagine.observables import Observable


class Hammurapy(Observer):
    def __init__(self, hammurabi_executable, magnetic_field_model, observables,
                 input_directory='./input', working_directory_base='.',
                 nside=64):
        self.hammurabi_executable = os.path.abspath(hammurabi_executable)

        if not isinstance(magnetic_field_model, MagneticFieldModel):
            raise TypeError("magnetic_field_model must be an instance of the "
                            "MagneticField class.")
        self.magnetic_field_model = magnetic_field_model

        if not isinstance(observables, list):
            if isinstance(observables, tuple):
                observables = list(observables)
            else:
                observables = [observables]
        for obs in observables:
            if not isinstance(obs, ObservableMixin):
                raise TypeError("observables must be an instance of the "
                                "ObservableMixin class.")
        self.observables = observables

        self.input_directory = os.path.abspath(input_directory)
        self.working_directory_base = os.path.abspath(working_directory_base)

        self.nside = int(nside)
        self._hpSpace = HPSpace(nside=self.nside)

        self.last_call_log = ""

    @property
    def magnetic_field_class(self):
        return self.magnetic_field_model.magnetic_field_class

    def _make_temp_folder(self):
        prefix = os.path.join(self.working_directory_base, 'temp_hammurabi_')
        return tempfile.mkdtemp(prefix=prefix)

    def _remove_folder(self, path):
        # Try multiple times in order to overcome 'Directory not empty' errors
        # Hopefully open file handles get closed in the meantime
        n = 0
        while n < 10:
            temp_process = subprocess.Popen(['rm', '-rf', path],
                                            stderr=subprocess.PIPE)
            # wait until process is finished
            errlog = temp_process.communicate()[1]
            # check if there were some errors
            if errlog == '':
                self.logger.debug("Successfully removed temporary folder.")
                break
        else:
            self.logger.warning('Could not delete %s' % path)

    def _call_hammurabi(self, path):
        temp_process = subprocess.Popen(
                                [self.hammurabi_executable, 'parameters.xml'],
                                stdout=subprocess.PIPE,
                                cwd=path)
        self.last_call_log = temp_process.communicate()[0]

    def _initialize_observable_dict(self, magnetic_field):
        observable_dict = {}
        for observable in self.observables:
            observable_dict = self._initialize_observable_dict_helper(
                    observable_dict, magnetic_field, observable)
        return observable_dict

    def _initialize_observable_dict_helper(self, observable_dict,
                                           magnetic_field, observable):
        ensemble_space = magnetic_field.domain[0]
        for component in observable.component_names:
            # It is important to initialize the Observables with an explicit
            # value. Otherwise the d2o will not instantaneuosly be created
            # (c.f. lazy object creation).
            observable_dict[component] = Observable(
                                    val=0,
                                    domain=(ensemble_space, self._hpSpace),
                                    distribution_strategy='equal')
        return observable_dict

    def _build_parameter_dict(self, parameter_dict, magnetic_field,
                              local_ensemble_index):

        parameter_dict.update(self.magnetic_field_model.parameter_dict)

        parameter_dict.update(
                {('./Interface/fe_grid', 'read'): '1',
                 ('./Interface/fe_grid', 'filename'):
                     os.path.join(self.input_directory, 'fe_grid.bin'),
                 })
        # access the magnetic-field's random-seed d2o directly, since we
        # know that the distribution strategy is the same for the
        # randam samples and the magnetic field itself
        random_seed = magnetic_field.random_seed.data[local_ensemble_index]
        parameter_dict.update(
                {('./Galaxy/MagneticField/Random', 'seed'): random_seed})

        for key, value in magnetic_field.parameters.iteritems():
            large_key = magnetic_field.descriptor_lookup[key]
            parameter_dict[large_key] = value

        grid_space = magnetic_field.domain[1]
        lx, ly, lz = np.array(grid_space.shape)*np.array(grid_space.distances)
        nx, ny, nz = grid_space.shape

        parameter_dict.update({('./Grid/Box/lx', 'value'): lx,
                               ('./Grid/Box/ly', 'value'): ly,
                               ('./Grid/Box/lz', 'value'): lz,
                               ('./Grid/Box/nx', 'value'): nx,
                               ('./Grid/Box/ny', 'value'): ny,
                               ('./Grid/Box/nz', 'value'): nz})
        parameter_dict.update(
                {('./Grid/Integration/nside', 'value'): self.nside})

    def _write_parameter_file(self, working_directory):
        # load the default xml
        try:
            default_parameters_xml = os.path.join(self.input_directory,
                                                  'default_parameters.xml')
            tree = et.parse(default_parameters_xml)
        except IOError:
            import imagine
            module_path = os.path.split(
                            imagine.observers.hammurapy.__file__)[0]
            default_parameters_xml = os.path.join(
                                module_path, 'input/default_parameters.xml')
            tree = et.parse(default_parameters_xml)

        root = tree.getroot()
        for key, value in parameter_dict.iteritems():
            root.find(key[0]).set(key[1], str(value))

        parameters_file_path = os.path.join(working_directory,
                                            'parameters.xml')
        tree.write(parameters_file_path)

    def _write_parameter_xml(self, magnetic_field, local_ensemble_index,
                             working_directory):
        # load the default xml
        try:
            default_parameters_xml = os.path.join(self.input_directory,
                                                  'default_parameters.xml')
            tree = et.parse(default_parameters_xml)
        except IOError:
            import imagine
            module_path = os.path.split(
                            imagine.observers.hammurapy.__file__)[0]
            default_parameters_xml = os.path.join(
                                module_path, 'input/default_parameters.xml')
            tree = et.parse(default_parameters_xml)

        root = tree.getroot()

        # modify the default_parameters.xml
        custom_parameters = [
                ['./Grid/Integration/shell/auto/nside_min', 'value',
                 self.nside],
                ['./Interface/fe_grid', 'read', '1'],
                ['./Interface/fe_grid', 'filename',
                 os.path.join(self.input_directory, 'fe_grid.bin')]
                             ]

        # access the magnetic-field's random-eed d2o directly, since we
        # know that the distribution strategy is the same for the
        # randam samples and the magnetic field itself
        random_seed = magnetic_field.random_seed.data[local_ensemble_index]
        custom_parameters += [['./Galaxy/MagneticField/Random', 'seed',
                               random_seed]]

        for key, value in magnetic_field.parameters.iteritems():
            desc = magnetic_field.descriptor_lookup[key]
            custom_parameters += [desc + [value]]

        # set up grid parameters
        grid_space = magnetic_field.domain[1]
        lx, ly, lz = \
            np.array(grid_space.shape)*np.array(grid_space.distances)/2.
        nx, ny, nz = grid_space.shape
        custom_parameters += [['./Grid/Box/x_min', 'value', -lx],
                              ['./Grid/Box/x_max', 'value', lx],
                              ['./Grid/Box/y_min', 'value', -ly],
                              ['./Grid/Box/y_max', 'value', ly],
                              ['./Grid/Box/z_min', 'value', -lz],
                              ['./Grid/Box/z_max', 'value', lz],
                              ['./Grid/Box/nx', 'value', nx],
                              ['./Grid/Box/ny', 'value', ny],
                              ['./Grid/Box/nz', 'value', nz]]

        for parameter in custom_parameters:
            root.find(parameter[0]).set(parameter[1], str(parameter[2]))

        self.magnetic_field_model.update_parameter_xml(root)

        for observable in self.observables:
            observable.update_parameter_xml(root)

        parameters_file_path = os.path.join(working_directory,
                                            'parameters.xml')
        tree.write(parameters_file_path)

    def _fill_observable_dict(self, observable_dict, working_directory,
                              local_ensemble_index):
        for observable in self.observables:
            observable.fill_observable_dict(
                            observable_dict=observable_dict,
                            working_directory=working_directory,
                            local_ensemble_index=local_ensemble_index,
                            nside=self.nside)
        return observable_dict

    def __call__(self, magnetic_field):

        if not isinstance(magnetic_field, self.magnetic_field_class):
            raise ValueError("Given magnetic field is not a subclass of" +
                             " %s" % str(self.magnetic_field_class))

        observable_dict = self._initialize_observable_dict(
                                            magnetic_field=magnetic_field)

        # iterate over ensemble and put result into result_observable
        # get the local shape by creating a dummy d2o
        ensemble_number = magnetic_field.shape[0]
        dummy = distributed_data_object(global_shape=(ensemble_number,),
                                        distribution_strategy='equal',
                                        dtype=np.float)

        local_length = dummy.distributor.local_length
        for local_ensemble_index in xrange(local_length):
            self.logger.debug("Processing local_ensemble_index %i." %
                              local_ensemble_index)
            # create a temporary folder
            working_directory = self._make_temp_folder()

            self._write_parameter_xml(
                                    magnetic_field=magnetic_field,
                                    local_ensemble_index=local_ensemble_index,
                                    working_directory=working_directory)

            # call hammurabi
            self._call_hammurabi(working_directory)

            # if hammurabi failed, _fill_observable_dict will fail
            try:
                self._fill_observable_dict(observable_dict,
                                           working_directory,
                                           local_ensemble_index)
            except:
                self.logger.critical("Hammurabi failed! Last call log:\n" +
                                     self.last_call_log)
                raise
            finally:
                pass
                #self._remove_folder(working_directory)

        return observable_dict
