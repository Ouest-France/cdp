#!/usr/bin/env python
import unittest
import os, sys
import datetime

from cdpcli.clicommand import CLICommand
from cdpcli.clidriver import CLIDriver, __doc__
from docopt import docopt, DocoptExit
from freezegun import freeze_time
from mock import call, patch

class FakeCommand(object):
    def __init__(self, verif_cmd):
        self._verif_cmd = verif_cmd
        self._index = 0
        self._tc = unittest.TestCase('__init__')

    def run_command(self, cmd, dry_run = None):
        try:
            # Check cmd parameter
            self._tc.assertEqual(self._verif_cmd[self._index]['cmd'], cmd)

            # Check dry-run parameter
            try:
                self._tc.assertEqual(self._verif_cmd[self._index]['dry_run'], dry_run)
            except KeyError:
                self._tc.assertTrue(dry_run is None)

            # Check variable environnement parameter
            try:
                env_vars = self._verif_cmd[self._index]['env_vars']
                for key, value in env_vars.items():
                    self._tc.assertEquals(os.environ[key], value)
            except KeyError:
                pass

            # Return mock output
            output = self._verif_cmd[self._index]['output']

            try:
                raise self._verif_cmd[self._index]['throw'](output)
            except KeyError:
                pass

            return output
        finally:
            self._index = self._index + 1

    def verify_commands(self):
        self._tc.assertEqual(len(self._verif_cmd), self._index)

class TestCliDriver(unittest.TestCase):

    cdp_gitlab_registry_read_only_token = 'abcdefghijklmnopqrstuvwxyz'
    ci_job_token = 'gitlab-ci'
    ci_commit_sha = '0123456789abcdef0123456789abcdef01234567'
    ci_registry_user = 'gitlab-ci'
    ci_registry = 'registry.gitlab.com'
    ci_commit_ref_name = 'branch_helloworld'
    ci_registry_image = 'registry.gitlab.com/helloworld/helloworld'
    ci_project_name = 'helloworld'
    ci_project_path = 'HelloWorld/HelloWorld'
    dns_subdomain = 'example.com'
    gitlab_user_email = 'test@example.com'
    gitlab_user_id = '12334'
    cdp_custom_registry_user = 'cdp_custom_registry_user'
    cdp_custom_registry_token = '1298937676109092092'
    cdp_custom_registry_read_only_token = '1298937676109092093'
    cdp_custom_registry = 'docker-artifact.fr:8123'
    cdp_artifactory_path = 'http://repo.fr/test'
    cdp_artifactory_token = '29873678036783'


    env_cdp_tag = 'CDP_TAG'
    env_cdp_registry = 'CDP_REGISTRY'

    @classmethod
    def setUpClass(cls):
        os.environ['CDP_GITLAB_REGISTRY_READ_ONLY_TOKEN'] = TestCliDriver.cdp_gitlab_registry_read_only_token
        os.environ['CI_JOB_TOKEN'] = TestCliDriver.ci_job_token
        os.environ['CI_COMMIT_SHA'] = TestCliDriver.ci_commit_sha
        os.environ['CI_REGISTRY_USER'] = TestCliDriver.ci_registry_user
        os.environ['CI_REGISTRY'] = TestCliDriver.ci_registry
        os.environ['CI_COMMIT_REF_NAME'] = TestCliDriver. ci_commit_ref_name
        os.environ['CI_REGISTRY_IMAGE'] = TestCliDriver.ci_registry_image
        os.environ['CI_PROJECT_NAME'] = TestCliDriver.ci_project_name
        os.environ['CI_PROJECT_PATH'] = TestCliDriver.ci_project_path
        os.environ['DNS_SUBDOMAIN'] = TestCliDriver.dns_subdomain
        os.environ['GITLAB_USER_EMAIL'] = TestCliDriver.gitlab_user_email
        os.environ['GITLAB_USER_ID'] = TestCliDriver.gitlab_user_id
        os.environ['CDP_CUSTOM_REGISTRY_USER'] = TestCliDriver.cdp_custom_registry_user
        os.environ['CDP_CUSTOM_REGISTRY_TOKEN'] = TestCliDriver.cdp_custom_registry_token
        os.environ['CDP_CUSTOM_REGISTRY_READ_ONLY_TOKEN'] = TestCliDriver.cdp_custom_registry_read_only_token
        os.environ['CDP_CUSTOM_REGISTRY'] = TestCliDriver.cdp_custom_registry
        os.environ['CDP_ARTIFACTORY_PATH'] = TestCliDriver.cdp_artifactory_path
        os.environ['CDP_ARTIFACTORY_TOKEN'] = TestCliDriver.cdp_artifactory_token
        os.environ['CDP_AWS_ACCESS_KEY_ID'] = 'accessKeyId'
        os.environ['CDP_AWS_SECRET_ACCESS_KEY'] = 'secretAccessKey'

    def test_build_dind_docker_host(self):
        # Create FakeCommand
        image_name = 'maven:3.5-jdk-8'
        command_name = 'mvn clean install'

        docker_host = 'tcp://docker:2375'
        os.environ['DOCKER_HOST'] = docker_host

        verif_cmd = [
            {'cmd': 'docker pull docker:dind', 'output': 'unnecessary'},
            {'cmd': 'docker run --rm --privileged --name docker-dind -d docker:dind', 'output': 'unnecessary'},
            {'cmd': 'docker pull %s' % (image_name), 'output': 'unnecessary'},
            {'cmd': 'docker run --rm --link docker-dind:docker -e DOCKER_HOST=tcp://docker:2375 -v ${PWD}:/cdp-data %s /bin/sh -c \'cd /cdp-data; %s\'' % (image_name, command_name), 'output': 'unnecessary'}
        ]
        self.__run_CLIDriver({ 'build', '--docker-image=%s' % image_name, '--command=%s' % command_name, '--dind' }, verif_cmd, docker_host = docker_host)

    def test_build_verbose_simulatemergeon_sleep(self):
        # Create FakeCommand
        branch_name = 'master'
        image_name = 'maven:3.5-jdk-8'
        command_name = 'mvn clean install'
        sleep = 10
        verif_cmd = [
            {'cmd': 'env', 'output': 'unnecessary'},
            {'cmd': 'git config --global user.email \"%s\"' % TestCliDriver.gitlab_user_email, 'output': 'unnecessary'},
            {'cmd': 'git config --global user.name \"%s\"' % TestCliDriver.gitlab_user_id, 'output': 'unnecessary'},
            {'cmd': 'git checkout %s' % branch_name, 'output': 'unnecessary'},
            {'cmd': 'git reset --hard origin/%s' % branch_name, 'output': 'unnecessary'},
            {'cmd': 'git merge %s --no-commit --no-ff' % TestCliDriver.ci_commit_sha, 'output': 'unnecessary'},
            {'cmd': 'docker pull %s' % (image_name), 'output': 'unnecessary'},
            {'cmd': 'docker run --rm  -v ${PWD}:/cdp-data %s /bin/sh -c \'cd /cdp-data; %s\'' % (image_name, command_name), 'output': 'unnecessary'},
            {'cmd': 'git checkout .', 'output': 'unnecessary'},
            {'cmd': 'sleep %s' % sleep, 'output': 'unnecessary'}
        ]
        self.__run_CLIDriver({ 'build', '--verbose', '--docker-image=%s' % image_name, '--command=%s' % command_name, '--simulate-merge-on=%s' % branch_name, '--sleep=%s' % sleep }, verif_cmd)

    def test_docker_usedocker_imagetagbranchname_usegitlabregistry_sleep_docker_host(self):
        # Create FakeCommand
        sleep = 10

        docker_host = 'tcp://docker:2375'
        os.environ['DOCKER_HOST'] = docker_host

        verif_cmd = [
            {'cmd': 'docker login -u %s -p %s https://%s' % (TestCliDriver.ci_registry_user, TestCliDriver.ci_job_token, TestCliDriver.ci_registry), 'output': 'unnecessary'},
            {'cmd': 'docker build -t %s:%s .' % (TestCliDriver.ci_registry_image, TestCliDriver.ci_commit_ref_name), 'output': 'unnecessary'},
            {'cmd': 'docker push %s:%s' % (TestCliDriver.ci_registry_image, TestCliDriver.ci_commit_ref_name), 'output': 'unnecessary'},
            {'cmd': 'sleep %s' % sleep, 'output': 'unnecessary'}
        ]
        self.__run_CLIDriver({ 'docker', '--use-docker', '--use-gitlab-registry', '--sleep=%s' % sleep }, verif_cmd, docker_host = docker_host)

    def test_docker_usedocker_imagetagsha1_usecustomregistry(self):
        # Create FakeCommand
        verif_cmd = [
            {'cmd': 'docker login -u %s -p %s https://%s' % (TestCliDriver.cdp_custom_registry_user, TestCliDriver.cdp_custom_registry_token, TestCliDriver.cdp_custom_registry), 'output': 'unnecessary'},
            {'cmd': 'docker build -t %s/%s:%s .' % (TestCliDriver.cdp_custom_registry, TestCliDriver.ci_project_path.lower(), TestCliDriver.ci_commit_sha), 'output': 'unnecessary'},
            {'cmd': 'docker push %s/%s:%s' % (TestCliDriver.cdp_custom_registry, TestCliDriver.ci_project_path.lower(), TestCliDriver.ci_commit_sha), 'output': 'unnecessary'}
        ]
        self.__run_CLIDriver({ 'docker', '--use-docker', '--use-custom-registry', '--image-tag-sha1' }, verif_cmd)


    def test_docker_verbose_usedockercompose_imagetaglatest_imagetagsha1_useawsecr_withrepo(self):
        # Create FakeCommand
        aws_host = 'ecr.amazonaws.com'
        login_cmd = 'docker login -u user -p pass https://%s' % aws_host
        verif_cmd = [
            {'cmd': 'aws ecr get-login --no-include-email --region eu-central-1', 'output': login_cmd, 'dry_run': False},
            {'cmd': 'env', 'output': 'unnecessary'},
            {'cmd': login_cmd, 'output': 'unnecessary'},
            {'cmd': 'aws ecr list-images --repository-name %s --max-items 0' % TestCliDriver.ci_project_path.lower(), 'output': 'unnecessary'},
            {'cmd': 'docker-compose build', 'output': 'unnecessary', 'env_vars' : { TestCliDriver.env_cdp_tag: 'latest', TestCliDriver.env_cdp_registry: '%s/%s' % (aws_host, TestCliDriver.ci_project_path.lower())}},
            {'cmd': 'docker-compose push', 'output': 'unnecessary', 'env_vars' : { TestCliDriver.env_cdp_tag: 'latest', TestCliDriver.env_cdp_registry: '%s/%s' % (aws_host, TestCliDriver.ci_project_path.lower())}},
            {'cmd': 'docker-compose build', 'output': 'unnecessary', 'env_vars' : { TestCliDriver.env_cdp_tag: TestCliDriver.ci_commit_sha, TestCliDriver.env_cdp_registry: '%s/%s' % (aws_host, TestCliDriver.ci_project_path.lower())}},
            {'cmd': 'docker-compose push', 'output': 'unnecessary', 'env_vars' : { TestCliDriver.env_cdp_tag: TestCliDriver.ci_commit_sha, TestCliDriver.env_cdp_registry: '%s/%s' % (aws_host, TestCliDriver.ci_project_path.lower())}}
        ]
        self.__run_CLIDriver({ 'docker', '--verbose', '--use-docker-compose', '--image-tag-latest', '--image-tag-sha1', '--use-aws-ecr' }, verif_cmd)


    def test_docker_verbose_usedockercompose_imagetaglatest_imagetagsha1_useawsecr_withoutrepo(self):
        # Create FakeCommand
        aws_host = 'ecr.amazonaws.com'
        login_cmd = 'docker login -u user -p pass https://%s' % aws_host
        verif_cmd = [
            {'cmd': 'aws ecr get-login --no-include-email --region eu-central-1', 'output': login_cmd, 'dry_run': False},
            {'cmd': 'env', 'output': 'unnecessary'},
            {'cmd': login_cmd, 'output': 'unnecessary'},
            {'cmd': 'aws ecr list-images --repository-name %s --max-items 0' % TestCliDriver.ci_project_path.lower(), 'output': 'unnecessary', 'throw': ValueError},
            {'cmd': 'aws ecr create-repository --repository-name %s' % TestCliDriver.ci_project_path.lower(), 'output': 'unnecessary'},
            {'cmd': 'docker-compose build', 'output': 'unnecessary', 'env_vars' : { TestCliDriver.env_cdp_tag: 'latest', TestCliDriver.env_cdp_registry: '%s/%s' % (aws_host, TestCliDriver.ci_project_path.lower())}},
            {'cmd': 'docker-compose push', 'output': 'unnecessary', 'env_vars' : { TestCliDriver.env_cdp_tag: 'latest', TestCliDriver.env_cdp_registry: '%s/%s' % (aws_host, TestCliDriver.ci_project_path.lower())}},
            {'cmd': 'docker-compose build', 'output': 'unnecessary', 'env_vars' : { TestCliDriver.env_cdp_tag: TestCliDriver.ci_commit_sha, TestCliDriver.env_cdp_registry: '%s/%s' % (aws_host, TestCliDriver.ci_project_path.lower())}},
            {'cmd': 'docker-compose push', 'output': 'unnecessary', 'env_vars' : { TestCliDriver.env_cdp_tag: TestCliDriver.ci_commit_sha, TestCliDriver.env_cdp_registry: '%s/%s' % (aws_host, TestCliDriver.ci_project_path.lower())}}
        ]
        self.__run_CLIDriver({ 'docker', '--verbose', '--use-docker-compose', '--image-tag-latest', '--image-tag-sha1', '--use-aws-ecr' }, verif_cmd)


    def test_artifactory_put_imagetagsha1_imagetaglatest_dockerhost(self):
        # Create FakeCommand
        upload_file = 'config/values.yaml'

        docker_host = 'tcp://docker:2375'
        os.environ['DOCKER_HOST'] = docker_host

        verif_cmd = [
            {'cmd': 'curl --fail -X PUT %s/%s/%s/ -H X-JFrog-Art-Api:%s -T %s'
                % (TestCliDriver.cdp_artifactory_path,
                    TestCliDriver.ci_project_path.lower(),
                    'latest',
                    TestCliDriver.cdp_artifactory_token,
                    upload_file ), 'output': 'unnecessary'},
            {'cmd': 'curl --fail -X PUT %s/%s/%s/ -H X-JFrog-Art-Api:%s -T %s'
                % (TestCliDriver.cdp_artifactory_path,
                    TestCliDriver.ci_project_path.lower(),
                    TestCliDriver.ci_commit_sha,
                    TestCliDriver.cdp_artifactory_token,
                    upload_file ), 'output': 'unnecessary'}
        ]
        self.__run_CLIDriver({ 'artifactory', '--put=%s' % upload_file, '--image-tag-sha1', '--image-tag-latest' }, verif_cmd, docker_host = docker_host)

    def test_artifactory_del(self):
        # Create FakeCommand
        upload_file = 'config/values.staging.yaml'
        verif_cmd = [
            {'cmd': 'curl --fail -X DELETE %s/%s/%s/%s -H X-JFrog-Art-Api:%s'
                % (TestCliDriver.cdp_artifactory_path,
                    TestCliDriver.ci_project_path.lower(),
                    TestCliDriver.ci_commit_ref_name,
                    upload_file,
                    TestCliDriver.cdp_artifactory_token), 'output': 'unnecessary'}
        ]
        self.__run_CLIDriver({ 'artifactory', '--delete=%s' % upload_file }, verif_cmd)


    def test_k8s_usegitlabregistry_namespaceprojectbranchname_values_dockerhost(self):
        # Create FakeCommand
        namespace = '%s-%s' % (TestCliDriver.ci_project_name, TestCliDriver.ci_commit_ref_name)
        namespace = namespace.replace('_', '-')
        staging_file = 'values.staging.yaml'
        int_file = 'values.int.yaml'
        values = ','.join([staging_file, int_file])

        docker_host = 'tcp://docker:2375'
        os.environ['DOCKER_HOST'] = docker_host

        verif_cmd = [
            {'cmd': 'cp /cdp/k8s/secret/cdp-secret.yaml charts/templates/', 'output': 'unnecessary'},
            {'cmd': 'helm upgrade %s charts --timeout 300 --set namespace=%s --set ingress.host=%s.%s.%s --set image.commit.sha=%s --set image.registry=%s --set image.repository=%s --set image.tag=%s --set image.credentials.username=%s --set image.credentials.password=%s --values charts/%s --values charts/%s --debug -i --namespace=%s'
                % (namespace,
                    namespace,
                    TestCliDriver.ci_commit_ref_name,
                    TestCliDriver.ci_project_name,
                    TestCliDriver.dns_subdomain,
                    TestCliDriver.ci_commit_sha[:8],
                    TestCliDriver.ci_registry,
                    TestCliDriver.ci_project_path.lower(),
                    TestCliDriver.ci_commit_ref_name,
                    TestCliDriver.ci_registry_user,
                    TestCliDriver.cdp_gitlab_registry_read_only_token,
                    staging_file,
                    int_file,
                    namespace), 'output': 'unnecessary'},
            {'cmd': 'kubectl get deployments -n %s -o name' % (namespace), 'output': 'deployments/package1\ndeployments/package2'},
            {'cmd': 'kubectl patch deployments package1 -p \'{"spec":{"template":{"spec":{"imagePullSecrets": [{"name": "cdp-%s"}]}}}}\' -n %s' % (TestCliDriver.ci_registry, namespace), 'output': 'unnecessary'},
            {'cmd': 'kubectl patch deployments package2 -p \'{"spec":{"template":{"spec":{"imagePullSecrets": [{"name": "cdp-%s"}]}}}}\' -n %s' % (TestCliDriver.ci_registry, namespace), 'output': 'unnecessary'},
            {'cmd': 'timeout 300 kubectl rollout status deployments/package1 -n %s' % namespace, 'output': 'unnecessary'},
            {'cmd': 'timeout 300 kubectl rollout status deployments/package2 -n %s' % namespace, 'output': 'unnecessary'}
        ]
        self.__run_CLIDriver({ 'k8s', '--use-gitlab-registry', '--namespace-project-branch-name', '--values=%s' % values }, verif_cmd, docker_host = docker_host)

    def test_k8s_usecustomregistry_namespaceprojectbranchname_values(self):
        # Create FakeCommand
        namespace = '%s-%s' % (TestCliDriver.ci_project_name, TestCliDriver.ci_commit_ref_name)
        namespace = namespace.replace('_', '-')
        staging_file = 'values.staging.yaml'
        int_file = 'values.int.yaml'
        values = ','.join([staging_file, int_file])
        verif_cmd = [
            {'cmd': 'cp /cdp/k8s/secret/cdp-secret.yaml charts/templates/', 'output': 'unnecessary'},
            {'cmd': 'helm upgrade %s charts --timeout 300 --set namespace=%s --set ingress.host=%s.%s.%s --set image.commit.sha=%s --set image.registry=%s --set image.repository=%s --set image.tag=%s --set image.credentials.username=%s --set image.credentials.password=%s --values charts/%s --values charts/%s --debug -i --namespace=%s'
                % (namespace,
                    namespace,
                    TestCliDriver.ci_commit_ref_name,
                    TestCliDriver.ci_project_name,
                    TestCliDriver.dns_subdomain,
                    TestCliDriver.ci_commit_sha[:8],
                    TestCliDriver.cdp_custom_registry,
                    TestCliDriver.ci_project_path.lower(),
                    TestCliDriver.ci_commit_ref_name,
                    TestCliDriver.cdp_custom_registry_user,
                    TestCliDriver.cdp_custom_registry_read_only_token,
                    staging_file,
                    int_file,
                    namespace), 'output': 'unnecessary'},
            {'cmd': 'kubectl get deployments -n %s -o name' % (namespace), 'output': 'deployments/package1\ndeployments/package2'},
            {'cmd': 'kubectl patch deployments package1 -p \'{"spec":{"template":{"spec":{"imagePullSecrets": [{"name": "cdp-%s"}]}}}}\' -n %s' % (TestCliDriver.cdp_custom_registry, namespace), 'output': 'unnecessary'},
            {'cmd': 'kubectl patch deployments package2 -p \'{"spec":{"template":{"spec":{"imagePullSecrets": [{"name": "cdp-%s"}]}}}}\' -n %s' % (TestCliDriver.cdp_custom_registry, namespace), 'output': 'unnecessary'},
            {'cmd': 'timeout 300 kubectl rollout status deployments/package1 -n %s' % namespace, 'output': 'unnecessary'},
            {'cmd': 'timeout 300 kubectl rollout status deployments/package2 -n %s' % namespace, 'output': 'unnecessary'}
        ]
        self.__run_CLIDriver({ 'k8s', '--use-custom-registry', '--namespace-project-branch-name', '--values=%s' % values }, verif_cmd)

    @freeze_time("2018-02-14 11:55:27")
    def test_k8s_verbose_imagetagsha1_useawsecr_namespaceprojectname_deployspecdir_timeout_values(self):
        # Create FakeCommand
        aws_host = 'ecr.amazonaws.com'
        login_cmd = 'docker login -u user -p pass https://%s' % aws_host
        namespace = TestCliDriver.ci_project_name
        timeout = 180
        deploy_spec_dir = 'deploy'
        values = 'values.staging.yaml'
        delete_minutes = 60
        date_format = '%Y-%m-%dT%H%M%S'

        verif_cmd = [
            {'cmd': 'aws ecr get-login --no-include-email --region eu-central-1', 'output': login_cmd, 'dry_run': False},
            {'cmd': 'env', 'output': 'unnecessary'},
            {'cmd': 'helm upgrade %s %s --timeout %s --set namespace=%s --set ingress.host=%s.%s --set image.commit.sha=%s --set image.registry=%s --set image.repository=%s --set image.tag=%s  --values %s/%s --debug -i --namespace=%s'
                % (TestCliDriver.ci_project_name,
                    deploy_spec_dir,
                    timeout,
                    namespace,
                    TestCliDriver.ci_project_name,
                    TestCliDriver.dns_subdomain,
                    TestCliDriver.ci_commit_sha[:8],
                    aws_host,
                    TestCliDriver.ci_project_path.lower(),
                    TestCliDriver.ci_commit_sha,
                    deploy_spec_dir,
                    values,
                    namespace), 'output': 'unnecessary'},
            {'cmd': 'kubectl label namespace %s deletable=true creationTimestamp=%s deletionTimestamp=%s --namespace=%s --overwrite'
                % (namespace,
                    datetime.datetime.now().strftime(date_format),
                    (datetime.datetime.now() + datetime.timedelta(minutes = delete_minutes)).strftime(date_format),
                    namespace), 'output': 'unnecessary'},
            {'cmd': 'kubectl get deployments -n %s -o name' % (namespace), 'output': 'deployments/package1'},
            {'cmd': 'timeout %s kubectl rollout status deployments/package1 -n %s' % (timeout, namespace), 'output': 'unnecessary'}
        ]
        self.__run_CLIDriver({ 'k8s', '--verbose', '--image-tag-sha1', '--use-aws-ecr', '--namespace-project-name', '--deploy-spec-dir=%s' % deploy_spec_dir, '--timeout=%s' % timeout, '--values=%s' % values, '--delete-labels=%s' % delete_minutes}, verif_cmd)

    @patch('cdpcli.clidriver.os.path.isdir', return_value=False)
    @patch('cdpcli.clidriver.os.path.isfile', return_value=False)
    @patch('cdpcli.clidriver.os.makedirs')
    @patch("__builtin__.open")
    @patch("cdpcli.clidriver.yaml.dump")
    def test_k8s_imagetagsha1_useawsecr_namespaceprojectname_sleep(self, mock_dump, mock_open, mock_makedirs, mock_isfile, mock_isdir):
        # Create FakeCommand
        aws_host = 'ecr.amazonaws.com'
        login_cmd = 'docker login -u user -p pass https://%s' % aws_host
        namespace = TestCliDriver.ci_project_name
        deploy_spec_dir = 'chart'
        sleep = 10
        verif_cmd = [
            {'cmd': 'aws ecr get-login --no-include-email --region eu-central-1', 'output': login_cmd, 'dry_run': False},
            {'cmd': 'cp -R /cdp/k8s/charts/* %s/' % deploy_spec_dir, 'output': 'unnecessary'},
            {'cmd': 'helm upgrade %s %s --timeout 300 --set namespace=%s --set ingress.host=%s.%s --set image.commit.sha=%s --set image.registry=%s --set image.repository=%s --set image.tag=%s   --debug -i --namespace=%s'
                % (TestCliDriver.ci_project_name,
                    deploy_spec_dir,
                    namespace,
                    TestCliDriver.ci_project_name,
                    TestCliDriver.dns_subdomain,
                    TestCliDriver.ci_commit_sha[:8],
                    aws_host,
                    TestCliDriver.ci_project_path.lower(),
                    TestCliDriver.ci_commit_sha,
                    namespace), 'output': 'unnecessary'},
            {'cmd': 'kubectl get deployments -n %s -o name' % (namespace), 'output': 'deployments/package1'},
            {'cmd': 'timeout 300 kubectl rollout status deployments/package1 -n %s' % (namespace), 'output': 'unnecessary'},
            {'cmd': 'sleep %s' % sleep, 'output': 'unnecessary'}
        ]
        self.__run_CLIDriver({ 'k8s', '--create-default-helm', '--image-tag-sha1', '--use-aws-ecr', '--namespace-project-name', '--deploy-spec-dir=%s' % deploy_spec_dir, '--sleep=%s' % sleep }, verif_cmd)

        mock_isdir.assert_called_with('%s/templates' % deploy_spec_dir)
        mock_isfile.assert_has_calls([call.isfile('%s/values.yaml' % deploy_spec_dir), call.isfile('%s/Chart.yaml' % deploy_spec_dir)])
        mock_makedirs.assert_called_with('%s/templates' % deploy_spec_dir)
        mock_open.assert_called_with('%s/Chart.yaml' % deploy_spec_dir, 'w')
        data = dict(
            apiVersion = 'v1',
            description = 'A Helm chart for Kubernetes',
            name = TestCliDriver.ci_project_name,
            version = '0.1.0'
        )
        mock_dump.assert_called_with(data, mock_open.return_value.__enter__.return_value, default_flow_style=False)

    def test_validator_dockerhost(self):
        docker_host = 'tcp://docker:2375'
        os.environ['DOCKER_HOST'] = docker_host

        verif_cmd = [
            {'cmd': 'validator-cli --url http://%s.%s.%s/configurations --schema BlockProviderConfig' % (TestCliDriver.ci_commit_ref_name, TestCliDriver.ci_project_name, TestCliDriver.dns_subdomain), 'output': 'unnecessary'}
        ]
        self.__run_CLIDriver({ 'validator' }, verif_cmd, docker_host = docker_host)

    def test_validator_verbose_path_namespaceprojectname_block(self):
        verif_cmd = [
            {'cmd': 'env', 'output': 'unnecessary'},
            {'cmd': 'validator-cli --url http://%s.%s/configurations --schema BlockConfig' % (TestCliDriver.ci_project_name, TestCliDriver.dns_subdomain), 'output': 'unnecessary'}
        ]
        self.__run_CLIDriver({ 'validator', '--verbose', '--namespace-project-name', '--block' }, verif_cmd)

    def test_validator_url_blockjson_sleep(self):
        url = 'http://test.com/configuration2'
        path = 'blockconfigurations'
        sleep = 10

        verif_cmd = [
            {'cmd': 'validator-cli --url http://%s.%s.%s/%s --schema BlockJSON' % (TestCliDriver.ci_commit_ref_name, TestCliDriver.ci_project_name, TestCliDriver.dns_subdomain, path), 'output': 'unnecessary'},
            {'cmd': 'sleep %s' % sleep, 'output': 'unnecessary'}
        ]
        self.__run_CLIDriver({ 'validator', '--path=%s' % path, '--block-json', '--sleep=%s' % sleep }, verif_cmd)

    def __run_CLIDriver(self, args, verif_cmd, return_code = None, docker_host = 'tcp://localhost:2375'):
        cmd = FakeCommand(verif_cmd = verif_cmd)
        cli = CLIDriver(cmd = cmd, opt = docopt(__doc__, args))
        self.assertEqual(return_code, cli.main())
        self.assertEqual(docker_host, os.environ['DOCKER_HOST'])
        cmd.verify_commands()
        del os.environ['DOCKER_HOST']
