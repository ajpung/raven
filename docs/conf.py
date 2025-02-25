# Configuration file for the Sphinx documentation builder.
import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "RAVEN"
copyright = "2025"
author = "Apung"

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
]

myst_enable_extensions = ["dollarmath", "amsmath"]

# Theme configuration
html_theme = "furo"
html_logo = "_static/logo.png"

html_theme_options = {}

html_theme_options = {
    "dark_css_variables": {
        "color-foreground-primary": "#ffffff",  # White text
        "color-foreground-secondary": "#a1a1a1",  # Lighter grey for secondary text
        "color-background-primary": "#131416",  # Dark background
        "color-background-secondary": "#1a1c1e",  # Slightly lighter dark background
        "color-foreground-muted": "#a1a1a1",  # For muted text
    }
}

# The master toctree document
master_doc = "index"

exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    # The following will prevent warnings about these not being in a toctree
    "units.md",
    "weather-codes.md",
    "http-codes.md",
]

# In conf.py
html_additional_pages: dict[str, str] = {}

# Fix the type mismatch - this should be a list not a dict
html_context = {"extra_docs": ["units", "weather-codes", "http-codes"]}

source_suffix: dict[str, str] = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# Explicitly include all your files
master_doc = "index"
include_patterns = ["*.md", "*.rst"]  # Include all markdown and restructuredtext files
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "README.md"]
