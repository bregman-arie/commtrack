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
import logging
import os
import sys
import yaml

from commtrack.link import Link
from commtrack.constants.links import LINKS
from commtrack.constants.chain import CHAIN_LOCATIONS
from commtrack.exceptions.usage import missing_link

LOG = logging.getLogger(__name__)


class Chain(object):

    def __init__(self, parameters):
        self.parameters = parameters
        if 'links' in self.parameters:
            self.links = [item for item in self.parameters['links'].split(',')]
        self.available_links = self.get_predefined_links()
        # Links can be provided via the configuration file
        # If provided by CLI they override the links provided via file.
        self.load_links_from_file(self.links)
        if self.links:
            self.links = self.get_link_instances(self.links)

    def get_predefined_links(self):
        """Loads links defined in the project."""
        links = dict()
        for link in LINKS:
            links[link['name']] = Link(
                link['name'], link['address'], link['type'])
        return links

    def load_links_from_file(self, ignore_chain):
        """Loads links from a file describing a chain"""
        chain_f = self.parameters['chain_file'] or self.locate_chain_file()
        chain = None
        if chain_f:
            with open(chain_f, 'r') as stream:
                data = yaml.load(stream)
                for k, v in data.items():
                    if k == 'chain' and not ignore_chain:
                        chain = v
                    if k == 'links':
                        for link_type, link in v.items():
                            for link_name, info in link.items():
                                self.add_link(link_name,
                                              info['address'],
                                              link_type)
            if chain:
                self.links = self.get_link_instances(chain)
            LOG.debug("Loaded data from: {}".format(chain_f))

    def get_link_instances(self, links):
        """Returns list of link objects based on given links names."""
        links_li = []
        # Handle cases where links passed as list or string
        links_data = links if isinstance(links, (list,)) else links.split()
        for link in links_data:
            try:
                links_li.append(self.available_links[link])
            except KeyError:
                LOG.info(missing_link(link))
                sys.exit(2)
        return links_li

    def add_link(self, name, address, ltype):
        self.available_links[name] = Link(name, address, ltype)

    def run(self):
        """Runs chain link by link."""
        for link in self.links:
            LOG.info("Looking in {}".format(crayons.yellow(link.name)))
            params = link.search(self.parameters)
            self.parameters.update(params)

    def generate_summary(self):
        """Outputs summary of the search for each link in the chain."""
        LOG.info("============ Summary ================\n")
        LOG.info("Tracked Change ID {}\n".format(self.change))

        for link in self.links:
            link.print_results()

    @staticmethod
    def locate_chain_file():
        """Locates chain file."""
        for chain_loc in CHAIN_LOCATIONS:
            if os.path.isfile(chain_loc):
                return chain_loc
