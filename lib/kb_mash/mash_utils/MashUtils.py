import time
import os
# import errno
import json
import subprocess
import csv
import requests


def log(message, prefix_newline=False):
    """
    Logging function, provides a hook to suppress or redirect log messages.
    """
    print(('\n' if prefix_newline else '') + '{0:.2f}'.format(time.time()) + ': ' + str(message))


mash_bin = '/kb/module/mash-Linux64-v2.0/mash'
# ahs_url  = 'https://homology.kbase.us/namespace/%s/search'

class MashUtils:

    def __init__(self, config, auth_token):
        self.scratch = os.path.abspath(config['scratch'])
        self.sw_url = config['srv-wiz-url']
        if config.get('id-mapper-url'):
            self.id_mapper_url = config['id-mapper-url']
        else:
            self.id_mapper_url = config['kbase-endpoint'] + "/idmapper/api/v1"
        self.auth_token = auth_token
        print(config)

    def mash_sketch(self, genome_file_path, paired_ends=False):
        """
        Generate a sketch file for a given fasta/fastq file path, saving the output to a tempfile.

        Documentation: http://mash.readthedocs.io/en/latest/tutorials.html
        """
        assert os.path.exists(genome_file_path), 'genome_file_path must exist'
        output_path = genome_file_path + '.msh'
        args = [mash_bin, 'sketch', genome_file_path, '-o', output_path]
        if paired_ends:
            # Sketch the reads using `-m 2` to improve results by ignoring single-copy k-mers, which
            # are more likely to be erroneous:
            args = args + ['-m', '2']
        self._run_command(' '.join(args))
        return output_path

    def get_sketch_service_url_with_service_wizard(self):
        '''
        '''
        payload = {
            "method":"ServiceWizard.get_service_status",
            "id":'',
            "params":[{"module_name":"sketch_service","version":"beta"}],
            "version":"1.1"
        }

        sw_resp  = requests.post(url=self.sw_url, data=json.dumps(payload))
        sketch_resp = sw_resp.json()
        if sketch_resp.get('error'):
            raise RuntimeError("ServiceWizard Error: " + sketch_resp['error'])
        sketch_url  = sketch_resp['result'][0]['url']

        return sketch_url

    def sketch_service_query(self, assembly_upa, n_max_results, search_db):
        '''Query assembly homology service to leverage its caching and mash implementation

        params:
            assembly_upa - reference to assembly 
            n_max_results - number of results to return
            search_db - string to specify search database
        '''
        payload = {
            "method":"get_homologs",
            "params":{
                'ws_ref':assembly_upa,
                'n_max_results':n_max_results,
                'search_db': search_db
            }
        }
        # get current sketch_service url from service wizard
        sketch_url = self.get_sketch_service_url_with_service_wizard()
        print("-------------------------")
        print("----------BLOOP----------")
        print("-------------------------")
        print("---sketch service url----"+sketch_url+'---')
        print("-------------------------")
        print("----------BLOOP----------")
        print("-------------------------")
        resp = requests.post(url=sketch_url, data=json.dumps(payload),headers={
            'content-type':"application/json-rpc",'Authorization':self.auth_token})

        return self.parse_results(resp.json())

    def parse_results(self, results_data):
        '''
        params:
            results_data: dictionary response from sketch_service
        '''
        if results_data.get('error'):
            raise RuntimeError("Sketch_service Error: " + results_data['error'])
        if not results_data.get('result'):
            raise ValueError("No results or results empty in JSON response body")
        if not results_data['result'].get('distances'):
            raise ValueError("No Distances in results JSON response")

        distances = results_data['result']['distances']
        id_to_similarity, id_to_upa = {}, {}
        for d in distances:
            id_to_similarity[d['sourceid']] = float(d['dist'])
            if d.get('kbase_id'):
                id_to_upa[d['sourceid']] = d['kbase_id']
        return id_to_similarity, id_to_upa

    def id_mapping_query(self, ids):
        """
        """
        payload = {
            "ids":ids
        }
        id_mapper_url = self.id_mapper_url + '/mapping/RefSeq'

        resp = requests.get(url=id_mapper_url, data=json.dumps(payload),\
                    headers={'content-type':"application/json-rpc",'Authorization':self.auth_token})
        return self.parse_mapper_response(resp.json())

    def parse_mapper_response(self, resp):
        """
        """
        if resp.get('error'):
            raise RuntimeError("ID Mapper Error: "+ str(resp.get('error', "unknown error")))

        id_to_upa = {}
        namespaces = set([])
        for id_ in resp:
            mappings = resp[id_]["mappings"]
            # default upa is no upa
            id_to_upa[id_] = ""
            for mapping in mappings:
                namespace = mapping['ns']
                namespaces.add(namespace)
                if namespace == "KBase":
                    id_to_upa[id_] = mapping['id']
        print("available response namespaces in the idmapping service:",namespaces)
        return id_to_upa

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
