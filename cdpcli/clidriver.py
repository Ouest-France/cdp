#!/usr/bin/env python
"""
Universal Command Line Environment for Continous Delivery Pipeline on Gitlab-CI.
Usage:
    cdp docker [(-v | --verbose | -q | --quiet)] [(-d | --dry-run)]
        [--use-docker | --use-docker-compose]
        [--image-tag-branch-name] [--image-tag-latest] [--image-tag-sha1]
        [--use-gitlab-registry | --use-aws-ecr]
        [--simulate-merge-on=<branch_name>]
    cdp k8s [(-v | --verbose | -q | --quiet)] [(-d | --dry-run)]
        [--image-tag-branch-name | --image-tag-latest | --image-tag-sha1]
        (--use-gitlab-registry | --use-aws-ecr)
        [--namespace-project-branch-name | --namespace-project-name]
        [--create-default-helm] [--deploy-spec-dir=<dir>]
        [--timeout=<timeout>]
    cdp validator [(-v | --verbose | -q | --quiet)] [(-d | --dry-run)]
        [--block-provider | --block | --block-json]
        [--namespace-project-branch-name | --namespace-project-name | --url=<url>]
    cdp (-h | --help | --version)
Options:
    -h, --help                          Show this screen and exit.
    -v, --verbose                       Make more noise.
    -q, --quiet                         Make less noise.
    -d, --dry-run                       Simulate execution.
    --use-docker                        Use docker to build / push image [default].
    --use-docker-compose                Use docker-compose to build / push image.
    --image-tag-branch-name             Tag docker image with branch name or use it [default].
    --image-tag-latest                  Tag docker image with 'latest'  or use it.
    --image-tag-sha1                    Tag docker image with commit sha1  or use it.
    --use-gitlab-registry               Use gitlab registry for pull/push docker image [default].
    --use-aws-ecr                       Use AWS ECR from k8s configuraiton for pull/push docker image.
    --simulate-merge-on=<branch_name>   Build docker image with the merge current branch on specify branch (no commit).
    --namespace-project-branch-name     Use project and branch name to create k8s namespace or choice environment host [default].
    --namespace-project-name            Use project name to create k8s namespace or choice environment host.
    --create-default-helm               Create default helm for simple project (One docker image).
    --deploy-spec-dir=<dir>             k8s deployment files [default: charts].
    --timeout=<timeout>                 Time in seconds to wait for any individual kubernetes operation [default: 300].
    --block-provider                    Valid BlockProviderConfig interface [default].
    --block                             Valid BlockConfig interface.
    --block-json                        Valid BlockJSON interface.
    --url=<url>                         Test.
"""

import sys, os
import logging, verboselogs
import time
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


    def main(self, args=None):
        if self._context.opt['docker']:
            self.__docker()

        if self._context.opt['k8s']:
            self.__k8s()

        if self._context.opt['validator']:
            self.__validator()

    def __docker(self):
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

        # Login to the docker registry
        self._cmd.run_command(self._context.login)

        # Tag and push docker image
        if not (self._context.opt['--image-tag-branch-name'] or self._context.opt['--image-tag-latest'] or self._context.opt['--image-tag-sha1']) or self._context.opt['--image-tag-branch-name']:
            # Default if none option selected
            self.__buildTagAndPushOnDockerRegistry(self.__getTagBranchName())
        if self._context.opt['--image-tag-latest']:
            self.__buildTagAndPushOnDockerRegistry(self.__getTagLatest())
        if self._context.opt['--image-tag-sha1']:
            self.__buildTagAndPushOnDockerRegistry(self.__getTagSha1())

        # Clean git repository
        if self._context.opt['--simulate-merge-on']:
            self._cmd.run_command('git checkout .')

    def __k8s(self):
        # Need to create default helm charts
        if self._context.opt['--create-default-helm']:
            # Check that the chart dir no exists
            if os.path.isdir(self._context.opt['--deploy-spec-dir']):
                raise ValueError('Directory %s already exists, while --deploy-spec-dir has been selected.' % self._context.opt['--deploy-spec-dir'])
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
        if self._context.opt['--use-gitlab-registry']:
            # Copy secret file on k8s deploy dir
            self._cmd.run_command('cp /cdp/k8s/secret/cdp-secret.yaml %s/templates/' % self._context.opt['--deploy-spec-dir'])
            secretParams = '--set image.credentials.username=%s --set image.credentials.password=%s' % (os.environ['CI_REGISTRY_USER'], os.environ['REGISTRY_PERMANENT_TOKEN'])
        else:
            secretParams = ''

        # Instal or Upgrade environnement
        self._cmd.run_command('helm upgrade %s %s --timeout %s --set namespace=%s --set ingress.host=%s --set image.commit.sha=%s --set image.registry=%s --set image.repository=%s --set image.tag=%s %s --debug -i --namespace=%s'
            % (namespace, self._context.opt['--deploy-spec-dir'], self._context.opt['--timeout'], namespace, host, os.environ['CI_COMMIT_SHA'][:8], self._context.registry, self._context.repository, tag, secretParams, namespace))

        ressources = self._cmd.run_command('kubectl get deployments -n %s -o name' % (namespace))
        if ressources is not None:
            ressources = ressources.strip().split('\n')

            # Patch
            for ressource in ressources:
                if self._context.opt['--use-gitlab-registry']:
                    # Patch secret on deployment (Only deployment imagePullSecrets patch is possible. It's forbidden for pods)
                    # Forbidden: pod updates may not change fields other than `containers[*].image` or `spec.activeDeadlineSeconds` or `spec.tolerations` (only additions to existing tolerations)
                    self._cmd.run_command('kubectl patch %s -p \'{"spec":{"template":{"spec":{"imagePullSecrets": [{"name": "cdp-%s"}]}}}}\' -n %s'
                        % (ressource.replace('/', ' '),  os.environ['CI_REGISTRY'], namespace))

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


    def __validator(self):
        if self._context.opt['--block']:
            schema =  'BlockConfig'
        elif self._context.opt['--block-json']:
            schema = 'BlockJSON'
        else :
            schema = 'BlockProviderConfig'

        if self._context.opt['--url']:
            url = self._context.opt['--url']
        else:
            url = 'http://%s/configurations' % self.__getHost()

        self._cmd.run_command('validator-cli --url %s --schema %s' % (url, schema))
