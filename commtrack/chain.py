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
from configparser import ConfigParser
import crayons
import logging
import os
import sys

from commtrack.link import Link
from commtrack.constants.links import LINKS
from commtrack.constants.chain import CHAIN_LOCATIONS
from commtrack.exceptions.usage import missing_link

LOG = logging.getLogger(__name__)


class Chain(object):

    def __init__(self, change, links=None, chain_f=None):
        self.change = change
        self.chain_f = chain_f
        self.load_all_links()
        # Links can be provided via the configuration file
        # If provided by CLI they override file 'links'
        if links:
            self.links = self.get_links(links)

    def load_all_links(self):
        """Loads links from different sources."""
        self.available_links = dict()
        self.load_predefined_links()
        self.load_links_from_file()

    def load_predefined_links(self):
        """Loads links defined in the project."""
        for link in LINKS:
            self.add_link(link['name'], link['address'], link['type'])
        LOG.debug("Loaded predefined links.")

    def load_links_from_file(self):
        """Loads links from a file describing a chain"""
        chain_f = self.chain_f or self.locate_chain_file()
        if chain_f:
            cfg = ConfigParser()
            cfg.read(chain_f)

            for section in cfg.sections():
                for link in cfg.options(section):
                    if link != 'links':
                        self.add_link(link, cfg.get(section, link),
                                      section)

            links = cfg['DEFAULT']['links'].split(',')
            self.links = self.get_links(links)
            LOG.debug("Loaded links from: {}".format(chain_f))

    def get_links(self, links):
        """Returns list of link objects based on given links names."""
        links_li = []
        for link in list(links):
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
            link.search(change=self.change)

    def generate_summary(self):
        """Outputs summary of the search for each link in the chain."""
        LOG.info("============ Summary ================\n")

        LOG.info("Tracked Change ID {}\n".format(self.change))
        for link in self.links:
            LOG.info("{}: {}".format(link.name, link.result))

    @staticmethod
    def locate_chain_file():
        """Locates chain file."""
        for chain_loc in CHAIN_LOCATIONS:
            if os.path.isfile(chain_loc):
                return chain_loc
