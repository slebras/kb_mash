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

    def sketch_service_query(self, input_upas, n_max_results, search_db):
        '''Query assembly homology service to leverage its caching and mash implementation

        params:
            input_upa - reference to assembly or genome
            n_max_results - number of results to return
            search_db - string to specify search database
        '''
        # get current sketch_service url from service wizard
        sketch_url = self.get_sketch_service_url_with_service_wizard()
        results = []
        for upa in input_upas:
            payload = {
                "method":"get_homologs",
                "params":{
                    'ws_ref':upa,
                    'n_max_results':n_max_results,
                    'search_db': search_db
                }
            }

            resp = requests.post(url=sketch_url, data=json.dumps(payload),headers={
                'content-type':"application/json-rpc",'Authorization':self.auth_token})

            if len(input_upas) == 1:
                results = self.parse_results(resp.json())
            else:
                curr = self.parse_results(resp.json(), input_name=upa)
                results += curr

        return results

    def parse_results(self, results_data, input_name=None):
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

        results = []
        distances = results_data['result']['distances']
        # id_to_similarity, id_to_upa, id_to_sciname, id_to_strain = {}, {}, {}, {}
        for d in distances:
            curr = {}
            curr['Id'] = d['sourceid']
            sciname = ""
            if d.get('sciname'):
                sciname += d['sciname']
            if d.get('kbase_id'):
                curr['item_link'] = "/#dataview/" + d['kbase_id']
            else:
                curr['item_link'] = ""
            if d.get('strain'):
                sciname = sciname + " " + d['strain']
            curr['sciname'] = sciname
            curr['dist'] = float(d['dist'])
            if input_name != None:
                curr['input_name'] = input_name
            results.append(curr)
            # id_to_similarity[d['sourceid']] = float(d['dist'])
            # if d.get('sciname'):
            #     id_to_sciname[d['sourceid']] = d['sciname']
            # if d.get('kbase_id'):
            #     id_to_upa[d['sourceid']] = d['kbase_id']
            # if d.get('strain'):
            #     id_to_strain[d['sourceid']] = d['strain']

        return results

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
        for id_ in resp:
            mappings = resp[id_]["mappings"]
            # default upa is no upa
            id_to_upa[id_] = ""
            for mapping in mappings:
                if mapping['ns'] == "KBase":
                    id_to_upa[id_] = mapping['id']
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
