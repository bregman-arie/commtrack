# Copyright 2019 Arie Bregman
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import crayons
import importlib
import logging
import sys

from commtrack.common import exceptions as common_exc
from commtrack.exceptions.usage import general_usage

LOG = logging.getLogger(__name__)


class Link(object):

    def __init__(self, name, address, ltype, parameters):
        self.name = name
        self.address = address
        self.ltype = ltype.lower()
        self.chain_params = parameters
        self.params = dict()
        self.plugin = importlib.import_module(
            "commtrack.plugins.{}".format(
                self.chain_params['global']['plugin']))
        self.results = []

    def print_results(self):
        LOG.info("\n{} link search results:\n".format(
            crayons.yellow(self.name, bold=True)))
        for result in self.results:
            LOG.info(result)

    def check_param_is_defined(self, param):
        for k, v in self.chain_params.items():
            if param in v and v[param]:
                self.params[param] = v[param]
                return True

    def verify_at_least_one_provided(self, params):
        one_defined = False
        for param in params:
            exists = self.check_param_is_defined(param)
            if exists:
                one_defined = True
        if not one_defined:
            LOG.error(common_exc.provide_at_least_one_param(self.name, params))
            LOG.error(general_usage())
            sys.exit(2)

    def verify_and_set_reqs(self, required_params):
        """Sets mandatory parameters required by the link to perform

        successful search.
        """
        for param in required_params:
            if isinstance(param, list):
                self.verify_at_least_one_provided(param)
            else:
                exists = self.check_param_is_defined(param)
                if not exists:
                    LOG.error(common_exc.missing_requirements(param))
                    LOG.error(general_usage())
                    sys.exit(2)

    def set_parameters(self, params):
        self.chain_params = params

    def __str__(self):
        link = "{}\nLink: {}\nAddress: {}\nType: {}".format(
            '-' * 6, self.name, self.address, self.ltype)
        return link
