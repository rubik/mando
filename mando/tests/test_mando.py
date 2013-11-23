import unittest
from paramunittest import parametrized
from mando import command, parse
from mando.core import action_by_type, fix_dashes, find_param_docs


@parametrized(
    dict(obj=True, result={'action': 'store_false'}),
    dict(obj=False, result={'action': 'store_true'}),
    dict(obj=[], result={'action': 'append'}),
    dict(obj=[1, False], result={'action': 'append'}),
    dict(obj=None, result={}),
    dict(obj=1, result={'type': type(1)}),
    dict(obj=1.1, result={'type': type(1.1)}),
    dict(obj='1', result={'type': type('1')}),
)
class TestActionByType(unittest.TestCase):

    def setParameters(self, obj, result):
        self.obj = obj
        self.result = result

    def testFunc(self):
        self.assertEqual(self.result, action_by_type(self.obj))


@parametrized(
    (['m'], ['-m']),
    (['m', 'min'], ['-m', '--min']),
    (['-m'], ['-m']),
    (['-m', 'min'], ['-m', '--min']),
    (['m', '--min'], ['-m', '--min']),
    (['-m', '--min'], ['-m', '--min']),
    (['-m', '--min', 'l', 'less'], ['-m', '--min', '-l', '--less']),
)
class TestFixDashes(unittest.TestCase):

    def setParameters(self, opts, result):
        self.opts = opts
        self.result = result

    def testFunc(self):
        self.assertEqual(self.result, list(fix_dashes(self.opts)))


a_1 = {'a_param': (['a-param'], 'Short story.')}
a_1_1 = {'a_param': (['a_param'], 'Short story.')}
a_2 = {'j': (['-j'], 'Woow')}
a_3 = {'noun': (['-n', '--noun'], 'cat')}
a_all = {}
for a in (a_1, a_2, a_3):
    a_all.update(a)

@parametrized(
    dict(doc='', params={}),
    dict(doc='Brevity is the soul of wit.', params={}),
    dict(doc=':param a-param: Short story.', params=a_1),
    dict(doc=':param a_param: Short story.', params=a_1_1),
    dict(doc=':param -j: Woow', params=a_2),
    dict(doc=':param -n, --noun: cat', params=a_3),
    dict(doc='''
         Some short text here and there.

         :param well: water''', params={'well': (['well'], 'water')}),
    dict(doc='''
         :param a-param: Short story.
         :param -j: Woow
         :param -n, --noun: cat''', params=a_all),
    dict(doc='''
         Lemme see.

         :param long-story: A long storey belive me: when all started, Adam and
             Bob were just two little farmers.
         ''', params={'long_story': (['long-story'], 'A long storey belive me:'
                                     ' when all started, Adam and Bob were '
                                     'just two little farmers.')}),
)
class TestFindParamDocs(unittest.TestCase):

    def setParameters(self, doc, params):
        self.doc = doc
        self.params = params

    def testFunc(self):
        self.assertEqual(self.params, find_param_docs(self.doc))


###############################################################################
### Program() tests
###############################################################################

@command
def goo(pos, verbose=False, bar=None):
    pass


@command
def vara(pos, foo, spam=24, *vars):
    pass


@command
def another(baw, owl=42, json=False, tomawk=None):
    '''This yet another example showcasing the power of Mando!

    :param baw: That's the positional argument, obviously.
    :param -o, --owl: Yeah, I know, this is too much.
    :param -j, --json: In case you want to pipe it through something.
    :param -t, --tomawk: Well, in this case -t isn't for time.'''
    pass  # (Obviously)


@parametrized(
    ('goo 2', ['2', False, None]),
    ('goo 2 --verbose', ['2', True, None]),
    ('goo 2 --bar 9', ['2', False, '9']),
    ('goo 2 --verbose --bar 8', ['2', True, '8']),
    ('vara 2 3', ['2', '3', 24]),
    ('vara 2 3 --spam 8', ['2', '3', 8]),
    #('vara 1 2 --spam 8 9 8', ['1', '2', 8, '9', '8']),
    ('vara 9 8 1 2 3 4', ['9', '8', 24, '1', '2', '3', '4']),
    ('another 2', ['2', 42, False, None]),
    ('another 2 -j', ['2', 42, True, None]),
    ('another 2 -t 1 -o 3', ['2', 3, False, '1']),
    ('another 2 --owl 89 --tomawk 98', ['2', 89, False, '98']),
    ('another 2 --json -o 1', ['2', 1, True, None]),
    ('another 3 --owl 8 --json --tomawk 8', ['3', 8, True, '8']),
)
class TestGenericCommands(unittest.TestCase):

    def setParameters(self, args, to_args):
        self.args = args.split()
        self.to_args = to_args

    def testParsing(self):
        parsed = parse(self.args)
        self.assertEqual(self.args[0], parsed[0].__name__)
        self.assertEqual(self.to_args, parsed[1])
