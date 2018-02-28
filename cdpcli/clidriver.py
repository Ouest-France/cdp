#!/usr/bin/env python3
"""
Universal Command Line Environment for Continous Delivery Pipeline on Gitlab-CI.
Usage:
    cdp build [(-v | --verbose | -q | --quiet)] [(-d | --dry-run)] [--sleep=<seconds>]
        (--docker-image=<image_name>)
        (--command=<build_cmd>)
        [--dind]
        [--simulate-merge-on=<branch_name>]
    cdp docker [(-v | --verbose | -q | --quiet)] [(-d | --dry-run)] [--sleep=<seconds>]
        [--use-docker | --use-docker-compose]
        [--image-tag-branch-name] [--image-tag-latest] [--image-tag-sha1]
        [--use-gitlab-registry | --use-aws-ecr | --use-custom-registry]
    cdp artifactory [(-v | --verbose | -q | --quiet)] [(-d | --dry-run)] [--sleep=<seconds>]
        [--image-tag-branch-name] [--image-tag-latest] [--image-tag-sha1]
        (--put=<file> | --delete=<file>)
    cdp k8s [(-v | --verbose | -q | --quiet)] [(-d | --dry-run)] [--sleep=<seconds>]
        [--image-tag-branch-name | --image-tag-latest | --image-tag-sha1]
        (--use-gitlab-registry | --use-aws-ecr | --use-custom-registry)
        [--values=<files>]
        [--delete-labels=<minutes>]
        [--namespace-project-branch-name | --namespace-project-name]
        [--create-default-helm] [--deploy-spec-dir=<dir>]
        [--timeout=<timeout>]
    cdp validator [(-v | --verbose | -q | --quiet)] [(-d | --dry-run)] [--sleep=<seconds>]
        [--path=<path>]
        [--block-provider | --block | --block-json]
        [--namespace-project-branch-name | --namespace-project-name]
    cdp (-h | --help | --version)
Options:
    -h, --help                          Show this screen and exit.
    -v, --verbose                       Make more noise.
    -q, --quiet                         Make less noise.
    -d, --dry-run                       Simulate execution.
    --sleep=<seconds>                   Time to sleep int the end (for debbuging) in seconds [default: 0].
    --docker-image=<image_name>         Specify docker image name for build project.
    --command=<build_cmd>               Command to run in the docker image.
    --dind                              Activate 'Docker in Docker' inside this container.
    --simulate-merge-on=<branch_name>   Build docker image with the merge current branch on specify branch (no commit).
    --use-docker                        Use docker to build / push image [default].
    --use-docker-compose                Use docker-compose to build / push image.
    --image-tag-branch-name             Tag docker image with branch name or use it [default].
    --image-tag-latest                  Tag docker image with 'latest'  or use it.
    --image-tag-sha1                    Tag docker image with commit sha1  or use it.
    --use-gitlab-registry               Use gitlab registry for pull/push docker image [default].
    --use-aws-ecr                       Use AWS ECR from k8s configuraiton for pull/push docker image.
    --use-custom-registry               Use custom registry for pull/push docker image.
    --put=<file>                        Put file to artifactory.
    --delete=<file>                     Delete file in artifactory.
    --values=<files>                    Specify values in a YAML file (can specify multiple separate by comma). The priority will be given to the last (right-most) file specified.
    --delete-labels=<minutes>           Add namespace labels (deletable=true deletionTimestamp=now + minutes) for external cleanup.
    --namespace-project-branch-name     Use project and branch name to create k8s namespace or choice environment host [default].
    --namespace-project-name            Use project name to create k8s namespace or choice environment host.
    --create-default-helm               Create default helm for simple project (One docker image).
    --deploy-spec-dir=<dir>             k8s deployment files [default: charts].
    --timeout=<timeout>                 Time in seconds to wait for any individual kubernetes operation [default: 300].
    --path=<path>                       Path to validate [default: configurations].
    --block-provider                    Valid BlockProviderConfig interface [default].
    --block                             Valid BlockConfig interface.
    --block-json                        Valid BlockJSON interface.
"""

import sys, os
import logging, verboselogs
import time, datetime
import yaml
from Context import Context
from clicommand import CLICommand
from cdpcli import __version__
from docopt import docopt, DocoptExit

LOG = verboselogs.VerboseLogger('clidriver')
LOG.addHandler(logging.StreamHandler())
LOG.setLevel(logging.INFO)

def main():
    opt = docopt(__doc__, sys.argv[1:], version=__version__)
    if opt['--verbose']:
        LOG.setLevel(logging.VERBOSE)
    elif opt['--quiet']:
        LOG.setLevel(logging.WARNING)

    driver = CLIDriver(cmd = CLICommand(opt['--dry-run']), opt = opt)
    return driver.main()

class CLIDriver(object):

    def __init__(self, cmd=None, opt=None):
        if cmd is None:
            raise ValueError('TODO')
        else:
            self._cmd = cmd

        if opt is None:
            raise ValueError('TODO')
        else:
            self._context = Context(opt, cmd)
            LOG.verbose('Context : %s', self._context.__dict__)

        # Default value of DOCKER_HOST env var if not set
        if os.getenv('DOCKER_HOST', None) is None:
            os.environ['DOCKER_HOST'] = 'tcp://localhost:2375'

        LOG.verbose('DOCKER_HOST : %s', os.getenv('DOCKER_HOST',''))


    def main(self, args=None):
        try:
            if self._context.opt['--verbose']:
                self._cmd.run_command('env')

            if self._context.opt['build']:
                self.__build()

            if self._context.opt['docker']:
                self.__docker()

            if self._context.opt['artifactory']:
                self.__artifactory()

            if self._context.opt['k8s']:
                self.__k8s()

            if self._context.opt['validator']:
                self.__validator()

        finally:
            if self._context.opt['--sleep'] != "0":
                self._cmd.run_command('sleep %s' % self._context.opt['--sleep'])


    def __build(self):
        if self._context.opt['--simulate-merge-on']:
            LOG.notice('Build docker image with the merge current branch on %s branch', self._context.opt['--simulate-merge-on'])

            # Merge branch on selected branch
            self._cmd.run_command('git config --global user.email \"%s\"' % os.environ['GITLAB_USER_EMAIL'])
            self._cmd.run_command('git config --global user.name \"%s\"' % os.environ['GITLAB_USER_ID'])
            self._cmd.run_command('git checkout %s' % self._context.opt['--simulate-merge-on'])
            self._cmd.run_command('git reset --hard origin/%s' % self._context.opt['--simulate-merge-on'])
            self._cmd.run_command('git merge %s --no-commit --no-ff' %  os.environ['CI_COMMIT_SHA'])

            # TODO Exception process
        else:
            LOG.notice('Build docker image with the current branch : %s', os.environ['CI_COMMIT_REF_NAME'])

        dind = ''
        if self._context.opt['--dind']:
            self._cmd.run_command('docker pull docker:dind')
            self._cmd.run_command('docker run --rm --privileged --name docker-dind -d docker:dind')
            dind = '--link docker-dind:docker -e DOCKER_HOST=tcp://docker:2375'

        self._cmd.run_command('docker pull %s' % (self._context.opt['--docker-image']))
        self._cmd.run_command('docker run --rm %s -v ${PWD}:/cdp-data %s /bin/sh -c \'cd /cdp-data; %s\'' % (dind, self._context.opt['--docker-image'], self._context.opt['--command']))

        # Clean git repository
        if self._context.opt['--simulate-merge-on']:
            self._cmd.run_command('git checkout .')


    def __docker(self):
        # Login to the docker registry
        self._cmd.run_command(self._context.login)

        if self._context.opt['--use-aws-ecr']:
            try:
                self._cmd.run_command('aws ecr list-images --repository-name %s --max-items 0' % self._context.repository)
            except ValueError:
                LOG.warning('AWS ECR repository doesn\'t  exist. Creating this one.')
                self._cmd.run_command('aws ecr create-repository --repository-name %s' % self._context.repository)

        # Tag and push docker image
        if not (self._context.opt['--image-tag-branch-name'] or self._context.opt['--image-tag-latest'] or self._context.opt['--image-tag-sha1']) or self._context.opt['--image-tag-branch-name']:
            # Default if none option selected
            self.__buildTagAndPushOnDockerRegistry(self.__getTagBranchName())
        if self._context.opt['--image-tag-latest']:
            self.__buildTagAndPushOnDockerRegistry(self.__getTagLatest())
        if self._context.opt['--image-tag-sha1']:
            self.__buildTagAndPushOnDockerRegistry(self.__getTagSha1())

    def __artifactory(self):
        if self._context.opt['--put']:
            upload_file = self._context.opt['--put']
            http_verb = 'PUT'
        elif self._context.opt['--delete']:
            upload_file = self._context.opt['--delete']
            http_verb = 'DELETE'
        else:
            raise ValueError('Incorrect option with artifactory command.')

        # Tag and push docker image
        if not (self._context.opt['--image-tag-branch-name'] or self._context.opt['--image-tag-latest'] or self._context.opt['--image-tag-sha1']) or self._context.opt['--image-tag-branch-name']:
            # Default if none option selected
            self.__callArtifactoryFile(self.__getTagBranchName(), upload_file, http_verb)
        if self._context.opt['--image-tag-latest']:
            self.__callArtifactoryFile(self.__getTagLatest(), upload_file, http_verb)
        if self._context.opt['--image-tag-sha1']:
            self.__callArtifactoryFile(self.__getTagSha1(), upload_file, http_verb)

    def __k8s(self):
        # Need to create default helm charts
        if self._context.opt['--create-default-helm']:
            # Check that the chart dir no exists
            if os.path.isdir('%s/templates' % self._context.opt['--deploy-spec-dir']):
                raise ValueError('Directory %s/templates already exists, while --deploy-spec-dir has been selected.' % self._context.opt['--deploy-spec-dir'])
            elif os.path.isfile('%s/values.yaml' % self._context.opt['--deploy-spec-dir']):
                raise ValueError('File %s/values.yaml already exists, while --deploy-spec-dir has been selected.' % self._context.opt['--deploy-spec-dir'])
            elif os.path.isfile('%s/Chart.yaml' % self._context.opt['--deploy-spec-dir']):
                raise ValueError('File %s/Chart.yaml already exists, while --deploy-spec-dir has been selected.' % self._context.opt['--deploy-spec-dir'])
            else:
                os.makedirs('%s/templates' % self._context.opt['--deploy-spec-dir'])
                self._cmd.run_command('cp -R /cdp/k8s/charts/* %s/' % self._context.opt['--deploy-spec-dir'])
                with open('%s/Chart.yaml' % self._context.opt['--deploy-spec-dir'], 'w') as outfile:
                    data = dict(
                        apiVersion = 'v1',
                        description = 'A Helm chart for Kubernetes',
                        name = os.environ['CI_PROJECT_NAME'],
                        version = '0.1.0'
                    )
                    yaml.dump(data, outfile, default_flow_style=False)

        namespace = self.__getNamespace()
        host = self.__getHost()

        if self._context.opt['--image-tag-latest']:
            tag =  self.__getTagLatest()
        elif self._context.opt['--image-tag-sha1']:
            tag = self.__getTagSha1()
        else :
            tag = self.__getTagBranchName()

        # Need to add secret file for docker registry
        if not self._context.opt['--use-aws-ecr']:
            # Copy secret file on k8s deploy dir
            self._cmd.run_command('cp /cdp/k8s/secret/cdp-secret.yaml %s/templates/' % self._context.opt['--deploy-spec-dir'])
            secretParams = '--set image.credentials.username=%s --set image.credentials.password=%s' % (self._context.registry_user, self._context.registry_token_ro)
        else:
            secretParams = ''

        if self._context.opt['--values']:
            valuesFiles = self._context.opt['--values'].strip().split(',')
            values = '--values %s/' % self._context.opt['--deploy-spec-dir'] + (' --values %s/' % self._context.opt['--deploy-spec-dir']).join(valuesFiles)
        else:
            values = ''

        # Instal or Upgrade environnement
        self._cmd.run_command('helm upgrade %s %s --timeout %s --set namespace=%s --set ingress.host=%s --set image.commit.sha=%s --set image.registry=%s --set image.repository=%s --set image.tag=%s %s %s --debug -i --namespace=%s'
            % (namespace, self._context.opt['--deploy-spec-dir'], self._context.opt['--timeout'], namespace, host, os.environ['CI_COMMIT_SHA'][:8], self._context.registry, self._context.repository, tag, secretParams, values, namespace))

        if self._context.opt['--delete-labels']:
            now = datetime.datetime.now()
            date_format = '%Y-%m-%dT%H%M%S'
            self._cmd.run_command('kubectl label namespace %s deletable=true creationTimestamp=%s deletionTimestamp=%s --namespace=%s --overwrite'
                % (namespace, now.strftime(date_format), (now + datetime.timedelta(minutes = int(self._context.opt['--delete-labels']))).strftime(date_format) , namespace))

        ressources = self._cmd.run_command('kubectl get deployments -n %s -o name' % (namespace))
        if ressources is not None:
            ressources = ressources.strip().split('\n')

            # Patch
            for ressource in ressources:
                if not self._context.opt['--use-aws-ecr']:
                    # Patch secret on deployment (Only deployment imagePullSecrets patch is possible. It's forbidden for pods)
                    # Forbidden: pod updates may not change fields other than `containers[*].image` or `spec.activeDeadlineSeconds` or `spec.tolerations` (only additions to existing tolerations)
                    self._cmd.run_command('kubectl patch %s -p \'{"spec":{"template":{"spec":{"imagePullSecrets": [{"name": "cdp-%s"}]}}}}\' -n %s'
                        % (ressource.replace('/', ' '),  self._context.registry, namespace))

            # Rollout
            for ressource in ressources:
                # Issue on --request-timeout option ? https://github.com/kubernetes/kubernetes/issues/51952
                self._cmd.run_command('timeout %s kubectl rollout status %s -n %s' % (self._context.opt['--timeout'], ressource, namespace))


    def __buildTagAndPushOnDockerRegistry(self, tag):
        if self._context.opt['--use-docker-compose']:
            os.environ['CDP_TAG'] = tag
            os.environ['CDP_REGISTRY'] = self.__getImageName()
            self._cmd.run_command('docker-compose build')
            self._cmd.run_command('docker-compose push')
        else:
            image_tag = self.__getImageTag(self.__getImageName(), tag)
            # Tag docker image
            self._cmd.run_command('docker build -t %s .' % (image_tag))
            # Push docker image
            self._cmd.run_command('docker push %s' % (image_tag))


    def __callArtifactoryFile(self, tag, upload_file, http_verb):
        if http_verb is 'PUT':
            self._cmd.run_command('curl --fail -X PUT %s/%s/%s/ -H X-JFrog-Art-Api:%s -T %s' % (os.environ['CDP_ARTIFACTORY_PATH'], self._context.repository, tag, os.environ['CDP_ARTIFACTORY_TOKEN'], upload_file))
        elif http_verb is 'DELETE':
            self._cmd.run_command('curl --fail -X DELETE %s/%s/%s/%s -H X-JFrog-Art-Api:%s' % (os.environ['CDP_ARTIFACTORY_PATH'], self._context.repository, tag, upload_file, os.environ['CDP_ARTIFACTORY_TOKEN']))

    def __validator(self):
        if self._context.opt['--block']:
            schema =  'BlockConfig'
        elif self._context.opt['--block-json']:
            schema = 'BlockJSON'
        else :
            schema = 'BlockProviderConfig'

        url = 'http://%s/%s' % (self.__getHost(), self._context.opt['--path'])

        self._cmd.run_command('validator-cli --url %s --schema %s' % (url, schema))


    def __getImageName(self):
        # Configure docker registry
        image_name = '%s/%s' % (self._context.registry, self._context.repository)
        LOG.verbose('Image name : %s', image_name)
        return image_name

    def __getImageTag(self, image_name, tag):
        return '%s:%s' %  (image_name, tag)

    def __getTagBranchName(self):
        return os.environ['CI_COMMIT_REF_NAME']

    def __getTagLatest(self):
        return 'latest'

    def __getTagSha1(self):
        return os.environ['CI_COMMIT_SHA']

    def __getNamespace(self):
        # Get k8s namespace
        if self._context.opt['--namespace-project-name']:
            namespace = os.environ['CI_PROJECT_NAME']
        else:
            namespace = '%s-%s' % (os.environ['CI_PROJECT_NAME'], os.environ['CI_COMMIT_REF_NAME'])    # Get deployment host

        return namespace.replace('_', '-')

    def __getHost(self):
        # Get k8s namespace
        if self._context.opt['--namespace-project-name']:
            return '%s.%s' % (os.environ['CI_PROJECT_NAME'], os.environ['DNS_SUBDOMAIN'])
        else:
            return '%s.%s.%s' % (os.getenv('CI_ENVIRONMENT_SLUG', os.environ['CI_COMMIT_REF_NAME']), os.environ['CI_PROJECT_NAME'], os.environ['DNS_SUBDOMAIN'])
