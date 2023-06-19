# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


import sys
from pathlib import Path
from sphinx.application import Sphinx

sys.path.insert(0, Path(__file__).parents[2].resolve().as_posix())

# remove previously generated files to avoid error messages from sphinx
for generated in (Path(__file__).parent / "generated").iterdir():
    generated.unlink()

import ch5mpy


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
needs_sphinx = "1.7"  # autosummary bugfix

project = "Ch5mpy"
copyright = "2023, Matteo Bouvier"
author = "Matteo Bouvier"
version = ch5mpy.__version__
release = version

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
# -- General configuration ---------------------------------------------------
templates_path = ["_templates"]
exclude_patterns = []

master_doc = "index"

extensions = [
    "sphinx.ext.autodoc",  # for generating API
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",  # for links to external docs
    "sphinx.ext.viewcode",  # for displaying code source
    "sphinx.ext.napoleon",  # for parsing Numpy and Google style docstrings
    "sphinx_autodoc_typehints",  # for adding typehint parsing
]


# sphinx.ext.autodoc -- config ----------------------------
autodoc_member_order = "bysource"
autodoc_default_flags = ["members"]
autoclass_content = "both"
autodoc_typehints = "both"


# sphinx.ext.autosummary -- config ------------------------
autosummary_generate = True


# sphinx.ext.intersphinx -- config ------------------------
intersphinx_mapping = dict(
    python=("https://docs.python.org/3/", None),
    numpy=("https://numpy.org/doc/stable/", None),
)


# sphinx.ext.napoleon -- config ---------------------------
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_use_rtype = True  # having a separate entry generally helps readability
napoleon_use_param = True


# sphinx_autodoc_typehints -- config ----------------------
typehints_defaults = "braces"


# -- Options for HTML output -------------------------------------------------
pygments_style = "sphinx"

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_logo = "_static/images/logo_ch5mpy_low.png"

html_context = dict(
    display_github=True,  # Integrate GitHub
    github_user="Vidium",  # Username
    github_repo="ch5mpy",  # Repo name
    github_version="master",  # Version
    conf_py_path="/docs/source/",  # Path in the checkout to the docs root
)

html_show_sphinx = False

# custom css styles in _static/css/
html_css_files = ["css/rtd_custom.css"]


def setup(app: Sphinx):
    # Don’t allow broken links.
    app.warningiserror = True
