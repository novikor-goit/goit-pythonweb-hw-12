import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "Python Web HW 12"
copyright = "2025, Me"
author = "Me"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_markdown_builder",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "alabaster"
html_static_path = ["_static"]
