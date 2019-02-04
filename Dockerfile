FROM alpine:3.7

ARG VERSION_HADOLINT="v1.16.0"

ARG VERSION_PYTHON="2.7.15-r2"
ARG VERSION_PYTHON_SETUPTOOLS="33.1.1-r1"
ARG VERSION_DOCKER="17.12.1-r0"
ARG VERSION_PY_PIP="9.0.1-r1"
ARG VERSION_GROFF="1.22.3-r2"
ARG VERSION_LESS="520-r0"
ARG VERSION_MAILCAP="2.1.48-r0"
ARG VERSION_CURL="7.61.1-r1"
ARG VERSION_OPENRC="0.24.1-r4"
ARG VERSION_BUILD_BASE="0.5-r0"
ARG VERSION_LIBGIT2_DEV="0.25.1-r4"
ARG VERSION_AUTOCONF="2.69-r0"
ARG VERSION_AUTOMAKE="1.15.1-r0"
ARG VERSION_LIBTOOL="2.4.6-r4"
ARG VERSION_JQ="1.5-r5"

ARG VERSION_WHEEL="0.32.3"
ARG VERSION_DOCKER_COMPOSE="1.21.2"

COPY . cdp/

ADD https://github.com/hadolint/hadolint/releases/download/${VERSION_HADOLINT}/hadolint-Linux-x86_64 /bin/hadolint

WORKDIR /cdp

RUN apk -v --no-cache add python=$VERSION_PYTHON \
      python-dev=$VERSION_PYTHON \
      py-setuptools=$VERSION_PYTHON_SETUPTOOLS \
      docker=$VERSION_DOCKER \
      py-pip=$VERSION_PY_PIP \
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
      jq=$VERSION_JQ \
    && chmod +x /bin/hadolint \
    && ln -s /usr/lib/libcurl.so.4 /usr/lib/libcurl-gnutls.so.4 \
    && rc-update add docker boot \
    && pip install --upgrade wheel==$VERSION_WHEEL docker-compose==$VERSION_DOCKER_COMPOSE \
    && pip install -r requirements.txt \
    && python setup.py install \
    && apk -v --purge del py-pip autoconf automake libtool build-base libgit2-dev python-dev \
    && rm -rf /var/lib/apt/lists/*
