'''Main module containing the class Program(), which allows the conversion from
ordinary Python functions into commands for the command line. It uses
:py:module:``argparse`` behind the scenes.'''

import argparse
import inspect
import sys

from mando.napoleon import Config, GoogleDocstring, NumpyDocstring

from mando.utils import (purify_doc, action_by_type, find_param_docs,
                         split_doc, ensure_dashes, purify_kwargs)
try:
    from inspect import signature
except ImportError:
    from funcsigs import signature


_POSITIONAL = type('_positional', (object,), {})
_DISPATCH_TO = '_dispatch_to'


class SubProgram(object):
    def __init__(self, parser, signatures):
        self.parser = parser
        self._subparsers = self.parser.add_subparsers()
        self._signatures = signatures

    @property
    def name(self):
        return self.parser.prog

    # Add global script options.
    def option(self, *args, **kwd):
        assert args and all(arg.startswith('-') for arg in args), \
            "Positional arguments not supported here"
        completer = kwd.pop('completer', None)
        arg = self.parser.add_argument(*args, **kwd)
        if completer is not None:
            arg.completer = completer
        # do not attempt to shadow existing attributes
        assert not hasattr(self, arg.dest), "Invalid option name: " + arg.dest
        return arg

    def add_subprog(self, name, **kwd):
        # also always provide help= to fix missing entry in command list
        help = kwd.pop('help', "{} subcommand".format(name))
        prog = SubProgram(self._subparsers.add_parser(name, help=help, **kwd),
                          self._signatures)
        # do not attempt to overwrite existing attributes
        assert not hasattr(self, name), "Invalid sub-prog name: " + name
        setattr(self, name, prog)
        return prog

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

    def _generate_command(self, func, name=None, doctype='rest',
                          *args, **kwargs):
        '''Generate argparse's subparser.

        :param func: The function to analyze.
        :param name: If given, a different name for the command. The default
            one is ``func.__name__``.'''

        name = name or func.__name__
        doc = (inspect.getdoc(func) or '').strip() + '\n'

        if doctype == 'numpy':
            config = Config(napoleon_google_docstring=False,
                            napoleon_use_rtype=False)
            doc = str(NumpyDocstring(doc, config))
        elif doctype == 'google':
            config = Config(napoleon_numpy_docstring=False,
                            napoleon_use_rtype=False)
            doc = str(GoogleDocstring(doc, config))
        elif doctype == 'rest':
            pass
        else:
            raise ValueError('doctype must be one of "numpy", "google", '
                             'or "rest"')
        cmd_help, cmd_desc = split_doc(purify_doc(doc))
        subparser = self._subparsers.add_parser(name,
                                                help=cmd_help or None,
                                                description=cmd_desc or None,
                                                **kwargs)

        doc_params = find_param_docs(doc)
        self._signatures[func.__name__] = signature(func)

        for a, kw in self._analyze_func(func, doc_params):
            completer = kw.pop('completer', None)
            arg = subparser.add_argument(*a, **purify_kwargs(kw))
            if completer is not None:
                arg.completer = completer

        subparser.set_defaults(**{_DISPATCH_TO: func})
        return func

    def _analyze_func(self, func, doc_params):
        '''Analyze the given function, merging default arguments, overridden
        arguments (with @arg) and parameters extracted from the docstring.

        :param func: The function to analyze.
        :param doc_params: Parameters extracted from docstring.
        '''

        # prevent unnecessary inspect calls
        sig = self._signatures.get(func.__name__) or signature(func)
        overrides = getattr(func, '_argopts', {})
        for name, param in sig.parameters.items():

            if param.kind is param.VAR_POSITIONAL:
                kwargs = {'nargs': '*'}
                kwargs.update(doc_params.get(name, (None, {}))[1])
                yield ([name], kwargs)
                continue

            default = param.default
            if default is sig.empty:
                default = _POSITIONAL()

            opts, meta = doc_params.get(name, ([], {}))
            # check docstring for type first, then type annotation
            if meta.get('type') is None and param.annotation is not sig.empty:
                meta['type'] = param.annotation

            override = overrides.get(name, ((), {}))
            yield merge(name, default, override, opts, meta)


class Program(SubProgram):
    def __init__(self, prog=None, version=None, **kwargs):
        parser = argparse.ArgumentParser(prog, **kwargs)
        if version is not None:
            parser.add_argument('-v', '--version', action='version',
                                version=version)

        super(Program, self).__init__(parser, dict())
        self._options = None
        self._current_command = None

    # Attribute lookup fallback redirecting to (internal) options instance.
    def __getattr__(self, attr):
        return getattr(self._options, attr)

    def parse(self, args):
        '''Parse the given arguments and return a tuple ``(command, args)``,
        where ``args`` is a list consisting of all arguments. The command can
        then be called as ``command(*args)``.

        :param args: The arguments to parse.'''
        try:
            # run completion handler before parsing
            import argcomplete
            argcomplete.autocomplete(self.parser)
        except ImportError:  # pragma: no cover
            # ignore error if not installed
            pass

        self._options = self.parser.parse_args(args)
        arg_map = self._options.__dict__
        if _DISPATCH_TO not in arg_map:  # pragma: no cover
            self.parser.error("too few arguments")

        command = arg_map.pop(_DISPATCH_TO)
        sig = self._signatures[command.__name__]
        real_args = []
        for name, arg in sig.parameters.items():
            if arg.kind is arg.VAR_POSITIONAL:
                if arg_map.get(name):
                    real_args.extend(arg_map.pop(name))
            else:
                real_args.append(arg_map.pop(name))
        return command, real_args

    def execute(self, args):
        '''Parse the arguments and execute the resulting command.

        :param args: The arguments to parse.'''
        command, a = self.parse(args)
        self._current_command = command.__name__
        return command(*a)

    def __call__(self):  # pragma: no cover
        '''Parse ``sys.argv`` and execute the resulting command.'''
        return self.execute(sys.argv[1:])


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
