#!/usr/bin/python

if __name__ == '__main__':
    import sys
    import pytest

    if sys.version_info[:2] >= (3, 10):
        pytest.main(['--strict-markers'])
    else:
        pytest.main(['--strict'])
