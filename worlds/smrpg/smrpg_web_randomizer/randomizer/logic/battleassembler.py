from . import utils
from .dialogs import allocate_string
from .patch import Patch
from ...randomizer.data import battlescripts
from ...randomizer.data.attacks import EnemyAttack
from ...randomizer.data.items import Item
from ...randomizer.data.spells import Spell, CharacterSpell, EnemySpell


mem_base = 0x7EE000

def lower(*args):
    return [getattr(arg, 'index', arg) for arg in args]

class BattleScriptAssember:
    def __init__(self):
        self.commands = []
        self.counter_called = False

    def append_byte(self, byte):
        assert 0 <= byte <= 0xFF
        self.commands.append(byte)
        return self

    def append_short(self, short):
        assert 0 <= short <= 0xFFFF
        self.commands.append(short & 0xFF)
        self.commands.append((short >> 8) & 0xFF)
        return self

    def append_address(self, address):
        assert mem_base <= address <= mem_base + 0xFF or 0 <= address <= 0xFF
        return self.append_byte(address - mem_base)

    def db(self, *args):
        for byte in args:
            self.append_byte(byte)
        return self

    def fin(self):
      assert self.counter_called
      self.commands.append(0xFF)
      return bytearray(self.commands)

    def assemble_from_tuples(tuples):
        assembler = BattleScriptAssember()
        for name, args in tuples:
            func = getattr(assembler, name, None)
            if not func:
                raise Exception('%s(%s) is an invalid instruction!'%(func, args))
            func(*args)
        return assembler.fin()

    # Commands
    def attack(self, arg_0, arg_1=None, arg_2=None):
        arg_0, arg_1, arg_2 = lower(arg_0, arg_1, arg_2)
        if arg_0 is not None and arg_1 is None and arg_2 is None:
            return self.db(arg_0)
        return self.db(0xE0, arg_0, arg_1, arg_2)

    def set_target(self, arg_0):
        return self.db(0xE2, arg_0)

    def battle_dialog(self, arg_0):
        return self.db(0xE3, arg_0)

    def battle_event(self, arg_0):
        return self.db(0xE5, arg_0)

    def inc(self, arg_0):
        return self.db(0xE6, 0x00).append_address(arg_0)

    def dec(self, arg_0):
        return self.db(0xE6, 0x01).append_address(arg_0)

    def set(self, arg_0, arg_1):
        return self.db(0xE7, 0x00).append_address(arg_0).append_byte(arg_1)

    def clear(self, arg_0, arg_1):
        return self.db(0xE7, 0x01).append_address(arg_0).append_byte(arg_1)

    def zero(self, arg_0):
        return self.append_byte(0xE8).append_address(arg_0)

    def remove(self, arg_0):
        return self.db(0xEA, 0x00, 0x00, arg_0)

    def call(self, arg_0):
        return self.db(0xEA, 0x01, 0x00, arg_0)

    def invuln(self, arg_0):
        return self.db(0xEB, 0x00, arg_0)

    def uninvuln(self, arg_0):
        return self.db(0xEB, 0x01, arg_0)

    def exit_battle(self):
        return self.db(0xEC)

    def rand(self, arg_0):
        return self.db(0xED, arg_0)

    def cast_spell(self, arg_0, arg_1=None, arg_2=None):
        arg_0, arg_1, arg_2 = lower(arg_0, arg_1, arg_2)
        if arg_0 is not None and arg_1 is None and arg_2 is None:
            return self.db(0xEF, arg_0)
        return self.db(0xF0, arg_0, arg_1, arg_2)

    def animate(self, arg_0):
        return self.db(0xF1, arg_0)

    def set_untargetable(self, arg_0):
        return self.db(0xF2, 0x00, arg_0)

    def set_targetable(self, arg_0):
        return self.db(0xF2, 0x01, arg_0)

    def enable_command(self, arg_0):
        return self.db(0xF3, 0x00, arg_0)

    def disable_command(self, arg_0):
        return self.db(0xF3, 0x01, arg_0)

    def remove_items(self):
        return self.db(0xF4, 0x00, 0x00, 0x00)

    def return_items(self):
        return self.db(0xF4, 0x00, 0x01, 0x00)

    # FB Do nothing
    def if_command(self, arg_0, arg_1=None):
        if arg_1 == None:
            arg_1 = arg_0
        return self.db(0xFC, 0x01, arg_0, arg_1)

    def if_spell(self, arg_0, arg_1=None):
        arg_0, arg_1 = lower(arg_0, arg_1)
        if arg_1 == None:
            arg_1 = arg_0
        return self.db(0xFC, 0x02, arg_0, arg_1)

    def if_item(self, arg_0, arg_1=None):
        arg_0, arg_1 = lower(arg_0, arg_1)
        if arg_1 == None:
            arg_1 = arg_0
        return self.db(0xFC, 0x03, arg_0, arg_1)

    def if_element(self, arg_0):
        return self.db(0xFC, 0x04, arg_0, 0x00)

    def if_attacked(self):
        return self.db(0xFC, 0x05, 0x00, 0x00)

    # FC 06 Target HP?
    def if_hp(self, arg_0):
        return self.db(0xFC, 0x07).append_short(arg_0)

    def if_target_status(self, arg_0, arg_1):
        return self.db(0xFC, 0x08, arg_0, arg_1)

    def if_not_target_status(self, arg_0, arg_1):
        return self.db(0xFC, 0x09, arg_0, arg_1)

    def if_phase(self, arg_0):
        return self.db(0xFC, 0x0A, arg_0, 0x00)

    def if_less_than(self, arg_0, arg_1):
        return self.db(0xFC, 0x0C).append_address(arg_0).append_byte(arg_1)

    def if_greater_or_equal(self, arg_0, arg_1):
        return self.db(0xFC, 0x0D).append_address(arg_0).append_byte(arg_1)

    def if_target_alive(self, arg_0):
        return self.db(0xFC, 0x10, 0x00, arg_0)

    def if_target_dead(self, arg_0):
        return self.db(0xFC, 0x10, 0x01, arg_0)

    def if_bits_set(self, arg_0, arg_1):
        return self.db(0xFC, 0x11).append_address(arg_0).append_byte(arg_1)

    def if_bits_clear(self, arg_0, arg_1):
        return self.db(0xFC, 0x12).append_address(arg_0).append_byte(arg_1)

    def if_monster_in_formation(self, arg_1):
        return self.db(0xFC, 0x13).append_short(arg_1)

    def if_solo(self):
        return self.db(0xFC, 0x14, 0x00, 0x00)

    def wait(self):
        return self.append_byte(0xFD)

    def wait_return(self):
        return self.append_byte(0xFE)

    def start_counter(self):
        assert not self.counter_called
        self.counter_called = True
        return self.commands.append(0xFF)

def type_assert(t, *args):
    for i, arg in enumerate(args):
        if isinstance(arg, int):
            if not (0 <= arg <= 0xFF):
                raise Exception('arg %d is out of range 0 <= %d <= 0xFF'%(i, arg))
        elif arg and not issubclass(arg, t):
            raise Exception('arg %s is not of type %s'%(arg, t))

class BattleScript:
    def __init__(self):
        self.counter_called = False
        self.script = []

    def append(self, name, *args):
        self.script.append((name, args))
        return self

    def fin(self):
        assert self.counter_called
        return self.script

    def attack(self, arg_0, arg_1=None, arg_2=None):
        type_assert(EnemyAttack, arg_0, arg_1, arg_2)
        return self.append('attack', arg_0, arg_1, arg_2)

    def set_target(self, arg_0):
        return self.append('set_target', arg_0)

    def battle_dialog(self, arg_0):
        return self.append('battle_dialog', arg_0)

    def battle_event(self, arg_0):
        return self.append('battle_event', arg_0)

    def inc(self, arg_0):
        return self.append('inc', arg_0)

    def dec(self, arg_0):
        return self.append('dec', arg_0)

    def set(self, arg_0, arg_1):
        return self.append('set', arg_0, arg_1)

    def clear(self, arg_0, arg_1):
        return self.append('clear', arg_0, arg_1)

    def zero(self, arg_0):
        return self.append('zero', arg_0)

    def remove(self, arg_0):
        return self.append('remove', arg_0)

    def call(self, arg_0):
        return self.append('call', arg_0)

    def invuln(self, arg_0):
        return self.append('invuln', arg_0)

    def uninvuln(self, arg_0):
        return self.append('uninvuln', arg_0)

    def exit_battle(self):
        return self.append('exit_battle')

    def rand(self, arg_0):
        return self.append('rand', arg_0)

    def cast_spell(self, arg_0, arg_1=None, arg_2=None):
        type_assert(EnemySpell, arg_0, arg_1, arg_2)
        return self.append('cast_spell', arg_0, arg_1, arg_2)

    def animate(self, arg_0):
        return self.append('animate', arg_0)

    def set_untargetable(self, arg_0):
        return self.append('set_untargetable', arg_0)

    def set_targetable(self, arg_0):
        return self.append('set_targetable', arg_0)

    def enable_command(self, arg_0):
        return self.append('enable_command', arg_0)

    def disable_command(self, arg_0):
        return self.append('disable_command', arg_0)

    def remove_items(self):
        return self.append('remove_items')

    def return_items(self):
        return self.append('return_items')

    def if_command(self, arg_0, arg_1=None):
        return self.append('if_command', arg_0, arg_1)

    def if_spell(self, arg_0, arg_1=None):
        type_assert(CharacterSpell, arg_0, arg_1)
        return self.append('if_spell', arg_0, arg_1)

    def if_item(self, arg_0, arg_1=None):
        type_assert(Item, arg_0, arg_1)
        return self.append('if_item', arg_0, arg_1)

    def if_element(self, arg_0):
        return self.append('if_element', arg_0)

    def if_attacked(self):
        return self.append('if_attacked')

    def if_hp(self, arg_0):
        return self.append('if_hp', arg_0)

    def if_target_status(self, arg_0, arg_1):
        return self.append('if_target_status', arg_0, arg_1)

    def if_not_target_status(self, arg_0, arg_1):
        return self.append('if_not_target_status', arg_0, arg_1)

    def if_phase(self, arg_0):
        return self.append('if_phase', arg_0)

    def if_less_than(self, arg_0, arg_1):
        return self.append('if_less_than', arg_0, arg_1)

    def if_greater_or_equal(self, arg_0, arg_1):
        return self.append('if_greater_or_equal', arg_0, arg_1)

    def if_target_alive(self, arg_0):
        return self.append('if_target_alive', arg_0)

    def if_target_dead(self, arg_0):
        return self.append('if_target_dead', arg_0)

    def if_bits_set(self, arg_0, arg_1):
        return self.append('if_bits_set', arg_0, arg_1)

    def if_bits_clear(self, arg_0, arg_1):
        return self.append('if_bits_clear', arg_0, arg_1)

    def if_monster_in_formation(self, arg_1):
        return self.append('if_monster_in_formation', arg_1)

    def if_solo(self):
        return self.append('if_solo')

    def wait(self):
        return self.append('wait')

    def wait_return(self):
        return self.append('wait_return')

    def start_counter(self):
        assert not self.counter_called
        self.counter_called = True
        return self.append('start_counter')


def assemble_battle_scripts(world):
    patch = Patch()

    if not world.open_mode:
        return patch

    free_list = {
        0x3932AA: 10058, # Original battle script location
        0x39F400: 3072,  # Lazy shell also saves scripts here
    }

    ptr_table_base = 0x3930AA
    for index in range(256):
        enemy = world.enemies_dict.get(index, None)
        if enemy:
            enemy.patch_script()
            script = enemy.script
        else:
            # This makes round tripping possible
            # Might be worth it to remove them and save on space...
            script = battlescripts.scripts[index]
        script_bytes = BattleScriptAssember.assemble_from_tuples(script)
        script_base = allocate_string(len(script_bytes), free_list)
        offset = index * 2
        script_short = script_base & 0xFFFF

        patch.add_data(ptr_table_base + offset, utils.ByteField(script_short, num_bytes=2).as_bytes())
        patch.add_data(script_base, script_bytes)

    return patch
