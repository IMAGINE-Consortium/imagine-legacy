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
      license = "GPLv3",
      keywords = "",
      #url = "https://gitlab.mpcdf.mpg.de/ift/keepers",
      packages=find_packages(),
      package_data={'imagine.observers.hammurapy': ['input/*'],},
      package_dir={"imagine": "imagine"},
      dependency_links=[
        'git+https://gitlab.mpcdf.mpg.de/ift/nifty.git/#egg=nifty4-4.2.0'],
      install_requires=['nifty4>=4.2.0', 'simplejson'],
      zip_safe=False,
      classifiers=[
         "Development Status :: 4 - Beta",
         "Topic :: Utilities",
         "License :: OSI Approved :: GNU General Public License v3 "
         "or later (GPLv3+)"],
)
