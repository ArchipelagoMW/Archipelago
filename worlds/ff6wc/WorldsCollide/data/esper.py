from ..data.ability_data import AbilityData
from ..data import text as text

from enum import IntFlag

class Esper(AbilityData):
    NO_BONUS = 0xff
    HP_10_PERCENT, HP_30_PERCENT, HP_50_PERCENT, MP_10_PERCENT, MP_30_PERCENT, MP_50_PERCENT, HP_100_PERCENT,\
    LVL_30_PERCENT, LVL_50_PERCENT, STRENGTH_1, STRENGTH_2, SPEED_1, SPEED_2, STAMINA_1, STAMINA_2, MAGIC_1, MAGIC_2 = range(17)

    LEARN_RATES = [1, 2, 3, 4, 5, 6, 7, 8, 10, 15, 16, 20]

    SPELL_COUNT = 5
    NO_SPELL = 0xff

    class SpellEntry:
        def __init__(self, id, rate):
            self.id = id
            self.rate = rate

        def __lt__(self, other):
            return self.id < other.id

    def __init__(self, id, spells_bonus_data, name_data, ability_data):
        super().__init__(id, ability_data)

        self.id = id
        self.name = text.get_string(name_data, text.TEXT2).rstrip('\0')

        self.spells = []
        self.spell_count = 0
        for spell_index in range(self.SPELL_COUNT):
            spell = self.SpellEntry(spells_bonus_data[spell_index * 2 + 1], spells_bonus_data[spell_index * 2])
            self.spells.append(spell)

            if spell.id != self.NO_SPELL:
                self.spell_count += 1

        self.bonus = spells_bonus_data[10]
        self.equipable_characters = 0x3fff # equipable characters bitmask (default to all)

    def spells_bonus_data(self):
        from ..data.espers import Espers
        data = [0x00] * Espers.SPELLS_BONUS_DATA_SIZE

        for spell_index in range(self.SPELL_COUNT):
            data[spell_index * 2 + 1] = self.spells[spell_index].id
            data[spell_index * 2] = self.spells[spell_index].rate

        data[10] = self.bonus
        return data

    def name_data(self):
        from ..data.espers import Espers
        data = text.get_bytes(self.name, text.TEXT2)
        data.extend([0xff] * (Espers.NAME_SIZE - len(data)))
        return data

    def get_name(self):
        return self.name.strip('\0')

    def has_spell(self, spell):
        for spell_index in range(self.SPELL_COUNT):
            if self.spells[spell_index].id == spell:
                return True
        return False

    def add_spell(self, spell, learn_rate):
        if spell == self.NO_SPELL:
            return
        if self.has_spell(spell):
            return

        for spell_index in range(self.SPELL_COUNT):
            if self.spells[spell_index].id == self.NO_SPELL:
                self.spells[spell_index].id = spell
                self.spells[spell_index].rate = learn_rate
                self.spell_count += 1
                return
        print(f"Error: Could not add spell {spell} to esper {self.id}. Esper spell slots are full")

    def remove_spell(self, spell):
        if spell == self.NO_SPELL:
            return

        # remove every instance of given spell and maintain ordering of other spells
        prev_spells_len = len(self.spells)
        self.spells = [spell_entry for spell_entry in self.spells if spell_entry.id != spell]

        spells_removed = prev_spells_len - len(self.spells)
        self.spell_count -= spells_removed
        for spell_index in range(spells_removed):
            self.spells.append(self.SpellEntry(self.NO_SPELL, 0))

    def get_spell_ids(self):
        return [spell.id for spell in self.spells if spell.id != self.NO_SPELL]

    def replace_spell(self, old_spell, new_spell):
        if(old_spell == self.NO_SPELL):
            return

        # get the old learn rate to reuse it
        learn_rate = self.LEARN_RATES[0]
        for spell_index in range(self.SPELL_COUNT):
            if self.spells[spell_index].id == old_spell:
                learn_rate = self.spells[spell_index].rate

        self.remove_spell(old_spell)
        if new_spell is not None:
            self.add_spell(new_spell, learn_rate)

    def clear_spells(self):
        for spell_index in range(self.SPELL_COUNT):
            self.spells[spell_index].id = self.NO_SPELL
            self.spells[spell_index].rate = 0
        self.spell_count = 0

    def set_bonus(self, bonus):
        if bonus < 0 or bonus > self.MAGIC_2:
            self.bonus = self.NO_BONUS
            return

        if bonus == self.LVL_30_PERCENT or bonus == self.LVL_50_PERCENT:
            self.bonus = self.NO_BONUS
            return

        self.bonus = bonus

    def randomize_rates(self):
        import random
        for spell_index in range(self.spell_count):
            self.spells[spell_index].rate = random.choice(self.LEARN_RATES)

    def randomize_rates_tiered(self):
        import random
        from ..data.esper_spell_tiers import tiers
        for spell_index in range(self.spell_count):
            if self.spells[spell_index].id in tiers[0]:
                self.spells[spell_index].rate = random.choice([10, 15, 16, 20])
            elif self.spells[spell_index].id in tiers[1]:
                self.spells[spell_index].rate = random.choice([5, 6, 7, 8])
            elif self.spells[spell_index].id in tiers[2]:
                self.spells[spell_index].rate = random.choice([1, 2, 3, 4])
            elif self.spells[spell_index].id in tiers[3]:
                self.spells[spell_index].rate = random.choice([10, 15, 16, 20])
            elif self.spells[spell_index].id in tiers[4]:
                self.spells[spell_index].rate = random.choice([6, 7, 8, 10, 15])
            elif self.spells[spell_index].id in tiers[5]:
                self.spells[spell_index].rate = random.choice([4, 5, 6, 7, 8])
            elif self.spells[spell_index].id in tiers[6]:
                self.spells[spell_index].rate = random.choice([2, 3, 4])
            elif self.spells[spell_index].id in tiers[7]:
                self.spells[spell_index].rate = 1

    def randomize_bonus(self):
        import random
        # exclude lvl percent bonuses
        possible = [self.HP_10_PERCENT, self.HP_30_PERCENT, self.HP_50_PERCENT, self.MP_10_PERCENT,
                    self.MP_30_PERCENT, self.MP_50_PERCENT, self.HP_100_PERCENT, self.STRENGTH_1, self.STRENGTH_2,
                    self.SPEED_1, self.SPEED_2, self.STAMINA_1, self.STAMINA_2, self.MAGIC_1, self.MAGIC_2]
        self.set_bonus(random.choice(possible))

    def get_equipable_characters(self):
        from ..data.characters import Characters
        characters = []
        for character in range(Characters.CHARACTER_COUNT):
            if self.equipable_characters & (1 << character):
                characters.append(character)
        return characters

    def get_bonus_string(self):
        if self.bonus == self.HP_10_PERCENT:
            return "HP +10%"
        if self.bonus == self.HP_30_PERCENT:
            return "HP +30%"
        if self.bonus == self.HP_50_PERCENT:
            return "HP +50%"
        if self.bonus == self.MP_10_PERCENT:
            return "MP +10%"
        if self.bonus == self.MP_30_PERCENT:
            return "MP +30%"
        if self.bonus == self.MP_50_PERCENT:
            return "MP +50%"
        if self.bonus == self.HP_100_PERCENT:
            return "HP +100%"
        if self.bonus == self.LVL_30_PERCENT:
            return "LVL +30%"
        if self.bonus == self.LVL_50_PERCENT:
            return "LVL +50%"
        if self.bonus == self.STRENGTH_1:
            return "STRENGTH +1"
        if self.bonus == self.STRENGTH_2:
            return "STRENGTH +2"
        if self.bonus == self.SPEED_1:
            return "SPEED +1"
        if self.bonus == self.SPEED_2:
            return "SPEED +2"
        if self.bonus == self.STAMINA_1:
            return "STAMINA +1"
        if self.bonus == self.STAMINA_2:
            return "STAMINA +2"
        if self.bonus == self.MAGIC_1:
            return "MAGIC +1"
        if self.bonus == self.MAGIC_2:
            return "MAGIC +2"
        return ""

    def print(self, spells):
        print(f"{self.id} {self.name}:")
        for x in range(self.SPELL_COUNT):
            if self.spells[x].id != self.NO_SPELL:
                print(f"  {self.spells[x].id} {spells.get_name(self.spells[x].id)} x{self.spells[x].rate}, ")
        print(f"{self.get_bonus_string()}")

