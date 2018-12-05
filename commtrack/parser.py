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

import argparse


def create_parser():
    """Returns argument parser"""

    parser = argparse.ArgumentParser(add_help=True)

    parser.add_argument('--debug', '-d', action='store_true',
                        dest="debug", help='Turn on debug')
    parser.add_argument('--links', '-l',
                        dest="links",
                        help='The name of the links the chain consists of')
    parser.add_argument('--changeid', '-ci',
                        dest="change_id",
                        help='The change ID to track')
    parser.add_argument('--commit', '-c',
                        dest="commit",
                        help='The commit hash to track')

    return parser
