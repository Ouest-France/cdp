#!/usr/bin/env python
import unittest
import os, sys
import mock

from cdpcli.clicommand import CLICommand
from cdpcli.clidriver import CLIDriver, __doc__
from docopt import docopt, DocoptExit

class FakeCommand(object):
    def __init__(self, verif_cmd):
        self._verif_cmd = verif_cmd
        self._index = 0
        self._tc = unittest.TestCase('__init__')

    def run_command(self, cmd, dry_run = None):
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
        self._index = self._index + 1
        return output

    def verify_commands(self):
        self._tc.assertEqual(len(self._verif_cmd), self._index)

class TestCliDriver(unittest.TestCase):

    registry_permanent_token = 'abcdefghijklmnopqrstuvwxyz'
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

    env_cdp_tag = 'CDP_TAG'
    env_cdp_registry = 'CDP_REGISTRY'

    @classmethod
    def setUpClass(cls):
        os.environ['REGISTRY_PERMANENT_TOKEN'] = TestCliDriver.registry_permanent_token
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

    def test_build(self):
        # Create FakeCommand
        image_name = 'maven:3.5-jdk-8'
        command_name = 'mvn clean install'
        verif_cmd = [
            {'cmd': 'docker pull %s' % (image_name), 'output': 'unnecessary'},
            {'cmd': 'docker run -v ${PWD}:/cdp-data %s /bin/sh -c \'cd /cdp-data; %s\'' % (image_name, command_name), 'output': 'unnecessary'}
        ]
        self.__run_CLIDriver({ 'build', '--docker-image=%s' % image_name, '--command=%s' % command_name }, verif_cmd)

    def test_build_simulatemergeon(self):
        # Create FakeCommand
        branch_name = 'master'
        image_name = 'maven:3.5-jdk-8'
        command_name = 'mvn clean install'
        verif_cmd = [
            {'cmd': 'git config --global user.email \"%s\"' % TestCliDriver.gitlab_user_email, 'output': 'unnecessary'},
            {'cmd': 'git config --global user.name \"%s\"' % TestCliDriver.gitlab_user_id, 'output': 'unnecessary'},
            {'cmd': 'git checkout %s' % branch_name, 'output': 'unnecessary'},
            {'cmd': 'git reset --hard origin/%s' % branch_name, 'output': 'unnecessary'},
            {'cmd': 'git merge %s --no-commit --no-ff' % TestCliDriver.ci_commit_sha, 'output': 'unnecessary'},
            {'cmd': 'docker pull %s' % (image_name), 'output': 'unnecessary'},
            {'cmd': 'docker run -v ${PWD}:/cdp-data %s /bin/sh -c \'cd /cdp-data; %s\'' % (image_name, command_name), 'output': 'unnecessary'},
            {'cmd': 'git checkout .', 'output': 'unnecessary'}
        ]
        self.__run_CLIDriver({ 'build', '--docker-image=%s' % image_name, '--command=%s' % command_name, '--simulate-merge-on=%s' % branch_name }, verif_cmd)

    def test_docker_usedocker_imagetagbranchname_usegitlabregistry(self):
        # Create FakeCommand
        verif_cmd = [
            {'cmd': 'docker login -u %s -p %s %s' % (TestCliDriver.ci_registry_user, TestCliDriver.ci_job_token, TestCliDriver.ci_registry), 'output': 'unnecessary'},
            {'cmd': 'docker build -t %s:%s .' % (TestCliDriver.ci_registry_image, TestCliDriver.ci_commit_ref_name), 'output': 'unnecessary'},
            {'cmd': 'docker push %s:%s' % (TestCliDriver.ci_registry_image, TestCliDriver.ci_commit_ref_name), 'output': 'unnecessary'}
        ]
        self.__run_CLIDriver({ 'docker', '--use-docker', '--use-gitlab-registry' }, verif_cmd)

    def test_docker_usedockercompose_imagetaglatest_imagetagsha1_useawsecr(self):
        # Create FakeCommand
        aws_host = 'ecr.amazonaws.com'
        login_cmd = 'docker login -u user -p pass https://%s' % aws_host
        verif_cmd = [
            {'cmd': 'aws ecr get-login --no-include-email --region eu-central-1', 'output': login_cmd, 'dry_run': False},
            {'cmd': login_cmd, 'output': 'unnecessary'},
            {'cmd': 'docker-compose build', 'output': 'unnecessary', 'env_vars' : { TestCliDriver.env_cdp_tag: 'latest', TestCliDriver.env_cdp_registry: '%s/%s' % (aws_host, TestCliDriver.ci_project_path.lower())}},
            {'cmd': 'docker-compose push', 'output': 'unnecessary', 'env_vars' : { TestCliDriver.env_cdp_tag: 'latest', TestCliDriver.env_cdp_registry: '%s/%s' % (aws_host, TestCliDriver.ci_project_path.lower())}},
            {'cmd': 'docker-compose build', 'output': 'unnecessary', 'env_vars' : { TestCliDriver.env_cdp_tag: TestCliDriver.ci_commit_sha, TestCliDriver.env_cdp_registry: '%s/%s' % (aws_host, TestCliDriver.ci_project_path.lower())}},
            {'cmd': 'docker-compose push', 'output': 'unnecessary', 'env_vars' : { TestCliDriver.env_cdp_tag: TestCliDriver.ci_commit_sha, TestCliDriver.env_cdp_registry: '%s/%s' % (aws_host, TestCliDriver.ci_project_path.lower())}}
        ]
        self.__run_CLIDriver({ 'docker', '--use-docker-compose', '--image-tag-latest', '--image-tag-sha1', '--use-aws-ecr' }, verif_cmd)

    def test_k8s_usegitlabregistry_namespaceprojectbranchname(self):
        # Create FakeCommand
        namespace = '%s-%s' % (TestCliDriver.ci_project_name, TestCliDriver.ci_commit_ref_name)
        namespace = namespace.replace('_', '-')
        verif_cmd = [
            {'cmd': 'cp /cdp/k8s/secret/cdp-secret.yaml charts/templates/', 'output': 'unnecessary'},
            {'cmd': 'helm upgrade %s charts --timeout 300 --set namespace=%s --set ingress.host=%s.%s.%s --set image.commit.sha=%s --set image.registry=%s --set image.repository=%s --set image.tag=%s --set image.credentials.username=%s --set image.credentials.password=%s --debug -i --namespace=%s'
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
                    TestCliDriver.registry_permanent_token,
                    namespace), 'output': 'unnecessary'},
            {'cmd': 'kubectl get deployments -n %s -o name' % (namespace), 'output': 'deployments/package1\ndeployments/package2'},
            {'cmd': 'kubectl patch deployments package1 -p \'{"spec":{"template":{"spec":{"imagePullSecrets": [{"name": "cdp-%s"}]}}}}\' -n %s' % (TestCliDriver.ci_registry, namespace), 'output': 'unnecessary'},
            {'cmd': 'kubectl patch deployments package2 -p \'{"spec":{"template":{"spec":{"imagePullSecrets": [{"name": "cdp-%s"}]}}}}\' -n %s' % (TestCliDriver.ci_registry, namespace), 'output': 'unnecessary'},
            {'cmd': 'timeout 300 kubectl rollout status deployments/package1 -n %s' % namespace, 'output': 'unnecessary'},
            {'cmd': 'timeout 300 kubectl rollout status deployments/package2 -n %s' % namespace, 'output': 'unnecessary'}
        ]
        self.__run_CLIDriver({ 'k8s', '--use-gitlab-registry', '--namespace-project-branch-name' }, verif_cmd)

    def test_k8s_imagetagsha1_useawsecr_namespaceprojectname_deployspecdir_timeout(self):
        # Create FakeCommand
        aws_host = 'ecr.amazonaws.com'
        login_cmd = 'docker login -u user -p pass https://%s' % aws_host
        namespace = TestCliDriver.ci_project_name
        timeout = 180
        deploy_spec_dir = 'deploy'

        verif_cmd = [
            {'cmd': 'aws ecr get-login --no-include-email --region eu-central-1', 'output': login_cmd, 'dry_run': False},
            {'cmd': 'helm upgrade %s %s --timeout %s --set namespace=%s --set ingress.host=%s.%s --set image.commit.sha=%s --set image.registry=%s --set image.repository=%s --set image.tag=%s  --debug -i --namespace=%s'
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
                    namespace), 'output': 'unnecessary'},
            {'cmd': 'kubectl get deployments -n %s -o name' % (namespace), 'output': 'deployments/package1'},
            {'cmd': 'timeout %s kubectl rollout status deployments/package1 -n %s' % (timeout, namespace), 'output': 'unnecessary'}
        ]
        self.__run_CLIDriver({ 'k8s', '--image-tag-sha1', '--use-aws-ecr', '--namespace-project-name', '--deploy-spec-dir=%s' % deploy_spec_dir, '--timeout=%s' % timeout}, verif_cmd)

    @mock.patch('cdpcli.clidriver.os.path.isdir', return_value=False)
    @mock.patch('cdpcli.clidriver.os.makedirs')
    @mock.patch("__builtin__.open")
    @mock.patch("cdpcli.clidriver.yaml.dump")
    def test_k8s_imagetagsha1_useawsecr_namespaceprojectname(self, mock_dump, mock_open, mock_makedirs, mock_isdir):
        # Create FakeCommand
        aws_host = 'ecr.amazonaws.com'
        login_cmd = 'docker login -u user -p pass https://%s' % aws_host
        namespace = TestCliDriver.ci_project_name
        deploy_spec_dir = 'chart'

        verif_cmd = [
            {'cmd': 'aws ecr get-login --no-include-email --region eu-central-1', 'output': login_cmd, 'dry_run': False},
            {'cmd': 'cp -R /cdp/k8s/charts/* %s/' % deploy_spec_dir, 'output': 'unnecessary'},
            {'cmd': 'helm upgrade %s %s --timeout 300 --set namespace=%s --set ingress.host=%s.%s --set image.commit.sha=%s --set image.registry=%s --set image.repository=%s --set image.tag=%s  --debug -i --namespace=%s'
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
            {'cmd': 'timeout 300 kubectl rollout status deployments/package1 -n %s' % (namespace), 'output': 'unnecessary'}
        ]
        self.__run_CLIDriver({ 'k8s', '--create-default-helm', '--image-tag-sha1', '--use-aws-ecr', '--namespace-project-name', '--deploy-spec-dir=%s' % deploy_spec_dir }, verif_cmd)

        mock_isdir.assert_called_with(deploy_spec_dir)
        mock_makedirs.assert_called_with('%s/templates' % deploy_spec_dir)
        mock_open.assert_called_with('%s/Chart.yaml' % deploy_spec_dir, 'w')
        data = dict(
            apiVersion = 'v1',
            description = 'A Helm chart for Kubernetes',
            name = TestCliDriver.ci_project_name,
            version = '0.1.0'
        )
        mock_dump.assert_called_with(data, mock_open.return_value.__enter__.return_value, default_flow_style=False)

    def test_validator(self):
        verif_cmd = [
            {'cmd': 'validator-cli --url http://%s.%s.%s/configurations --schema BlockProviderConfig' % (TestCliDriver.ci_commit_ref_name, TestCliDriver.ci_project_name, TestCliDriver.dns_subdomain), 'output': 'unnecessary'}
        ]
        self.__run_CLIDriver({ 'validator' }, verif_cmd)

    def test_validator_namespaceprojectname_block(self):
        verif_cmd = [
            {'cmd': 'validator-cli --url http://%s.%s/configurations --schema BlockConfig' % (TestCliDriver.ci_project_name, TestCliDriver.dns_subdomain), 'output': 'unnecessary'}
        ]
        self.__run_CLIDriver({ 'validator', '--namespace-project-name', '--block' }, verif_cmd)

    def test_validator_url_blockjson(self):
        url = 'http://test.com/configuration2'
        verif_cmd = [
            {'cmd': 'validator-cli --url %s --schema BlockJSON' % (url), 'output': 'unnecessary'}
        ]
        self.__run_CLIDriver({ 'validator', '--url=%s' % url, '--block-json' }, verif_cmd)


    def test_sleep(self):
        # Create FakeCommand
        verif_cmd = [
            {'cmd': 'sleep 600', 'output': 'unnecessary'}
        ]
        self.__run_CLIDriver({ 'sleep' }, verif_cmd)

    def test_sleep_seconds(self):
        # Create FakeCommand
        seconds = 300
        verif_cmd = [
            {'cmd': 'sleep %s' % seconds, 'output': 'unnecessary'}
        ]
        self.__run_CLIDriver({ 'sleep', '--seconds=%s' % seconds }, verif_cmd)


    def __run_CLIDriver(self, args, verif_cmd, return_code = None):
        cmd = FakeCommand(verif_cmd = verif_cmd)
        cli = CLIDriver(cmd = cmd, opt = docopt(__doc__, args))
        self.assertEqual(return_code, cli.main())
        cmd.verify_commands()
