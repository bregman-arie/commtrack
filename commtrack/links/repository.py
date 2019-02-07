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
from bs4 import BeautifulSoup
import logging
import re
import requests
import urllib.parse


from commtrack.repository import constants as repo_const
from commtrack.common import constants as const
from commtrack.link import Link

LOG = logging.getLogger(__name__)


class Repository(Link):
    """Repository Link."""

    def __init__(self, name, address, parameters):
        super(Repository, self).__init__(name, address,
                                         repo_const.LINK_TYPE, parameters)

    def check_if_package_exists(self, branch, version):
        """Returns True if package exists in the given version."""
        address_suffix = self.plugin.BRANCH_MAP[self.ltype][branch]

        # urljoin will drop part of the address if '/' is not presented
        if not (self.address).endswith('/'):
            self.address = self.address + '/'

        full_address = urllib.parse.urljoin(self.address, address_suffix)
        resp = requests.get(full_address)
        soup = BeautifulSoup(resp.text, 'html.parser')

        for a in soup.find_all('a'):
            for sep in const.PROJECT_SEPARATORS:
                project_name = self.params['project'].split(sep)[-1]
                if project_name in a.get('href'):
                    name_re = re.search(r'(^[a-zA-z0-9\-]*)\-\d', a.get('href'))
                    name = name_re.group(1)
                    print(name)
                    if project_name == name:
                        print(a.get('href'))

    def search(self):
        self.verify_and_set_reqs(repo_const.REQUIRED_PARAMS)
        for branch, tag in self.params['tags'].items():
            self.check_if_package_exists(branch, tag)
