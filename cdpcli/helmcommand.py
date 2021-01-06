import subprocess
import logging, verboselogs
import os

LOG = verboselogs.VerboseLogger('dockercommand')
LOG.addHandler(logging.StreamHandler())
LOG.setLevel(logging.INFO)

class HelmCommand(object):

    def __init__(self, cmd, version, volume_from = None, with_entrypoint = False):
        self._cmd = cmd
        self._version = version
        self._volume_from = volume_from
        self._with_entrypoint = with_entrypoint

    def run(self, prg_cmd, dry_run = None, timeout = None, workingDir = True):
        prg_cmd = '%s %s' % ("helm" if self._version == "3" else "helm2", prg_cmd)

        LOG.info('')
        LOG.info('******************** Docker command ********************')
        LOG.info('Version: %s' % self._version)
        LOG.info('Command: %s' % prg_cmd)

        return self._cmd.run(prg_cmd, dry_run=dry_run, timeout=timeout)
