FROM ubuntu:16.04

MAINTAINER Lucas POUZAC <lucas.pouzac.pro@gmail.com>

ARG KUBE_VERSION="v1.6.7"
ARG HELM_VERSION="v2.8.2"
ARG VALIDATOR_CLI_VERSION="1.0.67"
ARG SONAR_SCANNER_VERSION="3.1.0.1141"

ARG SONAR_SCANNER_HOME=/opt/sonar-scanner

ENV PATH="${PATH}:${SONAR_SCANNER_HOME}/bin"

ADD . cdp/

RUN apt-get update \
 && apt-get install -y --no-install-recommends bsdtar curl python python-pip git openssh-client apt-transport-https ca-certificates software-properties-common python-setuptools groff \
 && curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - \
 && add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
 && apt-get update \
 && apt-get install -y --no-install-recommends docker-ce \
 && mkdir -p ${SONAR_SCANNER_HOME} \
 && curl -L https://sonarsource.bintray.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-${SONAR_SCANNER_VERSION}-linux.zip -o ${SONAR_SCANNER_HOME}/sonar-scanner.zip \
 && curl -L https://storage.googleapis.com/kubernetes-release/release/${KUBE_VERSION}/bin/linux/amd64/kubectl -o /bin/kubectl \
 && curl -L https://storage.googleapis.com/kubernetes-helm/helm-${HELM_VERSION}-linux-amd64.tar.gz | tar zxv -C /bin/ --strip-components=1 linux-amd64/helm \
 && curl -L https://github.com/Ouest-France/platform/releases/download/${VALIDATOR_CLI_VERSION}/validator-cli--x86_64-unknown-linux-gnu.tar.gz | tar zxv -C /bin/ \
 && bsdtar xvf ${SONAR_SCANNER_HOME}/sonar-scanner.zip -C ${SONAR_SCANNER_HOME} --strip-components=1 && rm ${SONAR_SCANNER_HOME}/sonar-scanner.zip \
 && chmod +x /bin/kubectl /bin/helm /bin/validator-cli \
 && mkdir -p /aws \
 && pip install wheel \
 && pip install awscli \
 && pip install docker-compose \
 && cd cdp \
 && python setup.py install \
 && apt-get purge -y bsdtar python-pip python3 python3.5-minimal libpython3.5-minimal \
 && apt -y autoremove \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
