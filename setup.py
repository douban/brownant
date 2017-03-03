from setuptools import setup, find_packages
from os.path import dirname, realpath, join

current_dir = dirname(realpath(__file__))

with open(join(current_dir, "README.rst")) as long_description_file:
    long_description = long_description_file.read()

install_requires = [
    "Werkzeug >= 0.8",
    "requests >= 1.0",
    "lxml >= 3.7.3",
    "six",
]

setup(
    name="brownant",
    packages=find_packages(exclude=["tests", "docs"]),
    version="0.1.7",
    description="A lightweight web data extracting framework.",
    long_description=long_description,
    author="Subject-Dev Team, Douban Inc.",
    author_email="subject-dev@douban.com",
    url="https://github.com/douban/brownant",
    license="BSD",
    keywords=["extract", "web data"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Environment :: Other Environment",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=install_requires,
)
