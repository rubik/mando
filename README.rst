mando: CLI interfaces for Humans!
=================================

.. image:: https://travis-ci.org/rubik/mando.png?branch=master
    :alt: Travis-CI badge
    :target: https://travis-ci.org/rubik/mando

.. image:: https://drone.io/github.com/rubik/mando/status.png
    :alt: Drone badge
    :target: https://drone.io/github.com/rubik/mando

.. image:: https://coveralls.io/repos/rubik/mando/badge.png
    :alt: Coveralls badge
    :target: https://coveralls.io/r/rubik/mando

mando is a wrapper around ``argparse``, and allows you to write complete CLI
applications in seconds while maintaining all the flexibility.

The problem
-----------

While ``argparse`` is great for simple command line applications with only
one, default command, when you have to add multiple commands and manage them
things get really messy and long. But don't worry, mando comes to help!

Quickstart
----------

.. code-block:: python

    from mando import command, main

    @command
    def echo(text, capitalyze=False):
        if capitalyze:
            text = text.upper()
        print(text)

Generated help:

.. code-block:: console

    $ python example.py -h
    usage: example.py [-h] {echo} ...

    positional arguments:
      {echo}
        echo      Echo the given text.

    optional arguments:
      -h, --help  show this help message and exit

    $ python example.py echo -h
    usage: example.py echo [-h] [--capitalyze] text

    Echo the given text.

    positional arguments:
      text

    optional arguments:
      -h, --help    show this help message and exit
      --capitalyze

Actual usage:

.. code-block:: console

    $ python example.py echo spam
    spam
    $ python example.py echo --capitalyze spam
    SPAM


A *real* example
----------------

Something more complex and real-world-*ish*. The code:

.. code-block:: python

    from mando import command, main


    @command
    def push(repository, all=False, dry_run=False, force=False, thin=False):
        '''Update remote refs along with associated objects.

        :param repository: Repository to push to.
        :param --all: Push all refs.
        :param -n, --dry-run: Dry run.
        :param -f, --force: Force updates.
        :param --thin: Use thin pack.'''

        print ('Pushing to {0}. All: {1}, dry run: {2}, force: {3}, thin: {4}'
               .format(repository, all, dry_run, force, thin))


    if __name__ == '__main__':
        main()

mando understands Sphinx-style ``:param:``'s in the docstring, so it creates
short options and their help for you.

.. code-block:: console

    $ python git.py push -h
    usage: git.py push [-h] [--all] [-n] [-f] [--thin] repository

    :param --thin: Use thin pack.

    positional arguments:
      repository     Repository to push to.

    optional arguments:
      -h, --help     show this help message and exit
      --all          Push all refs.
      -n, --dry-run  Dry run.
      -f, --force    Force updates.
      --thin         Use thin pack.

Let's try it!

.. code-block:: console

    $ python git.py push --all myrepo
    Pushing to myrepo. All: True, dry run: False, force: False, thin: False
    $ python git.py push --all -f myrepo
    Pushing to myrepo. All: True, dry run: False, force: True, thin: False
    $ python git.py push --all -fn myrepo
    Pushing to myrepo. All: True, dry run: True, force: True, thin: False
    $ python git.py push --thin -fn myrepo
    Pushing to myrepo. All: False, dry run: True, force: True, thin: True
    $ python git.py push --thin
    usage: git.py push [-h] [--all] [-n] [-f] [--thin] repository
    git.py push: error: too few arguments

Amazed uh? Yes, mando got the short options and the help from the docstring!
You can put much more in the docstring, and if that isn't enough, there's an
``@arg`` decorator to customize the arguments that get passed to argparse.

For a complete documentation, visit https://mando.readthedocs.org/.
NOTE: Docs are still WIP!
