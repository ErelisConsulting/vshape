#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
doclink = """
Documentation
-------------

The full documentation is at http://vshape.rtfd.org."""
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='vshape',
    version='0.0.1',
    description='Utilities for validating ESRI shape files.',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='Jakub Jarosz',
    author_email='qba73@postpro.net',
    url='https://github.com/qba73/vshape',
    packages=[
        'vshape',
    ],
    package_dir={'vshape': 'vshape'},
    include_package_data=True,
    install_requires=['pyshp', 'Click', 'valideer'],
    license='MIT',
    zip_safe=False,
    keywords='vshape, geo, gis, esri, shapefile, map',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: GIS',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
