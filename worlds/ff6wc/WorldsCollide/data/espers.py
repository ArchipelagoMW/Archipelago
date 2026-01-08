from ..data.esper import Esper
from ..data.ability_data import AbilityData
from ..data.structures import DataArray

from ..data import espers_asm as espers_asm
import random

class Espers():
    ESPER_COUNT = 27

    RAMUH, IFRIT, SHIVA, SIREN, TERRATO, SHOAT, MADUIN, BISMARK, STRAY, PALIDOR, TRITOCH, ODIN, RAIDEN, BAHAMUT, ALEXANDR,\
    CRUSADER, RAGNAROK, KIRIN, ZONESEEK, CARBUNKL, PHANTOM, SRAPHIM, GOLEM, UNICORN, FENRIR, STARLET, PHOENIX = range(ESPER_COUNT)

    esper_names = ["Ramuh", "Ifrit", "Shiva", "Siren", "Terrato", "Shoat", "Maduin", "Bismark", "Stray", "Palidor", "Tritoch",
                   "Odin", "Raiden", "Bahamut", "Alexandr", "Crusader", "Ragnarok", "Kirin", "ZoneSeek", "Carbunkl", "Phantom",
                   "Sraphim", "Golem", "Unicorn", "Fenrir", "Starlet", "Phoenix"]

    # order epsers appear in menu going left to right, top to bottom
    esper_menu_order = [0, 17, 3, 8, 1, 2, 23, 6, 5, 20, 19, 7, 22, 18, 21, 9, 24, 10, 4, 25, 14, 26, 11, 13, 16, 15, 12]

    SPELLS_BONUS_DATA_START = 0x186e00
    SPELLS_BONUS_DATA_END = 0x186fff
    SPELLS_BONUS_DATA_SIZE = 11

    NAMES_START = 0x26f6e1
    NAMES_END = 0x26f7b8
    NAME_SIZE = 8

    ABILITY_DATA_START = 0x046db4
    ABILITY_DATA_END = 0x046fd5

    def __init__(self, rom, args, spells, characters):
        self.rom = rom
        self.args = args
        self.spells = spells
        self.characters = characters

        self.spells_bonus_data = DataArray(self.rom, self.SPELLS_BONUS_DATA_START, self.SPELLS_BONUS_DATA_END, self.SPELLS_BONUS_DATA_SIZE)
        self.name_data = DataArray(self.rom, self.NAMES_START, self.NAMES_END, self.NAME_SIZE)
        self.ability_data = DataArray(self.rom, self.ABILITY_DATA_START, self.ABILITY_DATA_END, AbilityData.DATA_SIZE)

        self.espers = []
        for esper_index in range(len(self.name_data)):
            esper = Esper(esper_index, self.spells_bonus_data[esper_index], self.name_data[esper_index], self.ability_data[esper_index])
            self.espers.append(esper)

        self.available_espers = list(range(self.ESPER_COUNT))
        self.starting_espers = []

        if args.starting_espers_min > 0:
            count = random.randint(args.starting_espers_min, args.starting_espers_max)
            self.starting_espers = [self.get_random_esper() for _esp in range(count)]

        # else if specific espers were named to start
        elif args.starting_espers_named:
            # for each esper in the list
            for specific_esper in args.starting_espers_list:
                # make sure we get that specific one
                self.starting_espers.append(self.get_specific_esper(self.esper_names[specific_esper]))

    def receive_dialogs_mod(self, dialogs):
        self.receive_dialogs = [1133, 1380, 1381, 1134, 1535, 1082, 1091, 1092, 1136, 1534, 2618, 1093, 1087,\
                                2975, 2799, 1506, 1095, 1135, 2755, 1097, 1098, 1572, 2756, 1099, 2273, 2733, 1100]

        # replace some dialog with ramuh in zozo with missing received esper dialogs
        dialogs.set_text(self.receive_dialogs[self.SHOAT],      '<line>     Received the Magicite<line>              “Shoat.”<end>')
        dialogs.set_text(self.receive_dialogs[self.MADUIN],     '<line>     Received the Magicite<line>              “Maduin.”<end>')

        dialogs.set_text(self.receive_dialogs[self.BISMARK],    '<line>     Received the Magicite<line>              “Bismark.”<end>')
        dialogs.set_text(self.receive_dialogs[self.ODIN],       '<line>     Received the Magicite<line>              “Odin.”<end>')
        dialogs.set_text(self.receive_dialogs[self.RAIDEN],     '<line>     Received the Magicite<line>              “Raiden.”<end>')
        #dialogs.set_text(self.receive_dialogs[self.RAIDEN],     '<line>   The Magicite "Odin" gains<line>              a level…<page><line>   and becomes the Magicite<line>              "Raiden!"<end>')
        dialogs.set_text(self.receive_dialogs[self.RAGNAROK],   '<line>     Received the Magicite<line>              “Ragnarok.”<end>')
        dialogs.set_text(self.receive_dialogs[self.CARBUNKL],   '<line>     Received the Magicite<line>              “Carbunkl.”<end>')
        dialogs.set_text(self.receive_dialogs[self.PHANTOM],    '<line>     Received the Magicite<line>              “Phantom.”<end>')
        dialogs.set_text(self.receive_dialogs[self.UNICORN],    '<line>     Received the Magicite<line>              “Unicorn.”<end>')
        dialogs.set_text(self.receive_dialogs[self.PHOENIX],    '<line>     Received the Magicite<line>              “Phoenix.”<end>')

        # remove phunbaba part of received fenrir dialog
        dialogs.set_text(self.receive_dialogs[self.FENRIR],     '<line>     Received the Magicite<line>              “Fenrir.”<end>')

    def shuffle_spells(self):
        # to prevent duplicates, get list of spells and sort it by their frequency
        # the sort prevents ending up with more than one of the same spell and only one esper left to give them to
        # randomly pick espers until find one without the spell and add it
        # once the esper has as many spells as it originally did remove it from available pool
        import copy
        spells = []
        for esper in self.espers:
            for spell_index in range(Esper.SPELL_COUNT):
                if esper.spells[spell_index].id != Esper.NO_SPELL:
                    spells.append(copy.deepcopy(esper.spells[spell_index]))

        # sort spells based on their frequency (the key is the spell id), most frequent last so they are popped first
        # NOTE: this does not also sort by spell id as a secondary key so resulting spells will not be in
        #       any order except the frequency of spell ids
        import collections
        frequencies = collections.Counter(spell.id for spell in spells)
        spells = sorted(spells, key = lambda spell: frequencies[spell.id])

        # get spell counts and pool of available espers and clear the spells they have now
        spell_counts = []
        esper_indices = []
        for esper_index, esper in enumerate(self.espers):
            spell_counts.append(esper.spell_count)
            esper.clear_spells()
            esper_indices.append(esper_index)

        random.shuffle(spell_counts)

        while len(spells) > 0:
            esper_index = random.choice(esper_indices)
            esper = self.espers[esper_index]
            if not esper.has_spell(spells[-1].id):
                spell = spells.pop()
                if self.args.esper_spells_shuffle_random_rates:
                    esper.add_spell(spell.id, random.choice(Esper.LEARN_RATES))
                else:
                    esper.add_spell(spell.id, spell.rate)
                if esper.spell_count == spell_counts[esper_index]:
                    esper_indices.remove(esper_index)

    def randomize_spells(self):
        for esper in self.espers:
            esper.clear_spells()
            num_spells = random.randint(self.args.esper_spells_random_min, self.args.esper_spells_random_max)
            spells = self.spells.get_random(count = num_spells)
            for spell_id in spells:
                esper.add_spell(spell_id, random.choice(Esper.LEARN_RATES))

    def randomize_spells_tiered(self):
        def get_spell():
            from ..data.esper_spell_tiers import tiers, weights, tier_s_distribution
            from ..ff6wcutils.weighted_random import weighted_random

            random_tier = weighted_random(weights)
            if random_tier < len(weights) - 1: # not s tier, use equal distribution
                random_tier_index = random.randrange(len(tiers[random_tier]))
                return tiers[random_tier][random_tier_index]

            weights = [entry[1] for entry in tier_s_distribution]
            random_s_index = weighted_random(weights)
            return tier_s_distribution[random_s_index][0]

        for esper in self.espers:
            esper.clear_spells()
            num_spells = random.randint(1, Esper.SPELL_COUNT)
            for spell_index in range(num_spells):
                learn_rate_index = int(random.triangular(0, len(Esper.LEARN_RATES), 0))
                if learn_rate_index == len(Esper.LEARN_RATES):
                    # triangular max is inclusive, very small chance need to round max down
                    learn_rate_index -= 1
                learn_rate = Esper.LEARN_RATES[learn_rate_index]
                esper.add_spell(get_spell(), learn_rate)

    def remove_flagged_learnables(self):
        for a_spell_id in self.args.remove_learnable_spell_ids:
            for esper in self.espers:
                if(esper.has_spell(a_spell_id)):
                    esper.remove_spell(a_spell_id)

    def replace_flagged_learnables(self):
        for esper in self.espers:
            for a_spell_id in self.args.remove_learnable_spell_ids:
                if(esper.has_spell(a_spell_id)):
                    # Also exclude spells this Esper already knows, to avoid duplicates
                    exclude_spell_ids = self.args.remove_learnable_spell_ids.copy()
                    exclude_spell_ids.extend(esper.get_spell_ids())

                    new_spell_id = self.spells.get_replacement(a_spell_id, exclude = exclude_spell_ids)
                    esper.replace_spell(a_spell_id, new_spell_id)


    def clear_spells(self):
        for esper in self.espers:
            esper.clear_spells()

    def randomize_rates(self):
        for esper in self.espers:
            esper.randomize_rates()

    def randomize_rates_tiered(self):
        for esper in self.espers:
            esper.randomize_rates_tiered()

    def shuffle_bonuses(self):
        bonuses = []
        for esper in self.espers:
            bonuses.append(esper.bonus)

        random.shuffle(bonuses)
        for esper in self.espers:
            esper.set_bonus(bonuses.pop())

    def randomize_bonuses(self):
        bonus_percent = self.args.esper_bonuses_random_percent / 100.0
        for esper in self.espers:
            if random.random() < bonus_percent:
                esper.randomize_bonus()
            else:
                esper.set_bonus(Esper.NO_BONUS)

    def shuffle_mp(self):
        mp = []
        for esper in self.espers:
            mp.append(esper.mp)

        random.shuffle(mp)
        for esper in self.espers:
            esper.mp = mp.pop()

    def random_mp_value(self):
        for esper in self.espers:
            esper.mp = random.randint(self.args.esper_mp_random_value_min, self.args.esper_mp_random_value_max)

    def random_mp_percent(self):
        for esper in self.espers:
            mp_percent = random.randint(self.args.esper_mp_random_percent_min,
                                        self.args.esper_mp_random_percent_max) / 100.0
            value = int(esper.mp * mp_percent)
            esper.mp = max(min(value, 254), 1)

    def equipable_random(self):
        from ..data.characters import Characters
        possible_characters = list(range(Characters.CHARACTER_COUNT - 2)) # exclude gogo/umaro

        for esper in self.espers:
            esper.equipable_characters = 0 # set equipable by no characters
            number_characters = random.randint(self.args.esper_equipable_random_min, self.args.esper_equipable_random_max)
            random_characters = random.sample(possible_characters, number_characters)
            for character in random_characters:
                esper.equipable_characters |= (1 << character)

    def equipable_balanced_random(self):
        # assign each esper exactly characters_per_esper unique characters
        # the total number of espers each character can equip should also be balanced
        # e.g. given 27 espers and 3 characters_per_esper:
        #      27 * 3 = 81 total equipable slots to assign, the 3 characters should be unique for each esper
        #      81 // 12 = 6, each character can equip 6 different espers
        #      81 % 12 = 9, 9 characters can equip 1 additional esper (7 total for those 9)

        from ..data.characters import Characters
        possible_characters = list(range(Characters.CHARACTER_COUNT - 2)) # exclude gogo/umaro
        characters_per_esper = self.args.esper_equipable_balanced_random_value

        for esper in self.espers:
            esper.equipable_characters = 0 # set equipable by no characters
            if len(possible_characters) < characters_per_esper:
                # fewer possibilities left than number of characters needed for each esper
                character_group = possible_characters # add remaining possible characters to current group
                possible_characters = list(range(Characters.CHARACTER_COUNT - 2)) # add characters back into pool

                # select characters at random from possible pool until
                # character_group contains characters_per_esper unique characters
                while len(character_group) < characters_per_esper:
                    candidate = random.choice(possible_characters)
                    if candidate not in character_group:
                        character_group.append(candidate)
                        possible_characters.remove(candidate)

                # assign character group to current esper
                for character in character_group:
                    esper.equipable_characters |= (1 << character)
            else:
                character_group = random.sample(possible_characters, characters_per_esper)
                for character in character_group:
                    possible_characters.remove(character)
                    esper.equipable_characters |= (1 << character)

    def phoenix_life3(self):
        # change phoenix behavior to cast life 3 on party instead of life
        self.espers[self.PHOENIX].flags1 = 0
        self.espers[self.PHOENIX].flags3 = 0x20
        self.espers[self.PHOENIX].power = 0
        self.espers[self.PHOENIX].status1 = 0
        self.espers[self.PHOENIX].status4 = 0x04

    def multi_summon(self):
        from ..memory.space import Reserve
        from ..instruction import asm as asm

        space = Reserve(0x24da3, 0x24da5, "espers set used in battle bit", asm.NOP())

    def mod(self, dialogs):
        self.receive_dialogs_mod(dialogs)

        if self.args.esper_spells_shuffle or self.args.esper_spells_shuffle_random_rates:
            self.shuffle_spells()
        elif self.args.esper_spells_random:
            self.randomize_spells()
        elif self.args.esper_spells_random_tiered:
            self.randomize_spells_tiered()

        if self.args.esper_spells_random or self.args.esper_spells_random_tiered:
            # if random, replace the spells
            self.replace_flagged_learnables()
        else:
            # otherwise (original or shuffled), remove them
            self.remove_flagged_learnables()

        if self.args.esper_learnrates_random:
            self.randomize_rates()

        if self.args.esper_learnrates_random_tiered:
            self.randomize_rates_tiered()

        if self.args.esper_bonuses_shuffle:
            self.shuffle_bonuses()
        elif self.args.esper_bonuses_random:
            self.randomize_bonuses()

        if self.args.esper_mp_shuffle:
            self.shuffle_mp()
        elif self.args.esper_mp_random_value:
            self.random_mp_value()
        elif self.args.esper_mp_random_percent:
            self.random_mp_percent()

        if self.args.esper_equipable_random:
            self.equipable_random()
        elif self.args.esper_equipable_balanced_random:
            self.equipable_balanced_random()
        espers_asm.equipable_mod(self)

        if self.args.esper_mastered_icon:
            espers_asm.mastered_mod(self)

        if self.args.permadeath:
            self.phoenix_life3()

        if self.args.esper_multi_summon:
            self.multi_summon()

    def write(self):
        if self.args.spoiler_log:
            self.log()

        for esper_index in range(len(self.espers)):
            self.spells_bonus_data[esper_index] = self.espers[esper_index].spells_bonus_data()
            self.name_data[esper_index] = self.espers[esper_index].name_data()
            self.ability_data[esper_index] = self.espers[esper_index].ability_data()

        self.spells_bonus_data.write()
        self.name_data.write()
        self.ability_data.write()

    def available(self) -> int:
        return len(self.available_espers)

    def get_random_esper(self):
        if not self.available_espers:
            return None

        rand_esper = random.sample(self.available_espers, 1)[0]
        self.available_espers.remove(rand_esper)
        return rand_esper
    
    def get_specific_esper(self, name: str) -> int:
        chosen_esper = None
        for index, esper in enumerate(self.espers):
            if esper.name == name:
                chosen_esper = esper
                break
        self.available_espers.remove(index)
        return index

    def get_receive_esper_dialog(self, esper):
        return self.receive_dialogs[esper]

    def get_name(self, esper):
        return self.esper_names[esper]

    def log(self):
        from ..log import COLUMN_WIDTH, section_entries, format_option
        from textwrap import wrap

        lentries = []
        rentries = []
        for entry_index in range(self.ESPER_COUNT):
            esper_index = self.esper_menu_order[entry_index]
            esper = self.espers[esper_index]
            prefix = "*" if esper.id in self.starting_espers else ""

            entry = [f"{prefix}{esper.get_name():<{self.NAME_SIZE}}  {esper.mp:>3} MP"]

            for spell_index in range(esper.spell_count):
                spell_name = self.spells.get_name(esper.spells[spell_index].id)
                learn_rate = esper.spells[spell_index].rate
                entry.append(format_option("{:<7} x{}".format(spell_name, str(learn_rate)), ""))

            bonus_string = esper.get_bonus_string()
            if bonus_string:
                entry.append(bonus_string)

            no_gogo_umaro_bits = 0xfff # bitmask for all characters except gogo/umaro
            if (esper.equipable_characters & no_gogo_umaro_bits) == no_gogo_umaro_bits:
                entry.append("Equipable: All")
            elif esper.equipable_characters == 0:
                entry.append("Equipable: None")
            else:
                character_names = []
                characters = esper.get_equipable_characters()
                for character in characters:
                    character_names.append(self.characters.get_name(character))

                character_names = "Equipable: " + ' '.join(character_names)
                character_names = wrap(character_names, width = COLUMN_WIDTH - 1)
                entry.append(character_names)

            if entry_index % 2:
                rentries.append(entry)
            else:
                lentries.append(entry)

        lentries.append("")
        lentries.append("* = Starting Esper")

        section_entries("Espers", lentries, rentries)

    def print(self):
        for esper in self.espers:
            esper.print(self.spells)
