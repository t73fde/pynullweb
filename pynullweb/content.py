#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Content - handles (minimal) content to be delivered by the web request.

:copyright: (c) 2017 by Detlef Kreuz
:license: Apache 2.0, see LICENSE
"""

from base64 import b64decode

from typing import List, Tuple  # NOQA, pylint: disable=unused-import


def deliver_text_html():  # type: () -> str
    """Return minimal HTML content."""
    return "<html></html>\n"


def deliver_image_gif():  # type: () -> str
    """Return a minimal GIF image."""
    return b64decode("""
R0lGODlhAQABAIABAP///wAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==
""")


def deliver_image_png():  # type: () -> str
    """Return a minimal PNG image."""
    return b64decode("""
iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVQYV2NgYAAAAAMAAWgmWQ0
AAAAASUVORK5CYII=
""")


def deliver_image_jpeg():  # type: () -> str
    """Return a minimal JPEG image."""
    return b64decode("""
/9j/2wBDAAMCAgICAgMCAgIDAwMDBAYEBAQEBAgGBgUGCQgKCgkICQkKDA8MCgsOCwkJDRENDg8Q
EBEQCgwSExIQEw8QEBD/yQALCAABAAEBAREA/8wABgAQEAX/2gAIAQEAAD8A0s8g/9k=
""")


DELIVER_MAP = {
    ("text", "html"): deliver_text_html,
    ("image", "gif"): deliver_image_gif,
    ("image", "png"): deliver_image_png,
    ("image", "jpeg"): deliver_image_jpeg,
}


def content_types():  # type: () -> List[Tuple[str, str]]
    """Return a list of content types that are handled by this module."""
    return DELIVER_MAP.keys()


def minimal_content(content_type):  # type: (Tuple[str, str]) -> str
    """Return minimal content for given content type.

    content_type is a string pair (type, subtype).

    Return the content as a binary string. The string is empty for content
    types that are not handled by this module.
    """
    deliver_function = DELIVER_MAP.get(content_type, None)
    return "" if deliver_function is None else deliver_function()
