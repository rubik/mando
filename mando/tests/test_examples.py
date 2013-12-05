import os
import unittest
import subprocess
from paramunittest import parametrized


d = os.path.dirname
EXAMPLES = os.path.join(d(d(os.path.dirname(__file__))), 'examples')


def execute(*args):
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    output, _ = p.communicate()
    retcode = p.poll()
    if retcode:
        raise ValueError('Command {0} exited with non-zero exit code'
                         ' {1}'.format(args, retcode))
    return output


@parametrized(
    ('echo.py',),
    ('git.py',),
    ('gnu.py',),
    ('pow.py',),
    ('pow_arg.py',),
)
class TestExamplesCommands(unittest.TestCase):

    def setParameters(self, name):
        self.path = os.path.join(EXAMPLES, name)

    def testHelp(self):
        self.assertTrue(execute('python', self.path, '-h'))
        self.assertTrue(execute('python', self.path, '--help'))
