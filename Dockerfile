FROM alpine:3.14

ARG VERSION_HADOLINT="v1.16.0"

ARG VERSION_PYTHON="3.9.5-r1"
ARG VERSION_DOCKER="20.10.7-r2"
ARG VERSION_GROFF="1.22.4-r1"
ARG VERSION_LESS="581-r1"
ARG VERSION_MAILCAP="2.1.52-r0"
ARG VERSION_CURL="7.79.1-r0"
ARG VERSION_OPENRC="0.43.3-r1"
ARG VERSION_BUILD_BASE="0.5-r2"
ARG VERSION_LIBGIT2_DEV="1.1.0-r2"
ARG VERSION_AUTOCONF="2.71-r0"
ARG VERSION_AUTOMAKE="1.16.3-r0"
ARG VERSION_LIBTOOL="2.4.6-r7"
ARG VERSION_JQ="1.6-r1"
ARG VERSION_GIT="2.32.0-r0"
ARG VERSION_WHEEL="0.33.1"
ARG VERSION_DOCKER_COMPOSE="1.23.2"
ARG VERSION_UNZIP="6.0-r9"
COPY . cdp/

ADD https://github.com/hadolint/hadolint/releases/download/${VERSION_HADOLINT}/hadolint-Linux-x86_64 /bin/hadolint

WORKDIR /cdp

RUN apk -v --no-cache add tar python3=$VERSION_PYTHON \
      python3-dev=$VERSION_PYTHON \
      groff=$VERSION_GROFF \
      less=$VERSION_LESS \
      mailcap=$VERSION_MAILCAP \
      curl=$VERSION_CURL \
      openrc=$VERSION_OPENRC \
      build-base=$VERSION_BUILD_BASE \
      libgit2-dev=$VERSION_LIBGIT2_DEV \
      autoconf=$VERSION_AUTOCONF \
      automake=$VERSION_AUTOMAKE \
      libtool=$VERSION_LIBTOOL \
      docker=$VERSION_DOCKER \
      jq=$VERSION_JQ \
      git=$VERSION_GIT \
      unzip=$VERSION_UNZIP \
    && chmod +x /bin/hadolint \
    && if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi \
    && python -m ensurepip \
    && if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi \
    && pip install --upgrade pip setuptools \
    && rm -r /root/.cache \
    && ln -s /usr/lib/libcurl.so.4 /usr/lib/libcurl-gnutls.so.4 \
    && rc-update add docker boot \
    && pip install --upgrade wheel==$VERSION_WHEEL docker-compose==$VERSION_DOCKER_COMPOSE \
    && pip install -r requirements.txt \
    && python setup.py install \
    && apk -v --no-cache --purge del py-pip autoconf automake libtool build-base libgit2-dev python3-dev \
    && rm -rf /var/lib/apt/lists/*
