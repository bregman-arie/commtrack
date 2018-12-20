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


def general_usage():
    """Help message format."""
    message = """
Usage Examples:

    Track change ID:
    $ {0}

    Track commit in given links:
    $ {1}

    Specify additional parameters like project name:
    $ {2}

""".format(crayons.red("commtrack --changeid 23231"),
           crayons.red("commtrack --commit 2d4m2 --links openstack"),
           crayons.red("commtrack --changeid xyz --project neutron"),)
    return message


def missing_link(link):
    """Message on how to use links."""
    message = """
Couldn't find the link {0}.
Make sure link in configured in chain file the following way:

    {1}
      {2}
    {3}
    """.format(crayons.red(link),
               crayons.red("<link_type>:"),
               crayons.red(link),
               crayons.red("    address: 'my_gerrit.com'"))
    return message
