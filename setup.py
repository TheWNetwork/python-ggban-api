import io, os
from setuptools import setup, find_packages

DESCRIPTION = "Python Elsa API Wrapper"

try:
    with io.open(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md"),
        encoding="utf-8",
    ) as f:
        LONG_DESCRIPTION = "\n" + f.read()
except FileNotFoundError:
    LONG_DESCRIPTION = DESCRIPTION

setup(
    name="python-ggban-api",
    version="0.0.1",
    description="Python Elsa API Wrapper",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="NachABR",
    author_email=None,
    packages=find_packages(),
    install_requires=["aiohttp >=3.7.4"],
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
