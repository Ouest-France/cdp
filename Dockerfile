FROM gcr.io/kaniko-project/executor:latest AS kaniko
FROM instrumenta/conftest:v0.18.2 AS conftest
FROM alpine:3.12

ARG VERSION_HADOLINT="v1.16.0"

ARG VERSION_PYTHON="3.8.5-r0"
ARG VERSION_DOCKER="19.03.12-r0"
ARG VERSION_GROFF="1.22.4-r1"
ARG VERSION_LESS="551-r0"
ARG VERSION_MAILCAP="2.1.49-r0"
ARG VERSION_CURL="7.69.1-r3"
ARG VERSION_OPENRC="0.42.1-r11"
ARG VERSION_BUILD_BASE="0.5-r2"
ARG VERSION_LIBGIT2_DEV="1.0.0-r0"
ARG VERSION_AUTOCONF="2.69-r2"
ARG VERSION_AUTOMAKE="1.16.2-r0"
ARG VERSION_LIBTOOL="2.4.6-r7"
ARG VERSION_JQ="1.6-r1"
ARG VERSION_GIT="2.26.2-r0"
ARG VERSION_OPENSSH="8.3_p1-r1"
ARG VERSION_WHEEL="0.33.1"
ARG VERSION_DOCKER_COMPOSE="1.23.2"
ARG VERSION_UNZIP="6.0-r8"
ARG VERSION_KUBECTL="v1.17.2"
ARG VERSION_HELM="v3.4.2"
ARG VERSION_AWSCLI="1.18.134"
ARG VERSION_SONAR_SCANNER="3.1.0.1141"
ARG VERSION_MAVEN="3.6.3-r0"
ARG DIR_SONAR_SCANNER="/root"

COPY . cdp/
COPY --from=kaniko /kaniko /kaniko
RUN rm /kaniko/docker*
RUN mkdir -p /root/.docker
COPY --from=conftest /conftest /bin/conftest

ADD https://github.com/hadolint/hadolint/releases/download/${VERSION_HADOLINT}/hadolint-Linux-x86_64 /bin/hadolint
ADD https://storage.googleapis.com/kubernetes-release/release/${VERSION_KUBECTL}/bin/linux/amd64/kubectl /bin/kubectl

WORKDIR /cdp

RUN apk -v --no-cache add tar ca-certificates python3=$VERSION_PYTHON \
      python3-dev=$VERSION_PYTHON \
      skopeo \
      openjdk8 \
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
      git=$VERSION_GIT \
      openssh=$VERSION_OPENSSH \
      maven=$VERSION_MAVEN \
      unzip=$VERSION_UNZIP \
    && chmod +x /bin/hadolint && chmod +x /bin/kubectl \
    && if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi \
    && python -m ensurepip \
    && if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi \
    && pip install --upgrade pip setuptools \
    && ln -s /usr/lib/libcurl.so.4 /usr/lib/libcurl-gnutls.so.4 \
    && pip install --upgrade wheel==$VERSION_WHEEL \
    && pip install awscli \
    && pip install -r requirements.txt \
    && python setup.py install \
    && apk -v --no-cache --purge del py-pip autoconf automake libtool build-base libgit2-dev python3-dev \
    && curl -L https://get.helm.sh/helm-${VERSION_HELM}-linux-amd64.tar.gz | tar zxv -C /bin/ --strip-components=1 linux-amd64/helm &&  chmod +x /bin/helm \
    && rm -rf /var/lib/apt/lists/* 


#sonar-scanner
ENV PATH="${PATH}:${DIR_SONAR_SCANNER}/sonar-scanner-${VERSION_SONAR_SCANNER}-linux/bin"
RUN curl -L https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-${VERSION_SONAR_SCANNER}-linux.zip -o ${DIR_SONAR_SCANNER}/sonar-scanner.zip && \
    unzip ${DIR_SONAR_SCANNER}/sonar-scanner.zip -d ${DIR_SONAR_SCANNER} && \
    rm ${DIR_SONAR_SCANNER}/sonar-scanner.zip && \
    rm -rf ${DIR_SONAR_SCANNER}/sonar-scanner-${VERSION_SONAR_SCANNER}-linux/jre && \
    sed -i 's/use_embedded_jre=true/use_embedded_jre=false/g' ${DIR_SONAR_SCANNER}/sonar-scanner-${VERSION_SONAR_SCANNER}-linux/bin/sonar-scanner && \ 
    ln -s ${DIR_SONAR_SCANNER}/sonar-scanner-${VERSION_SONAR_SCANNER}-linux/bin/sonar-scanner /bin/sonar-scanner

ENV JAVA_HOME=/usr/lib/jvm/default-jvm
ENV PATH="$JAVA_HOME/bin:${PATH}"

#Nettoyage
WORKDIR /cdp
RUN rm -rf /var/lib/apt/lists/* && rm -rf /var/cache/apk/* /root/.cache /usr/lib/python3.8/site-packages/pip /usr/lib/python3.8/__pycache__ /usr/lib/python3.8/site-packages/awscli/examples /usr/lib/python3.8/site-packages/config-3.8*


