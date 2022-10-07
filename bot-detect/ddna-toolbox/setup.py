from __future__ import print_function
import sys
from setuptools import setup, find_packages

if sys.version_info.major < 3:
    sys.exit('Sorry, Python < 3 is not supported')
    
with open('requirements.txt') as f:
    INSTALL_REQUIRES = [l.strip() for l in f.readlines() if l]

setup(name='digitaldna',
      version='0.0.5',
      description='A Python implementation of Digital DNA',
      packages=find_packages(),
      install_requires=INSTALL_REQUIRES,
      url='https://github.com/WAFI-CNR/ddna-toolbox',
      author='WAFI CNR',
      author_email='giuseppe.gagliano@iit.cnr.it',
      license='MIT'
      )
