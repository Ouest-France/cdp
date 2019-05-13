#!/usr/bin/env python3.6

"""
Universal Command Line Environment for Continous Delivery Pipeline on Gitlab-CI.
Usage:
    cdp build [(-v | --verbose | -q | --quiet)] [(-d | --dry-run)] [--sleep=<seconds>]
        (--docker-image=<image_name>) (--command=<cmd>)
        [--docker-image-git=<image_name_git>] [--simulate-merge-on=<branch_name>]
        [--volume-from=<host_type>]
    cdp maven [(-v | --verbose | -q | --quiet)] [(-d | --dry-run)] [--sleep=<seconds>]
        (--docker-image-maven=<image_name_maven>|--docker-version=<version>) (--goals=<goals-opts>|--deploy=<type>)
        [--maven-release-plugin=<version>]
        [--docker-image-git=<image_name_git>] [--simulate-merge-on=<branch_name>]
        [--volume-from=<host_type>]
        [--use-gitlab-registry | --use-aws-ecr | --use-custom-registry]
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
        [--tiller-namespace]
        [--release-project-branch-name]
        [--image-pull-secret]
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
    --docker-image-helm=<image_name_helm>                      Docker image which execute helm command [default: ouestfrance/cdp-helm:2.13.1].
    --docker-image-kubectl=<image_name_kubectl>                Docker image which execute kubectl command [default: ouestfrance/cdp-kubectl:1.9.9].
    --docker-image-maven=<image_name_maven>                    Docker image which execute mvn command [default: maven:3.5.3-jdk-8].
    --docker-image-sonar-scanner=<image_name_sonar_scanner>    Docker image which execute sonar-scanner command [default: ouestfrance/cdp-sonar-scanner:3.1.0].
    --docker-image=<image_name>                                Specify docker image name for build project.
    --docker-version=<version>                                 Specify maven docker version. deprecated [default: 3.5.3-jdk-8].
    --goals=<goals-opts>                                       Goals and args to pass maven command.
    --image-pull-secret                                        Add the imagePullSecret value to use the helm --wait option instead of patch and rollout (deprecated)
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
    --release-project-branch-name                              Force the release to be created with the project branch name.
    --sast                                                     Static Application Security Testing mode.
    --simulate-merge-on=<branch_name>                          Build docker image with the merge current branch on specify branch (no commit).
    --sleep=<seconds>                                          Time to sleep int the end (for debbuging) in seconds [default: 0].
    --timeout=<timeout>                                        Time in seconds to wait for any individual kubernetes operation [default: 600].
    --tiller-namespace                                         Force the tiller namespace to be the same as the pod namespace (deprecated)
    --use-aws-ecr                                              Use AWS ECR from k8s configuration for pull/push docker image.
    --use-custom-registry                                      Use custom registry for pull/push docker image.
    --use-docker                                               Use docker to build / push image [default].
    --use-docker-compose                                       Use docker-compose to build / push image.
    --use-gitlab-registry                                      Use gitlab registry for pull/push docker image [default].
    --validate-configurations                                  Validate configurations schema of BlockProvider.
    --values=<files>                                           Specify values in a YAML file (can specify multiple separate by comma). The priority will be given to the last (right-most) file specified.
    --volume-from=<host_type>                                  Volume type of sources - docker, k8s or local [default: k8s]
"""

import configparser
import sys, os, re
import logging, verboselogs
import time, datetime
import yaml, json
import gitlab
import pyjq
import shutil
from .Context import Context
from .clicommand import CLICommand
from cdpcli import __version__
from .dockercommand import DockerCommand
from docopt import docopt, DocoptExit
from .PropertiesParser import PropertiesParser

LOG = verboselogs.VerboseLogger('clidriver')
LOG.addHandler(logging.StreamHandler())

def main():
    opt = docopt(__doc__, sys.argv[1:], version=__version__)

    # Log management
    log_level = logging.INFO
    if CLIDriver.verbose(opt['--verbose']):
        log_level = logging.VERBOSE
    elif CLIDriver.warning(opt['--quiet']):
        log_level = logging.WARNING
    LOG.setLevel(log_level)

    driver = CLIDriver(cmd = CLICommand(opt['--dry-run'], log_level = log_level), opt = opt)
    return driver.main()

class CLIDriver(object):

    def __init__(self, cmd=None, opt=None):
        if cmd is None:
            raise ValueError('TODO')
        else:
            self._cmd = cmd

        # Default value of DOCKER_HOST env var if not set
        if os.getenv('DOCKER_HOST', None) is None:
            os.environ['DOCKER_HOST'] = 'unix:///var/run/docker.sock'

        os.environ['CDP_DOCKER_HOST_INTERNAL'] = self._cmd.run_command('ip route | awk \'NR==1 {print $3}\'')[0].strip()

        LOG.verbose('DOCKER_HOST : %s', os.getenv('DOCKER_HOST',''))

        if self.verbose(opt['--verbose']):
            self._cmd.run_command('env', dry_run=False)

        if opt is None:
            raise ValueError('TODO')
        else:
            self._context = Context(opt, cmd)
            LOG.verbose('Context : %s', self._context.__dict__)

    def main(self, args=None):
        try:
            if self._context.opt['build']:
                self.__build()

            if self._context.opt['maven']:
                self.__maven()

            if self._context.opt['sonar']:
                self.__sonar()

            if self._context.opt['docker']:
                self.__docker()

            if self._context.opt['artifactory']:
                self.__artifactory()

            if self._context.opt['k8s']:
                self.__k8s()

            if self._context.opt['validator-server']:
                self.__validator()

        finally:
            sleep =  os.getenv('CDP_SLEEP', self._context.opt['--sleep'])
            if sleep is not None and sleep != "0":
                self._cmd.run_command('sleep %s' % sleep)


    def __build(self):
        self.__simulate_merge_on()

        docker_image_cmd = DockerCommand(self._cmd, self._context.opt['--docker-image'], self._context.opt['--volume-from'])
        docker_image_cmd.run(self._context.opt['--command'])

    def __maven(self):
        force_git_config = False

        settings = 'maven-settings.xml'

        command = self._context.opt['--goals']

        if self._context.opt['--deploy']:
            if self._context.opt['--deploy'] == 'release':
                force_git_config = True
                command = '--batch-mode org.apache.maven.plugins:maven-release-plugin:%s:prepare org.apache.maven.plugins:maven-release-plugin:%s:perform -Dresume=false -DautoVersionSubmodules=true -DdryRun=false -DscmCommentPrefix="[ci skip]" -Dproject.scm.id=git' % (self._context.opt['--maven-release-plugin'], self._context.opt['--maven-release-plugin'])
                arguments = '-DskipTests -DskipITs -Dproject.scm.id=git -DaltDeploymentRepository=release::default::%s/%s' % (os.environ['CDP_REPOSITORY_URL'], os.environ['CDP_REPOSITORY_MAVEN_RELEASE'])

                if os.getenv('MAVEN_OPTS', None) is not None:
                    arguments = '%s %s' % (arguments, os.environ['MAVEN_OPTS'])

                command = '%s -DreleaseProfiles=release -Darguments="%s"' % (command, arguments)
            else:
                command = 'deploy -DskipTests -DskipITs -DaltDeploymentRepository=snapshot::default::%s/%s' % (os.environ['CDP_REPOSITORY_URL'], os.environ['CDP_REPOSITORY_MAVEN_SNAPSHOT'])


        if os.getenv('MAVEN_OPTS', None) is not None:
            command = '%s %s' % (command, os.environ['MAVEN_OPTS'])

        command = 'mvn %s %s' % (command, '-s %s' % settings)

        self.__simulate_merge_on(force_git_config)

        self._cmd.run_command('cp /cdp/maven/settings.xml %s' % settings)

        if self._context.opt['--docker-version'] is not None and self._context.opt['--docker-version'] != "3.5.3-jdk-8":
            maven_cmd = DockerCommand(self._cmd, 'maven:%s' % (self._context.opt['--docker-version']), self._context.opt['--volume-from'])
        else:
            maven_cmd = DockerCommand(self._cmd, '%s' % (self._context.opt['--docker-image-maven']), self._context.opt['--volume-from'])
        maven_cmd.run(command)


    def __sonar(self):
        self.__simulate_merge_on()

        sonar_file = 'sonar-project.properties'
        project_key = None
        sources = None

        command = '-Dsonar.login=%s' % os.environ['CDP_SONAR_LOGIN']
        command = '%s -Dsonar.host.url=%s' % (command, os.environ['CDP_SONAR_URL'])
        command = '%s -Dsonar.gitlab.user_token=%s' % (command, os.environ['GITLAB_USER_TOKEN'])
        command = '%s -Dsonar.gitlab.commit_sha=%s' % (command, os.environ['CI_COMMIT_SHA'])
        command = '%s -Dsonar.gitlab.ref_name=%s' % (command, os.environ['CI_COMMIT_REF_NAME'])
        command = '%s -Dsonar.gitlab.project_id=%s' % (command, os.environ['CI_PROJECT_PATH_SLUG'])
        command = '%s -Dsonar.branch.name=%s' % (command, self.__getTagBranchName())

        # Check if mandatory properties are setted
        if os.path.isfile(sonar_file):
            LOG.verbose('Read : %s', sonar_file)
            cfg = PropertiesParser()
            cfg.read(sonar_file)
            project_key = cfg.get('sonar.projectKey')
            sources = cfg.get('sonar.sources')

        # Set property if not setted
        if not (project_key and project_key.strip()):
            command = "%s -Dsonar.projectKey=%s" % (command, os.environ['CI_PROJECT_PATH_SLUG'])

        # Set property if not setted
        if not (sources and sources.strip()):
            command = "%s -Dsonar.sources=." % command

        if self._context.opt['--sast']:
            command = "%s -Dsonar.gitlab.json_mode=SAST" % command
        else:
            command = "%s -Dsonar.gitlab.json_mode=CODECLIMATE" % command

        if self._context.opt['--preview']:
            command = "%s -Dsonar.analysis.mode=preview" % command

        sonar_scanner_cmd = DockerCommand(self._cmd, self._context.opt['--docker-image-sonar-scanner'], self._context.opt['--volume-from'], True)
        sonar_scanner_cmd.run(command)

    def __docker(self):
        if self._context.opt['--use-aws-ecr']:
            aws_cmd = DockerCommand(self._cmd, self._context.opt['--docker-image-aws'], None, True)

            repos = []

            if self._context.opt['--use-docker'] or not (self._context.opt['--use-docker-compose']):
                repos.append(self._context.repository)
            elif self._context.opt['--use-docker-compose']:
                docker_services = self._cmd.run_command('docker-compose config --services')
                for docker_service in docker_services:
                    repos.append('%s/%s' % (self._context.repository, docker_service.strip()))

            for repo in repos:
                try:
                    aws_cmd.run('ecr list-images --repository-name %s --max-items 0' % repo)
                except ValueError:
                    LOG.warning('AWS ECR repository doesn\'t  exist. Creating this one.')
                    aws_cmd.run('ecr create-repository --repository-name %s' % repo)

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
        kubectl_cmd = DockerCommand(self._cmd, self._context.opt['--docker-image-kubectl'], self._context.opt['--volume-from'], True)
        helm_cmd = DockerCommand(self._cmd, self._context.opt['--docker-image-helm'], self._context.opt['--volume-from'], True)

		# Use release name instead of the namespace name for release
        release = self.__getRelease()
        namespace = self.__getNamespace()
        host = self.__getHost()

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

        final_deploy_spec_dir = '%s_final' % self._context.opt['--deploy-spec-dir']
        final_template_deploy_spec_dir = '%s/templates' % final_deploy_spec_dir
        try:
            os.makedirs(final_template_deploy_spec_dir)
            shutil.copyfile('%s/Chart.yaml' % self._context.opt['--deploy-spec-dir'], '%s/Chart.yaml' % final_deploy_spec_dir)
        except OSError as e:
            LOG.error(str(e))

        command = 'upgrade %s' % release
        command = '%s %s' % (command, final_deploy_spec_dir)
        command = '%s --timeout %s' % (command, self._context.opt['--timeout'])
        set_command = '--set namespace=%s' % namespace

        #Deprecated, we will detect if tiller is available in our namespace or in kube-system
        if self._context.opt['--tiller-namespace']:
            command = '%s --tiller-namespace=%s' % (command, namespace)

        tiller_length = 0
        tiller_json = ''
        try:
            if not self._context.opt['--tiller-namespace']:
                tiller_json = ''.join(kubectl_cmd.run('get pod --namespace %s -l name="tiller" -o json --ignore-not-found=false' % ( namespace )))
                tiller_length = len(pyjq.first('.items[] | .metadata.labels.name', json.loads(tiller_json)))
                command = '%s --tiller-namespace=%s' % (command, namespace)
        except Exception as e:
            # Not present
            LOG.verbose(str(e))
        # Need to create default helm charts
        if self._context.opt['--create-default-helm']:
            set_command = '%s --set service.internalPort=%s' % (set_command, self._context.opt['--internal-port'])

        if self._context.opt['--image-tag-latest']:
            tag =  self.__getTagLatest()
            pullPolicy = 'Always'
        elif self._context.opt['--image-tag-sha1']:
            tag = self.__getTagSha1()
            pullPolicy = 'IfNotPresent'
        else:
            tag = self.__getTagBranchName()
            pullPolicy = 'Always'

        set_command = '%s --set ingress.host=%s' % (set_command, host)
        set_command = '%s --set ingress.subdomain=%s' % (set_command, os.getenv('CDP_DNS_SUBDOMAIN', None))
        set_command = '%s --set image.commit.sha=sha-%s' % (set_command, os.environ['CI_COMMIT_SHA'][:8])
        set_command = '%s --set image.registry=%s' % (set_command,  self._context.registry)
        set_command = '%s --set image.repository=%s' % (set_command, self._context.repository)
        set_command = '%s --set image.tag=%s' % (set_command, tag)
        set_command = '%s --set image.pullPolicy=%s' % (set_command, pullPolicy)

        # Need to add secret file for docker registry
        if not self._context.opt['--use-aws-ecr']:
            # Add secret (Only if secret is not exist )
            self._cmd.run_command('cp /cdp/k8s/secret/cdp-secret.yaml %s/templates/' % self._context.opt['--deploy-spec-dir'])
            set_command = '%s --set image.credentials.username=%s' % (set_command, self._context.registry_user_ro)
            set_command = '%s --set image.credentials.password=%s' % (set_command, self._context.registry_token_ro)
            set_command = '%s --set image.imagePullSecrets=cdp-%s-%s' % (set_command, self._context.registry,release)

        command = '%s --debug' % command
        command = '%s -i' % command
        command = '%s --namespace=%s' % (command, namespace)
        command = '%s --force' % command
        command = '%s --wait' % command

        now = datetime.datetime.utcnow()
        date_format = '%Y-%m-%dT%H%M%S'
        if self._context.opt['--delete-labels']:
            command = '%s --description deletionTimestamp=%sZ' % (command,(now + datetime.timedelta(minutes = int(self._context.opt['--delete-labels']))).strftime(date_format))

        # Template charts for secret
        tmp_templating_file = '%s/all_resources.tmp' % final_deploy_spec_dir
        template_command = 'template %s' % self._context.opt['--deploy-spec-dir']
        template_command = '%s %s' % (template_command, set_command)

        if self._context.opt['--values']:
            valuesFiles = self._context.opt['--values'].strip().split(',')
            values = '--values %s/' % self._context.opt['--deploy-spec-dir'] + (' --values %s/' % self._context.opt['--deploy-spec-dir']).join(valuesFiles)
            template_command = '%s %s' % (template_command, values)

        template_command = '%s --name=%s' % (template_command, release)
        template_command = '%s --namespace=%s' % (template_command, namespace)
        template_command = '%s > %s' % (template_command, tmp_templating_file)
        helm_cmd.run(template_command)

        image_pull_secret_value = 'cdp-%s-%s' % (self._context.registry, release)
        with open(tmp_templating_file, 'r') as stream:
            docs = list(yaml.safe_load_all(stream))
            for doc in docs:
                if doc is not None:
                    LOG.verbose(doc)
                    if 'kind' in doc and doc['kind'] == 'Deployment' and 'spec' in doc and 'template' in doc['spec'] and 'spec' in doc['spec']['template']:
                        find_image_pull_secret = False
                        if 'imagePullSecrets' in doc['spec']['template']['spec'] and doc['spec']['template']['spec']['imagePullSecrets']:
                            for image_pull_secret in doc['spec']['template']['spec']['imagePullSecrets']:
                                if image_pull_secret['name'] == '%s' % image_pull_secret_value:
                                    find_image_pull_secret = True
                        if not find_image_pull_secret:
                            if 'imagePullSecrets' in doc['spec']['template']['spec']:
                                doc['spec']['template']['spec']['imagePullSecrets'].append({ 'name' : '%s' % image_pull_secret_value })
                                LOG.info('Append image pull secret %s' % image_pull_secret_value)
                            else:
                                doc['spec']['template']['spec']['imagePullSecrets'] = [ { 'name' : '%s' % image_pull_secret_value } ]
                                LOG.info('Add image pull secret %s' % image_pull_secret_value)

                            LOG.info('Updated %s: %s' % (doc['kind'], doc))

        with open('%s/all_resources.yaml' % final_template_deploy_spec_dir, 'w') as outfile:
            yaml.dump_all(docs, outfile, default_flow_style=False)

        # Install or Upgrade environnement
        helm_cmd.run(command)

        if self._context.opt['--delete-labels']:
            kubectl_cmd.run('label namespace %s deletable=true creationTimestamp=%sZ deletionTimestamp=%sZ --namespace=%s --overwrite'
                % (namespace, now.strftime(date_format), (now + datetime.timedelta(minutes = int(self._context.opt['--delete-labels']))).strftime(date_format), namespace))

        self.__update_environment()


    def __buildTagAndPushOnDockerRegistry(self, tag):
        if self._context.opt['--use-docker-compose']:
            os.environ['CDP_TAG'] = tag
            os.environ['CDP_REGISTRY'] = self.__getImageName()
            self._cmd.run_command('docker-compose build')
            self._cmd.run_command('docker-compose push')
        else:
            # Hadolint
            self._cmd.run_command('hadolint Dockerfile', raise_error = False)

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
        url = 'https://%s/%s' % (self.__getHost(), self._context.opt['--path'])

        if self._context.opt['--validate-configurations']:
            url_validator = '%s/validate/configurations?url=%s' % (os.environ['CDP_BP_VALIDATOR_HOST'], url)
        else :
            raise ValueError('NOT IMPLEMENTED')

        LOG.info('---------- Silent mode ----------')
        self._cmd.run_command('curl -s %s | jq .' % url_validator)

        LOG.info('---------- Failed mode ----------')
        self._cmd.run_command('curl -sf --output /dev/null %s' % url_validator)


    def __getImageName(self):
        # Configure docker registry
        image_name = '%s/%s' % (self._context.registry, self._context.repository)
        LOG.verbose('Image name : %s', image_name)
        return image_name

    def __getImageTag(self, image_name, tag):
        return '%s:%s' %  (image_name, tag)

    def __getTagBranchName(self):
        return os.environ['CI_COMMIT_REF_SLUG']

    def __getEnvironmentName(self):
        return os.environ['CI_ENVIRONMENT_NAME'][:128]

    def __getTagLatest(self):
        return 'latest'

    def __getTagSha1(self):
        return os.environ['CI_COMMIT_SHA']

    def __getNamespace(self):
        return self.__getName(self._context.is_namespace_project_name)[:63]

    # get release name based on given parameters
    def __getRelease(self):
        if self._context.opt['--release-project-branch-name']:
            # https://github.com/kubernetes/helm/issues/1528
            return self.__getName(False)[:53]
        else:
            return self.__getNamespace()[:53]

    def __getName(self, condition):
        # Get k8s namespace
        if condition:
            name = os.environ['CI_PROJECT_NAME']
        else:
            # Get first letter for each word
            projectFistLetterEachWord = ''.join([word if len(word) == 0 else word[0] for word in re.split('[^a-zA-Z\d]', os.environ['CI_PROJECT_NAME'])])
            name = '%s%s-%s' % (projectFistLetterEachWord, os.environ['CI_PROJECT_ID'], os.getenv('CI_COMMIT_REF_SLUG', os.environ['CI_COMMIT_REF_NAME']))    # Get deployment host

        return name.replace('_', '-')

    def __getHost(self):
        dns_subdomain = os.getenv('CDP_DNS_SUBDOMAIN', None)
        # Deprecated
        if dns_subdomain is None:
            ci_runner_tags = os.getenv('CI_RUNNER_TAGS', None)
            if ci_runner_tags is not None:
                tags = ci_runner_tags.strip().split(',')
                for tag in tags:
                    dns_subdomain = os.getenv('CDP_DNS_SUBDOMAIN_%s' % tag.strip().upper().replace('-', '_'), None)
                    if dns_subdomain is not None:
                        break;

        if dns_subdomain is None:
            dns_subdomain = os.getenv('CDP_DNS_SUBDOMAIN_DEFAULT', None)
        # /Deprecated

        # Get k8s namespace
        return '%s.%s' % (self.__getRelease(), dns_subdomain)


    def __simulate_merge_on(self, force_git_config = False):
        if force_git_config or self._context.opt['--simulate-merge-on']:
            git_cmd = DockerCommand(self._cmd, self._context.opt['--docker-image-git'], self._context.opt['--volume-from'], True)

            git_cmd.run('config user.email \"%s\"' % os.environ['GITLAB_USER_EMAIL'])
            git_cmd.run('config user.name \"%s\"' % os.environ['GITLAB_USER_NAME'])

            if force_git_config:
                git_cmd.run('checkout %s' % os.environ['CI_COMMIT_REF_NAME'])

            if self._context.opt['--simulate-merge-on']:
                LOG.notice('Build docker image with the merge current branch on %s branch', self._context.opt['--simulate-merge-on'])
                # Merge branch on selected branch
                git_cmd.run('checkout %s' % self._context.opt['--simulate-merge-on'])
                git_cmd.run('reset --hard origin/%s' % self._context.opt['--simulate-merge-on'])
                git_cmd.run('merge %s --no-commit --no-ff' %  os.environ['CI_COMMIT_SHA'])

            # TODO Exception process
        else:
            LOG.notice('Build docker image with the current branch : %s', os.environ['CI_COMMIT_REF_NAME'])

    def __get_environment(self):
        if os.getenv('CDP_GITLAB_API_URL', None) is not None and os.getenv('CDP_GITLAB_API_TOKEN', None) is not None:
            gl = gitlab.Gitlab(os.environ['CDP_GITLAB_API_URL'], private_token=os.environ['CDP_GITLAB_API_TOKEN'])
            # Get a project by ID
            project = gl.projects.get(os.environ['CI_PROJECT_ID'])
            LOG.verbose('Project %s' % project)

            env = None
            # Find environment
            LOG.verbose('List environments:')
            for environment in project.environments.list(all=True):
                LOG.verbose(' - env %s.' % (environment.name))
                if environment.name == os.getenv('CI_ENVIRONMENT_NAME', None):
                    env = environment
                    break

            return env

    def __update_environment(self):
        if os.getenv('CI_ENVIRONMENT_NAME', None) is not None:
            LOG.info('******************** Update env url ********************')
            LOG.info('Search environment %s.' % os.getenv('CI_ENVIRONMENT_NAME', None))
            env = self.__get_environment()
            if env is not None:
                env.external_url = 'https://%s' % self.__getHost()
                env.save()
                LOG.info('Update external url, unless present in the file gitlabci.yaml: %s.' % env.external_url)
            else:
                LOG.warning('Environment %s not found.' % os.getenv('CI_ENVIRONMENT_NAME', None))

    @staticmethod
    def verbose(verbose):
        return verbose or os.getenv('CDP_LOG_LEVEL', None) == 'verbose'

    @staticmethod
    def warning(quiet):
        return quiet or os.getenv('CDP_LOG_LEVEL', None) == 'warning'
