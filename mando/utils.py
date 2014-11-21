import re

PARAM_RE = re.compile(r"^([\t ]*):param (.*?): (.*\n(\1[ \t]+.*\n*)*)",
                      re.MULTILINE)
ARG_RE = re.compile(r'-(?P<long>-)?(?P<key>(?(long)[^ =,]+|.))[ =]?'
                    '(?P<meta>[^ ,]+)?')
POS_RE = re.compile(r'(?P<meta>[^ ,]+)?')
ARG_TYPE_MAP = {
    'n': int, 'num': int, 'number': int,
    'i': int, 'int': int, 'integer': int,
    's': str, 'str': str, 'string': str,
    'f': float, 'float': float,
    None: None, '': None,
}


def purify_doc(string):
    '''Remove Sphinx's :param: lines from the docstring.'''
    return PARAM_RE.sub('', string).rstrip()


def split_doc(string):
    '''Split the documentation into help and description.

    A two-value list is returned, of the form ``[help, desc]``. If no
    description is provided, the help is duplicated.'''
    parts = [part.strip() for part in string.split('\n\n', 1)]
    if len(parts) == 1:
        return parts * 2
    return parts


def purify_kwargs(kwargs):
    '''If type or metavar are set to None, they are removed from kwargs.'''
    for key, value in kwargs.copy().items():
        if key in set(['type', 'metavar']) and value is None:
            del kwargs[key]
    return kwargs


def find_param_docs(docstring):
    '''Find Sphinx's :param: lines and return a dictionary of the form:
        ``param: (opts, {metavar: meta, type: type, help: help})``.'''
    paramdocs = {}
    for _, param, value, _ in PARAM_RE.findall(docstring + '\n'):
        name, opts, meta = get_opts(param.strip())
        name = name.replace('-', '_')
        paramdocs[name] = (opts, {
            'metavar': meta or None,
            'type': ARG_TYPE_MAP.get(meta.strip('<>')),
            'help': value.rstrip(),
        })
    return paramdocs


def get_opts(param):
    '''Extract options from a parameter name.'''
    if param.startswith('-'):
        opts = []
        names = []
        meta = None
        for long, name, meta in ARG_RE.findall(param):
            prefix = ['-', '--'][len(long)]
            opts.append('{0}{1}'.format(prefix, name))
            names.append(name)
        return max(names, key=len), opts, meta
    opt, meta = (list(filter(None, POS_RE.findall(param))) + [''])[:2]
    return opt, [opt], meta


def action_by_type(obj):
    '''Determine an action and a type for the given object if possible.'''
    kw = {}
    if isinstance(obj, bool):
        return {'action': ['store_true', 'store_false'][obj]}
    elif isinstance(obj, list):
        kw = {'action': 'append'}
    kw.update(get_type(obj))
    return kw


def get_type(obj):
    '''Determine the type of the object if among some of the built-in ones.'''
    otype = type(obj)
    if any(otype is t for t in set([int, float, str, bool])):
        return {'type': otype}
    return {}


def ensure_dashes(opts):
    '''Ensure that the options have the right number of dashes.'''
    for opt in opts:
        if opt.startswith('-'):
            yield opt
        else:
            yield '-' * (1 + 1 * (len(opt) > 1)) + opt
