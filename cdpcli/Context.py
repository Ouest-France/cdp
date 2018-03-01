#!/usr/bin/env python2.7

import os
import re

class Context(object):

    def __init__(self, opt, cmd):
        self._opt = opt

        if opt['--use-aws-ecr']:
            os.environ['AWS_ACCESS_KEY_ID'] = os.environ['CDP_AWS_ACCESS_KEY_ID']
            os.environ['AWS_SECRET_ACCESS_KEY'] = os.environ['CDP_AWS_SECRET_ACCESS_KEY']
            # Use AWS ECR from k8s configuration on gitlab-runner deployment
            login_regex = re.findall('docker login -u (.*) -p (.*) https://(.*)', cmd.run_command('aws ecr get-login --no-include-email --region eu-central-1', False).strip())
            self._registry = login_regex[0][2]
            self._registry_user = login_regex[0][0]
            self._registry_token = login_regex[0][1]
            self._registry_token_ro = login_regex[0][1]
        elif opt['--use-custom-registry']:
            self._registry = os.environ['CDP_CUSTOM_REGISTRY']
            self._registry_user = os.environ['CDP_CUSTOM_REGISTRY_USER']
            self._registry_token = os.environ['CDP_CUSTOM_REGISTRY_TOKEN']
            self._registry_token_ro = os.environ['CDP_CUSTOM_REGISTRY_READ_ONLY_TOKEN']
        elif opt['--use-gitlab-registry']:
            # Use gitlab registry
            self._registry = os.environ['CI_REGISTRY']
            self._registry_user = os.environ['CI_REGISTRY_USER']
            self._registry_token = os.environ['CI_JOB_TOKEN']
            self._registry_token_ro = os.environ['CDP_GITLAB_REGISTRY_READ_ONLY_TOKEN']

        if opt['--put'] or opt['--delete']:
            self._registry = os.environ['CI_REGISTRY']

        self._repository = os.environ['CI_PROJECT_PATH'].lower()


    @property
    def opt(self):
        return self._opt

    @property
    def login(self):
        return 'docker login -u %s -p %s https://%s' % (self._registry_user, self._registry_token, self._registry)

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
