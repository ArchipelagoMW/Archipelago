import argparse
import re
import os
from datetime import datetime
from io import BytesIO
import time
import random
import hashlib

from . import ff4bin
from . import consts
from .bytes_patch import BytesPatch

from . import compile_cache
from . import compile_event
from . import compile_consts
from . import compile_text
from . import compile_trigger
from . import compile_postprocess
from . import compile_ai_script
from . import compile_placement
from . import compile_map
from . import compile_npc
from . import compile_event_call
from . import compile_shop
from . import compile_patch
from . import compile_myselfpatch
from . import compile_actor
from . import compile_drop_table
from . import compile_formation
from . import compile_monster
from . import compile_spell_set
from . import compile_gfx

block_processors = {
    'consts' : compile_consts.process_consts_block,
    'event' : compile_event.process_event_block,
    'text' : compile_text.process_text_block,
    'trigger' : compile_trigger.process_trigger_block,
    'ai_script' : compile_ai_script.process_ai_script_block,
    'placement' : compile_placement.process_placement_block,
    'map' : compile_map.process_map_block,
    'mapgrid' : compile_map.process_mapgrid_block,
    'npc' : compile_npc.process_npc_block,
    'eventcall' : compile_event_call.process_eventcall_block,
    'shop' : compile_shop.process_shop_block,
    'actor' : compile_actor.process_actor_block,
    'droptable' : compile_drop_table.process_droptable_block,
    'formation' : compile_formation.process_formation_block,
    'monster' : compile_monster.process_monster_block,
    'spellset' : compile_spell_set.process_spellset_block,

    'patch' : compile_patch.process_patch_block,
    'msfpatch' : compile_myselfpatch.process_msfpatch_block,
    'chr' : compile_gfx.process_chr_block,
    'pal' : compile_gfx.process_pal_block,
}

class CompileError(Exception):
    pass

class MetricsContext:
    def __init__(self, metrics, name):
        self._metrics = metrics
        self._name = name

    def __enter__(self):
        self._metrics.start(self._name)

    def __exit__(self, type, value, traceback):
        self._metrics.end(self._name)

class Metrics:
    def __init__(self):
        self._start_times = {}
        self._totals = {}

    def start(self, name):
        self._start_times[name] = time.process_time()
        self._last_name = name

    def end(self, name=None):
        if name is None:
            name = self._last_name

        if name in self._start_times:
            total = time.process_time() - self._start_times[name]
            del self._start_times[name]
            self._totals.setdefault(name, 0)
            self._totals[name] += total

        self._last_name = None

    def measure(self, name):
        return MetricsContext(self, name)

    def __repr__(self):
        max_name_length = max([len(n) for n in self._totals])
        fmt = '{:%d} : {}' % max_name_length
        key_order = sorted(self._totals.keys(), key=lambda k: self._totals[k], reverse=True)
        lines = [fmt.format(name, self._totals[name]) for name in key_order]
        return '\n'.join(lines)

class CompileOptions:
    def __init__(self):
        self.build_cache_path = None
        self.clean_cache = False
        self.force_recompile = False
        self.shuffle_msfpatches = False
        self.random_seed = None

class CompileEnvironment:
    def __init__(self, rom, options):
        self.rom = rom
        self.options = options
        self.postprocess = compile_postprocess.Postprocessor()
        self.cache = None
        self.reports = {}

        self.rnd = random.Random()
        if options.random_seed is not None:
            if type(options.random_seed) is str:
                numeric_seed = int(hashlib.sha1(options.random_seed.encode('utf-8')).hexdigest(), 16)
            else:
                numeric_seed = options.random_seed            
            self.rnd.seed(numeric_seed)

class CompileReport:
    def __init__(self):
        self.metrics = None
        self.symbol_table = None

CODE_TOKENS = ['/*', '*/', '//', '{', '}', '(', ')']
WHITESPACE = ['\n', '\r', '\t', ' ']
WHITESPACE_REGEX = re.compile(r'^\s+')

def _tokenize_code_line(line):
    line = line.replace('\r', '')
    tokens = re.split(r'(\s+|/\*|//|\*/|\{|\}|\(|\))', line)
    return filter(lambda x: x != '', tokens)

'''
Main interface function for running the F4C compiler.
@param input_rom: Either a stream of the input ROM file, or a path to it
@param output_rom: Either a stream to write the output ROM data to, or an output file path
@param options: Compile options struct
@param scripts: Any number of paths to f4c/f4t script files and/or raw F4C/F4T data.
'''
def compile(input_rom, output_rom, *scripts, options=CompileOptions()):
    metrics = Metrics()
    metrics.start('total')

    with metrics.measure('load rom'):
        rom = ff4bin.Rom(input_rom)

    with metrics.measure('load scripts'):
        code_token_sets = []
        text_lines = []
        bytes_patches = []
        for script in scripts:
            autodetect_format = True
            is_text_file = False
            in_multiline_comment = False
            code_tokens = None

            if isinstance(script, BytesPatch):
                bytes_patches.append(script)
                continue

            if '\n' not in script and os.path.isfile(script):        
                extension = os.path.splitext(script)[1].lower()
                if extension == '.f4c':
                    autodetect_format = False
                elif extension == '.f4t':
                    autodetect_format = False
                    is_text_file = True

                close_lines = True
                lines = open(script, 'r')
            else:
                close_lines = False
                lines = script.splitlines(True)

            for line in lines:
                if autodetect_format and not line.strip():
                    autodetect_format = False
                    if line.strip().startswith('---'):
                        is_text_file = True

                if is_text_file:
                    line = re.sub(r'[\n\r]+$', '', line)
                    text_lines.append(line)
                else:
                    if code_tokens is None:
                        code_tokens = []
                        code_token_sets.append(code_tokens)

                    with metrics.measure('tokenize line'):
                        tokens = _tokenize_code_line(line)

                    for token in tokens:
                        if in_multiline_comment:
                            if token == '*/':
                                in_multiline_comment = False
                        elif token == '/*':
                            in_multiline_comment = True
                        elif token == '//':
                            break
                        else:
                            code_tokens.append(token)

            if close_lines:
                lines.close()

    # read code blocks
    with metrics.measure('read code blocks'):
        blocks = []
        for code_tokens in code_token_sets:
            def pop_whitespace():
                while code_tokens and code_tokens[0][0] in WHITESPACE:
                    code_tokens.pop(0)

            current_block = None
            pop_whitespace()

            while code_tokens:
                block_type = code_tokens.pop(0)
                if not re.search(r'^[A-Za-z_][A-Za-z_0-9]*$', block_type):
                    raise CompileError("Expected block type identifier, got '{}' (context: {})".format(block_type, ''.join(code_tokens[:10])))

                current_block = {'type' : block_type, 'parameters' : '', 'body' : ''}
                blocks.append(current_block)

                pop_whitespace()
                if code_tokens[0] == '(':
                    code_tokens.pop(0)

                    param_tokens = []
                    if not code_tokens:
                        raise CompileError("Unexpected EOF while parsing parameters for '{}' block".format(current_block['type']))

                    pop_whitespace()
                    while code_tokens[0] != ')':
                        param_tokens.append(code_tokens.pop(0))
                        pop_whitespace()
                        if not code_tokens:
                            raise CompileError("Unexpected EOF while parsing parameters for '{}' block".format(current_block['type']))
                    code_tokens.pop(0)
                    pop_whitespace()
                    current_block['parameters'] = ' '.join(param_tokens)

                if not code_tokens or code_tokens[0] != '{':
                    raise CompileError("Expected {{ to begin body definition for '{}({})' block".format(current_block['type'], current_block['parameters']))

                code_tokens.pop(0)
                if not code_tokens:
                    raise CompileError("Unexpected EOF while parsing body for '{}({})' block".format(current_block['type'], current_block['parameters']))
                body_tokens = []
                brace_level = 0
                while brace_level > 0 or code_tokens[0] != '}':
                    tk = code_tokens.pop(0)
                    body_tokens.append(tk)

                    if tk == '}':
                        brace_level -= 1
                    elif tk == '{':
                        brace_level += 1

                    if not code_tokens:
                        raise CompileError("Unexpected EOF while parsing body for '{}({})' block".format(current_block['type'], current_block['parameters']))

                code_tokens.pop(0)
                current_block['body'] = ''.join(body_tokens)

                # remove starting/ending brace lines for text blocks, if applicable
                if current_block['type'] == 'text':
                    current_block['body'] = re.sub(r'^[ \t\f\v]*\n\r?', '', current_block['body'])
                    current_block['body'] = re.sub(r'\n\r?[ \t\f\v]*$', '', current_block['body'])

                pop_whitespace()

    # read text blocks
    with metrics.measure('read text blocks'):
        current_text_block = None
        for line in text_lines:
            m = re.search(r'^\s*---\s*(?P<header>.*[^\s])\s*---\s*$', line)
            if m:
                current_text_block = {'type' : 'text', 'parameters' : m.group('header'), 'body' : '', 'lines' : []}
                blocks.append(current_text_block)
            elif current_text_block is not None:
                current_text_block['lines'].append(line)

        for block in blocks:
            if block['type'] == 'text' and 'lines' in block:
                lines = block['lines']
                while not lines[-1].strip():
                    lines = lines[:-1]
                block['body'] = '\n'.join(lines)

    # process blocks
    env = CompileEnvironment(rom, options)
    if options.build_cache_path:
        env.cache = compile_cache.CompileCache(options.build_cache_path)

    blocks.sort(key = lambda b : (0 if b['type'] == 'consts' else 1))

    for block in blocks:
        if block['type'] not in block_processors:
            print('No compiler found for block type "{}"'.format(block['type']))
            continue

        with metrics.measure('process {} block'.format(block['type'])):
            process_func = block_processors[block['type']]
            process_func(block, rom, env)

    # apply bytes patches
    with metrics.measure('bytes patches'):
        for bp in bytes_patches:
            rom.add_patch(bp.get_unheadered_address(), bp.data)

    with metrics.measure('postprocess'):
        env.postprocess.apply_registered_processes(env)
        compile_postprocess.apply_cleanup_processes(env)

    if env.cache and options.clean_cache:
        env.cache.cleanup()

    with metrics.measure('output'):
        rom.save_rom(output_rom)

    metrics.end('total')

    report = CompileReport()
    report.metrics = metrics
    report.symbols = env.reports.get('symbols', {})
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('rom')
    parser.add_argument('code_files', nargs='*')
    parser.add_argument('--no-default-consts', action='store_true')
    parser.add_argument('-o', '--output')
    parser.add_argument('-t', '--test', action="store_true")
    parser.add_argument('-m', '--metrics', action="store_true")
    parser.add_argument('-l', '--list', action='append')
    args = parser.parse_args()

    scripts = []
    if not args.no_default_consts:
        scripts.append(os.path.join(os.path.dirname(__file__), 'default.consts'))

    if args.list:
        for list_file in args.list:
            with open(list_file) as infile:
                for line in infile:
                    if line.strip() and not line.strip().startswith('#'):
                        scripts.append(line.strip())

    scripts.extend(args.code_files)

    output_buffer = BytesIO()

    metrics = compile(args.rom, output_buffer, *scripts)

    # apply output
    if not args.test:
        output_filename = args.output
        if output_filename is None:
            parts = os.path.splitext(args.rom)
            output_filename = parts[0] + '.f4c-' + datetime.now().strftime('%Y%m%d%H%M%S') + parts[1]
        with open(output_filename, 'wb') as outfile:
            output_buffer.seek(0)
            outfile.write(output_buffer.read())

    if args.metrics:
        print(metrics)
