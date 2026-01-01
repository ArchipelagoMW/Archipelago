import json

from functools import reduce

INDENT = '  '

class CollapseList(list):
    pass
class CollapseDict(dict):
    pass
class AlignedDict(dict):
    def __init__(self, src_dict, depth):
        self.depth = depth - 1
        super().__init__(src_dict)
class SortedDict(dict):
    pass


def is_scalar(value):
    return not is_list(value) and not is_dict(value)


def is_list(value):
    return isinstance(value, list) or isinstance(value, tuple)


def is_dict(value):
    return isinstance(value, dict)


def dump_scalar(obj, ensure_ascii=False):
    return json.dumps(obj, ensure_ascii=ensure_ascii)


def dump_list(obj, current_indent='', ensure_ascii=False):
    entries = [dump_obj(value, current_indent + INDENT, ensure_ascii=ensure_ascii) for value in obj]

    if len(entries) == 0:
        return '[]'

    if isinstance(obj, CollapseList):
        values_format = '{value}'
        output_format = '[{values}]'
        join_format   = ', '
    else:
        values_format = '{indent}{value}'
        output_format = '[\n{values}\n{indent}]'
        join_format   = ',\n'

    output = output_format.format(
        indent=current_indent,
        values=join_format.join([values_format.format(
            value=entry,
            indent=current_indent + INDENT
        ) for entry in entries])
    )

    return output


def get_keys(obj, depth):
    if depth == 0:
        yield from obj.keys()
    else:
        for value in obj.values():
            yield from get_keys(value, depth - 1)


def dump_dict(obj, current_indent='', sub_width=None, ensure_ascii=False):
    entries = []

    key_width = None
    if sub_width is not None:
        sub_width = (sub_width[0]-1, sub_width[1])
        if sub_width[0] == 0:
            key_width = sub_width[1]

    if isinstance(obj, AlignedDict):
        sub_keys = get_keys(obj, obj.depth)
        sub_width = (obj.depth, reduce(lambda acc, entry: max(acc, len(entry)), sub_keys, 0))

    for key, value in obj.items():        
        entries.append((dump_scalar(str(key), ensure_ascii), dump_obj(value, current_indent + INDENT, sub_width, ensure_ascii)))

    if key_width is None:
        key_width = reduce(lambda acc, entry: max(acc, len(entry[0])), entries, 0)

    if len(entries) == 0:
        return '{}'

    if isinstance(obj, SortedDict):
        entries.sort(key=lambda item: item[0])

    if isinstance(obj, CollapseDict):
        values_format = '{key} {value}'
        output_format = '{{{values}}}'
        join_format   = ', '
    else:
        values_format = '{indent}{key:{padding}}{value}'
        output_format = '{{\n{values}\n{indent}}}'
        join_format   = ',\n'

    output = output_format.format(
        indent=current_indent,
        values=join_format.join([values_format.format(
            key='{key}:'.format(key=key), 
            value=value,
            indent=current_indent + INDENT,
            padding=key_width + 2,
        ) for (key, value) in entries])
    )

    return output


def dump_obj(obj, current_indent='', sub_width=None, ensure_ascii=False):
    if is_list(obj):
        return dump_list(obj, current_indent, ensure_ascii)
    elif is_dict(obj):
        return dump_dict(obj, current_indent, sub_width, ensure_ascii)
    else:
        return dump_scalar(obj, ensure_ascii)
