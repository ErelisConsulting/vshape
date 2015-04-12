#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()

setup(
    name='vshape',
    version='0.1.0',
    description='Utilities for validating ESRI shape files.',
    long_description=readme,
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
    keywords='shape, geo, gis, esri, shapefile, map',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
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
