import subprocess
import logging, verboselogs

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

    def run(self, prg_cmd, dry_run = None, timeout = None):
        run_docker_cmd = 'docker run --rm -e DOCKER_HOST'
        run_docker_cmd = '%s $(env | grep "\(^CI\|^CDP\|^AWS\|^GIT\|^KUBERNETES\)" | cut -f1 -d= | sed \'s/^/-e /\')' % (run_docker_cmd)
        run_docker_cmd = '%s -v /var/run/docker.sock:/var/run/docker.sock' % (run_docker_cmd)

        if self._volume_from == 'k8s':
            run_docker_cmd = '%s --volumes-from $(docker ps -aqf "name=k8s_build_${HOSTNAME}")' % (run_docker_cmd)
        elif self._volume_from == 'docker':
            run_docker_cmd = '%s --volumes-from $(docker ps -aqf "name=${HOSTNAME}-build")' % (run_docker_cmd)

        run_docker_cmd = '%s -w ${PWD}' % (run_docker_cmd)
        run_docker_cmd = '%s %s' % (run_docker_cmd, self._docker_image)
        if (self._with_entrypoint):
            run_docker_cmd = '%s %s' % (run_docker_cmd, prg_cmd)
        else:
            run_docker_cmd = '%s /bin/sh -c \'%s\'' % (run_docker_cmd, prg_cmd)

        return self._cmd.run_command(run_docker_cmd, dry_run=dry_run, timeout=timeout)
