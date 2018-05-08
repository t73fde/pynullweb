#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test header module.

:copyright: (c) 2017 by Detlef Kreuz
:license: Apache 2.0, see LICENSE
"""

import unittest

import pynullweb.header


class ParseAcceptHeaderTestCase(unittest.TestCase):
    """Test function header.parse_accept_header."""

    def assert_header(self, expected, accept_header):
        """Test whether accept header is transformed to expected list."""
        self.assertEqual(
            expected, pynullweb.header.parse_accept_header(accept_header))

    def test_null_header(self):
        """Test for empty header."""
        self.assert_header([], "")

    def test_catch_all(self):
        """Test for */* header."""
        self.assert_header([("*", "*", 1)], "*/*")
        self.assert_header(
            [("text", "*", 1), ("image", "*", 1), ("*", "*", 1)],
            "text,*/*,image")

    def test_no_subtype(self):
        """Test for header without sub-type."""
        self.assert_header([("text", "*", 1)], "text")
        self.assert_header([("text", "*", 0.6)], "text ; q=0.6")
        self.assert_header(
            [("text", "*", 1), ("image", "*", 0.5)], "text,image;q=.5")
        self.assert_header(
            [("text", "*", 1), ("image", "*", 0.5)], "image;q=.5,text")

    def test_same_main_type(self):
        """Test for same main type."""
        self.assert_header(
            [("text", "html", 1), ("text", "*", 1)], "text,text/html")
        self.assert_header(
            [("text", "plain", 1), ("text", "html", 1)],
            "text/plain,text/html")
        self.assert_header(
            [("text", "html", 1), ("text", "plain", 0)],
            "text/plain;q=0,text/html")

    def test_rfc7231(self):
        """Test examples from RFC7231, section 5.3.2."""
        self.assert_header(
            [("audio", "basic", 1), ("audio", "*", 0.2)],
            "audio/*; q=0.2, audio/basic")
        self.assert_header(
            [("text", "x-c", 1), ("text", "html", 1), ("text", "x-dvi", 0.8),
                ("text", "plain", 0.5)],
            "text/plain; q=0.5, text/html, text/x-dvi; q=0.8, text/x-c")
        self.assert_header(
            [("text", "plain;format=flowed", 1), ("text", "plain", 1),
                ("text", "*", 1), ("*", "*", 1)],
            "text/*, text/plain, text/plain;format=flowed, */*")
        self.assert_header(
            [("text", "html;level=1", 1),
                ("text", "html", 0.7),
                ("*", "*", 0.5),
                ("text", "html;level=2", 0.4),
                ("text", "*", 0.3)],
            "text/*;q=0.3, text/html;q=0.7, text/html;level=1, " +
            "text/html;level=2;q=0.4, */*;q=0.5")


class DoesTypeMatchTestCase(unittest.TestCase):
    """Test function header.does_type_match."""

    def test_match(self):
        """Test for matching."""
        does_type_match = pynullweb.header.does_type_match
        self.assertTrue(does_type_match("*", "any", "any", "any"))
        self.assertTrue(does_type_match("main", "*", "main", "any"))
        self.assertFalse(does_type_match("main", "*", "item", "any"))
        self.assertTrue(does_type_match("main", "sub", "main", "sub"))
        self.assertFalse(does_type_match("main", "sub", "main", "item"))


class BestMatchTestCase(unittest.TestCase):
    """Test function header.best_match."""


class BestMatchOnPathTestCase(unittest.TestCase):
    """Test function header.best_match_on_path."""

    def assert_type(self, content_type, path):
        """Test whether path leads to content_type."""
        self.assertEqual(
            content_type, pynullweb.header.best_match_on_path(path))

    def test_text_type(self):
        """Test on text types."""
        self.assert_type(("text", "html"), "/foo.html")
        self.assert_type(("text", "plain"), "/foo.txt")

    def test_image_type(self):
        """Test on image types."""
        self.assert_type(("image", "gif"), "/foo.gif")
        self.assert_type(("image", "jpeg"), "/foo.jpeg")
        self.assert_type(("image", "jpeg"), "/foo.jpg")
        self.assert_type(("image", "png"), "/foo.png")
        self.assert_type(("image", "vnd.microsoft.icon"), "/foo.ico")

    def test_illegal_type(self):
        """Test for wrong / non-standard extensions.

        It is expected that such paths will result in HTML as the content type.
        """
        for path in ("/foo", "/foo.", "/foo.qwertz", "foo", "/", ""):
            self.assert_type(("text", "html"), path)

    def test_none_type(self):
        """Test for a None value as the path."""
        self.assert_type(("text", "html"), None)


class GetContentTypeTestCase(unittest.TestCase):
    """Test function header.get_content_type."""
