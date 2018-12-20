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
from os.path import expanduser

HOME_DIR = expanduser("~")

PROJECT_PATHS = [HOME_DIR, HOME_DIR + '/commtrack',
                 HOME_DIR + '/git', '/tmp/git']

DEFAULT_PATH = PROJECT_PATHS[0]

LINK_TYPE = 'Git'

CLONE_CMD = ['git', 'clone']

LS_REMOTE_CMD = ['git', 'ls-remote']

DEFAULT_CLONE_PATH = '~'

PROJECT_SEPARATORS = ['.', '/']

COLORED_STATS = {'merged': crayons.green('Merged'),
                 'missing': crayons.red('Missing')}

REQUIRED_PARAMS = ['project', 'branch']
