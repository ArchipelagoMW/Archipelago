# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys

from Utils import __version__

# if this is being built via the workflow action Archipelago isn't in path but needs to be for autodocs
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if base_dir not in sys.path:
    sys.path.append(base_dir)


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Archipelago"
copyright = "2025, Archipelago"
author = "Archipelago"
release = __version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.autodoc", "myst_parser"]
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

autodoc_default_options = {
    "undoc_members": True,
    "show-inheritance": True,
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_theme = "bizstyle"
html_theme_options = {
    "sidebarwidth": "15%",
}
html_css_files = ["custom.css"]
html_sidebars = {"**": ["globaltoc.html", "relations.html", "sourcelink.html", "searchbox.html"]}

html_logo = "_static/header-logo.svg"
html_favicon = "_static/favicon.ico"
