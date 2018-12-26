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
import sys

from commtrack.gerrit import constants as const
from commtrack.gerrit import exceptions as exc
from commtrack.link import Link

LOG = logging.getLogger(__name__)


class Gerrit(Link):
    """Managing operations on Gerrit Code review system."""

    def __init__(self, name, address, parameters):
        super(Gerrit, self).__init__(name, address,
                                     const.LINK_TYPE, parameters)

    def get_basic_query_cmd(self, address):
        """Returns a very basic query command which extended based

        on provided input from the user.
        """
        return ['ssh', '-p', '29418',
                address.strip('\"'),
                'gerrit', 'query',
                'limit:5',
                '--format JSON']

    def query(self):
        """Returns query result"""

        query_cmd = self.get_basic_query_cmd(self.address)

        if self.chain_params['global']['change_id']:
            query_cmd.append('change:{}'.format(self.chain_params['global']['change_id']))

        output = subprocess.check_output(query_cmd)
        decoded_output = output.decode('utf-8')
        query_result_li = decoded_output.split('\n')

        # Handle multiple matches
        if len(query_result_li) > 1 and self.chain_params['global']['commit']:
            LOG.info(exc.multiple_matches())
            sys.exit(2)

        # return json.loads(query_result_li)
        return query_result_li

    def search(self):
        """Returns the result of searching the given change."""
        self.verify_and_set_reqs(const.REQUIRED_PARAMS)
        raw_result_li = self.query()

        for res in raw_result_li:
            if 'type' not in res and res != '':
                self.update_link_params(res)
                self.results.append(self.process_result(res))

        return self.params

    def update_link_params(self, raw_data):
        """Update link parameters using data discovered during the query."""
        data = json.loads(raw_data)
        for param in const.SINGLE_PROVIDED_PARAMS:
            if param in data:
                self.params[param] = data[param]
        for param in const.MULTI_PROVIDED_PARAMS:
            if param in data:
                if param not in self.params:
                    self.params[param] = list()
                self.params[param].append(data[param])

    def process_result(self, result):
        """Returns adjusted result with only the relevant information."""
        data = json.loads(result)

        result_str = "Status in project {} branch {} is {}".format(
            data['project'],
            data['branch'],
            self.colorize_result(data['status']))

        return result_str

    def colorize_result(self, status):
        return const.COLORED_STATS[status]
