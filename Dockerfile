FROM ubuntu:16.04

MAINTAINER Lucas POUZAC <lucas.pouzac.pro@gmail.com>

ENV KUBE_VERSION="v1.6.7"
ENV HELM_VERSION="v2.8.2"
ENV VALIDATOR_CLI_VERSION="1.0.67"

ADD . cdp/

RUN apt-get update \
 && apt-get install -y --no-install-recommends curl python python-pip docker git openssh-client apt-transport-https ca-certificates software-properties-common python-setuptools groff \
 && curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - \
 && add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
 && apt-get update \
 && apt-get install -y --no-install-recommends docker-ce \
 && curl -L https://storage.googleapis.com/kubernetes-release/release/${KUBE_VERSION}/bin/linux/amd64/kubectl -o /bin/kubectl \
 && curl -L https://storage.googleapis.com/kubernetes-helm/helm-${HELM_VERSION}-linux-amd64.tar.gz -o helm.tar.gz \
 && curl -L https://github.com/Ouest-France/platform/releases/download/${VALIDATOR_CLI_VERSION}/validator-cli--x86_64-unknown-linux-gnu.tar.gz -o validator-cli.tar.gz \
 && tar xvf helm.tar.gz \
 && tar xvf validator-cli.tar.gz \
 && mv linux-amd64/helm validator-cli /bin \
 && rm -rf linux-amd64 helm.tar.gz validator-cli.tar.gz \
 && chmod +x /bin/kubectl /bin/helm /bin/validator-cli \
 && mkdir -p /aws \
 && pip install wheel \
 && pip install awscli \
 && pip install docker-compose \
 && cd cdp \
 && python setup.py install \
 && apt-get purge -y python-pip python3 python3.5-minimal libpython3.5-minimal \
 && apt -y autoremove \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


ADD entrypoint.sh /entrypoint.sh
RUN chmod 755 /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
