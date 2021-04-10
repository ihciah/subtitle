# -*- coding: utf-8 -*-
import os
import codecs
from setuptools import setup, find_packages
from setuptools.command.install import install
from subtitle.config import __version__, __author__, __email__


ROOT = os.path.abspath(os.path.dirname(__file__))

setup(
    name='subtitle',
    version=__version__,
    author=__author__,
    author_email=__email__,
    keywords='subtitle, downloader',
    description='A cli tool to download subtitles.',
    long_description='# A cli tool to download subtitles.\n'
                     'Usage: `sub movie.mkv`, `sub movie_dir`.\n'
                     'Run `sub -h` to see all usages.',
    url='https://github.com/ihciah/subtitle',
    packages=find_packages(),
    package_data={'': ['LICENSES']},
    include_package_data=True,
    zip_safe=False,
    install_requires=['requests>=2.17', 'urllib3>=1.23'],
    entry_points={
        'console_scripts': [
            'sub = subtitle.main:main',
            'subtitle = subtitle.main:main'
        ]
    },
    license='MIT License',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Other Audience',
        'Natural Language :: Chinese (Traditional)',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
