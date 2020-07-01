from argparse import ArgumentParser
from collections import deque
from functools import partial
from inspect import Signature
from itertools import tee
from operator import add
from unittest import TestCase, main as unittest_main

from mando import Program


def rest_add(a, b):
    """
    The sum of two numbers.

    :param a: The first number
    :type a: ```int or float```

    :param b: The second number
    :type b: ```int or float```

    :returns: the summation of the two inputs
    :rtype: ```int or float```
    """
    return add(a, b)


def numpy_add(a, b):
    """The sum of two numbers.

    a : int or float
        The first number.

    b : int or float
        The second number.

    Returns
    -------
    int or float
        The summation of the two inputs.
    """
    return add(a, b)


def google_add(a, b):
    """The sum of two numbers.

    Args:
        a (int or float): The first number.
        b (int or float): The second number.

    Returns:
        int or float: The summation of the two inputs.
    """
    return add(a, b)


# A simple helper from https://docs.python.org/3/library/itertools.html
def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


class NoDecoratorTest(TestCase):
    def setUp(self) -> None:
        self.program = Program('example.py', '1.0.10')

    def tearDown(self) -> None:
        del self.program

    def test_rest_no_decorator(self):
        self.program.command(rest_add)
        self.assertIn('rest_add', self.program._signatures)

    def test_numpy_no_decorator(self):
        self.program.command(numpy_add)
        self.assertIn('numpy_add', self.program._signatures)

    def test_google_no_decorator(self):
        self.program.command(google_add)
        self.assertIn('google_add', self.program._signatures)

    def test_all(self):
        all_funcs = 'rest_add', 'numpy_add', 'google_add'
        global_symbols = globals()
        deque(map(self.program.command, map(global_symbols.__getitem__, all_funcs)), maxlen=0)
        deque(map(partial(self.assertIn, container=self.program._signatures), all_funcs), maxlen=0)

        def compare_signatures(*signatures):  # type: ((Signature, Signature)) -> None
            self.assertEquals(len(signatures), 1)
            self.assertEquals(len(signatures[0]), 2)
            signatures0, signatures1 = signatures[0]
            self.assertTupleEqual(tuple(signatures0._parameters), tuple(signatures1._parameters))

        def compare_argument_parsers(*argparses):  # type: ((ArgumentParser, ArgumentParser)) -> None
            self.assertEquals(len(argparses), 1)
            self.assertEquals(len(argparses[0]), 2)
            argparse0, argparse1 = argparses[0]
            self.assertEquals(argparse0.description, argparse1.description)

        deque(map(compare_signatures, pairwise(map(self.program._signatures.__getitem__, all_funcs))), maxlen=0)
        deque(map(compare_argument_parsers, pairwise(map(self.program._subparsers.choices.__getitem__, all_funcs))),
              maxlen=0)


if __name__ == '__main__':
    unittest_main()
