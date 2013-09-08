from setuptools import setup, find_packages

from brownant import __version__


setup(
    name="brownant",
    version=__version__,
    description="Brown Ant is a crawling framework.",
    author="Jiangge Zhang",
    author_email="tonyseek@gmail.com",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "Werkzeug >= 0.8",
    ],
)
