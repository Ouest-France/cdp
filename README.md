# SIPA/Ouest-France - Continous Delivery Pipeline (CDP) for Gitlab CI

[![Build Status](https://travis-ci.org/Ouest-France/cdp.svg?branch=master)](https://travis-ci.org/Ouest-France/cdp) ![extra](https://img.shields.io/badge/actively%20maintained-yes-ff69b4.svg?)

## Usage

```
Universal Command Line Environment for Continous Delivery Pipeline on Gitlab-CI.
Usage:
    cdp build [(-v | --verbose | -q | --quiet)] [(-d | --dry-run)] [--sleep=<seconds>]
        (--docker-image=<image_name>) (--command=<cmd>)
        [--docker-image-git=<image_name_git>] [--simulate-merge-on=<branch_name>]
        [--volume-from=<host_type>]
    cdp maven [(-v | --verbose | -q | --quiet)] [(-d | --dry-run)] [--sleep=<seconds>]
        (--docker-version=<version>) (--goals=<goals-opts>|--deploy=<type>)
        [--maven-release-plugin=<version>]
        [--docker-image-git=<image_name_git>] [--simulate-merge-on=<branch_name>]
        [--volume-from=<host_type>]
    cdp sonar [(-v | --verbose | -q | --quiet)] [(-d | --dry-run)] [--sleep=<seconds>]
        [--docker-image-sonar-scanner=<image_name_sonar_scanner>] (--preview | --publish) (--codeclimate | --sast)
        [--docker-image-git=<image_name_git>] [--simulate-merge-on=<branch_name>]
        [--volume-from=<host_type>]
    cdp docker [(-v | --verbose | -q | --quiet)] [(-d | --dry-run)] [--sleep=<seconds>]
        [--docker-image-aws=<image_name_aws>]
        [--use-docker | --use-docker-compose]
        [--image-tag-branch-name] [--image-tag-latest] [--image-tag-sha1]
        [--use-gitlab-registry | --use-aws-ecr | --use-custom-registry]
    cdp artifactory [(-v | --verbose | -q | --quiet)] [(-d | --dry-run)] [--sleep=<seconds>]
        [--image-tag-branch-name] [--image-tag-latest] [--image-tag-sha1]
        (--put=<file> | --delete=<file>)
    cdp k8s [(-v | --verbose | -q | --quiet)] [(-d | --dry-run)] [--sleep=<seconds>]
        [--docker-image-kubectl=<image_name_kubectl>] [--docker-image-helm=<image_name_helm>] [--docker-image-aws=<image_name_aws>]
        [--image-tag-branch-name | --image-tag-latest | --image-tag-sha1]
        (--use-gitlab-registry | --use-aws-ecr | --use-custom-registry)
        [--values=<files>]
        [--delete-labels=<minutes>]
        [--namespace-project-branch-name | --namespace-project-name]
        [--create-default-helm] [--internal-port=<port>] [--deploy-spec-dir=<dir>]
        [--timeout=<timeout>]
        [--volume-from=<host_type>]
    cdp validator-server [(-v | --verbose | -q | --quiet)] [(-d | --dry-run)] [--sleep=<seconds>]
        [--path=<path>]
        (--validate-configurations)
        [--namespace-project-branch-name | --namespace-project-name]
    cdp (-h | --help | --version)
Options:
    -h, --help                                                 Show this screen and exit.
    -v, --verbose                                              Make more noise.
    -q, --quiet                                                Make less noise.
    -d, --dry-run                                              Simulate execution.
    --codeclimate                                              Codeclimate mode.
    --command=<cmd>                                            Command to run in the docker image.
    --create-default-helm                                      Create default helm for simple project (One docker image).
    --delete-labels=<minutes>                                  Add namespace labels (deletable=true deletionTimestamp=now + minutes) for external cleanup.
    --delete=<file>                                            Delete file in artifactory.
    --deploy-spec-dir=<dir>                                    k8s deployment files [default: charts].
    --deploy=<type>                                            'release' or 'snapshot' - Maven command to deploy artifact.
    --docker-image-aws=<image_name_aws>                        Docker image which execute git command [default: ouestfrance/cdp-aws:1.15.19].
    --docker-image-git=<image_name_git>                        Docker image which execute git command [default: ouestfrance/cdp-git:2.15.0].
    --docker-image-helm=<image_name_helm>                      Docker image which execute helm command [default: ouestfrance/cdp-helm:2.8.2-1.6.7].
    --docker-image-kubectl=<image_name_kubectl>                Docker image which execute kubectl command [default: ouestfrance/cdp-kubectl:1.6.7].
    --docker-image-sonar-scanner=<image_name_sonar_scanner>    Docker image which execute sonar-scanner command [default: ouestfrance/cdp-sonar-scanner:3.1.0].
    --docker-image=<image_name>                                Specify docker image name for build project.
    --docker-version=<version>                                 Specify maven docker version [default: 3.5-jdk-8].
    --goals=<goals-opts>                                       Goals and args to pass maven command.
    --image-tag-branch-name                                    Tag docker image with branch name or use it [default].
    --image-tag-latest                                         Tag docker image with 'latest'  or use it.
    --image-tag-sha1                                           Tag docker image with commit sha1  or use it.
    --internal-port=<port>                                     Internal port used if --create-default-helm is activate [default: 8080]
    --maven-release-plugin=<version>                           Specify maven-release-plugin version [default: 2.5.3].
    --namespace-project-branch-name                            Use project and branch name to create k8s namespace or choice environment host [default].
    --namespace-project-name                                   Use project name to create k8s namespace or choice environment host.
    --path=<path>                                              Path to validate [default: configurations].
    --preview                                                  Run issues mode (Preview).
    --publish                                                  Run publish mode (Analyse).
    --put=<file>                                               Put file to artifactory.
    --sast                                                     Static Application Security Testing mode.
    --simulate-merge-on=<branch_name>                          Build docker image with the merge current branch on specify branch (no commit).
    --sleep=<seconds>                                          Time to sleep int the end (for debbuging) in seconds [default: 0].
    --timeout=<timeout>                                        Time in seconds to wait for any individual kubernetes operation [default: 600].
    --use-aws-ecr                                              Use AWS ECR from k8s configuration for pull/push docker image.
    --use-custom-registry                                      Use custom registry for pull/push docker image.
    --use-docker                                               Use docker to build / push image [default].
    --use-docker-compose                                       Use docker-compose to build / push image.
    --use-gitlab-registry                                      Use gitlab registry for pull/push docker image [default].
    --validate-configurations                                  Validate configurations schema of BlockProvider.
    --values=<files>                                           Specify values in a YAML file (can specify multiple separate by comma). The priority will be given to the last (right-most) file specified.
    --volume-from=<host_type>                                  Volume type of sources - docker or k8s [default: k8s]
```

### Prerequisites

Gitlab >= 10.8

```yaml
available:
  - CDP_DOCKER_HOST_INTERNAL – IP of docker host. Could be used in your tests if necessary.

maven:
 - MAVEN_OPTS – Add option for maven command (Optional)
 --deploy=x:
    - CDP_REPOSITORY_USERNAME – Username for read/write in maven repository
    - CDP_REPOSITORY_PASSWORD – Password
    - CDP_REPOSITORY_URL – URL of maven repository
 --deploy=snapshot:
    - CDP_REPOSITORY_MAVEN_SNAPSHOT – Repository for snapshot (example libs-snapshot-local)
 --deploy=release:
    - CDP_REPOSITORY_MAVEN_RELEASE – Repository for release (example libs-release-local)

sonar:
 - CDP_SONAR_LOGIN – Sonar access token (scope Administer Quality Profiles / Administer Quality Gates).
 - CDP_SONAR_URL – Sonar url access.
 - GITLAB_USER_TOKEN – Gitlab access token (scope api).
 - sonar-project.properties - Add this file to the root of the project. If not present, -Dsonar.projectKey=$CI_PROJECT_PATH and -Dsonar.sources=.

docker:
 --use-docker:
    - File Dockerfile required at the root of the project.
 --use-docker-compose:
    - File docker-compose.yml required at the root of the project.

k8s:
  without: --create-default-helm:
    - Helm and k8s files to configure the deployment. Must be present in the directory configured by the --deploy-spec-dir=<dir> option.

docker|k8s:
  --use-aws-ecr:
    - AWS_ACCESS_KEY_ID (Gitlab-runner env var) – AWS access key.
    - AWS_SECRET_ACCESS_KEY (Gitlab-runner env var) – AWS secret key. Access and secret key variables override credentials stored in credential and config files.
    - AWS_DEFAULT_REGION – The region to use. Overrides config/env settings.
  --use-custom-registry:
    - CDP_CUSTOM_REGISTRY (Gitlab-runner env var) – Custom docker registry (host:port).
    - CDP_CUSTOM_REGISTRY_TOKEN (Gitlab-runner env var) – Access token used for authentication on custom docker registry.
    - CDP_CUSTOM_REGISTRY_TOKEN_READ_ONLY (Gitlab-runner env var) – Read only access token used for authentication on custom docker registry.
    - CDP_CUSTOM_REGISTRY_USER (Gitlab-runner env var) – User used for authentication on custom docker registry.
  --use-gitlab-registry:
    - Deploy token with the name gitlab-deploy-token and the scope read_registry must be created for each project.

artifactory:
  --put=<file>|--delete=<file>:
    - CDP_ARTIFACTORY_PATH (Gitlab-runner env var) – Repository path used for put or delete file.
    - CDP_ARTIFACTORY_TOKEN (Gitlab-runner env var) – Access token used by X-JFrog-Art-Api header for autentication on artifactory.

validator-server:
  - CDP_BP_VALIDATOR_HOST – Validator server access (example - https://validator.example.com)
```

### Example .gitlab-ci.yml file

```yaml
stages:
  ...
  - build
  - quality
  - package
  - deploy
  ...

build:
  image: ouestfrance/cdp:latest
  stage: build
  script:
    - cdp build --docker-image=maven:3.5-jdk-8 --command='mvn clean verify' --simulate-merge-on=develop
  artifacts:
    paths:
    - target/*.jar

codeclimate:
  image: ouestfrance/cdp:latest
  stage: quality
  script:
    - cdp sonar --preview --codeclimate --simulate-merge-on=develop
  artifacts:
    paths:
    - codeclimate.json

sast:
  image: ouestfrance/cdp:latest
  stage: quality
  script:
    - cdp sonar --preview --sast --simulate-merge-on=develop
  artifacts:
    paths:
    - gl-sast-report.json

package:
  image: ouestfrance/cdp:latest
  stage: package
  script:
    - cdp docker --image-tag-branch-name --use-gitlab-registry
    - cdp artifactory --image-tag-branch-name --put=conf/example.yaml

deploy_review:
  variables:
    DNS_SUBDOMAIN: { ingress.k8s }
  image: ouestfrance/cdp:latest
  stage: deploy
  script:
    - cdp k8s --use-gitlab-registry --namespace-project-branch-name --image-tag-branch-name
  environment:
    name: review/$CI_COMMIT_REF_NAME
    url: http://$CI_COMMIT_REF_SLUG.$CI_PROJECT_NAME.$DNS_SUBDOMAIN

deploy_staging:
  variables:
    DNS_SUBDOMAIN: { ingress.k8s }
  image: ouestfrance/cdp:latest
  stage: deploy
  script:
    - cdp k8s --use-gitlab-registry --namespace-project-name --image-tag-sha1 --values=values.staging.yaml
  environment:
    name: staging
    url: http://$CI_PROJECT_NAME.$DNS_SUBDOMAIN
```

### Environment variables set by the CDP

When you use the `docker build --use-docker-compose` command, you may need information from the CDP context. Below, the environment variables made available by the CDP for use in the docker-compose.yml.

```yaml
CDP_REGISTRY:        --use-gitlab-registry: env['CI_REGISTRY'] | --use-aws-ecr: result from 'aws ecr get-login ...' command | --use-custom-registry: env['CDP_CUSTOM_REGISTRY'] + '/' + env['CI_PROJECT_PATH'].lower()
CDP_TAG:             --image-tag-branch-name: env['CI_COMMIT_REF_NAME'] | --image-tag-latest: 'latest'| --image-tag-sha1:  env['CI_COMMIT_SHA']
```

#### docker-compose.yml sample

```yaml
version: '3'
services:
  nginx:
    image: ${CDP_REGISTRY:-local}/my-nginx-project-name:${CDP_TAG:-latest}
    ...
  php:
    image: ${CDP_REGISTRY:-local}/my-php-project-name:${CDP_TAG:-latest}
    ...
...
```


### Helm charts

When you use the `docker k8s` command, you may need information from the CDP context. Below, the variables made available by the CDP for use in the helm context.

```yaml
namespace:           Name of kubernetes namespace, based on the following options: [ --namespace-project-branch-name | --namespace-project-name ]
ingress.host:        Ingress, based on the following options : [ --namespace-project-branch-name | --namespace-project-name ]
image.commit.sha:    First 8 characters of sha1 corresponding to the current commit.
image.registry:      Docker image registry, based on the following options: [ --use-gitlab-registry | --use-aws-ecr | --use-custom-registry ]
image.repository:    Name of the repository corresponding to the CI_PROJECT_PATH environment variable in lowercase.
image.tag:           Docker image tag, based on the following options: [ --image-tag-branch | --image-tag-latest | --image-tag-sha1 ]
image.pullPolicy:    Docker pull policy, based on the following options: [ --image-tag-branch | --image-tag-latest | --image-tag-sha1 ]
```

#### charts/deployment.yaml sample

```yaml
apiVersion: extensions/v1beta1
kind: Deployment
spec:
  template:
    spec:
      containers:
        - name: {{ template "nginx.name" . }}-{{ .Values.image.commit.sha }}
          image: "{{ .Values.image.registry }}/{{ .Values.image.repository }}/my-nginx-project-name:{{ .Values.image.tag }}"
          ...
        - name: {{ template "php.name" . }}-{{ .Values.image.commit.sha }}
          image: "{{ .Values.image.registry }}/{{ .Values.image.repository }}/my-php-project-name:{{ .Values.image.tag }}"
          ...
...
```

## Development

### Prerequisites

- python 2.7
- pip 2.7

### Tests

```sh
python setup.py test
```
### Installations

```sh
pip install -r requirements.txt
sudo python setup.py install

cdp --help
```

## TODO

Vault usage for token and password storage
