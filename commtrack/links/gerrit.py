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

        if 'change_id' in self.params:
            query_cmd.append('change:{}'.format(self.params['change_id']))

        if 'subject' in self.params:
            query_cmd.append(self.params['subject'])

        output = subprocess.check_output(query_cmd)
        decoded_output = output.decode('utf-8')
        query_result_li = decoded_output.split('\n')

        # Handle multiple matches
        if len(query_result_li) > 1 and self.chain_params['global']['commit']:
            LOG.info(exc.multiple_matches())
            sys.exit(2)

        # return json.loads(query_result_li)
        return query_result_li

    def search(self, same_project=True):
        """Returns the result of searching the given change."""
        self.verify_and_set_reqs(const.REQUIRED_PARAMS)
        raw_result_li = self.query()

        # Check if there is at least one result
        if len(raw_result_li) < 3:
            self.results.append("{} find such change.".format(crayons.red("Couldn't")))
        else:
            self.params['found'] = True

        json_result_li = []
        for res in raw_result_li:
            if 'type' not in res and res != '':
                json_result_li.append(json.loads(res))
        if len(json_result_li) > 1:
            same_project = self.verify_same_project(json_result_li)
        if same_project:
            for result in json_result_li:
                self.update_link_params(result)
                self.results.append(self.process_result(result))
        else:
            LOG.error(exc.multiple_projects())
            sys.exit(2)

        return self.params

    def verify_same_project(self, changes):
        """Returns true if all the changes belong to the same project."""
        project = changes[0]['project']
        for change in changes[1:]:
            if change['project'] != project:
                return False
        return True

    def update_link_params(self, data):
        """Update link parameters using data discovered during the query."""
        for param in const.SINGLE_PROVIDED_PARAMS:
            if param in data:
                self.params[param] = data[param]
        for param in const.MULTI_PROVIDED_PARAMS:
            if param in data:
                if param not in self.params:
                    self.params[param] = list()
                self.params[param].append(data[param])

    def process_result(self, data):
        """Returns adjusted result with only the relevant information."""
        result_str = "Status in project {} branch {} is {}".format(
            data['project'],
            data['branch'],
            self.colorize_result(data['status']))

        return result_str

    def colorize_result(self, status):
        return const.COLORED_STATS[status]
