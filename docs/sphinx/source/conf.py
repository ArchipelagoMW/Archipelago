# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys

from Utils import __version__


# if this is being built via the workflow action Archipelago isn't in path but needs to be for autodocs
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
stable = base_dir in sys.path  # generated from webhost
if not stable:
    sys.path.append(base_dir)


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

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
exclude_patterns = []
html_theme = "bizstyle"
html_theme_options = {
    "sidebarwidth": "15%",
}

if stable:
    # pull in custom template and styling for stable doc
    static_dir = os.path.join(base_dir, "WebHostLib", "static")
    templates_path = ["_templates"]
    html_static_path = [
        "_static",
        os.path.join(static_dir, "styles", "themes", "base.css"),
        os.path.join(static_dir, "static", "backgrounds", "header", "stone-header.png"),
        os.path.join(static_dir, "static", "backgrounds", "stone.png"),
    ]
else:
    html_logo = "_static/header-logo.svg"
    html_favicon = "_static/favicon.ico"
