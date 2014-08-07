__version__ = '0.3.2'

try:
    from mando.core import Program
except ImportError as e:  # unfortunately this is the only workaround for argparse
                          # and Python 2.6
    e.version = __version__
    raise e

main = Program()
command = main.command
arg = main.arg
parse = main.parse
execute = main.execute
