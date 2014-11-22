import unittest
from paramunittest import parametrized
from mando.utils import action_by_type, ensure_dashes, find_param_docs, split_doc


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
class TestEnsureDashes(unittest.TestCase):

    def setParameters(self, opts, result):
        self.opts = opts
        self.result = result

    def testFunc(self):
        self.assertEqual(self.result, list(ensure_dashes(self.opts)))


@parametrized(
    ('', ['', '']),
    ('only help.', ['only help.', 'only help.']),
    ('help.\nstill help.', ['help.\nstill help.', 'help.\nstill help.']),
    ('help\n\ndesc', ['help', 'desc']),
    ('help\n\n\ndesc\n', ['help', 'desc']),
)
class TestSplitDoc(unittest.TestCase):

    def setParameters(self, doc, parts):
        self.doc = doc
        self.parts = parts

    def testFunc(self):
        self.assertEqual(self.parts, split_doc(self.doc))


a_1 = {'a_param': (['a-param'], {'help': 'Short story.'})}
a_1_1 = {'a_param': (['a_param'], {'help': 'Short story.'})}
a_2 = {'j': (['-j'], {'help': 'Woow'})}
a_3 = {'noun': (['-n', '--noun'], {'help': 'cat'})}
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

         :param well: water''', params={'well': (['well'], {'help': 'water'})}),
    dict(doc='''
         :param a-param: Short story.
         :param -j: Woow
         :param -n, --noun: cat''', params=a_all),
    dict(doc='''
         Lemme see.

         :param long-story: A long storey belive me: when all started, Adam and Bob were just two little farmers.
         ''', params={'long_story': (['long-story'], {'help': 'A long storey '\
                                     'belive me: when all started, Adam and '\
                                     'Bob were just two little farmers.'})}),
)
class TestFindParamDocs(unittest.TestCase):

    def setParameters(self, doc, params):
        self.doc = doc
        self.params = params

    def testFunc(self):
        found_params = find_param_docs(self.doc)
        self.assertTrue(self.params.keys() == found_params.keys())
        for key, value in self.params.items():
            self.assertTrue(key in found_params)
            found_value = found_params[key]
            self.assertTrue(value[0] == found_value[0])
            for kwarg, val in value[1].items():
                self.assertTrue(val == found_value[1][kwarg])
