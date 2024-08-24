import re
import os
import math
import hashlib
import pickle

try:
    from . import ff4struct
    from . import lark
except ImportError:
    import ff4struct
    import lark

_msf_parser = None
_expr_transformer = None

_PART_SIZES = {
    'byte'  : 1,
    'short' : 2,
    'long'  : 3,
    'high'  : 1,
    'bank'  : 1
}

_OPERATIONS = {
    '+' : (lambda x, y: x + y),
    '-' : (lambda x, y: x - y),
    '*' : (lambda x, y: x * y),
    '/' : (lambda x, y: x // y),
    '%' : (lambda x, y: x % y),
    '&' : (lambda x, y: x & y),
    '|' : (lambda x, y: x | y),
    '^' : (lambda x, y: x ^ y),
    '>>' : (lambda x, y: x >> y),
    '<<' : (lambda x, y: x << y),
}

def _extract_part(value, part):
    if part == 'byte':
        return (value & 0xFF)
    elif part == 'short':
        return (value & 0xFFFF)
    elif part == 'long':
        return (value)
    elif part == 'high':
        return (value >> 8) & 0xFF
    elif part == 'bank':
        return (value >> 16) & 0xFF
    else:
        raise ValueError(f"Unknown numeric part name {part}")

def _load_parser():
    global _msf_parser
    if _msf_parser is None:
        with open(os.path.join(os.path.dirname(__file__), "grammar_myselfpatch.lark"), 'r') as infile:
            _msf_parser = lark.Lark(infile.read())

    global _expr_transformer
    if _expr_transformer is None:
        _expr_transformer = ExpressionTransformer()

def _build_expr_tree(parse_tree):
    if type(parse_tree)  is lark.lexer.Token:
        return str(parse_tree)
    elif type(parse_tree) is not lark.Tree:
        return parse_tree

    return _expr_transformer.transform(parse_tree)

def _format_expr_tree(tree):
    if type(tree) in (list, tuple):
        return f'({_format_expr_tree(tree[1])}{tree[0]}{_format_expr_tree(tree[2])})'
    else:
        return str(tree)

def _resolve_expr_tree(tree, definitions):
    if type(tree) is str:
        if tree not in definitions:
            raise ValueError(f"{tree} is not defined")
        return definitions[tree]
    elif type(tree) in (list, tuple):
        op = tree[0]
        if op not in _OPERATIONS:
            raise ValueError(f"Expression operation {op} is not supported")
        return _OPERATIONS[op](*[_resolve_expr_tree(t, definitions) for t in tree[1:]])
    else:
        return tree

class ExpressionTransformer(lark.Transformer):
    def expr_passthrough(self, n):
        return n[0]
    
    def expr_binary_op(self, n):
        left_operand,op,right_operand = n
        return [str(op), left_operand, right_operand]
    
    def decimal_number(self, n):
        return int(n[0])

    def hex_number(self, n):
        if n[0].startswith('$'):
            return int(n[0][1:], 16)
        elif n[0].startswith('0x'):
            return int(n[0][2:], 16)
        else:
            raise ValueError(f'Malformed hex number {n[0]}')

    def expr_identifier(self, n):
        return str(n[0])

class CompiledBlock:
    def __init__(self):
        self.address = None
        self.data = []
        self.definitions = {}
        self.labels = {}
        self.expressions = []
        self.label_branch_references = []

    def as_dict(self):
        print(self.labels)
        return {
            'address' : self.address,
            'data' : self.data,
            'definitions' : self.definitions,
            'labels' : self.labels,
            'expressions' : self.expressions,
            'label_branch_references' : self.label_branch_references,
            }

    def from_dict(self, d):
        self.address = d['address']
        self.data = d['data']
        self.definitions = d['definitions']
        self.labels = d['labels']
        self.expressions = d['expressions']
        self.label_branch_references = d['label_branch_references']

    def set_address(self, addr):
        self.address = addr

    def add_definition(self, name, value):
        self.definitions[name] = value

    def set_label_at_current_location(self, label_name, local=False):
        self.labels[label_name] = (len(self.data), local)

    def add_expression(self, tree, part, size=None):
        if size is None:
            size = _PART_SIZES[part]

        self.expressions.append( {
            'tree' : tree, 
            'part' : part, 
            'size' : size,
            'position' : len(self.data)
            } )    

        self.data.extend([None] * size)

    def add_label_branch_reference(self, label_name, byte_size=1):
        self.label_branch_references.append( {
            'label' : label_name,
            'size' : byte_size,
            'position' : len(self.data)
            })
        self.data.extend([None] * byte_size)

    def resolve_branch_references(self):
        for ref in self.label_branch_references:
            label_name = ref['label']
            if label_name not in self.labels:
                raise ValueError("Cannot branch to label '{}' -- label not found in same patch block".format(label_name))

            position = ref['position']
            # position points to the byte before the next instruction;
            # the next instruction is the reference for the offset
            offset = self.labels[label_name][0] - (position + 1)
            offset_min = -(1 << (ref['size'] * 8 - 1))
            offset_max = -offset_min - 1

            if offset > offset_max or offset < offset_min:
                raise ValueError("Branch to label '{}' is out of range (offset {})".format(label_name, offset))

            if offset < 0:
                offset = (1 << (ref['size'] * 8)) + offset

            for i in range(ref['size']):
                b = (offset >> (i * 8)) & 0xFF
                self.data[ref['position'] + i] = b

    def resolve_expressions(self, definitions):
        for expr in self.expressions:
            value = _extract_part(_resolve_expr_tree(expr['tree'], definitions), expr['part'])

            for i in range(expr['size']):
                b = (value >> (i * 8)) & 0xFF
                self.data[expr['position'] + i] = b

    def pretty_print(self):
        if self.address is None:
            print('unlocated block')
        else:
            print('block at address: {:X}'.format(self.address))
        parts = []
        for i,b in enumerate(self.data):
            if b is None:
                for expr in self.expressions:
                    if i == expr['position']:
                        parts.append(f"[{expr['part']}:{_format_expr_tree(expr['tree'])}] ")
            else:
                parts.append(f'{b:02X} ')

            if (i + 1) % 16 == 0:
                parts.append('\n')

        print(''.join(parts))

def save_precompiled_blocks(path, *compiled_blocks):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    with open(path, 'wb') as outfile:
        pickle.dump(compiled_blocks, outfile)

def load_precompiled_blocks(path):
    with open(path, 'rb') as infile:
        compiled_blocks = pickle.load(infile)
    return compiled_blocks

def process_msfpatch_block(block, rom, env):
    # check for precompiled version
    if env and env.cache:
        cache_name = env.cache.get_block_cache_name(block)
        if not env.options.force_recompile:
            precompiled_blocks = env.cache.load(cache_name)
            if precompiled_blocks is not None:
                env.postprocess.register(_postprocess_msfpatches, *precompiled_blocks)
                return

    _load_parser()

    try:
        tree = _msf_parser.parse(block['body'])
    except lark.common.ParseError as e:
        print(block['body'])
        raise e

    current_block = CompiledBlock()
    compiled_blocks = [ current_block ]
    a_size = 1
    xy_size = 2

    def num_value(node):
        if node.data == 'decimal_number':
            return int(str(node.children[0])), None
        elif node.data == 'direct_patch_address':
            return int(str(node.children[0]), 16), None
        else:
            s = str(node.children[0])
            if s.startswith('$'):
                s = s[1:]
            if s.startswith('0x'):
                s = s[2:]

            return int(s, 16), int(math.ceil(len(s) / 2.0))

    for item in tree.children:
        if item.data == 'label':
            current_block.set_label_at_current_location(str(item.children[0]))
        elif item.data == 'local_label':
            current_block.set_label_at_current_location(str(item.children[0]), local=True)
        elif item.data == 'directive':
            directive = item.children[0]
            if directive == '.mx':
                param, dummy = num_value(item.children[1])
                a_size = (1 if (param & 0x20) else 2)
                xy_size = (1 if (param & 0x10) else 2)
            elif directive == '.addr' or directive == '.new':
                if directive == '.addr':
                    addr, dummy = num_value(item.children[1])
                else:
                    addr = None

                if len(current_block.data) > 0:
                    current_block = CompiledBlock()
                    compiled_blocks.append(current_block)

                if addr is not None:
                    current_block.set_address(addr)
            elif directive == '.def':
                if len(item.children) < 3:
                    raise ValueError(".def directive for '{}' is missing value".format(param))
                current_block.add_definition(str(item.children[1]), num_value(item.children[2])[0])
            else:
                raise ValueError("Unsupported directive '{}'".format(directive))
        elif item.data == 'command':
            op = str(item.children[0])
            if op not in OPCODES:
                raise ValueError("Could not find operation '{}' -- command parse tree {}".format(op, str(item)))

            op_info = OPCODES[op]
            if type(op_info) is int:
                # this is an opcode with no parameters
                if len(item.children) > 1:
                    raise ValueError("Operation '{}' called with parameters but does not use them -- command parse tree {}".format(op, str(item)))
                current_block.data.append(op_info)
            elif len(item.children) < 2:
                raise ValueError("Operation '{}' requires parameters but none were provided -- command parse tree".format(op, str(item)))
            else:
                param = item.children[1]

                param_values = []

                if param.data == 'branch_label':
                    param_value = str(param.children[0])
                    if 'pcr long' in op_info:
                        slug = 'pcr long'
                        param_size = 2
                    else:
                        slug = 'pcr'
                        param_size = 1
                    param_values.append( ('branch', param_value, param_size) )
                else:
                    slug = param.data.replace('_', ' ')

                    for param_child in param.children:
                        if param_child.data == 'address_expression':
                            param_type = 'expression'
                            part = param_child.children[0].data.rsplit('_', maxsplit=1)[-1]
                            param_size = _PART_SIZES[part]

                            param_value = {
                                'part' : part,
                                'tree' : _build_expr_tree(param_child.children[1])
                            }
                        else:
                            param_type = 'literal'
                            param_value, param_size = num_value(param_child)

                        # set param size automatically for commands that have a variable argument size
                        if param.data == 'immediate':
                            if op in VARIABLE_SIZE_OPS:
                                if VARIABLE_SIZE_OPS[op] == 'a':
                                    param_size = a_size
                                elif VARIABLE_SIZE_OPS[op] == 'xy':
                                    param_size = xy_size
                                else:
                                    raise ValueError("Don't know how to find size of register '{}'".format(VARIABLE_SIZE_OPS[op]))

                        param_values.append( (param_type, param_value, param_size) )

                    if param.data == 'block':
                        # in assembly, parameters are SRC BANK, DST BANK
                        # but in the object code DST comes first
                        param_values.reverse()

                if slug.startswith('addr'):
                    ADDR_NAMES = { 1: 'dp', 2: 'absolute', 3: 'absolute long'}
                    slug = ADDR_NAMES[param_size] + slug[4:]

                if slug not in op_info:
                    if slug == 'dp':
                        slug = 'pcr'
                    elif slug == 'absolute':
                        slug = 'pcr long'

                if slug not in op_info:
                    raise ValueError("Could not find operation '{}' matching parameter format '{}' -- command parse tree {}".format(op, slug, str(item)))

                opcode = op_info[slug]
                current_block.data.append(opcode)

                for param_type,param_value,param_size in param_values:
                    if param_type == 'literal':
                        for i in range(param_size):
                            b = (param_value >> (i * 8)) & 0xFF
                            current_block.data.append(b)
                    elif param_type == 'expression':
                        current_block.add_expression(param_value['tree'], param_value['part'], param_size)
                    elif param_type == 'branch':
                        current_block.add_label_branch_reference(param_value, param_size)
                    else:
                        raise ValueError(f"Unhandled param type '{param_type}'")

        elif item.data == 'direct_patch':
            patch_block = CompiledBlock()
            patch_block.set_address(num_value(item.children[0])[0])
            patch_block.data.append(num_value(item.children[1])[0])
            compiled_blocks.append(patch_block)

        elif item.data == 'raw_data':
            for subitem in item.children:
                if subitem.data == 'raw_byte':
                    current_block.data.append(int(str(subitem.children[0]), 16))
                else:
                    part = subitem.children[0].data.rsplit('_', maxsplit=1)[-1]
                    expr_tree = _build_expr_tree(subitem.children[1])
                    current_block.add_expression(expr_tree, part)

        elif item.data == 'string':
            text = str(item.children[0])[1:-1]
            encoded_text = ff4struct.text.encode(text, allow_dual_char=False)
            if encoded_text and encoded_text[-1] == 0:
                encoded_text.pop()
            current_block.data.extend(encoded_text)
        
    for block in compiled_blocks:
        block.resolve_branch_references()

    if env:
        if env.cache:
            env.cache.save(cache_name, compiled_blocks)

        env.postprocess.register(_postprocess_msfpatches, *compiled_blocks)

    return compiled_blocks

def _rom_to_snes_address(rom_address):
    bank = (rom_address >> 15)
    addr = (rom_address & 0x7FFF) | 0x8000
    if bank == 0x7E or bank == 0x7F:
        bank += 0x80
    return (bank << 16) | addr

def _snes_to_rom_address(snes_address):
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


def _postprocess_msfpatches(env, blocks):
    if env.options.shuffle_msfpatches:
        blocks = list(blocks)
        env.rnd.shuffle(blocks)

    # assign addresses to all new code blocks
    new_code_address = _rom_to_snes_address(0x100000) # TODO: get number from ROM?
    for block in blocks:
        if block.address is None:
            # TODO: test if block will cross bank boundaries?
            block.address = new_code_address
            new_code_address += len(block.data)

    # build global name tables
    global_definitions = {}
    block_definitions = []

    for block in blocks:
        local_definitions = {}
        block_definitions.append(local_definitions)

        for name in block.definitions:
            if name in global_definitions:
                raise ValueError("Duplicate definition for symbol '{}' in MSF patches".format(name))
            global_definitions[name] = block.definitions[name]

        for name in block.labels:
            value = block.address + block.labels[name][0]
            local = block.labels[name][1]
            if not local:
                if name in global_definitions:
                    raise ValueError("Duplicate definition for symbol '{}' in MSF patches".format(name))
                global_definitions[name] = value
            else:
                if name in local_definitions:
                    raise ValueError("Duplicate definition for symbol '{}' in MSF patches".format(name))
                local_definitions[name] = value

    # resolve expressions
    for i,block in enumerate(blocks):
        block.resolve_expressions({**global_definitions, **block_definitions[i]})

    # add raw patches to ROM
    for block in blocks:
        if env:
            env.rom.add_patch(_snes_to_rom_address(block.address), block.data)
        else:
            block.pretty_print()

    env.reports['symbols'] = global_definitions

#----------------------------------------------------

OPCODES = {
    'adc' : {
        'dp x indirect'         : 0x61,
        'sr'                    : 0x63,
        'dp'                    : 0x65,
        'dp indirect long'      : 0x67,
        'immediate'             : 0x69,
        'absolute'              : 0x6D,
        'absolute long'         : 0x6F,
        'dp indirect y'         : 0x71,
        'dp indirect'           : 0x72,
        'sr indirect y'         : 0x73,
        'dp x'                  : 0x75,
        'dp indirect long y'    : 0x77,
        'absolute y'            : 0x79,
        'absolute x'            : 0x7D,
        'absolute long x'       : 0x7F,
    },
    'and' : {
        'dp x indirect'         : 0x21,
        'sr'                    : 0x23,
        'dp'                    : 0x25,
        'dp indirect long'      : 0x27,
        'immediate'             : 0x29,
        'absolute'              : 0x2D,
        'absolute long'         : 0x2F,
        'dp indirect y'         : 0x31,
        'dp indirect'           : 0x32,
        'sr indirect y'         : 0x33,
        'dp x'                  : 0x35,
        'dp indirect long y'    : 0x37,
        'absolute y'            : 0x39,
        'absolute x'            : 0x3D,
        'absolute long x'       : 0x3F,
    },
    'asl' : {
        'dp'                    : 0x06,
        'a'                     : 0x0A,
        'absolute'              : 0x0E,
        'dp x'                  : 0x16,
        'absolute x'            : 0x1E,
    },
    'bcc' : { 'pcr' : 0x90 },
    'blt' : { 'pcr' : 0x90 },
    'bcs' : { 'pcr' : 0xB0 },
    'bge' : { 'pcr' : 0xB0 },
    'beq' : { 'pcr' : 0xF0 },
    'bit' : {
        'dp'                    : 0x24,
        'absolute'              : 0x2C,
        'dp x'                  : 0x34,
        'absolute x'            : 0x3C,
        'immediate'             : 0x89,
    },
    'bmi' : { 'pcr' : 0x30 },
    'bne' : { 'pcr' : 0xD0 },
    'bpl' : { 'pcr' : 0x10 },
    'bra' : { 'pcr' : 0x80 },
    'brk' : 0x00,
    'brl' : { 'pcr long' : 0x82 },
    'bvc' : { 'pcr' : 0x50 },
    'bvs' : { 'pcr' : 0x70 },
    'clc' : 0x18,
    'cld' : 0xD8,
    'cli' : 0x58,
    'clv' : 0xB8,
    'cmp' : {
        'dp x indirect'         : 0xC1,
        'sr'                    : 0xC3,
        'dp'                    : 0xC5,
        'dp indirect long'      : 0xC7,
        'immediate'             : 0xC9,
        'absolute'              : 0xCD,
        'absolute long'         : 0xCF,
        'dp indirect y'         : 0xD1,
        'dp indirect'           : 0xD2,
        'sr indirect y'         : 0xD3,
        'dp x'                  : 0xD5,
        'dp indirect long y'    : 0xD7,
        'absolute y'            : 0xD9,
        'absolute x'            : 0xDD,
        'absolute long x'       : 0xDF,
    },
    'cop' : { 'interrupt' : 0x02 },
    'cpx' : {
        'immediate'             : 0xE0,
        'dp'                    : 0xE4,
        'absolute'              : 0xEC,
    },
    'cpy' : {
        'immediate'             : 0xC0,
        'dp'                    : 0xC4,
        'absolute'              : 0xCC,
    },
    'dec' : {
        'a'                     : 0x3A,
        'dp'                    : 0xC6,
        'absolute'              : 0xCE,
        'dp x'                  : 0xD6,
        'absolute x'            : 0xDE,
    },
    'dea' : 0x3A,
    'dex' : 0xCA,
    'dey' : 0x88,
    'eor' : {
        'dp x indirect'         : 0x41,
        'sr'                    : 0x43,
        'dp'                    : 0x45,
        'dp indirect long'      : 0x47,
        'immediate'             : 0x49,
        'absolute'              : 0x4D,
        'absolute long'         : 0x4F,
        'dp indirect y'         : 0x51,
        'dp indirect'           : 0x52,
        'sr indirect y'         : 0x53,
        'dp x'                  : 0x55,
        'dp indirect long y'    : 0x57,
        'absolute y'            : 0x59,
        'absolute x'            : 0x5D,
        'absolute long x'       : 0x5F,    
    },
    'inc' : {
        'a'                     : 0x1A,
        'dp'                    : 0xE6,
        'absolute'              : 0xEE,
        'dp x'                  : 0xF6,
        'absolute x'            : 0xFE,
    },
    'ina' : 0x1A,
    'inx' : 0xE8,
    'iny' : 0xC8,
    'jmp' : {
        'absolute'              : 0x4C,
        'absolute long'         : 0x5C,
        'absolute indirect'     : 0x6C,
        'absolute x indirect'   : 0x7C,
        'absolute indirect long': 0xDC,
    },
    'jml' : {
        'absolute long'         : 0x5C,
        'absolute indirect long': 0xDC,
    },
    'jsr' : {
        'absolute'              : 0x20,
        'absolute long'         : 0x22,
        'absolute x indirect'   : 0xFC,
    },
    'jsl' : {
        'absolute long'         : 0x22,    
    },
    'lda' : {
        'dp x indirect'         : 0xA1,
        'sr'                    : 0xA3,
        'dp'                    : 0xA5,
        'dp indirect long'      : 0xA7,
        'immediate'             : 0xA9,
        'absolute'              : 0xAD,
        'absolute long'         : 0xAF,
        'dp indirect y'         : 0xB1,
        'dp indirect'           : 0xB2,
        'sr indirect y'         : 0xB3,
        'dp x'                  : 0xB5,
        'dp indirect long y'    : 0xB7,
        'absolute y'            : 0xB9,
        'absolute x'            : 0xBD,
        'absolute long x'       : 0xBF,
    },
    'ldx' : {
        'immediate'             : 0xA2,
        'dp'                    : 0xA6,
        'absolute'              : 0xAE,
        'dp y'                  : 0xB6,
        'absolute y'            : 0xBE,
    },
    'ldy' : {
        'immediate'             : 0xA0,
        'dp'                    : 0xA4,
        'absolute'              : 0xAC,
        'dp x'                  : 0xB4,
        'absolute x'            : 0xBC,
    },
    'lsr' : {
        'dp'                    : 0x46,
        'a'                     : 0x4A,
        'absolute'              : 0x4E,
        'dp x'                  : 0x56,
        'absolute x'            : 0x5E,
    },
    'mvn' : { 'block' : 0x54 },
    'mvp' : { 'block' : 0x44 },
    'nop' : 0xEA,
    'ora' : {
        'dp x indirect'         : 0x01,
        'sr'                    : 0x03,
        'dp'                    : 0x05,
        'dp indirect long'      : 0x07,
        'immediate'             : 0x09,
        'absolute'              : 0x0D,
        'absolute long'         : 0x0F,
        'dp indirect y'         : 0x11,
        'dp indirect'           : 0x12,
        'sr indirect y'         : 0x13,
        'dp x'                  : 0x15,
        'dp indirect long y'    : 0x17,
        'absolute y'            : 0x19,
        'absolute x'            : 0x1D,
        'absolute long x'       : 0x1F,
    },
    'pea' : { 'absolute' : 0xF4 },
    'pei' : { 'dp' : 0xD4 },
    'per' : { 'pcr' : 0x62 },
    'pha' : 0x48,
    'phb' : 0x8B,
    'phd' : 0x0B,
    'phk' : 0x4B,
    'php' : 0x08,
    'phx' : 0xDA,
    'phy' : 0x5A,
    'pla' : 0x68,
    'plb' : 0xAB,
    'pld' : 0x2B,
    'plp' : 0x28,
    'plx' : 0xFA,
    'ply' : 0x7A,
    'rep' : { 'immediate' : 0xC2 },
    'rol' : {
        'dp'                    : 0x26,
        'a'                     : 0x2A,
        'absolute'              : 0x2E,
        'dp x'                  : 0x36,
        'absolute x'            : 0x3E,        
    },
    'ror' : {
        'dp'                    : 0x66,
        'a'                     : 0x6A,
        'absolute'              : 0x6E,
        'dp x'                  : 0x76,
        'absolute x'            : 0x7E,        
    },
    'rti' : 0x40,
    'rtl' : 0x6B,
    'rts' : 0x60,
    'sbc' : {
        'dp x indirect'         : 0xE1,
        'sr'                    : 0xE3,
        'dp'                    : 0xE5,
        'dp indirect long'      : 0xE7,
        'immediate'             : 0xE9,
        'absolute'              : 0xED,
        'absolute long'         : 0xEF,
        'dp indirect y'         : 0xF1,
        'dp indirect'           : 0xF2,
        'sr indirect y'         : 0xF3,
        'dp x'                  : 0xF5,
        'dp indirect long y'    : 0xF7,
        'absolute y'            : 0xF9,
        'absolute x'            : 0xFD,
        'absolute long x'       : 0xFF,
    },
    'sec' : 0x38,
    'sed' : 0xF8,
    'sei' : 0x78,
    'sep' : { 'immediate' : 0xE2 },
    'sta' : {
        'dp x indirect'         : 0x81,
        'sr'                    : 0x83,
        'dp'                    : 0x85,
        'dp indirect long'      : 0x87,
        'absolute'              : 0x8D,
        'absolute long'         : 0x8F,
        'dp indirect y'         : 0x91,
        'dp indirect'           : 0x92,
        'sr indirect y'         : 0x93,
        'dp x'                  : 0x95,
        'dp indirect long y'    : 0x97,
        'absolute y'            : 0x99,
        'absolute x'            : 0x9D,
        'absolute long x'       : 0x9F,
    },
    'stp' : 0xDB,
    'stx' : {
        'dp'                    : 0x86,
        'absolute'              : 0x8E,
        'dp y'                  : 0x96,
    },
    'sty' : {
        'dp'                    : 0x84,
        'absolute'              : 0x8C,
        'dp x'                  : 0x94,
    },
    'stz' : {
        'dp'                    : 0x64,
        'dp x'                  : 0x74,
        'absolute'              : 0x9C,
        'absolute x'            : 0x9E,
    },
    'tax' : 0xAA,
    'tay' : 0xA8,
    'tcd' : 0x5B,
    'tcs' : 0x1B,
    'tdc' : 0x7B,
    'trb' : {
        'dp'                    : 0x14,
        'absolute'              : 0x1C,
    },
    'tsb' : {
        'dp'                    : 0x04,
        'absolute'              : 0x0C,
    },
    'tsc' : 0x3B,
    'tsx' : 0xBA,
    'txa' : 0x8A,
    'txs' : 0x9A,
    'txy' : 0x9B,
    'tya' : 0x98,
    'tyx' : 0xBB,
    'wai' : 0xCB,
    'wdm' : 0x42,
    'xba' : 0xEB,
    'xce' : 0xFB
}

VARIABLE_SIZE_OPS = {
    'adc' : 'a',
    'and' : 'a',
    'bit' : 'a',
    'cmp' : 'a',
    'cpx' : 'xy',
    'cpy' : 'xy',
    'eor' : 'a',
    'lda' : 'a',
    'ldx' : 'xy',
    'ldy' : 'xy',
    'ora' : 'a',
    'sbc' : 'a'
}

#----------------------------------------------------

def _test_check_opcodes():
    codes = {}
    def add_code(opcode, description):
        if opcode in codes:
            print("Duplicate opcode found for {} -- already set as {}".format(description, codes[opcode]))
        else:
            codes[opcode] = description

    for k in OPCODES:
        data = OPCODES[k]
        if type(data) is int:
            add_code(data, k)
        else:
            for p in data:
                add_code(data[p], k + " " + p)

    for c in range(256):
        if c not in codes:
            print("Could not find opcode {:2X}".format(c))

def _test_original_myself_patches():
    # this needs to be updated for the new CompileEnvironment paradigm
    filenames = [
        '../reference/myselfpatches/Indoor_Dash.txt',
        '../reference/myselfpatches/PatchIndoor.txt',
        '../reference/myselfpatches/FastMenu.txt',
        '../reference/myselfpatches/PatchFastMenu.txt',
        '../reference/myselfpatches/LongCall.txt',
    ]

    for filename in filenames:
        lines = []
        with open(filename, 'r') as infile:
            for line in infile:
                lines.append(re.sub(r'//.*$', '', line.rstrip()))

        block = { 'body' : '\n'.join(lines) }
        process_msfpatch_block(block, None,)

    compile_postprocess.apply_registered_processes(None)

if __name__ == '__main__':
    test_script = '''
            AddressingTestBlock:
                [[ 
                    $=TestValue
                    $_TestValue
                ]]

                .mx 0x00
                lda #$`TestValue
                sta $_TestValue
                jmp $_TestValue
                ora #$.TestValue
                and $^TestValue
                jmp $=(TestValue % 4)


        '''

    compiled_blocks = process_msfpatch_block({'body':test_script}, None, None)
    for b in compiled_blocks:
        b.pretty_print()
        b.resolve_expressions({'TestValue':0x7e1234})
        b.pretty_print()
