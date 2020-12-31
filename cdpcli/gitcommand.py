import subprocess
import logging, verboselogs
import os

LOG = verboselogs.VerboseLogger('dockercommand')
LOG.addHandler(logging.StreamHandler())
LOG.setLevel(logging.INFO)

class GitCommand(object):

    def __init__(self, cmd, docker_image, volume_from = None, with_entrypoint = False):
        self._cmd = cmd
        self._docker_image = docker_image
        self._volume_from = volume_from
        self._with_entrypoint = with_entrypoint

    def run(self, prg_cmd, dry_run = None, timeout = None, workingDir = True):
        prg_cmd = 'git %s' % (prg_cmd)

        LOG.info('')
        LOG.info('******************** Docker command ********************')
        LOG.info('Image: %s' % self._docker_image)
        LOG.info('Command: %s' % prg_cmd)

        return self._cmd.run(prg_cmd, dry_run=dry_run, timeout=timeout)
