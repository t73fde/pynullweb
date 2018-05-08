#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test content module.

:copyright: (c) 2017 by Detlef Kreuz
:license: Apache 2.0, see LICENSE
"""

import unittest

import pynullweb.content


class ContentTypeTestCase(unittest.TestCase):
    """Test function content.content_types."""

    def test_expected_content_types(self):
        """Test for expected content types such as HTML."""
        content_types = pynullweb.content.content_types()
        expected_types = (
            ("text", "html"), ("image", "gif"), ("image", "jpeg"),
            ("image", "png"))
        for content_type in expected_types:
            self.assertIn(content_type, content_types)


class MinimalContentTestCase(unittest.TestCase):
    """Test function content.minimal_content."""

    def test_content_types(self):
        """Test that for each known content type some content is available."""
        for content_type in pynullweb.content.content_types():
            content = pynullweb.content.minimal_content(content_type)
            self.assertNotEqual("", content)

    def test_illegal_content_types(self):
        """Test for empty content when content type is not supported."""
        for content_type in (None, ('foo', 'bar')):
            content = pynullweb.content.minimal_content(content_type)
            self.assertEqual("", content)
