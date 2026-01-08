import functools
import importlib
import itertools
import logging
import os
import random
import string
import threading
from typing import Any, ClassVar

from typing_extensions import override

from BaseClasses import Item, Location, Region, MultiWorld, ItemClassification, Tutorial
from .id_maps import item_name_to_id, location_name_to_id
from .item_rewards import build_ir_from_placements, get_item_rewards, limit_event_items
from .gen_data import GenData
from . import Rom
from .patch import FF6WCPatch, NA10HASH
from worlds.generic.Rules import add_rule, set_rule, add_item_rule
from worlds.AutoWorld import World, WebWorld
from . import Locations
from . import Items
from .Logic import can_beat_final_kefka
from .Options import FF6WCOptions, Treasuresanity, generate_flagstring, resolve_character_options, verify_flagstring
import Utils
import settings

importlib.import_module(".Client", "worlds.ff6wc")  # register with SNIClient


class FF6WCItem(Item):
    game = 'Final Fantasy 6 Worlds Collide'


class FF6WCLocation(Location):
    game = 'Final Fantasy 6 Worlds Collide'


class FF6WCSettings(settings.Group):
    class RomFile(settings.SNESRomPath):
        """File name of the FF6 NA 1.0 rom"""
        description = "Final Fantasy III (USA) ROM File"
        copy_to = "Final Fantasy III (USA).sfc"
        md5s = [NA10HASH]
    rom_file: RomFile = RomFile(RomFile.copy_to)


class FF6WCWeb(WebWorld):
    theme = "dirt"
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the FF6WC randomizer and connecting to an Archipelago server.",
        "English",
        "setup_en.md",
        "setup/en",
        ["bigmalletman"]
    )
    tutorials = [setup_en]


class FF6WCWorld(World):
    """
    Final Fantasy VI, initially called Final Fantasy III on the Super Nintendo in North America,
    is a role-playing game and the last in the series to feature 2D sprite based graphics.
    Worlds Collide is an open-world randomizer for Final Fantasy VI. Players begin aboard the airship
    and can travel freely between the World of Balance and the World of Ruin to discover characters and espers.
    Once you've gathered enough, you can face off against Kefka. Currently based on Worlds Collide version 1.4.2.
    """
    options_dataclass = FF6WCOptions
    options: FF6WCOptions  # type: ignore
    settings: ClassVar[FF6WCSettings]  # type: ignore
    game = "Final Fantasy 6 Worlds Collide"
    location_name_groups = {
        "Terra Major": {*Locations.major_terra_checks},
        "Locke Major": {*Locations.major_locke_checks},
        "Edgar Major": {*Locations.major_edgar_checks},
        "Sabin Major": {*Locations.major_sabin_checks},
        "Celes Major": {*Locations.major_celes_checks},
        "Shadow Major": {*Locations.major_shadow_checks},
        "Cyan Major": {*Locations.major_cyan_checks},
        "Gau Major": {*Locations.major_gau_checks},
        "Setzer Major": {*Locations.major_setzer_checks},
        "Mog Major": {*Locations.major_mog_checks},
        "Strago Major": {*Locations.major_strago_checks},
        "Relm Major": {*Locations.major_relm_checks},
        "Umaro Major": {*Locations.major_umaro_checks},
        "Gogo Major": {*Locations.major_gogo_checks},
        "Kefka Major": {*Locations.major_kefka_checks},
        "Generic Major": {*Locations.major_generic_checks},
        "All Major": {*Locations.major_checks},
        "Terra Minor": {*Locations.minor_terra_checks},
        "Edgar Minor": {*Locations.minor_edgar_checks},
        "Sabin Minor": {*Locations.minor_sabin_checks},
        "Celes Minor": {*Locations.minor_celes_checks},
        "Shadow Minor": {*Locations.minor_shadow_checks},
        "Cyan Minor": {*Locations.minor_cyan_checks},
        "Gau Minor": {*Locations.minor_gau_checks},
        "Setzer Minor": {*Locations.minor_setzer_checks},
        "Strago Minor": {*Locations.minor_strago_checks},
        "Relm Minor": {*Locations.minor_relm_checks},
        "Umaro Minor": {*Locations.minor_umaro_checks},
        "Gogo Minor": {*Locations.minor_gogo_checks},
        "Kefka Minor": {*Locations.minor_kefka_checks},
        "Generic Minor": {*Locations.minor_generic_checks},
        "All Minor": {*Locations.minor_checks}
    }
    topology_present = False
    data_version = 0
    web = FF6WCWeb()
    wc_ready = threading.Lock()
    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id

    all_characters = [
        'Terra', 'Locke', 'Cyan', 'Shadow', 'Edgar',
        'Sabin', 'Celes', 'Strago', 'Relm', 'Setzer',
        'Mog', 'Gau', 'Gogo', 'Umaro'
    ]

    all_espers = [
        "Ramuh", "Ifrit", "Shiva", "Siren", "Terrato", "Shoat", "Maduin",
        "Bismark", "Stray", "Palidor", "Tritoch", "Odin", "Raiden", "Bahamut",
        "Alexandr", "Crusader", "Ragnarok Esper", "Kirin", "ZoneSeek", "Carbunkl",
        "Phantom", "Sraphim", "Golem", "Unicorn", "Fenrir", "Starlet", "Phoenix",
    ]

    all_dragon_clears = [
        "Removed!", "Stomped!",
        "Blasted!", "Ditched!",
        "Wiped!", "Incinerated!",
        "Skunked!", "Gone!"
    ]

    item_name_groups = {
        'characters': set(all_characters),
        'espers': set(all_espers),
    }

    starting_characters: list[str] | None
    flagstring: list[str] | None

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)
        self.starting_characters = None
        self.starting_espers = []
        self.flagstring = None
        self.item_rewards = []
        self.item_nonrewards = []
        self.generator_in_use = threading.Event()
        self.wc = None
        self.rom_name = bytearray()
        self.rom_name_available_event = threading.Event()

    @override
    def create_item(self, name: str):
        return FF6WCItem(name, ItemClassification.progression, self.item_name_to_id[name], self.player)

    def create_good_filler_item(self, name: str):
        return FF6WCItem(name, ItemClassification.useful, self.item_name_to_id[name], self.player)

    def create_filler_item(self, name: str):
        return FF6WCItem(name, ItemClassification.filler, self.item_name_to_id[name], self.player)

    def create_event(self, event: str):
        return FF6WCItem(event, ItemClassification.progression, None, self.player)

    def create_location(self, name: str, id: int | None, parent: Region) -> FF6WCLocation:
        return_location = FF6WCLocation(self.player, name, id, parent)
        return return_location

    @override
    def generate_early(self):
        # if requested to exclude the Zozo Clock Chest, add to exclude_locations
        if self.options.ZozoClockChestExclude:
            self.options.exclude_locations.value.add("Zozo Clock Puzzle")

        if (self.options.Flagstring.value).capitalize() != "False":

            self.starting_characters = []
            self.starting_espers = []
            character_list: list[str] = []
            flags = self.options.Flagstring.value
            # Determining Starting Characters
            flags_list = flags.split(" ")
            sc1_index = flags_list.index("-sc1") + 1
            character_list.append(flags_list[sc1_index])
            sc2_index = sc3_index = sc4_index = len(flags_list)
            if "-sc2" in flags_list:
                sc2_index = flags_list.index("-sc2") + 1
                character_list.append(flags_list[sc2_index])
            if "-sc3" in flags_list:
                sc3_index = flags_list.index("-sc3") + 1
                character_list.append(flags_list[sc3_index])
            if "-sc4" in flags_list:
                sc4_index = flags_list.index("-sc4") + 1
                character_list.append(flags_list[sc4_index])

            for character in range(len(character_list)):
                if character_list[character] == "randomngu":
                    compare_character_list = character_list.copy()
                    character_list[character] = random.choice(Rom.characters[:12]).lower()
                    while character_list[character] in compare_character_list:
                        character_list[character] = random.choice(Rom.characters[:12]).lower()
                elif character_list[character] == "random":
                    compare_character_list = character_list.copy()
                    character_list[character] = random.choice(Rom.characters[:14]).lower()
                    while character_list[character] in compare_character_list:
                        character_list[character] = random.choice(Rom.characters[:14]).lower()
                elif character_list[character] not in character_list:
                    character_list[character] = character_list[character]

            for x in range(len(character_list)):
                if x == 0:
                    flags_list[sc1_index] = character_list[x]
                if x == 1:
                    flags_list[sc2_index] = character_list[x]
                if x == 2:
                    flags_list[sc3_index] = character_list[x]
                if x == 3:
                    flags_list[sc4_index] = character_list[x]

            self.options.StartingCharacterCount.value = len(character_list)
            starting_char_options = list(self.options.StartingCharacter1.name_lookup.values())
            self.options.StartingCharacter1.value = starting_char_options.index(character_list[0])
            self.options.StartingCharacter2.value = 14
            self.options.StartingCharacter3.value = 14
            self.options.StartingCharacter4.value = 14
            if len(character_list) > 1:
                self.options.StartingCharacter2.value = starting_char_options.index(character_list[1])
            if len(character_list) > 2:
                self.options.StartingCharacter3.value = starting_char_options.index(character_list[2])
            if len(character_list) > 3:
                self.options.StartingCharacter4.value = starting_char_options.index(character_list[3])

            proper_names = " ".join(character_list)
            proper_names = proper_names.title()
            character_list = proper_names.split(" ")
            self.starting_characters = character_list

            # Determining character, esper, dragon, and boss requirements
            # Finding KT Objective in flagstring (starts with 2)
            character_count = 0
            esper_count = 0
            dragon_count = 0
            boss_count = 0

            kt_obj_list: list[str] = []
            kt_obj_code_index = len(flags_list)
            alphabet = string.ascii_lowercase
            for letter in alphabet:
                objective = f"-o{letter}"
                try:
                    obj_i = flags_list.index(objective) + 1
                except ValueError:
                    # TODO: Is it legal to skip letters? -oa ... -ob ... -od
                    # if not, change continue to break
                    continue
                if obj_i >= len(flags_list):
                    raise ValueError(f"invalid flags {objective}")
                objective_code = flags_list[obj_i]
                objective_code_list = objective_code.split(".")
                if len(objective_code_list) < 3:
                    raise ValueError(f"invalid objective string for {objective}: {objective_code}")
                if objective_code_list[0] == "2":
                    kt_obj_list = objective_code_list
                    kt_obj_code_index = obj_i
                    break
            if kt_obj_code_index == len(flags_list):
                # TODO: use yaml options instead?
                raise ValueError("kt objective code not found in flags")
            # Determining Character, Esper, Dragon and Boss Counts
            # Since AP only (currently) takes in counts for bosses, espers, characters, and dragons, this code
            # identifies the root objective number/prefix, parses the ranges/values, and then tells the loop to skip to
            # the next requirement. There are requirements that have 2 inputs because of ranges (bosses, characters,
            # espers, dragons) and skip the next 2 indices in objective identification. The others only have 1 number in
            # objective identification and only skip 1/the next index

            # Also, the player can input a "range" of conditions to be met for KT entry. When building the AP logic of
            # the seed, suggest not including these ranges in the logic selection, but instead ensuring that all
            # possible conditions are required. As such, this section does not account for the range of conditions that
            # are required for seed completion. For example, if 1 of 2 conditions is required, one being 14 characters
            # and the other being Kill Cid, the logic should still be such that 14 characters can be acquired.

            not_ranged_obj_numbers = {"1", "3", "5", "7", "9", "11", "12"}  # Random or looking for something specific.

            err_msg = f"invalid kt objective string: {flags_list[kt_obj_code_index]}"
            cursor_i = 3
            while cursor_i < len(kt_obj_list):
                if kt_obj_list[cursor_i] in not_ranged_obj_numbers:  # not a ranged objective type
                    cursor_i += 1
                    if cursor_i >= len(kt_obj_list):
                        raise ValueError(err_msg)
                    cursor_i += 1
                    continue
                # is a ranged objective, note that checks (type "10") are not currently parsed by AP
                if cursor_i + 2 >= len(kt_obj_list):
                    raise ValueError(err_msg)
                try:
                    count_low = int(kt_obj_list[cursor_i + 1])
                    count_high = int(kt_obj_list[cursor_i + 2])
                except ValueError as e:
                    raise ValueError(err_msg) from e
                if kt_obj_list[cursor_i] == "2":
                    character_count = self.random.randint(count_low, count_high)
                    kt_obj_list[cursor_i + 1] = str(character_count)
                    kt_obj_list[cursor_i + 2] = str(character_count)
                elif kt_obj_list[cursor_i] == "4":
                    esper_count = self.random.randint(count_low, count_high)
                    kt_obj_list[cursor_i + 1] = str(esper_count)
                    kt_obj_list[cursor_i + 2] = str(esper_count)
                elif kt_obj_list[cursor_i] == "6":
                    dragon_count = self.random.randint(count_low, count_high)
                    kt_obj_list[cursor_i + 1] = str(dragon_count)
                    kt_obj_list[cursor_i + 2] = str(dragon_count)
                elif kt_obj_list[cursor_i] == "8":
                    boss_count = self.random.randint(count_low, count_high)
                    kt_obj_list[cursor_i + 1] = str(boss_count)
                    kt_obj_list[cursor_i + 2] = str(boss_count)
                # else 10 - not parsed

                cursor_i += 3
            kt_obj_list_string = ".".join(kt_obj_list)
            flags_list[kt_obj_code_index] = kt_obj_list_string

            self.options.Flagstring.value = " ".join(flags_list)
            self.options.CharacterCount.value = character_count
            self.options.EsperCount.value = esper_count
            self.options.DragonCount.value = dragon_count
            self.options.BossCount.value = boss_count

            # starting espers
            if self.options.Flagstring.has_flag("-stesp"):
                # initialize -sen flag to indicate specific espers
                sen_flag = ""
                stesp_str = self.options.Flagstring.get_flag("-stesp")
                stesp_err_msg = f"invalid -stesp flag {stesp_str}"
                stesp_list = stesp_str.split(" ")
                if len(stesp_list) != 2:
                    raise ValueError(stesp_err_msg)
                stesp_min_str, stesp_max_str = stesp_list
                try:
                    stesp_min = int(stesp_min_str)
                    stesp_max = int(stesp_max_str)
                except ValueError as e:
                    raise ValueError(stesp_err_msg) from e
                if stesp_min > 0 or stesp_max > 0:
                    # pick a random number of starting espers between min & max specified
                    num_start_espers = self.random.randint(stesp_min, stesp_max)
                    chosen_esper_indexes = self.random.sample(range(len(Rom.espers)), num_start_espers)
                    # update the -sen flag to include a list of chosen esper numbers
                    sen_flag = ",".join([str(id_) for id_ in chosen_esper_indexes])
                    # populate list of starting espers
                    self.starting_espers = [Rom.espers[i] for i in chosen_esper_indexes]
                    # Now, replace -stesp min max flags with -sen x,y,z,etc
                    self.options.Flagstring.replace_flag("-stesp", "-sen", sen_flag)

        else:
            self.starting_characters = resolve_character_options(self.options, self.random)

    @override
    def create_regions(self):
        menu = Region("Menu", self.player, self.multiworld)
        world_map = Region("World Map", self.player, self.multiworld)
        final_dungeon = Region("Kefka's Tower", self.player, self.multiworld)

        for name, id in self.location_name_to_id.items():
            if self.options.Treasuresanity.value == 0:
                if name in Locations.all_minor_checks:
                    continue
            if name in Locations.dragon_events:
                id = None
            if "(Boss)" in name:
                id = None
            if name in Locations.kefka_checks:
                final_dungeon.locations.append(self.create_location(name, id, final_dungeon))
            elif name in Locations.accomplishment_data:
                final_dungeon.locations.append(self.create_location(name, None, final_dungeon))
            else:
                world_map.locations.append(self.create_location(name, id, world_map))

        menu.connect(world_map)
        world_map.connect(final_dungeon)
        final_dungeon.connect(world_map)

        self.multiworld.regions.append(menu)
        self.multiworld.regions.append(world_map)
        self.multiworld.regions.append(final_dungeon)

    @override
    def create_items(self) -> None:
        item_pool: list[FF6WCItem] = []
        assert self.starting_characters
        for item in map(self.create_item, self.item_name_to_id):
            if item.name in self.starting_characters:
                self.multiworld.push_precollected(item)
            # if this is a starting esper
            elif item.name in self.starting_espers:
                # put into the pre-collected list so it is not assigned again
                self.multiworld.push_precollected(item)
            elif item.name in Rom.characters or item.name in Rom.espers:
                item_pool.append(item)

        for index, dragon in enumerate(Locations.dragons):
            dragon_event = Locations.dragon_events_link[dragon]
            self.get_location(dragon_event).place_locked_item(
                self.create_event(self.all_dragon_clears[index]))

        for boss in [location for location in Locations.major_checks if "(Boss)" in location]:
            self.get_location(boss).place_locked_item(self.create_event("Busted!"))

        self.get_location("Kefka's Tower").place_locked_item(
            self.create_event("Kefka's Tower Access"))
        self.get_location("Beat Final Kefka").place_locked_item(
            self.create_event("Victory"))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

        self.item_rewards = get_item_rewards(self.options)

        # update the non-reward items to be everything that's not in item_rewards
        self.item_nonrewards = [item for item in Items.items if item not in self.item_rewards]

        filler_pool: list[str] = []
        # Each filler item has a chest item tier weight
        filler_pool_weights: list[int] = []
        good_filler_pool: list[str] = []

        for item in Items.items:
            # Skips adding an item to filler_pool and good_filler_pool if item restrictions are in place
            if self.options.no_paladin_shields() and (item == "Paladin Shld" or item == "Cursed Shld"):
                continue
            if self.options.no_exp_eggs() and item == "Exp. Egg":
                continue
            if self.options.no_illuminas() and item == "Illumina":
                continue
            # if -noshoes No SprintShoes specified, remove from list
            if self.options.no_shoes() and item == "Sprint Shoes":
                continue
            # if -nmc No MoogleCharms specified, remove from list
            if self.options.no_moogle_charm() and item == "Moogle Charm":
                continue
            if item != "ArchplgoItem":
                filler_pool.append(item)
                # Each filler item has a chest item tier weight
                weight = Items.item_name_weight.get(item)
                assert not (weight is None)
                filler_pool_weights.append(weight)
            # update to use self.item_rewards as calculated above
            if item in self.item_rewards:
                good_filler_pool.append(item)

        major_items = len([location for location in Locations.major_checks if "(Boss)" not in location and "Status"
                           not in location])
        progression_items = len(item_pool)
        major_items = major_items - progression_items
        for _ in range(major_items):
            item_pool.append(self.create_good_filler_item(self.random.choice(good_filler_pool)))
        if self.options.Treasuresanity.value:
            minor_items = len(Locations.all_minor_checks)
            for _ in range(minor_items):
                # random filler item, but use chest item tier weights
                item_pool.append(self.create_filler_item(
                    self.random.choices(filler_pool, filler_pool_weights)[0]
                ))
        self.multiworld.itempool += item_pool

    @override
    def set_rules(self):
        check_list = {
            "Terra": (Locations.major_terra_checks, Locations.minor_terra_checks, Locations.minor_terra_ext_checks),
            "Locke": (Locations.major_locke_checks, Locations.minor_locke_checks, Locations.minor_locke_ext_checks),
            "Cyan": (Locations.major_cyan_checks, Locations.minor_cyan_checks, Locations.minor_cyan_ext_checks),
            "Shadow": (Locations.major_shadow_checks, Locations.minor_shadow_checks, Locations.minor_shadow_ext_checks),
            "Edgar": (Locations.major_edgar_checks, Locations.minor_edgar_checks, Locations.minor_edgar_ext_checks),
            "Sabin": (Locations.major_sabin_checks, Locations.minor_sabin_checks, Locations.minor_sabin_ext_checks),
            "Celes": (Locations.major_celes_checks, Locations.minor_celes_checks, Locations.minor_celes_ext_checks),
            "Strago": (Locations.major_strago_checks, Locations.minor_strago_checks, Locations.minor_strago_ext_checks),
            "Relm": (Locations.major_relm_checks, Locations.minor_relm_checks, Locations.minor_relm_ext_checks),
            "Setzer": (Locations.major_setzer_checks, Locations.minor_setzer_checks, Locations.minor_setzer_ext_checks),
            "Mog": (Locations.major_mog_checks, Locations.minor_mog_checks, Locations.minor_mog_ext_checks),
            "Gau": (Locations.major_gau_checks, Locations.minor_gau_checks, Locations.minor_gau_ext_checks),
            "Gogo": (Locations.major_gogo_checks, Locations.minor_gogo_checks, Locations.minor_gogo_ext_checks),
            "Umaro": (Locations.major_umaro_checks, Locations.minor_umaro_checks, Locations.minor_umaro_ext_checks),
        }

        treasuresanity = self.options.Treasuresanity.value != Treasuresanity.option_off

        # Set every character locked check to require that character.
        for check_name, checks in check_list.items():
            # Major checks. These are always on.
            for check in checks[0]:
                set_rule(self.get_location(check),
                         lambda state, character=check_name: state.has(character, self.player))
            # Minor checks. These are only on if Treasuresanity is on.
            if treasuresanity:
                for check in checks[1]:
                    set_rule(self.get_location(check),
                             lambda state, character=check_name: state.has(character, self.player))
            # Minor extended gating checks. These are on if Treasuresanity are on, but can be character gated.
            if self.options.Treasuresanity.value == 2:
                for check in checks[2]:
                    set_rule(self.get_location(check),
                             lambda state, character=check_name: state.has(character, self.player))

        # Lock (ha!) these behind Terra as well as Locke, since whatever isn't chosen is put behind Whelk
        for check_name in ["Narshe Weapon Shop 1", "Narshe Weapon Shop 2"]:
            add_rule(self.get_location(check_name),
                     lambda state: state.has("Terra", self.player))

        # This rule was causing generation failures. (And I don't see a good reason for it to exist.)
        # for check in Locations.major_checks:
        #     add_item_rule(self.get_location(check),
        #                   # add things that are NOT in the non-rewards list
        #                   # or something for another player (based on their settings)
        #                   lambda item: item.name not in self.item_nonrewards or item.player != self.player)

        for check in Locations.item_only_checks:
            if treasuresanity or (
                check not in Locations.minor_checks and check not in Locations.minor_ext_checks
            ):
                add_item_rule(self.get_location(check),
                              lambda item: (item.name not in self.item_name_groups["characters"]
                                            and item.name not in self.item_name_groups['espers']
                                            or item.player != self.player))

        for check in Locations.no_character_checks:
            add_item_rule(self.get_location(check),
                          lambda item: (item.name not in self.item_name_groups["characters"]
                                        or item.player != self.player))

        for dragon in Locations.dragons:
            dragon_event = Locations.dragon_events_link[dragon]
            add_rule(self.get_location(dragon_event),
                     lambda state: state.can_reach(str(dragon), 'Location', self.player))

        for location in Locations.fanatics_tower_checks:
            if treasuresanity or location not in Locations.all_minor_checks:
                add_rule(self.get_location(location),
                         lambda state: state.has_group("espers", self.player, 4))

        # TODO: This might be better on the region entrance to final dungeon
        kefka_tower = itertools.chain(
            Locations.major_kefka_checks,
            Locations.minor_kefka_checks if treasuresanity else ()
        )
        for location_name in kefka_tower:
            # TODO: maybe this should be has_group_unique
            # I don't know what happens if you get more than 1 of a character
            add_rule(self.get_location(location_name),
                     lambda state: state.has_group("characters", self.player, 3))

        two_players_required = itertools.chain(
            Locations.phoenix_cave_major_checks,
            Locations.phoenix_cave_minor_ext_checks if treasuresanity else (),
            ("Kefka at Narshe", "Kefka at Narshe (Boss)")
        )
        for location_name in two_players_required:
            # TODO: maybe this should be has_group_unique
            # I don't know what happens if you get more than 1 of a character
            add_rule(self.get_location(location_name),
                     lambda state: state.has_group("characters", self.player, 2))

        set_rule(self.get_location("Beat Final Kefka"),
                 functools.partial(can_beat_final_kefka, self.options, self.player))

        assert not (self.starting_characters is None), "need starting characters from generate_early"
        # TODO: move this generate_flagstring earlier if we can verify that options aren't changed
        self.flagstring = generate_flagstring(self.options, self.starting_characters)

    @override
    def post_fill(self) -> None:
        spheres = list(self.multiworld.get_spheres())
        sphere_count = len(spheres)
        upgrade_base = sphere_count * 2
        for current_sphere_count, sphere in enumerate(spheres):
            for location in sphere:
                if location.item and location.item.player == self.player:
                    if self.random.randint(0, upgrade_base) < current_sphere_count:
                        self.upgrade_item(location.item)

        if self.options.Treasuresanity.value != Treasuresanity.option_off:
            wc_event_locations = [
                loc
                for loc in self.multiworld.get_locations(self.player)
                if loc.name in Locations.checks_that_need_dialog_for_items
            ]
            limit_event_items(wc_event_locations, self.random)

    def upgrade_item(self, item: Item):
        if item.name in self.item_nonrewards:
            # Prevents upgrades to restricted items based on flags or AllowStrongestItems value
            nfps = nee = nil = 1
            temp_new_item = ""
            while (nfps or nee or nil) == 1:
                temp_new_item = self.random.choice(self.item_rewards)
                if self.options.no_paladin_shields() and (temp_new_item == "Paladin Shld"
                                                          or temp_new_item == "Cursed Shld"):
                    nfps = 1
                else:
                    nfps = 0
                if self.options.no_exp_eggs() and temp_new_item == "Exp. Egg":
                    nee = 1
                else:
                    nee = 0
                if self.options.no_illuminas() and temp_new_item == "Illumina":
                    nil = 1
                else:
                    nil = 0
            assert temp_new_item
            # if Ragnarok, translate into sword for item_name_to_id dictionary
            if temp_new_item == "Ragnarok":
                temp_new_item = "Ragnarok Sword"
            new_item = temp_new_item
            new_item_id = self.item_name_to_id[new_item]
            item.name = new_item
            item.code = new_item_id
            item.classification = ItemClassification.useful
        return

    @override
    def generate_output(self, output_directory: str):
        locations: dict[str, str] = dict()
        # get all locations
        for location in self.multiworld.get_locations(self.player):
            assert location.item
            if location.name in Locations.minor_checks:
                location_name = Rom.treasure_chest_data[location.name][2]
            elif location.name in Locations.minor_ext_checks:
                location_name = Rom.treasure_chest_data[location.name][2]
            else:
                location_name = location.name
            location_name = str(location_name)  # dict needs str keys
            locations[location_name] = "Archipelago Item"
            if location.item.player == self.player:
                if location_name in Locations.major_checks or location.item.name in Items.items:
                    locations[location_name] = location.item.name
        rom_name_text = f'6WC{Utils.__version__.replace(".", "")[0:3]}_{self.player}_{self.multiworld.seed:11}'
        rom_name_text = rom_name_text[:20]
        self.rom_name = bytearray(rom_name_text, 'utf-8')
        self.rom_name.extend([0] * (20 - len(self.rom_name)))
        self.rom_name_available_event.set()
        locations["RomName"] = rom_name_text

        assert not (self.flagstring is None), "need flagstring from earlier generation step"
        if self.options.Treasuresanity.value != Treasuresanity.option_off:
            wc_event_locations = [
                loc
                for loc in self.multiworld.get_locations(self.player)
                if loc.name in Locations.checks_that_need_dialog_for_items
            ]
            ir_flag = build_ir_from_placements(wc_event_locations)
            try:
                ir_index = self.flagstring.index("-ir")
            except ValueError:
                ir_index = -1
            if ir_index == -1:
                self.flagstring.extend(ir_flag)
            else:
                self.flagstring[ir_index:ir_index + 2] = ir_flag
        verify_flagstring(self.flagstring)
        gen_data = GenData(locations, self.flagstring)
        out_file_base = self.multiworld.get_out_file_name_base(self.player)
        patch_file_name = os.path.join(output_directory, f"{out_file_base}{FF6WCPatch.patch_file_ending}")
        patch = FF6WCPatch(patch_file_name,
                           player=self.player,
                           player_name=self.multiworld.player_name[self.player],
                           gen_data_str=gen_data.to_json())
        patch.write()

        logging.debug(f"FF6WC player {self.player} finished generate_output")

    @override
    def modify_multidata(self, multidata: dict[str, Any]) -> None:
        import base64
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = self.rom_name
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]
