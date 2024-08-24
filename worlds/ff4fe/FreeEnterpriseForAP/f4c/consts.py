import os,inspect
from . import lark

_ROOT_FAMILY = "__"
_consts = {}

_parser = lark.Lark('''
    start           : const_block*
    const_block     : "consts" "(" identifier ")" "{" const_def* "}"
    const_def       : number identifier
    ?number         : hex_value
                    | decimal_value
    hex_value       : /\$[0-9A-Fa-f]+/
    decimal_value   : /[0-9]+/
    identifier      : /[A-Za-z_][A-Za-z0-9_]*/

    %import common.WS
    %ignore WS
    ''')

class ConstsTransformer(lark.Transformer):
    def hex_value(self, n):
        v = n[0]
        return int(v[1:], 16)
    def decimal_value(self, n):
        v = n[0]
        return int(v)
    def identifier(self, n):
        v = n[0]
        return str(v)

def load_file(const_file_path):
    with open(const_file_path, 'r') as infile:
        data = infile.read()
        load_string(data)

def load_string(const_data):
    lines = []
    for line in const_data.splitlines(True):
        lines.append(line.strip().split('//')[0])
    
    tree = _parser.parse('\n'.join(lines))

    tree = ConstsTransformer().transform(tree)

    for block in tree.children:
        if type(block.children[0] is str):
            family_name = block.children[0]
            definitions = block.children[1:]
        else:
            family_name = _ROOT_FAMILY
            definitions = block.children

        family = _consts.setdefault(family_name, {})

        for definition in definitions:
            try:
                value, identifier = definition.children
            except ValueError:
                print(definition)
                continue

            if identifier in family:
                raise ValueError("Const '{}.{}' already defined as value ${:02X}".format(family_name, identifier, family[identifier]))
            else:
                family[identifier] = value

def set_value(identifier, family, value):
    _consts.setdefault(family, {})[identifier] = value

def get_value(identifier, family=None):
    if '.' in identifier:
        family, identifier = identifier.split('.')

    if family in _consts and identifier in _consts[family]:
        return _consts[family][identifier]
    else:
        return None

def get_name(value, family):
    if family in _consts:
        for identifier in _consts[family]:
            if _consts[family][identifier] == value:
                return identifier

    return None

class ConstsResolver(lark.Transformer):
    def const(self, nodes):
        const_name = str(nodes[0])
        if '.' in const_name:
            value = get_value(const_name)
            if value is None:
                raise ValueError("Const #{} not found".format(const_name))
            return value
        else:
            # bubble up unqualified const name to see if the family can be inferred from context
            return const_name

    def __getattr__(self, name):
        if name.startswith('value_'):
            family = name[len('value_'):]
            def resolver_function(nodes):
                n = nodes[0]
                if type(n) is str:
                    value = get_value(n, family)
                    if value is None:
                        raise ValueError("Const #{} not found in family '{}'".format(n, family))
                    return value
                else:
                    return n

            return resolver_function
        else:
            return lark.Transformer.__getattribute__(self, name)

def resolve_consts(tree):
    return ConstsResolver().transform(tree)

#-------------------------------------------------------------------------------------

if __name__ == '__main__':
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    load_file(os.path.join(currentdir, 'default.consts'))
