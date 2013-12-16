import os
from setuptools import setup
try:
    import mando
except ImportError as e:
    version = e.version
else:
    version = mando.__version__


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
      packages=['mando', 'mando.tests'],
      install_requires=['argparse'],
      test_suite='mando.tests',
      classifiers=[
          'Development Status :: 3 - Alpha',
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
