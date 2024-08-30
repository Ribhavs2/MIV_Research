FROM tacc/tacc-ubuntu18-impi19.0.7-common

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys BAC6F0C353D04109

RUN apt-get update && apt-get install -y \
    python3.8 \
    python3-pip \
    python3.8-dev \
    libmpich-dev

RUN python3.8 -m pip install --upgrade pip

RUN pip install --no-cache-dir mpi4py h5py

RUN pip install --no-cache-dir MiV-OS spyking-circus

# Clean up pip cache
RUN rm -rf /root/.cache/pip
