import time
import os
import uuid
import errno

from AssemblyUtil.AssemblyUtilClient import AssemblyUtil
from AssemblyUtil.baseclient import ServerError as AssemblyUtilError

def log(message, prefix_newline=False):
    """
    Logging function, provides a hook to suppress or redirect log messages.
    """
    print(('\n' if prefix_newline else '') + '{0:.2f}'.format(time.time()) + ': ' + str(message))


class KBObjectUtils:

    def __init__(self, config):
        self.scratch = os.path.abspath(config['scratch'])
        self.tmp = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(self.tmp)
        self.callbackURL = os.environ['SDK_CALLBACK_URL']

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

    def stage_assembly_files(self, object_list):
        """
        _stage_assembly_files: download the fasta files to the scratch area
        return list of file names
        """
        log('Processing assembly object list: {}'.format(object_list))

        auc = AssemblyUtil(self.callbackURL)
        staged_file_list = []

        for assembly_upa in object_list:
            try:
                filename = auc.get_assembly_as_fasta({'ref': assembly_upa})['path']
            except AssemblyUtilError as assembly_error:
                print(str(assembly_error))
                raise

            staged_file_list.append(filename)

        log('Created file list: {}'.format(staged_file_list))
        return staged_file_list
