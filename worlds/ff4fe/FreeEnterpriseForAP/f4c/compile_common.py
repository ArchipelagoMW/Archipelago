from . import lark
from . import consts
import os

_parsers = {}
_common_grammar = None
_grammar_path = os.path.dirname(__file__)

class CompileError(Exception):
    pass

class ParseError(Exception):
    pass

def get_parser(name, start='start'):
    global _common_grammar

    if _common_grammar is None:
        with open(os.path.join(_grammar_path, 'grammar_common.lark'), 'r') as infile:
            _common_grammar = infile.read()

    key = '{}|{}'.format(name, start)
    if key not in _parsers:
        with open(os.path.join(_grammar_path, 'grammar_{}.lark').format(name), 'r') as infile:
            grammar = infile.read()

        _parsers[key] = lark.Lark(grammar + _common_grammar, start=start)

    return _parsers[key]

def snes_to_rom_address(snes_address):
    bank = (snes_address >> 16) & 0xFF
    addr = (snes_address & 0xFFFF)
    if bank == 0x7E or bank == 0x7F:
        raise ValueError("Cannot convert SNES address {:X} to ROM address : address is WRAM".format(snes_address))
    if bank >= 0x80:
        bank -= 0x80
    if addr < 0x8000:
        if bank >= 0x40 and bank <= 0x6F:
            addr += 0x8000
        else:
            raise ValueError("Cannot convert SNES address {:X} to ROM address : this address does not map to ROM".format(snes_address))
    if not (bank & 0x01):
        addr -= 0x8000
    bank = (bank >> 1)
    return ((bank << 16) | addr)

class ValueTransformer(lark.Transformer):
    def hex_number(self, n):
        v = n[0]
        return int(v[1:], 16)

    def decimal_number(self, n):
        v = n[0]
        return int(v)

    def direction_up(self, n):
        return 0

    def direction_right(self, n):
        return 1

    def direction_down(self, n):
        return 2

    def direction_left(self, n):
        return 3

    def bus_address(self, n):
        return snes_to_rom_address(n[0])

    def unheadered_rom_address(self, n):
        return n[0]

    def headered_rom_address(self, n):
        return n[0] - 0x200

_value_transformer = ValueTransformer()

def transform_values(tree):
    return _value_transformer.transform(tree)

def parse(text, grammar_name, start_symbol='start'):
    parser = get_parser(grammar_name, start_symbol)
    try:
        tree = parser.parse(text)
    except lark.common.ParseError as e:
        raise lark.common.ParseError(str(e) + ' - input:\n' + text)
    tree = transform_values(tree)
    tree = consts.resolve_consts(tree)
    return tree

