#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages


requirements = ['ruamel.yaml']
test_requirements = ['pytest']

setup(
    name='yamiconfig',
    version='0.1.0',
    description="Yet another yaml-based settings package",
    long_description="Yet another yaml-based settings package",
    author="Timothy McFadden",
    author_email='tim@timandjamie.com',
    url='https://github.com/mtik00/yamiconfig',
    packages=find_packages(include=['yamiconfig']),
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=True,
    keywords='yamiconfig',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=[],
)