# -*- coding: utf-8 -*-
############################################################
#
# Autogenerated by the KBase type compiler -
# any changes made here will be overwritten
#
############################################################

from __future__ import print_function
# the following is a hack to get the baseclient to import whether we're in a
# package or not. This makes pep8 unhappy hence the annotations.
try:
    # baseclient and this client are in a package
    from .baseclient import BaseClient as _BaseClient  # @UnusedImport
except:
    # no they aren't
    from baseclient import BaseClient as _BaseClient  # @Reimport


class kb_mash(object):

    def __init__(
            self, url=None, timeout=30 * 60, user_id=None,
            password=None, token=None, ignore_authrc=False,
            trust_all_ssl_certificates=False,
            auth_svc='https://kbase.us/services/authorization/Sessions/Login'):
        if url is None:
            raise ValueError('A url is required')
        self._service_ver = None
        self._client = _BaseClient(
            url, timeout=timeout, user_id=user_id, password=password,
            token=token, ignore_authrc=ignore_authrc,
            trust_all_ssl_certificates=trust_all_ssl_certificates,
            auth_svc=auth_svc)

    def run_mash_dist_search(self, params, context=None):
        """
        :param params: instance of type "MashParams" (Insert your typespec
           information here.) -> structure: parameter "input_assembly_upa" of
           String, parameter "workspace_name" of String, parameter
           "search_db" of String, parameter "max_hits" of Long
        :returns: instance of type "MashResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        return self._client.call_method(
            'kb_mash.run_mash_dist_search',
            [params], self._service_ver, context)

    def run_mash_sketch(self, params, context=None):
        """
        :param params: instance of type "MashSketchParams" -> structure:
           parameter "fasta_path" of String
        :returns: instance of type "MashSketchResults" -> structure:
           parameter "sketch_path" of String
        """
        return self._client.call_method(
            'kb_mash.run_mash_sketch',
            [params], self._service_ver, context)

    def status(self, context=None):
        return self._client.call_method('kb_mash.status',
                                        [], self._service_ver, context)
