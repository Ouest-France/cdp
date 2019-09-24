FROM python:3.7.4-slim-buster

ARG VERSION_HADOLINT="v1.16.0"

ARG VERSION_PYTHON="3.6.8-r2"
ARG VERSION_DOCKER="18.09.8-r0"
ARG VERSION_GROFF="1.22.3-r2"
ARG VERSION_LESS="530-r0"
ARG VERSION_MAILCAP="2.1.48-r0"
ARG VERSION_CURL="7.64.0-r3"
ARG VERSION_OPENRC="0.39.2-r3"
ARG VERSION_BUILD_BASE="0.5-r1"
ARG VERSION_LIBGIT2_DEV="0.27.7-r0"
ARG VERSION_AUTOCONF="2.69-r2"
ARG VERSION_AUTOMAKE="1.16.1-r0"
ARG VERSION_LIBTOOL="2.4.6-r5"
ARG VERSION_JQ="1.6-r0"
ARG VERSION_GIT="2.20.1-r0"
ARG VERSION_WHEEL="0.33.1"
ARG VERSION_DOCKER_COMPOSE="1.23.2"

ADD https://github.com/hadolint/hadolint/releases/download/${VERSION_HADOLINT}/hadolint-Linux-x86_64 /bin/hadolint 
RUN chmod +x /bin/hadolint

RUN apt-get update \
 && apt-get install -y --no-install-recommends gcc libc6-dev make dh-autoreconf git jq  docker.io apt-transport-https curl apt-utils  openssh-client libterm-readline-gnu-perl \
 && apt -y autoremove \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


RUN python -m pip install wheel docker-compose setuptools


COPY . cdp/
WORKDIR /cdp


RUN python -m pip install -r requirements.txt \
 && python setup.py install \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*



 # && apt-get purge -y python-pip \
# && apt -y autoremove \
# && apt-get clean \