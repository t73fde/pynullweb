#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Handler - handles web requests.

:copyright: (c) 2017 by Detlef Kreuz
:license: Apache 2.0, see LICENSE
"""

from __future__ import print_function

import BaseHTTPServer
import sys

from typing import cast
from typing import Optional, Tuple  # NOQA, pylint: disable=unused-import

import pynullweb.content
import pynullweb.header
import pynullweb.server  # NOQA, pylint: disable=unused-import


ACCEPT_HEADERS = pynullweb.content.content_types()


class NullWebHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """A handler that returns minimal content."""

    def send_null_response(self, code, size="-"):
        # type: (int, str) -> None
        """Send the response header and log the response code.

        Also send two standard headers with the server software
        version and the current date.
        """
        self.log_request(code, size=size)
        if code in self.responses:
            message = self.responses[code][0]
        else:
            message = ""

        if self.request_version != "HTTP/0.9":
            self.wfile.write(
                "%s %d %s\r\n" % (self.protocol_version, code, message))
        self.send_header("Server", "Apache")
        self.send_header("Date", self.date_time_string())

    def log_message(  # pylint: disable=arguments-differ
            self, message_format, *args):
        # type: (str, str) -> None
        """Log an arbitrary message."""
        sys.stderr.write("%s %s - [%s] %s\n" % (
            self.client_address[0],
            self.headers.get("Host", "-"),
            self.log_date_time_string(),
            message_format % args))

    @staticmethod
    def is_localhost(host, localhosts):
        # type: (str, Tuple[str, ...]) -> bool
        """Check if request is for local host."""
        if not host:
            return True
        for localhost in localhosts:
            if host == localhost:
                return True
            if host.startswith(localhost + ":"):
                return True
        return False

    def redirect_localhost(self):
        # type: () -> bool
        """Redirect to local content."""
        server = cast(pynullweb.server.NullWebServer, self.server)
        if self.is_localhost(self.headers.get("Host"), server.localhosts):
            self.send_null_response(302)
            self.send_header("Location", server.redirect + self.path)
            self.end_headers()
            return True
        return False

    def send_head(self):
        # type: () -> Optional[str]
        """Execute common code for GET and HEAD requests."""
        if self.redirect_localhost():
            return None
        content_type = pynullweb.header.get_content_type(
            self.headers.get("Accept"),
            ACCEPT_HEADERS,
            self.path)
        content = pynullweb.content.minimal_content(content_type)

        self.send_null_response(200, str(len(content)))
        self.send_header("Content-type", "/".join(content_type))
        self.send_header("Content-length", str(len(content)))
        self.send_header("Cache-control", "public,max-age=86400")
        self.send_header("Expires", "Wed, 01 Jan 2070 16:17:18 GMT")
        self.end_headers()
        return content

    def do_GET(self):  # pylint: disable=invalid-name
        # type: () -> None
        """Implement the HTTP GET method."""
        content = self.send_head()
        if content:
            self.wfile.write(content)

    def do_HEAD(self):  # pylint: disable=invalid-name
        # type: () -> None
        """Implement the HTTP HEAD method."""
        self.send_head()
