FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
run ln -snf /bin/bash /bin/sh

RUN apt-get update && apt-get -y install gawk wget git diffstat unzip texinfo gcc build-essential \
        chrpath socat cpio python3 python3-pip python3-pexpect xz-utils debianutils iputils-ping \
         python3-git python3-jinja2 libegl1-mesa libsdl1.2-dev python3-subunit mesa-common-dev \
         zstd liblz4-tool file locales libacl1 npm python3-venv

RUN locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8 LANGUAGE=en_US:en LC_ALL=en_US.UTF-8

RUN useradd -m ds-build \
    && echo "ds-build:ds-build" | chpasswd \
    && adduser ds-build sudo

WORKDIR /yocto

USER ds-build

VOLUME ["/yocto"]

CMD ["/bin/bash"]




