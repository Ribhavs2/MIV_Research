FROM python:3.8-slim
WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    git

RUN pip install MiV-OS

RUN pip install spyking-circus

# COPY . /app

# ENV PATH="/miv-os/bin:${PATH}"

# CMD ["python", "your_script.py"]
