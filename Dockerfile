FROM alpine:3.7

MAINTAINER Lucas POUZAC <lucas.pouzac.pro@gmail.com>

ARG VERSION_DOCKER="17.12.1-r0"
ARG VERSION_DOCKER_COMPOSE="1.21.2"
ARG VERSION_PYTHON="2.7.15-r2"
ARG VERSION_PYTHON_SETUPTOOLS="33.1.1-r1"

ADD . cdp/

RUN apk -v --update add python=$VERSION_PYTHON python-dev=$VERSION_PYTHON py-setuptools=$VERSION_PYTHON_SETUPTOOLS docker=$VERSION_DOCKER py-pip groff less mailcap curl openrc build-base libgit2-dev autoconf automake=1.15.1-r0 libtool \
    && ln -s /usr/lib/libcurl.so.4 /usr/lib/libcurl-gnutls.so.4 \
    && rc-update add docker boot \
    && pip install --upgrade wheel docker-compose==$VERSION_DOCKER_COMPOSE \
    && cd cdp \
    && pip install -r requirements.txt \
    && python setup.py install \
    && apk -v --purge del py-pip autoconf automake libtool build-base libgit2-dev python-dev \
    && rm -rf /var/lib/apt/lists/* \
    && rm /var/cache/apk/*
