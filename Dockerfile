FROM tacc/tacc-ubuntu18-impi19.0.7-common

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys BAC6F0C353D04109

RUN apt-get update && apt-get install -y \
    python3.8 \
    python3-pip \
    python3.8-dev \
    # libmpich-dev \
    wget \
    git \
    vim

RUN python3.8 -m pip install --upgrade pip

# Download and install HDF5
ENV HDF5_VERSION=1.12.0
RUN wget https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.12/hdf5-$HDF5_VERSION/src/hdf5-$HDF5_VERSION.tar.gz \
    && tar -xzf hdf5-$HDF5_VERSION.tar.gz \
    && cd hdf5-$HDF5_VERSION \
    && ./configure --enable-parallel --enable-shared --prefix=/usr/local \
    && make -j$(nproc) \
    && make install \
    && cd .. \
    && rm -rf hdf5-$HDF5_VERSION hdf5-$HDF5_VERSION.tar.gz

ENV CC="mpicc"
ENV HDF5_MPI="ON"

RUN pip install --no-cache-dir mpi4py 

ENV LD_LIBRARY_PATH=/usr/local/lib:${LD_LIBRARY_PATH}

RUN pip install --no-cache-dir --no-binary=h5py h5py

# RUN pip install --no-cache-dir MiV-OS spyking-circus
RUN pip install --no-cache-dir MiV-OS

RUN pip install git+https://github.com/skim0119/spyking-circus.git

# Test scripts to verify installation
COPY test_mpi.py /test_mpi.py
COPY test_parallel_h5py.py /test_parallel_h5py.py
RUN mpiexec -n 4 python3.8 /test_mpi.py
RUN mpiexec -n 4 python3.8 /test_parallel_h5py.py

# RUN pip install --no-cache-dir nose
# RUN git clone https://github.com/spyking-circus/spyking-circus.git /opt/spyking-circus
# RUN nosetests /opt/spyking-circus/tests/



# Clean up pip cache
RUN rm -rf /root/.cache/pip
