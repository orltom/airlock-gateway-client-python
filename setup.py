#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools
from version import __version__

setuptools.setup(
    name="airlock-waf-client",
    version=__version__,
    author='Orlando Tomás',
    author_email="orlando.tomas@hotmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    scripts=['waf-client'],
    packages=['src'],
    python_requires='>=3.8'
)
