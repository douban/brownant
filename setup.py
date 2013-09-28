from setuptools import setup, find_packages

from brownant import __version__


with open("README.rst") as long_description_file:
    long_description = long_description_file.read()


setup(
    name="brownant",
    packages=find_packages(exclude=["tests", "docs"]),
    version=__version__,
    description="BrownAnt is a crawling framework",
    long_description=long_description,
    author="Jiangge Zhang",
    author_email="tonyseek@gmail.com",
    url="https://github.com/tonyseek/brownant",
    license="MIT",
    keywords=["crawler", "crawling"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Environment :: Other Environment",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        "Werkzeug >= 0.8",
        "lxml >= 3.1",
        "requests >= 1.0",
        "six",
    ],
)
