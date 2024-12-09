from . import consts

_DIRECTIONS = ['up', 'right', 'down', 'left']

def value_text(value, const_family=None, hex=True):
    if const_family == 'direction':
        return _DIRECTIONS[value]

    if const_family is not None:
        name = consts.get_name(value, const_family)
        if name is not None:
            return '#{}'.format(name)

    if hex:
        return '${:02X}'.format(value)
    else:
        return '{}'.format(value)

