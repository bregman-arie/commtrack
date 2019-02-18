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


def create_list_parser(subparsers, pparser):
    """The parser for sub command 'list'."""
    list_parser = subparsers.add_parser("list", parents=[pparser])
    list_parser.add_argument('--links', '-l',
                             dest="list_links",
                             help='List all available and chosen links.')


def create_parser():
    """Returns argument parser"""

    # Top level parser
    parent_parser = argparse.ArgumentParser(add_help=False)
    main_parser = argparse.ArgumentParser()

    main_parser.add_argument('--debug', '-d', action='store_true',
                             dest="debug", help='Turn on debug')
    main_parser.add_argument('--links', '-l',
                             dest="links",
                             help='The name of the links the chain consists of')
    main_parser.add_argument('--changeid', '-ci',
                             dest="change_id",
                             help='The change ID to track')
    main_parser.add_argument('--commit', '-c',
                             dest="commit",
                             help='The commit hash to track')
    main_parser.add_argument('--chain-file', '-f',
                             dest="chain_file",
                             help="Chain file path")
    main_parser.add_argument('--plugin',
                             dest="plugin",
                             default="openstack",
                             help="The name of the plugin to use (Default: openstack)")
    main_parser.add_argument('--project', '-p',
                             dest="project",
                             help="The name of the project.")
    main_parser.add_argument('--branch', '-b',
                             dest="branch",
                             nargs='+',
                             help="The name of the branch.")
    main_parser.add_argument('--subject', '-s',
                             dest="subject",
                             help="The subject of the commit message.")

    action_subparsers = main_parser.add_subparsers(
        title="sub-actions", dest="main_command")

    create_list_parser(action_subparsers, parent_parser)

    return main_parser
