import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

project = 'Airlock Gateway REST client'
copyright = '2020, Orlando Tomás'
author = 'Orlando Tomás'
release = '0.0.1'

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon']
templates_path = ['_templates']
exclude_patterns = ["*requestlogger*"]

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']