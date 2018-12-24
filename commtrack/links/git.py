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
from commtrack.locator import Locator

LOG = logging.getLogger(__name__)


class Git(Link):
    """Managing operations on Git based servers."""

    def __init__(self, name, address, parameters):
        super(Git, self).__init__(name, address, const.LINK_TYPE, parameters)
        self.locator = Locator(paths=const.PROJECT_PATHS, sub_dirs=[self.name],
                               separators=const.PROJECT_SEPARATORS)

    def get_git_url(self):
        """Returns working git URL based on project name and predefined
        separators."""
        self.locator.locate_remote_git(self.address, self.params['project'])
        repo_url = os.path.join(self.address, self.params['project'])
        ls_cmd = const.LS_REMOTE_CMD
        res = subprocess.run(ls_cmd + [repo_url], stderr=subprocess.DEVNULL,
                             stdout=subprocess.DEVNULL)
        if res.returncode == 0:
            return repo_url
        else:
            for sep in const.PROJECT_SEPARATORS:
                project_name = project.split(sep)[-1]
                project_url = address + '/' + project_name
                res = subprocess.run(ls_cmd + [project_url],
                                     stdout=subprocess.DEVNULL)
                if res.returncode == 0:
                    return project_url, project_name

    def clone_project(self):
        git_url, project_name = self.get_git_url()
        self.project_path = const.DEFAULT_PATH
        + '/' + self.name + '/' + project_name
        clone_cmd = const.CLONE_CMD + [git_url] + [self.project_path]
        subprocess.run(clone_cmd, stdout=subprocess.DEVNULL)

    def verify_branch(self, branch):
        verify_branch_cmd = 'git rev-parse --verify ' + branch
        res = subprocess.run([verify_branch_cmd],
                             shell=True, cwd=self.params['project_path'],
                             stderr=subprocess.DEVNULL)
        if res.returncode != 0:
            # Try to get the branch name from plugin mapping
            if branch in self.plugin.BRANCH_MAP[self.ltype]:
                return self.plugin.BRANCH_MAP[self.ltype][branch]
            else:
                print(exc.missing_branch(branch))
                sys.exit(2)

    def checkout_branch(self, branch):
        checkout_branch_cmd = 'git checkout ' + branch
        subprocess.run([checkout_branch_cmd],
                       shell=True, cwd=self.params['project_path'],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)

    def grep_change(self, change):
        """Checks if change is part of the project."""
        change_grep_cmd = ["git log | grep {}".format(change)]
        res = subprocess.run(change_grep_cmd, shell=True,
                             cwd=self.params['project_path'],
                             stdout=subprocess.DEVNULL)
        return res

    def append_result(self, res, branch):
        """Append customized result based on given result."""
        if res.returncode == 0:
            status = const.COLORED_STATS['merged']
        else:
            status = const.COLORED_STATS['missing']
        self.results.append("Status in project {} branch {} is: {}".format(
            self.params['project_path'].split('/')[-1], branch, status))

    def query_branch(self, branch):
        # Make sure branch exists
        branch = self.verify_branch(branch)
        self.checkout_branch(branch)
        res = self.grep_change(self.params['change_id'])
        self.append_result(res, branch)

    def search(self):
        """Returns result of the search based on the given change."""
        self.verify_and_set_reqs(const.REQUIRED_PARAMS)
        self.params['project_path'] = self.locator.locate_local_project(
            self.params['project'])
        if not self.params['project_path']:
            self.clone_project()
        for branch in self.params['branch']:
            self.query_branch(branch)
