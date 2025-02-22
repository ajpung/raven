# Configuration file for the Sphinx documentation builder.
import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "RAVEN"
copyright = "2025"
author = "Apung"

extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon", "myst_parser"]

# Theme configuration
html_theme = "furo"
html_logo = "_static/logo.png"

html_theme_options = {
    "light_css_variables": {
        # Light mode variables
    },
    "dark_css_variables": {
        "color-foreground-primary": "var(--color-foreground-primary)",
        "color-background-primary": "#131416",
        "color-background-secondary": "#1a1c1e",
    },
    "dark_mode_theme": "dark",
    "logo_only": True,
    "display_version": False,
}

# The master toctree document
master_doc = "index"

# File extensions to include
source_suffix = [".rst", ".md"]
