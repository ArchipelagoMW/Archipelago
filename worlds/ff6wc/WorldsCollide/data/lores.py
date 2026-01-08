from ..data.lore import Lore
from ..data.ability_data import AbilityData
from ..data.structures import DataBits, DataArray, DataList

from ..memory.space import Bank, Reserve, Allocate, Write, Space
from ..instruction import asm as asm

class Lores:
    LORE_COUNT = 24
    CONDEMNED, ROULETTE, CLEAN_SWEEP, AQUA_RAKE, AERO, BLOW_FISH, BIG_GUARD, REVENGE, PEARL_WIND, L_5_DOOM, L_4_FLARE, L_3_MUDDLE, REFLECT, L_PEARL, STEP_MINE, FORCE_FIELD, DISCHORD, SOUR_MOUTH, PEP_UP, RIPPLER, STONE, QUASAR, GRAND_TRAIN, EXPLODER = range(LORE_COUNT)

    DIALOG_OFFSET = 139 # starting offset for battle dialog

    INITIAL_LORES_START = 0x26f564
    INITIAL_LORES_END = 0x26f566

    NAMES_START = 0x26f9fd
    NAMES_END = 0x26faec # https://discord.com/channels/666661907628949504/931737764205047858/1069100781216739328
    NAME_SIZE = 10

    DESC_PTRS_START = 0x2d7a70
    DESC_PTRS_END = 0x2d7a9f

    DESC_START = 0x2d77a0
    DESC_END = 0x2d7a6f

    ABILITY_DATA_START = 0x04725a
    ABILITY_DATA_END = 0x0473a9

    def __init__(self, rom, args, characters):
        self.rom = rom
        self.args = args
        self.characters = characters

        self.init_data = DataBits(self.rom, self.INITIAL_LORES_START, self.INITIAL_LORES_END)
        self.name_data = DataArray(self.rom, self.NAMES_START, self.NAMES_END, self.NAME_SIZE)
        self.ability_data = DataArray(self.rom, self.ABILITY_DATA_START, self.ABILITY_DATA_END, AbilityData.DATA_SIZE)

        self.desc_data = DataList(Space.rom, self.DESC_PTRS_START, self.DESC_PTRS_END,
                                    Space.rom.SHORT_PTR_SIZE, self.DESC_START,
                                    self.DESC_START, self.DESC_END)

        self.lores = []
        for lore_index in range(len(self.ability_data)):
            lore = Lore(lore_index, self.name_data[lore_index], self.ability_data[lore_index], self.desc_data[lore_index])
            self.lores.append(lore)

    def write_learners_table(self):
        self.learners = self.characters.get_characters_with_command("Lore")

        space = Allocate(Bank.CF, self.characters.CHARACTER_COUNT, "lore learners")
        space.write(self.learners)

        self.learners_table = space.start_address
        self.learners_table_end = self.learners_table + len(self.learners)

    def write_is_learner(self):
        from ..instruction import c0 as c0

        src = [
            asm.PHP(),
            asm.XY16(),
            asm.PHX(),
            asm.PHY(),
            asm.LDX(self.learners_table_end, asm.IMM16),    # offset in bank to last learner in table + 1
            asm.LDY(len(self.learners), asm.IMM16),         # learners table size
            asm.JSR(c0.is_skill_learner, asm.ABS),
            asm.PLY(),
            asm.PLX(),
            asm.PLP(),
            asm.RTL(),
        ]
        space = Write(Bank.C0, src, "lore is learner")
        self.is_learner_function = space.start_address_snes

    def after_battle_check_mod(self):
        from ..memory.space import START_ADDRESS_SNES
        from ..instruction import c0 as c0

        character_available = START_ADDRESS_SNES + c0.character_available

        # NOTE: lores are learned by being in the party
        #       on the veldt, the character to possibly appear is added to the party and hidden
        #       this means the invisible character who may or may not show up after battle can still learn abilities
        #       to fix this, CHARACTER_AVAILABLE is called to filter out leapt or not yet recruited characters
        space = Allocate(Bank.C2, 54, "lore check after battle", asm.NOP())
        space.write(
            asm.LDX(0x00, asm.IMM8),            # x = party slot 0
            "LEARNER_CHECK_LOOP",
            asm.TDC(),
            asm.LDA(0x3ed9, asm.ABS_X),         # a = character id
            asm.CMP(0xff, asm.IMM8),            # no character in this slot?
            asm.BEQ("LOOP_INCREMENT"),          # branch to next slot if no character in this slot
            asm.JSL(character_available),
            asm.CMP(0x00, asm.IMM8),            # compare result with 0
            asm.BEQ("LOOP_INCREMENT"),          # branch if character not available
            asm.TXY(),                          # transfer character index to y
            asm.PEA(0xb0c3),                    # dark/zombie/petrify/death/berserk/muddle/sleep
            asm.PEA(0x2310),                    # stop/rage/frozen/hide
            asm.JSR(0x5864, asm.ABS),           # clear carry if any of above status effects set
        )
        if self.args.lores_everyone_learns:
            space.write(
                asm.BCS("RETURN_TRUE"),         # branch if character does not have any of above status effects
            )
        else:
            space.write(
                asm.BCC("LOOP_INCREMENT"),      # branch if character has any of above status effects
                asm.LDA(0x3ed9, asm.ABS_X),     # a = character id
                asm.JSL(self.is_learner_function),
                asm.CMP(0x00, asm.IMM8),        # compare result with 0
                asm.BNE("RETURN_TRUE"),         # branch if character can learn
            )

        space.write(
            "LOOP_INCREMENT",
            asm.INX(),
            asm.INX(),
            asm.CPX(0x08, asm.IMM8),
            asm.BNE("LEARNER_CHECK_LOOP"),      # branch if haven't checked all 4 party members

            asm.LDA(0x00, asm.IMM8),            # return 0 in a register
            asm.BRA("RETURN"),

            "RETURN_TRUE",
            asm.LDA(0x01, asm.IMM8),            # return 1 in a register

            "RETURN",
            asm.RTS(),
        )
        learn_lore = space.start_address

        space = Reserve(0x236e1, 0x236f0, "lore check strago in party and status", asm.NOP())
        space.add_label("RETURN", 0x23708)
        space.write(
            asm.JSR(learn_lore, asm.ABS),
            asm.CMP(0x00, asm.IMM8),            # compare result with 0
            asm.BEQ("RETURN"),                  # branch if learn lore returned false
            asm.SEC(),
        )

    def start_random_lores(self):
        import random

        self.init_data.clear_all()

        number_initial_lores = random.randint(self.args.start_lores_random_min, self.args.start_lores_random_max)
        initial_lores = random.sample(range(self.LORE_COUNT), number_initial_lores)
        for lore_id in initial_lores:
            self.init_data[lore_id] = 1

    def shuffle_mp(self):
        mp = []
        for lore in self.lores:
            mp.append(lore.mp)

        import random
        random.shuffle(mp)
        for lore in self.lores:
            lore.mp = mp.pop()

    def random_mp_value(self):
        import random
        for lore in self.lores:
            lore.mp = random.randint(self.args.lores_mp_random_value_min, self.args.lores_mp_random_value_max)

    def random_mp_percent(self):
        import random
        for lore in self.lores:
            mp_percent = random.randint(self.args.lores_mp_random_percent_min,
                                        self.args.lores_mp_random_percent_max) / 100.0
            value = int(lore.mp * mp_percent)
            lore.mp = max(min(value, 254), 0)

    def _get_new_level_desc(lore_index, level_divisor):
        level_string = f'LV{level_divisor}' # keeping it simple to not use extra space
        new_desc = ''
        if(lore_index == Lores.L_5_DOOM):
            new_desc = f'Casts <dotted line>Doom" on {level_string} enemy<end>'
        elif(lore_index == Lores.L_4_FLARE):
            new_desc = f'Casts <dotted line>Flare" on {level_string} enemy<end>'
        elif(lore_index == Lores.L_3_MUDDLE):
            new_desc = f'Casts <dotted line>Muddle" on {level_string} enemy<end>'
        elif(lore_index == Lores.L_PEARL):
            new_desc = f'Pearl attack on {level_string} enemy<end>'
        else:
            raise ValueError(f'Unexpected lore index: {lore_index}')
        return new_desc

    def random_lx_levels(self, dialogs):
        import random, re
        LX_LORE_IDX = [Lores.L_5_DOOM, Lores.L_4_FLARE, Lores.L_3_MUDDLE, Lores.L_PEARL]
        LQ_EFFECT = 29 # the AbilityData.effect setting for L?
        NO_EFFECT = 255 # The AbilityData.effect setting for no effect
        MAX_DIVISOR = 5

        for lore_index in LX_LORE_IDX:
            lore = self.lores[lore_index]

            level_divisor = random.randint(0, MAX_DIVISOR)
            if lore_index == Lores.L_5_DOOM:
                # prevent soft-locks with bosses by removing unmissable doom
                level_divisor = random.randint(2, MAX_DIVISOR) 

            lore.accuracy = level_divisor
            if level_divisor: # non-zero
                lore.effect = NO_EFFECT
            else: # zero - use for L?
                level_divisor = '?'
                lore.effect = LQ_EFFECT
            lore.name = re.sub('L.*[?1-9]', f'L.{level_divisor}', lore.name)
            lore.desc = Lores._get_new_level_desc(lore_index, level_divisor)
            battle_message = re.sub('<dotted line>', '“', lore.desc)
            dialogs.set_battle_message_text(self.DIALOG_OFFSET + lore_index, battle_message)

    def show_mp_mod(self):
        # Show Party member MP in menus if they have Lore, even if they don't know any Magic
        # Thanks to Lenophis for most of this work: https://discord.com/channels/666661907628949504/931737764205047858/1054557544942673940
        src = [
            asm.JSR(0x30d2b, asm.ABS), # check to see if this character knows magic; this is displaced code
            asm.BCS("magic_exit"),
            # if we are at this point, we have a magic command but no magic.
            # so now we are going to do a back-up check and see if a secondary command is present so MP can be shown
            # if not, it will be grayed out as normal
            asm.LDY(0x67, asm.DIR), # this gets set earlier in our route. Let's pull this character's index again for our back-up check
            asm.LDX(0x0000, asm.IMM16),
            "command_loop",
            asm.LDA(0x0016, asm.ABS_Y),
            asm.CMP(0x0C, asm.IMM8), # Lore
            asm.BEQ("command_ok"),
            asm.INY(),
            asm.INX(),
            asm.CPX(0x0004, asm.IMM16), # have we done 4 commands yet?
            asm.BNE("command_loop"), # branch if not
            # if we have exited the loop with no match, we need to flag MP to not show up
            asm.CLC(),
            asm.RTS(),
            "command_ok",
            # at this point, we have matched supplemental command, so let's flag MP as ok to show up
            asm.SEC(),
            "magic_exit",
            asm.RTS(),
        ]
        space = Write(Bank.C3, src, "check for Lore")
        mp_hook = space.start_address
        space = Reserve(0x30cb7, 0x30cb9, "check for magic command")
        space.write(
            asm.JSR(mp_hook, asm.ABS),
        )
        space = Reserve(0x36134, 0x36136, "check for magic command 2")
        space.write(
            asm.JSR(mp_hook, asm.ABS),
        )

    def mod(self, dialogs):
        self.write_learners_table()
        self.write_is_learner()
        self.after_battle_check_mod()
        self.show_mp_mod()

        if self.args.start_lores_random:
            self.start_random_lores()

        if self.args.lores_mp_shuffle:
            self.shuffle_mp()
        elif self.args.lores_mp_random_value:
            self.random_mp_value()
        elif self.args.lores_mp_random_percent:
            self.random_mp_percent()

        if self.args.lores_level_randomize:
            self.random_lx_levels(dialogs)

    def write(self):
        if self.args.spoiler_log:
            self.log()

        for lore_index, lore in enumerate(self.lores):
            self.name_data[lore_index] = lore.name_data()
            self.ability_data[lore_index] = lore.ability_data()
            self.desc_data[lore_index] = lore.desc_data()

        self.init_data.write()
        self.name_data.write()
        self.ability_data.write()
        self.desc_data.write()

    def log(self):
        from ..log import section

        lcolumn = []
        for lore_index in range(self.LORE_COUNT):
            lore = self.lores[lore_index]
            lore_name = lore.get_name()

            start = "*" if self.init_data[lore_index] else " "
            lcolumn.append(f"{start}{lore_name:<{self.NAME_SIZE}} {lore.mp:>3} MP")

        lcolumn.append("")
        lcolumn.append("* = Starting Lore")

        section("Lores", lcolumn, [])

    def print(self):
        for lore in self.lores:
            lore.print()
