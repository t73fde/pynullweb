#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PyNullWeb - a web server that returns minimal content.

:copyright: (c) 2017 by Detlef Kreuz
:license: Apache 2.0, see LICENSE
"""

from __future__ import print_function

import ConfigParser
import argparse

from typing import Dict, List, Tuple  # NOQA, pylint: disable=unused-import

import pynullweb.handler
import pynullweb.server


def parser2dict(config_parser):
    # type: (ConfigParser.ConfigParser) -> Dict[str, Dict[str, str]]
    """Transform the data from a config parser into a dict of dicts."""
    result = {}
    for section in config_parser.sections():
        items = {}
        for name, value in config_parser.items(section):
            items[name] = value
        result[section] = items
    return result


def get_config(args):
    # type: (argparse.Namespace) -> Dict[str, Dict[str, str]]
    """Read config file and set configuration."""
    config_parser = ConfigParser.SafeConfigParser()
    config_parser.add_section("server")
    config_parser.set("server", "verbose", "0")
    config_parser.set("server", "port", "2468")
    config_parser.set("server", "redirect", "")
    config_parser.set("server", "localhosts", "")
    # read config
    config = parser2dict(config_parser)
    if args.verbose:
        config["server"]["verbose"] = args.verbose
    else:
        config["server"]["verbose"] = str(int(config["server"]["verbose"]))
    if args.port:
        config["server"]["port"] = args.port
    else:
        config["server"]["port"] = str(int(config["server"]["port"]))
    if args.redirect:
        config["server"]["redirect"] = args.redirect
    if args.localhosts:
        config["server"]["localhosts"] = args.localhosts
    return config


def main():
    # type: () -> None
    """Start the main program."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p', '--port', type=int, help="port number of web server")
    parser.add_argument(
        "-l", "--localhosts", type=str, help="list of local hosts")
    parser.add_argument(
        "-r", "--redirect", type=str, help="redirect local traffic")
    parser.add_argument(
        "-v", "--verbose", action="count", default=0,
        help="increase verbosity")
    args = parser.parse_args()
    print(args)
    config = get_config(args)

    server_address = ("", int(config["server"]["port"]))
    httpd = pynullweb.server.NullWebServer(
        server_address, pynullweb.handler.NullWebHandler, config)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
