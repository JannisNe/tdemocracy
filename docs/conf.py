import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

project = "tdemocracy"
author = "Jannis Necker"
html_theme = "sphinx_rtd_theme"
html_title = "tdemocracy"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx_autodoc_typehints",
    "sphinxcontrib.autodoc_pydantic",
    "sphinx_rtd_theme",
    "sphinx.ext.graphviz",
    "sphinx.ext.viewcode",
]

autodoc_default_flags = ["members"]
autosummary_generate = True

autodoc_pydantic_field_doc_policy = "docstring"
autodoc_pydantic_model_members = True
autodoc_pydantic_model_show_field_summary = False
