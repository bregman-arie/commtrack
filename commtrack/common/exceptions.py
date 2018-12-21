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


class CommtrackException(Exception):
    """Base Commtrack Exception.

    To use this class, inherit from it and define a 'message' property.
    """

    message = "An unknown exception occurred."

    def __init__(self, **properties):
        super(CommtrackException, self).__init__()
        self._properties = properties
        message = self.message  # pylint: disable=exception-message-attribute
        if properties:
            message = message % properties
        self._message = message

    def __str__(self):
        return self._message


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
