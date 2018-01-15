IMAGINE - 


Description
-------

The Galactic magnetic field (GMF) has a huge impact on the evolution of the Milky Way. Yet currently there exists no standard model for it, as its structure is not fully understood. In the past many parametric GMF models of varying complexity have been developed that all have been fitted to an individual set of observational data complicating comparability.
Our goal is to systematize parameter inference of GMF models. We want to enable a statistical comparison of different models in the future, allow for simple refitting with respect to newly available data sets and thereby increase the research area’s transparency. We aim to make state-of-the-art Bayesian methods easily available and in particular to treat the statistics related to the random components of the GMF correctly.
To achieve our goals, we built IMAGINE, the Interstellar Magnetic Field Inference Engine. It is a modular open source framework for doing inference on generic parametric models of the Galaxy. We combine highly optimized tools and technology such as the MultiNest sampler and the information field theory framework NIFTy in order to leverage existing expertise.
We demonstrate the steps needed for robust parameter inference and model comparison. Our results show how important the combination of complementary observables like synchrotron emission and Faraday depth is while building a model and fitting its parameters to data. IMAGINE is open-source software available under the GNU General Public License v3 (GPL-3) at: https://gitlab.mpcdf.mpg.de/ift/IMAGINE


Installation
------------

### Requirements

-   [Python](http://www.python.org/) (v2.7.x)
-   [NumPy](http://www.numpy.org/)
-   [NIFTy] (https://gitlab.mpcdf.mpg.de/ift/NIFTy) (installed automatically)
-   [D2O] (https://gitlab.mpcdf.mpg.de/ift/D2O) (installed automatically)
-   [keepers] (https://gitlab.mpcdf.mpg.de/ift/keepers) (installed automatically)
-   [simplejson] (https://github.com/simplejson/simplejson) (installed automatically)

### Download

The current version of IMAGINE can be obtained by cloning the repository:

    git clone https://gitlab.mpcdf.mpg.de/ift/IMAGINE.git

### Installation on Ubuntu

This is for you if you want to install IMAGINE on your personal computer
running with an Ubuntu-like linux system where you have root priviledges.
Starting with a fresh Ubuntu installation move to a folder like
`~/Downloads`:

-   Install basic packages like python, python-dev, gsl and others:

        sudo apt-get install curl git autoconf libtool python-dev python-pip python-numpy

-   Finally, IMAGINE:

        git clone https://gitlab.mpcdf.mpg.de/ift/IMAGINE.git
        (cd IMAGINE && python setup.py install --user)

### Docker

IMAGINE provides a docker container based on Ubuntu:latest with all dependencies installed and preconfigured. 
To build the docker container yourself, switch to the 'docker' directory and running

        docker build --build-arg CACHE_DATE=2018-01-08 -t iftmpa/imagine:dev .
		
Alternatively, you can also fetch the docker container from docker hub

        docker pull iftmpa/imagine:dev 
		
Finally, you can create an instance with a host-shared folder by

        docker run -i -v /host/folder:/folder/in/container -t iftmpa/imagine:dev /bin/bash
		