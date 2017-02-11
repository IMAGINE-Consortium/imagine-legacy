FROM python:2.7-wheezy

RUN mkdir /home/Downloads
WORKDIR /home/Downloads

# CFITSIO
RUN wget http://heasarc.gsfc.nasa.gov/FTP/software/fitsio/c/cfitsio_latest.tar.gz && tar xzf cfitsio_latest.tar.gz
WORKDIR cfitsio
RUN ./configure --prefix=/usr/local/ && make && make install 
WORKDIR ..

#FFTW
RUN wget http://www.fftw.org/fftw-3.3.5.tar.gz && tar xzf fftw-3.3.5.tar.gz
WORKDIR fftw-3.3.5
RUN ./configure --enable-threads --enable-shared --prefix=/usr/local/ && make && make install
WORKDIR ..

#GSL
RUN wget http://ftp.halifax.rwth-aachen.de/gnu/gsl/gsl-2.3.tar.gz && tar xzf gsl-2.3.tar.gz
WORKDIR gsl-2.3
RUN ./configure --enable-shared --prefix=/usr/local/ && make && make install
WORKDIR ..
ENV LD_LIBRARY_PATH=/usr/local/lib

#HEALPIX
RUN wget http://downloads.sourceforge.net/project/healpix/Healpix_3.31/Healpix_3.31_2016Aug26.tar.gz && tar xzf Healpix_3.31_2016Aug26.tar.gz 
WORKDIR Healpix_3.31
COPY healpy_config healpy_config
RUN  ./configure < healpy_config && make 
WORKDIR ..
#RUN [ -r /root/.healpix/3_31_Linux/config ] && . /root/.healpix/3_31_Linux/config
ENV HEALPIX_TARGET optimized_gcc 
ENV HEALPIX /home/Downloads/Healpix_3.31

#Hammurabi
RUN wget http://downloads.sourceforge.net/project/hammurabicode/hammurabi_v3.01.tar.gz && tar xzf hammurabi_v3.01.tar.gz 
WORKDIR hammurabicode-code
COPY hammurabi_Makefile Makefile
RUN [ -r /root/.healpix/3_31_Linux/config ] && . /root/.healpix/3_31_Linux/config && make hammurabi && make clean
WORKDIR ..

#(Py)MultiNest
RUN apt-get update && apt-get install -y libblas3 libblas-dev \
					 liblapack3 liblapack-dev \
					 libatlas3-base libatlas-dev \
					 cmake \
					 build-essential \
					 git \
					 gfortran
#RUN apt-get install -y libopenmpi-dev openmpi-bin openmpi-doc
RUN pip install numpy scipy matplotlib progressbar ipython

RUN git clone https://github.com/JohannesBuchner/MultiNest.git
WORKDIR MultiNest/build
RUN cmake .. && make && make install
WORKDIR ../..

RUN git clone https://github.com/JohannesBuchner/PyMultiNest.git
WORKDIR PyMultiNest
RUN python setup.py install --user
WORKDIR ..


RUN apt-get install -y libopenmpi-dev openmpi-bin openmpi-doc
RUN pip install mpi4py

RUN pip install cython healpy 
RUN git clone https://gitlab.mpcdf.mpg.de/ift/NIFTy.git -b master
WORKDIR NIFTy
RUN python setup.py install --user
WORKDIR ..




