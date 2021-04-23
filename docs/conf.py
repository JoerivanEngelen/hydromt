# -*- coding: utf-8 -*-
#
# hydromt documentation build configuration file, created by
# sphinx-quickstart on Wed Jul 24 15:19:00 2019.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import shutil
import sphinx_autosummary_accessors
from click.testing import CliRunner

# here = os.path.dirname(__file__)
# sys.path.insert(0, os.path.abspath(os.path.join(here, "..")))

import hydromt
from hydromt import DataCatalog
from hydromt.cli.main import main as hydromt_cli


def cli2rst(output, fn):
    with open(fn, "w") as f:
        f.write(".. code-block:: console\n\n")
        for line in output.split("\n"):
            f.write(f"    {line}\n")


# NOTE: the examples/ folder in the root should be copied to docs/examples/examples/ before running sphinx
# -- Project information -----------------------------------------------------

project = "hydromt"
copyright = "Deltares"
author = "Dirk Eilander"

# The short version which is displayed
version = hydromt.__version__

# -- Generate data catalog csv table to inlcude in docs -------
if not os.path.isdir("_generated"):
    os.makedirs("_generated")

data_catalog = DataCatalog()
data_catalog.from_deltares_sources()
df = data_catalog.to_dataframe()
df.index = [
    f"`{k} <{url}>`__" if isinstance(url, str) else k
    for k, url in zip(df.index, df["source_url"])
]
df["reference"] = [
    f"`{k} <https://doi.org/{doi}>`__" if isinstance(doi, str) else k
    for k, doi in zip(df["paper_ref"], df["paper_doi"])
]
df["source_license"] = [
    k
    if not isinstance(k, str)
    else ((f"`Specific <{k}>`__") if k.startswith("https://") else k)
    for k in df["source_license"]
]
df.index.name = "name (link)"
cols = ["category", "data_type", "reference", "source_version", "source_license"]
rm = {
    "source_version": "version",
    "source_license": "license",
    "data_type": "data type",
}
df.loc[:, cols].rename(columns=rm).to_csv(r"_generated/data_sources.csv")

# -- Generate cli help docs ----------------------------------------------

cli_build = CliRunner().invoke(hydromt_cli, ["build", "--help"])
cli2rst(cli_build.output, r"_generated/cli_build.rst")

cli_update = CliRunner().invoke(hydromt_cli, ["update", "--help"])
cli2rst(cli_update.output, r"_generated/cli_update.rst")

cli_clip = CliRunner().invoke(hydromt_cli, ["clip", "--help"])
cli2rst(cli_clip.output, r"_generated/cli_clip.rst")

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.todo",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
    "sphinx.ext.githubpages",
    "sphinx_autosummary_accessors",
    "IPython.sphinxext.ipython_directive",
    "IPython.sphinxext.ipython_console_highlighting",
    "nbsphinx",
]

autosummary_generate = True
# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates", sphinx_autosummary_accessors.templates_path]
# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = ".rst"
# The master toctree document.
master_doc = "index"

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
autodoc_member_order = "bysource"  # overwrite default alphabetical sort
autoclass_content = "both"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_context = {
    "css_files": [
        "_static/theme_overrides.css",
    ],  # override wide tables in RTD theme
}

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# This is required for the alabaster theme
# refs: http://alabaster.readthedocs.io/en/latest/installation.html#sidebars
# html_sidebars = {
#     "**": [
#         "relations.html",  # needs 'show_related': True theme option to display
#         "searchbox.html",
#     ]
# }


# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "pyflwdir_doc"


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',
    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (
        master_doc,
        "hydromt.tex",
        "HydroMT Documentation",
        [author],
        "manual",
    ),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, "hydromt", "HydroMT Documentation", [author], 1)]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "hydromt",
        "HydroMT Documentation",
        author,
        "HydroMT",
        "Build and analyze hydrological models like a data-wizard.",
        "Miscellaneous",
    ),
]

# FIXME exception while evaluating only directive expression: chunk after expression
# nbsphinx_prolog = r"""
# {% set docname = env.doc2path(env.docname, base=None) %}
# .. only:: html
#     .. role:: raw-html(raw)
#         :format: html
#     .. note::
#         | This page was generated from `{{ docname }}`__.
#         | Interactive online version: :raw-html:`<a href="https://mybinder.org/v2/gh/Deltares/hydromt/main?urlpath=lab/tree/examples/{{ docname }}"><img alt="Binder badge" src="https://mybinder.org/badge_logo.svg" style="vertical-align:text-bottom"></a>`
#         __ https://github.com/Deltares/hydromt/blob/main/examples/{{ docname }}
# """
