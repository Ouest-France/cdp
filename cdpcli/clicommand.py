import subprocess, threading
import logging, verboselogs

LOG = verboselogs.VerboseLogger('clicommand')
LOG.addHandler(logging.StreamHandler())
LOG.setLevel(logging.INFO)

class CLICommand(object):

    def __init__(self, dry_run = 1):
        self._dry_run = dry_run
        LOG.verbose('Dry-run init %s' % self._dry_run)

    def run_command(self, command, dry_run = None, timeout = None):
        self._output = None
        self._process = None
        if dry_run is None:
            self._real_dry_run = self._dry_run
        else:
            self._real_dry_run = dry_run

        def target():
            LOG.info('')
            LOG.info('******************** Run command ********************')
            LOG.info(command)
            # If dry-run option, no execute command
            if not self._real_dry_run:
                self._process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
                self._output, error = self._process.communicate()

                if self._process.returncode != 0:
                    LOG.warning('---------- ERROR ----------')
                    if self._process.returncode == 143:
                        raise ValueError('Timeout %ss' % self._context.opt['--timeout'])
                    else:
                        raise ValueError(output)
                else:
                    LOG.info('---------- Output ----------')
                    LOG.info(output)

            LOG.info('')

        thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            self._process.terminate()
            thread.join()

        print self._output
