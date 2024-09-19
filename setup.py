"""
Setup module for the py_remote_recorder package.
"""

# Rest of setup.py


from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="py_remote_recorder",
    version="0.0.8",
    description="py_remote_recorder is a Python package for recording screens and audio remotely via API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Klajdi Beqiraj",
    author_email="klajdibeqiraj96@gmail.com",
    url="https://github.com/KlajdiBeqiraj/py_remote_recorder.git",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
