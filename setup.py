"""Setup script for the Python Grader Tool package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="1012-grader",
    version="0.1.0",
    author="COMP 1012 Team",
    author_email="your.email@example.com",
    description="A tool to assist in grading Python assignments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pieberrykinnie/1012-grader",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "1012-grader=grader.main:main",
        ],
    },
) 