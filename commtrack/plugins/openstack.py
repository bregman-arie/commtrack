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

BRANCH_MAP = {'git':
              {'master': 'rhos-14.0-patches',
               'stable/pike': 'rhos-12.0-patches',
               'stable/queens': 'rhos-13.0-patches',
               'stable/rocky': 'rhos-14.0-patches',
               'stable/ocata': 'rhos-11.0-patches'},
              'distgit':
              {'master': 'rhos-14.0-patches',
               'stable/pike': 'rhos-12.0-patches',
               'stable/queens': 'rhos-13.0-patches',
               'stable/rocky': 'rhos-14.0-patches',
               'stable/ocata': 'rhos-11.0-patches'},
              }

REPLACE_CHARS = {'distgit': [('/', '-')]}
