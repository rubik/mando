def purify_kwargs(kwargs):
    """If type or metavar are set to None, they are removed from kwargs."""
    for key, value in kwargs.copy().items():
        if key in ["type", "metavar"] and value is None:
            del kwargs[key]
    return kwargs


def action_by_type(obj):
    """Determine an action and a type for the given object if possible."""
    kw = {}
    if isinstance(obj, bool):
        return {"action": ["store_true", "store_false"][obj]}
    elif isinstance(obj, list):
        kw = {"action": "append"}
    kw.update(get_type(obj))
    return kw


def get_type(obj):
    """Determine the type of the object if among some of the built-in ones."""
    otype = type(obj)
    if any(otype is t for t in set([int, float, str, bool])):
        return {"type": otype}
    return {}


def ensure_dashes(opts):
    """Ensure that the options have the right number of dashes."""
    for opt in opts:
        if opt.startswith("-"):
            yield opt
        else:
            yield "-" * (1 + 1 * (len(opt) > 1)) + opt
