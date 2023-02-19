import os
import typing
# import math
import threading

from BaseClasses import Item, Region, Entrance, Location, MultiWorld, Tutorial, ItemClassification
from .Items import CV64Item, ItemData, item_table, junk_table, main_table
from .Locations import CV64Location, all_locations, create_locations
from .Entrances import create_entrances
from .Options import cv64_options
from .Stages import stage_dict, vanilla_stage_order
from .Names import ItemName, LocationName, RegionName
from ..AutoWorld import WebWorld, World
from .Rom import LocalRom, patch_rom, get_base_rom_path, CV64DeltaPatch, rom_sub_weapon_offsets
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

    tutorials = "Insert setup webpage here"


class CV64World(World):
    """
    Castlevania for the Nintendo 64 is the first 3D game in the franchise. As either whip-wielding Belmont descendant
    Reinhardt Schneider or powerful sorceress Carrie Fernandez, brave many terrifying traps and foes as you make your
    way to Dracula's chamber and stop his rule of terror.
    """
    game: str = "Castlevania 64"
    option_definitions = cv64_options
    topology_present = True
    data_version = 0
    remote_items = False

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.code for name, data in all_locations.items()}

    active_stage_list: typing.List[str]
    villa_cc_ids = [2, 3]
    active_warp_list: typing.List[str]
    sub_weapon_dict: typing.Dict[int, int]
    # music_dict: typing.Dict[int, int]
    # TODO: Make a list of every instance of the music changing for music rando.
    required_s2s = 0
    web = CV64Web()

    def __init__(self, world: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(world, player)

    @classmethod
    def stage_assert_generate(cls, world):
        rom_file = get_base_rom_path()
        if not os.path.exists(rom_file):
            raise FileNotFoundError(rom_file)

    def _get_slot_data(self):
        return {
            "death_link": self.multiworld.death_link[self.player].value,
            "active_levels": self.active_stage_list,
            "active_warps": self.active_warp_list,
        }

    def generate_early(self):
        # Handle Stage Shuffle here
        self.active_stage_list = vanilla_stage_order.copy()
        self.active_warp_list = self.multiworld.random.sample(self.active_stage_list, 7)
        self.sub_weapon_dict = rom_sub_weapon_offsets.copy()

        if self.multiworld.stage_shuffle[self.player]:
            self.active_stage_list.remove(RegionName.villa)
            self.active_stage_list.remove(RegionName.castle_center)
            self.active_stage_list.remove(RegionName.castle_keep)
            self.multiworld.random.shuffle(self.active_stage_list)
            self.villa_cc_ids = self.multiworld.random.sample(range(0, 6), 2)
            if self.villa_cc_ids[0] < self.villa_cc_ids[1]:
                self.active_stage_list.insert(self.villa_cc_ids[0], RegionName.villa)
                self.active_stage_list.insert(self.villa_cc_ids[1] + 2, RegionName.castle_center)
            else:
                self.active_stage_list.insert(self.villa_cc_ids[1], RegionName.castle_center)
                self.active_stage_list.insert(self.villa_cc_ids[0] + 4, RegionName.villa)
            self.active_stage_list.append(RegionName.castle_keep)
            # Prevent Clock Tower from being Stage 1 if more than 4 S1s are needed to warp.
            if self.multiworld.special1s_per_warp[self.player].value > 4 and self.active_stage_list[0] == RegionName.clock_tower:
                self.active_stage_list.remove(RegionName.clock_tower)
                new_ct_slot = self.multiworld.random.randint(1, 11)
                self.active_stage_list.insert(new_ct_slot, RegionName.clock_tower)

        # Handle Warp Shuffle here
        if self.multiworld.warp_shuffle[self.player].value == 0:
            new_list = self.active_stage_list.copy()
            for warp in self.active_stage_list:
                if warp not in self.active_warp_list:
                    new_list.remove(warp)
            self.active_warp_list = new_list
        elif self.multiworld.warp_shuffle[self.player].value == 2:
            new_list = stage_dict.keys()
            for warp in stage_dict:
                if warp not in self.active_warp_list:
                    new_list.remove(warp)
            self.active_warp_list = new_list

    def create_regions(self):
        active_regions = {}

        for name, stage in RegionName.regions_to_stages.items():
            if stage in self.active_stage_list or stage is None:
                active_regions[name] = Region(name, None, name, self.player, self.multiworld)

        create_locations(self.multiworld, self.player, active_regions)

        create_entrances(self.multiworld, self.player, self.active_stage_list, self.active_warp_list, self.required_s2s,
                         active_regions)

        # Set up the regions correctly
        for region in active_regions:
            self.multiworld.regions.append(active_regions[region])

    def create_item(self, name: str, force_non_progression=False) -> Item:
        data = item_table[name]

        if force_non_progression:
            classification = ItemClassification.filler
        elif name == ItemName.special_two:
            classification = ItemClassification.progression_skip_balancing
        elif data.progression:
            classification = ItemClassification.progression
        else:
            classification = ItemClassification.filler

        created_item = CV64Item(name, classification, data.code, self.player)
        if self.multiworld.draculas_condition[self.player].value != 3 and created_item.name == ItemName.special_two:
            created_item.code = None

        return created_item

    def create_items(self):
        item_counts = {name: data.quantity for name, data in item_table.items()}

        total_required_locations = 210

        self.multiworld.get_location(LocationName.the_end, self.player).place_locked_item(self.create_item(ItemName.victory))

        item_counts[ItemName.special_one] = self.multiworld.total_special1s[self.player].value
        total_available_bosses = 14

        required_s1s = self.multiworld.special1s_per_warp[self.player].value * 7

        if required_s1s > item_counts[ItemName.special_one]:
            raise Exception(f"Not enough Special1 jewels for player {self.multiworld.get_player_name(self.player)} to "
                            f"use the whole warp menu. Need {required_s1s - item_counts[ItemName.special_one]} more.")

        if self.multiworld.draculas_condition[self.player].value == 1:
            self.required_s2s = 1
            self.multiworld.get_location(LocationName.cc_behind_the_seal, self.player) \
                .place_locked_item(self.create_item(ItemName.special_two))
        elif self.multiworld.draculas_condition[self.player].value == 2:
            self.required_s2s = self.multiworld.bosses_required[self.player].value
            self.multiworld.get_location(LocationName.forest_boss_one, self.player) \
                .place_locked_item(self.create_item(ItemName.special_two))
            self.multiworld.get_location(LocationName.forest_boss_two, self.player) \
                .place_locked_item(self.create_item(ItemName.special_two))
            self.multiworld.get_location(LocationName.forest_boss_three, self.player) \
                .place_locked_item(self.create_item(ItemName.special_two))
            self.multiworld.get_location(LocationName.cw_boss, self.player) \
                .place_locked_item(self.create_item(ItemName.special_two))
            self.multiworld.get_location(LocationName.villa_boss_one, self.player) \
                .place_locked_item(self.create_item(ItemName.special_two))
            self.multiworld.get_location(LocationName.villa_boss_two, self.player) \
                .place_locked_item(self.create_item(ItemName.special_two))
            self.multiworld.get_location(LocationName.uw_boss, self.player) \
                .place_locked_item(self.create_item(ItemName.special_two))
            self.multiworld.get_location(LocationName.cc_boss_one, self.player) \
                .place_locked_item(self.create_item(ItemName.special_two))
            self.multiworld.get_location(LocationName.cc_boss_two, self.player) \
                .place_locked_item(self.create_item(ItemName.special_two))
            self.multiworld.get_location(LocationName.dt_boss_one, self.player) \
                .place_locked_item(self.create_item(ItemName.special_two))
            self.multiworld.get_location(LocationName.dt_boss_two, self.player) \
                .place_locked_item(self.create_item(ItemName.special_two))
            self.multiworld.get_location(LocationName.dt_boss_three, self.player) \
                .place_locked_item(self.create_item(ItemName.special_two))
            self.multiworld.get_location(LocationName.dt_boss_four, self.player) \
                .place_locked_item(self.create_item(ItemName.special_two))
            self.multiworld.get_location(LocationName.roc_boss, self.player) \
                .place_locked_item(self.create_item(ItemName.special_two))
            if self.multiworld.renon_fight_condition[self.player].value != 0:
                self.multiworld.get_location(LocationName.ck_boss_one, self.player) \
                    .place_locked_item(self.create_item(ItemName.special_two))
                total_available_bosses += 1
            if self.multiworld.vincent_fight_condition[self.player].value != 0:
                self.multiworld.get_location(LocationName.ck_boss_two, self.player) \
                    .place_locked_item(self.create_item(ItemName.special_two))
                total_available_bosses += 1
            if self.required_s2s > total_available_bosses:
                raise Exception(f"More bosses required than there are for player {self.multiworld.get_player_name(self.player)}. "
                                f"Need {self.required_s2s - total_available_bosses} more enabled.")
        elif self.multiworld.draculas_condition[self.player].value == 3:
            item_counts[ItemName.special_two] = self.multiworld.total_special2s[self.player].value
            self.required_s2s = self.multiworld.special2s_required[self.player].value
            if self.required_s2s > item_counts[ItemName.special_two]:
                raise Exception(f"More Special2 jewels required than there are for player {self.multiworld.get_player_name(self.player)}. "
                                f"Need {self.required_s2s - item_counts[ItemName.special_two]} more.")

        if self.multiworld.extra_keys[self.player].value == 1:
            for item in item_counts:
                if item_table[item].progression and item in main_table:
                    item_counts[item] += 1
        elif self.multiworld.extra_keys[self.player].value == 2:
            for item in item_counts:
                extra_count = self.multiworld.random.randint(0, 1)
                if item_table[item].progression and item in main_table:
                    item_counts[item] += extra_count

        if self.multiworld.carrie_logic[self.player]:
            item_counts[ItemName.roast_beef] += 1
            item_counts[ItemName.moon_card] += 1
            total_required_locations += 2

        if self.multiworld.lizard_generator_items[self.player]:
            item_counts[ItemName.powerup] += 1
            item_counts[ItemName.sun_card] += 1
            total_required_locations += 6

        total_junk_count = total_required_locations - sum(item_counts.values())
        for junk_item in self.multiworld.random.choices(list(junk_table.keys()), k=total_junk_count):
            item_counts[junk_item] += 1

        itempool: typing.List[CV64Item] = []
        for item in item_counts:
            if item_counts[item] != 0:
                itempool += [self.create_item(item) for _ in range(item_counts[item])]

        self.multiworld.itempool += itempool

        if self.multiworld.sub_weapon_shuffle[self.player]:
            sub_bytes = list(self.sub_weapon_dict.values())
            self.multiworld.random.shuffle(sub_bytes)
            self.sub_weapon_dict = dict(zip(self.sub_weapon_dict, sub_bytes))

    def set_rules(self):
        self.multiworld.completion_condition[self.player] = lambda state: state.has(ItemName.victory, self.player)

    def pre_fill(self):
        if self.active_stage_list[0] == RegionName.tower_of_science:
            if self.multiworld.special1s_per_warp[self.player].value > 3:
                self.multiworld.local_early_items[self.player][ItemName.science_key_two] = 1
        elif self.active_stage_list[0] == RegionName.clock_tower:
            if self.multiworld.special1s_per_warp[self.player].value > 2:
                self.multiworld.local_early_items[self.player][ItemName.clocktower_key_one] = 1

    def get_offsets_and_ids(self):
        offsets_to_ids = {}

        # Items
        active_locations = self.location_name_to_id.copy()

        if not self.multiworld.carrie_logic[self.player]:
            del active_locations[LocationName.uw_carrie1]
            del active_locations[LocationName.uw_carrie2]

        if not self.multiworld.lizard_generator_items[self.player]:
            del active_locations[LocationName.ccff_lizard_coffin_fl]
            del active_locations[LocationName.ccff_lizard_coffin_fr]
            del active_locations[LocationName.ccff_lizard_coffin_nfl]
            del active_locations[LocationName.ccff_lizard_coffin_nfr]
            del active_locations[LocationName.ccff_lizard_coffin_nml]
            del active_locations[LocationName.ccff_lizard_coffin_nmr]
        
        for location_name in active_locations:
            loc = self.multiworld.get_location(location_name, self.player)
            if loc.item.game == "Castlevania 64" and loc.cv64_loc_type != "event":
                if loc.item.player == self.player:
                    offsets_to_ids[loc.cv64_rom_offset] = loc.item.code - 0xC64000
                    if loc.cv64_loc_type == "npc":
                        if 0x19 < offsets_to_ids[loc.cv64_rom_offset] < 0x1D:
                            offsets_to_ids[loc.cv64_rom_offset] += 0x0D
                        elif offsets_to_ids[loc.cv64_rom_offset] > 0x1C:
                            offsets_to_ids[loc.cv64_rom_offset] -= 0x03
                else:
                    if loc.item.classification == ItemClassification.progression:
                        offsets_to_ids[loc.cv64_rom_offset] = 0x11
                    else:
                        offsets_to_ids[loc.cv64_rom_offset] = 0x12

        # Sub-weapons
        if self.multiworld.sub_weapon_shuffle[self.player]:
            for offset, sub_id in self.sub_weapon_dict.items():
                offsets_to_ids[offset] = sub_id

        # Loading zones
        if self.multiworld.stage_shuffle[self.player]:
            offsets_to_ids[0xB73308] = stage_dict[self.active_stage_list[0]].start_map_id
            offsets_to_ids[0xD9DAB] = stage_dict[
                self.active_stage_list[self.active_stage_list.index(RegionName.villa) + 2]].start_map_id
            offsets_to_ids[0x109CCF] = stage_dict[
                self.active_stage_list[self.active_stage_list.index(RegionName.castle_center) + 3]].start_map_id
            for stage in range(len(self.active_stage_list) - 1):
                if self.active_stage_list[stage - 1] == RegionName.villa:
                    offsets_to_ids[stage_dict[self.active_stage_list[stage]].endzone_map_offset] = stage_dict[
                        self.active_stage_list[stage + 2]].start_map_id
                    offsets_to_ids[stage_dict[self.active_stage_list[stage]].endzone_spawn_offset] = stage_dict[
                        self.active_stage_list[stage + 2]].start_spawn_id
                elif self.active_stage_list[stage - 2] == RegionName.castle_center:
                    offsets_to_ids[stage_dict[self.active_stage_list[stage]].endzone_map_offset] = stage_dict[
                        self.active_stage_list[stage + 3]].start_spawn_id
                    offsets_to_ids[stage_dict[self.active_stage_list[stage]].endzone_spawn_offset] = stage_dict[
                        self.active_stage_list[stage + 3]].start_spawn_id
                else:
                    offsets_to_ids[stage_dict[self.active_stage_list[stage]].endzone_map_offset] = stage_dict[
                        self.active_stage_list[stage + 1]].start_map_id
                    offsets_to_ids[stage_dict[self.active_stage_list[stage]].endzone_spawn_offset] = stage_dict[
                        self.active_stage_list[stage + 1]].start_spawn_id

                if stage_dict[self.active_stage_list[stage]].startzone_map_offset != 0xFFFFFF:
                    if stage - 1 < 0:
                        offsets_to_ids[stage_dict[self.active_stage_list[stage]].startzone_map_offset] = stage_dict[
                            self.active_stage_list[stage]].start_map_id
                        offsets_to_ids[stage_dict[self.active_stage_list[stage]].startzone_spawn_offset] = \
                            stage_dict[self.active_stage_list[stage]].start_spawn_id
                    elif self.active_stage_list[stage - 2] == RegionName.villa:
                        offsets_to_ids[stage_dict[self.active_stage_list[stage]].startzone_map_offset] = 0x1A
                        offsets_to_ids[stage_dict[self.active_stage_list[stage]].startzone_spawn_offset] = 0x03
                    elif self.active_stage_list[stage - 3] == RegionName.villa:
                        offsets_to_ids[stage_dict[self.active_stage_list[stage]].startzone_map_offset] = stage_dict[
                            self.active_stage_list[stage - 2]].end_map_id
                        offsets_to_ids[stage_dict[self.active_stage_list[stage]].startzone_spawn_offset] = \
                            stage_dict[self.active_stage_list[stage - 2]].end_spawn_id
                    elif self.active_stage_list[stage - 3] == RegionName.castle_center:
                        offsets_to_ids[stage_dict[self.active_stage_list[stage]].startzone_map_offset] = 0x0F
                        offsets_to_ids[stage_dict[self.active_stage_list[stage]].startzone_spawn_offset] = 0x03
                    elif self.active_stage_list[stage - 5] == RegionName.castle_center:
                        offsets_to_ids[stage_dict[self.active_stage_list[stage]].startzone_map_offset] = stage_dict[
                            self.active_stage_list[stage - 3]].end_map_id
                        offsets_to_ids[stage_dict[self.active_stage_list[stage]].startzone_spawn_offset] = \
                            stage_dict[self.active_stage_list[stage - 3]].end_spawn_id
                    else:
                        offsets_to_ids[stage_dict[self.active_stage_list[stage]].startzone_map_offset] = stage_dict[
                            self.active_stage_list[stage - 1]].end_map_id
                        offsets_to_ids[stage_dict[self.active_stage_list[stage]].startzone_spawn_offset] = \
                            stage_dict[self.active_stage_list[stage - 1]].end_spawn_id

        return offsets_to_ids
    
    def generate_output(self, output_directory: str):
        try:
            world = self.multiworld
            player = self.player

            rom = LocalRom(get_base_rom_path())

            offsets_to_ids = self.get_offsets_and_ids()

            patch_rom(self.multiworld, rom, self.player, offsets_to_ids, self.active_stage_list, self.active_warp_list,
                      self.required_s2s)

            outfilepname = f'_P{player}'
            outfilepname += f"_{world.player_name[player].replace(' ', '_')}" \
                if world.player_name[player] != 'Player%d' % player else ''

            rompath = os.path.join(output_directory, f'AP_{world.seed_name}{outfilepname}.z64')
            rom.write_to_file(rompath)
            self.rom_name = rom.name

            patch = CV64DeltaPatch(os.path.splitext(rompath)[0]+CV64DeltaPatch.patch_file_ending, player=player,
                                   player_name=world.player_name[player], patched_path=rompath)
            patch.write()
        except:
            print("D'oh, something went wrong in CV64's generate_output!")
            raise
        finally:
            if os.path.exists(rompath):
                os.unlink(rompath)
            self.rom_name_available_event.set()  # make sure threading continues and errors are collected

    def write_spoiler(self, spoiler_handle: typing.TextIO):
        stage_count = 1
        spoiler_handle.write("\n")
        header_text = "Castlevania 64 stage order:\n"
        header_text = header_text.format(self.multiworld.player_name[self.player])
        spoiler_handle.write(header_text)
        for x in range(len(self.active_stage_list)):
            if self.active_stage_list[x - 2] == RegionName.villa or self.active_stage_list[x - 3] \
                    == RegionName.castle_center or self.active_stage_list[x - 4] == RegionName.castle_center:
                path = "'"
            else:
                path = " "

            if self.active_stage_list[x - 2] == RegionName.villa:
                stage_count -= 1
            elif self.active_stage_list[x - 3] == RegionName.castle_center:
                stage_count -= 2

            if stage_count < 10:
                text = "Stage {0}{1}:\t{2}\n"
            else:
                text = "Stage {0}:\t{2}\n"
            text = text.format(stage_count, path, self.active_stage_list[x])
            spoiler_handle.writelines(text)
            stage_count += 1

        spoiler_handle.writelines("\nStart :\t" + self.active_stage_list[0])
        for x in range(len(self.active_warp_list)):
            text = "\nWarp {0}:\t{1}"
            text = text.format(x + 1, self.active_warp_list[x])
            spoiler_handle.writelines(text)

    def fill_slot_data(self) -> dict:
        slot_data = self._get_slot_data()
        for option_name in cv64_options:
            option = getattr(self.multiworld, option_name)[self.player]
            slot_data[option_name] = option.value

        return slot_data

    def modify_multidata(self, multidata: dict):
        import base64
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]
