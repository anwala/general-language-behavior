	# -*- coding: utf-8 -*-

import sys
import os
import sphinx_rtd_theme
try:
    import gen_rst
except:
    pass
    
sys.path.insert(0, os.path.abspath('../digitaldna/'))
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'numpydoc',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx_gallery.gen_gallery'
]
import sphinx
from distutils.version import LooseVersion
if LooseVersion(sphinx.__version__) < LooseVersion('1.4'):
    extensions.append('sphinx.ext.pngmath')
else:
    extensions.append('sphinx.ext.imgmath')
    
sphinx_gallery_conf = {
    'examples_dirs' : '../examples',
    'gallery_dirs'  : 'auto_examples'}
templates_path = ['templates']
source_suffix = '.rst'
autodoc_default_flags = ['members', 'inherited-members']
autosummary_generate = True
plot_gallery = 'True'
master_doc = 'index'
project = u'digitaldna'
copyright = u'2018, Giuseppe Gagliano'
version = '0.0.5'
exclude_patterns = ['_build', '_templates']
show_authors = True
pygments_style = 'sphinx'
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_title = 'Digital DNA'
html_logo = 'logos/ddna_wide.png'
html_favicon = 'logos/ddna_wide.png'
html_static_path = ['_static']
html_last_updated_fmt = '%b %d, %Y'
html_show_sourcelink = False
htmlhelp_basename = 'digitaldna-doc'


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
# The paper size ('letterpaper' or 'a4paper').
#'papersize': 'letterpaper',

# The font size ('10pt', '11pt' or '12pt').
#'pointsize': '10pt',

# Additional stuff for the LaTeX preamble.
#'preamble': '',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
  ('index', 'digitaldna.tex', u'Digital DNA Documentation',
   u'Giuseppe Gagliano', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# If true, show page references after internal links.
#latex_show_pagerefs = False

# If true, show URL addresses after external links.
#latex_show_urls = False

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_domain_indices = True


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'digitaldna', u'DigitalDNA Documentation',
     [u'Giuseppe Gagliano'], 1)
]

# If true, show URL addresses after external links.
#man_show_urls = False


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
  ('index', 'digitaldna', u'DigitalDNA Documentation',
   u'Giuseppe Gagliano', 'digitaldna', 'One line description of project.',
   'Miscellaneous'),
]

def generate_example_rst(app, what, name, obj, options, lines):
    # generate empty examples files, so that we don't get
    # inclusion errors if there are no examples for a class / module
    examples_path = os.path.join(app.srcdir, "generated",
                                 "%s.examples" % name)
    if not os.path.exists(examples_path):
        # touch file
        open(examples_path, 'w').close()


def setup(app):
    app.connect('autodoc-process-docstring', generate_example_rst)

# Documents to append as an appendix to all manuals.
#texinfo_appendices = []

# If false, no module index is generated.
#texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
#texinfo_show_urls = 'footnote'

# If true, do not generate a @detailmenu in the "Top" node's menu.
#texinfo_no_detailmenu = False


# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    'python': ('https://docs.python.org/{.major}'.format(
        sys.version_info), None),
    'numpy': ('https://docs.scipy.org/doc/numpy/', None),
    'scipy': ('https://docs.scipy.org/doc/scipy/reference', None),
    'matplotlib': ('https://matplotlib.org/', None),
    'sklearn': ('http://scikit-learn.org/stable', None)
}
# sphinx-gallery configuration
sphinx_gallery_conf = {
    'doc_module': 'digitaldna',
    'backreferences_dir': os.path.join('generated'),
    'reference_url': {
        'digitaldna': None}
}
