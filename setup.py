# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

exec(open('imagine/version.py').read())

#from distutils.core import setup
# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name = "imagine",
      version = __version__,
      author = "Theo Steininger",
      author_email = "theos@mpa-garching.mpg.de",
      description = ("A framework for galactic magnetic field model analysis."),
      license = "BSD",
      keywords = "",
      #url = "https://gitlab.mpcdf.mpg.de/ift/keepers",
      packages=find_packages(),
      package_data={'': ['*.npy'],
                    'imagine.hammurapy': ['confs/*'],},
      package_dir={"imagine": "imagine"},
      dependency_links=[
        'git+https://gitlab.mpcdf.mpg.de/ift/nifty.git/@master#egg=nifty-3.0.3'],
      install_requires=['ift_nifty>=3.0.3', 'simplejson'],
      zip_safe=False,
      classifiers=[
         "Development Status :: 3 - Alpha",
         "Topic :: Utilities",
         "License :: OSI Approved :: BSD License",
          ],
)