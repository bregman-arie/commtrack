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

LOG = logging.getLogger(__name__)


class Link(object):

    def __init__(self, name, address, ltype, parameters):
        self.name = name
        self.address = address
        self.ltype = ltype.lower()
        self.chain_params = parameters
        self.params = dict()
        self.plugin = importlib.import_module(
            "commtrack.plugins.{}".format(self.chain_params['plugin']))
        self.results = []

    def print_results(self):
        LOG.info("\n{} link search results:\n".format(
            crayons.yellow(self.name, bold=True)))
        for result in self.results:
            LOG.info(result)

    def verify_requirements(self, required_params):
        for param in required_params:
            if not self.chain_params[param]:
                print(common_exc.missing_requirements(param))
                sys.exit(2)
