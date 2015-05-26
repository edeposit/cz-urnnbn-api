#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from setuptools import setup, find_packages

from docs import getVersion


# Variables ===================================================================
CHANGELOG = open('CHANGELOG.rst').read()
LONG_DESCRIPTION = "\n\n".join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    CHANGELOG
])
URL = "https://resolver.nkp.cz"


# Actual setup definition =====================================================
setup(
    name='cz-urnnbn-api',
    version=getVersion(CHANGELOG),
    description="API for the Czech URN:NBN resolver (%s)." % URL,
    long_description=LONG_DESCRIPTION,
    url='https://github.com/edeposit/cz-urnnbn-api/',

    author='Edeposit team',
    author_email='edeposit@email.cz',

    classifiers=[
        "Development Status :: 3 - Alpha",

        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",

        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications :: File Sharing",

        "License :: OSI Approved :: MIT License",
    ],
    license='MIT',

    packages=find_packages('src'),
    package_dir={'': 'src'},

    include_package_data=True,
    zip_safe=False,

    install_requires=open("requirements.txt").read().splitlines(),
    extras_require={
        "test": [
            "pytest",
            "fake-factory"
        ],
        "docs": [
            "sphinx",
            "sphinxcontrib-napoleon",
        ]
    }
)
