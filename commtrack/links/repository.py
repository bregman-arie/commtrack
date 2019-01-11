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


from commtrack.repository import constants as const
from commtrack.link import Link

LOG = logging.getLogger(__name__)


class Repository(Link):
    """Repository Link."""

    def __init__(self, name, address, parameters):
        super(Repository, self).__init__(name, address,
                                         const.LINK_TYPE, parameters)

    def check_if_package_exists(self, version):
        """Returns True if package exists in the given version."""
        resp = requests.get(self.address)
        soup = BeautifulSoup(resp.text, 'html.parser')
        for tr in soup.find_all('tr'):
            print(tr)
            if tr.a:
                name = re.search(r'(^[a-zA-z0-9\-]*)\-\d', tr.a.get('href'))
                print(name)

    def search(self):
        self.verify_and_set_reqs(const.REQUIRED_PARAMS)
        for tag in self.params['tags']:
            self.check_if_package_exists(tag)
