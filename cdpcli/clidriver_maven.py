#!/usr/bin/env python3.6

"""
Universal Command Line Environment for Continuous Delivery Pipeline on Gitlab-CI.
Usage:
    cdp maven [(-v | --verbose | -q | --quiet)] [(-d | --dry-run)] [--sleep=<seconds>]
        (--goals=<goals-opts>|--deploy=<type>) [--simulate-merge-on=<branch_name>]
        [--maven-release-plugin=<version>]
        [--use-gitlab-registry | --use-aws-ecr | --use-custom-registry | --use-registry=<registry_name>]
        [--altDeploymentRepository=<repository_name>]
        [--login-registry=<registry_name>]
        [--docker-image-maven=<image_name_maven>|--docker-version=<version>] [--docker-image-git=<image_name_git>] [--volume-from=<host_type>]
    cdp (-h | --help | --version)
Options:
    -h, --help                                                 Show this screen and exit.
    -v, --verbose                                              Make more noise.
    -q, --quiet                                                Make less noise.
    -d, --dry-run                                              Simulate execution.
    --altDeploymentRepository=<repository_name>                Use custom Maven Dpeloyement repository
    --build-context=<path>                                     Specify the docker building context [default: .].
    --build-arg=<arg>                                          Build args for docker
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
    --image-pull-secret                                        Add the imagePullSecret value to use the helm --wait option instead of patch and rollout (deprecated)
    --image-tag-branch-name                                    Tag docker image with branch name or use it [default].
    --image-tag-latest                                         Tag docker image with 'latest'  or use it.
    --image-tag-sha1                                           Tag docker image with commit sha1  or use it.
    --image-tag=<tag>                                          Tag name
    --image-prefix-tag=<tag>                                   Tag prefix for docker image.
    --ingress-tlsSecretName=<secretName>                       Name of the tls secret for ingress 
    --internal-port=<port>                                     Internal port used if --create-default-helm is activate [default: 8080]
    --login-registry=<registry_name>                           Login on specific registry for build image [default: none].
    --maven-release-plugin=<version>                           Specify maven-release-plugin version [default: 2.5.3].
    --namespace-project-branch-name                            Use project and branch name to create k8s namespace or choice environment host [default].
    --namespace-project-name                                   Use project name to create k8s namespace or choice environment host.
    --no-conftest                                              Do not run conftest validation tests.
    --path=<path>                                              Path to validate [default: configurations].
    --put=<file>                                               Put file to artifactory.
    --release-custom-name=<release_name>                       Customize release name with namespace-name-<release_name>
    --release-project-branch-name                              Force the release to be created with the project branch name.
    --release-project-env-name                                 Force the release to be created with the job env name.define in gitlab
    --release-shortproject-name                                Force the release to be created with the shortname (first letters of word + id) of the Gitlab project
    --release-project-name                                     Force the release to be created with the name of the Gitlab project
    --simulate-merge-on=<branch_name>                          Build docker image with the merge current branch on specify branch (no commit).
    --sleep=<seconds>                                          Time to sleep int the end (for debbuging) in seconds [default: 0].
    --timeout=<timeout>                                        Time in seconds to wait for any individual kubernetes operation [default: 600].
    --tiller-namespace                                         Force the tiller namespace to be the same as the pod namespace (deprecated)
    --use-aws-ecr                                              DEPRECATED - Use AWS ECR from k8s configuration for pull/push docker image.
    --use-custom-registry                                      DEPRECATED - Use custom registry for pull/push docker image.
    --use-docker                                               Use docker to build / push image [default].
    --use-docker-compose                                       Use docker-compose to build / push image / retag container [DEPRECATED]
    --use-gitlab-registry                                      DEPRECATED - Use gitlab registry for pull/push docker image [default].
    --use-registry=<registry_name>                             Use registry for pull/push docker image (none, aws-ecr, gitlab, harbor or custom name for load specifics environments variables) [default: none].
    --validate-configurations                                  Validate configurations schema of BlockProvider.
    --values=<files>                                           Specify values in a YAML file (can specify multiple separate by comma). The priority will be given to the last (right-most) file specified.
    --volume-from=<host_type>                                  Volume type of sources - docker, k8s, local or docker volume description (dir:mount) [default: k8s]
"""
