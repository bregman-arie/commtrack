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
import logging
import os


LOG = logging.getLogger(__name__)


class Locator(object):
    """Manage project discovery."""

    def __init__(self, address=None, paths=[], sub_dirs=[],
                 separators=[], replacers=[]):
        self.address = address
        self.paths = paths
        # Empty string is used for searching in original path
        # as well and not only in sub directories
        self.sub_dirs = [''] + sub_dirs
        self.separators = separators
        self.replacers = replacers

    def local_search(self, project):
        """Search for the project in defined paths, without

        using separators or replacers
        """
        for path in self.paths:
            for sub in self.sub_dirs:
                project_path = os.path.join(path, sub, project)
                if os.path.isdir(project_path):
                    LOG.info("\nFound {} in {}".format(project, path))
                    return project_path

    def locate_remote_project(self, address, project):
        """Locate remote repository."""
        pass

    def locate_local_project(self, project):
        """Searches for given project in local paths."""
        res = self.local_search(project)
        if res:
            return res
        for sep in self.separators:
            project_name = project.split(sep)[-1]
            res = self.local_search(project_name)
            if res:
                return res
        return None
