#!/usr/bin/env python3
import pathlib

from setuptools import setup, find_packages

README = (pathlib.Path(__file__).parent / "README.md").read_text()

setup(
    name="colima-helper",
    version="0.1.0",
    python_requires='>3.9.0',
    description="colima local DX helper",
    long_description=README,
    long_description_content_type="text/markdown",
    author_email="olivier@micoli.org",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "ansi",
        "colored_traceback",
        "daemon",
        "dependency-injector",
        "docker",
        "event-bus",
        "expiringdict",
        "paramiko",
        "parsedatetime",
        "python-daemon",
        "pygments",
        "pyyaml",
        "requests",
        "supervisor",
        "urwid",
        "urwidtrees",
        "watchdog"
    ],
    extras_require={
        "testing": [
            "pylint"
        ]
    },
    entry_points={
        "console_scripts": [
            "colima-helper=colima_helper.__main__:main",
        ]
    },
)
