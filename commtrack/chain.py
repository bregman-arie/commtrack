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
import logging
import os
import sys

from commtrack.link import Link
from commtrack.constants.links import LINKS

LOG = logging.getLogger(__name__)


class Chain(object):

    def __init__(self, links={}, chain_f=None):
        self.links = links
        self.chain_f = chain_f
        self.load_links()

    def load_links(self):
        """Loads links from different sources."""
        self.load_predefined_links()
        self.load_links_from_file()

    def load_predefined_links(self):
        """Loads links defined in the project."""
        for link in LINKS:
            self.add_link(link['name'], link['address'], link['type'])
        LOG.debug("Loaded predefined links.")
        print(self.links)

    def load_links_from_file(self):
        """Loads links from a file describing a chain"""
        chain_f = self.chain_f or self.locate_chain_file()
        if chain_f:
            cfg = ConfigParser()
            cfg.read(chain_f)
            self.order = cfg['DEFAULT']['chain'].split(',')

            for section in cfg.sections():
                for link in cfg.options(section):
                    if link != 'chain':
                        self.add_link(link, cfg.get(section, link),
                                      section)
            LOG.debug("Loaded links from: {}".format(chain_f))

    def add_link(self, name, address, ltype):
        self.links[name] = Link(name, address, ltype)

    def run(self, commit):
        """Runs chain link by link based on order attribute."""
        for link in self.order:
            LOG.info("Found commit in {}".format(link))

    @staticmethod
    def locate_chain_file():
        """Locates chain file."""
        if os.path.isfile('.chain'):
            return '.chain'
        elif os.path.isfile('/etc/commtrack/chain'):
            return '/etc/commtrack/chain'
        else:
            LOG.info("Unable to find chain file...exiting")
            sys.exit(2)
