FROM ubuntu:18.04
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America/New_York

COPY .  /home/GazeTracking
WORKDIR /home/GazeTracking

RUN apt-get update &&  \
    apt-get install -y gnupg ca-certificates && \
    apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF &&  \
    mkdir -p /etc/apt-get/sources.list.d/ && \
    echo "deb https://download.mono-project.com/repo/ubuntu stable-bionic main" | tee /etc/apt-get/sources.list.d/mono-official-stable.list && \
    apt-get update && \
    apt-get install -y python3 python3-pip cmake \
    libsm6 libxext6 libxrender1 libfontconfig1  \
    mono-devel clang  python3-tk python3-dev && \
    python3 -m pip install --upgrade pip && \
    python3 -m pip install -r requirements.txt


