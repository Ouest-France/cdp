#!/usr/bin/env python
"""
Universal Command Line Environment for Continous Delivery Pipeline on Gitlab-CI.
Usage:
    cdp docker [(-v | --verbose | -q | --quiet)] [(-d | --dry-run)]
        [--image-tag-branch-name] [--image-tag-latest] [--image-tag-sha1]
        (--use-gitlab-registry | --use-aws-ecr)
        [--simulate-merge-on=<branch_name>]
    cdp k8s [(-v | --verbose | -q | --quiet)] [(-d | --dry-run)]
        [--image-tag-branch-name] [--image-tag-latest] [--image-tag-sha1]
        (--use-gitlab-registry | --use-aws-ecr)
        (--namespace-project-branch-name | --namespace-project-name)
        [--deploy-spec-dir=<dir>]
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
    --deploy-spec-dir=<dir>             k8s deployment files [default: charts/].
"""

import sys, os, subprocess
import logging, verboselogs
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

    # Configure docker registry
    if opt['--use-aws-ecr']:
        # Use AWS ECR from k8s configuration on gitlab-runner deployment
        login = __runCommand("aws ecr get-login --no-include-email --region eu-central-1", False).strip()
        image_name = "%s/%s" % ((login.split("https://")[1]).strip(), os.environ['CI_PROJECT_PATH'].lower())
    else:
        # Use gitlab registry
        login="docker login -u %s -p %s %s" % (os.environ['CI_REGISTRY_USER'], os.environ['CI_JOB_TOKEN'], os.environ['CI_REGISTRY'])
        image_name = os.environ['CI_REGISTRY_IMAGE']

    logger.verbose("Image name : %s", image_name)

    # Login to the docker registry
    __runCommand(login)

    # Build docker image from Dockerfile
    __runCommand("docker build -t %s ." % image_name)

    # Tag docker image
    if not (opt['--image-tag-branch-name'] or opt['--image-tag-latest'] or opt['--image-tag-sha1']) or opt['--image-tag-branch-name']:
        # Default if none option selected
        __tagAndPushOnDockerRegistry(image_name, os.environ['CI_COMMIT_REF_NAME'])
    if opt['--image-tag-latest']:
        __tagAndPushOnDockerRegistry(image_name, "latest")
    if opt['--image-tag-sha1']:
        __tagAndPushOnDockerRegistry(image_name, os.environ['CI_COMMIT_SHA'])

    # Clean git repository
    if opt['--simulate-merge-on']:
        __runCommand("git checkout .")

def __k8s():
    print('k8s - need to be implemented')


def __tagAndPushOnDockerRegistry(image_name, tag):
    # Tag docker image
    __runCommand("docker tag %s %s:%s" % (image_name, image_name, tag))
    # Push docker image
    __runCommand("docker push %s:%s" % (image_name, tag))

def __runCommand(command, dry_run = opt['--dry-run']):
    output = None
    logger.info("")
    logger.info("******************** Run command ********************")
    logger.info(command)
    # If dry-run option, no execute command
    if not dry_run:
        output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read()
        logger.notice(output)

    logger.info("")
    return output
