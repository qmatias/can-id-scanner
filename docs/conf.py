"""Sphinx configuration."""
project = "CAN ID Scanner"
author = "Matias Kotlik"
copyright = "2023, Matias Kotlik"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
