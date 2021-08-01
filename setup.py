#!/bin/env python3
# -*- coding: utf-8 -*-

"""Setup.py for the Meteoserver Python package."""


# Package version:
version='0.0.16'

# Get long description from README.md:
with open('README.md', 'r') as fh:
    long_description = fh.read()

# Set package properties:
from setuptools import setup
setup(
    name='meteoserver',
    description='A Python module to obtain and read Dutch weather data from Meteoserver.nl',
    author='Marc van der Sluys',
    url='https://github.com/MarcvdSluys/Meteoserver',
    
    packages=['meteoserver'],
    install_requires=['pandas','requests'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    
    version=version,
    license='GPLv3+',
    keywords=['weather','sun','data','forecast','api'],
    
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Physics',
    ]
)
