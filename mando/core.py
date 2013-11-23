import re
import sys
import inspect
import argparse
from itertools import izip_longest


_POSITIONAL = type('_positional', (object,), {})
PARAM_RE = re.compile(r"^([\t ]*):param (.*?): ([^\n]*\n(\1[ \t]+[^\n]*\n)*)",
                                            re.MULTILINE)


class Program(object):

    _DISPATCH_TO = '_dispatch_to'

    def __init__(self, prog=None, version=None):
        self.parser = argparse.ArgumentParser(prog)
        if version is not None:
            self.parser.add_argument('-v', '--version', action='version',
                                     version=version)
        self.subparsers = self.parser.add_subparsers()

    def command(self, *args, **kwargs):
        if len(args) == 1 and hasattr(args[0], '__call__'):
            return self._generate_command(args[0])
        else:
            def _command(func):
                return self._generate_command(func, *args, **kwargs)
            return _command

    def _generate_command(self, func, *args, **kwargs):
        self.argspec = argspec = inspect.getargspec(func)
        argz = izip_longest(reversed(argspec.args), reversed(argspec.defaults),
                            fillvalue=_POSITIONAL())
        cmd_help, all_args = analyze_func(func, argspec.varargs, argz)
        subparser = self.subparsers.add_parser(func.__name__,
                                               description=cmd_help or None,
                                               **kwargs)
        for a, kw in all_args:
            subparser.add_argument(*a, **kw)
        subparser.set_defaults(**{self._DISPATCH_TO: func})
        return func

    def execute(self, args):
        arg_map = self.parser.parse_args(args).__dict__
        command = arg_map.pop(self._DISPATCH_TO)
        real_args = []
        for arg in self.argspec.args:
            real_args.append(arg_map.pop(arg))
        if arg_map and arg_map.get(self.argspec.varargs):
            real_args.append(arg_map.pop(self.argspec.varargs))
        return command(*real_args)

    def __call__(self):
        self.execute(sys.argv[1:])


def analyze_func(func, varargs_name, argz):
    doc = (inspect.getdoc(func) or '').strip() + '\n'
    params = find_param_docs(re.sub(r'[\r\t ]+', ' ', doc))
    docstring = PARAM_RE.sub('', doc).rstrip()
    all_args = []
    for k, v in argz:
        kwargs = {}
        is_positional = isinstance(v, _POSITIONAL)
        if k in params:
            args, help = params[k]
            kwargs['help'] = help
            if not is_positional:
                args = fix_dashes(args)
        elif not is_positional:
            args = ['--{0}'.format(k)]
        else:
            args = [k]
        if not is_positional:
            kwargs.update({'default': v, 'dest': k})
            kwargs.update(action_by_type(v))
        all_args.append((args, kwargs))
    if varargs_name:
        kwargs = {'nargs': '*'}
        if varargs_name in params:
            kwargs['help'] = params[varargs_name][1]
        all_args.append(((varargs_name,), kwargs))
    return docstring, all_args


def find_param_docs(docstring):
    paramdocs = {}
    for match in PARAM_RE.finditer(docstring):
        name = match.group(2)
        opts = list(map(str.strip, name.split(',')))
        if len(opts) == 2:
            name = max(opts, key=len).lstrip('-').replace('-', '_')
        elif len(opts) == 1:
            name = opts[0].lstrip('-')
        paramdocs[name] = (opts, match.group(3).rstrip())
    return paramdocs


def action_by_type(obj):
    kw = {}
    if isinstance(obj, bool):
        return {'action': ['store_true', 'store_false'][obj]}
    elif isinstance(obj, list):
        kw = {'action': 'append'}
    kw.update(get_type(obj))
    return kw


def get_type(obj):
    otype = type(obj)
    if any(otype is t for t in set([int, float, str, bool])):
        return {'type': otype}
    return {}


def fix_dashes(opts):
    for opt in opts:
        if opt.startswith('-'):
            yield opt
        else:
            yield '-' * (1 + 1 * (len(opt) > 1)) + opt
