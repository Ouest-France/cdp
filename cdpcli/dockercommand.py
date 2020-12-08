import subprocess
import logging, verboselogs
import os

LOG = verboselogs.VerboseLogger('dockercommand')
LOG.addHandler(logging.StreamHandler())
LOG.setLevel(logging.INFO)

class DockerCommand(object):

    def __init__(self, cmd, docker_image, volume_from = None, with_entrypoint = False):
        self._cmd = cmd
        self._docker_image = docker_image
        self._volume_from = volume_from
        self._with_entrypoint = with_entrypoint
        self._cmd.run_command('docker pull %s' % docker_image)

    def run(self, prg_cmd, dry_run = None, timeout = None, workingDir = True):
        run_docker_cmd = 'docker run --rm -e DOCKER_HOST'

        for env in os.environ:
            if env.startswith('CI') or env.startswith('CDP') or env.startswith('AWS') or env.startswith('GIT') or env.startswith('KUBERNETES') or env.startswith('http'):
                run_docker_cmd = '%s -e %s' % (run_docker_cmd, env)

        run_docker_cmd = '%s -v /var/run/docker.sock:/var/run/docker.sock' % (run_docker_cmd)
       
        if self._volume_from is not None:
          if self._volume_from == 'k8s':
            run_docker_cmd = '%s --volumes-from $(docker ps -aqf "name=k8s_build_${HOSTNAME}")' % (run_docker_cmd)
          elif self._volume_from == 'docker':
            run_docker_cmd = '%s --volumes-from $(docker ps -aqf "name=${HOSTNAME}-build")' % (run_docker_cmd)
          elif self._volume_from == 'local':
            run_docker_cmd = '%s -v $PWD:$PWD' % (run_docker_cmd)
          else:  
            run_docker_cmd = '%s -v %s' % (run_docker_cmd, self._volume_from)
        
        if (workingDir is not False):
            run_docker_cmd = '%s -w %s' % (run_docker_cmd, '${PWD}' if workingDir is True else workingDir )

        run_docker_cmd = '%s %s' % (run_docker_cmd, self._docker_image)
        if (self._with_entrypoint):
            run_docker_cmd = '%s %s' % (run_docker_cmd, prg_cmd)
        else:
            run_docker_cmd = '%s /bin/sh -c \'%s\'' % (run_docker_cmd, prg_cmd)


        LOG.info('')
        LOG.info('******************** Docker command ********************')
        LOG.info('Image: %s' % self._docker_image)
        LOG.info('Command: %s' % prg_cmd)
        LOG.verbose(run_docker_cmd)

        return self._cmd.run(run_docker_cmd, dry_run=dry_run, timeout=timeout)
