#!/usr/bin/env python3.6

"""
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
        [--namespace-project-name | --namespace-name=<namespace_name> ] [--namespace-project-branch-name]
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
    --namespace-name=<namespace_name>                          Use namespace_name to create k8s namespace.
    --no-conftest                                              Do not run conftest validation tests.
    --path=<path>                                              Path to validate [default: configurations].
    --put=<file>                                               Put file to artifactory.
    --release-custom-name=<release_name>                       Customize release name with namespace-name-<release_name>
    --release-namespace-name                                   Force the release to be created with the namespace name. Same as --release-project-name if namespace-name option is not set. [default]
    --release-project-branch-name                              Force the release to be created with the project branch name.
    --release-project-env-name                                 Force the release to be created with the job env name.define in gitlab
    --release-shortproject-name                                Force the release to be created with the shortname (first letters of word + id) of the Gitlab project
    --release-project-name                                     Force the release to be created with the name of the Gitlab project
    --simulate-merge-on=<branch_name>                          Build docker image with the merge current branch on specify branch (no commit).
    --sleep=<seconds>                                          Time to sleep int the end (for debbuging) in seconds [default: 0].
    --timeout=<timeout>                                        Time in seconds to wait for any individual kubernetes operation [default: 600].
    --tiller-namespace                                         Force the tiller namespace to be the same as the pod namespace [DEPRECATED]
    --use-aws-ecr                                              Use AWS ECR from k8s configuration for pull/push docker image. [DEPRECATED]
    --use-custom-registry                                      Use custom registry for pull/push docker image. [DEPRECATED]
    --use-docker                                               Use docker to build / push image [default].
    --use-docker-compose                                       Use docker-compose to build / push image / retag container [DEPRECATED]
    --use-gitlab-registry                                      Use gitlab registry for pull/push docker image [default]. [DEPRECATED]
    --use-registry=<registry_name>                             Use registry for pull/push docker image (none, aws-ecr, gitlab, harbor or custom name for load specifics environments variables) [default: none].
    --validate-configurations                                  Validate configurations schema of BlockProvider.
    --values=<files>                                           Specify values in a YAML file (can specify multiple separate by comma). The priority will be given to the last (right-most) file specified.
    --volume-from=<host_type>                                  Volume type of sources - docker, k8s, local or docker volume description (dir:mount) [default: k8s]
"""
import base64
import configparser
import sys, os, re
import logging, verboselogs
import time, datetime
import json
import gitlab
import pyjq
import shutil

from .Context import Context
from .clicommand import CLICommand
from cdpcli import __version__
from .kanikocommand import KanikoCommand
from .dockercommand import DockerCommand
from .gitcommand import GitCommand
from .awscommand import AwsCommand
from .kubectlcommand import KubectlCommand
from .helmcommand import HelmCommand
from .conftestcommand import ConftestCommand
from docopt import docopt, DocoptExit
from .PropertiesParser import PropertiesParser
from .Yaml import Yaml
from envsubst import envsubst

LOG = verboselogs.VerboseLogger('clidriver')
LOG.addHandler(logging.StreamHandler())
LOG.setLevel(logging.INFO)

yaml = Yaml()
yaml.preserve_quotes = True
yaml.explicit_start = True

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

        if self.verbose(opt['--verbose']):
            self._cmd.run_command('env', dry_run=False)

        if opt is None:
            raise ValueError('TODO')
        else:
            self._context = Context(opt, cmd)
            LOG.verbose('Context : %s', self._context.__dict__)

            deprecated = {'docker-version','docker-image-aws','docker-image-git','docker-image-kubectl','docker-image-maven','docker-image-conftest','docker-image','use-docker-compose','namespace-project-branch-name'}
            for option in deprecated:
               if (self._context.getParamOrEnv(option)):
                 LOG.warning("\x1b[31;1mWARN : Option %s is DEPRECATED and will not be used\x1b[0m",option)

            if self._context.getParamOrEnv("docker-image-helm") :
                 image_helm_version = self._context.getParamOrEnv("docker-image-helm")
                 helm_version = image_helm_version[21]
                 LOG.warning("\x1b[31;1mWARN : Option docker-image-helm is DEPRECATED. Use --helm-version instead. Set to %s\x1b[0m")
                 opt["--helm-version"] = helm_version

            if self._context.opt['--create-default-helm']:
                 LOG.warning("\x1b[31;1mWARN : Option -create-default-helm is DEPRECATED and is replaced by --use-chart=legacy\x1b[0m")
                 opt["--use-chart"] = "legacy"

            if (not self._context.opt['--namespace-project-name'] and not self._context.opt['--namespace-name']):
                opt["--namespace-project-name"] = True                      


    def main(self, args=None):
        try:
            if self._context.opt['build']:
                self.__build()

            if self._context.opt['maven']:
                self.__maven()

            if self._context.opt['docker']:
                self.__docker()

            if self._context.opt['artifactory']:
                self.__artifactory()

            if self._context.opt['k8s']:
                self.__k8s()

            if self._context.opt['conftest']:
                self.__conftest()

            if self._context.opt['validator-server']:
                self.__validator()

        finally:
            sleep =  os.getenv('CDP_SLEEP', self._context.opt['--sleep'])
            if sleep is not None and sleep != "0":
                self._cmd.run_command('sleep %s' % sleep)


    def __build(self):
        self.__simulate_merge_on()

        docker_image_cmd = KanikoCommand(self._cmd,'', self._context.opt['--volume-from'])
        docker_image_cmd.run(self._context.opt['--command'])

    def __maven(self):
        force_git_config = False

        settings = 'maven-settings.xml'

        command = self._context.opt['--goals']

        if self._context.opt['--deploy']:
            if self._context.opt['--deploy'] == 'release':
                force_git_config = True
                command = '--batch-mode org.apache.maven.plugins:maven-release-plugin:%s:prepare org.apache.maven.plugins:maven-release-plugin:%s:perform -Dresume=false -DautoVersionSubmodules=true -DdryRun=false -DscmCommentPrefix="[ci skip]" -Dproject.scm.id=git' % (self._context.opt['--maven-release-plugin'], self._context.opt['--maven-release-plugin'])
                if self._context.opt['--altDeploymentRepository']:
                    arguments = '-DskipTests -DskipITs -Dproject.scm.id=git -DaltDeploymentRepository=release::default::%s/%s' % (os.environ['CDP_REPOSITORY_URL'],self._context.opt['--altDeploymentRepository'])
                else:
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

        self._cmd.run_command(command)

    def __docker(self):
        if self._context.opt['--use-aws-ecr'] or self._context.opt['--use-registry'] == 'aws-ecr':
            aws_cmd = AwsCommand(self._cmd, '', None, True)

            repos = []

            if self._context.opt['--use-docker'] or not (self._context.opt['--use-docker-compose']) and not (self._context.opt['--docker-build-target']):
                repos.append(self._context.repository)
            elif (self._context.opt['--docker-build-target']):
                repos.append('%s/%s' % (self._context.repository, self._context.opt['--docker-build-target']))
            elif self._context.opt['--use-docker-compose']:
                raise ValueError('docker-compose is deprecated.')

            for repo in repos:
                try:
                    aws_cmd.run('ecr list-images --repository-name %s --max-items 0' % repo)
                except ValueError:
                    LOG.warning('AWS ECR repository doesn\'t  exist. Creating this one.')
                    aws_cmd.run('ecr create-repository --repository-name %s' % repo)

        # Tag and push docker image
        if not (self._context.opt['--image-tag-branch-name'] or self._context.opt['--image-tag-latest'] or self._context.opt['--image-tag-sha1'] or self._context.opt['--image-tag']) or self._context.opt['--image-tag-branch-name']:
            # Default if none option selected
            self.__buildTagAndPushOnDockerRegistry(self.__getTagBranchName())
        if self._context.opt['--image-tag-latest']:
            self.__buildTagAndPushOnDockerRegistry(self.__getTagLatest())
        if self._context.opt['--image-tag-sha1']:
            self.__buildTagAndPushOnDockerRegistry(self.__getTagSha1())
        if self._context.opt['--image-tag']:
            self.__buildTagAndPushOnDockerRegistry(self._context.opt['--image-tag'])

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
        if not (self._context.opt['--image-tag-branch-name'] or self._context.opt['--image-tag-latest'] or self._context.opt['--image-tag-sha1'] or self._context.opt['--image-tag']) or self._context.opt['--image-tag-branch-name']:
            # Default if none option selected
            self.__callArtifactoryFile(self.__getTagBranchName(), upload_file, http_verb)
        if self._context.opt['--image-tag-latest']:
            self.__callArtifactoryFile(self.__getTagLatest(), upload_file, http_verb)
        if self._context.opt['--image-tag-sha1']:
            self.__callArtifactoryFile(self.__getTagSha1(), upload_file, http_verb)
        if self._context.opt['--image-tag']:
            self.__callArtifactoryFile(self._context.opt['--image-tag'], upload_file, http_verb)

    def __k8s(self):
        kubectl_cmd = KubectlCommand(self._cmd, '', self._context.opt['--volume-from'], True)
        helm_migration = True if self._context.getParamOrEnv("helm-migration") == "true" else False
        
        if self._context.opt['--image-tag-latest']:
            tag =  self.__getTagLatest()
            pullPolicy = 'Always'
        else:
            if self._context.opt['--image-tag-sha1']:
               tag = self.__getTagSha1()
               pullPolicy = 'IfNotPresent'
            elif self._context.opt['--image-tag']:
               tag = self._context.opt['--image-tag']
               pullPolicy = 'IfNotPresent'
            else:
               tag = self.__getTagBranchName()
               pullPolicy = 'Always'

        # Gestion des prefix des tags pour la retention auto de Harbor            
        prefixs = []
        # Ajout systématique pour les releases tempo 
        if self._context.opt['--delete-labels']:
              prefixs.append("fb")

        prefix = self._context.getParamOrEnv("image-prefix-tag")
        if prefix:
           prefixs.append(prefix)

        if len(prefixs) > 0:
            # Apply prefix to all built images
            images = self.__getImagesToBuild(self.__getImageName(), tag)
            for image in images:
                imagePath = image["image"].rsplit(':', 1)[0]
                self.__addPrefixToTag(imagePath, tag, prefixs)
            
        # Use release name instead of the namespace name for release
        release = self.__getRelease().replace('/', '-')
        namespace = self.__getNamespace()
        host = self.__getHost()

        final_deploy_spec_dir = '%s_final' % self._context.opt['--deploy-spec-dir']
        final_template_deploy_spec_dir = '%s/templates' % final_deploy_spec_dir
        tmp_chart_dir = "/cdp/k8s/charts"
        cleanupHelm2 = False

        # Helm2to3 migration
        if helm_migration:
           try:
              output = self._cmd.run_command('/cdp/scripts/migrate_helm.sh -n %s -r %s' % (namespace, release))            
           except OSError as e:            
              if e.errno > 1:
                 raise ValueError('Migration to helm 3 of release %s has failed : %s' % (release, str(e)))
              if e.errno == 1:
                 cleanupHelm2 = True

           # migration effectuee ou non nécessaire, on force la version de Helm à 3 
           self._context.opt["--helm-version"] = '3' 

        helm_cmd = HelmCommand(self._cmd, self._context.getParamOrEnv("helm-version"), self._context.opt['--volume-from'], True)
        chart_placeholders = ['<project.name>','<helm.version>']
        chart_replacement = [os.environ['CI_PROJECT_NAME'], "v1" if self.isHelm2() else "v2"]

        os.makedirs(final_template_deploy_spec_dir)
        # Need to create default helm charts
        if self._context.opt['--use-chart']:
            os.makedirs('%s/templates' % self._context.opt['--deploy-spec-dir'],0o777, True)
            # Check that the chart dir no exists
            if os.path.isfile('%s/values.yaml' % self._context.opt['--deploy-spec-dir']):
                raise ValueError('File %s/values.yaml already exists, while --deploy-spec-dir has been selected.' % self._context.opt['--deploy-spec-dir'])
            else:
                chartIsPresent = False
                #Download predefined chart in a temporary directory
                self.downloadChart(tmp_chart_dir)
                if os.path.isfile('%s/Chart.yaml' % self._context.opt['--deploy-spec-dir']):
                   chartIsPresent = True
                   # We delete default Chart.yaml cause it exists in working directory
                   os.remove(tmp_chart_dir + "/Chart.yaml")
                else:
                   # replace placeholders
                   with open('%s/Chart.yaml' % tmp_chart_dir, 'r+') as f:
                       text = f.read()
                       for i in range(0,len(chart_placeholders)):
                           text = text.replace(chart_placeholders[i], chart_replacement[i])
                       f.seek(0)
                       f.write(text)
                       f.truncate()
            self._cmd.run_command('cp -R %s/* %s/' % (tmp_chart_dir, self._context.opt['--deploy-spec-dir']))
            #shutil.copytree('%s' % tmp_chart_dir, '%s' % self._context.opt['--deploy-spec-dir'])


        shutil.copyfile('%s/Chart.yaml' % self._context.opt['--deploy-spec-dir'], '%s/Chart.yaml' % final_deploy_spec_dir)

        command = 'upgrade %s' % release
        command = '%s %s' % (command, final_deploy_spec_dir)
        if not self.isHelm2():
           command = '%s --timeout %ss' % (command, self._context.opt['--timeout'])
           #Don't retain more than 20 release for history
           command = '%s --history-max %s' % (command, 20)
        else:
          command = '%s --timeout %s' % (command, self._context.opt['--timeout'])           
   
        set_command = '--set namespace=%s' % namespace
 
        if self._context.opt['--tiller-namespace'] and self.isHelm2():
            command = '%s --tiller-namespace=%s' % (command, namespace)
        tiller_length = 0
        tiller_json = ''
        try:
            if not self._context.opt['--tiller-namespace'] and self.isHelm2():
                tiller_json = ''.join(kubectl_cmd.run('get pod --namespace %s -l name="tiller" -o json --ignore-not-found=false' % ( namespace )))
                tiller_length = len(pyjq.first('.items[] | .metadata.labels.name', json.loads(tiller_json)))
                command = '%s --tiller-namespace=%s' % (command, namespace)
        except Exception as e:
            # Not present
            LOG.verbose(str(e))

        # Need to create default helm charts
        if self._context.opt['--create-default-helm']:
            set_command = '%s --set service.internalPort=%s' % (set_command, self._context.opt['--internal-port'])

        set_command = '%s --set ingress.host=%s' % (set_command, host)
        set_command = '%s --set ingress.subdomain=%s' % (set_command, os.getenv('CDP_DNS_SUBDOMAIN', None))
        set_command = '%s --set image.commit.sha=sha-%s' % (set_command, os.environ['CI_COMMIT_SHA'][:8])
        set_command = '%s --set image.registry=%s' % (set_command,  self._context.registry)
        set_command = '%s --set image.repository=%s' % (set_command, self._context.registryRepositoryName)
        set_command = '%s --set image.tag=%s' % (set_command, tag)
        set_command = '%s --set image.pullPolicy=%s' % (set_command, pullPolicy)
        tlsSecretName = self._context.getParamOrEnv("ingress-tlsSecretName")
        if (tlsSecretName):
            set_command = '%s --set ingress.tlsSecretName=%s' % (set_command, tlsSecretName)
        # Need to add secret file for docker registry
        if not self._context.opt['--use-aws-ecr'] and not self._context.opt['--use-registry'] == 'aws-ecr':
            # Add secret (Only if secret is not exist )
            self._cmd.run_command('cp /cdp/k8s/secret/cdp-secret.yaml %s/templates/' % self._context.opt['--deploy-spec-dir'])
            set_command = '%s --set image.credentials.username=%s' % (set_command, self._context.registry_user_ro)
            set_command = '%s --set image.credentials.password=%s' % (set_command, self._context.string_protected(self._context.registry_token_ro))
            set_command = '%s --set image.imagePullSecrets=cdp-%s-%s' % (set_command, self._context.registry.replace(':', '-'),release)

        if self._context.opt['--create-gitlab-secret'] or self._context.opt['--create-gitlab-secret-hook'] :
            if os.getenv('CI_ENVIRONMENT_NAME', None) is None :
              LOG.err('Can not use gitlab secret because environment is not defined in gitlab job.')
            secretEnvPattern = 'CDP_SECRET_%s_' % os.getenv('CI_ENVIRONMENT_NAME', None)
            fileSecretEnvPattern = 'CDP_FILESECRET_%s_' % os.getenv('CI_ENVIRONMENT_NAME', None)
            #LOG.info('Looking for environnement variables starting with : %s' % secretEnvPattern)
            for envVar, envValue in dict(os.environ).items():
                if envVar.startswith(secretEnvPattern.upper(),0):
                    self.__create_secret("secret",envVar,envValue,secretEnvPattern)
                if envVar.startswith(fileSecretEnvPattern.upper(), 0):
                    self.__create_secret("file-secret", envVar, envValue, fileSecretEnvPattern)

        command = '%s -i' % command
        command = '%s --namespace=%s' % (command, namespace)
        
        if not self.isHelm2():
          try:
            kubectl_cmd.run('get namespace %s' % (namespace))
          except Exception as e:
            LOG.verbose("Namespace not exists, create it")
            command = '%s --create-namespace' % (command)
        else:
            command = '%s --force' % command        

        command = '%s --wait' % command
        command = '%s --atomic' % command

        now = datetime.datetime.utcnow()
        date_format = '%Y-%m-%dT%H%M%S'
        if self._context.opt['--delete-labels']:
            command = '%s --description deletionTimestamp=%sZ' % (command,(now + datetime.timedelta(minutes = int(self._context.opt['--delete-labels']))).strftime(date_format))

        # Template charts for secret
        tmp_templating_file = '%s/all_resources.tmp' % final_deploy_spec_dir
        if not self.isHelm2():
            template_command = 'template %s %s' % (release, self._context.opt['--deploy-spec-dir'])
        else:
            template_command = 'template %s' % (self._context.opt['--deploy-spec-dir'])
        
        template_command = '%s %s' % (template_command, set_command)

        if self._context.opt['--values']:
            valuesFiles = self._context.opt['--values'].strip().split(',')
            values = '--values %s/' % self._context.opt['--deploy-spec-dir'] + (' --values %s/' % self._context.opt['--deploy-spec-dir']).join(valuesFiles)
            template_command = '%s %s' % (template_command, values)

        if self.isHelm2():
          template_command = '%s --name=%s' % (template_command, release)

        template_command = '%s --namespace=%s' % (template_command, namespace)
        template_command = '%s > %s' % (template_command, tmp_templating_file)
        helm_cmd.run("dependency update %s" % self._context.opt['--deploy-spec-dir'])
        try:
            # Suppression de l'entrée dependencies car le helm upgrade écrase les modifications apportées après le helm tempate
            if os.path.isdir('%s/charts' % self._context.opt['--deploy-spec-dir']):
               with open('%s/Chart.yaml' % self._context.opt['--deploy-spec-dir']) as chartyml:
                 data = yaml.load(chartyml)
                 if 'dependencies' in data:
                    del data['dependencies']
                    with open('%s/Chart.yaml' % final_deploy_spec_dir, "w") as f:
                        yaml.dump(data, f)
        except OSError as e:
            LOG.error(str(e))        
        helm_cmd.run(template_command)

        image_pull_secret_value = 'cdp-%s-%s' % (self._context.registry, release)
        image_pull_secret_value = image_pull_secret_value.replace(':', '-')

        with open(tmp_templating_file, 'r') as stream:
            docs = list(yaml.load_all(stream))
            final_docs = []
            for doc in docs:
                if doc is not None:
                    # Ajout du label deletable sur tous les objets si la release est temporaire
                    if "metadata" in doc and "labels" in doc['metadata']:
                       doc['metadata']['labels']['deletable'] = "true" if self._context.opt['--delete-labels'] else "false"

                    final_docs.append(doc)
                    CLIDriver.addGitlabLabels(doc)
                    #Manage Deployement and
                    if os.getenv('CDP_MONITORING')and os.getenv('CDP_MONITORING', 'TRUE').upper() != "FALSE":
                        if os.getenv('CDP_ALERTING', 'TRUE').upper()=="FALSE":
                            doc = CLIDriver.addMonitoringLabel(doc, False)
                        else:
                            doc = CLIDriver.addMonitoringLabel(doc, True)
                    if not self._context.opt['--use-aws-ecr'] and not self._context.opt['--use-registry'] == 'aws-ecr' and 'kind' in doc and  'spec' in doc and ('template' in doc['spec'] or 'jobTemplate' in doc['spec']):
                        doc=CLIDriver.addImageSecret(doc,image_pull_secret_value)
                    
                    LOG.verbose(doc)

        with open('%s/all_resources.yaml' % final_template_deploy_spec_dir, 'w') as outfile:
            LOG.info(yaml.dump_all(final_docs))
            yaml.dump_all(final_docs, outfile)

        #Run conftest
        conftest_temp_dir = '%s_conftest' % self._context.opt['--deploy-spec-dir']
        try:
            os.makedirs(conftest_temp_dir)
            shutil.copyfile('%s/all_resources.yaml' % final_template_deploy_spec_dir, '%s/all_resources.yaml' % conftest_temp_dir)
        except OSError as e:
            LOG.error(str(e))

        if (os.path.isdir('%s/data' % self._context.opt['--deploy-spec-dir'])):
            shutil.copytree('%s/data' % self._context.opt['--deploy-spec-dir'], '%s/data' % conftest_temp_dir)
        
        if (os.path.isdir('%s/policy' % self._context.opt['--deploy-spec-dir'])):
            shutil.copytree('%s/policy' % self._context.opt['--deploy-spec-dir'], '%s/policy' % conftest_temp_dir)

        self.__runConftest(os.path.abspath(conftest_temp_dir), 'all_resources.yaml'.split(','))

        # Install or Upgrade environnement
        helm_cmd.run(command)

        # Tout s'est bien passé, on clean la release ou le namespace si dernière release
        if cleanupHelm2:
           self._cmd.run_command("/cdp/scripts/cleanup.sh -n %s -r %s" % (namespace, release))            

        self.__update_environment()

    def __create_secret(self,type,envVar,envValue,secretEnvPattern):
        if type == 'file-secret':
            secretFile = open(envValue, "r")
            fileContent = secretFile.read()
            secretFile.close()
            envValue = str(base64.b64encode(bytes(fileContent, 'utf-8')), 'utf-8')
        if not os.path.isfile('%s/templates/cdp-gitlab-%s.yaml' % (self._context.opt['--deploy-spec-dir'],type)):
            self._cmd.run_command('cp /cdp/k8s/secret/cdp-gitlab-%s.yaml %s/templates/' % (type , self._context.opt['--deploy-spec-dir']))
        self._cmd.run_secret_command('echo "  %s: \'%s\'" >> %s/templates/cdp-gitlab-%s.yaml' % (envVar[len(secretEnvPattern):],envValue,self._context.opt['--deploy-spec-dir'],type))
        if self._context.opt['--create-gitlab-secret-hook']:
            if not os.path.isfile('%s/templates/cdp-gitlab-%s.yaml' % (self._context.opt['--deploy-spec-dir'],type+"-hook")):
                self._cmd.run_command('cp /cdp/k8s/secret/cdp-gitlab-%s.yaml %s/templates/' % (type+"-hook" , self._context.opt['--deploy-spec-dir']))
            self._cmd.run_secret_command('echo "  %s: \'%s\'" >> %s/templates/cdp-gitlab-%s.yaml' % (envVar[len(secretEnvPattern):],envValue,self._context.opt['--deploy-spec-dir'],type+"-hook"))

    @staticmethod
    def addImageSecret(doc,image_pull_secret_value):
        if doc['kind'] == 'Deployment' or doc['kind'] == 'StatefulSet' or doc['kind'] == 'Job':
            yaml_doc = doc['spec']['template']['spec']
            if 'imagePullSecrets' in yaml_doc and yaml_doc['imagePullSecrets']:
                for image_pull_secret in yaml_doc['imagePullSecrets']:
                    if (image_pull_secret['name'] != '%s' % image_pull_secret_value):
                        doc['spec']['template']['spec']['imagePullSecrets'].append({'name': '%s' % image_pull_secret_value})
                        LOG.info('Append image pull secret %s' % image_pull_secret_value)
            else:
                doc['spec']['template']['spec']['imagePullSecrets'] = [{'name': '%s' % image_pull_secret_value}]
                LOG.info('Add imagePullSecret')

        elif doc['kind'] == 'CronJob':
            yaml_doc = doc['spec']['jobTemplate']['spec']['template']['spec']
            if 'imagePullSecrets' in yaml_doc and yaml_doc['imagePullSecrets']:
                LOG.info('Find imagepullsecret')
                for image_pull_secret in yaml_doc['imagePullSecrets']:
                    if image_pull_secret['name'] == '%s' % image_pull_secret_value:
                        LOG.info('secret name find')
                        if (image_pull_secret['name'] != '%s' % image_pull_secret_value):
                            doc['spec']['jobTemplate']['spec']['template']['spec']['imagePullSecrets'].append({'name': '%s' % image_pull_secret_value})
                            LOG.info('Append image pull secret %s' % image_pull_secret_value)
            else:
                 doc['spec']['jobTemplate']['spec']['template']['spec']['imagePullSecrets'] = [{'name': '%s' % image_pull_secret_value}]
                 LOG.info('Add imagePullSecret')
        return doc

    @staticmethod
    def addMonitoringLabel(doc,escalation):
        if doc['kind'] == 'Deployment' or doc['kind'] == 'StatefulSet' or doc['kind'] == 'Service':
             doc['metadata']['labels']['monitoring'] = 'true'
             if 'template' in doc['spec'].keys():
                doc['spec']['template']['metadata']['labels']['monitoring']  = 'true'
             LOG.warning("Add monitoring Label")
             if escalation:
                 doc['metadata']['labels']['owner-escalation'] = 'true'
                 if 'template' in doc['spec'].keys():
                    doc['spec']['template']['metadata']['labels']['owner-escalation'] = 'true'
             else:
                 doc['metadata']['labels']['owner-escalation'] = 'false'
                 if 'template' in doc['spec'].keys():
                    doc['spec']['template']['metadata']['labels']['owner-escalation'] = 'false'
        return doc

    def addGitlabLabels(doc):
        if doc['kind'] == 'Deployment' or doc['kind'] == 'StatefulSet' or doc['kind'] == 'Service':
           gl = gitlab.Gitlab(os.environ['CDP_GITLAB_API_URL'], private_token=os.environ['CDP_GITLAB_API_TOKEN'])
           project = gl.projects.get(os.environ['CI_PROJECT_ID'])
           labels={}
           for index, value in enumerate(project.attributes['tag_list']):
               if "=" in value:
                  tag = value.split("=")
                  doc['metadata']['labels'][tag[0]] = tag[1]
                  if 'template' in doc['spec'].keys():
                      doc['spec']['template']['metadata']['labels'][tag[0]] = tag[1]
        return doc

    def __addPrefixToTag(self, image_repo, tag, prefixs):
      try:
        for prefix in prefixs:
           prefixTag = "%s-%s" % (prefix, tag)
           source_image_tag = self.__getImageTag(image_repo,  tag)
           dest_image_tag = self.__getImageTag(image_repo, prefixTag)
           LOG.info("Nouveau tag %s sur l'image %s" % (dest_image_tag, source_image_tag))
           # Utilisation de Skopeo
           self._cmd.run_command('skopeo copy docker://%s docker://%s' % (source_image_tag, dest_image_tag))
      except OSError as e:
               print('************************** SKPEO *******************************')
               print(e)
               print('****************************************************************')
               raise e          
        
      return prefixTag
        
    def __buildTagAndPushOnDockerRegistry(self, tag):
        kaniko_cmd = KanikoCommand(self._cmd, '', self._context.opt['--volume-from'], True)
        image_tag = self.__getImageTag(self.__getImageName(), tag)
        if self._context.opt['--use-docker-compose']:
             raise ValueError('docker-compose is deprecated.')
        else:
          images_to_build = self.__getImagesToBuild(self.__getImageName(), tag)
          for image_to_build in images_to_build:
            dockerfile = image_to_build["dockerfile"]
            context = image_to_build["context"]
            image_tag = image_to_build["image"]
            # Hadolint
            self._cmd.run_command('hadolint %s/%s' % (context, dockerfile), raise_error = False)

            # Tag docker image
            docker_build_command = '--context %s --dockerfile %s --destination %s' % (context,dockerfile,image_tag)
            if self._context.opt['--docker-build-target']:
              docker_build_command = '%s --target %s' % (docker_build_command, self._context.opt['--docker-build-target'])
            if 'CDP_ARTIFACTORY_TAG_RETENTION' in os.environ and (self._context.opt['--use-custom-registry'] or self._context.opt['--use-registry'] == 'artifactory' or self._context.opt['--use-registry'] == 'custom'):
              docker_build_command = '%s --label com.jfrog.artifactory.retention.maxCount="%s"' % (docker_build_command, os.environ['CDP_ARTIFACTORY_TAG_RETENTION'])

            if self._context.opt['--build-arg']:
                self._context.opt['--build-arg'].sort()
                for buildarg in self._context.opt['--build-arg']:
                    docker_build_command = '%s --build-arg %s' % (docker_build_command, buildarg)

            kaniko_cmd.run(docker_build_command)
            
    def __conftest(self):
        dir = self._context.opt['--deploy-spec-dir']
        files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir,f))]
        self.__runConftest(dir,files,False)

    def __callArtifactoryFile(self, tag, upload_file, http_verb):
        if http_verb == 'PUT':
            self._cmd.run_command('curl --fail -X PUT %s/%s/%s/ -H X-JFrog-Art-Api:%s -T %s' % (os.environ['CDP_ARTIFACTORY_PATH'], self._context.repository, tag, os.environ['CDP_ARTIFACTORY_TOKEN'], upload_file))
        elif http_verb == 'DELETE':
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

    def __getImagesToBuild(self,image, tag):

        os.environ['CDP_TAG'] = tag
        os.environ['CDP_REGISTRY'] = image

        # Default image if no build file
        images_to_build = [ {"composant": "image", "dockerfile" : "Dockerfile","context": self._context.opt['--build-context'],"image": self.__getImageTag(image, tag)}]
        if os.path.isfile(self._context.opt['--build-file']):
           images_to_build = []
           with open(self._context.opt['--build-file']) as chartyml:
                 data = yaml.load(chartyml)
                 for service in data["services"]:
                     servicedef = data["services"][service]
                     images_to_build.append({"composant": service, "dockerfile" : servicedef["build"]["dockerfile"],"context": servicedef["build"]["context"], "image": envsubst(servicedef["image"])})
        return images_to_build

    def __getImageName(self):
        # Configure docker registry
        image_name = '%s/%s' % (self._context.registry, self._context.registryRepositoryName)
        if self._context.opt['--docker-build-target']:
           image_name = '%s/%s' % (image_name, self._context.opt['--docker-build-target'])
        return image_name

    def __getImageTag(self, image_name, tag):
        return '%s:%s' %  (image_name, tag)

    def __getTagBranchName(self):
        return os.environ['CI_COMMIT_REF_SLUG']

    def __getEnvironmentName(self):
        return os.environ['CI_ENVIRONMENT_NAME'].replace('/', '-').replace('_', '-')[:128]

    def __getTagLatest(self):
        return 'latest'

    def __getTagSha1(self):
        return os.environ['CI_COMMIT_SHA']

    def __getNamespace(self):
        name = os.environ['CI_PROJECT_NAME']
        if (self._context.opt['--namespace-name']):
            name = self._context.opt['--namespace-name'] 
        return name.replace('_', '-')[:63]

    # get release name based on given parameters
    def __getRelease(self):
        if self._context.opt['--release-project-branch-name']:
            projectFistLetterEachWord = self.__getShortProjectName()
            release = '%s-%s' % (projectFistLetterEachWord, os.getenv('CI_COMMIT_REF_SLUG', os.environ['CI_COMMIT_REF_NAME']))
        elif self._context.opt['--release-project-env-name']:
            release = self.__getEnvName()
        elif self._context.opt['--release-custom-name']:
            release =  (self.__getShortProjectName() +'-'+ self._context.opt['--release-custom-name'])
        elif self._context.opt['--release-project-name']:
            release = os.environ['CI_PROJECT_NAME']
        elif self._context.opt['--release-shortproject-name']:
            release = self.__getShortProjectName()
        else:
            release = self.__getNamespace()
        # K8s ne supporte plus les . dans les noms de release
        return release.replace('_', '-').replace(".","-")[:53]

    def __getShortProjectName(self):
        namespace = os.environ['CI_PROJECT_NAME']
        projectFistLetterEachWord = ''.join([word if len(word) == 0 else word[0] for word in re.split('[^a-zA-Z0-9]',namespace)]) 
        return projectFistLetterEachWord + os.environ['CI_PROJECT_ID']

    def __getEnvName(self):
        # Get k8s namespace
        if(self.__getEnvironmentName() is not None):
            # Get first letter for each word
            projectFistLetterEachWord = self.__getShortProjectName()
            name = '%s-env-%s' % (projectFistLetterEachWord, self.__getEnvironmentName().replace('/', '-'))    # Get deployment host
        elif(self.__getEnvironmentName() is None):
            LOG.err('can not use environnement release option because environment is not defined in gitlab job.')

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
            git_cmd = GitCommand(self._cmd, '', self._context.opt['--volume-from'], True)

            git_cmd.run('config user.email \"%s\"' % os.environ['GITLAB_USER_EMAIL'])
            git_cmd.run('config user.name \"%s\"' % os.environ['GITLAB_USER_NAME'])
            git_cmd.run('fetch')

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

    def __get_team(self):
        gl = gitlab.Gitlab(os.environ['CDP_GITLAB_API_URL'], private_token=os.environ['CDP_GITLAB_API_TOKEN'])
        # Get a project by ID
        project = gl.projects.get(os.environ['CI_PROJECT_ID'])
        pattern = re.compile("^team=")
        for index, value in enumerate(project.attributes['tag_list']):
            if pattern.match(value):
                return value[5:]
        return "empty_team"

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

    def __getLabelName(self):
        return ( os.getenv("CDP_REGISTRY_LABEL"))

    '''
    Lancement des tests conftest. 
      <chartdir> : répertoire de définition des charts du projet. Peut contenir les répertoires policy et data contenant
                  restpectivement les policies à appliquer et les éventuelles valeurs spécifiques       
      <charts>   : Tableau des charts à controller
    '''
    def __runConftest(self, chartdir, charts, withWorkingDir=True):
        no_conftest = self._context.getParamOrEnv('no-conftest')
        if (no_conftest is True or no_conftest == "true"):
            return

       
        conftest_repo = self._context.getParamOrEnv('conftest-repo','')
        if (conftest_repo != "" and conftest_repo != "none" ):
            try: 
               repo = conftest_repo.split(":")
               repo_name = repo[0].replace("/","%2F")
               repo_sha= ""
               repo_dir= ""
               strip=1
               if (len(repo) > 1):
                   if len(repo[1]) > 0:
                     repo_dir="'*/%s'" % repo[1]
                     strip= repo_dir.count("/") + 1
                   if (len(repo) > 2):
                     repo_sha="?sha=%s" % repo[2]

               cmd = 'curl -H "PRIVATE-TOKEN: %s" -skL %s/api/v4/projects/%s/repository/archive.tar.gz%s | tar zx --wildcards --strip %s -C %s %s' % (os.environ['CDP_GITLAB_API_TOKEN'], os.environ['CDP_GITLAB_API_URL'], repo_name,repo_sha, strip, chartdir, repo_dir)
               self._cmd.run_secret_command(cmd.strip())
            except Exception as e:
                LOG.error("Error when downloading %s - Pass - %s" % (conftest_repo,str(e)))               

        if (not os.path.isdir("%s/policy" % chartdir)):
            LOG.info('conftest : No policy found in %s - pass' % chartdir)
            return

        conftest_cmd = ConftestCommand(self._cmd,'', self._context.opt['--volume-from'], True)
        cmd = "test --policy policy"
        if (os.path.isdir("%s/data" % chartdir)):
           cmd = "%s --data data" % cmd

        # Boucle sur tous les namespaces
        conftest_ns = self._context.getParamOrEnv('conftest-namespaces','').split(",")
        LOG.info("=============================================================")
        LOG.info("== CONFTEST                                               ==")
        LOG.info("=============================================================")
        for ns in conftest_ns:
          if (ns == "all"):
              cmd = "%s --all-namespaces" % (cmd)
          elif not ns == "":
              cmd = "%s --namespace=%s" % (cmd, ns)

          conftest_cmd.run("%s %s" % (cmd, ' '.join(charts)), None, None, chartdir if withWorkingDir else False)

    def isHelm2(self):
        return self._context.getParamOrEnv("helm-version") == '2'

    def isHelm3(self):
        return self._context.getParamOrEnv("helm-version") == '3'

    @staticmethod
    def verbose(verbose):
        return verbose or os.getenv('CDP_LOG_LEVEL', None) == 'verbose'

    @staticmethod
    def warning(quiet):
        return quiet or os.getenv('CDP_LOG_LEVEL', None) == 'warning'

    def downloadChart(self, chartdir):
        chart_repo = self._context.getParamOrEnv('chart-repo',"")
        if (chart_repo == "" or chart_repo == "none" ):
            return

        chart_repo = chart_repo.replace("/","%2F")
        use_chart = self._context.getParamOrEnv('use-chart',"")
        if (use_chart != "" and use_chart != "none" ):

            try: 
               helm_chart = use_chart.split(":")
               chart_name = helm_chart[0]
               chart_sha = "master" if len(helm_chart) == 1 else helm_chart[1]
               strip=chart_name.count("/") + 2 # Pour ne créer le répertoire du chart

               cmd = 'curl -H "PRIVATE-TOKEN: %s" -skL %s/api/v4/projects/%s/repository/archive.tar.gz?sha=%s | tar zx --wildcards --strip %s -C %s \'*/%s\'' % (os.environ['CDP_GITLAB_API_TOKEN'], os.environ['CDP_GITLAB_API_URL'], chart_repo,chart_sha, strip, chartdir, chart_name)
               self._cmd.run_secret_command(cmd.strip())
            except Exception as e:
                LOG.error("Error when downloading %s - Pass - %s/%s" % (chart_repo, use_chart,str(e)))               

