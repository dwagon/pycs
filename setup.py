#!/usr/bin/env python

"""The setup script."""

from typing import Any
from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as readme_file:
    readme = readme_file.read()

with open("requirements.txt", encoding="utf-8") as requirements_file:
    requirements = requirements_file.readlines()

test_requirements: list[Any] = []

setup(
    author="Dougal Scott",
    author_email="dougal.scott@gmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Python D&D Combat simulator",
    entry_points={
        "console_scripts": [
            "pycs=pycs.cli:main",
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n",
    include_package_data=True,
    keywords="pycs",
    name="pycs",
    packages=find_packages(include=["pycs", "pycs.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/dwagon/pycs",
    version="0.3.16",
    zip_safe=False,
)
