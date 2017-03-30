
from .version import __version__

from likelihoods import *
from magnetic_fields import *
from observables import *
from observers import *
from priors import *

from pymultinest_importer import pymultinest

from pipeline import Pipeline

from sample import Sample

import nifty
nifty.nifty_configuration['default_distribution_strategy'] = 'equal'
