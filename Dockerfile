FROM gcr.io/kaniko-project/executor:latest AS kaniko
FROM instrumenta/conftest:v0.18.2 AS conftest
FROM alpine:3.13.3

ARG VERSION_HADOLINT="v2.0.0"
ARG VERSION_KUBECTL="v1.17.2"
ARG VERSION_HELM="v3.4.2"
ARG VERSION_HELM2="v2.17.0"
ARG VERSION_AWSCLI="1.18.134"
ARG VERSION_SONAR_SCANNER="3.1.0.1141"
ARG DIR_SONAR_SCANNER="/root"

COPY . cdp/
COPY --from=kaniko /kaniko /kaniko
COPY --from=conftest /conftest /bin/conftest

ADD https://github.com/hadolint/hadolint/releases/download/${VERSION_HADOLINT}/hadolint-Linux-x86_64 /bin/hadolint
ADD https://storage.googleapis.com/kubernetes-release/release/${VERSION_KUBECTL}/bin/linux/amd64/kubectl /bin/kubectl

WORKDIR /cdp

RUN apk -v --no-cache add tar ca-certificates python3  python3-dev  skopeo coreutils openjdk8 \
      groff less mailcap curl openrc build-base libgit2-dev autoconf automake libtool jq git openssh maven unzip \
    && chmod +x /bin/hadolint && chmod +x /bin/kubectl \
    && if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi \
    && python -m ensurepip \
    && if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi \
    && pip install --upgrade pip setuptools \
    && ln -s /usr/lib/libcurl.so.4 /usr/lib/libcurl-gnutls.so.4 \
    && pip install --upgrade wheel \
    && pip install awscli \
    && pip install -r requirements.txt \
    && python setup.py install \
    && apk -v --no-cache --purge del py-pip autoconf automake libtool build-base libgit2-dev python3-dev \
    && curl -L https://get.helm.sh/helm-${VERSION_HELM}-linux-amd64.tar.gz | tar zxv -C /tmp/ --strip-components=1 linux-amd64/helm && mv /tmp/helm /bin/helm3 && chmod +x /bin/helm3 \
    && curl -L https://get.helm.sh/helm-${VERSION_HELM2}-linux-amd64.tar.gz | tar zxv -C /tmp/ --strip-components=1 linux-amd64/helm && mv /tmp/helm /bin/helm2 && chmod +x /bin/helm2 \
    && rm -rf /var/lib/apt/lists/* && rm -rf /var/cache/apk/* /root/.cache /usr/lib/python3.8/site-packages/pip /usr/lib/python3.8/__pycache__ /usr/lib/python3.8/site-packages/awscli/examples /usr/lib/python3.8/site-packages/config-3.8* \
    && rm /kaniko/docker* && rm -rf /cdp/..?* .[!.]*  && mkdir -p /root/.docker 

#sonar-scanner
ENV JAVA_HOME=/usr/lib/jvm/default-jvm
ENV PATH="$JAVA_HOME/bin:${PATH}"


