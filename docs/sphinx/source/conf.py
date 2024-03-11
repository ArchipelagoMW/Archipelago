# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys


# if this is being built via the workflow action Archipelago isn't in path but needs to be for autodocs
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if base_dir not in sys.path:
    sys.path.append(base_dir)


from Utils import __version__

# get important paths for adding stuff to context
templates_dir = os.path.join(base_dir, "WebHostLib", "templates")
static_dir = os.path.join(base_dir, "WebHostLib", "static")

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Archipelago"
copyright = "2024, Archipelago"
author = "Archipelago"
release = __version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.autodoc", "myst_parser"]
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# we need to copy over the AP templates in order to use them in the generated html
templates_path = [
    "_templates",
]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_static_path = [
    "_static",
    static_dir,
]
