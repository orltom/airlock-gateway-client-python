#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools
from version import __version__


setuptools.setup(
    version=__version__,
    packages=['client'],
    python_requires='>=3.8',
    setup_requires=['Sphinx'],
)
