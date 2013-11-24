import re

PARAM_RE = re.compile(r"^([\t ]*):param (.*?): ([^\n]*\n(\1[ \t]+[^\n]*\n)*)",
                                            re.MULTILINE)
ARG_RE = re.compile(r'-(?P<long>-)?(?P<key>(?(long)[^ =,]+|.))[ =]?(?P<meta>[^ ,]+)?')
POS_RE = re.compile(r'(?P<meta>[^ ,]+)?')
ARG_TYPE_MAP = {
    'n': int, 'num': int, 'number': int,
    'i': int, 'int': int, 'integer': int,
    's': str, 'str': str, 'string': str,
    'f': float, 'float': float,
    None: None, '': None,
}

def normalize_spaces(string):
    return re.sub(r'[\r\t\n ]+', ' ', string)


def find_param_docs(docstring):
    #if not docstring.endswith('\n'):
    paramdocs = {}
    for _, param, value, _ in PARAM_RE.findall(docstring + '\n'):
        name, opts, meta = get_opts(param.strip())
        name = name.replace('-', '_')
        paramdocs[name] = (opts, {
            'type': ARG_TYPE_MAP[meta.strip('<>')],
            'help': normalize_spaces(value).rstrip(),
        })
    return paramdocs


def get_opts(param):
    if param.startswith('-'):
        opts = []
        names = []
        for long, name, meta in ARG_RE.findall(param):
            prefix = ['-', '--'][len(long)]
            opts.append('{0}{1}'.format(prefix, name))
            names.append(name)
        return max(names, key=len), opts, meta
    opt, meta = (list(filter(None, POS_RE.findall(param))) + [''])[:2]
    return opt, [opt], meta


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
