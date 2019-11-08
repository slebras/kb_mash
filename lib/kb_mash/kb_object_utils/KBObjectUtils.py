import time
import os
import uuid
import errno
import operator
from jinja2 import Environment, PackageLoader, select_autoescape

from KBaseReport.KBaseReportClient import KBaseReport
from KBaseReport.baseclient import ServerError as _RepError
from AssemblyUtil.AssemblyUtilClient import AssemblyUtil
from AssemblyUtil.baseclient import ServerError as AssemblyUtilError
from Workspace.WorkspaceClient import Workspace as _Workspace
from DataFileUtil.DataFileUtilClient import DataFileUtil as _DFUClient
from DataFileUtil.baseclient import ServerError as _DFUError

def log(message, prefix_newline=False):
    """
    Logging function, provides a hook to suppress or redirect log messages.
    """
    print(('\n' if prefix_newline else '') + '{0:.2f}'.format(time.time()) + ': ' + str(message))


env = Environment(loader=PackageLoader('kb_mash','kb_object_utils/templates'),
                  autoescape=select_autoescape(['html']))

class KBObjectUtils:

    KBASE_DBS = {'KBaseRefseq'}

    def __init__(self, config):
        self.scratch = os.path.abspath(config['scratch'])
        self.tmp = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(self.tmp)
        self.callbackURL = os.environ['SDK_CALLBACK_URL']
        self.ws_url = config['workspace-url']
        self.dfu = _DFUClient(self.callbackURL)
        self.ws = _Workspace(self.ws_url)

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

    def get_upa_names(self, upas):
        """"""
        resp = self.ws.get_objects2({'objects': upas, 'no_data': 1})
        return [
            {
                'name': obj['info'][1],
                'upa': str('/'.join(
                    [str(obj['info'][6]), str(obj['info'][0]), str(obj['info'][4])]
                ))
            }
            for obj in resp['data']
        ]

    def input_upa_parse(self, upa):

        obj_data = self.dfu.get_objects({"object_refs":[upa]})['data'][0]
        obj_type  = obj_data['info'][2]
        name = obj_data['info'][1]
        gs_obj = obj_data['data']

        if 'KBaseSets.GenomeSet' in obj_type:
            upas = self.get_upa_names([{'ref': gsi['ref']} for gsi in gs_obj['items']])
        elif 'KBaseSearch.GenomeSet' in obj_type:
            upas = self.get_upa_names([{'ref': gse['ref']} for gse in gs_obj['elements'].values()])
        elif "KBaseGenomes.ContigSet" in obj_type or "KBaseGenomeAnnotations.Assembly" in obj_type or "KBaseGenomes.Genome" in obj_type:
            upas = [{'upa': upa, 'name': name}]
        else:
            raise TypeError("provided input must of type 'KBaseSets.GenomeSet','KBaseSearch.GenomeSet','KBaseGenomes.ContigSet','KBaseGenomeAnnotations.Assembly' or 'KBaseGenomes.Genome' not " +str(obj_type))        
        return upas

    def _to_upa(self, objinfo, sep='/'):
        return str(objinfo[6]) + sep + str(objinfo[0]) + sep + str(objinfo[4])

    def create_search_report(self, wsname, query_results, multi):

        outdir = os.path.join(self.tmp, 'search_report')
        self._mkdir_p(outdir)

        if multi:
            template = env.get_template("index_multi.html")
        else:
            template = env.get_template("index.html")
        html_output = template.render(results=query_results)
        with open(os.path.join(outdir,'index.html'), 'w') as f:
            f.write(html_output)

        log('Saving Mash search report')

        html_link = {
            'path':outdir,
            'name':'index.html',
            'description': 'Mash html report'
        }

        try:
            report = KBaseReport(self.callbackURL)
            return report.create_extended_report({
                'direct_html_link_index':0,
                'html_links':[html_link],
                'workspace_name': wsname,
                'report_object_name':'kb_mash_report_' + str(uuid.uuid4())
            })
        except _RepError as re:
            log('Logging exception from creating report object')
            log(str(re))
            # TODO delete shock node
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
