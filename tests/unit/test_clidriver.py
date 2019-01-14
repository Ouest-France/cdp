#!/usr/bin/env python2.7

import unittest
import os, sys, re
import datetime

from cdpcli.clicommand import CLICommand
from cdpcli.clidriver import CLIDriver, __doc__
from docopt import docopt, DocoptExit
from freezegun import freeze_time
from mock import call, patch, Mock

class FakeCommand(object):
    def __init__(self, verif_cmd):
        self._verif_cmd = verif_cmd
        self._index = 0
        self._tc = unittest.TestCase('__init__')

    def run_command(self, cmd, dry_run = None, timeout = None):
        return self.run(cmd, dry_run, timeout)

    def run(self, cmd, dry_run = None, timeout = None):
        print cmd
        try:

            try:
                with_entrypoint_assert = self._verif_cmd[self._index]['with_entrypoint']
            except KeyError:
                with_entrypoint_assert = True

            try:
                volume_from_assert = self._verif_cmd[self._index]['volume_from']
            except KeyError:
                volume_from_assert = None

            try:
                cmd_assert = self.__get_rundocker_cmd(self._verif_cmd[self._index]['docker_image'], self._verif_cmd[self._index]['cmd'], volume_from = volume_from_assert, with_entrypoint = with_entrypoint_assert)
            except KeyError:
                cmd_assert = self._verif_cmd[self._index]['cmd']

            # Check cmd parameter
            self._tc.assertEqual(cmd_assert, cmd)

            # Check dry-run parameter
            try:
                self._tc.assertEqual(self._verif_cmd[self._index]['dry_run'], dry_run)
            except KeyError:
                self._tc.assertTrue(dry_run is None)

            # Check timeout parameter
            try:
                self._tc.assertEqual(self._verif_cmd[self._index]['timeout'], timeout)
            except KeyError:
                self._tc.assertTrue(timeout is None)

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



    def __get_rundocker_cmd(self, docker_image, prg_cmd, volume_from = None, with_entrypoint = True):

        run_docker_cmd = 'docker run --rm -e DOCKER_HOST'

        for env in os.environ:
            if env.startswith('CI') or env.startswith('CDP') or env.startswith('AWS') or env.startswith('GIT') or env.startswith('KUBERNETES'):
                run_docker_cmd = '%s -e %s' % (run_docker_cmd, env)

        run_docker_cmd = '%s -v /var/run/docker.sock:/var/run/docker.sock' % run_docker_cmd

        if volume_from == 'k8s':
            run_docker_cmd = '%s --volumes-from $(docker ps -aqf "name=k8s_build_${HOSTNAME}")' % (run_docker_cmd)
        elif volume_from == 'docker':
            run_docker_cmd = '%s --volumes-from $(docker ps -aqf "name=${HOSTNAME}-build")' % (run_docker_cmd)


        run_docker_cmd = '%s -w ${PWD}' % (run_docker_cmd)
        run_docker_cmd = '%s %s' % (run_docker_cmd, docker_image)

        if (with_entrypoint):
            run_docker_cmd = '%s %s' % (run_docker_cmd, prg_cmd)
        else:
            run_docker_cmd = '%s /bin/sh -c \'%s\'' % (run_docker_cmd, prg_cmd)

        return run_docker_cmd

class TestCliDriver(unittest.TestCase):

    ci_job_token = 'gitlab-ci'
    ci_commit_sha = '0123456789abcdef0123456789abcdef01234567'
    ci_registry_user = 'gitlab-ci'
    ci_registry = 'registry.gitlab.com'
    ci_repository_url = 'https://gitlab-ci-token:iejdzkjziuiez7786@gitlab.com/HelloWorld/HelloWorld/helloworld.git'
    ci_commit_ref_name = 'branch_helloworld_with_many.characters_because_helm_k8s_because_the_length_must_not_longer_than.53'
    ci_commit_ref_slug = 'branch_helloworld_with_many-characters_because_helm_k8s_because_the_length_must_not_longer_than_53'
    ci_registry_image = 'registry.gitlab.com/helloworld/helloworld'
    ci_project_id = '14'
    ci_project_name = 'hello-world'
    ci_project_name_fisrt_letter = ''.join([word if len(word) == 0 else word[0] for word in re.split('[^a-zA-Z\d]', ci_project_name)])
    ci_project_path = 'HelloWorld/HelloWorld'
    ci_project_path_slug = 'helloworld-helloworld'
    ci_deploy_user = 'gitlab+deploy-token-1'
    ci_deploy_password = 'ak5zALsZd8g5KvFRxMyD'
    cdp_dns_subdomain = 'example.com'
    cdp_dns_subdomain_staging = 'staging.example.com'
    gitlab_token = 'azlemksiu76dza'
    gitlab_user_email = 'test@example.com'
    gitlab_user_name = 'Hello WORLD'
    gitlab_user_token = '897873763'
    cdp_custom_registry_user = 'cdp_custom_registry_user'
    cdp_custom_registry_token = '1298937676109092092'
    cdp_custom_registry_read_only_token = '1298937676109092093'
    cdp_custom_registry = 'docker-artifact.fr:8123'
    cdp_artifactory_path = 'http://repo.fr/test'
    cdp_artifactory_token = '29873678036783'
    cdp_repository_url = 'http://repo.fr'
    cdp_repository_maven_snapshot = 'libs-snapshot-local'
    cdp_repository_maven_release = 'libs-release-local'
    cdp_sonar_url = "https://sonar:9000"
    cdp_sonar_login = "987656436908"
    cdp_gitlab_api_url = 'https://www.gitlab.com'
    cdp_gitlab_api_token = 'azlemksiu84dza'
    cdp_bp_validator_host = 'https://validator-server.com'
    image_name_git = 'ouestfrance/cdp-git:2.15.0'
    image_name_sonar_scanner = 'ouestfrance/cdp-sonar-scanner:3.1.0'
    image_name_aws = 'ouestfrance/cdp-aws:1.15.19'
    image_name_kubectl = 'ouestfrance/cdp-kubectl:1.9.9'
    image_name_helm = 'ouestfrance/cdp-helm:2.9.1-1.9.9'

    env_cdp_tag = 'CDP_TAG'
    env_cdp_registry = 'CDP_REGISTRY'

    deployment_json_without_secret = """{
      "apiVersion": "extensions/v1beta1",
      "kind": "Deployment",
      "metadata": {
      },
      "spec": {
          "revisionHistoryLimit": 1,
          "template": {
              "spec": {
              }
          }
      },
      "status": {
          "availableReplicas": 3,
          "conditions": [
              {
                  "lastTransitionTime": "2018-09-26T11:33:39Z",
                  "lastUpdateTime": "2018-09-26T11:33:39Z",
                  "message": "Deployment has minimum availability.",
                  "reason": "MinimumReplicasAvailable",
                  "status": "True",
                  "type": "Available"
              }
          ],
          "observedGeneration": 2,
          "readyReplicas": 3,
          "replicas": 3,
          "updatedReplicas": 3
      }
  }"""

    deployment_json_with_secret = """{
      "apiVersion": "extensions/v1beta1",
      "kind": "Deployment",
      "metadata": {
      },
      "spec": {
          "revisionHistoryLimit": 1,
          "template": {
              "spec": {
                  "imagePullSecrets": [
                      {
                          "name": "cdp-registry.gitlab.com"
                      },
                      {
                          "name": "custom"
                      }
                  ]
              }
          }
      },
      "status": {
          "availableReplicas": 3,
          "conditions": [
              {
                  "lastTransitionTime": "2018-09-26T11:33:39Z",
                  "lastUpdateTime": "2018-09-26T11:33:39Z",
                  "message": "Deployment has minimum availability.",
                  "reason": "MinimumReplicasAvailable",
                  "status": "True",
                  "type": "Available"
              }
          ],
          "observedGeneration": 2,
          "readyReplicas": 3,
          "replicas": 3,
          "updatedReplicas": 3
      }
  }"""

    @classmethod
    def setUpClass(cls):
        os.environ['CI_JOB_TOKEN'] = TestCliDriver.ci_job_token
        os.environ['CI_COMMIT_SHA'] = TestCliDriver.ci_commit_sha
        os.environ['CI_REGISTRY_USER'] = TestCliDriver.ci_registry_user
        os.environ['CI_REGISTRY'] = TestCliDriver.ci_registry
        os.environ['CI_REPOSITORY_URL'] = TestCliDriver.ci_repository_url
        os.environ['CI_COMMIT_REF_NAME'] = TestCliDriver.ci_commit_ref_name
        os.environ['CI_COMMIT_REF_SLUG'] = TestCliDriver.ci_commit_ref_slug
        os.environ['CI_REGISTRY_IMAGE'] = TestCliDriver.ci_registry_image
        os.environ['CI_PROJECT_ID'] = TestCliDriver.ci_project_id
        os.environ['CI_PROJECT_NAME'] = TestCliDriver.ci_project_name
        os.environ['CI_PROJECT_PATH'] = TestCliDriver.ci_project_path
        os.environ['CI_PROJECT_PATH_SLUG'] = TestCliDriver.ci_project_path_slug
        os.environ['CI_DEPLOY_USER'] = TestCliDriver.ci_deploy_user
        os.environ['CI_DEPLOY_PASSWORD'] = TestCliDriver.ci_deploy_password
        os.environ['CDP_DNS_SUBDOMAIN_DEFAULT'] = TestCliDriver.cdp_dns_subdomain
        os.environ['CDP_DNS_SUBDOMAIN_PROD'] = TestCliDriver.cdp_dns_subdomain
        os.environ['CDP_DNS_SUBDOMAIN_STAGING'] = TestCliDriver.cdp_dns_subdomain_staging
        os.environ['GITLAB_TOKEN'] = TestCliDriver.gitlab_token
        os.environ['GITLAB_USER_EMAIL'] = TestCliDriver.gitlab_user_email
        os.environ['GITLAB_USER_NAME'] = TestCliDriver.gitlab_user_name
        os.environ['GITLAB_USER_TOKEN'] = TestCliDriver.gitlab_user_token
        os.environ['CDP_CUSTOM_REGISTRY_USER'] = TestCliDriver.cdp_custom_registry_user
        os.environ['CDP_CUSTOM_REGISTRY_TOKEN'] = TestCliDriver.cdp_custom_registry_token
        os.environ['CDP_CUSTOM_REGISTRY_READ_ONLY_TOKEN'] = TestCliDriver.cdp_custom_registry_read_only_token
        os.environ['CDP_CUSTOM_REGISTRY'] = TestCliDriver.cdp_custom_registry
        os.environ['CDP_ARTIFACTORY_PATH'] = TestCliDriver.cdp_artifactory_path
        os.environ['CDP_ARTIFACTORY_TOKEN'] = TestCliDriver.cdp_artifactory_token
        os.environ['CDP_REPOSITORY_URL'] = TestCliDriver.cdp_repository_url
        os.environ['CDP_REPOSITORY_MAVEN_SNAPSHOT'] = TestCliDriver.cdp_repository_maven_snapshot
        os.environ['CDP_REPOSITORY_MAVEN_RELEASE'] = TestCliDriver.cdp_repository_maven_release
        os.environ['CDP_SONAR_URL'] = TestCliDriver.cdp_sonar_url
        os.environ['CDP_SONAR_LOGIN'] = TestCliDriver.cdp_sonar_login
        os.environ['CDP_GITLAB_API_URL'] = TestCliDriver.cdp_gitlab_api_url
        os.environ['CDP_GITLAB_API_TOKEN'] = TestCliDriver.cdp_gitlab_api_token
        os.environ['CDP_BP_VALIDATOR_HOST'] = TestCliDriver.cdp_bp_validator_host




    def test_build_verbose_simulatemergeon_sleep(self):
        # Create FakeCommand
        branch_name = 'master'
        image_name = 'maven:3.5-jdk-8'
        command_name = 'mvn clean install'
        sleep = 10
        verif_cmd = [
            {'cmd': 'env', 'dry_run': False, 'output': 'unnecessary'},
            {'cmd': 'docker pull %s' % TestCliDriver.image_name_git, 'output': 'unnecessary'},
            {'cmd': 'config user.email \"%s\"' % TestCliDriver.gitlab_user_email, 'volume_from' : 'k8s', 'output': 'unnecessary', 'docker_image': TestCliDriver.image_name_git},
            {'cmd': 'config user.name \"%s\"' % TestCliDriver.gitlab_user_name, 'volume_from' : 'k8s', 'output': 'unnecessary', 'docker_image': TestCliDriver.image_name_git},
            {'cmd': 'checkout %s' % branch_name, 'volume_from' : 'k8s', 'output': 'unnecessary', 'docker_image': TestCliDriver.image_name_git},
            {'cmd': 'reset --hard origin/%s' % branch_name, 'volume_from' : 'k8s', 'output': 'unnecessary', 'docker_image': TestCliDriver.image_name_git},
            {'cmd': 'merge %s --no-commit --no-ff' % TestCliDriver.ci_commit_sha, 'volume_from' : 'k8s', 'output': 'unnecessary', 'docker_image': TestCliDriver.image_name_git},
            {'cmd': 'docker pull %s' % (image_name), 'output': 'unnecessary'},
            {'cmd': command_name, 'volume_from' : 'k8s', 'with_entrypoint' : False, 'output': 'unnecessary', 'docker_image': image_name},
            {'cmd': 'sleep %s' % sleep, 'output': 'unnecessary'}
        ]
        self.__run_CLIDriver({ 'build', '--verbose', '--docker-image=%s' % image_name, '--command=%s' % command_name, '--simulate-merge-on=%s' % branch_name, '--sleep=%s' % sleep }, verif_cmd)

    def test_build_volumefromdocker(self):
        # Create FakeCommand
        branch_name = 'master'
        image_name = 'maven:3.5-jdk-8'
        command_name = 'mvn clean install'
        verif_cmd = [
            {'cmd': 'docker pull %s' % (image_name), 'output': 'unnecessary'},
            {'cmd': command_name, 'volume_from' : 'docker', 'with_entrypoint' : False, 'output': 'unnecessary', 'docker_image': image_name}
        ]
        self.__run_CLIDriver({ 'build', '--docker-image=%s' % image_name, '--command=%s' % command_name, '--volume-from=docker' }, verif_cmd)

    def test_maven_goals_verbose_simulatemergeon_sleep(self):
        # Create FakeCommand
        branch_name = 'master'
        image_name_maven = 'maven:3.5-jdk-8'
        goals = 'clean install -DskipTests'
        sleep = 10
        verif_cmd = [
            {'cmd': 'env', 'dry_run': False, 'output': 'unnecessary'},
            {'cmd': 'docker pull %s' % TestCliDriver.image_name_git, 'output': 'unnecessary'},
            {'cmd': 'config user.email \"%s\"' % TestCliDriver.gitlab_user_email, 'volume_from' : 'k8s', 'output': 'unnecessary', 'docker_image': TestCliDriver.image_name_git},
            {'cmd': 'config user.name \"%s\"' % TestCliDriver.gitlab_user_name, 'volume_from' : 'k8s', 'output': 'unnecessary', 'docker_image': TestCliDriver.image_name_git},
            {'cmd': 'checkout %s' % branch_name, 'volume_from' : 'k8s', 'output': 'unnecessary', 'docker_image': TestCliDriver.image_name_git},
            {'cmd': 'reset --hard origin/%s' % branch_name, 'volume_from' : 'k8s', 'output': 'unnecessary', 'docker_image': TestCliDriver.image_name_git},
            {'cmd': 'merge %s --no-commit --no-ff' % TestCliDriver.ci_commit_sha, 'volume_from' : 'k8s', 'output': 'unnecessary', 'docker_image': TestCliDriver.image_name_git},
            {'cmd': 'cp /cdp/maven/settings.xml maven-settings.xml', 'output': 'unnecessary'},
            {'cmd': 'docker pull %s' % (image_name_maven), 'output': 'unnecessary'},
            {'cmd': 'mvn %s -s maven-settings.xml' % goals, 'volume_from' : 'k8s', 'with_entrypoint' : False, 'output': 'unnecessary', 'docker_image': '%s' % image_name_maven},
            {'cmd': 'sleep %s' % sleep, 'output': 'unnecessary'}
        ]
        self.__run_CLIDriver({ 'maven', '--verbose', '--docker-image-maven=%s' % image_name_maven, '--goals=%s' % goals, '--simulate-merge-on=%s' % branch_name, '--sleep=%s' % sleep }, verif_cmd)


    def test_maven_deployrelease_mavenopts(self):
        # Create FakeCommand
        branch_name = 'master'
        image_name_maven = 'maven:3.5-jdk-8'
        goals = 'clean install -DskipTests'
        maven_opts = '-Djava.awt.headless=true -Dmaven.repo.local=./.m2/repository -e'
        verif_cmd = [
            {'cmd': 'docker pull %s' % TestCliDriver.image_name_git, 'output': 'unnecessary'},
            {'cmd': 'config user.email \"%s\"' % TestCliDriver.gitlab_user_email, 'volume_from' : 'k8s', 'output': 'unnecessary', 'docker_image': TestCliDriver.image_name_git},
            {'cmd': 'config user.name \"%s\"' % TestCliDriver.gitlab_user_name, 'volume_from' : 'k8s', 'output': 'unnecessary', 'docker_image': TestCliDriver.image_name_git},
            {'cmd': 'checkout %s' % TestCliDriver.ci_commit_ref_name, 'volume_from' : 'k8s', 'output': 'unnecessary', 'docker_image': TestCliDriver.image_name_git},
            {'cmd': 'cp /cdp/maven/settings.xml maven-settings.xml', 'output': 'unnecessary'},
            {'cmd': 'docker pull %s' % (image_name_maven), 'output': 'unnecessary'},
            {'cmd': 'mvn --batch-mode org.apache.maven.plugins:maven-release-plugin:2.5.3:prepare org.apache.maven.plugins:maven-release-plugin:2.5.3:perform -Dresume=false -DautoVersionSubmodules=true -DdryRun=false -DscmCommentPrefix="[ci skip]" -Dproject.scm.id=git -DreleaseProfiles=release -Darguments="-DskipTests -DskipITs -Dproject.scm.id=git -DaltDeploymentRepository=release::default::%s/%s %s" %s -s maven-settings.xml' % (TestCliDriver.cdp_repository_url, TestCliDriver.cdp_repository_maven_release, maven_opts, maven_opts), 'volume_from' : 'k8s', 'with_entrypoint' : False, 'output': 'unnecessary', 'docker_image': '%s' % image_name_maven}
        ]

        self.__run_CLIDriver({ 'maven', '--docker-image-maven=%s' % image_name_maven, '--deploy=release'},
            verif_cmd, env_vars = {'MAVEN_OPTS': maven_opts})


    def test_maven_deployrelease_mavenreleaseversion(self):
        # Create FakeCommand
        branch_name = 'master'
        image_version = '3.5-jdk-8'
        maven_release_version = '1.0.0'
        goals = 'clean install -DskipTests'
        verif_cmd = [
            {'cmd': 'docker pull %s' % TestCliDriver.image_name_git, 'output': 'unnecessary'},
            {'cmd': 'config user.email \"%s\"' % TestCliDriver.gitlab_user_email, 'volume_from' : 'k8s', 'output': 'unnecessary', 'docker_image': TestCliDriver.image_name_git},
            {'cmd': 'config user.name \"%s\"' % TestCliDriver.gitlab_user_name, 'volume_from' : 'k8s', 'output': 'unnecessary', 'docker_image': TestCliDriver.image_name_git},
            {'cmd': 'checkout %s' % TestCliDriver.ci_commit_ref_name, 'volume_from' : 'k8s', 'output': 'unnecessary', 'docker_image': TestCliDriver.image_name_git},
            {'cmd': 'cp /cdp/maven/settings.xml maven-settings.xml', 'output': 'unnecessary'},
            {'cmd': 'docker pull maven:%s' % (image_version), 'output': 'unnecessary'},
            {'cmd': 'mvn --batch-mode org.apache.maven.plugins:maven-release-plugin:%s:prepare org.apache.maven.plugins:maven-release-plugin:%s:perform -Dresume=false -DautoVersionSubmodules=true -DdryRun=false -DscmCommentPrefix="[ci skip]" -Dproject.scm.id=git -DreleaseProfiles=release -Darguments="-DskipTests -DskipITs -Dproject.scm.id=git -DaltDeploymentRepository=release::default::%s/%s" -s maven-settings.xml' % (maven_release_version, maven_release_version, TestCliDriver.cdp_repository_url, TestCliDriver.cdp_repository_maven_release), 'volume_from' : 'k8s', 'with_entrypoint' : False, 'output': 'unnecessary', 'docker_image': 'maven:%s' % image_version}
        ]

        self.__run_CLIDriver({ 'maven', '--docker-version=%s' % image_version, '--deploy=release', '--maven-release-plugin=%s' % maven_release_version}, verif_cmd)

    def test_maven_deploysnapshot(self):
        # Create FakeCommand
        branch_name = 'master'
        image_version = '3.5-jdk-8'
        goals = 'clean install -DskipTests'
        verif_cmd = [
            {'cmd': 'cp /cdp/maven/settings.xml maven-settings.xml', 'output': 'unnecessary'},
            {'cmd': 'docker pull maven:%s' % (image_version), 'output': 'unnecessary'},
            {'cmd': 'mvn deploy -DskipTests -DskipITs -DaltDeploymentRepository=snapshot::default::%s/%s -s maven-settings.xml' % (TestCliDriver.cdp_repository_url, TestCliDriver.cdp_repository_maven_snapshot), 'volume_from' : 'k8s', 'with_entrypoint' : False, 'output': 'unnecessary', 'docker_image' : 'maven:%s' % image_version}
        ]

        self.__run_CLIDriver({ 'maven', '--docker-version=%s' % image_version, '--deploy=snapshot' }, verif_cmd)

    @patch('cdpcli.clidriver.os.path.isfile', return_value=False)
    def test_sonar_preview_codeclimate_verbose_simulatemergeon_sleep(self, mock_isfile):
        # Create FakeCommand
        branch_name = 'master'
        sleep = 10
        verif_cmd = [
            {'cmd': 'env', 'dry_run': False, 'output': 'unnecessary'},
            {'cmd': 'docker pull %s' % TestCliDriver.image_name_git, 'output': 'unnecessary'},
            {'cmd': 'config user.email \"%s\"' % TestCliDriver.gitlab_user_email, 'volume_from' : 'k8s', 'output': 'unnecessary', 'docker_image': TestCliDriver.image_name_git},
            {'cmd': 'config user.name \"%s\"' % TestCliDriver.gitlab_user_name, 'volume_from' : 'k8s', 'output': 'unnecessary', 'docker_image': TestCliDriver.image_name_git},
            {'cmd': 'checkout %s' % branch_name, 'volume_from' : 'k8s', 'output': 'unnecessary', 'docker_image': TestCliDriver.image_name_git},
            {'cmd': 'reset --hard origin/%s' % branch_name, 'volume_from' : 'k8s', 'output': 'unnecessary', 'docker_image': TestCliDriver.image_name_git},
            {'cmd': 'merge %s --no-commit --no-ff' % TestCliDriver.ci_commit_sha, 'volume_from' : 'k8s', 'output': 'unnecessary', 'docker_image': TestCliDriver.image_name_git},
            {'cmd': 'docker pull %s' % TestCliDriver.image_name_sonar_scanner, 'output': 'unnecessary'},
            {'cmd': '-Dsonar.login=%s -Dsonar.host.url=%s -Dsonar.gitlab.user_token=%s -Dsonar.gitlab.commit_sha=%s -Dsonar.gitlab.ref_name=%s -Dsonar.gitlab.project_id=%s -Dsonar.branch.name=%s -Dsonar.projectKey=%s -Dsonar.sources=. -Dsonar.gitlab.json_mode=CODECLIMATE -Dsonar.analysis.mode=preview'
                % (TestCliDriver.cdp_sonar_login,
                    TestCliDriver.cdp_sonar_url,
                    TestCliDriver.gitlab_user_token,
                    TestCliDriver.ci_commit_sha,
                    TestCliDriver.ci_commit_ref_name,
                    TestCliDriver.ci_project_path_slug,
                    TestCliDriver.ci_commit_ref_name,
                    TestCliDriver.ci_project_path_slug), 'volume_from' : 'k8s', 'output': 'unnecessary', 'docker_image': TestCliDriver.image_name_sonar_scanner},
            {'cmd': 'sleep %s' % sleep, 'output': 'unnecessary'}
        ]
        self.__run_CLIDriver({ 'sonar', '--preview', '--codeclimate', '--verbose', '--simulate-merge-on=%s' % branch_name, '--sleep=%s' % sleep }, verif_cmd)
        mock_isfile.assert_called_with('sonar-project.properties')

    @patch('cdpcli.clidriver.os.path.isfile', return_value=True)
    @patch('cdpcli.clidriver.PropertiesParser.get')
    def test_sonar_publish_sast(self, mock_get, mock_isfile):
        mock_get.side_effect = ['project_key', 'sources']
        # Create FakeCommand
        verif_cmd = [
            {'cmd': 'docker pull %s' % TestCliDriver.image_name_sonar_scanner, 'output': 'unnecessary'},
            {'cmd': '-Dsonar.login=%s -Dsonar.host.url=%s -Dsonar.gitlab.user_token=%s -Dsonar.gitlab.commit_sha=%s -Dsonar.gitlab.ref_name=%s -Dsonar.gitlab.project_id=%s -Dsonar.branch.name=%s -Dsonar.gitlab.json_mode=SAST'
                % (TestCliDriver.cdp_sonar_login,
                    TestCliDriver.cdp_sonar_url,
                    TestCliDriver.gitlab_user_token,
                    TestCliDriver.ci_commit_sha,
                    TestCliDriver.ci_commit_ref_name,
                    TestCliDriver.ci_project_path_slug,
                    TestCliDriver.ci_commit_ref_name), 'volume_from' : 'k8s', 'output': 'unnecessary', 'docker_image': TestCliDriver.image_name_sonar_scanner}
        ]
        self.__run_CLIDriver({ 'sonar', '--publish', '--sast' }, verif_cmd)
        mock_isfile.assert_called_with('sonar-project.properties')
        mock_get.assert_has_calls([call.get('sonar.projectKey'), call.get('sonar.sources')])

    def test_docker_usedocker_imagetagbranchname_usegitlabregistry_sleep_docker_host(self):
        # Create FakeCommand
        sleep = 10

        docker_host = 'unix:///var/run/docker.sock'

        verif_cmd = [
            {'cmd': 'docker login -u %s -p %s https://%s' % (TestCliDriver.ci_registry_user, TestCliDriver.ci_job_token, TestCliDriver.ci_registry), 'output': 'unnecessary'},
            {'cmd': 'docker login -u %s -p %s https://%s' % (TestCliDriver.cdp_custom_registry_user, TestCliDriver.cdp_custom_registry_token, TestCliDriver.cdp_custom_registry), 'output': 'unnecessary'},
            {'cmd': 'docker build -t %s:%s .' % (TestCliDriver.ci_registry_image, TestCliDriver.ci_commit_ref_name), 'output': 'unnecessary'},
            {'cmd': 'docker push %s:%s' % (TestCliDriver.ci_registry_image, TestCliDriver.ci_commit_ref_name), 'output': 'unnecessary'},
            {'cmd': 'sleep %s' % sleep, 'output': 'unnecessary'}
        ]
        self.__run_CLIDriver({ 'docker', '--use-docker', '--use-gitlab-registry', '--sleep=%s' % sleep },
            verif_cmd, docker_host = docker_host, env_vars = {'DOCKER_HOST': docker_host})

    def test_docker_usedocker_imagetagsha1_usecustomregistry(self):
        # Create FakeCommand
        verif_cmd = [
            {'cmd': 'docker login -u %s -p %s https://%s' % (TestCliDriver.cdp_custom_registry_user, TestCliDriver.cdp_custom_registry_token, TestCliDriver.cdp_custom_registry), 'output': 'unnecessary'},
            {'cmd': 'docker build -t %s/%s:%s .' % (TestCliDriver.cdp_custom_registry, TestCliDriver.ci_project_path.lower(), TestCliDriver.ci_commit_sha), 'output': 'unnecessary'},
            {'cmd': 'docker push %s/%s:%s' % (TestCliDriver.cdp_custom_registry, TestCliDriver.ci_project_path.lower(), TestCliDriver.ci_commit_sha), 'output': 'unnecessary'}
        ]
        self.__run_CLIDriver({ 'docker', '--use-docker', '--use-custom-registry', '--image-tag-sha1' }, verif_cmd)


    def test_docker_imagetagsha1_useawsecr(self):
        # Create FakeCommand
        aws_host = 'ecr.amazonaws.com'
        login_cmd = 'docker login -u user -p pass https://%s' % aws_host
        verif_cmd = [
            {'cmd': 'docker pull %s' % TestCliDriver.image_name_aws, 'output': 'unnecessary'},
            {'cmd': 'ecr get-login --no-include-email', 'output': [ login_cmd ], 'dry_run': False, 'docker_image': TestCliDriver.image_name_aws},
            {'cmd': login_cmd, 'output': 'unnecessary'},
            {'cmd': 'docker login -u %s -p %s https://%s' % (TestCliDriver.cdp_custom_registry_user, TestCliDriver.cdp_custom_registry_token, TestCliDriver.cdp_custom_registry), 'output': 'unnecessary'},
            {'cmd': 'docker pull %s' % TestCliDriver.image_name_aws, 'output': 'unnecessary'},
            {'cmd': 'ecr list-images --repository-name %s --max-items 0' % (TestCliDriver.ci_project_path.lower()), 'output': 'unnecessary', 'docker_image': TestCliDriver.image_name_aws},
            {'cmd': 'docker build -t %s/%s:%s .' % (aws_host, TestCliDriver.ci_project_path.lower(), TestCliDriver.ci_commit_sha), 'output': 'unnecessary'},
            {'cmd': 'docker push %s/%s:%s' % (aws_host, TestCliDriver.ci_project_path.lower(), TestCliDriver.ci_commit_sha), 'output': 'unnecessary'}
        ]
        self.__run_CLIDriver({ 'docker', '--use-aws-ecr', '--image-tag-sha1' }, verif_cmd)


    def test_docker_verbose_usedockercompose_imagetaglatest_imagetagsha1_useawsecr_withrepo(self):
        # Create FakeCommand
        aws_host = 'ecr.amazonaws.com'
        login_cmd = 'docker login -u user -p pass https://%s' % aws_host
        verif_cmd = [
            {'cmd': 'env', 'dry_run': False, 'output': 'unnecessary'},
            {'cmd': 'docker pull %s' % TestCliDriver.image_name_aws, 'output': 'unnecessary'},
            {'cmd': 'ecr get-login --no-include-email', 'output': [ login_cmd ], 'dry_run': False, 'docker_image': TestCliDriver.image_name_aws},
            {'cmd': login_cmd, 'output': 'unnecessary'},
            {'cmd': 'docker login -u %s -p %s https://%s' % (TestCliDriver.cdp_custom_registry_user, TestCliDriver.cdp_custom_registry_token, TestCliDriver.cdp_custom_registry), 'output': 'unnecessary'},
            {'cmd': 'docker pull %s' % TestCliDriver.image_name_aws, 'output': 'unnecessary'},
            {'cmd': 'docker-compose config --services', 'output': ['test', 'test2']},
            {'cmd': 'ecr list-images --repository-name %s/test --max-items 0' % (TestCliDriver.ci_project_path.lower()), 'output': 'unnecessary', 'docker_image': TestCliDriver.image_name_aws},
            {'cmd': 'ecr list-images --repository-name %s/test2 --max-items 0' % (TestCliDriver.ci_project_path.lower()), 'output': 'unnecessary', 'docker_image': TestCliDriver.image_name_aws},
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
            {'cmd': 'env', 'dry_run': False, 'output': 'unnecessary'},
            {'cmd': 'docker pull %s' % TestCliDriver.image_name_aws, 'output': 'unnecessary'},
            {'cmd': 'ecr get-login --no-include-email', 'output': [ login_cmd ], 'dry_run': False, 'docker_image': TestCliDriver.image_name_aws},
            {'cmd': login_cmd, 'output': 'unnecessary'},
            {'cmd': 'docker login -u %s -p %s https://%s' % (TestCliDriver.cdp_custom_registry_user, TestCliDriver.cdp_custom_registry_token, TestCliDriver.cdp_custom_registry), 'output': 'unnecessary'},
            {'cmd': 'docker pull %s' % TestCliDriver.image_name_aws, 'output': 'unnecessary'},
            {'cmd': 'docker-compose config --services', 'output': ['test', 'test2']},
            {'cmd': 'ecr list-images --repository-name %s/test --max-items 0' % (TestCliDriver.ci_project_path.lower()), 'output': 'unnecessary', 'throw': ValueError, 'docker_image': TestCliDriver.image_name_aws},
            {'cmd': 'ecr create-repository --repository-name %s/test' % (TestCliDriver.ci_project_path.lower()), 'output': 'unnecessary', 'docker_image': TestCliDriver.image_name_aws},
            {'cmd': 'ecr list-images --repository-name %s/test2 --max-items 0' % (TestCliDriver.ci_project_path.lower()), 'output': 'unnecessary', 'throw': ValueError, 'docker_image': TestCliDriver.image_name_aws},
            {'cmd': 'ecr create-repository --repository-name %s/test2' % (TestCliDriver.ci_project_path.lower()), 'output': 'unnecessary', 'docker_image': TestCliDriver.image_name_aws},
            {'cmd': 'docker-compose build', 'output': 'unnecessary', 'env_vars' : { TestCliDriver.env_cdp_tag: 'latest', TestCliDriver.env_cdp_registry: '%s/%s' % (aws_host, TestCliDriver.ci_project_path.lower())}},
            {'cmd': 'docker-compose push', 'output': 'unnecessary', 'env_vars' : { TestCliDriver.env_cdp_tag: 'latest', TestCliDriver.env_cdp_registry: '%s/%s' % (aws_host, TestCliDriver.ci_project_path.lower())}},
            {'cmd': 'docker-compose build', 'output': 'unnecessary', 'env_vars' : { TestCliDriver.env_cdp_tag: TestCliDriver.ci_commit_sha, TestCliDriver.env_cdp_registry: '%s/%s' % (aws_host, TestCliDriver.ci_project_path.lower())}},
            {'cmd': 'docker-compose push', 'output': 'unnecessary', 'env_vars' : { TestCliDriver.env_cdp_tag: TestCliDriver.ci_commit_sha, TestCliDriver.env_cdp_registry: '%s/%s' % (aws_host, TestCliDriver.ci_project_path.lower())}}
        ]
        self.__run_CLIDriver({ 'docker', '--verbose', '--use-docker-compose', '--image-tag-latest', '--image-tag-sha1', '--use-aws-ecr' }, verif_cmd)


    def test_artifactory_put_imagetagsha1_imagetaglatest_dockerhost(self):
        # Create FakeCommand
        upload_file = 'config/values.yaml'

        docker_host = 'unix:///var/run/docker.sock'

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
        self.__run_CLIDriver({ 'artifactory', '--put=%s' % upload_file, '--image-tag-sha1', '--image-tag-latest' },
            verif_cmd, docker_host = docker_host, env_vars = {'DOCKER_HOST': docker_host})

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

    def test_k8s_usegitlabregistry_missing_deploy_token(self):
        verif_cmd = [
            {'cmd': 'docker pull %s' % TestCliDriver.image_name_kubectl, 'output': 'unnecessary'},
            {'cmd': 'docker pull %s' % TestCliDriver.image_name_helm, 'output': 'unnecessary'},
            {'cmd': 'cp /cdp/k8s/secret/cdp-secret.yaml charts/templates/', 'output': 'unnecessary'}
        ]

        del os.environ['CI_DEPLOY_USER']
        del os.environ['CI_DEPLOY_PASSWORD']
        try:
            self.__run_CLIDriver({ 'k8s', '--use-gitlab-registry', '--namespace-project-branch-name' }, verif_cmd)
            raise ValueError('Previous command must return error.')
        except ValueError as e:
            # Ok beacause previous command return error.
             print e
        finally:
            os.environ['CI_DEPLOY_USER'] = TestCliDriver.ci_deploy_user
            os.environ['CI_DEPLOY_PASSWORD'] = TestCliDriver.ci_deploy_password


    @patch('cdpcli.clidriver.gitlab.Gitlab')
    def test_k8s_usegitlabregistry_namespaceprojectbranchname_values_dockerhost(self, mock_Gitlab):
        env_name = 'production'

        #Get Mock
        mock_projects, mock_environments, mock_env1, mock_env2 = self.__get_gitlab_mock(mock_Gitlab, env_name)

        # Create FakeCommand
        namespace = '%s%s-%s' % (TestCliDriver.ci_project_name_fisrt_letter, TestCliDriver.ci_project_id, TestCliDriver.ci_commit_ref_slug)
        namespace = namespace.replace('_', '-')[:63]
        staging_file = 'values.staging.yaml'
        int_file = 'values.int.yaml'
        values = ','.join([staging_file, int_file])

        docker_host = 'unix:///var/run/docker.sock'

        verif_cmd = [
            {'cmd': 'docker pull %s' % TestCliDriver.image_name_kubectl, 'output': 'unnecessary'},
            {'cmd': 'docker pull %s' % TestCliDriver.image_name_helm, 'output': 'unnecessary'},
            {'cmd': 'cp /cdp/k8s/secret/cdp-secret.yaml charts/templates/', 'output': 'unnecessary'},
            {'cmd': 'upgrade %s charts --timeout 600 --set namespace=%s --set ingress.host=%s.%s --set image.commit.sha=sha-%s --set image.registry=%s --set image.repository=%s --set image.tag=%s --set image.pullPolicy=Always --set image.credentials.username=%s --set image.credentials.password=%s --values charts/%s --values charts/%s --debug -i --namespace=%s --force'
                % (namespace[:53],
                    namespace,
                    namespace,
                    TestCliDriver.cdp_dns_subdomain,
                    TestCliDriver.ci_commit_sha[:8],
                    TestCliDriver.ci_registry,
                    TestCliDriver.ci_project_path.lower(),
                    TestCliDriver.ci_commit_ref_name,
                    TestCliDriver.ci_deploy_user,
                    TestCliDriver.ci_deploy_password,
                    staging_file,
                    int_file,
                    namespace), 'volume_from' : 'k8s', 'output': 'unnecessary', 'docker_image': TestCliDriver.image_name_helm},
            {'cmd': 'get deployments -n %s -o name' % (namespace), 'volume_from' : 'k8s', 'output': ['deployments/package1','deployments/package2'], 'docker_image': TestCliDriver.image_name_kubectl},
            {'cmd': 'get deployments package1 -n %s -o json' % (namespace), 'volume_from' : 'k8s', 'output': [ TestCliDriver.deployment_json_with_secret ], 'docker_image': TestCliDriver.image_name_kubectl},
            {'cmd': 'get deployments package2 -n %s -o json' % (namespace), 'volume_from' : 'k8s', 'output': [ TestCliDriver.deployment_json_with_secret ], 'docker_image': TestCliDriver.image_name_kubectl},
            {'cmd': 'rollout status deployments/package1 -n %s' % namespace, 'volume_from' : 'k8s', 'output': 'deployments/package1', 'timeout': '600', 'docker_image': TestCliDriver.image_name_kubectl},
            {'cmd': 'rollout status deployments/package2 -n %s' % namespace, 'volume_from' : 'k8s', 'output': 'deployments/package2', 'timeout': '600', 'docker_image': TestCliDriver.image_name_kubectl}
        ]
        self.__run_CLIDriver({ 'k8s', '--use-gitlab-registry', '--namespace-project-branch-name', '--values=%s' % values },
            verif_cmd, docker_host = docker_host, env_vars = { 'DOCKER_HOST': docker_host, 'CI_ENVIRONMENT_NAME': env_name})

        # GITLAB API check
        mock_Gitlab.assert_called_with(TestCliDriver.cdp_gitlab_api_url, private_token=TestCliDriver.cdp_gitlab_api_token)
        mock_projects.get.assert_called_with(TestCliDriver.ci_project_id)
        self.assertEqual(mock_env2.external_url, 'https://%s.%s' % (namespace, TestCliDriver.cdp_dns_subdomain))
        mock_env2.save.assert_called_with()


    def test_k8s_usecustomregistry_namespaceprojectbranchname_values(self):
        # Create FakeCommand
        namespace = '%s%s-%s' % (TestCliDriver.ci_project_name_fisrt_letter, TestCliDriver.ci_project_id, TestCliDriver.ci_commit_ref_slug)
        namespace = namespace.replace('_', '-')[:63]
        staging_file = 'values.staging.yaml'
        int_file = 'values.int.yaml'
        values = ','.join([staging_file, int_file])
        verif_cmd = [
            {'cmd': 'docker pull %s' % TestCliDriver.image_name_kubectl, 'output': 'unnecessary'},
            {'cmd': 'docker pull %s' % TestCliDriver.image_name_helm, 'output': 'unnecessary'},
            {'cmd': 'cp /cdp/k8s/secret/cdp-secret.yaml charts/templates/', 'output': 'unnecessary'},
            {'cmd': 'upgrade %s charts --timeout 600 --set namespace=%s --set ingress.host=%s.%s --set image.commit.sha=sha-%s --set image.registry=%s --set image.repository=%s --set image.tag=%s --set image.pullPolicy=Always --set image.credentials.username=%s --set image.credentials.password=%s --values charts/%s --values charts/%s --debug -i --namespace=%s --force'
                % (namespace[:53],
                    namespace,
                    namespace,
                    TestCliDriver.cdp_dns_subdomain_staging,
                    TestCliDriver.ci_commit_sha[:8],
                    TestCliDriver.cdp_custom_registry,
                    TestCliDriver.ci_project_path.lower(),
                    TestCliDriver.ci_commit_ref_name,
                    TestCliDriver.cdp_custom_registry_user,
                    TestCliDriver.cdp_custom_registry_read_only_token,
                    staging_file,
                    int_file,
                    namespace), 'volume_from' : 'k8s', 'output': 'unnecessary', 'docker_image': TestCliDriver.image_name_helm},
            {'cmd': 'get deployments -n %s -o name' % (namespace), 'volume_from' : 'k8s', 'output': ['deployments/package1','deployments/package2'], 'docker_image': TestCliDriver.image_name_kubectl},
            {'cmd': 'get deployments package1 -n %s -o json' % (namespace), 'volume_from' : 'k8s', 'output': [ TestCliDriver.deployment_json_without_secret ], 'docker_image': TestCliDriver.image_name_kubectl},
            {'cmd': 'patch deployments package1 -p \'{"spec":{"template":{"spec":{"imagePullSecrets": [{"name": "cdp-%s"}]}}}}\' -n %s' % (TestCliDriver.cdp_custom_registry, namespace), 'volume_from' : 'k8s', 'output': 'unnecessary', 'docker_image': TestCliDriver.image_name_kubectl},
            {'cmd': 'get deployments package2 -n %s -o json' % (namespace), 'volume_from' : 'k8s', 'output': [ TestCliDriver.deployment_json_without_secret ], 'docker_image': TestCliDriver.image_name_kubectl},
            {'cmd': 'patch deployments package2 -p \'{"spec":{"template":{"spec":{"imagePullSecrets": [{"name": "cdp-%s"}]}}}}\' -n %s' % (TestCliDriver.cdp_custom_registry, namespace), 'volume_from' : 'k8s', 'output': 'unnecessary', 'docker_image': TestCliDriver.image_name_kubectl},
            {'cmd': 'rollout status deployments/package1 -n %s' % namespace, 'volume_from' : 'k8s', 'output': 'deployments/package1', 'timeout': '600', 'docker_image': TestCliDriver.image_name_kubectl},
            {'cmd': 'rollout status deployments/package2 -n %s' % namespace, 'volume_from' : 'k8s', 'output': 'deployments/package2', 'timeout': '600', 'docker_image': TestCliDriver.image_name_kubectl}
        ]
        self.__run_CLIDriver({ 'k8s', '--use-custom-registry', '--namespace-project-branch-name', '--values=%s' % values }, verif_cmd,
            env_vars = {'CI_RUNNER_TAGS': 'test, staging'})

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
        date_format = '%Y-%m-%dT%H%M%SZ'

        verif_cmd = [
            {'cmd': 'env', 'dry_run': False, 'output': 'unnecessary'},
            {'cmd': 'docker pull %s' % TestCliDriver.image_name_aws, 'output': 'unnecessary'},
            {'cmd': 'ecr get-login --no-include-email', 'output': [ login_cmd ], 'dry_run': False, 'docker_image': TestCliDriver.image_name_aws},
            {'cmd': 'docker pull %s' % TestCliDriver.image_name_kubectl, 'output': 'unnecessary'},
            {'cmd': 'docker pull %s' % TestCliDriver.image_name_helm, 'output': 'unnecessary'},
            {'cmd': 'upgrade %s %s --timeout %s --set namespace=%s --set ingress.host=%s.%s --set image.commit.sha=sha-%s --set image.registry=%s --set image.repository=%s --set image.tag=%s --set image.pullPolicy=IfNotPresent --values %s/%s --debug -i --namespace=%s --force'
                % (TestCliDriver.ci_project_name,
                    deploy_spec_dir,
                    timeout,
                    namespace,
                    TestCliDriver.ci_project_name,
                    TestCliDriver.cdp_dns_subdomain,
                    TestCliDriver.ci_commit_sha[:8],
                    aws_host,
                    TestCliDriver.ci_project_path.lower(),
                    TestCliDriver.ci_commit_sha,
                    deploy_spec_dir,
                    values,
                    namespace), 'volume_from' : 'k8s', 'output': 'unnecessary', 'docker_image': TestCliDriver.image_name_helm},
            {'cmd': 'label namespace %s deletable=true creationTimestamp=%s deletionTimestamp=%s --namespace=%s --overwrite'
                % (namespace,
                    datetime.datetime.now().strftime(date_format),
                    (datetime.datetime.now() + datetime.timedelta(minutes = delete_minutes)).strftime(date_format),
                    namespace), 'volume_from' : 'k8s', 'output': 'unnecessary', 'docker_image': TestCliDriver.image_name_kubectl},
            {'cmd': 'get deployments -n %s -o name' % (namespace), 'volume_from' : 'k8s', 'output': ['deployments/package1'], 'docker_image': TestCliDriver.image_name_kubectl},
            {'cmd': 'rollout status deployments/package1 -n %s' % (namespace), 'volume_from' : 'k8s', 'output': 'unnecessary', 'timeout': str(timeout), 'docker_image': TestCliDriver.image_name_kubectl}
        ]
        self.__run_CLIDriver({ 'k8s', '--verbose', '--image-tag-sha1', '--use-aws-ecr', '--namespace-project-name', '--deploy-spec-dir=%s' % deploy_spec_dir, '--timeout=%s' % timeout, '--values=%s' % values, '--delete-labels=%s' % delete_minutes}, verif_cmd,
            env_vars = {'CI_RUNNER_TAGS': 'test, test2'})

    @patch('cdpcli.clidriver.gitlab.Gitlab')
    @patch('cdpcli.clidriver.os.path.isdir', return_value=False)
    @patch('cdpcli.clidriver.os.path.isfile', return_value=False)
    @patch('cdpcli.clidriver.os.makedirs')
    @patch("__builtin__.open")
    @patch("cdpcli.clidriver.yaml.dump")
    def test_k8s_createdefaulthelm_imagetagsha1_useawsecr_namespaceprojectname_overridesleep(self, mock_dump, mock_open, mock_makedirs, mock_isfile, mock_isdir, mock_Gitlab):
        env_name = 'review/test'

        #Get Mock
        mock_projects, mock_environments, mock_env1, mock_env2 = self.__get_gitlab_mock(mock_Gitlab, env_name)

        # Create FakeCommand
        aws_host = 'ecr.amazonaws.com'
        login_cmd = 'docker login -u user -p pass https://%s' % aws_host
        namespace = TestCliDriver.ci_project_name
        deploy_spec_dir = 'chart'
        sleep = 10
        sleep_override = 20
        verif_cmd = [
            {'cmd': 'docker pull %s' % TestCliDriver.image_name_aws, 'output': 'unnecessary'},
            {'cmd': 'ecr get-login --no-include-email', 'output': [ login_cmd ], 'dry_run': False, 'docker_image': TestCliDriver.image_name_aws},
            {'cmd': 'docker pull %s' % TestCliDriver.image_name_kubectl, 'output': 'unnecessary'},
            {'cmd': 'docker pull %s' % TestCliDriver.image_name_helm, 'output': 'unnecessary'},
            {'cmd': 'cp -R /cdp/k8s/charts/* %s/' % deploy_spec_dir, 'output': 'unnecessary'},
            {'cmd': 'upgrade %s %s --timeout 600 --set namespace=%s --set service.internalPort=8080 --set ingress.host=%s.%s --set image.commit.sha=sha-%s --set image.registry=%s --set image.repository=%s --set image.tag=%s --set image.pullPolicy=IfNotPresent --debug -i --namespace=%s --force'
                % (TestCliDriver.ci_project_name,
                    deploy_spec_dir,
                    namespace,
                    TestCliDriver.ci_project_name,
                    TestCliDriver.cdp_dns_subdomain,
                    TestCliDriver.ci_commit_sha[:8],
                    aws_host,
                    TestCliDriver.ci_project_path.lower(),
                    TestCliDriver.ci_commit_sha,
                    namespace), 'volume_from' : 'k8s', 'output': 'unnecessary', 'docker_image': TestCliDriver.image_name_helm},
            {'cmd': 'get deployments -n %s -o name' % (namespace), 'volume_from' : 'k8s', 'output': ['deployments/package1'], 'docker_image': TestCliDriver.image_name_kubectl},
            {'cmd': 'rollout status deployments/package1 -n %s' % (namespace), 'volume_from' : 'k8s', 'output': 'unnecessary', 'timeout': '600', 'docker_image': TestCliDriver.image_name_kubectl},
            {'cmd': 'sleep %s' % sleep_override, 'output': 'unnecessary'}
        ]
        self.__run_CLIDriver({ 'k8s', '--create-default-helm', '--image-tag-sha1', '--use-aws-ecr', '--namespace-project-name', '--deploy-spec-dir=%s' % deploy_spec_dir, '--sleep=%s' % sleep },
            verif_cmd, env_vars = { 'CI_ENVIRONMENT_NAME' : env_name, 'CI_RUNNER_TAGS': 'test', 'CDP_SLEEP': str(sleep_override)})

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

        # GITLAB API check
        mock_Gitlab.assert_called_with(TestCliDriver.cdp_gitlab_api_url, private_token=TestCliDriver.cdp_gitlab_api_token)
        mock_projects.get.assert_called_with(TestCliDriver.ci_project_id)
        self.assertEqual(mock_env2.external_url, 'https://%s.%s' % (TestCliDriver.ci_project_name, TestCliDriver.cdp_dns_subdomain))
        mock_env2.save.assert_called_with()

    @patch('cdpcli.clidriver.gitlab.Gitlab')
    @patch('cdpcli.clidriver.os.path.isdir', return_value=False)
    @patch('cdpcli.clidriver.os.path.isfile', return_value=False)
    @patch('cdpcli.clidriver.os.makedirs')
    @patch("__builtin__.open")
    @patch("cdpcli.clidriver.yaml.dump")
    def test_k8s_createdefaulthelmwithspecificport_imagetagsha1_useawsecr_namespaceprojectname_sleep(self, mock_dump, mock_open, mock_makedirs, mock_isfile, mock_isdir, mock_Gitlab):
        env_name = 'review/test'

        #Get Mock
        mock_projects, mock_environments, mock_env1, mock_env2 = self.__get_gitlab_mock(mock_Gitlab, env_name)

        # Create FakeCommand
        internal_port = 80
        aws_host = 'ecr.amazonaws.com'
        login_cmd = 'docker login -u user -p pass https://%s' % aws_host
        namespace = TestCliDriver.ci_project_name
        deploy_spec_dir = 'chart'
        sleep = 10
        verif_cmd = [
            {'cmd': 'docker pull %s' % TestCliDriver.image_name_aws, 'output': 'unnecessary'},
            {'cmd': 'ecr get-login --no-include-email', 'output': [ login_cmd ], 'dry_run': False, 'docker_image': TestCliDriver.image_name_aws},
            {'cmd': 'docker pull %s' % TestCliDriver.image_name_kubectl, 'output': 'unnecessary'},
            {'cmd': 'docker pull %s' % TestCliDriver.image_name_helm, 'output': 'unnecessary'},
            {'cmd': 'cp -R /cdp/k8s/charts/* %s/' % deploy_spec_dir, 'output': 'unnecessary'},
            {'cmd': 'upgrade %s %s --timeout 600 --set namespace=%s --set service.internalPort=%s --set ingress.host=%s.%s --set image.commit.sha=sha-%s --set image.registry=%s --set image.repository=%s --set image.tag=%s --set image.pullPolicy=IfNotPresent --debug -i --namespace=%s --force'
                % (TestCliDriver.ci_project_name,
                    deploy_spec_dir,
                    namespace,
                    internal_port,
                    TestCliDriver.ci_project_name,
                    TestCliDriver.cdp_dns_subdomain,
                    TestCliDriver.ci_commit_sha[:8],
                    aws_host,
                    TestCliDriver.ci_project_path.lower(),
                    TestCliDriver.ci_commit_sha,
                    namespace), 'volume_from' : 'k8s', 'output': 'unnecessary', 'docker_image': TestCliDriver.image_name_helm},
            {'cmd': 'get deployments -n %s -o name' % (namespace), 'volume_from' : 'k8s', 'output': ['deployments/package1'], 'docker_image': TestCliDriver.image_name_kubectl},
            {'cmd': 'rollout status deployments/package1 -n %s' % (namespace), 'volume_from' : 'k8s', 'output': 'unnecessary', 'timeout': '600', 'docker_image': TestCliDriver.image_name_kubectl},
            {'cmd': 'sleep %s' % sleep, 'output': 'unnecessary'}
        ]
        self.__run_CLIDriver({ 'k8s', '--create-default-helm', '--internal-port=%s' % internal_port, '--image-tag-sha1', '--use-aws-ecr', '--namespace-project-name', '--deploy-spec-dir=%s' % deploy_spec_dir, '--sleep=%s' % sleep },
            verif_cmd, env_vars = { 'CI_ENVIRONMENT_NAME' : env_name, 'CI_RUNNER_TAGS': 'test'})

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

        # GITLAB API check
        mock_Gitlab.assert_called_with(TestCliDriver.cdp_gitlab_api_url, private_token=TestCliDriver.cdp_gitlab_api_token)
        mock_projects.get.assert_called_with(TestCliDriver.ci_project_id)
        self.assertEqual(mock_env2.external_url, 'https://%s.%s' % (TestCliDriver.ci_project_name, TestCliDriver.cdp_dns_subdomain))
        mock_env2.save.assert_called_with()


    def test_validator_validateconfigurations_dockerhost(self):
        docker_host = 'unix:///var/run/docker.sock'

        namespace = '%s%s-%s' % (TestCliDriver.ci_project_name_fisrt_letter, TestCliDriver.ci_project_id, TestCliDriver.ci_commit_ref_slug)
        namespace = namespace.replace('_', '-')[:63]

        url = '%s/validate/configurations?url=https://%s.%s/%s' % (TestCliDriver.cdp_bp_validator_host, namespace, TestCliDriver.cdp_dns_subdomain, 'configurations')

        verif_cmd = [
            {'cmd': 'curl -s %s | jq .' % (url), 'output': 'unnecessary'},
            {'cmd': 'curl -sf --output /dev/null %s' % (url), 'output': 'unnecessary'}
        ]
        self.__run_CLIDriver({ 'validator-server', '--validate-configurations' }, verif_cmd, docker_host = docker_host, env_vars = { 'DOCKER_HOST' : docker_host})

    def test_validator_verbose_namespaceprojectname_validateconfigurations(self):

        url = '%s/validate/configurations?url=https://%s.%s/%s' % (TestCliDriver.cdp_bp_validator_host, TestCliDriver.ci_project_name, TestCliDriver.cdp_dns_subdomain, 'configurations')

        verif_cmd = [
            {'cmd': 'env', 'dry_run': False, 'output': 'unnecessary'},
            {'cmd': 'curl -s %s | jq .' % (url), 'output': 'unnecessary'},
            {'cmd': 'curl -sf --output /dev/null %s' % (url), 'output': 'unnecessary'}
        ]
        self.__run_CLIDriver({ 'validator-server', '--verbose', '--namespace-project-name', '--validate-configurations' }, verif_cmd)

    def test_validator_path_validateconfigurations_sleep(self):
        path = 'blockconfigurations'
        sleep = 10

        namespace = '%s%s-%s' % (TestCliDriver.ci_project_name_fisrt_letter, TestCliDriver.ci_project_id, TestCliDriver.ci_commit_ref_slug)
        namespace = namespace.replace('_', '-')[:63]

        url = '%s/validate/configurations?url=https://%s.%s/%s' % (TestCliDriver.cdp_bp_validator_host, namespace, TestCliDriver.cdp_dns_subdomain, path)

        verif_cmd = [
            {'cmd': 'curl -s %s | jq .' % (url), 'output': 'unnecessary'},
            {'cmd': 'curl -sf --output /dev/null %s' % (url), 'output': 'unnecessary'},
            {'cmd': 'sleep %s' % sleep, 'output': 'unnecessary'}
        ]
        self.__run_CLIDriver({ 'validator-server', '--path=%s' % path, '--validate-configurations', '--sleep=%s' % sleep }, verif_cmd)


    def test_validator_validateconfigurations_ko(self):
        namespace = '%s%s-%s' % (TestCliDriver.ci_project_name_fisrt_letter, TestCliDriver.ci_project_id, TestCliDriver.ci_commit_ref_slug)
        namespace = namespace.replace('_', '-')[:63]

        url = '%s/validate/configurations?url=https://%s.%s/%s' % (TestCliDriver.cdp_bp_validator_host, namespace, TestCliDriver.cdp_dns_subdomain, 'configurations')

        verif_cmd = [
            {'cmd': 'curl -s %s | jq .' % (url), 'output': 'unnecessary'},
            {'cmd': 'curl -sf --output /dev/null %s' % (url), 'output': 'unnecessary', 'throw': ValueError}
        ]
        try:
            self.__run_CLIDriver({ 'validator-server', '--validate-configurations' }, verif_cmd)
            raise ValueError('Previous command must return error.')
        except ValueError as e:
            # Ok beacause previous command return error.
             print e

    def __run_CLIDriver(self, args, verif_cmd, docker_host = 'unix:///var/run/docker.sock', env_vars = {}):
        cdp_docker_host_internal = '172.17.0.1'
        try:
            for key,val in env_vars.items():
                os.environ[key] = val

            verif_cmd.insert(0, {'cmd': 'ip route | awk \'NR==1 {print $3}\'', 'output': [cdp_docker_host_internal]})
            cmd = FakeCommand(verif_cmd = verif_cmd)
            cli = CLIDriver(cmd = cmd, opt = docopt(__doc__, args))
            cli.main()
        except BaseException as e:
            print '************************** ERROR *******************************'
            print e
            print '****************************************************************'
            raise e
        finally:
            try:
                self.assertEqual(docker_host, os.environ['DOCKER_HOST'])
                self.assertEqual(cdp_docker_host_internal, os.environ['CDP_DOCKER_HOST_INTERNAL'])
                cmd.verify_commands()
            finally:
                for key,val in env_vars.items():
                    del os.environ[key]

    def __get_gitlab_mock(self, mock_Gitlab, mock_env2_name = 'test2'):
        mock_env1 = Mock()
        mock_env1.name = 'test'
        mock_env1.external_url = None
        mock_env2 = Mock()
        mock_env2.name = mock_env2_name
        mock_env2.external_url = None

        mock_environments = Mock()
        attrs1 = {'list.return_value': [mock_env1, mock_env2]}
        mock_environments.configure_mock(**attrs1)

        mock_projects = Mock()
        attrs = {'get.return_value.environments': mock_environments}
        mock_projects.configure_mock(**attrs)

        mock_Gitlab.return_value.projects = mock_projects

        return mock_projects, mock_environments, mock_env1, mock_env2
