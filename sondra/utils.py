import inspect
import re
from copy import deepcopy

def convert_camelcase(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def camelcase_slugify(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()


def mapjson(fun, doc):
    if isinstance(doc, dict):
        return {k: mapjson(fun, v) for k, v in doc.items()}
    elif isinstance(doc, list):
        return [mapjson(fun, v) for v in doc]
    else:
        return fun(doc)


def is_exposed(fun):
    return inspect.ismethod(fun) and hasattr(fun, 'exposed')


def schema_with_properties(original, **updates):
    new_schema = deepcopy(original)
    new_schema['properties'].update(updates)
    return new_schema


def schema_sans_properties(original, *properties):
    new_schema = deepcopy(original)
    for property in (p for p in properties if p in new_schema['properties']):
        del new_schema['properties'][property]
    return new_schema


def schema_with_definitions(original, **updates):
    new_schema = deepcopy(original)
    new_schema['definitions'].update(updates)
    return new_schema


def schema_sans_definitions(original, *properties):
    new_schema = deepcopy(original)
    for property in (p for p in properties if p in new_schema['definitions']):
        del new_schema['definitions'][property]
    return new_schema