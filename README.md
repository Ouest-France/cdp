# SIPA/Ouest-France - Continous Delivery Pipeline (CDP) for Gitlab CI

[![Build Status](https://travis-ci.org/Ouest-France/cdp.svg?branch=master)](https://travis-ci.org/Ouest-France/cdp) ![extra](https://img.shields.io/badge/actively%20maintained-yes-ff69b4.svg?)

## Prerequisites
cdp docker / k8s
Si usage de l'ECR, les registry de chaque iimage à déployer doit exister

cdp docker
Fichier Dockerfile ou docker-compose.yml (multi Dockerfile) présent à la racine du projet permettant de générer l'image à déployer.

cdp k8s
Fichiers HELM / k8s permettant de faire le déploiement

## Usage

### .gitlab-ci.yml file

```yaml
variables:
  DOCKER_HOST: tcp://localhost:2375

services:
  - docker:dind

package:
  image: ouest-france/cdp:latest
  stage: package
  script:
    - cdp docker --image-tag-branch-name --use-gitlab-registry

deploy:
  variables:
    DNS_SUBDOMAIN: { ingress.k8s }
  image: ouest-france/cdp:latest
  stage: deploy
  script:
    - cdp k8s --use-gitlab-registry --namespace-project-branch-name --image-tag-branch-name
  environment:
    name: review/$CI_COMMIT_REF_NAME
    url: http://$CI_ENVIRONMENT_SLUG.$CI_PROJECT_NAME.$DNS_SUBDOMAIN
```
### Helm charts

namespace           Name of kubernetes namespace, based on the following options: [ --namespace-project-branch-name | --namespace-project-name ]
ingress.host        Ingress, based on the following options : [ --namespace-project-branch-name | --namespace-project-name ]
image.commit.sha    First 8 characters of sha1 corresponding to the current commit.
image.registry      Docker image registry, based on the following options: [ --use-gitlab-registry | --use-aws-ecr ]
image.repository    Name of the repository corresponding to the CI_PROJECT_PATH environment variable in lowercase.
image.tag           Docker image tag, based on the following options: [ --image-tag-branch | --image-tag-latest | --image-tag-sha1 ]

## Command Completion

TODO
