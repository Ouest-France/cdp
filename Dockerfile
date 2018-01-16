FROM alpine:latest

MAINTAINER Lucas POUZAC <lucas.pouzac.pro@gmail.com>

ENV KUBE_VERSION="v1.6.7"
ENV HELM_VERSION="v2.5.1"

ADD . cdp/

RUN apk add --update ca-certificates \
 && apk add --update -t deps curl \
 && curl -L https://storage.googleapis.com/kubernetes-release/release/${KUBE_VERSION}/bin/linux/amd64/kubectl -o /bin/kubectl \
 && curl -L https://storage.googleapis.com/kubernetes-helm/helm-${HELM_VERSION}-linux-amd64.tar.gz -o helm.tar.gz \
 && tar xvf helm.tar.gz \
 && mv linux-amd64/helm /bin \
 && rm -rf linux-amd64 helm.tar.gz \
 && chmod +x /bin/kubectl /bin/helm \
 && mkdir -p /aws \
 && apk -Uuv add groff less python py-pip \
 && pip install awscli \
 && apk add openrc --no-cache \
 && apk add docker \
 && rc-update add docker boot \
 && apk add --update git openssh-client \
 && cd cdp \
 && python setup.py install \
 && apk del --purge deps \
 && rm /var/cache/apk/*
