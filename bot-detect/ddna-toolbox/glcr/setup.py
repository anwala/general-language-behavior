import sys
from distutils.core import setup, Extension
from sysconfig import get_paths

try:
    import numpy
except ImportError:
    sys.exit('numpy is required during installation')

if sys.version_info.major < 3:
    sys.exit('Sorry, Python < 3 is not supported')

sfc_module = Extension(
    'glcr',
    sources=[
        'esa/GSA.cpp', 'esa/lcp.cpp', 'esa/skew.cpp', 'glcr.cpp',
        'lcx/GLCR.cpp', 'lcx/LCR.cpp', 'lcx/LCS.cpp', 'lcx/LCX.cpp',
        'lcx/lv/GLCR_last_visited_int.cpp', 'lcx/lv/LCR_last_visited.cpp',
        'lcx/lv/LCR_last_visited_int.cpp', 'lcx/lv/LCS_last_visited.cpp',
        'lcx/lv/LCS_last_visited_int.cpp', 'lcx/lv/util/LV_list_glcr_int.cpp',
        'lcx/lv/util/LV_list_item.cpp', 'lcx/lv/util/LV_list_lcr.cpp',
        'lcx/lv/util/LV_list_lcr_int.cpp', 'lcx/lv/util/LV_list_lcs.cpp',
        'lcx/lv/util/LV_list_lcs_int.cpp', 'lcx/lv/util/Priority_QLS.cpp',
        'lcx/lv/util/QLS_item.cpp', 'lcx/Result.cpp', 'lcx/Result_saver.cpp',
        'TC_reader.cpp'],

    include_dirs=[get_paths()['include'], numpy.get_include()],
    language='c++')

setup(name='glcr',
      version='1.2',
      description='Support module for the Digital DNA Toolbox (https://github.com/WAFI-CNR/ddna-toolbox)',
      long_description='This module implements the Generalized Longest Common Subsequence algorithm, used by the'
                       'digitaldna module to compute common DNA subsequences.',
      url='https://github.com/WAFI-CNR/ddna-lcs',
      author='WAFI CNR',
      author_email='giuseppe.gagliano@iit.cnr.it',
      license='MIT',
      install_requires=[
          'numpy',
      ],
      ext_modules=[sfc_module]
      )
