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


def missing_branch(branch):
    """Display message in case branch couldn't be found."""
    message = """
Couldn't find branch {0}
This could happen for several reasons:

    1. If you provided branch via CLI then wrong name was provided
    2. The same project has different branch names across systems.
    It should be possible to overcome this by:
        - Using the right plugin with {1}
        - Add branch mapping to your plugin module in {2}

""".format(crayons.red(branch),
           crayons.yellow('commtrack --plugin <plugin_name>'),
           crayons.yellow('commtrack/plugins/<plugin_name>'))
    return message


def missing_requirements(req):
    """Display message in case some must-provided requirements are missing."""
    message = """
Can't perform search in Git server without the parameter {0}

It can be resolved by:

    1. Specifying the parameter '--{0} <{0}>' with the CLI
    2. Change chain order if there are additional link types.
       For example, Gerrit link type provides the parameter {0} to Git without
       the need to specify it manually

""".format(crayons.red(req))
    return message
