from . import consts
from . import compile_common
import re

HEX_REGEX = re.compile(r'^\$[A-Fa-f0-9]+$')
DEC_REGEX = re.compile(r'^[0-9]+$')
IDENTIFIER_REGEX = re.compile(r'^[A-Za-z_][A-Za-z_0-9]*$')

def process_consts_block(block, rom, env):
    family = block['parameters'].strip()

    tokens = block['body'].split()
    for i in range(0, len(tokens), 2):
        if i + 1 >= len(tokens):
            raise compile_common.ParseError('Expected identifier after "{}" in const definition (family "{}")'.format(tokens[i], family))

        if HEX_REGEX.match(tokens[i]):
            value = int(tokens[i][1:], 16)
        elif DEC_REGEX.match(tokens[i]):
            value = int(tokens[i])
        else:
            raise compile_common.ParseError('Expected value, got "{}" in const definition (family "{}")'.format(tokens[i], family))

        if not IDENTIFIER_REGEX.match(tokens[i+1]):
            raise compile_common.ParseError('Invalid identifier name "{}" in const definition (family "{}")'.format(tokens[i+1], family))

        consts.set_value(tokens[i+1], family, value)

