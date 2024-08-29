FROM python:3.8-slim
WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    libmpich-dev

RUN pip install MiV-OS

RUN pip install spyking-circus
