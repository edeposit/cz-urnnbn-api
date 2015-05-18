#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from setuptools import setup, find_packages

from docs import getVersion


# Variables ===================================================================
changelog = open('CHANGES.rst').read()
long_description = "\n\n".join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    changelog
])


# Actual setup definition =====================================================
setup(
    name='cz-urnnbn-api',
    version=getVersion(changelog),
    description="API for the Czech URN:NBN resolver (https://resolver.nkp.cz).",
    long_description=long_description,
    url='https://github.com/edeposit/cz-urnnbn-api/',

    author='Edeposit team',
    author_email='edeposit@email.cz',

    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    license='GPL2+',

    packages=find_packages('src'),
    package_dir={'': 'src'},

    # scripts=[''],

    namespace_packages=['edeposit', 'edeposit.amqp'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        "xmltodict",
        "pydhtmlparser>=2.0.9",
        "odictliteral",
    ],
    extras_require={
        "test": [
            "pytest"
        ],
        "docs": [
            "sphinx",
            "sphinxcontrib-napoleon",
        ]
    }
)
