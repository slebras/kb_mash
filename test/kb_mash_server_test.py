# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import requests
import shutil

from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint  # noqa: F401

from biokbase.workspace.client import Workspace as workspaceService
from kb_mash.kb_mashImpl import kb_mash
from kb_mash.kb_mashServer import MethodContext
from kb_mash.authclient import KBaseAuth as _KBaseAuth
from AssemblyUtil.AssemblyUtilClient import AssemblyUtil

class kb_mashTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('kb_mash'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'kb_mash',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL)
        #suffix = int(time.time() * 1000)
        #wsName = "test_kb_mash_" + str(suffix)
        #cls.ws_info = cls.wsClient.create_workspace({'workspace': wsName})
        cls.serviceImpl = kb_mash(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        #cls.au = AssemblyUtil(os.environ['SDK_CALLBACK_URL'])
        #cls.setup_data()

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def get_genome_ref(self):
        if hasattr(self.__class__, 'genomeInfo'):
            return self.__class__.genomeInfo
        au = AssemblyUtil(os.environ['SDK_CALLBACK_URL'])
        tf = 'ecoliMG1655.fa'
        target = os.path.join(self.scratch, tf)
        shutil.copy('data/' + tf, target)
        self.__class__.genomeInfo = au.save_assembly_from_fasta({'file': {'path': target},
                                                   'workspace_name': self.getWsName(),
                                                   'assembly_name': 'ecoliMG1655'})
        return self.__class__.genomeInfo

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        if hasattr(self.__class__, 'wsName'):
            return self.__class__.wsName
        suffix = int(time.time() * 1000)
        wsName = "test_kb_mash_" + str(suffix)
        ret = self.getWsClient().create_workspace({'workspace': wsName})  # noqa
        self.__class__.wsName = wsName
        return wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    @unittest.skip('skip')
    def test_your_method(self):
        # Prepare test objects in workspace if needed using
        # self.getWsClient().save_objects({'workspace': self.getWsName(),
        #                                  'objects': []})
        #
        # Run your method by
        # ret = self.getImpl().your_method(self.getContext(), parameters...)
        #
        # Check returned data with
        # self.assertEqual(ret[...], ...) or other unittest methods
        pass

    @unittest.skip('skip')
    def test_mash_search(self):
        params = {'input_assembly_upa': self.get_genome_ref(), 'workspace_name': self.getWsName(),
                  'search_db': 'KBaseRefseq', 'max_hits': 100}
        self.getImpl().run_mash_dist_search(self.getContext(), params)

    def test_mash_sketch_valid(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        params = {'fasta_path': os.path.join(dir_path, 'data', 'ecoliMG1655.fa')}
        self.getImpl().run_mash_sketch(self.getContext(), params)
        output_path = os.path.join(dir_path, 'data', 'ecoliMG1655.fa.msh')
        with open(output_path, 'rb') as output_file:
            num_lines = sum(1 for line in output_file)
        self.assertTrue(os.path.exists(output_path))
        self.assertEqual(num_lines, 103)
