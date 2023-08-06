import os
import random
import typing
# import math
import threading
import copy

from BaseClasses import Item, Region, Entrance, Location, MultiWorld, Tutorial, ItemClassification
from .Items import CV64Item, item_table, filler_junk_table, non_filler_junk_table, key_table, special_table, \
    sub_weapon_table, pickup_item_discrepancies
from .Locations import CV64Location, all_locations, create_locations, boss_table, base_id
from .Entrances import create_entrances
from .Options import cv64_options
from .Stages import CV64Stage, stage_info, shuffle_stages, vanilla_stage_order, vanilla_stage_exits
from .Names import IName, LName, RName
from ..AutoWorld import WebWorld, World
from .Rom import LocalRom, patch_rom, get_base_rom_path, CV64DeltaPatch, rom_sub_weapon_offsets, \
    rom_looping_music_fade_ins, rom_axe_cross_lower_values


# import math


class CV64Web(WebWorld):
    theme = "stone"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Castlevania 64 randomizer connected to an Archipelago Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Liquid Cat"]
    )

    tutorials = [setup_en]


class CV64World(World):
    """
    Castlevania for the Nintendo 64 is the first 3D game in the franchise. As either whip-wielding Belmont descendant
    Reinhardt Schneider or powerful sorceress Carrie Fernandez, brave many terrifying traps and foes as you make your
    way to Dracula's chamber and stop his rule of terror.
    """
    game: str = "Castlevania 64"
    item_name_groups = {
        "Bomb": {IName.magical_nitro, IName.mandragora},
        "Ingredient": {IName.magical_nitro, IName.mandragora},
    }
    option_definitions = cv64_options
    topology_present = True
    data_version = 0
    remote_items = False

    item_name_to_id = {name: code + 0xC64000 for name, code in item_table.items()}
    location_name_to_id = {name: data.code + base_id for name, data in all_locations.items()}

    active_stage_list: typing.List[str]
    active_warp_list: typing.List[str]
    active_stage_exits: typing.Dict[str, typing.List]
    total_available_bosses = 0
    required_s2s = 0
    web = CV64Web()

    def __init__(self, world: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(world, player)

    @classmethod
    def stage_assert_generate(cls, world) -> None:
        rom_file = get_base_rom_path()
        if not os.path.exists(rom_file):
            raise FileNotFoundError(rom_file)

    def generate_early(self) -> None:
        # If there are more S1s needed to unlock the whole warp menu than there are S1s in total, force the total S1
        # count to be higher than the former by a random amount.
        if self.multiworld.special1s_per_warp[self.player].value * 7 > \
                self.multiworld.total_special1s[self.player].value:
            self.multiworld.total_special1s[self.player].value = \
                self.multiworld.random.randint(self.multiworld.special1s_per_warp[self.player].value * 7, 70)

        # If there are more S2s needed to unlock Dracula's chamber than there are S2s in total, force the total S2
        # count to be higher than the former by a random amount.
        if self.multiworld.special2s_required[self.player].value > \
                self.multiworld.total_special2s[self.player].value:
            self.multiworld.total_special2s[self.player].value = \
                self.multiworld.random.randint(self.multiworld.special2s_required[self.player].value, 70)

        self.active_stage_list = vanilla_stage_order.copy()
        self.active_stage_exits = copy.deepcopy(vanilla_stage_exits)

        stage_1_blacklist = []

        # Prevent Clock Tower from being Stage 1 if more than 4 S1s are needed to warp out of it.
        if self.multiworld.special1s_per_warp[self.player].value > 4 and \
                self.multiworld.multi_hit_breakables[self.player].value == 0:
            stage_1_blacklist.append(RName.clock_tower)

        # Remove character stages from the stage list and exits dict if they're not enabled
        if self.multiworld.character_stages[self.player].value == 2:
            self.active_stage_list.remove(RName.underground_waterway)
            self.active_stage_list.remove(RName.tower_of_science)
            self.active_stage_list.remove(RName.tower_of_sorcery)
            del (self.active_stage_exits[RName.underground_waterway])
            del (self.active_stage_exits[RName.tower_of_science])
            del (self.active_stage_exits[RName.tower_of_sorcery])
            self.active_stage_exits[RName.villa][2] = RName.tunnel
            self.active_stage_exits[RName.castle_center][2] = RName.duel_tower
        elif self.multiworld.character_stages[self.player].value == 3:
            self.active_stage_list.remove(RName.tunnel)
            self.active_stage_list.remove(RName.duel_tower)
            self.active_stage_list.remove(RName.tower_of_execution)
            del (self.active_stage_exits[RName.tunnel])
            del (self.active_stage_exits[RName.duel_tower])
            del (self.active_stage_exits[RName.tower_of_execution])
            self.active_stage_exits[RName.villa][1] = RName.underground_waterway
            self.active_stage_exits[RName.castle_center][1] = RName.tower_of_science

        if self.multiworld.stage_shuffle[self.player]:
            shuffle_stages(self.multiworld, self.player, self.active_stage_list, self.active_stage_exits,
                           stage_1_blacklist)
        elif self.multiworld.character_stages[self.player].value != 0:
            # Update the stage numbers here if we have branching paths disabled and not shuffling stages.
            for i in range(len(self.active_stage_list)):
                self.active_stage_exits[self.active_stage_list[i]][3] = i + 1

        # Create a list of warps from the active stage list. They are in a random order by default and will never
        # include the starting stage.
        possible_warps = self.active_stage_list.copy()
        del (possible_warps[0])
        self.active_warp_list = self.multiworld.random.sample(possible_warps, 7)

        if self.multiworld.warp_shuffle[self.player].value == 0:
            # Arrange the warps to be in the seed's stage order
            new_list = self.active_stage_list.copy()
            for warp in self.active_stage_list:
                if warp not in self.active_warp_list:
                    new_list.remove(warp)
            self.active_warp_list = new_list
        elif self.multiworld.warp_shuffle[self.player].value == 2:
            # Arrange the warps to be in the vanilla game's stage order
            new_list = vanilla_stage_order.copy()
            for warp in vanilla_stage_order:
                if warp not in self.active_warp_list:
                    new_list.remove(warp)
            self.active_warp_list = new_list

        # Insert the starting stage at the start of the warp list
        self.active_warp_list.insert(0, self.active_stage_list[0])

    def create_regions(self) -> None:
        active_regions = {"Menu": Region("Menu", self.player, self.multiworld)}
        for i in range(1, len(self.active_warp_list)):
            active_regions[f"Warp {i}"] = Region(f"Warp {i}", self.player, self.multiworld)

        for name, stage in RName.regions_to_stages.items():
            if stage in self.active_stage_list or stage is None:
                active_regions[name] = Region(name, self.player, self.multiworld)

        if not self.multiworld.shopsanity[self.player]:
            del(active_regions[RName.renon])

        create_locations(self.multiworld, self.player, active_regions)

        create_entrances(self.multiworld, self.player, self.active_stage_exits, self.active_warp_list, active_regions)

        # Set up the regions correctly
        for region in active_regions:
            self.multiworld.regions.append(active_regions[region])

    def create_item(self, name: str, force_non_progression=False) -> Item:
        if force_non_progression:
            classification = ItemClassification.filler
        elif name in key_table:
            classification = ItemClassification.progression
        elif name in special_table:
            classification = ItemClassification.progression_skip_balancing
        else:
            classification = ItemClassification.filler

        if name in item_table:
            code = item_table[name]
        else:
            code = None
            classification = ItemClassification.progression

        created_item = CV64Item(name, classification, code, self.player)

        return created_item

    def create_items(self) -> None:
        item_counts = {
            "filler_junk_counts": {name: 0 for name in filler_junk_table.keys()},
            "non_filler_junk_counts": {name: 0 for name in non_filler_junk_table.keys()},
            "key_counts": {name: 0 for name in key_table.keys()},
            "special_counts": {name: 0 for name in special_table.keys()},
        }
        extras_count = 0

        def add_filler_junk(number_to_add):
            for index in range(number_to_add):
                item_to_add = self.get_filler_item_name()
                if item_to_add not in item_counts["filler_junk_counts"]:
                    item_counts["filler_junk_counts"][item_to_add] = 0
                item_counts["filler_junk_counts"][item_to_add] += 1

        def add_items(amounts_dict, counts_to_add_on_to):
            for item_name in amounts_dict:
                if item_name not in item_counts[counts_to_add_on_to]:
                    item_counts[counts_to_add_on_to][item_name] = 0
                item_counts[counts_to_add_on_to][item_name] += amounts_dict[item_name]

        # Add up all the item counts per stage
        for stage in self.active_stage_list:
            add_items(stage_info[stage].stage_key_counts, "key_counts")
            add_items(stage_info[stage].stage_non_filler_junk_counts, "non_filler_junk_counts")
            add_filler_junk(stage_info[stage].stage_filler_junk_count)

            # If 3HBs are on, add those items too
            if self.multiworld.multi_hit_breakables[self.player]:
                add_items(stage_info[stage].multihit_non_filler_junk_counts, "non_filler_junk_counts")
                add_filler_junk(stage_info[stage].multihit_filler_junk_count)

            # If sub-weapons are shuffled in the main pool, add those in too
            if self.multiworld.sub_weapon_shuffle[self.player].value > 1:
                add_items(stage_info[stage].sub_weapon_counts, "non_filler_junk_counts")

            # If both 3HBs are on AND sub-weapons are shuffled in the main pool...yeah
            if self.multiworld.multi_hit_breakables[self.player] and \
                    self.multiworld.sub_weapon_shuffle[self.player].value > 1:
                add_items(stage_info[stage].multihit_sub_weapon_counts, "non_filler_junk_counts")

        # Put in the Carrie-only items if applicable
        if self.multiworld.carrie_logic[self.player] and RName.underground_waterway in self.active_stage_list:
            item_counts["non_filler_junk_counts"][IName.roast_beef] += 1
            item_counts["non_filler_junk_counts"][IName.moon_card] += 1

        # Put in empty breakable items if applicable
        if self.multiworld.empty_breakables[self.player]:
            if RName.forest_of_silence in self.active_stage_list:
                add_filler_junk(6)
            if RName.villa in self.active_stage_list:
                add_filler_junk(1)
            if RName.room_of_clocks in self.active_stage_list:
                add_filler_junk(2)

        # Put in the lizard-man generator items if applicable
        if self.multiworld.lizard_generator_items[self.player] and RName.castle_center in self.active_stage_list:
            item_counts["non_filler_junk_counts"][IName.powerup] += 1
            item_counts["non_filler_junk_counts"][IName.sun_card] += 1
            add_filler_junk(4)

        # Put in Renon's shop items if applicable
        if self.multiworld.shopsanity[self.player]:
            item_counts["non_filler_junk_counts"][IName.roast_chicken] += 1
            item_counts["non_filler_junk_counts"][IName.roast_beef] += 1
            item_counts["non_filler_junk_counts"][IName.healing_kit] += 1
            item_counts["non_filler_junk_counts"][IName.purifying] += 1
            item_counts["non_filler_junk_counts"][IName.cure_ampoule] += 1
            item_counts["non_filler_junk_counts"][IName.sun_card] += 1
            item_counts["non_filler_junk_counts"][IName.moon_card] += 1

        # Determine the S1 count
        item_counts["special_counts"][IName.special_one] = self.multiworld.total_special1s[self.player].value
        extras_count += item_counts["special_counts"][IName.special_one]

        # Determine the S2 count if applicable
        if self.multiworld.draculas_condition[self.player].value == 3:
            item_counts["special_counts"][IName.special_two] = self.multiworld.total_special2s[self.player].value
            extras_count += item_counts["special_counts"][IName.special_two]

        # Determine the extra key counts if applicable
        if self.multiworld.extra_keys[self.player].value == 1:
            for key in item_counts["key_counts"]:
                extra_copies = item_counts["key_counts"][key]
                item_counts["key_counts"][key] += extra_copies
                extras_count += extra_copies
        elif self.multiworld.extra_keys[self.player].value == 2:
            for key in item_counts["key_counts"]:
                extra_copies = 0
                if item_counts["key_counts"][key] > 0:
                    for i in range(item_counts["key_counts"][key]):
                        extra_copies += self.multiworld.random.randint(0, 1)
                item_counts["key_counts"][key] += extra_copies
                extras_count += extra_copies

        # Subtract from the junk tables the total number of "extra" items we're adding. Tier 1 will be subtracted from
        # first until it runs out, at which point we'll start subtracting from Tier 2.
        total_filler_junk = 0
        total_non_filler_junk = 0
        for junk in item_counts["filler_junk_counts"]:
            total_filler_junk += item_counts["filler_junk_counts"][junk]
        for junk in item_counts["non_filler_junk_counts"]:
            total_non_filler_junk += item_counts["non_filler_junk_counts"][junk]

        for i in range(extras_count):
            table = "filler_junk_counts"
            if total_filler_junk > 0:
                total_filler_junk -= 1
            elif total_non_filler_junk > 0:
                table = "non_filler_junk_counts"
                total_non_filler_junk -= 1

            item_to_subtract = self.multiworld.random.choice(list(item_counts[table].keys()))
            while item_counts[table][item_to_subtract] == 0:
                item_to_subtract = self.multiworld.random.choice(list(item_counts[table].keys()))
            item_counts[table][item_to_subtract] -= 1

        # Set up the items correctly
        for table in item_counts:
            for item in item_counts[table]:
                for i in range(item_counts[table][item]):
                    self.multiworld.itempool.append(self.create_item(item))

    def set_rules(self) -> None:
        self.multiworld.get_location(LName.the_end, self.player).place_locked_item(
            CV64Item(IName.victory, ItemClassification.progression, None, self.player))

        if self.multiworld.draculas_condition[self.player].value == 1:
            self.required_s2s = 1
            self.multiworld.get_location(LName.cc_behind_the_seal, self.player).place_locked_item(
                CV64Item(IName.special_two, ItemClassification.progression, None, self.player))
        elif self.multiworld.draculas_condition[self.player].value == 2:
            self.required_s2s = self.multiworld.bosses_required[self.player].value
            for boss_loc in boss_table:
                try:
                    self.multiworld.get_location(boss_loc, self.player).place_locked_item(
                        CV64Item(IName.special_two, ItemClassification.progression, None, self.player))
                except KeyError:
                    continue

            # Verify enough bosses are active in the player's world. If there aren't, the number of required bosses will
            # lower to a random number between 1 and the actual number available.
            for stage in self.active_stage_list:
                self.total_available_bosses += stage_info[stage].boss_count

            if self.multiworld.renon_fight_condition[self.player].value == 0:
                self.total_available_bosses -= 1
            if self.multiworld.vincent_fight_condition[self.player].value == 0:
                self.total_available_bosses -= 1
            if self.required_s2s > self.total_available_bosses:
                self.multiworld.bosses_required[self.player].value = \
                    self.multiworld.random.randint(1, self.total_available_bosses)
                self.required_s2s = self.multiworld.bosses_required[self.player].value
        elif self.multiworld.draculas_condition[self.player].value == 0:
            self.required_s2s = 0

        self.multiworld.completion_condition[self.player] = lambda state: state.has(IName.victory, self.player)
        self.multiworld.get_entrance(RName.ck_drac_chamber, self.player).access_rule = \
            lambda state: state.has(IName.special_two, self.player, self.required_s2s)

    def pre_fill(self) -> None:
        if self.active_stage_list[0] == RName.tower_of_science:
            if self.multiworld.special1s_per_warp[self.player].value > 3:
                self.multiworld.local_early_items[self.player][IName.science_key_two] = 1
        elif self.active_stage_list[0] == RName.clock_tower:
            if (self.multiworld.special1s_per_warp[self.player].value > 2 and
                self.multiworld.multi_hit_breakables[self.player].value == 0) or \
                    (self.multiworld.special1s_per_warp[self.player].value > 8 and
                     self.multiworld.multi_hit_breakables[self.player].value == 1):
                self.multiworld.local_early_items[self.player][IName.clocktower_key_one] = 1
        elif self.active_stage_list[0] == RName.castle_wall:
            if self.multiworld.special1s_per_warp[self.player].value > 5 and \
                    self.multiworld.hard_logic[self.player].value == 0 and \
                    self.multiworld.multi_hit_breakables[self.player].value == 0:
                self.multiworld.local_early_items[self.player][IName.left_tower_key] = 1

    def generate_output(self, output_directory: str) -> None:
        try:
            # Use the world's slot seed for the slot-specific random elements
            random.seed(self.multiworld.per_slot_randoms[self.player])

            # Handle sub-weapon shuffle here.
            sub_weapon_dict = rom_sub_weapon_offsets.copy()

            if self.multiworld.multi_hit_breakables[self.player]:
                sub_weapon_dict[0x10CD65] = 0x0D

            if self.multiworld.sub_weapon_shuffle[self.player].value == 1:
                sub_bytes = list(sub_weapon_dict.values())
                random.shuffle(sub_bytes)
                sub_weapon_dict = dict(zip(sub_weapon_dict, sub_bytes))

            # Handle music shuffle/disable here.
            music_list = [0] * 0x7A
            if self.multiworld.background_music[self.player].value == 2:
                looping_songs = []
                non_looping_songs = []
                fade_in_songs = {}
                # Create shuffle-able lists of all the looping, non-looping, and fade-in track IDs
                for i in range(0x10, len(music_list)):
                    if i not in rom_looping_music_fade_ins.keys() and i not in rom_looping_music_fade_ins.values() and \
                            i != 0x72:  # Credits song is blacklisted
                        non_looping_songs.append(i)
                    elif i in rom_looping_music_fade_ins.keys():
                        looping_songs.append(i)
                    elif i in rom_looping_music_fade_ins.values():
                        fade_in_songs[i] = i
                # Shuffle the looping songs
                rando_looping_songs = looping_songs.copy()
                random.shuffle(rando_looping_songs)
                looping_songs = dict(zip(looping_songs, rando_looping_songs))
                # Shuffle the non-looping songs
                rando_non_looping_songs = non_looping_songs.copy()
                random.shuffle(rando_non_looping_songs)
                non_looping_songs = dict(zip(non_looping_songs, rando_non_looping_songs))
                non_looping_songs[0x72] = 0x72
                # Figure out the new fade-in songs if applicable
                for vanilla_song in looping_songs:
                    if rom_looping_music_fade_ins[vanilla_song]:
                        if rom_looping_music_fade_ins[looping_songs[vanilla_song]]:
                            fade_in_songs[rom_looping_music_fade_ins[vanilla_song]] = rom_looping_music_fade_ins[
                                looping_songs[vanilla_song]]
                        else:
                            fade_in_songs[rom_looping_music_fade_ins[vanilla_song]] = looping_songs[vanilla_song]
                # Build the new music list
                for i in range(0x10, len(music_list)):
                    if i in looping_songs.keys():
                        music_list[i] = looping_songs[i]
                    elif i in non_looping_songs.keys():
                        music_list[i] = non_looping_songs[i]
                    else:
                        music_list[i] = fade_in_songs[i]
            del (music_list[0x00: 0x10])

            offsets_to_ids = {}

            # Handle map lighting rando here.
            if self.multiworld.map_lighting[self.player].value == 1:
                for entry in range(67):
                    for sub_entry in range(19):
                        if sub_entry not in [3, 7, 11, 15] and entry != 4:
                            # The fourth entry in the lighting table affects the lighting on some item pickups; skip it
                            offsets_to_ids[0x1091A0 + (entry * 28) + sub_entry] = \
                                random.randint(0, 255)

            # Handle randomized shop prices here.
            shop_price_list = []
            if self.multiworld.shop_prices[self.player].value == 1:
                min_price = self.multiworld.minimum_gold_price[self.player].value
                max_price = self.multiworld.maximum_gold_price[self.player].value
                if min_price > max_price:
                    min_price = random.randint(0, max_price)

                shop_price_list = [random.randint(min_price * 100, max_price * 100) for i in range(7)]

            world = self.multiworld
            player = self.player

            rom = LocalRom(get_base_rom_path())

            active_locations = self.multiworld.get_locations(self.player)
            countdown_list = [0 for i in range(15)]
            shop_name_list = []
            shop_desc_list = []

            inv_setting = self.multiworld.invisible_items[self.player].value

            for loc in active_locations:
                # If the Location is an event, skip it.
                if loc.address is None:
                    continue

                # Figure out the item ID bytes to put in each Location here.
                if loc.item.player == self.player:
                    if loc.cv64_loc_type not in ["npc", "shop"] and loc.item.name in pickup_item_discrepancies:
                        offsets_to_ids[loc.cv64_rom_offset] = pickup_item_discrepancies[loc.item.name]
                    else:
                        offsets_to_ids[loc.cv64_rom_offset] = item_table[loc.item.name]
                else:
                    if loc.item.advancement:
                        offsets_to_ids[loc.cv64_rom_offset] = 0x11  # Wooden stakes are majors
                    else:
                        offsets_to_ids[loc.cv64_rom_offset] = 0x12  # Roses are minors

                    # If it's another CV64 player's item, change the multiworld item's model to match what it is.
                    if loc.item.game == "Castlevania 64" and loc.cv64_loc_type != "npc":
                        offsets_to_ids[loc.cv64_rom_offset - 1] = item_table[loc.item.name]

                # Apply the invisibility variable depending on the "invisible items" setting.
                if (inv_setting == 1 and loc.cv64_loc_type == "inv") or \
                        (inv_setting == 2 and loc.cv64_loc_type not in ["npc", "shop"]):
                    offsets_to_ids[loc.cv64_rom_offset - 1] = 0xC0
                elif inv_setting == 3 and loc.cv64_loc_type not in ["npc", "shop"]:
                    invisible = random.randint(0, 1)
                    if invisible:
                        offsets_to_ids[loc.cv64_rom_offset - 1] = 0xC0

                # If it's an Axe or Cross in a higher freestanding location, lower it into grab range.
                # KCEK made these spawn 3.2 units higher for some reason.
                if loc.address in rom_axe_cross_lower_values and loc.item.code in [0xC6400F, 0xC64010]:
                    offsets_to_ids[rom_axe_cross_lower_values[loc.address][0]] = \
                        rom_axe_cross_lower_values[loc.address][1]

                # Figure out the list of shop names and descriptions here.
                if loc.parent_region.name == RName.renon:

                    shop_name = loc.item.name
                    if len(shop_name) > 18:
                        shop_name = shop_name[0:18]
                    shop_name_list.append(shop_name)

                    if loc.item.player == self.player:
                        shop_desc_list.append([item_table[loc.item.name], None])
                    elif loc.item.game == "Castlevania 64":
                        shop_desc_list.append([item_table[loc.item.name],
                                               self.multiworld.get_player_name(loc.item.player)])
                    else:
                        if loc.item.advancement:
                            shop_desc_list.append(["prog", self.multiworld.get_player_name(loc.item.player)])
                        elif loc.item.classification == ItemClassification.useful:
                            shop_desc_list.append(["useful", self.multiworld.get_player_name(loc.item.player)])
                        elif loc.item.classification == ItemClassification.trap:
                            shop_desc_list.append(["trap", self.multiworld.get_player_name(loc.item.player)])
                        else:
                            shop_desc_list.append(["common", self.multiworld.get_player_name(loc.item.player)])

                # Figure out the Countdown numbers here.
                if loc.cv64_stage is not None:
                    if self.multiworld.countdown[self.player].value == 2 or \
                            (self.multiworld.countdown[self.player].value == 1 and loc.item.advancement):
                        if loc.parent_region.name in [RName.villa_maze, RName.villa_crypt]:
                            countdown_list[13] += 1
                        elif loc.parent_region.name in [RName.cc_upper, RName.cc_library]:
                            countdown_list[14] += 1
                        else:
                            countdown_list[vanilla_stage_order.index(loc.cv64_stage)] += 1

            # Figure out the sub-weapon bytes if shuffling sub-weapons in their own pool.
            if self.multiworld.sub_weapon_shuffle[self.player].value == 1:
                for offset, sub_id in sub_weapon_dict.items():
                    offsets_to_ids[offset] = sub_id

            # Figure out the loading zone bytes
            if self.multiworld.stage_shuffle[self.player]:
                offsets_to_ids[0xB73308] = stage_info[self.active_stage_list[0]].start_map_id
            for stage in self.active_stage_exits:

                # Start loading zones
                if self.active_stage_exits[stage][0] == "Menu":
                    offsets_to_ids[stage_info[stage].startzone_map_offset] = 0xFF
                    offsets_to_ids[stage_info[stage].startzone_spawn_offset] = 0x00
                elif self.active_stage_exits[stage][0]:
                    offsets_to_ids[stage_info[stage].startzone_map_offset] = stage_info[
                        self.active_stage_exits[stage][0]].end_map_id
                    offsets_to_ids[stage_info[stage].startzone_spawn_offset] = stage_info[
                        self.active_stage_exits[stage][0]].end_spawn_id
                    # Change CC's end-spawn ID to put you at Carrie's exit if appropriate
                    if self.active_stage_exits[stage][0] == RName.castle_center:
                        if self.multiworld.character_stages[self.player].value == 3 or \
                                (self.active_stage_exits[RName.castle_center][2] == stage
                                 and self.multiworld.character_stages[self.player].value == 0):
                            offsets_to_ids[stage_info[stage].startzone_spawn_offset] += 1

                # End loading zones
                if self.active_stage_exits[stage][1]:
                    offsets_to_ids[stage_info[stage].endzone_map_offset] = stage_info[
                        self.active_stage_exits[stage][1]].start_map_id
                    offsets_to_ids[stage_info[stage].endzone_spawn_offset] = stage_info[
                        self.active_stage_exits[stage][1]].start_spawn_id

                # Alternate end loading zones
                if self.active_stage_exits[stage][2]:
                    offsets_to_ids[stage_info[stage].altzone_map_offset] = stage_info[
                        self.active_stage_exits[stage][2]].start_map_id
                    offsets_to_ids[stage_info[stage].altzone_spawn_offset] = stage_info[
                        self.active_stage_exits[stage][2]].start_spawn_id

            patch_rom(self.multiworld, rom, self.player, offsets_to_ids, self.total_available_bosses,
                      self.active_stage_list, self.active_stage_exits, self.active_warp_list, self.required_s2s,
                      music_list, countdown_list, shop_name_list, shop_desc_list, shop_price_list)

            outfilepname = f'_P{player}'
            outfilepname += f"_{world.player_name[player].replace(' ', '_')}" \
                if world.player_name[player] != 'Player%d' % player else ''

            rompath = os.path.join(output_directory, f'AP_{world.seed_name}{outfilepname}.z64')
            rom.write_to_file(rompath)
            self.rom_name = rom.name

            patch = CV64DeltaPatch(os.path.splitext(rompath)[0] + CV64DeltaPatch.patch_file_ending, player=player,
                                   player_name=world.player_name[player], patched_path=rompath)
            patch.write()
        except:
            print("D'oh, something went wrong in CV64's generate_output!")
            raise
        finally:
            if os.path.exists(rompath):
                os.unlink(rompath)
            self.rom_name_available_event.set()  # make sure threading continues and errors are collected

    def write_spoiler(self, spoiler_handle: typing.TextIO) -> None:
        # Write the stage order to the spoiler log
        spoiler_handle.write(f"\nCastlevania 64 stage order for {self.multiworld.player_name[self.player]}:\n")
        used_numbers = []
        for stage in self.active_stage_list:
            num = str(self.active_stage_exits[stage][3]).zfill(2)
            if self.active_stage_exits[stage][3] in used_numbers:
                alt_stage = "'"
            else:
                alt_stage = " "
                used_numbers.append(self.active_stage_exits[stage][3])
            spoiler_handle.writelines(f"Stage {num}{alt_stage}:\t{stage}\n")

        # Write the warp order to the spoiler log
        spoiler_handle.writelines(f"\nStart :\t{self.active_stage_list[0]}\n")
        for i in range(1, len(self.active_warp_list)):
            spoiler_handle.writelines(f"Warp {i}:\t{self.active_warp_list[i]}\n")

    def fill_slot_data(self) -> dict:
        slot_data = {"death_link": self.multiworld.death_link[self.player].value}
        for option_name in cv64_options:
            option = getattr(self.multiworld, option_name)[self.player]
            slot_data[option_name] = option.value

        return slot_data

    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choice(list(filler_junk_table.keys()))
    
    def modify_multidata(self, multidata: dict) -> None:
        import base64
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]
