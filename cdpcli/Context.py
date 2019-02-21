#!/usr/bin/env python2.7

from __future__ import absolute_import
import os
import re

from .dockercommand import DockerCommand

class Context(object):

    def __init__(self, opt, cmd):
        self._opt = opt
        self._cmd = cmd

        if opt['--use-aws-ecr'] or opt['--use-custom-registry'] or opt['--use-gitlab-registry']:

            if opt['--use-aws-ecr'] or opt['maven'] or opt['docker']:
                aws_cmd = DockerCommand(cmd, opt['--docker-image-aws'], None, True)
                # Use AWS ECR from k8s configuration on gitlab-runner deployment
                login_regex = re.findall('docker login -u (.*) -p (.*) https://(.*)', aws_cmd.run('ecr get-login --no-include-email', dry_run=False)[0].strip())

                self._registry = login_regex[0][2]
                self._registry_user_ro = login_regex[0][0]
                self._registry_token_ro = login_regex[0][1]

                # Login AWS registry
                self.__login(login_regex[0][2], login_regex[0][0], login_regex[0][1])

            if opt['--use-custom-registry']:
                self._registry = os.environ['CDP_CUSTOM_REGISTRY']
                self._registry_user_ro = os.environ['CDP_CUSTOM_REGISTRY_USER']
                self._registry_token_ro = os.environ['CDP_CUSTOM_REGISTRY_READ_ONLY_TOKEN']

            if opt['--use-gitlab-registry']:
                # Use gitlab registry
                self._registry = os.environ['CI_REGISTRY']
                self._registry_user_ro = os.getenv('CI_DEPLOY_USER', None)
                self._registry_token_ro =  os.getenv('CI_DEPLOY_PASSWORD', None)


            # Login custom registry
            self.__login(os.getenv('CDP_CUSTOM_REGISTRY', None), os.getenv('CDP_CUSTOM_REGISTRY_USER', None), os.getenv('CDP_CUSTOM_REGISTRY_TOKEN', None))

            # Login gitlab registry
            self.__login(os.getenv('CI_REGISTRY', None), os.getenv('CI_REGISTRY_USER', None), os.getenv('CI_JOB_TOKEN', None))



        if opt['--put'] or opt['--delete']:
            self._registry = os.environ['CI_REGISTRY']

        self._repository = os.environ['CI_PROJECT_PATH'].lower()


    @property
    def opt(self):
        return self._opt

    @property
    def registry(self):
        return self._registry

    @property
    def registry_user_ro(self):
        return self.__verif_attr(self._registry_user_ro)

    @property
    def registry_token_ro(self):
        return self.__verif_attr(self._registry_token_ro)

    @property
    def repository(self):
        return self._repository

    def __verif_attr(self, attr):
        if attr is None:
            raise ValueError('Compatible with gitlab >= 10.8 or deploy token with the name gitlab-deploy-token and the scope read_registry must be created in this project.')
        return attr

    def __login(self, registry, registry_user, registry_token):
        # Activate login, only specific stage.
        if self._opt['maven'] or self._opt['docker']:
            if registry_user is not None and registry_token is not None and registry is not None:
                self._cmd.run_command('docker login -u %s -p %s https://%s' % (registry_user, registry_token, registry))
