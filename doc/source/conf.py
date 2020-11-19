import os
import sys

sys.path.insert(0, os.path.abspath('../..'))

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon']
templates_path = ['_templates']
exclude_patterns = ["*requestlogger*"]
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
