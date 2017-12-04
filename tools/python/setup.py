#!/usr/bin/env python
from __future__ import print_function

import os
#from distutils.core import setup

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path


DESCRIPTION = 'iso2dpn'
NAME = 'iso2dpn'
DIR_ROOT = os.path.abspath(os.path.dirname(__file__))
DIR_PACKAGE = os.path.join(DIR_ROOT, 'lib', NAME)



def extract_description():
    description = DESCRIPTION
    fname = os.path.join(DIR_ROOT, 'README.rst')
    if os.path.isfile(fname):
        with open(fname) as fin:
            description = fin.read()
    return description


setup(
    name=NAME,
    version='0.1',
    description=DESCRIPTION,
    long_description=extract_description(),
    platforms=['Linux', 'Max OS X', 'Windows'],
    license='BSD',
    url='https://github.com/CSIRO-LW-LD/dpn-ontology/tree/master/tools/python',
    package_dir={'': 'lib'},
    packages=[NAME, '{}.tests'.format(NAME),
              '{}.tests.unit'.format(NAME),
              '{}.tests.integration'.format(NAME)],
    package_data={'{}.tests.integration'.format(NAME):
                  ['CDL/*.cdl', 'HTML/*.html', 'TTL/*.ttl']},
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Development Status :: 1 - Planning Development Status',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Libraries'],
    entry_points={
        'console_scripts': [
           'iso2dpn=iso2dpn.__main__:main',
           'cswiso2dpn=iso2dpn.cswiso2dpn:main',
         ],
     },
)


#if __name__ == '__main__':
   # setup(**setup_args)
