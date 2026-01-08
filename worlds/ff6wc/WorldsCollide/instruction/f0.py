from ..memory.space import START_ADDRESS_SNES, Bank, Reserve, Allocate, Write, Read
from ..instruction import asm as asm
from .. import args as args
import random

def _divide_mod():
    # 16 bit a = 16 bit a // 8 bit x
    # 8 bit x = 16 bit a % 8 bit x
    src = [
        Read(0x024792, 0x0247b5),   # copy c2 implementation
        asm.RTS(),
    ]
    space = Write(Bank.F0, src, "f0 divide a16 = a16 // x8, x8 = a16 % x8")
    return space.start_address
divide = _divide_mod()

def _set_bit_x_mod():
    # set bit #x in a
    src = [
        Read(0x021e57, 0x021e5c),   # copy c2 implementation
        asm.RTS(),
    ]
    space = Write(Bank.F0, src, "f0 set bit #x in a")
    return space.start_address
set_bit_x = _set_bit_x_mod()

def _set_user_text_color_mod():
    # user configuration text color
    src = [
        asm.LDA(0x20, asm.IMM8),
        asm.STA(0x29, asm.DIR),
        asm.RTS(),
    ]
    space = Write(Bank.F0, src, "f0 set user text color in menu")
    return space.start_address
set_user_text_color = _set_user_text_color_mod()

def _set_blue_text_color_mod():
    src = [
        asm.LDA(0x24, asm.IMM8),
        asm.STA(0x29, asm.DIR),
        asm.RTS(),
    ]
    space = Write(Bank.F0, src, "f0 set blue text color in menu")
    return space.start_address
set_blue_text_color = _set_blue_text_color_mod()

def _set_gray_text_color_mod():
    src = [
        asm.LDA(0x28, asm.IMM8),
        asm.STA(0x29, asm.DIR),
        asm.RTS(),
    ]
    space = Write(Bank.F0, src, "f0 set gray text color in menu")
    return space.start_address
set_gray_text_color = _set_gray_text_color_mod()

def _boss_formations_mod():
    from ..data.bosses import normal_formation_name

    bosses_table = []
    for formation in normal_formation_name:
        bosses_table.append(
            formation.to_bytes(2, "little"),
        )
    space = Write(Bank.F0, bosses_table, "f0 boss formations table")

    boss_formations = space.start_address + START_ADDRESS_SNES
    boss_formations_size = len(space)
    return (boss_formations, boss_formations_size)
boss_formations, boss_formations_size = _boss_formations_mod()

def _dragon_formations_mod():
    from ..data.bosses import dragon_formation_name

    dragons_table = []
    for formation in dragon_formation_name:
        dragons_table.append(
            formation.to_bytes(2, "little"),
        )
    space = Write(Bank.F0, dragons_table, "f0 dragon formations table")

    dragon_formations = space.start_address + START_ADDRESS_SNES
    dragon_formations_size = len(space)
    return (dragon_formations, dragon_formations_size)
dragon_formations, dragon_formations_size = _dragon_formations_mod()

def _final_battle_formations_mod():
    from ..data.bosses import final_battle_formation_name

    final_battles_table = []
    for formation in final_battle_formation_name:
        final_battles_table.append(
            formation.to_bytes(2, "little"),
        )
    space = Write(Bank.F0, final_battles_table, "f0 final battle formations table")

    final_battle_formations = space.start_address + START_ADDRESS_SNES
    final_battle_formations_size = len(space)
    return (final_battle_formations, final_battle_formations_size)
final_battle_formations, final_battle_formations_size = _final_battle_formations_mod()

def _color_absolute_addition_mod():
    # move to f0 to make room in c1 bank
    src = [
        Read(0x1fd00, 0x1fd65),
        asm.RTL(),
    ]
    space = Write(Bank.F0, src, "f0 color absolute addition")
    return space.start_address
color_absolute_addition = _color_absolute_addition_mod()

def _color_absolute_subtraction_mod():
    # move to f0 to make room in c1 bank
    src = [
        Read(0x1fc99, 0x1fcfe),
        asm.RTL(),
    ]
    space = Write(Bank.F0, src, "f0 color absolute subtraction")
    return space.start_address
color_absolute_subtraction = _color_absolute_subtraction_mod()
