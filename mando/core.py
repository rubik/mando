import re
import sys
import inspect
import argparse
try:
    from itertools import izip_longest
except ImportError:  # pragma: no cover
    from itertools import zip_longest as izip_longest
from mando.utils import (purify_doc, action_by_type, find_param_docs,
                         ensure_dashes, purify_kwargs)


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

    def arg(self, param, *args, **kwargs):
        def wrapper(func):
            if not hasattr(func, '_argopts'):
                func._argopts = {}
            func._argopts[param] = (args, kwargs)
            return func
        return wrapper

    def _generate_command(self, func, name=None, *args, **kwargs):
        func_name = func.__name__
        name = func_name if name is None else name
        argspec = inspect.getargspec(func)
        self.argspecs[func_name] = argspec
        argz = izip_longest(reversed(argspec.args), reversed(argspec.defaults),
                            fillvalue=_POSITIONAL())
        argz = reversed(list(argz))
        doc = (inspect.getdoc(func) or '').strip()
        cmd_help = purify_doc(doc)
        subparser = self.subparsers.add_parser(name,
                                               description=cmd_help or None,
                                               **kwargs)
        for a, kw in self.analyze_func(func, doc, argz, argspec.varargs):
            subparser.add_argument(*a, **purify_kwargs(kw))
        subparser.set_defaults(**{_DISPATCH_TO: func})
        return func

    def analyze_func(self, func, doc, argz, varargs_name):
        params = find_param_docs(doc)
        for arg, default in argz:
            override = getattr(func, '_argopts', {}).get(arg, ((), {}))
            yield merge(arg, default, override, *params.get(arg, ([], {})))
        if varargs_name is not None:
            kwargs = {'nargs': '*'}
            kwargs.update(params.get(varargs_name, (None, {}))[1])
            yield ([varargs_name], kwargs)

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


def merge(arg, default, override, args, kwargs):
    opts = [arg]
    if not isinstance(default, _POSITIONAL):
        opts = list(ensure_dashes(args or opts))
        kwargs.update({'default': default, 'dest': arg})
        kwargs.update(action_by_type(default))
    kwargs.update(override[1])
    return override[0] or opts, kwargs
