#!/usr/bin/env python
# -*- coding: utf-8 -*-
from version import __version__
from setuptools import setup

setup(
    version=__version__,
    packages=[
        'client',
        'workspace'
    ],
    python_requires='>=3.13',
    setup_requires=[
        'pytest-runner'
    ],
)
