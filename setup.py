import os

import setuptools

try:
    import mando
except ImportError as e:
    version = e.version
else:
    version = mando.__version__

deps = ["six"]
extras = {"restructuredText": ["rst2ansi"]}


sversion = tuple(setuptools.__version__.split("."))

if sversion > ("36", "2"):
    deps += ['argparse ; python_version<="2.6"', 'funcsigs ; python_version<="3.2"']
elif sversion > ("18", "0"):
    extras[':python_version<="2.6"'] = ["argparse"]
    extras[':python_version<="3.2"'] = ["funcsigs"]


with open(os.path.join(os.path.dirname(__file__), "README.rst")) as fobj:
    readme = fobj.read()

setuptools.setup(
    name="mando",
    version=version,
    author="Michele Lacchia",
    author_email="michelelacchia@gmail.com",
    url="https://mando.readthedocs.org/",
    download_url="https://pypi.python.org/mando/",
    license="MIT",
    description="Create Python CLI apps with little to no effort at all!",
    platforms="any",
    long_description=readme,
    packages=setuptools.find_packages(),
    install_requires=deps,
    extras_require=extras,
    test_suite="mando.tests",
    keywords="argparse,argument parser,arguments,cli,command line,"
    "commands,decorator,dispatch,flags,getopt,options,optparse,"
    "parser,subcommands",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
)
