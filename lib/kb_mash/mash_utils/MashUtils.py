import time
import os
import errno
import subprocess
import csv


def log(message, prefix_newline=False):
    """
    Logging function, provides a hook to suppress or redirect log messages.
    """
    print(('\n' if prefix_newline else '') + '{0:.2f}'.format(time.time()) + ': ' + str(message))


class MashUtils:

    def __init__(self, config):
        self.scratch = os.path.abspath(config['scratch'])

    def mash_dist_runner(self, file_path, search_db):
        output_file_name = "outfile"
        dist_search_command = ['/kb/module/mash-Linux64-v2.0/mash', 'dist', search_db,
                               file_path, "| sort -gk3 >", output_file_name]
        self._run_command(' '.join(dist_search_command))
        return output_file_name

    def parse_search_results(self, results_path, maxcount):
        id_to_similarity = {}

        with open(results_path, 'rb') as fh:
            csvfile = csv.reader(fh, delimiter='\t')
            count = 0
            for line in csvfile:
                if count >= maxcount:
                    break
                id_to_similarity[line[0]] = float(line[2])
                count += 1
        return id_to_similarity

    def _run_command(self, command):
        """
        _run_command: run command and print result
        """

        log('Start executing command:\n{}'.format(command))
        pipe = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        output = pipe.communicate()[0]
        exitCode = pipe.returncode

        if (exitCode == 0):
            log('Executed command:\n{}\n'.format(command) +
                'Exit Code: {}\nOutput:\n{}'.format(exitCode, output))
        else:
            error_msg = 'Error running command:\n{}\n'.format(command)
            error_msg += 'Exit Code: {}\nOutput:\n{}'.format(exitCode, output)
            raise ValueError(error_msg)

    def _mkdir_p(self, path):
        """
        _mkdir_p: make directory for given path
        """
        # https://stackoverflow.com/a/600612/643675
        if not path:
            return
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise
