'''Main module containing the class Program(), which allows the conversion from
ordinary Python functions into commands for the command line. It uses
:py:module:``argparse`` behind the scenes.'''

import sys
import inspect
import argparse
try:
    from itertools import izip_longest
except ImportError:  # pragma: no cover
    from itertools import zip_longest as izip_longest
from mando.utils import (purify_doc, action_by_type, find_param_docs,
                         split_doc, ensure_dashes, purify_kwargs)


_POSITIONAL = type('_positional', (object,), {})
_DISPATCH_TO = '_dispatch_to'


class Program(object):

    def __init__(self, prog=None, version=None, **kwargs):
        self.parser = argparse.ArgumentParser(prog, **kwargs)
        if version is not None:
            self.parser.add_argument('-v', '--version', action='version',
                                     version=version)
        self.subparsers = self.parser.add_subparsers()
        self.argspecs = {}
        self.current_command = None

    def command(self, *args, **kwargs):
        '''A decorator to convert a function into a command. It can be applied
        as ``@command`` or as ``@command(new_name)``, specifying an alternative
        name for the command (default one is ``func.__name__``).'''
        if len(args) == 1 and hasattr(args[0], '__call__'):
            return self._generate_command(args[0])
        else:
            def _command(func):
                return self._generate_command(func, *args, **kwargs)
            return _command

    def arg(self, param, *args, **kwargs):
        '''A decorator to override the parameters extracted from the docstring
        or to add new ones.

        :param param: The parameter's name. It must be among the function's
            arguments names.'''
        def wrapper(func):
            if not hasattr(func, '_argopts'):
                func._argopts = {}
            func._argopts[param] = (args, kwargs)
            return func
        return wrapper

    def _generate_command(self, func, name=None, *args, **kwargs):
        '''Generate argparse's subparser.

        :param func: The function to analyze.
        :param name: If given, a different name for the command. The default
            one is ``func.__name__``.'''
        func_name = func.__name__
        name = func_name if name is None else name
        argspec = inspect.getargspec(func)
        self.argspecs[func_name] = argspec
        argz = izip_longest(reversed(argspec.args), reversed(argspec.defaults
                                                             or []),
                            fillvalue=_POSITIONAL())
        argz = reversed(list(argz))
        doc = (inspect.getdoc(func) or '').strip() + '\n'
        cmd_help, cmd_desc = split_doc(purify_doc(doc))
        subparser = self.subparsers.add_parser(name,
                                               help=cmd_help or None,
                                               description=cmd_desc or None,
                                               **kwargs)
        for a, kw in self.analyze_func(func, doc, argz, argspec.varargs):
            subparser.add_argument(*a, **purify_kwargs(kw))
        subparser.set_defaults(**{_DISPATCH_TO: func})
        return func

    def analyze_func(self, func, doc, argz, varargs_name):
        '''Analyze the given function, merging default arguments, overridden
        arguments (with @arg) and parameters extracted from the docstring.

        :param func: The function to analyze.
        :param doc: The function's docstring.
        :param argz: A list of the form (arg, default), containing arguments
            and their default value.
        :param varargs_name: The name of the variable arguments, if present,
            otherwise ``None``.'''
        params = find_param_docs(doc)
        for arg, default in argz:
            override = getattr(func, '_argopts', {}).get(arg, ((), {}))
            yield merge(arg, default, override, *params.get(arg, ([], {})))
        if varargs_name is not None:
            kwargs = {'nargs': '*'}
            kwargs.update(params.get(varargs_name, (None, {}))[1])
            yield ([varargs_name], kwargs)

    def parse(self, args):
        '''Parse the given arguments and return a tuple ``(command, args)``,
        where ``args`` is a list consisting of all arguments. The command can
        then be called as ``command(*args)``.

        :param args: The arguments to parse.'''
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
        '''Parse the arguments and execute the resulting command.

        :param args: The arguments to parse.'''
        command, a = self.parse(args)
        self.current_command = command.__name__
        return command(*a)

    def __call__(self):  # pragma: no cover
        '''Parse ``sys.argv`` and execute the resulting command.'''
        self.execute(sys.argv[1:])


def merge(arg, default, override, args, kwargs):
    '''Merge all the possible arguments into a tuple and a dictionary.

    :param arg: The argument's name.
    :param default: The argument's default value or an instance of _POSITIONAL.
    :param override: A tuple containing (args, kwargs) given to @arg.
    :param args: The arguments extracted from the docstring.
    :param kwargs: The keyword arguments extracted from the docstring.'''
    opts = [arg]
    if not isinstance(default, _POSITIONAL):
        opts = list(ensure_dashes(args or opts))
        kwargs.update({'default': default, 'dest': arg})
        kwargs.update(action_by_type(default))
    else:
        # positionals can't have a metavar, otherwise the help is screwed
        # if one really wants the metavar, it can be added with @arg
        kwargs['metavar'] = None
    kwargs.update(override[1])
    return override[0] or opts, kwargs
