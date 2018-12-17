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

from commtrack.constants import gerrit as constants

LOG = logging.getLogger(__name__)


class Gerrit(object):
    """Managing operations on Gerrit Code review system."""

    def __init__(self):
        pass

    def get_basic_query_cmd(self, address):
        """Returns a very basic query command which extended based

        on provided input from the user.
        """
        return ['ssh', '-p', '29418',
                address.strip('\"'),
                'gerrit', 'query',
                'limit:5',
                '--format JSON']

    def query(self, address, params):
        """Returns query result"""

        query_cmd = self.get_basic_query_cmd(address)

        if params['change']:
            query_cmd.append('change:{}'.format(params['change']))

        output = subprocess.check_output(query_cmd)

        data = output.decode('ascii')
        json_data = json.loads(data.split('\n')[0])
        return json_data

    def search(self, address, params):
        """Returns the result of searching the given change."""
        result = self.query(address, params)
        if result['project']:
            status = self.colorize_result(result['status'])
            return status
        return None

    def colorize_result(self, status):
        return constants.COLORED_STATS[status]
