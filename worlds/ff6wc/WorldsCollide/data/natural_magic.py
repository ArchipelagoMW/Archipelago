from ..data.natural_spell import NaturalSpell
from ..data.structures import DataArray

from ..memory.space import Bank, Reserve, Allocate
from ..instruction import asm as asm

class NaturalMagic:
    TERRA_SPELL_DATA_START = 0x2ce3c0
    TERRA_SPELL_DATA_END = 0x2ce3df

    CELES_SPELL_DATA_START = 0x2ce3e0
    CELES_SPELL_DATA_END = 0x2ce3ff

    SPELL_DATA_SIZE = 2

    def __init__(self, rom, args, characters, spells):
        self.rom = rom
        self.args = args
        self.characters = characters
        self.spells = spells

        self.terra_spell_data = DataArray(self.rom, self.TERRA_SPELL_DATA_START, self.TERRA_SPELL_DATA_END, self.SPELL_DATA_SIZE)
        self.celes_spell_data = DataArray(self.rom, self.CELES_SPELL_DATA_START, self.CELES_SPELL_DATA_END, self.SPELL_DATA_SIZE)

        self.terra_spells = []
        for spell_index, spell_data in enumerate(self.terra_spell_data):
            spell = NaturalSpell(spell_index, spell_data)
            self.terra_spells.append(spell)

        self.celes_spells = []
        for spell_index, spell_data in enumerate(self.celes_spell_data):
            spell = NaturalSpell(spell_index, spell_data)
            self.celes_spells.append(spell)

        self.learner1 = 0
        self.learner1_name = "Terra"
        self.learner2 = 6
        self.learner2_name = "Celes"

    def event_check_mod(self):
        # modify event code to also check for swdtech/blitz if character can learn natural magic

        from ..data.spells import Spells

        def call_check_spell_learn(space, spell_check_address, learner, unique_label):
            space.write(
                asm.CMP(learner, asm.IMM8),
                asm.BNE(unique_label),                  # branch if this is not the natural magic learner
                asm.PHA(),                              # save character id
                asm.JSR(spell_check_address, asm.ABS),  # learn spells for character's current level
                asm.PLA(),                              # restore character id
                unique_label,
            )

        def update_known_spells_address(space_start, learner):
            known_spells_start = 0x1a6e + Spells.SPELL_COUNT * learner

            # update which character's known spells are modified
            space = Reserve(space_start, space_start + 1, "natural magic known spells address", asm.NOP())
            space.write(known_spells_start.to_bytes(2, "little"))

        space = Allocate(Bank.C0, 19, "natural magic event character check", asm.NOP())
        natural_magic_check = space.next_address
        if self.learner1 is not None:
            call_check_spell_learn(space, 0xa196, self.learner1, self.learner1_name + "1")
            update_known_spells_address(0x0a1ac, self.learner1)
        if self.learner2 is not None:
            call_check_spell_learn(space, 0xa1b8, self.learner2, self.learner2_name + "2")
            update_known_spells_address(0x0a1ce, self.learner2)
        space.write(
            asm.RTS(),
        )

        space = Reserve(0x0a182, 0x0a189, "natural magic character check events", asm.NOP())
        if self.learner1 is not None or self.learner2 is not None:
            space.write(
                asm.JSR(natural_magic_check, asm.ABS),
            )

    def after_battle_check_mod(self):
        # modify after battle code to also check for swdtech/blitz if character can learn natural magic

        def call_check_spell_learn(space, learner, unique_label):
            space.write(
                asm.CMP(learner, asm.IMM8),
                asm.BNE(unique_label),      # branch if this is not the natural magic learner
                asm.A16(),
                asm.PHA(),                  # save character id and level
                asm.A8(),
                asm.JSR(0x61fc, asm.ABS),   # check if spell learned at level
                asm.A16(),
                asm.PLA(),                  # restore character id and level
                asm.A8(),
                unique_label,
            )

        space = Allocate(Bank.C2, 41, "natural magic character check", asm.NOP())
        natural_magic_check = space.next_address
        if self.learner1 is not None:
            space.copy_from(0x261b6, 0x261b8)   # initialize x to 0 (start of terra natural magic)
            call_check_spell_learn(space, self.learner1, self.learner1_name + "1")
        if self.learner2 is not None:
            space.copy_from(0x261bd, 0x261bf)   # initialize x to 32 (start of celes natural magic)
            call_check_spell_learn(space, self.learner2, self.learner2_name + "2")
        space.write(
            asm.RTS(),
        )

        space = Reserve(0x261b6, 0x261c3, "natural magic character check after battle", asm.NOP())
        if self.learner1 is not None or self.learner2 is not None:
            space.write(
                asm.JSR(natural_magic_check, asm.ABS),
            )

    def mod_learners(self):
        import random
        from ..data.characters import Characters
        possible_learners = list(range(Characters.CHARACTER_COUNT - 2)) # exclude gogo/umaro

        if self.args.natural_magic1 == "random":
            self.learner1 = random.choice(possible_learners)
            self.learner1_name = self.characters.get_name(self.learner1)
        elif self.args.natural_magic1:
            self.learner1 = self.characters.get_by_name(self.args.natural_magic1).id
            self.learner1_name = self.characters.get_name(self.learner1)
        else:
            self.learner1 = None
            self.learner1_name = ""

        try:
            possible_learners.remove(self.learner1)
        except ValueError:
            pass

        if self.args.natural_magic2 == "random":
            self.learner2 = random.choice(possible_learners)
            self.learner2_name = self.characters.get_name(self.learner2)
        elif self.args.natural_magic2:
            self.learner2 = self.characters.get_by_name(self.args.natural_magic2).id
            self.learner2_name = self.characters.get_name(self.learner2)
        else:
            self.learner2 = None
            self.learner2_name = ""

        self.event_check_mod()
        self.after_battle_check_mod()

    def randomize_spells1(self):
        random_spells = self.spells.get_random(count = len(self.terra_spells), exclude = self.args.remove_learnable_spell_ids)
        for index, spell in enumerate(random_spells):
            self.terra_spells[index].spell = spell

    def randomize_spells2(self):
        random_spells = self.spells.get_random(count = len(self.celes_spells), exclude = self.args.remove_learnable_spell_ids)
        for index, spell in enumerate(random_spells):
            self.celes_spells[index].spell = spell

    def remove_excluded(self):
        for a_spell_id in self.args.remove_learnable_spell_ids:

            #linear search through Terra's spells
            for terra_spell in self.terra_spells:
                if terra_spell.spell == a_spell_id:
                    terra_spell.spell = 0xFF
                    terra_spell.level = 0

            #linear search through Celes' spells
            for celes_spell in self.celes_spells:
                if celes_spell.spell == a_spell_id:
                    celes_spell.spell = 0xFF
                    celes_spell.level = 0

    def randomize_levels1(self):
        import random
        levels = random.sample(range(1, 100), len(self.terra_spells))
        sorted_levels = sorted(levels)

        for index, spell in enumerate(self.terra_spells):
            spell.level = sorted_levels[index]

    def randomize_levels2(self):
        import random
        levels = random.sample(range(1, 100), len(self.celes_spells))
        sorted_levels = sorted(levels)

        for index, spell in enumerate(self.celes_spells):
            spell.level = sorted_levels[index]

    def mod(self):
        self.mod_learners()

        if self.args.natural_magic1:
            if self.args.random_natural_levels1:
                self.randomize_levels1()
            if self.args.random_natural_spells1:
                self.randomize_spells1()

        if self.args.natural_magic2:
            if self.args.random_natural_levels2:
                self.randomize_levels2()
            if self.args.random_natural_spells2:
                self.randomize_spells2()

        # Remove any excluded spells remaining. 
        # As randomize_spells respects the exclusion list, this should only have the effect of removing any excluded non-random spells.
        self.remove_excluded()

    def log(self):
        from ..log import section, format_option

        lcolumn = [self.learner1_name]
        if self.args.natural_magic1:
            for spell in self.terra_spells:
                if spell.level:
                    name = self.spells.get_name(spell.spell)
                    lcolumn.append(format_option(name, spell.level))

        rcolumn = [self.learner2_name]
        if self.args.natural_magic2:
            for spell in self.celes_spells:
                if spell.level:
                    name = self.spells.get_name(spell.spell)
                    rcolumn.append(format_option(name, spell.level))

        section("Natural Magic", lcolumn, rcolumn)

    def write(self):
        if self.args.spoiler_log:
            self.log()

        for spell_index, spell in enumerate(self.terra_spells):
            self.terra_spell_data[spell_index] = spell.data()
        self.terra_spell_data.write()

        for spell_index, spell in enumerate(self.celes_spells):
            self.celes_spell_data[spell_index] = spell.data()
        self.celes_spell_data.write()
