#!/usr/bin/env python

import os

class Context(object):

    def __init__(self, opt, cmd):
        self._opt = opt
        login = 'docker login -u %s -p %s %s'

        if opt['--use-aws-ecr']:
            # Use AWS ECR from k8s configuration on gitlab-runner deployment
            self._login = cmd.run_command('aws ecr get-login --no-include-email --region eu-central-1', False).strip()
            self._registry = (self._login.split('https://')[1]).strip()
        else:
            if opt['--use-custom-registry']:
                self._registry = os.environ['CDP_CUSTOM_REGISTRY']
                self._registry_user = os.environ['CDP_CUSTOM_REGISTRY_USER']
                self._registry_token = os.environ['CDP_CUSTOM_REGISTRY_TOKEN']
                self._registry_token_ro = os.environ['CDP_CUSTOM_REGISTRY_TOKEN_READ_ONLY']
            else:
                # Use gitlab registry
                self._registry = os.environ['CI_REGISTRY']
                self._registry_user = os.environ['CI_REGISTRY_USER']
                self._registry_token = os.environ['CI_JOB_TOKEN']
                self._registry_token_ro = os.environ['CDP_GITLAB_REGISTRY_TOKEN_READ_ONLY']

            self._login = login % (self._registry_user, self._registry_token, self._registry)

        self._repository = os.environ['CI_PROJECT_PATH'].lower()


    @property
    def opt(self):
        return self._opt

    @property
    def login(self):
        return self._login

    @property
    def registry(self):
        return self._registry

    @property
    def registry_user(self):
        return self._registry_user

    @property
    def registry_token(self):
        return self._registry_token

    @property
    def registry_token_ro(self):
        return self._registry_token_ro

    @property
    def repository(self):
        return self._repository
