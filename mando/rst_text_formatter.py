
import argparse
import sys

from rst2ansi import rst2ansi


def b(s):
    # Useful for very coarse version differentiation.
    PY2 = sys.version_info[0] == 2
    PY3 = sys.version_info[0] == 3
    if PY3:
        return s.encode("utf-8")
    else:
        return s


class RSTHelpFormatter(argparse.RawTextHelpFormatter):
    """
    """
    def format_help(self):
        return rst2ansi(b(super(RSTHelpFormatter, self).format_help())) + '\n'

    def format_usage(self):
        return rst2ansi(b(super(RSTHelpFormatter, self).format_usage())) + '\n'
