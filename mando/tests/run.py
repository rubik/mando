#!/usr/bin/env python

if __name__ == '__main__':
    import unittest
    from mando.tests.test_core import *
    from mando.tests.test_utils import *
    from mando.tests.test_unicode_docstring_on_py2 import *

    from mando.tests.test_google import *
    from mando.tests.test_numpy import *

    unittest.main()
