FROM ubuntu:16.04

MAINTAINER Lucas POUZAC <lucas.pouzac.pro@gmail.com>

ARG VALIDATOR_CLI_VERSION="1.0.67"

ADD . cdp/

RUN apt-get update \
 && apt-get install -y --no-install-recommends curl python python-pip openssh-client apt-transport-https ca-certificates software-properties-common python-setuptools groff \
 && curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - \
 && add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
 && apt-get update \
 && apt-get install -y --no-install-recommends docker-ce \
 && curl -L https://github.com/Ouest-France/platform/releases/download/${VALIDATOR_CLI_VERSION}/validator-cli--x86_64-unknown-linux-gnu.tar.gz | tar zxv -C /bin/ \
 && chmod +x /bin/validator-cli \
 && mkdir -p /aws \
 && pip install wheel \
 && pip install docker-compose \
 && cd cdp \
 && python setup.py install \
 && apt-get purge -y python-pip python3 python3.5-minimal libpython3.5-minimal \
 && apt -y autoremove \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
