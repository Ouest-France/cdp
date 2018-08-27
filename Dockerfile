FROM alpine:3.7

MAINTAINER Lucas POUZAC <lucas.pouzac.pro@gmail.com>

ARG VERSION_DOCKER="17.12.1-r0"
ARG VERSION_DOCKER_COMPOSE="1.21.2"
ARG VERSION_PYTHON="2.7.15-r2"

ADD . cdp/

RUN apk -v --update add python=$VERSION_PYTHON docker=$VERSION_DOCKER py-pip groff less mailcap curl openrc jq \
    && rc-update add docker boot \
    && pip install --upgrade wheel docker-compose==$VERSION_DOCKER_COMPOSE \
    && cd cdp \
    && pip install -r requirements.txt \
    && python setup.py install \
    && apk -v --purge del py-pip \
    && rm -rf /var/lib/apt/lists/* \
    && rm /var/cache/apk/*
