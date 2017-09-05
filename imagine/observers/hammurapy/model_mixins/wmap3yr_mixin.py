# -*- coding: utf-8 -*-

from imagine.magnetic_fields.wmap3yr_magnetic_field import WMAP3yrMagneticField

class WMAP3yrMixin(object):
	def __init__(self, hammurabi_executable, conf_directory='./confs',
		working_directory_base='.', nside=128,
		analytic_ensemble_mean=False):
		
		self.__parameter_dict={'B_field_type': '1',
				'B_field_do_random': 'T',
				'B_field_RMS_uG': '1.0',
				'B_field_z_antisym': '0',
				}
		super(WMAP3yrMixin, self).__init__(hammurabi_executable,
						conf_directory,
						working_directory_base,
						nside,
						analytic_ensemble_mean)

	@property
	def magnetic_field_class(self):
		return WMAP3yrMagneticField
	
	def _build_parameter_dict(self, parameter_dict, magnetic_field,
				working_directory, local_ensemble_index):
		parameter_dict.update(self.__parameter_dict)

		parameter_dict.update(magnetic_field.parameters)

		super(WMAP3yrMixin, self)._build_parameter_dict(parameter_dict,
							magnetic_field,
							working_directory,
							local_ensemble_index)
