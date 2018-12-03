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
        self.address = address
        self.ltype = ltype.lower()
        self.source = self.load_source()

    def load_source(self):
        """Returns source instance based on the link type."""
        source_class = getattr(
            importlib.import_module("commtrack.sources.{}".format(
                self.ltype)), self.ltype.capitalize())
        return source_class()

    def search(self, change):
        print(change)
        print(self.source)
        result = (self.source).search(self.address, change)
        self.result = result
