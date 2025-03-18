"""This file is used to package the project for distribution."""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cits5505-group",
    version="1.0.0",
    description="This repository is dedicated to the CITS5505 group project, \
        focused on building a request forum application.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tonglam/CITS5505_group-project",
    python_requires=">=3.11",
    packages=find_packages(),
)
