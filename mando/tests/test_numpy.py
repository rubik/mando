import unittest

from paramunittest import parametrized
from mando import Program

from . import capture

program = Program('example.py', '1.0.10')

@program.command(doctype='numpy')
def simple_numpy_docstring(arg1, arg2="string"):
    '''One line summary.

    Extended description.

    Parameters
    ----------
    arg1 : int
        Description of `arg1`
    arg2 : str
        Description of `arg2`
    Returns
    -------
    str
        Description of return value.
    '''
    return int(arg1) * arg2

@parametrized(
    ('simple_numpy_docstring 2 --arg2=test', 'testtest'),
    )
class TestGenericCommands(unittest.TestCase):

    def setParameters(self, args, result):
        self.args = args.split()
        self.result = result

    def testExecute(self):
        self.assertEqual(self.result, program.execute(self.args))
        self.assertEqual(program.parse(self.args)[0].__name__,
                         program._current_command)


@parametrized(
    ('simple_numpy_docstring --help 2 --arg2=test', '''usage: example.py simple_numpy_docstring [-h] [--arg2 ARG2] arg1

Extended description.

positional arguments:
  arg1         Description of `arg1`

optional arguments:
  -h, --help   show this help message and exit
  --arg2 ARG2  Description of `arg2`
'''
    ),
)
class TestNumpyDocstringHelp(unittest.TestCase):

    def setParameters(self, args, result):
        self.args = args.split()
        self.result = result

    def testExecute(self):
        with self.assertRaises(SystemExit) as cm:
            with capture.capture_sys_output() as (stdout, stderr):
                program.execute(self.args)
        self.assertEqual(self.result, stdout.getvalue())
