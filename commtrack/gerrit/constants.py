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

# Note that order is very important since it determines which
# chain file will be used first in case of multiple matches.
import crayons

COLORED_STATS = {'MERGED': crayons.green('Merged'),
                 'NEW': crayons.blue('In Review'),
                 'missing': crayons.red('Not Found')}

SINGLE_PROVIDED_PARAMS = ['id', 'project', 'subject']
MULTI_PROVIDED_PARAMS = ['branch']

PORT = 29418

LINK_TYPE = 'Gerrit'

REQUIRED_PARAMS = [['change_id', 'commit', 'subject']]
