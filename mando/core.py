import re
import sys
import inspect
import argparse
try:
    from itertools import izip_longest
except ImportError:  # pragma: no cover
    from itertools import zip_longest as izip_longest
from mando.utils import find_param_docs, action_by_type, fix_dashes, PARAM_RE


_POSITIONAL = type('_positional', (object,), {})
_DISPATCH_TO = '_dispatch_to'


class Program(object):

    def __init__(self, prog=None, version=None):
        self.parser = argparse.ArgumentParser(prog)
        if version is not None:
            self.parser.add_argument('-v', '--version', action='version',
                                     version=version)
        self.subparsers = self.parser.add_subparsers()
        self.argspecs = {}

    def command(self, *args, **kwargs):
        if len(args) == 1 and hasattr(args[0], '__call__'):
            return self._generate_command(args[0])
        else:
            def _command(func):
                return self._generate_command(func, *args, **kwargs)
            return _command

    def _generate_command(self, func, name=None, *args, **kwargs):
        name = func.__name__ if name is None else name
        argspec = inspect.getargspec(func)
        self.argspecs[func.__name__] = argspec
        argz = izip_longest(reversed(argspec.args), reversed(argspec.defaults),
                            fillvalue=_POSITIONAL())
        argz = reversed(list(argz))
        cmd_help, all_args = analyze_func(func, argspec.varargs, argz)
        subparser = self.subparsers.add_parser(name,
                                               description=cmd_help or None,
                                               **kwargs)
        for a, kw in all_args:
            kw = dict((k, v) for k, v in kw.items() if v is not None)
            subparser.add_argument(*a, **kw)
        subparser.set_defaults(**{_DISPATCH_TO: func})
        return func

    def parse(self, args):
        arg_map = self.parser.parse_args(args).__dict__
        command = arg_map.pop(_DISPATCH_TO)
        argspec = self.argspecs[command.__name__]
        real_args = []
        for arg in argspec.args:
            real_args.append(arg_map.pop(arg))
        if arg_map and arg_map.get(argspec.varargs):
            real_args.extend(arg_map.pop(argspec.varargs))
        return command, real_args

    def execute(self, args):
        command, a = self.parse(args)
        return command(*a)

    def __call__(self):  # pragma: no cover
        self.execute(sys.argv[1:])


def analyze_func(func, varargs_name, argz):
    doc = (inspect.getdoc(func) or '').strip()
    params = find_param_docs(doc)
    docstring = PARAM_RE.sub('', doc).rstrip()
    all_args = []
    for k, v in argz:
        kwargs = {}
        is_positional = isinstance(v, _POSITIONAL)
        if k in params:
            args, kw = params[k]
            kwargs.update(kw)
            if not is_positional:
                args = fix_dashes(args)
        elif not is_positional:
            args = fix_dashes([k])
        else:
            args = [k]
        if not is_positional:
            kwargs.update({'default': v, 'dest': k})
            kwargs.update(action_by_type(v))
        all_args.append((args, kwargs))
    if varargs_name:
        kwargs = {'nargs': '*'}
        if varargs_name in params:
            kwargs['help'] = params[varargs_name][1]['help']
        all_args.append(((varargs_name,), kwargs))
    return docstring, all_args
