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


def multiple_matches():
    """Display message about multiple query matches in Gerrit."""
    message = """
Found multiple matches for the commit you specified.
Try perhaps switching to change ID instead of commit:

    $ {0}

""".format(crayons.red("commtrack --changeid xyz"))
    return message
