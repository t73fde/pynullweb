#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Server - null web server object.

:copyright: (c) 2017 by Detlef Kreuz
:license: Apache 2.0, see LICENSE
"""

from __future__ import print_function

import BaseHTTPServer

from typing import Dict, List, Tuple  # NOQA, pylint: disable=unused-import


def cleanup_localhosts(raw_hosts):
    # type: (str) -> Tuple[str, ...]
    """Transform comma-separated host names into tuple of strings."""
    return tuple([name.strip() for name in raw_hosts.split(",")])


class NullWebServer(BaseHTTPServer.HTTPServer):
    """Web server with config data."""

    def __init__(self, server_address, request_handler, config):
        # type: (Tuple[str, int], type, Dict[str, Dict[str, str]]) -> None
        """Initialize the server data."""
        self.setup_configuration(config)
        BaseHTTPServer.HTTPServer.__init__(
            self, server_address, request_handler)

    def setup_configuration(self, config):
        # type: (Dict[str, Dict[str, str]]) -> None
        """Transform external configuration into internal representation."""
        self._verbose = int(config["server"]["verbose"])
        self._localhosts = cleanup_localhosts(config["server"]["localhosts"])
        self._redirect = config["server"]["redirect"]

    def server_activate(self):
        # type: () -> None
        """Activate the server."""
        BaseHTTPServer.HTTPServer.server_activate(self)
        if self._verbose > 0:
            print("Server listening on port %d" % (self.server_port,))
            print("- Local hosts = %s" % (self.localhosts,))
            print("- Redirect    = %s" % (self.redirect,))

    @property
    def redirect(self):
        # type: () -> str
        """Return URL prefix for local redirection."""
        return self._redirect

    @property
    def localhosts(self):
        # type: () -> Tuple[str, ...]
        """Return tuple of local host names."""
        default = ()  # type: Tuple[str, ...]
        return self._localhosts if self._redirect else default
