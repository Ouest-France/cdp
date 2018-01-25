import subprocess
import logging, verboselogs

LOG = verboselogs.VerboseLogger('clicommand')
LOG.addHandler(logging.StreamHandler())
LOG.setLevel(logging.INFO)

class CLICommand(object):

    def __init__(self, dry_run = 1):
        self._dry_run = dry_run
        LOG.info('Dry-run init %s' % self._dry_run)

    def run_command(self, command, dry_run = None):
        if dry_run is None:
            dry_run = self._dry_run

        output = None
        LOG.info('')
        LOG.info('******************** Run command ********************')
        LOG.info(command)
        # If dry-run option, no execute command
        if not dry_run:
            p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            output, error = p.communicate()

            if p.returncode != 0:
                LOG.warning('---------- ERROR ----------')
                if p.returncode == 143:
                    raise ValueError('Timeout %ss' % self._context.opt['--timeout'])
                else:
                    raise ValueError(output)
            else:
                LOG.info('---------- Output ----------')
                LOG.info(output)

        LOG.info('')
        return output
