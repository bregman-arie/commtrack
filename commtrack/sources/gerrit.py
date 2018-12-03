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
import json
import logging
import subprocess

LOG = logging.getLogger(__name__)


class Gerrit(object):
    """Managing operations on Gerrit Code review system."""

    def __init__(self):
        pass

    def query(self, address, change):
        """Returns query result,"""
        d = subprocess.check_output([
            'ssh', '-p', '29418',
            address.strip('\"'),
            'gerrit', 'query',
            'limit:5',
            'change:{}'.format(change),
            '--format JSON'])

        data = d.decode('ascii')
        json_data = json.loads(data.split('\n')[0])
        return json_data

    def search(self, address, commit):
        """Returns the result of searching the given change."""
        result = self.query(address, commit)
        if result['project']:
            return result['status']
