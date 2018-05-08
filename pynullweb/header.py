#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Handler - handles web requests.

:copyright: (c) 2017 by Detlef Kreuz
:license: Apache 2.0, see LICENSE
"""

from __future__ import print_function

import mimetypes
import re

from typing import List, Optional, Tuple  # NOQA, pylint: disable=unused-import


ACCEPT_RE = re.compile(
    r"""(                         # media-range capturing-parenthesis
            [^\s;,]+              # type/subtype
            (?:[ \t]*;[ \t]*      # ";"
            (?:                   # parameter non-capturing-parenthesis
                [^\s;,q][^\s;,]*  # token that doesn't start with "q"
            |                     # or
                q[^\s;,=][^\s;,]* # token that is more than just "q"
            )
            )*                    # zero or more parameters
        )                         # end of media-range
        (?:[ \t]*;[ \t]*q=        # weight is a "q" parameter
            (\d*(?:\.\d+)?)       # qvalue capturing-parentheses
            [^,]*                 # "extension" accept params: who cares?
        )?                        # accept params are optional
    """, re.VERBOSE)


def parse_accept_header(header):
    # type: (str) -> List[Tuple[str, str, float]]
    """Return parsed Accept:-header as a list of weighted mime types.

    The result is a list of 3-tuples (main-type, sub-type, weigth), where

    * main-type is the mime main type (e.g. "text", "*"),
    * sub-type is the mime sub-type (e.g. "html" or "*",
    * weight is a number between 0 and 1 (included).

    The list is sorted in reverse by weight first, main type second, and sub
    type last. Please not: if the weight is the same for all 3-tuples, a "text"
    type is placed before an "image" type. So is "text/plain" placed before
    "text/html".
    """
    if not header:
        return []
    result = []
    for match in ACCEPT_RE.finditer(header.lower()):
        parts = match.group(1).split("/")
        main_type = parts[0]
        if len(parts) == 1:
            sub_type = "*"
        else:
            sub_type = parts[1]
        quality_str = match.group(2)
        if not quality_str:
            quality = 1.0
        else:
            quality = max(min(float(quality_str), 1.0), 0.0)
        result.append((main_type, sub_type, quality))
    return sorted(result, key=lambda x: (x[2], x[0], x[1]), reverse=True)


def does_type_match(main_type, sub_type, main_item, sub_item):
    # type: (str, str, str, str) -> bool
    """Return True iff mime type matches item type.

    For example:

    >>> does_type_match("*", "any", "any", "any")
    True
    >>> does_type_match("main", "*", "main", "any")
    True
    >>> does_type_match("main", "*", "item", "any")
    False
    >>> does_type_match("main", "sub", "main", "sub")
    True
    >>> does_type_match("main", "sub", "main", "item")
    False

    """
    if main_type == "*":
        return True
    if main_type == main_item:
        if sub_type == "*":
            return True
        return sub_type == sub_item
    return False


def best_match(values,  # type: List[Tuple[str, str, float]]
               matches  # type: List[Tuple[str, str]]
              ):  # NOQA
    # type: (...) -> Optional[Tuple[str, str]]
    """Return best matching mime type."""
    result = None
    best_quality = 0.0
    for main_item, sub_item in matches:
        for main_type, sub_type, quality in values:
            if main_type == "*" and sub_type == "*":
                continue
            if quality <= best_quality:
                break
            if does_type_match(main_type, sub_type, main_item, sub_item):
                result = (main_item, sub_item)
                best_quality = quality
                break
    return result


def best_match_on_path(path):  # type: (str) -> Tuple[str, str]
    """Return mime type based on URI path."""
    if path:
        mime_type, _ = mimetypes.guess_type(path)
        if mime_type:
            main_sub_type = mime_type.split('/')
            if len(main_sub_type) > 1:
                return (main_sub_type[0], main_sub_type[1])
    return ("text", "html")


def get_content_type(accept_header, content_types, url_path):
    # type: (str, List[Tuple[str, str]], str) -> Tuple[str, str]
    """Calculate content type based on accept header and url path."""
    content_type = best_match(
        parse_accept_header(accept_header), content_types)
    return content_type if content_type else best_match_on_path(url_path)
