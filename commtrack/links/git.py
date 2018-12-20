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
import subprocess
import sys

from commtrack.git import constants as const
from commtrack.git import exceptions as exc
from commtrack.link import Link

LOG = logging.getLogger(__name__)


class Git(Link):
    """Managing operations on Git based servers."""

    def __init__(self, name, address, parameters):
        super(Git, self).__init__(name, address, const.LINK_TYPE, parameters)
        self.git_dir = const.DEFAULT_CLONE_PATH + '/' + self.name

    def locate_project(self, project):
        """Returns project path.

        If project couldn't be find, return None.
        """
        for path in const.PROJECT_PATHS:
            for sep in const.PROJECT_SEPARATORS:
                for sub_dir in ['', self.name + '/']:
                    project_name = project.split(sep)[-1]
                    project_path = "{}/{}{}".format(
                        path, sub_dir, project_name)
                    if os.path.isdir(project_path):
                        LOG.info("\nFound local copy of {} at: {}".format(
                            project_name, project_path))
                        return project_path
        return

    def get_git_url(self, address, project):
        """Returns working git URL based on project name and predefined
        separators."""
        repo_url = address + '/' + project
        ls_cmd = const.LS_REMOTE_CMD
        res = subprocess.run(ls_cmd + [repo_url], stderr=subprocess.DEVNULL,
                             stdout=subprocess.DEVNULL)
        if res.returncode == 0:
            return repo_url, project
        else:
            for sep in const.PROJECT_SEPARATORS:
                project_name = project.split(sep)[-1]
                project_url = address + '/' + project_name
                res = subprocess.run(ls_cmd + [project_url],
                                     stdout=subprocess.DEVNULL)
                if res.returncode == 0:
                    return project_url, project_name

    def clone_project(self, address, project):
        git_url, project_name = self.get_git_url(address, project)
        self.project_path = const.DEFAULT_PATH
        + '/' + self.name + '/' + project_name
        clone_cmd = const.CLONE_CMD + [git_url] + [self.projet_path]
        subprocess.run(clone_cmd, stdout=subprocess.DEVNULL)

    def verify_branch(self, branch):
        verify_branch_cmd = 'git rev-parse --verify ' + branch
        res = subprocess.run([verify_branch_cmd],
                             shell=True, cwd=self.project_path,
                             stderr=subprocess.DEVNULL)
        if res.returncode != 0:
            # Try to get the branch name from plugin mapping
            if branch in self.plugin.BRANCH_MAP:
                return self.plugin.BRANCH_MAP[branch]
            else:
                print(exc.missing_branch(branch))
                sys.exit(2)

    def checkout_branch(self, branch):
        checkout_branch_cmd = 'git checkout ' + branch
        subprocess.run([checkout_branch_cmd],
                       shell=True, cwd=self.project_path,
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)

    def query(self, params):
        for branch in params['branch']:
            branch = self.verify_branch(branch)
            self.checkout_branch(branch)
            change_grep_cmd = ["git log | grep {}".format(params['change_id'])]
            res = subprocess.run(change_grep_cmd, shell=True,
                                 cwd=self.project_path,
                                 stdout=subprocess.DEVNULL)
            if res.returncode == 0:
                status = const.COLORED_STATS['merged']
            else:
                status = const.COLORED_STATS['missing']
            self.results.append("Status in project {} branch {} is: {}".format(
                self.project_path.split('/')[-1], branch, status))

    def verify_requirements(self):
        for param in const.REQUIRED_PARAMS:
            if not self.parameters[param]:
                print(exc.missing_requirements(param))
                sys.exit(2)

    def search(self, address, params):
        """Returns result of the search based on the given change."""
        self.verify_requirements()
        self.project_path = self.locate_project(params['project'])
        if not self.project_path:
            self.clone_project(address, params['project'])
        self.query(params)
        return self.parameters
