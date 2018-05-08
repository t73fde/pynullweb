#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages


def open_local(filename):
    """Open a file in this directory."""
    heredir = os.path.abspath(".")
    return open(os.path.join(heredir, filename), 'r')


def read_requires(filename):
    """Read installation requirements from pip install files."""
    with open_local(filename) as reqfile:
        lines = [line.strip() for line in reqfile.readlines()]
    return lines


if __name__ == "__main__":
    README = open_local('README.md').read()
    # CHANGES = open(os.path.join(here, 'CHANGELOG')).read()

    install_requires = read_requires('requirements.txt')
    setup(
        name="pynullweb",
        description="Null Web Server",
        long_description=README,
        version='0.0.1',
        packages=find_packages(exclude=["tests"]),
        install_requires=install_requires,
        data_files=[("../..", ["__main__.py"])],
        license="APL2",
        url="http://github.com/t73fde/pynullweb",
        maintainer="Detlef Stern",
        maintainer_email="mail-pynullweb@yoyod.de",
        keywords="education agile",
        classifiers=[
            "Development Status :: 1 - Planning",
            "Environment :: Web Environment",
            "License :: OSI Approved :: Apache Software License",
            "Programming Language :: Python :: 2.7",
        ],
    )
