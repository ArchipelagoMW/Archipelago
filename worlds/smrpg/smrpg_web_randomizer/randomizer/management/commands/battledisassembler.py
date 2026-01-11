from django.core.management.base import BaseCommand

from ...randomizer.data.battletables import Targets, targeting_table, Monsters, monsters_table
from ...randomizer.data.attacks import get_default_enemy_attacks
from ...randomizer.data.items import get_default_items
from ...randomizer.data.spells import ChestScrow, ChestFear, ChestMute, ChestPoison, Nothing, get_default_spells

battle_lengths = [
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
    4,0,2,2,0,2,3,4,2,0,4,3,1,2,0,2,
    4,2,3,3,4,0,0,0,0,0,0,1,4,1,1,1,
]


def byte(offset=0, prefix='', table=None):
    def inner_byte(args):
        if table and args[0] in table:
            return '%s%s'%(prefix and (prefix + '.'), table[args[0]]), args[1:]
        return '0x%02x'%(args[0] + offset), args[1:]
    return inner_byte

def short(offset=0):
    def inner_short(args):
        return '0x%04x'%(args[0] + (args[1] << 8) + offset), args[2:]
    return inner_short

def con(constant):
    def inner_con(args):
        return '0x%02x'%(constant), args
    return inner_con

def named(name, *arg_parsers):
    def inner_named(args):
        acc = []
        for parse in arg_parsers:
            parsed_arg, args = parse(args)
            acc.append(parsed_arg)
        return name, acc
    return inner_named

def d_name(name_0, name_1, *parsers):
    n = named('', *parsers)
    def inner_d_name(args):
        (_, parsed) = n(args[1:])
        return ([name_0, name_1][args[0]], parsed)
    return inner_d_name

def build_table(list):
    return {i.index: i.name for i in list}

attacks_table = build_table(get_default_enemy_attacks(None))
items_table = build_table(get_default_items(None))
spells_table = build_table(get_default_spells(None) + [ChestScrow(None), ChestFear(None), ChestMute(None), ChestPoison(None), Nothing(None)])

attack_parse = byte(prefix='attacks', table=attacks_table)
item_parse = byte(prefix='items', table=items_table)
spell_parse = byte(prefix='spells', table=spells_table)
target_parse = byte(prefix='Targets', table=targeting_table)
monster_target_parse = byte(prefix='Monsters', table=monsters_table)

base = 0x7EE000
def tokenize(rom, start):
    dex = start
    ff_seen = False
    acc = []
    while True:
        cmd = rom[dex]
        if cmd == 0xFF:
            if ff_seen:
                break
            ff_seen = True
        l = battle_lengths[cmd]
        acc.append((rom[dex:dex+l], dex))
        dex += l
    return acc

def attack(num):
    def inner_attack(args):
        attack = '0x%02x'%(num)
        if num in attacks_table:
            attack = 'attacks.%s'%(attacks_table[num])
        return 'attack', [attack]
    return inner_attack

_if_name_table = [
    ('ERROR', []), 
    ('if_command', [byte(), byte()]),
    ('if_spell', [spell_parse, spell_parse]),
    ('if_item', [item_parse, item_parse]),
    ('if_element', [byte()]), 
    ('if_attacked', []),
    ('if_target_hp', [target_parse, byte()]),
    ('if_hp', [short()]),
    ('if_target_status', [target_parse, byte()]),
    ('if_not_target_status', [target_parse, byte()]),
    ('if_phase', [byte()]),
    ('ERROR', []), 
    ('if_less_than', [byte(base), byte()]),
    ('if_greater_or_equal', [byte(base), byte()]),
    ('ERROR', []), 
    ('ERROR', []), 
    ('if_target_alive',[byte(), target_parse]),
    ('if_bits_set', [byte(base), byte()]),
    ('if_bits_clear', [byte(base), byte()]),
    ('if_monster_in_formation', [short()]),
    ('if_solo', []),
]

def _if(args):
    name, parsers = _if_name_table[args[0]]
    rest = args[1:]
    acc = []
    for parser in parsers:
        parsed_arg, rest = parser(rest)
        acc.append(parsed_arg)
    if name == 'if_target_alive':
        acc = acc[1:]
        if args[1] == 0x1:
            name = 'if_target_dead'

    return name, acc



cmd_table = [None]*256
for i in range(0xE0):
    cmd_table[i] = attack(i)

cmd_table[0xE0] = named('attack', attack_parse, attack_parse, attack_parse)
cmd_table[0xE2] = named('set_target', target_parse)
cmd_table[0xE3] = named('battle_dialog', byte())
cmd_table[0xE5] = named('battle_event', byte())
cmd_table[0xE6] = d_name('inc', 'dec', byte(base))
cmd_table[0xE7] = d_name('set', 'clear', byte(base), byte())
cmd_table[0xE8] = named('zero', byte(base))
cmd_table[0xEA] = lambda args: (['remove', 'call'][args[0]], ['0x%02x'%(args[2])])
cmd_table[0xEB] = d_name('invuln', 'uninvuln', target_parse)
cmd_table[0xEC] = named('exit_battle')
cmd_table[0xED] = named('rand', byte())
cmd_table[0xEF] = named('cast_spell', spell_parse)
cmd_table[0xF0] = named('cast_spell', spell_parse, spell_parse, spell_parse)
cmd_table[0xF1] = named('animate', byte())
cmd_table[0xF2] = d_name('set_untargetable', 'set_targetable', monster_target_parse)
cmd_table[0xF3] = d_name('enable_command', 'disable_command', byte())
cmd_table[0xF4] = lambda args: (['remove_items', 'return_items'][args[1]], []) #WTF?
cmd_table[0xFB] = named('do_nothing')
cmd_table[0xFC] = _if
cmd_table[0xFD] = named('wait')
cmd_table[0xFE] = named('wait_return')
cmd_table[0xFF] = named('start_counter')


def parse_script(rom, dex):
    bank = 0x390000
    offset = bank+0x30AA+(dex*2)

    hi = rom[offset+1]
    lo = rom[offset]
    start = (hi << 8) + lo + bank

    acc = []
    cmds = tokenize(rom, start)
    for l,offset in cmds:
        cmd = l[0]
        if cmd_table[cmd]:
            name, args = cmd_table[cmd](l[1:])
        else:
            name, args = 'db', ['0x%02x'%(i) for i in l]
        acc.append((name, args))
  
    return acc

def print_list(script, dex):
    args = ', '.join(['(\'%s\', [%s])'%(n, ', '.join(args)) for n,args in script])
    print ('scripts[0x%x] = [%s]'%(dex, args))

def print_script(script, dex):
    print('        script = BattleScript()')
    for n,a in script:
        print('        script.%s(%s)'%(n, ', '.join(a)))
        if n == 'wait_return' or n == 'start_counter':
            print()
    print('        self.script = script.fin()')

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-r', '--rom', dest='rom',
            help='Path to a Mario RPG rom')

        parser.add_argument('-m', '--mode', dest='mode', choices=['parse', 'dump'],
            help='Either parse a single script to Python code or dump all of them in intermediate form')

        parser.add_argument('-i', '--index', dest='dex', type=int,
            help='Monster number to disassemble. Used with --mode parse.')


    def handle(self, *args, **options):
        mode = options['mode']
        rom = bytearray(open(options['rom'], 'rb').read())
        if mode == 'parse':
            dex = int(options['dex'])
            script = parse_script(rom, dex)
            print_script(script, dex)
        elif mode == 'dump':
            print('# AUTOGENERATED DO NOT EDIT!!')
            print('# Run the following command if you need to reassemble the table')
            print('# python manage.py battledisassembler --mode dump --rom ROM > randomizer/data/battlescripts.py')
            print('from .battletables import Targets, Monsters')
            print('from . import attacks, items, spells')
            print('scripts = [None]*256')
            for dex in range(256):
                script = parse_script(rom, dex)
                print_list(script, dex)
