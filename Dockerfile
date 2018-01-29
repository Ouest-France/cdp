FROM alpine:latest

MAINTAINER Lucas POUZAC <lucas.pouzac.pro@gmail.com>

ENV KUBE_VERSION="v1.6.7"
ENV HELM_VERSION="v2.5.1"
ENV VALIDATOR_CLI_VERSION="1.0.44"

ADD . cdp/

RUN apk add --update ca-certificates \
 && apk add --update -t deps curl \
 && curl -L https://storage.googleapis.com/kubernetes-release/release/${KUBE_VERSION}/bin/linux/amd64/kubectl -o /bin/kubectl \
 && curl -L https://storage.googleapis.com/kubernetes-helm/helm-${HELM_VERSION}-linux-amd64.tar.gz -o helm.tar.gz \
 && curl -L https://github.com/Ouest-France/platform/releases/download/${VALIDATOR_CLI_VERSION}/validator-cli--x86_64-unknown-linux-gnu.tar.gz -o validator-cli.tar.gz \
 && tar xvf helm.tar.gz \
 && tar xvf validator-cli.tar.gz \
 && mv linux-amd64/helm validator-cli /bin \
 && rm -rf linux-amd64 helm.tar.gz validator-cli.tar.gz \
 && chmod +x /bin/kubectl /bin/helm /bin/validator-cli \
 && mkdir -p /aws \
 && apk -Uuv add groff less python py-pip \
 && pip install awscli \
 && apk add openrc --no-cache \
 && apk add docker \
 && rc-update add docker boot \
 && pip install docker-compose \
 && apk add --update git openssh-client \
 && cd cdp \
 && python setup.py install \
 && apk del --purge deps \
 && rm /var/cache/apk/*
