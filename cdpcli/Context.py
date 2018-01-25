#!/usr/bin/env python

import os

class Context(object):

    def __init__(self, opt, cmd):
        self._opt = opt
        if opt['--use-aws-ecr']:
            # Use AWS ECR from k8s configuration on gitlab-runner deployment
            self._login = cmd.run_command('aws ecr get-login --no-include-email --region eu-central-1', False).strip()
            self._registry = (self._login.split('https://')[1]).strip()
        else:
            self._login = 'docker login -u %s -p %s %s' % (os.environ['CI_REGISTRY_USER'], os.environ['CI_JOB_TOKEN'], os.environ['CI_REGISTRY'])
                # Use gitlab registry
            self._registry = os.environ['CI_REGISTRY']

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
    def repository(self):
        return self._repository
