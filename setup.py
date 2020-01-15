#!/usr/bin/env python
import codecs
import os.path
import re
import sys

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


requires = ['docopt==0.6.2',
            'python-gitlab==1.11.0',
            'verboselogs==1.7',
            'ruamel.yaml==0.16.5']


if sys.version_info[:2] == (2, 6):
    # For python2.6 we have to require argparse since it
    # was not in stdlib until 2.7.
    requires.append('argparse>=1.1')


setup_options = dict(
    name='cdpcli',
    version=find_version('cdpcli', '__init__.py'),
    description='Universal Command Line Environment for Continous Delivery Pipeline on Gitlab-CI.',
    long_description=open('README.md').read(),
    author='Ouest-France SIPA',
    url='https://github.com/Ouest-France/cdp',
    scripts=['bin/cdp'],
    packages=find_packages(exclude=['tests*']),
    package_data={'cdpcli': ['data/*.json', 'examples/*/*.rst',
                             'examples/*/*/*.rst', 'topics/*.rst',
                             'topics/*.json']},
    install_requires=requires,
    extras_require={
        ':python_version=="3.6"': [
            'argparse>=1.1',
        ]
    },
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'freezegun'],
    license='Apache License 2.0',
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ),
)

setup(**setup_options)
