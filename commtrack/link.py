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
import importlib


class Link(object):

    def __init__(self, name, address, ltype):
        self.name = name
        self.adress = address
        self.ltype = ltype.lower()
        self.plugin = self.load_plugin()

    def load_plugin(self):
        """Returns plugin instance based on the link type."""
        plugin_class = getattr(
            importlib.import_module("commtrack.plugins.{}".format(
                self.ltype)), self.ltype.capitalize())
        return plugin_class()

    def search(self, commit):
        print(commit)
        print(self.plugin)
        (self.plugin).search(commit)
