
# SIPA/Ouest-France - Continuous Delivery Pipeline (CDP) for Gitlab CI

[![Build Status](https://travis-ci.org/Ouest-France/cdp.svg?branch=master)](https://travis-ci.org/Ouest-France/cdp) ![extra](https://img.shields.io/badge/actively%20maintained-yes-ff69b4.svg?)

## Usage

```python
Universal Command Line Environment for Continuous Delivery Pipeline on Gitlab-CI.
Usage:
    cdp build [(-v | --verbose | -q | --quiet)] [(-d | --dry-run)] [--sleep=<seconds>]
        (--command=<cmd>) [--simulate-merge-on=<branch_name>]
        [--docker-image=<image_name>]  [--docker-image-git=<image_name_git>] [--volume-from=<host_type>]         
    cdp maven [(-v | --verbose | -q | --quiet)] [(-d | --dry-run)] [--sleep=<seconds>]
        (--goals=<goals-opts>|--deploy=<type>) [--simulate-merge-on=<branch_name>]
        [--maven-release-plugin=<version>]
        [--use-gitlab-registry | --use-aws-ecr | --use-custom-registry | --use-registry=<registry_name>]
        [--altDeploymentRepository=<repository_name>]
        [--login-registry=<registry_name>]
        [--docker-image-maven=<image_name_maven>|--docker-version=<version>] [--docker-image-git=<image_name_git>] [--volume-from=<host_type>]
    cdp docker [(-v | --verbose | -q | --quiet)] [(-d | --dry-run)] [--sleep=<seconds>]
        (--use-gitlab-registry | --use-aws-ecr | --use-custom-registry | --use-registry=<registry_name>)
        [--use-docker | --use-docker-compose]
        [--image-tag-branch-name] [--image-tag-latest] [--image-tag-sha1] [--image-tag=<tag>]
        [--build-context=<path>]
        [--build-arg=<arg> ...]
        [--build-file=<buildFile>]
        [--login-registry=<registry_name>]
        [--docker-build-target=<target_name>] [--docker-image-aws=<image_name_aws>]
    cdp artifactory [(-v | --verbose | -q | --quiet)] [(-d | --dry-run)] [--sleep=<seconds>]
        (--put=<file> | --delete=<file>)
        [--image-tag-branch-name] [--image-tag-latest] [--image-tag-sha1] [--image-tag=<tag>]
    cdp k8s [(-v | --verbose | -q | --quiet)] [(-d | --dry-run)] [--sleep=<seconds>]
        (--use-gitlab-registry | --use-aws-ecr | --use-custom-registry | --use-registry=<registry_name>)
        [--helm-version=<version>]
        [--image-tag-branch-name | --image-tag-latest | --image-tag-sha1 | --image-tag=<tag>] 
        [--image-prefix-tag=<tag>]
        [(--create-gitlab-secret)]
        [(--create-gitlab-secret-hook)]
        [(--use-docker-compose)] 
        [--build-file=<buildFile>]
        [--values=<files>]
        [--delete-labels=<minutes>]
        [--namespace-project-name | --namespace-name=<namespace_name>] [--namespace-project-branch-name]
        [--create-default-helm] [--internal-port=<port>] [--deploy-spec-dir=<dir>]
        [--helm-migration=[true|false]]
        [--chart-repo=<repo>] [--use-chart=<chart:branch>]
        [--timeout=<timeout>]
        [--tiller-namespace]
        [--release-project-branch-name | --release-project-env-name | --release-project-name | --release-shortproject-name | --release-namespace-name | --release-custom-name=<release_name>]
        [--image-pull-secret] [--ingress-tlsSecretName=<secretName>]
        [--conftest-repo=<repo:dir:branch>] [--no-conftest] [--conftest-namespaces=<namespaces>]
        [--docker-image-kubectl=<image_name_kubectl>] [--docker-image-helm=<image_name_helm>] [--docker-image-aws=<image_name_aws>] [--docker-image-conftest=<image_name_conftest>]
        [--volume-from=<host_type>]
    cdp conftest [(-v | --verbose | -q | --quiet)] (--deploy-spec-dir=<dir>) 
        [--conftest-repo=<gitlab repo>] [--no-conftest] [--volume-from=<host_type>] [--conftest-namespaces=<namespaces>] [--docker-image-conftest=<image_name_conftest>] 
    cdp validator-server [(-v | --verbose | -q | --quiet)] [(-d | --dry-run)] [--sleep=<seconds>]
        (--validate-configurations)
        [--path=<path>]
        [--namespace-project-branch-name ][ --namespace-project-name]
    cdp (-h | --help | --version)
Options:
    -h, --help                                                 Show this screen and exit.
    -v, --verbose                                              Make more noise.
    -q, --quiet                                                Make less noise.
    -d, --dry-run                                              Simulate execution.
    --altDeploymentRepository=<repository_name>                Use custom Maven Dpeloyement repository
    --build-arg=<arg>                                          Build args for docker
    --build-context=<path>                                     Specify the docker building context [default: .].
    --build-file=<buildFile>                                   Specify the file to build multiples images [default: cdp-build-file.yml].
    --command=<cmd>                                            Command to run in the docker image.
    --chart-repo=<repo>                                        Path of the repository of default charts
    --use-chart=<chart:branch>                                 Name of the pre-defined chart to use. Format : name or name:branch
    --conftest-repo=<repo:dir:branch>                          Gitlab project with generic policies for conftest [default: ]. CDP_CONFTEST_REPO is used if empty. none value overrides env var. See notes.
    --conftest-namespaces=<namespaces>                         Namespaces (comma separated) for conftest [default: ]. CDP_CONFTEST_NAMESPACES is used if empty.
    --create-default-helm                                      Create default helm for simple project (One docker image).
    --create-gitlab-secret                                     Create a secret from gitlab env starting with CDP_SECRET_<Environnement>_ where <Environnement> is the gitlab env from the job ( or CI_ENVIRONNEMENT_NAME )
    --create-gitlab-secret-hook                                Create gitlab secret with hook
    --delete-labels=<minutes>                                  Add namespace labels (deletable=true deletionTimestamp=now + minutes) for external cleanup.
    --delete=<file>                                            Delete file in artifactory.
    --deploy-spec-dir=<dir>                                    k8s deployment files [default: charts].
    --deploy=<type>                                            'release' or 'snapshot' - Maven command to deploy artifact.
    --docker-image-aws=<image_name_aws>                        Docker image which execute git command [DEPRECATED].
    --docker-image-git=<image_name_git>                        Docker image which execute git command [DEPRECATED].
    --docker-image-helm=<image_name_helm>                      Docker image which execute helm command [DEPRECATED].
    --docker-image-kubectl=<image_name_kubectl>                Docker image which execute kubectl command [DEPRECATED].
    --docker-image-maven=<image_name_maven>                    Docker image which execute mvn command [DEPRECATED].
    --docker-image-conftest=<image_name_conftest>              Docker image which execute conftest command [DEPRECATED].
    --docker-image=<image_name>                                Specify docker image name for build project [DEPRECATED].
    --docker-build-target=<target_name>                        Specify target in multi stage build
    --docker-version=<version>                                 Specify maven docker version. [DEPRECATED].
    --goals=<goals-opts>                                       Goals and args to pass maven command.
    --helm-version=<version>                                   Major version of Helm. [default: 3]
    --helm-migration=<true|false>                              Do helm 2 to Helm 3 migration
    --image-pull-secret                                        Add the imagePullSecret value to use the helm --wait option instead of patch and rollout [DEPRECATED]
    --image-tag-branch-name                                    Tag docker image with branch name or use it [default].
    --image-tag-latest                                         Tag docker image with 'latest'  or use it.
    --image-tag-sha1                                           Tag docker image with commit sha1  or use it.
    --image-tag=<tag>                                          Tag name
    --image-prefix-tag=<tag>                                   Tag prefix for docker image.
    --ingress-tlsSecretName=<secretName>                       Name of the tls secret for ingress 
    --internal-port=<port>                                     Internal port used if --create-default-helm is activate [default: 8080]
    --login-registry=<registry_name>                           Login on specific registry for build image [default: none].
    --maven-release-plugin=<version>                           Specify maven-release-plugin version [default: 2.5.3].
    --namespace-project-branch-name                            Use project and branch name to create k8s namespace or choice environment host [DEPRECATED].
    --namespace-project-name                                   Use project name to create k8s namespace or choice environment host.
    --namespace-name=<namespace_name>                          Use <namespace name> to create k8s namespace.
    --no-conftest                                              Do not run conftest validation tests.
    --path=<path>                                              Path to validate [default: configurations].
    --put=<file>                                               Put file to artifactory.
    --release-custom-name=<release_name>                       Customize release name with namespace-name-<release_name>
    --release-namespace-name                                   Force the release to be created with the namespace name. Same as  to --release-project-name if --namespace-name is not set. [default]
    --release-project-branch-name                              Force the release to be created with the project branch name.
    --release-project-env-name                                 Force the release to be created with the job env name.define in gitlab
    --release-shortproject-name                                Force the release to be created with the shortname (first letters of word + id) of the Gitlab project
    --release-project-name                                     Force the release to be created with the name of the Gitlab project
    --simulate-merge-on=<branch_name>                          Build docker image with the merge current branch on specify branch (no commit).
    --sleep=<seconds>                                          Time to sleep int the end (for debbuging) in seconds [default: 0].
    --timeout=<timeout>                                        Time in seconds to wait for any individual kubernetes operation [default: 600].
    --tiller-namespace                                         Force the tiller namespace to be the same as the pod namespace [DEPRECATED]
    --use-aws-ecr                                              DEPRECATED - Use AWS ECR from k8s configuration for pull/push docker image.
    --use-custom-registry                                      DEPRECATED - Use custom registry for pull/push docker image.
    --use-docker                                               Use docker to build / push image [default].
    --use-docker-compose                                       Use docker-compose to build / push image / retag container [DEPRECATED]
    --use-gitlab-registry                                      DEPRECATED - Use gitlab registry for pull/push docker image [default].
    --use-registry=<registry_name>                             Use registry for pull/push docker image (none, aws-ecr, gitlab, harbor or custom name for load specifics environments variables) [default: none].
    --validate-configurations                                  Validate configurations schema of BlockProvider.
    --values=<files>                                           Specify values in a YAML file (can specify multiple separate by comma). The priority will be given to the last (right-most) file specified.
    --volume-from=<host_type>                                  Volume type of sources - docker, k8s, local or docker volume description (dir:mount) [default: k8s]
```
### _Prerequisites_

Gitlab >= 10.8

```yaml
maven:
 - MAVEN_OPTS – Add option for maven command (Optional)
 --deploy=x:
    - CDP_REPOSITORY_USERNAME – Username for read/write in maven repository
    - CDP_REPOSITORY_PASSWORD – Password
    - CDP_REPOSITORY_URL – URL of maven repository
    - CDP_PLUGINREPOSITORY_URL – URL of maven plugin repository
 --deploy=snapshot:
    - CDP_REPOSITORY_MAVEN_SNAPSHOT – Repository for snapshot (example libs-snapshot-local)
    - CDP_PLUGINREPOSITORY_MAVEN_SNAPSHOT – Plugin repository for snapshot (example libs-snapshot-local)
 --deploy=release:
    - CDP_REPOSITORY_MAVEN_RELEASE – Repository for release (example libs-release-local)
    - CDP_PLUGINREPOSITORY_MAVEN_RELEASE – Plugin repository for release (example libs-release-local)

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
 --login-registry=<registry_name>:
    - CDP_<REGISTRY_NAME>_REGISTRY (Gitlab-runner env var) – docker registry (host:port).
    - CDP_<REGISTRY_NAME>_REGISTRY_TOKEN (Gitlab-runner env var) – Access token used for authentication on docker registry.
    - CDP_<REGISTRY_NAME>_REGISTRY_TOKEN_READ_ONLY (Gitlab-runner env var) – Read only access token used for authentication on docker registry.
    - CDP_<REGISTRY_NAME>_REGISTRY_USER (Gitlab-runner env var) – User used for authentication on docker registry.

k8s:
    - Helm and k8s files to configure the deployment. Must be present in the directory configured by the --deploy-spec-dir=<dir> option.
    -- repo-chart : Path of the charts repository in Gitlab
    --use-chart: Name of chart in the repo to use. Can be written as chart:version where version is the tag or branch in the repository

docker|k8s:
  - CDP_DNS_SUBDOMAIN – Specify the subdomain of k8s cluster (set by environment variable in runner).
  - CDP_IMAGE_PULL_SECRET – Add the imagePullSecret value to use the helm --wait option instead of patch and rollout.
  - CDP_NAMESPACE – if value = 'project-name', force usage of project name to create k8s namespace.
  - CDP_IMAGE_PREFIX_TAG - Prefix of the tag when pushing to registry (for --image-tag-sha1 only)
  --use-registry=aws-ecr:
    - AWS_ACCESS_KEY_ID (Gitlab-runner env var) – AWS access key.
    - AWS_SECRET_ACCESS_KEY (Gitlab-runner env var) – AWS secret key. Access and secret key variables override credentials stored in credential and config files.
    - AWS_DEFAULT_REGION – The region to use. Overrides config/env settings.
  --use-registry=gitlab:
    - Deploy token with the name gitlab-deploy-token and the scope read_registry must be created for each project.
  --use-registry=<registry_name>:
    - CDP_<REGISTRY_NAME>_REGISTRY (Gitlab-runner env var) – Custom docker registry (host:port).
    - CDP_<REGISTRY_NAME>_REGISTRY_TOKEN (Gitlab-runner env var) – Access token used for authentication on custom docker registry.
    - CDP_<REGISTRY_NAME>_REGISTRY_TOKEN_READ_ONLY (Gitlab-runner env var) – Read only access token used for authentication on custom docker registry.
    - CDP_<REGISTRY_NAME>_REGISTRY_USER (Gitlab-runner env var) – User used for authentication on custom docker registry.
    - CDP_ARTIFACTORY_TAG_RETENTION - Used to define label maxCount for artifactory tag retention

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
    - cdp docker --image-tag-branch-name --use-registry=gitlab
    - cdp artifactory --image-tag-branch-name --put=conf/example.yaml

deploy_review:
  image: ouestfrance/cdp:latest
  stage: deploy
  script:
    - cdp k8s --use-registry=gitlab --namespace-project-branch-name --image-tag-branch-name
  environment:
    name: review/$CI_COMMIT_REF_NAME
    url: https://$CI_COMMIT_REF_SLUG.$CI_PROJECT_NAME.$CDP_DNS_SUBDOMAIN

deploy_staging:
  image: ouestfrance/cdp:latest
  stage: deploy
  script:
    - cdp k8s --use-registry=gitlab --namespace-project-name --image-tag-sha1 --values=values.staging.yaml
  environment:
    name: staging
    url: https://$CI_PROJECT_NAME.$CDP_DNS_SUBDOMAIN
```

#### cdp-build-file.yml sample

You can build multiple images in one command by creating a cdp-build-file.yml file in the root of your project. 
This file follows the same description as the docker-compose.yml files

CDP_REGISTRY and CDP_TAG environment variables are automatically set by CDP and refer to the path of the current built image and the tag issued from --image-tagx options.

```yaml
version: '3'
services:
  nginx:
    image: ${CDP_REGISTRY:-local}/my-nginx-project-name:${CDP_TAG:-latest}
    build:
      context: ./distribution/nginx
      dockerfile: Dockerfile
  php:
    image: ${CDP_REGISTRY:-local}/my-php-project-name:${CDP_TAG:-latest}
    build:
      context: ./distribution/php7-fpm
      dockerfile: Dockerfile
```


### _Helm charts_

When you use the `docker k8s` command, you may need information from the CDP context. Below, the variables made available by the CDP for use in the helm context.

```yaml
namespace:               Name of kubernetes namespace, based on the following options: [ --namespace-project-branch-name | --namespace-project-name ]
ingress.host:            Ingress, based on the following options : [ --namespace-project-branch-name | --namespace-project-name ]
ingress.subdomain:       Only DNS subdomain, based on this environment variable CDP_DNS_SUBDOMAIN
image.commit.sha:        First 8 characters of sha1 corresponding to the current commit.
image.registry:          Docker image registry, based on the following options: [ --use-registry=gitlab | --use-registry=aws-ecr | --use-registry=<registry_name> ]
image.repository:        Name of the repository corresponding to the CI_PROJECT_PATH environment variable in lowercase.
image.tag:               Docker image tag, based on the following options: [ --image-tag-branch | --image-tag-latest | --image-tag-sha1 ]
image.pullPolicy:        Docker pull policy, based on the following options: [ --image-tag-branch | --image-tag-latest | --image-tag-sha1 ]
image.imagePullSecrets:  If --image-pull-secret option is set, we add this value to be used in the chart to avoid patch + rollout.
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

### Helm2 to Helm3 automatic migration

If helm-migration option or correlated environment variable is set to true, helm2 charts are automatically migrated to helm3 and used for deployment.

### Team label

If your gitlab project contains a tag formed as "team=my _team_name", the CDP will automatically report this tag in the Kubernetes object labels. This is designed to work with [Kube-resource-report](https://github.com/hjacobs/kube-resource-report) tool. 

### Monitoring Label

CDP allows you to add labels on the pods(from deployement and statefulset) to identify which pods should be monitored or not and wich which ones should trigger alerting.
 ```yaml
monitoring: [true|false]
owner-escalation: [true|false]
```
To do this it uses two envrionnement variable "CDP_MONITORING" and "CDP_ALERTING"  
CDP_MONITORING: [TRUE|FALSE] : Enable or disable monitoring (Use to set "monitoring")  
CDP_ALERTING: [TRUE|FALSE] : Enable or disable alerting (Use to set "owner-scalation")  

### conftest charts validation

#### Policies repository

Charts can be validated by conftest (https://www.conftest.dev/).
Conftest is based upon policies in rego format.
To define policies to apply, create a gitlab repo with your policies in a **policy** folder. Datas must be defined in a **data** folder
You can pass this repo to the cdp with --conftest-repo (or CDP_CONFTEST_REPO var).
Value of this parameter is like reponame:repodir:branch.

Examples ;
- monrepo-conftest
- monrepo-conftest:policies/k8s
- monrepo-conftest:policies/k8s:staging
- monrepo-conftest::staging

#### Namespaces

Policies are grouped by namespace (package in rego definition). By default, main package is used.

You can use multiple packages in cdp by using --conftest-namespaces (or CDP_CONFTEST_NAMESPACES) with namespaces separated by comma or all for all packages.

#### Custom project policies

A projet can define their own policies. To do that, policies must be created in charts/policy folder of the projet as the same level as templates. Datas must be defined in charts/data folder
Project struct
```
project
   |-charts
   |   |-templates
   |   |-policy
   |   |-data
   ... 
```

### _Gitlab secret usage sample_

#### 1 - Create a job with environnement using the --create-gitlab-secret option
```.gitlab-ci.yml
deploy_staging:
  image: $CDP_IMAGE
  stage: deploy
  script:
    - cdp k8s --use-aws-ecr --namespace-project-name --image-tag-sha1 --create-gitlab-secret
  environment:
    name: staging
  only:
    - develop
  tags:
    - staging
```
cdp will search every variable with the pattern CDP_SECRET_STAGING_* and put them in a secret.

#### 2 - Create secret as project variable
Adding CDP_SECRET_STAGING_MY_SECRET_KEY as a project variable in gitlab

#### 3 - Updating the chart
```yaml
apiVersion: extensions/v1beta1
kind: Deployment
spec:
  template:
    spec:
      containers:
        - name: {{ template "nginx.name" . }}-{{ .Values.image.commit.sha }}
          image: "{{ .Values.image.registry }}/{{ .Values.image.repository }}/my-nginx-project-name:{{ .Values.image.tag }}"
        env:
        -name: "MY_GITLAB_SECRET"
         valueFrom:
           secretKeyRef:
             name: cdp-gitlab-secret-{{ .Release.Name |trunc 35 | trimAll "-" }}
             key: MY_SECRET_KEY
...
```
### Gitlab file secret usage sample_

#### 1 - Create a job with environnement using the --create-gitlab-secret option
```.gitlab-ci.yml
deploy_staging:
  image: $CDP_IMAGE
  stage: deploy
  script:
    - cdp k8s --use-aws-ecr --namespace-project-name --image-tag-sha1 --create-gitlab-secret
  environment:
    name: staging
  only:
    - develop
  tags:
    - staging
```
cdp will search every variable with the pattern CDP_FILESECRET_STAGING_* and put them in a secret.

#### 2 - Create file secret as project variable
Adding CDP_FILESECRET_STAGING_MY_SECRET_KEY as a project variable in gitlab

#### 3 - Updating the chart
```yaml
apiVersion: extensions/v1beta1
kind: Deployment
spec:
  template:
    spec:
      containers:
        - name: {{ template "nginx.name" . }}-{{ .Values.image.commit.sha }}
          image: "{{ .Values.image.registry }}/{{ .Values.image.repository }}/my-nginx-project-name:{{ .Values.image.tag }}"
          volumeMounts:
           - name: foo
             mountPath: "/etc/foo"
             readOnly: true
      volumes:
      - name: foo
        secret:
         secretName: cdp-gitlab-file-secret-{{ .Release.Name |trunc 35 | trimAll "-" }}
```
cdp will search every variable with the pattern CDP_FILESECRET_STAGING_* and put them in a secret.

### Gitlab secret hook usage sample_

It's possible to deploy secret and filesecret before others ressources with option --create-gitlab-secret-hook. This option duplicate gitlab secret and file secret.
Secret will be named :
- cdp-gitlab-secret-hook-{{ .Release.Name |trunc 35 | trimAll "-" }}  for  cdp-gitlab-secret
- cdp-gitlab-file-secret-hook-{{ .Release.Name |trunc 35 | trimAll "-" }}  for  cdp-gitlab-file-secret

## Development

### Prerequisites

- python 3.6
- python3-setuptools
- python3-pip
- python3-mock

### Tests

```sh
python3 -m pip install -r requirements.txt
python3 setup.py test

# Single test
python3 setup.py test --addopts tests/unit/test_clidriver.py::TestCliDriver::test_k8s_usecustomregistry_forcebyenvnamespaceprojectname_values
```
### Installations

```sh
python3 -m pip install -r requirements.txt
sudo python3 setup.py install

cdp --help
```
