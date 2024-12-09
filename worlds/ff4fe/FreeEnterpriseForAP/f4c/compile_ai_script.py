from . import compile_common
from . import lark
from . import consts
from . import ai_common

class AiScriptTransformer(lark.Transformer):
    def races(self, children):
        b = 0
        for n in children:
            b |= (1 << n)
        return b

    def elements(self, children):
        b = 0
        for n in children:
            b |= (1 << n)
        return b

    def speed_delta(self, n):
        sign,value = n
        if str(sign) == '-':
            return 0x80 | (value & 0x7F)
        else:
            return value & 0x7F

    def condition_increment(self, n):
        return 0x01

    def condition_set(self, n):
        v = n[0]
        return 0x80 | (v & 0x7F)

    def reaction_number(self, n):
        v = n[0]
        return 0x80 | (v & 0x7F)

    def target(self, children):
        if type(children[0]) is int:
            return children[0]

        slug = ''.join([str(x).lower() for x in children])
        if slug not in ai_common.TARGET_CODES_BY_SLUG:
            raise ValueError("Could not find code for target specification: {}".format(slug))

        return ai_common.TARGET_CODES_BY_SLUG[slug]


    def ai_command(self, children):
        slug = ''
        parameter = None
        for c in children:
            if type(c) is int:
                parameter = c
            else:
                slug += str(c).lower()

        if slug in ai_common.COMMAND_CODES_BY_SLUG:
            code = [ai_common.COMMAND_CODES_BY_SLUG[slug]]
            if parameter is not None:
                code.append(parameter)
            return code
        elif slug == 'use':
            return [parameter]
        elif slug == 'useongroup':
            return [parameter + 0x30]
        elif slug == 'usecommand':
            return [parameter + 0xC0]
        elif slug == 'wait':
            return [0xFE]
        elif slug == 'chaininto':
            return [0xFB]
        else:
            raise ValueError("Unrecognized AI script command: {}".format(slug))

    def chain_block(self, children):
        return [0xFD] + self.partition_commands(children, 0xFB) + [0xFC]

    def ai_script_block_body(self, children):
        return self.partition_commands(children, 0xFE) + [0xFF]

    def partition_commands(self, children, separator_byte=None):
        sections = [ [] ]

        for c in children:
            sections[-1].extend(c)
            if c[0] == 0xFE or c[0] == 0xFB and len(sections) > 1:
                sections[-2].extend(sections[-1])
                sections.pop()
            elif c[0] <= 0xE7 or c[0] == 0xFD:
                sections.append([])

        if len(sections) > 1:
            sections[-2].extend(sections[-1])
            sections.pop()

        result = []
        for i,section in enumerate(sections):
            if separator_byte is not None and i > 0:
                result.append(separator_byte)
            result.extend(section)

        return result

_ai_script_transformer = AiScriptTransformer()

def compile_ai_script(script_body):
    tree = compile_common.parse(script_body, 'ai', 'ai_script_block_body')
    return _ai_script_transformer.transform(tree)

def process_ai_script_block(block, rom, env):
    params_tree = compile_common.parse(block['parameters'], 'ai', 'ai_script_block_parameters')
    encoded_script = compile_ai_script(block['body'])

    if params_tree.data == 'normal_script':
        rom.monster_scripts[params_tree.children[0]] = encoded_script
    elif params_tree.data == 'moon_script':
        rom.moon_monster_scripts[params_tree.children[0]] = encoded_script
    else:
        raise ValueError("Don't know where to put script for ai_script({})".format(block['parameters']))



