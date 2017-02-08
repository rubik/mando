
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
        ret = rst2ansi(b(super(RSTHelpFormatter, self).format_help())
                       + '\n')
        return ret.encode(sys.stdout.encoding,
                          'replace').decode(sys.stdout.encoding)

    def format_usage(self):
        ret = rst2ansi(b(super(RSTHelpFormatter, self).format_usage())
                       + '\n')
        return ret.encode(sys.stdout.encoding,
                          'replace').decode(sys.stdout.encoding)

