from ...objectives.results._objective_result import *
from ... import args as args

def _random_spell_table():
    from ...constants.spells import spell_id

    spell_table = list(range(len(spell_id)))

    for a_spell_id in args.remove_learnable_spell_ids:
        spell_table.remove(a_spell_id)

    random.shuffle(spell_table)

    if len(spell_table) > 0:
        space = Write(Bank.F0, spell_table, "forget spells random spell table")
        return space.start_address, len(spell_table)
    else:
        return None, 0
random_forget_spell_table, random_forget_spell_table_size = _random_spell_table()

def _forget_random_spells():
    # input: 8 bit number of random spells to forget with each character
    # output: all characters forget next given number of spells in random_forget_spelL_table, skips spells not known

    from ...constants.spells import id_spell
    from ...constants.entities import id_character

    learned_start_address = 0x1a6e
    character_count = len(id_character) - 2     # characters except gogo/umaro
    spell_count = len(id_spell)

    learned_start = 0x30    # temporarily store learned_start_address in field/battle scratch ram
    spells_left = 0x32      # temporarily store number spells left to forget in field/battle scratch ram

    if random_forget_spell_table_size > 0:
        src = [
            asm.PHP(),
            asm.XY16(),
            asm.LDY(learned_start, asm.DIR),
            asm.PHY(),                              # store value at $learned_start to be restored before returning
            asm.LDA(spells_left, asm.DIR),
            asm.PHA(),                              # store value at $spells_left to be restored before returning

            asm.LDY(learned_start_address, asm.IMM16),
            asm.STY(learned_start, asm.DIR),        # $learned_start = start of character's learned spells
            asm.LDY(character_count, asm.IMM16),    # y = number of characters remaining

            "CHARACTER_LOOP_START",
            asm.PHY(),
            asm.TDC(),
            asm.LDA(field.LongCall.ARG_ADDRESS, asm.DIR),   # a = number of spells to forget
            asm.STA(spells_left, asm.DIR),          # $spells_left = number of spells left to forget
            asm.LDX(0x0000, asm.IMM16),             # x = spell table index

            "SPELL_LOOP_START",
            asm.LDA(START_ADDRESS_SNES + random_forget_spell_table, asm.LNG_X),
            asm.TAY(),                              # y = id of next spell in table
            asm.LDA(0xff, asm.IMM8),                # a = known spell value
            asm.CMP(learned_start, asm.DIR_16_Y),   # compare with value at learned start address for character + spell id
            asm.BNE("NEXT_SPELL"),                  # branch if character does not know this spell
            asm.LDA(0x00, asm.IMM8),
            asm.STA(learned_start, asm.DIR_16_Y),   # forget spell
            asm.DEC(spells_left, asm.DIR),          # decrement number of spells left to forget
            asm.BEQ("NEXT_CHARACTER"),              # next character if number of spells to forget is 0
            "NEXT_SPELL",
            asm.INX(),                              # next spell in spell table
            asm.CPX(random_forget_spell_table_size, asm.IMM16),
            asm.BLT("SPELL_LOOP_START"),            # branch if spell index < len(spell table)

            "NEXT_CHARACTER",
            asm.PLY(),                              # y = characters remaining
            asm.DEY(),
            asm.BEQ("RETURN"),                      # return if zero characters remaining

            asm.A16(),
            asm.LDA(learned_start, asm.DIR),        # a = start of learned spells for character
            asm.CLC(),
            asm.ADC(spell_count, asm.IMM16),        # add number of spells
            asm.STA(learned_start, asm.DIR),        # $learned_start = start of learned spells for next character
            asm.A8(),
            asm.BRA("CHARACTER_LOOP_START"),        # forget spells with next character

            "RETURN",
            asm.PLA(),
            asm.STA(spells_left, asm.DIR),          # restore original value at $spells_left
            asm.PLY(),
            asm.STY(learned_start, asm.DIR),        # restore original value at $learned_start
            asm.PLP(),
            asm.RTL(),
        ]
    else: # no spells to forget
        src = [
            asm.RTL()
        ]
    space = Write(Bank.F0, src, "forget spells forget random spells")
    return space.start_address
forget_random_spells = _forget_random_spells()

class Field(field_result.Result):
    def src(self, count):
        return [
            field.LongCall(START_ADDRESS_SNES + forget_random_spells, count),
        ]

class Battle(battle_result.Result):
    def src(self, count):
        return [
            asm.LDA(count, asm.IMM8),
            asm.STA(field.LongCall.ARG_ADDRESS, asm.DIR),
            asm.JSL(START_ADDRESS_SNES + forget_random_spells),
        ]

class Result(ObjectiveResult):
    NAME = "Forget Spells"
    def __init__(self, min_count, max_count):
        self.count = random.randint(min_count, max_count)
        super().__init__(Field, Battle, self.count)
