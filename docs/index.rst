.. mando documentation master file, created by
   sphinx-quickstart on Wed Dec  4 15:37:28 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

mando - CLI interfaces for Humans
=================================

mando is a wrapper around ``argparse``, allowing you to write complete CLI
applications in seconds while maintaining all the flexibility.

The problem
-----------

``argparse`` is great for single-command applications, which only have some
options and one, default command. Unfortunately, when more commands are added,
the code grows too much along with its complexity.

The solution
------------
mando makes an attempt to simplify this. Since commands are nothing but
functions, mando simply provides a couple of decorators and the job is done.
mando tries to infer as much as possible, in order to allow you to write just
the code that is strictly necessary.

This example should showcase most of mando's features::

    # gnu.py
    from mando import main, command, arg
    
    
    @command
    @arg("maxdepth", "-d", "--maxdepth", metavar="<levels>")
    @arg("D", metavar="<debug-opt>")
    def find(path, pattern, maxdepth=None, P=False, D=None):
        """Mock some features of the GNU find command.
    
        This is not at all a complete program, but a simple representation to
        showcase mando's coolest features.
    
        :param path: The starting path.
        :param pattern: The pattern to look for.
        :param int maxdepth: Descend at most <levels>.
        :param P: Do not follow symlinks.
        :param D: Debug option, print diagnostic information."""
    
        if maxdepth is not None and maxdepth < 2:
            print("If you choose maxdepth, at least set it > 1")
        if P:
            print("Following symlinks...")
        print("Debug options: {0}".format(D))
        print("Starting search with pattern: {0}".format(pattern))
        print("No file found!")
    
    
    if __name__ == "__main__":
        main()

mando extracts information from your command's signature and docstring, so you 
can document your code and create the CLI application at once! In the above
example the Sphinx format is used, but mando does not force you to write
ReST docstrings. Currently, mando automatically detects the following styles:

- Sphinx
- Google
- Numpy

The first paragraph of the docstring is taken to generate the command's *help*.
The remaining part (before the parameter descriptions) is the command
*description*.  For everything that needs to be different from the information
taken from the docstring or function signature, mando provides the ``@arg``
decorator, to override arguments before they get passed to ``argparse``.

.. code-block:: console

    $ python gnu.py -h
    usage: gnu.py [-h] {find} ...

    positional arguments:
      {find}
        find      Mock some features of the GNU find command.

    optional arguments:
      -h, --help  show this help message and exit

.. code-block:: console

    $ python gnu.py find -h
    usage: gnu.py find [-h] [-d <levels>] [-P] [-D <debug-opt>] path pattern

    This is not at all a complete program, but a simple representation to
    showcase mando's coolest features.

    positional arguments:
      path                  The starting path.
      pattern               The pattern to look for.

    optional arguments:
      -h, --help            show this help message and exit
      -d <levels>, --maxdepth <levels>
                            Descend at most <levels>.
      -P                    Do not follow symlinks.
      -D <debug-opt>        Debug option, print diagnostic information.

As you can see the short options and metavars have been passed to argparse. Now
let's check the program itself:

.. code-block:: console

    $ python gnu.py find . "*.py"
    Debug options: None
    Starting search with pattern: *.py
    No file found!

.. code-block:: console

    $ python gnu.py find . "*.py" -P
    Following symlinks...
    Debug options: None
    Starting search with pattern: *.py
    No file found!

.. code-block:: console

    $ python gnu.py find . "*" -P -D dbg
    Following symlinks...
    Debug options: dbg
    Starting search with pattern: *
    No file found!

.. code-block:: console

    $ python gnu.py find . "*" -P -D "dbg,follow,trace"
    Following symlinks...
    Debug options: dbg,follow,trace
    Starting search with pattern: *
    No file found!

.. code-block:: console

    $ python gnu.py find -d 1 . "*.pyc"
    If you choose maxdepth, at least set it > 1
    Debug options: None
    Starting search with pattern: *.pyc
    No file found!

.. code-block:: console

    $ python gnu.py find --maxdepth 0 . "*.pyc"
    If you choose maxdepth, at least set it > 1
    Debug options: None
    Starting search with pattern: *.pyc
    No file found!

.. code-block:: console

    $ python gnu.py find --maxdepth 4 . "*.pyc"
    Debug options: None
    Starting search with pattern: *.pyc
    No file found!

.. code-block:: console

    $ python gnu.py find --maxdepth 4 .
    usage: gnu.py find [-h] [--maxdepth <levels>] [-P] [-D <debug_opts] path pattern
    gnu.py find: error: the following arguments are required: pattern

.. code-block:: console

    $ python gnu.py find -d "four" . filename
    usage: gnu.py find [-h] [--maxdepth <levels>] [-P] [-D <debug_opts] path pattern
    gnu.py find: error: argument --maxdepth/-d: invalid int value: 'four'


Contents
--------

.. toctree::
   :maxdepth: 2

   usage.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
