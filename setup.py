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
    version='0.1.0',
    description='Shapefile validator',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='Jakub Jarosz',
    author_email='qba73@postpro.net',
    url='https://github.com/qba73/vshape',
    packages=[
        'vshape',
    ],
    package_dir={'vshape': 'vshape'},
    include_package_data=True,
    install_requires=[
    ],
    license='MIT',
    zip_safe=False,
    keywords='vshape',
    classifiers=[
        'Development Status :: 1 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: GIS',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)
