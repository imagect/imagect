# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import os.path

docs_dir = os.path.dirname(__file__)
repo_dir = os.path.abspath(os.path.join(docs_dir, '../..'))
sys.path.insert(0, repo_dir)
os.chdir(repo_dir)
print(repo_dir)


# -- Project information -----------------------------------------------------

project = 'imagect'
copyright = '2019, ChenZhihui'
author = 'ChenZhihui'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
  'sphinx.ext.autodoc',
  'sphinx.ext.todo',
  'sphinx.ext.intersphinx',
  'sphinx.ext.coverage',
  'sphinx.ext.viewcode',
  'sphinx.ext.autosummary',
  'sphinx.ext.napoleon',
  'repoze.sphinx.autointerface',
  "recommonmark"
]

master_doc = 'contents'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# use markdown
from recommonmark.parser import CommonMarkParser
    
# source_parsers = {
#         '.md': CommonMarkParser,
# }
    
source_suffix = {
        '.rst' : "restructuredtext",
        '.md' : "markdown",
         ".txt" : "markdown"
         }

import recommonmark.transform
github_doc_root = 'https://github.com/imagect/imagect/tree/master/doc/source'
def setup(app):
    app.add_config_value('recommonmark_config', {
            'url_resolver': lambda url: github_doc_root + url,
            'auto_toc_tree_section': 'Contents',
            }, True)
    app.add_transform(recommonmark.transform.AutoStructify)

#     app.add_source_parser(CommonMarkParser)
