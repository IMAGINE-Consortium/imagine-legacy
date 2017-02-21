
from .version import __version__

from likelihoods import *
from magnetic_fields import *
from observers import *
from priors import *

from pymultinest import pymultinest

from pipeline import Pipeline

import nifty
nifty.nifty_configuration['default_distribution_strategy'] = 'equal'
