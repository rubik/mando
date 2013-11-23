import unittest
from paramunittest import parametrized
from mando.core import Program, action_by_type, fix_dashes, find_param_docs


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


a_1 = {'a_param': (['a-param'], 'Short story.\n')}
a_1_1 = {'a_param': (['a_param'], 'Short story.\n')}
a_2 = {'j': (['-j'], 'Woow\n')}
a_3 = {'noun': (['-n', '--noun'], 'cat\n')}
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

         :param well: water''', params={'well': 'water\n'}),
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
                                     'just two little farmers.\n')}),
)
class TestFindParamDocs(unittest.TestCase):

    def setParameters(self, doc, params):
        self.doc = doc
        self.params = params

    def testFunc(self):
        self.assertEqual(self.params, find_param_docs(self.doc))
