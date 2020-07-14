# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md', 'r') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Eve Fit Export Parser',
    version='0.1.0',
    description='Simple parser for the Eve Fit export format',
    long_description=readme,
    author='Ken Beck',
    author_email='beckkenneth@gmail.com',
    url='https://github.com/cmptrgeekken/eve-fit-parser',
    license=license,
    packages=find_packages(exclude=('tests')),
    python_requires='>=2.7'
)

