#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools
from version import __version__


setuptools.setup(
    version=__version__,
    packages=['client'],
    python_requires='>=3.8',
    install_requires=[
        'requests==2.24.0'
    ],
    setup_requires=[
        'Sphinx'
    ]
)
