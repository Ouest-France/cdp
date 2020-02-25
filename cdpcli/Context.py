#!/usr/bin/env python2.7

from __future__ import absolute_import
import os
import re

from .dockercommand import DockerCommand

class Context(object):

    def __init__(self, opt, cmd):
        self._opt = opt
        self._cmd = cmd
        self._project_name = os.environ['CI_PROJECT_NAME'].lower()
        self._repository = os.environ['CI_PROJECT_PATH'].lower()
        self._registry_api_url = None
        self._registry_isHarbor = False

        if opt['--put'] or opt['--delete']:
            self._registry = os.environ['CI_REGISTRY']

        if opt['--login-registry'] and opt['--login-registry'] != opt['--use-registry']:
            if opt['--login-registry'] == 'aws-ecr':
                aws_cmd = DockerCommand(cmd, opt['--docker-image-aws'], None, True)
                login_regex = re.findall('docker login -u (.*) -p \'(.*)\' https://(.*)', aws_cmd.run('ecr get-login --no-include-email --cli-read-timeout 30 --cli-connect-timeout 30', dry_run=False)[0].strip())
                self._registry = login_regex[0][2]
                self._registry_user_ro = login_regex[0][0]
                self._registry_token_ro = login_regex[0][1]
                # Login AWS registry
                self.__login(self._registry, self._registry_user_ro,self._registry_token_ro)
            else:
                self.__login(os.getenv('CDP_%s_REGISTRY' % opt['--login-registry'].upper(), None),
                             os.getenv('CDP_%s_REGISTRY_USER' % opt['--login-registry'].upper(), None),
                             os.getenv('CDP_%s_REGISTRY_TOKEN' % opt['--login-registry'].upper(), None))

        if opt['--use-aws-ecr'] or opt['--use-custom-registry'] or opt['--use-gitlab-registry'] or opt['--use-registry'] != 'none':
            if opt['maven'] or opt['docker'] or opt['k8s']:
                if opt['--use-aws-ecr'] or opt['--use-registry'] == 'aws-ecr' or opt['--use-custom-registry'] == 'aws-ecr' :
                    ### Get login from AWS-CLI
                    aws_cmd = DockerCommand(cmd, opt['--docker-image-aws'], None, True)
                    login_regex = re.findall('docker login -u (.*) -p \'(.*)\' https://(.*)', aws_cmd.run('ecr get-login --no-include-email --cli-read-timeout 30 --cli-connect-timeout 30', dry_run=False)[0].strip())
                    self._registry = login_regex[0][2]
                    self._registry_user_ro = login_regex[0][0]
                    self._registry_token_ro = login_regex[0][1]
                    # Login AWS registry
                    self.__login(self._registry, self._registry_user_ro,self._registry_token_ro)

                elif opt['--use-gitlab-registry'] or opt['--use-registry'] == 'gitlab' or opt['--use-custom-registry'] == 'gitlab':
                    # Use gitlab registry
                    self.__set_registry(os.getenv('CI_REGISTRY', None),
                                        os.getenv('CI_DEPLOY_USER', None),
                                        os.getenv('CI_DEPLOY_PASSWORD', None))
                    # Login gitlab registry
                    self.__login(os.getenv('CI_REGISTRY', None),
                                 os.getenv('CI_REGISTRY_USER', None),
                                 os.getenv('CI_JOB_TOKEN', None))

                elif opt['--use-custom-registry']:
                    #deprecated
                    self.__set_registry(os.getenv('CDP_CUSTOM_REGISTRY', None),
                                       os.getenv('CDP_CUSTOM_REGISTRY_USER', None),
                                       os.getenv('CDP_CUSTOM_REGISTRY_READ_ONLY_TOKEN', None))
                    # Login custom registry
                    self.__login(os.getenv('CDP_CUSTOM_REGISTRY', None),
                                 os.getenv('CDP_CUSTOM_REGISTRY_USER', None),
                                 os.getenv('CDP_CUSTOM_REGISTRY_TOKEN', None))

                else:
                    ### Used by '--use-registry' params
                    self.__set_registry(os.getenv('Cvi % opt['--use-registry'].upper(),None),
                                        os.getenv('CDP_%s_REGISTRY_USER' % opt['--use-registry'].upper(),None),
                                        os.getenv('CDP_%s_REGISTRY_READ_ONLY_TOKEN' % opt['--use-registry'].upper(),None),
                                        os.getenv('CDP_%s_REGISTRY_TOKEN' % opt['--use-registry'].upper(),None),
                                        os.getenv('CDP_%s_REGISTRY_API_URL' % opt['--use-registry'].upper(),None))
                    self.__login(os.getenv('CDP_%s_REGISTRY' % opt['--use-registry'].upper(), None),
                                 os.getenv('CDP_%s_REGISTRY_USER' % opt['--use-registry'].upper(), None),
                                 os.getenv('CDP_%s_REGISTRY_TOKEN' % opt['--use-registry'].upper(), None))

    def __set_registry(self,registry,user_ro,token_ro, tokenOrPassword=None, api_url=None):
        self._registry = registry
        self._registry_user_ro = user_ro
        self._registry_token_ro = token_ro
        self._registry_token = token_ro
        if tokenOrPassword is not None:
           self._registry_token = tokenOrPassword
        self._registry_api_url = api_url
        if 'HARBOR' in registry.upper():
           self._registry_isHarbor = True
           
        self._registry_basic_auth = (user_ro, self._registry_token)

    @property
    def registryRepositoryName(self):
        if self._registry_isHarbor:
           return '%s/%s' % (self._project_name, self._project_name)
        return self._repository
        
    @property
    def registrySlugRepositoryName(self):
        return self.registryRepositoryName.replace('/','%2F')

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

    @property
    def project_name(self):
        return self._project_name

    @property
    def is_namespace_project_name(self):
        namespace =  os.getenv('CDP_NAMESPACE', None)
        if namespace is not None:
            return True if namespace == 'project-name' else False
        else:
            return self._opt['--namespace-project-name']

    @property
    def is_image_pull_secret(self):
        image_pull_secret =  os.getenv('CDP_IMAGE_PULL_SECRET', None)
        if image_pull_secret is not None:
            return True if image_pull_secret == 'true' else False
        else:
            return self.opt['--image-pull-secret']

    def __verif_attr(self, attr):
        if attr is None:
            raise ValueError('Compatible with gitlab >= 10.8 or deploy token with the name gitlab-deploy-token and the scope read_registry must be created in this project.')
        return attr

    def __login(self, registry, registry_user, registry_token):
        # Activate login, only specific stage.
        if registry_user is not None and registry_token is not None and registry is not None:
            self._cmd.run_secret_command('docker login -u %s -p \'%s\' https://%s' % (registry_user, registry_token, registry))