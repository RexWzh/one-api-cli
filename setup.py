#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

VERSION = '0.1.0'

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = ['requests', 'click']

test_requirements = ['pytest>=3']

setup(
    author="Rex Wang",
    author_email='1073853456@qq.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="A CLI for the One API project",
    install_requires=requirements,
    license="MIT license",
    # long_description=readme + '\n\n' + history ,
    include_package_data=True,
    keywords='One API CLI',
    name='one-api-cli',
    packages=find_packages(include=['src', 'src.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/RexWzh/one-api-cli',
    version=VERSION,
    zip_safe=False,
)
