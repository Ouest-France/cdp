import os
import subprocess, threading
import logging, verboselogs
import timeit

LOG = verboselogs.VerboseLogger('clicommand')
LOG.addHandler(logging.StreamHandler())


class CLICommand(object):

    def __init__(self, dry_run = 1, log_level = logging.INFO):
        self._dry_run = dry_run
        LOG.setLevel(log_level)
        LOG.verbose('Dry-run init %s' % self._dry_run)

    def run_command(self, command, dry_run = None, timeout = None, raise_error = True):
        LOG.info('')
        LOG.info('******************** Run command ********************')
        LOG.info(command)
        return self.run(command, dry_run, timeout, raise_error)

    def run_secret_command(self, command, dry_run = None, timeout = None, raise_error = True):
        if "CDP_DEBUG" in os.environ:
            LOG.info('')
            LOG.info('******************** Run command (debug) ********************')
            LOG.info(command)
        return self.run(command, dry_run, timeout, raise_error)
        
    def run(self, command, dry_run = None, timeout = None, raise_error = True):
        start = timeit.default_timer()
        self._process = None
        self._output = []
        if "CDP_DEBUG" in os.environ:
          LOG.verbose('******************** Run command (debug) ********************')
          LOG.verbose(command)

        if dry_run is None:
            self._real_dry_run = self._dry_run
        else:
            self._real_dry_run = dry_run

        def target():
            LOG.info('---------- Output ----------')
            # If dry-run option, no execute command
            if not self._real_dry_run:
                self._process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
                while True:
                    line = self._process.stdout.readline().decode('UTF-8')
                    if line.strip() == '' and self._process.poll() is not None:
                        break
                    if line:
                        self._output.append(line.strip())
                        LOG.info(line.rstrip('\n'))

        thread = threading.Thread(target=target)
        thread.start()
        thread.join(timeout if timeout is None else float(timeout))

        if thread.is_alive():
            self._process.terminate()
            thread.join()

        LOG.info('---------- Time: %s s' % (round(timeit.default_timer() - start, 3)))
        LOG.info('')
        LOG.verbose('---------- CLICommand output: %s' % self._output)
        LOG.verbose('')

        if raise_error and self._process is not None and self._process.returncode != 0:
            LOG.warning('---------- ERROR ----------')
            raise OSError(self._process.returncode,'Error code %s' % self._process.returncode)

        return self._output
