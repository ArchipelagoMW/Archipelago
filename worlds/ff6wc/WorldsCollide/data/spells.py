from ..data.spell import Spell
from ..data.spell_names import id_name, name_id
from ..data.ability_data import AbilityData
from ..data.structures import DataArray
from ..memory.space import Reserve

class Spells:
    BLACK_MAGIC_COUNT = 24
    EFFECT_MAGIC_COUNT = 21
    WHITE_MAGIC_COUNT = 9
    SPELL_COUNT = BLACK_MAGIC_COUNT + EFFECT_MAGIC_COUNT + WHITE_MAGIC_COUNT

    NAMES_START = 0x26f567
    NAMES_END = 0x26f6e0
    NAME_SIZE = 7

    ABILITY_DATA_START = 0x046ac0
    ABILITY_DATA_END = 0x046db3

    # (default) order spells appear in menu going left to right, top to bottom
    # put white magic before black and effect magic
    import itertools
    spell_menu_order = itertools.chain(range(45, 54), range(45))

    def __init__(self, rom, args):
        self.rom = rom
        self.args = args

        self.name_data = DataArray(self.rom, self.NAMES_START, self.NAMES_END, self.NAME_SIZE)
        self.ability_data = DataArray(self.rom, self.ABILITY_DATA_START, self.ABILITY_DATA_END, AbilityData.DATA_SIZE)

        self.spells = []
        for spell_index in range(len(self.name_data)):
            spell = Spell(spell_index, self.name_data[spell_index], self.ability_data[spell_index])
            self.spells.append(spell)

    def get_id(self, name):
        return name_id[name]

    def get_name(self, id):
        if id == 0xff:
            return ""
        return self.spells[id].get_name()

    def get_random(self, count = 1, exclude = None):
        if exclude is None:
            exclude = []

        import random
        possible_spell_ids = [spell.id for spell in self.spells if spell.id not in exclude]
        count = min(len(possible_spell_ids), count)
        return random.sample(possible_spell_ids, count)

    def get_replacement(self, spell_id, exclude):
        ''' get a random spell from the same tier as the given spell_id '''
        import random
        from ..data.esper_spell_tiers import tiers

        same_tier = next((tier for tier in tiers if spell_id in tier), [])
        replacements = [i for i in same_tier if i not in exclude]
        replacement = random.choice(replacements) if len(replacements) else None
        return replacement

    def no_mp_scan(self):
        scan_id = name_id["Scan"]
        self.spells[scan_id].mp = 0

    def no_mp_warp(self):
        warp_id = name_id["Warp"]
        self.spells[warp_id].mp = 0

    def ultima_254_mp(self):
        ultima_id = name_id["Ultima"]
        self.spells[ultima_id].mp = 254

    def shuffle_mp(self):
        mp = []
        for spell in self.spells:
            mp.append(spell.mp)

        import random
        random.shuffle(mp)
        for spell in self.spells:
            spell.mp = mp.pop()

    def random_mp_value(self):
        import random
        for spell in self.spells:
            spell.mp = random.randint(self.args.magic_mp_random_value_min, self.args.magic_mp_random_value_max)

    def random_mp_percent(self):
        import random
        for spell in self.spells:
            mp_percent = random.randint(self.args.magic_mp_random_percent_min,
                                        self.args.magic_mp_random_percent_max) / 100.0
            value = int(spell.mp * mp_percent)
            spell.mp = max(min(value, 254), 0)

    def alternate_healing_text_color(self):
        #Thanks to Osteoclave for identifying this change
        space = Reserve(0x02c693, 0x02c694, "alternate healing color")
        space.write(0x44, 0x7f) #default: F6 4B

    def mod(self):
        if self.args.magic_mp_shuffle:
            self.shuffle_mp()
        elif self.args.magic_mp_random_value:
            self.random_mp_value()
        elif self.args.magic_mp_random_percent:
            self.random_mp_percent()

        # Apply No MP Scan after any MP shuffle/rando
        if self.args.scan_all:
            self.no_mp_scan()
        if self.args.warp_all:
            self.no_mp_warp()

        # Apply Ultima 254 MP after any MP shuffle/rando
        if self.args.ultima_254_mp:
            self.ultima_254_mp()

        # Graphical changes to spells
        if self.args.alternate_healing_text_color:
            self.alternate_healing_text_color()

    def write(self):
        if self.args.spoiler_log:
            self.log()
            
        for spell_index, spell in enumerate(self.spells):
            self.name_data[spell_index] = spell.name_data()
            self.ability_data[spell_index] = spell.ability_data()

        self.name_data.write()
        self.ability_data.write()

    def log(self):
        from ..log import section
        
        lcolumn = []
        for spell in self.spells:
            spell_name = spell.get_name()

            lcolumn.append(f"{spell_name:<{self.NAME_SIZE}} {spell.mp:>3} MP")
        
        section("Spells", lcolumn, [])

    def print(self):
        for spell in self.spells:
            spell.print()
