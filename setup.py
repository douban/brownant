from setuptools import setup, find_packages
from os.path import dirname, realpath, join
from platform import python_implementation


current_dir = dirname(realpath(__file__))

with open(join(current_dir, "README.rst")) as long_description_file:
    long_description = long_description_file.read()

install_requires = [
    "Werkzeug >= 0.8",
    "requests >= 1.0",
    "six",
]

if python_implementation() == "PyPy":
    # lxml 3.3.0 series have a fatal bug while working with PyPy
    # See: https://bugs.launchpad.net/lxml/+bug/1273709
    install_requires.append("lxml >= 3.1, != 3.3.0, != 3.3.0beta5, "
                            "!= 3.3.0beta4, != 3.3.0beta3")
else:
    install_requires.append("lxml >= 3.1")


setup(
    name="brownant",
    packages=find_packages(exclude=["tests", "docs"]),
    version="0.1.6",
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
