FROM python:2.7.15-alpine3.7

MAINTAINER Lucas POUZAC <lucas.pouzac.pro@gmail.com>

ARG VERSION_VALIDATOR_CLI="1.0.67"
ARG VERSION_DOCKER="17.12.1-r0"
ARG VERSION_DOCKER_COMPOSE="1.21.2"

ADD . cdp/

RUN apk -v --update add docker=$VERSION_DOCKER py-pip groff less mailcap curl openrc \
    && rc-update add docker boot \
    && pip install --upgrade wheel docker-compose==$VERSION_DOCKER_COMPOSE \
    && curl -L https://github.com/Ouest-France/platform/releases/download/${VERSION_VALIDATOR_CLI}/validator-cli--x86_64-unknown-linux-gnu.tar.gz | tar zxv -C /bin/ \
    && chmod +x /bin/validator-cli \
    && cd cdp \
    && python setup.py install \
    && apk -v --purge del py-pip curl \
    && rm -rf /var/lib/apt/lists/* \
    && rm /var/cache/apk/*
