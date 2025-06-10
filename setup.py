#!/usr/bin/env python3
"""
Setup script for Rebol 3 Script Analysis Tool
Provides easy installation and dependency management
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="rebol-script-analyzer",
    version="1.0.0",
    author="Rebol Analysis Tool",
    description="Comprehensive analysis tool for Rebol 3 scripts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["app", "analyzer"],
    install_requires=[
        "Flask>=2.0.0",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    entry_points={
        "console_scripts": [
            "rebol-analyzer=app:main",
        ],
    },
)