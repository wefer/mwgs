#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Based on https://github.com/pypa/sampleproject/blob/master/setup.py."""
# To use a consistent encoding
import codecs
import os
# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys

# Shortcut for building/publishing to Pypi
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel upload')
    sys.exit()


def parse_reqs(req_path='./requirements.txt'):
    """Recursively parse requirements from nested pip files."""
    install_requires = []
    with codecs.open(req_path, 'r') as handle:
        # remove comments and empty lines
        lines = (line.strip() for line in handle
                 if line.strip() and not line.startswith('#'))
        for line in lines:
            # check for nested requirements files
            if line.startswith('-r'):
                # recursively call this function
                install_requires += parse_reqs(req_path=line[3:])
            else:
                # add the line as a new requirement
                install_requires.append(line)
    return install_requires


# This is a plug-in for setuptools that will invoke py.test
# when you run python setup.py test
class PyTest(TestCommand):

    """Set up the py.test test runner."""

    def finalize_options(self):
        """Set options for the command line."""
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        """Execute the test runner command."""
        # Import here, because outside the required eggs aren't loaded yet
        import pytest
        sys.exit(pytest.main(self.test_args))


# Get the long description from the relevant file
here = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='mwgs',

    # Versions should comply with PEP440. For a discussion on
    # single-sourcing the version across setup.py and the project code,
    # see http://packaging.python.org/en/latest/tutorial.html#version
    version='1.0.3',

    description=('Analyze microbial WGS samples.'),
    long_description=long_description,
    # What does your project relate to? Separate with spaces.
    keywords='mwgs microbial development',
    author='Hugo Wefer',
    author_email='hugo.wefer@scilifelab.se',
    license='MIT',

    # The project's main homepage
    url='https://github.com/Clinical-Genomics/mwgs',

    packages=find_packages(exclude=('tests*', 'docs', 'examples')),

    # If there are data files included in your packages that need to be
    # installed, specify them here.
    include_package_data=True,
    zip_safe=False,

    # Although 'package_data' is the preferred approach, in some case you
    # may need to place data files outside of your packages.
    # In this case, 'data_file' will be installed into:
    # '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],

    # Install requirements loaded from ``requirements.txt``
    install_requires=parse_reqs(),
    tests_require=[
        'pytest',
    ],
    cmdclass=dict(
        test=PyTest,
    ),
    entry_points={
        'console_scripts': [
            'mwgs = mwgs.cli:root',
        ],
    },
)
