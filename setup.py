import os
from setuptools import setup, find_packages
try:
    import mando
except ImportError as e:
    version = e.version
else:
    version = mando.__version__

deps = ['six']
try:
    # Will fail with 2.6
    import argparse
except ImportError:
    deps.append('argparse')

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as fobj:
    readme = fobj.read()

setup(name='mando',
      version=version,
      author='Michele Lacchia',
      author_email='michelelacchia@gmail.com',
      url='https://mando.readthedocs.org/',
      download_url='https://pypi.python.org/mando/',
      license='MIT',
      description='Create Python CLI apps with little to no effort at all!',
      platforms='any',
      long_description=readme,
      packages=find_packages(),
      install_requires=deps,
      extras_require={'restructuredText': ['rst2ansi'],},
      test_suite='mando.tests',
      keywords='argparse,argument parser,arguments,cli,command line,'
               'commands,decorator,dispatch,flags,getopt,options,optparse,'
               'parser,subcommands',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.1',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Topic :: Software Development',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Utilities',
      ]
)
