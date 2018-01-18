#!/usr/bin/env python
"""
Universal Command Line Environment for Continous Delivery Pipeline on Gitlab-CI.
Usage:
    cdp docker [(-v | --verbose | -q | --quiet)] [(-d | --dry-run)]
        [--image-tag-branch-name] [--image-tag-latest] [--image-tag-sha1]
        (--use-gitlab-registry | --use-aws-ecr)
        [--simulate-merge-on=<branch_name>]
    cdp k8s [(-v | --verbose | -q | --quiet)] [(-d | --dry-run)]
        [--image-tag-branch-name | --image-tag-latest | --image-tag-sha1]
        (--use-gitlab-registry | --use-aws-ecr)
        (--namespace-project-branch-name | --namespace-project-name)
        [--deploy-spec-dir=<dir>]
        [--timeout=<timeout>]
    cdp (-h | --help | --version)
Options:
    -h, --help                          Show this screen and exit.
    -v, --verbose                       Make more noise
    -q, --quiet                         Make less noise
    -d, --dry-run                       Simulate execution
    --image-tag-branch-name             Tag docker image with branch name or use it [default].
    --image-tag-latest                  Tag docker image with 'latest'  or use it.
    --image-tag-sha1                    Tag docker image with commit sha1  or use it.
    --use-gitlab-registry               Use gitlab registry for pull/push docker image [default].
    --use-aws-ecr                       Use AWS ECR from k8s configuraiton for pull/push docker image.
    --simulate-merge-on=<branch_name>   Build docker image with the merge current branch on specify branch (no commit).
    --namespace-project-branch-name     Use project and branch name to create k8s namespace [default].
    --namespace-project-name            Use project name to create k8s namespace.
    --deploy-spec-dir=<dir>             k8s deployment files [default: charts].
    --timeout=<timeout>                 Time in seconds to wait for any individual kubernetes operation [default: 180]
"""

import sys, os, subprocess
import logging, verboselogs
import time
from cdpcli import __version__
from docopt import docopt, DocoptExit

logger = verboselogs.VerboseLogger('cdp')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)

opt = docopt(__doc__, sys.argv[1:], version=__version__)
if opt['--verbose']:
    logger.setLevel(logging.VERBOSE)
elif opt['--quiet']:
    logger.setLevel(logging.WARNING)

def main():
    logger.verbose(opt)

    if opt['docker']:
        __docker()

    if opt['k8s']:
        __k8s()

def __docker():
    if opt['--simulate-merge-on']:
        logger.notice("Build docker image with the merge current branch on %s branch", opt['--simulate-merge-on'])

        # Merge branch on selected branch
        __runCommand("git config --global user.email \"%s\"" % os.environ['GITLAB_USER_EMAIL'])
        __runCommand("git config --global user.name \"%s\"" % os.environ['GITLAB_USER_ID'])
        __runCommand("git checkout %s" % opt['--simulate-merge-on'])
        __runCommand("git reset --hard origin/%s" % opt['--simulate-merge-on'])
        __runCommand("git merge %s --no-commit --no-ff" %  os.environ['CI_COMMIT_SHA'])

        # TODO Exception process
    else:
        logger.notice("Build docker image with the current branch : %s", os.environ['CI_COMMIT_REF_NAME'])

    login = __getLoginCmd()
    image_name = __getImageName(login)

    # Login to the docker registry
    __runCommand(login)

    # Build docker image from Dockerfile
    __runCommand("docker build -t %s ." % image_name)

    # Tag and push docker image
    if not (opt['--image-tag-branch-name'] or opt['--image-tag-latest'] or opt['--image-tag-sha1']) or opt['--image-tag-branch-name']:
        # Default if none option selected
        __tagAndPushOnDockerRegistry(image_name, __getImageTagBranchName(image_name))
    if opt['--image-tag-latest']:
        __tagAndPushOnDockerRegistry(image_name, __getImageTagLatest(image_name))
    if opt['--image-tag-sha1']:
        __tagAndPushOnDockerRegistry(image_name, __getImageTagSha1(image_name))



    # Clean git repository
    if opt['--simulate-merge-on']:
        __runCommand("git checkout .")

def __k8s():
    # Get k8s namespace
    if opt['--namespace-project-name']:
        namespace = os.environ['CI_PROJECT_NAME']
        host = "%s.%s" % (os.environ['CI_PROJECT_NAME'], os.environ['DNS_SUBDOMAIN'])
    else:
        namespace = "%s-%s" % (os.environ['CI_PROJECT_NAME'], os.environ['CI_COMMIT_REF_NAME'])    # Get deployment host
        host = "%s.%s.%s" % (os.environ['CI_ENVIRONMENT_SLUG'], os.environ['CI_PROJECT_NAME'], os.environ['DNS_SUBDOMAIN'])

    # Get image tag name
    image_name = __getImageName(__getLoginCmd())
    if opt['--image-tag-latest']:
        image_tag = __getImageTagLatest(image_name)
    elif opt['--image-tag-sha1']:
        image_tag = __getImageTagSha1(image_name)
    else :
        image_tag = __getImageTagBranchName(image_name)

    # Copy secret file on k8s deploy dir
    __runCommand("cp /cdp/charts/templates/*.yaml %s/templates/")

    # Instal or Upgrade environnement
    __runCommand("helm upgrade %s %s --timeout %s --set namespace=%s --set ingress.host=%s --set image.registry=%s --set image.commit.sha=%s --set image.tag=%s --set image.credentials.username=%s --set image.credentials.password=%s --debug -i --namespace=%s"
        % (namespace, opt['--deploy-spec-dir'], opt['--timeout'], namespace, host, os.environ['CI_REGISTRY'], os.environ['CI_COMMIT_SHA'][:8], image_tag, os.environ['CI_REGISTRY_USER'], os.environ['REGISTRY_PERMANENT_TOKEN'], namespace))

    # Patch secret on deployment
    deployment_names = __runCommand("kubectl get deployment -n %s -o name" % (namespace)).strip().split("\n")
    for deployment_name in deployment_names:
        __runCommand("kubectl patch deployment %s -p '{\"spec\":{\"template\":{\"spec\":{\"imagePullSecrets\": [{\"name\": \"cdp-%s\"}]}}}}' -n %n" % (deployment_name, os.environ['CI_REGISTRY'], namespace))

    # Issue on --request-timeout option ? https://github.com/kubernetes/kubernetes/issues/51952
    __runCommand("timeout -t %s kubectl rollout status deployment/%s -n %s" % (opt['--timeout'], os.environ['CI_PROJECT_NAME'], namespace))


def __tagAndPushOnDockerRegistry(image_name, image_tag):
    # Tag docker image
    __runCommand("docker tag %s %s" % (image_name, image_tag))
    # Push docker image
    __runCommand("docker push %s" % (image_tag))

def __runCommand(command, dry_run = opt['--dry-run']):
    output = None
    logger.info("")
    logger.info("******************** Run command ********************")
    logger.info(command)
    # If dry-run option, no execute command
    if not dry_run:
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        output, error = p.communicate()

        if p.returncode != 0:
            logger.warning("---------- ERROR ----------")
            if p.returncode == 143:
                raise ValueError("Timeout %ss" % opt['--timeout'])
            else:
                raise ValueError(output)
        else:
            logger.info("---------- Output ----------")
            logger.info(output)

    logger.info("")
    return output

def __getLoginCmd():
    # Configure docker registry
    if opt['--use-aws-ecr']:
        # Use AWS ECR from k8s configuration on gitlab-runner deployment
        login = __runCommand("aws ecr get-login --no-include-email --region eu-central-1", False).strip()
    else:
        # Use gitlab registry
        login = "docker login -u %s -p %s %s" % (os.environ['CI_REGISTRY_USER'], os.environ['CI_JOB_TOKEN'], os.environ['CI_REGISTRY'])

    return login

def __getImageName(login):
    # Configure docker registry
    if opt['--use-aws-ecr']:
        # Use AWS ECR from k8s configuration on gitlab-runner deployment
        image_name = "%s/%s" % ((login.split("https://")[1]).strip(), os.environ['CI_PROJECT_PATH'].lower())
    else:
        # Use gitlab registry
        image_name = os.environ['CI_REGISTRY_IMAGE']

    logger.verbose("Image name : %s", image_name)
    return image_name

def __getImageTagBranchName(image_name):
    return "%s:%s" %  (image_name, os.environ['CI_COMMIT_REF_NAME'])

def __getImageTagLatest(image_name):
    return "%s:latest" % image_name

def __getImageTagSha1(image_name):
    return "%s:%s" %  (image_name, os.environ['CI_COMMIT_SHA'])
