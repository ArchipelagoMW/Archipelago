# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys

from Utils import __version__
from WebHostLib import app as raw_app

# get important paths for adding stuff to context
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
templates_dir = os.path.join(base_dir, "WebHostLib", "templates")
static_dir = os.path.join(base_dir, "WebHostLib", "static")
# add this path to sys to load everything correctly
# sys.path.append(os.path.dirname(__file__))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Archipelago"
copyright = "2024, Archipelago"
author = "Archipelago"
release = __version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.autodoc"]

# we need to copy over the AP templates in order to use them in the generated html
templates_path = [
    "_templates",
    os.path.join(templates_dir),
    os.path.join(templates_dir, "header"),
]
exclude_patterns = []
# template_bridge = "APTemplateBridge.APTemplateBridge"


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_static_path = [
    "_static",
    static_dir,
    # os.path.join(static_dir, "static", "branding"),
    # os.path.join(static_dir, "static", "backgrounds"),
    # os.path.join(static_dir, "static", "backgrounds", "header"),
]


def setup_hooks(app, pagename, templatename, context, doctree):
    context["url_for"] = raw_app.url_for


def setup(app):
    app.connect("html-page-context", setup_hooks)
