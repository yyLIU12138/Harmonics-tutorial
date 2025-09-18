# Configuration file for the Sphinx documentation builder.

# -- Project information

project = "Harmonics"
copyright = "2025, Yuyao Liu"
author = "Yuyao Liu"

release = "0.0.4"
version = "0.0.4"

# -- General configuration

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",  # Add "copy to clipboard" buttons to all text/code boxes
    "nbsphinx",  # Jupyter Notebook tools for Sphinx
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
intersphinx_disabled_domains = ["std"]

templates_path = ["_templates"]

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

html_theme_options = dict(navigation_depth=4, logo_only=True)  # Only show the logo
html_logo = "INSTINCT_LOGO.png"

# -- Options for EPUB output
epub_show_urls = 'footnote'
