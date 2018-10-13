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
import logging
import os
import sys

LOG = logging.getLogger(__name__)


class Chain(object):

    def __init__(self):
        links = self.load_chain()
        print(links)

    def load_chain(self):
        """Loads chain as provided by the user."""
        chain_f = self.find_chain_file()
        print(chain_f)

    def find_chain_file(self):
        """Locate chain file."""
        if os.path.isfile('.chain'):
            return '.chain'
        elif os.path.isfile('/etc/commtrack/chain'):
            return '/etc/commtrack/chain'
        else:
            LOG.info("Unable to find chain file...exiting")
            sys.exit(2)
