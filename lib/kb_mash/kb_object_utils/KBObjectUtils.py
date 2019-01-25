import time
import os
import uuid
import errno
import operator

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


class KBObjectUtils:

    KBASE_DBS = {'KBaseRefseq'}

    def __init__(self, config):
        self.scratch = os.path.abspath(config['scratch'])
        self.tmp = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(self.tmp)
        self.callbackURL = os.environ['SDK_CALLBACK_URL']
        self.ws_url = config['workspace-url']

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

    def _create_link_mapping(self, id_to_upa):
        idmap = {}

        log('Looking up object names and scientific names in KBase data stores')
        wsrefs = []
        for x in id_to_upa.values():
            if x is not "":
                wsrefs.append({'ref':x})
        if len(ws_refs) > 0:
            ws = _Workspace(self.ws_url)
            # should really catch error and log here, later. Same below for taxa lookup
            objs = ws.get_objects2({'objects': wsrefs, 'no_data': 1})['data']
            upa_to_name = {}
            upa_to_taxon_upa = {}
            for o in objs:
                upa_ = self._to_upa(o['info'], '_')
                upa_to_name[upa_] = o['info'][1]
                upa_to_taxon_upa[upa_] = o['refs'][0]
            taxrefs = [{'ref': x} for x in upa_to_taxon_upa.values()]
            # 1) Really should use a reference path here, but since the taxons are public skip
            # 2) The taxon objects should have the scientific name in the metadata so the entire
            #    object doesn't need to be fetched. At least the taxa objects are small.
            # 3) Should use DFU for getting objects
            # 4) This code is a Very Bad Example of how to do things, basically
            upa_to_sci_name = {}
            taxobjs = ws.get_objects2({'objects': taxrefs})['data']
            for t in taxobjs:
                upa = self._to_upa(t['info'])
                upa_to_sci_name[upa] = t['data']['scientific_name']
            for id_ in id_to_upa.keys():
                upa = id_to_upa[id_]
                if upa == "":
                    idmap[id_] = {'id': '{} ({})'.format(
                                    upa_to_name[upa], upa_to_sci_name[upa_to_taxon_upa[upa]]),
                                'link': '/#dataview/' + upa.replace('_', '/')}

        return idmap

    def _to_upa(self, objinfo, sep='/'):
        return str(objinfo[6]) + sep + str(objinfo[0]) + sep + str(objinfo[4])

    def _write_search_results(self, outfile, id_to_similarity, id_to_link):
        # change to mustache or something later. Or just rewrite this whole thing since this is
        # a demo
        with open(outfile, 'w') as html_file:
            html_file.write('<html><body>\n')
            html_file.write('<div>Showing {} matches</div>\n'
                            .format(len(id_to_similarity)))
            html_file.write('<table>\n')
            html_file.write('<tr><th>ID</th><th>Minhash distance</th></tr>\n')
            for id_, similarity in sorted(
                    id_to_similarity.items(), key=operator.itemgetter(1), reverse=False):
                if id_ in id_to_link:
                    html_file.write(
                        '<tr><td><a href="{}" target="_blank">{}</a></td><td>{}</td>\n'.format(
                            id_to_link[id_]['link'], id_to_link[id_]['id'], similarity))
                else:
                    html_file.write('<tr><td>{}</td><td>{}</td>\n'.format(id_, similarity))
            html_file.write('</table>\n')
            html_file.write('</body></html>\n')

    def create_search_report(self, wsname, id_to_similarity, id_to_upa):

        outdir = os.path.join(self.tmp, 'search_report')
        self._mkdir_p(outdir)

        id_to_link = self._create_link_mapping(id_to_upa)

        self._write_search_results(
            os.path.join(outdir, 'index.html'), id_to_similarity, id_to_link)

        log('Saving Mash search report')

        dfu = _DFUClient(self.callbackURL)
        try:
            dfuout = dfu.file_to_shock({'file_path': outdir, 'make_handle': 0, 'pack': 'zip'})
        except _DFUError as dfue:
            # not really any way to test this block
            log('Logging exception loading results to shock')
            log(str(dfue))
            raise
        log('saved report to shock node ' + dfuout['shock_id'])
        try:
            kbr = KBaseReport(self.callbackURL)
            return kbr.create_extended_report(
                {'direct_html_link_index': 0,
                 'html_links': [{'shock_id': dfuout['shock_id'],
                                 'name': 'index.html',
                                 'label': 'Sourmash search results'}
                                ],
                 'report_object_name': 'kb_sourmash_report_' + str(uuid.uuid4()),
                 'workspace_name': wsname
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
