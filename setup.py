# !/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='togglsgu',
    version='1.0.0',
    author='Rodrigo Mendonça',
    description='A simple project to automate the creation of csv files for sgu import from a config file.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ro-56/toggl-api-sgu-csv',

    license = 'MIT',
    classifiers=[
        'Development Status :: 1 - Planning',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        "Operating System :: OS Independent",

        'Programming Language :: Python :: 3.10',
    ],

    package_dir={'': 'src'},

    packages=find_packages(where="src"), 

    python_requires='>=3.10',

    install_requires=[
        'pandas>=1.2.4',
        'requests>=2.25.*',
        'datetime>=2.7.*',
        'pyyaml>=6.0'
    ],

    entry_points={
        'console_scripts': [
            'sguTogglCsv=togglsgu.__main__:main',
        ],
    }
)