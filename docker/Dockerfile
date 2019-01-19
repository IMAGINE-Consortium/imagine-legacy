FROM ubuntu:latest

RUN apt-get update
#need python-tk???
RUN apt-get install -y build-essential python python-pip python-dev git gfortran autoconf gsl-bin libgsl-dev wget unzip vim cmake
RUN pip install numpy scipy cython astropy ipython==5.3.0
 
RUN mkdir /home/Downloads
WORKDIR /home/Downloads

# CFITSIO
RUN wget http://heasarc.gsfc.nasa.gov/FTP/software/fitsio/c/cfitsio_latest.tar.gz && tar xzf cfitsio_latest.tar.gz
WORKDIR cfitsio
RUN ./configure --prefix=/usr/local/ && make && make install 
WORKDIR ..

#FFTW
RUN wget http://www.fftw.org/fftw-3.3.8.tar.gz && tar xzf fftw-3.3.8.tar.gz
WORKDIR fftw-3.3.8
RUN ./configure --enable-threads --enable-openmp --enable-shared --prefix=/usr/local/ && make && make install
WORKDIR ..

#HEALPIX
RUN wget http://downloads.sourceforge.net/project/healpix/Healpix_3.31/Healpix_3.31_2016Aug26.tar.gz && tar xzf Healpix_3.31_2016Aug26.tar.gz 
WORKDIR Healpix_3.31
RUN echo '4\n\
	/sur/local/bin\n\
	/usr/local/include\n\
	4\n\
	y\n\
	0\n'\
	> hlpx_config
RUN  ./configure -L < hlpx_config && make 
WORKDIR ..
ENV HEALPIX_TARGET optimized_gcc 
ENV HEALPIX /home/Downloads/Healpix_3.31

#healpy
RUN pip install healpy 

#(Py)MultiNest
RUN apt-get install -y libblas3 libblas-dev liblapack3 liblapack-dev libatlas-base-dev libatlas3-base
RUN pip install numpy scipy matplotlib progressbar ipython==5.3.0

RUN git clone https://github.com/JohannesBuchner/MultiNest.git
WORKDIR MultiNest/build
RUN cmake .. && make && make install
WORKDIR ../..

RUN git clone https://github.com/JohannesBuchner/PyMultiNest.git
WORKDIR PyMultiNest
RUN python setup.py install
WORKDIR ..

#mpi4py
RUN apt-get install -y libopenmpi-dev openmpi-bin openmpi-doc
RUN pip install mpi4py 

#hdf5
RUN apt-get install -y libhdf5-100 libhdf5-dev libhdf5-openmpi-100 libhdf5-openmpi-dev hdf5-tools

#h5py
RUN wget https://api.github.com/repos/h5py/h5py/tags -O - | grep tarball_url | grep -v rc | head -n 1 | cut -d '"' -f 4 | wget -i - -O h5py.tar.gz
RUN mkdir h5py
RUN tar xzf h5py.tar.gz -C h5py --strip-components=1
WORKDIR h5py
ENV CC=mpicc
ENV HDF5_DIR=/usr/lib/x86_64-linux-gnu/hdf5/openmpi
RUN python setup.py configure --mpi
RUN python setup.py build
RUN python setup.py install
WORKDIR ..

#NIFTy
RUN git clone https://gitlab.mpcdf.mpg.de/ift/NIFTy.git
WORKDIR NIFTy
RUN python setup.py install
WORKDIR ..

#Hammurabi
RUN git clone https://bitbucket.org/hammurabicode/hamx
WORKDIR hamx
#RUN mkdir build && cd build && cmake .. && make install
#ENV HAMMURABI=/home/Downloads/hamx/bin/hamx
WORKDIR ..

#for pyhamx
RUN pip install jupyter pandas matplotlib

#IMAGINE
RUN git clone https://gitlab.mpcdf.mpg.de/ift/IMAGINE.git -b master
WORKDIR IMAGINE
RUN python setup.py install
WORKDIR ..




