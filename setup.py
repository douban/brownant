from setuptools import setup, find_packages
from os.path import dirname, realpath, join


CURRENT_DIR = dirname(realpath(__file__))

with open(join(CURRENT_DIR, "README.rst")) as long_description_file:
    long_description = long_description_file.read()

with open(join(CURRENT_DIR, "brownant/__init__.py")) as package_file:
    version = next(eval(line.split("=")[-1])
                   for line in package_file if line.startswith("__version__"))


setup(
    name="brownant",
    packages=find_packages(exclude=["tests", "docs"]),
    version=version,
    description="Brownant is a crawling framework",
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
