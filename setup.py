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
    url='https://gist.github.com/ihciah/30eda05ca36ee9f9f190067538b0ae04',
    packages=find_packages(),
    package_data={'': ['LICENSES']},
    include_package_data=True,
    zip_safe=False,
    install_requires=['requests>=2.17', 'inotify'],
    entry_points={
        'console_scripts': [
            'sub = subtitle.main:main',
            'subtitle = subtitle.main:main'
        ]
    },
    license='MIT License',
    classifiers=(
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
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ),
)