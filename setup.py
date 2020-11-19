#!/usr/bin/env python
# -*- coding: utf-8 -*-
from version import __version__
from setuptools import setup
from sphinx.setup_command import BuildDoc
import subprocess


class BuildDocApiDoc(BuildDoc, object):
    """Execute sphinx-apidoc before trigger the sphinx-build"""
    def run(self):
        sphinx_apidoc = subprocess.run(["sphinx-apidoc", "-f", "-o", "doc/source/", "client/"])
        if sphinx_apidoc.returncode != 0:
            raise Exception("sphinx-apidoc failed.")
        super(BuildDocApiDoc, self).run()


setup(
    version=__version__,
    packages=['client'],
    python_requires='>=3.8',
    install_requires=[
        'requests==2.24.0'
    ],
    setup_requires=[
        'sphinx',
        'pytest-runner'
    ],
    tests_require=[
        'pytest'
    ],
    cmdclass={'build_sphinx': BuildDocApiDoc}
)
