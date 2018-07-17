# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os
from kb_mash.kb_object_utils.KBObjectUtils import KBObjectUtils
from kb_mash.mash_utils.MashUtils import MashUtils
#END_HEADER


class kb_mash:
    '''
    Module Name:
    kb_mash

    Module Description:
    A KBase module: kb_mash
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = ""
    GIT_COMMIT_HASH = "a7f618e7aefaf545f91b078f142e0583d2f9a3b8"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.config = config
        self.scratch = os.path.abspath(config['scratch'])
        self.callbackURL = os.environ['SDK_CALLBACK_URL']
        self.SEARCH_DBS = {'Ecoli': '/kb/module/test/data/ecolidb.msh',
                           'KBaseRefseq': '/data/kb_refseq_ci.msh'}
        #END_CONSTRUCTOR
        pass


    def run_mash_dist_search(self, ctx, params):
        """
        :param params: instance of type "MashParams" (Insert your typespec
           information here.) -> structure: parameter "input_assembly_upa" of
           String, parameter "workspace_name" of String, parameter
           "search_db" of String, parameter "max_hits" of Long
        :returns: instance of type "MashResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: results
        #BEGIN run_mash_dist_search

        params['max_hits'] = 200

        os.chdir(self.scratch)
        kb_obj_helper = KBObjectUtils(self.config)
        [file_list] = kb_obj_helper.stage_assembly_files([params['input_assembly_upa']])
        print(file_list)
        mash_helper = MashUtils(self.config)
        outfile = mash_helper.mash_dist_runner(file_list, self.SEARCH_DBS[params['search_db']])
        id_to_similarity = mash_helper.parse_search_results(outfile, params['max_hits'])
        report = kb_obj_helper.create_search_report(params['workspace_name'], id_to_similarity, params['search_db'])

        results = {'report_name': report['name'], 'report_ref': report['ref']}
        #END run_mash_dist_search

        # At some point might do deeper type checking...
        if not isinstance(results, dict):
            raise ValueError('Method run_mash_dist_search return value ' +
                             'results is not type dict as required.')
        # return the results
        return [results]

    def run_mash_sketch(self, ctx, params):
        """
        :param params: instance of type "MashSketchParams" -> structure:
           parameter "fasta_path" of String
        :returns: instance of type "MashSketchResults" -> structure:
           parameter "sketch_path" of String
        """
        # ctx is the context object
        # return variables are: results
        #BEGIN run_mash_sketch
        assert params.get('fasta_path'), 'must provide a path to a fasta file'
        mash_utils = MashUtils(self.config)
        output_file_path = mash_utils.mash_sketch(params['fasta_path'])
        results = {'sketch_path': output_file_path}
        #END run_mash_sketch

        # At some point might do deeper type checking...
        if not isinstance(results, dict):
            raise ValueError('Method run_mash_sketch return value ' +
                             'results is not type dict as required.')
        # return the results
        return [results]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
