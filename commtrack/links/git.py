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
import re
import subprocess
import sys

from commtrack.git import constants as git_const
from commtrack.common import constants as const
from commtrack.git import exceptions as exc
from commtrack.link import Link
from commtrack.locator import Locator

LOG = logging.getLogger(__name__)


class Git(Link):
    """Managing operations on Git based servers."""

    def __init__(self, name, address, parameters):
        super(Git, self).__init__(name, address,
                                  git_const.LINK_TYPE, parameters)
        self.locator = Locator(paths=git_const.PROJECT_PATHS,
                               sub_dirs=[self.name],
                               separators=const.PROJECT_SEPARATORS)
        self.params['commit'] = self.params['tags'] = dict()

    def clone_project(self):
        git_url, project_name = self.get_git_url(self.address,
                                                 self.params['project'])
        self.project_path = (git_const.DEFAULT_PATH + '/' + self.name +
                             '/' + project_name)
        clone_cmd = const.CLONE_CMD + [git_url] + [self.project_path]
        subprocess.run(clone_cmd, stdout=subprocess.DEVNULL)

    def verify_branch(self, branch):
        verify_branch_cmd = 'git rev-parse --verify ' + branch
        res = subprocess.run([verify_branch_cmd],
                             shell=True, cwd=self.params['project_path'],
                             stderr=subprocess.DEVNULL,
                             stdout=subprocess.DEVNULL)
        if res.returncode != 0:
            # Try to get the branch name from plugin mapping
            if branch in self.plugin.BRANCH_MAP[self.ltype]:
                return self.plugin.BRANCH_MAP[self.ltype][branch]
            else:
                LOG.error((exc.missing_branch(branch)))
                sys.exit(2)
        else:
            return branch

    def checkout_branch(self, branch):
        checkout_branch_cmd = 'git checkout ' + branch
        subprocess.run([checkout_branch_cmd],
                       shell=True, cwd=self.params['project_path'],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)

    def grep_change(self, change):
        """Checks if change is part of the project."""
        # Don't use git --grep as it always returns 0
        change_grep_cmd = ["git --no-pager log | grep -B 50 '{}'".format(change)]
        res = subprocess.run(change_grep_cmd, shell=True,
                             cwd=self.params['project_path'],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.DEVNULL)
        return res

    def get_commit(self, text):
        """Returns commit from given text."""
        commit_re = re.search(r'commit (\b[0-9a-f]{5,40}\b)', text)
        return commit_re.group(1)

    def get_tag(self, commit):
        """Returns tag from given commit."""
        get_tag_cmd = ['git --no-pager tag --contains {} | head -n 1'.format(
            commit)]
        res = subprocess.run(get_tag_cmd, shell=True,
                             cwd=self.params['project_path'],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.DEVNULL)
        tag = res.stdout.decode('utf-8').strip()
        if not tag:
            res = subprocess.run(
                git_const.LAST_TAG_CMD, shell=True,
                cwd=self.params['project_path'],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL)
            tag = res.stdout.decode('utf-8').strip()

        return tag

    def append_result(self, res, branch):
        """Append customized result based on given result."""
        if res.returncode == 0:
            self.params['commit'][branch] = self.get_commit(
                str(res.stdout))
            self.params['tags'][branch] = self.get_tag(
                self.params['commit'][branch])
            status = git_const.COLORED_STATS['merged']
            self.params['found'] = True
        else:
            status = git_const.COLORED_STATS['missing']
        self.results.append("Status in project {} branch {} is: {}".format(
            self.params['project'], branch, status))

    def query_branch(self, branch, params={}):
        # Make sure branch exists
        branch = self.verify_branch(branch)
        self.checkout_branch(branch)
        if 'id' in self.params or 'id' in params:
            change_id = self.params.get('id') or params.get('id')
            res = self.grep_change(change_id)
        elif 'change_id' in self.params or not res:
            res = self.grep_change(self.params['change_id'])
        if not res or res.returncode == 1:
            res = self.grep_change(self.params['subject'])
        self.append_result(res, branch)

    def search(self, params):
        """Returns result of the search based on the given change."""
        self.verify_and_set_reqs(git_const.REQUIRED_PARAMS)
        # Check if local copy exists
        self.params['project_path'] = self.locator.locate_local_project(
            self.params['project'])
        if not self.params['project_path']:
            self.clone_project()
        for branch in self.params['branch']:
            self.query_branch(branch, params)
        return self.params

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
            for rep in self.plugin.REPLACE_CHARS[self.ltype]:
                project_name = project.replace(rep[0], rep[1])
                project_url = address + '/' + project_name
                res = subprocess.run(ls_cmd + [project_url],
                                     stdout=subprocess.DEVNULL)
                if res.returncode == 0:
                    return project_url, project_name
