import os
import typing
# import math
import threading

from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification
from .Items import CV64Item, ItemData, item_table, junk_table
from .Locations import CV64Location, all_locations, setup_locations
from .Options import cv64_options
from .Regions import create_regions, connect_regions
from .Levels import level_list
from .Rules import set_rules
from .Names import ItemName, LocationName
from ..AutoWorld import WebWorld, World
from .Rom import LocalRom, patch_rom, get_base_rom_path, CV64DeltaPatch, rom_item_bytes, rom_sub_weapon_offsets
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
    # hint_blacklist = {}
    remote_items = False

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = all_locations

    active_level_list: typing.List[str]
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
            "active_levels": self.active_level_list,
            "active_warps": self.active_warp_list,
        }

    def generate_early(self):
        self.active_level_list = level_list.copy()
        self.active_warp_list = self.multiworld.random.sample(self.active_level_list, 7)
        self.sub_weapon_dict = rom_sub_weapon_offsets.copy()

        if self.multiworld.stage_shuffle[self.player]:
            self.active_level_list.remove(LocationName.villa)
            self.active_level_list.remove(LocationName.castle_center)
            self.active_level_list.remove(LocationName.castle_keep)
            self.multiworld.random.shuffle(self.active_level_list)
            self.villa_cc_ids = self.multiworld.random.sample(range(0, 6), 2)
            if self.villa_cc_ids[0] < self.villa_cc_ids[1]:
                self.active_level_list.insert(self.villa_cc_ids[0], LocationName.villa)
                self.active_level_list.insert(self.villa_cc_ids[1] + 2, LocationName.castle_center)
            else:
                self.active_level_list.insert(self.villa_cc_ids[1], LocationName.castle_center)
                self.active_level_list.insert(self.villa_cc_ids[0] + 4, LocationName.villa)
            self.active_level_list.append(LocationName.castle_keep)
            # Prevent Clock Tower from being Stage 1 if more than 4 S1s are needed to warp.
            if self.multiworld.special1s_per_warp[self.player].value > 4 and self.active_level_list[0] == LocationName.clock_tower:
                self.active_level_list.remove(LocationName.clock_tower)
                new_ct_slot = self.multiworld.random.randint(1, 11)
                self.active_level_list.insert(new_ct_slot, LocationName.clock_tower)

        if self.multiworld.warp_shuffle[self.player].value == 0:
            new_list = self.active_level_list.copy()
            for warp in self.active_level_list:
                if warp not in self.active_warp_list:
                    new_list.remove(warp)
            self.active_warp_list = new_list
        elif self.multiworld.warp_shuffle[self.player].value == 2:
            new_list = level_list.copy()
            for warp in level_list:
                if warp not in self.active_warp_list:
                    new_list.remove(warp)
            self.active_warp_list = new_list

    def create_regions(self):
        location_table = setup_locations(self.multiworld, self.player)
        create_regions(self.multiworld, self.player, location_table)

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
        if name in rom_item_bytes:
            created_item.item_byte = rom_item_bytes[name]

        return created_item

    def set_rules(self):
        set_rules(self.multiworld, self.player)

    def generate_basic(self):
        itempool: typing.List[CV64Item] = []

        # Levels
        total_required_locations = 211

        self.multiworld.get_location(LocationName.the_end, self.player).place_locked_item(self.create_item(ItemName.victory))

        number_of_s1s = self.multiworld.total_special1s[self.player].value
        number_of_s2s = self.multiworld.total_special2s[self.player].value
        total_available_bosses = 14

        required_s1s = self.multiworld.special1s_per_warp[self.player].value*7

        if required_s1s > number_of_s1s:
            raise Exception(f"Not enough Special1 jewels for player {self.multiworld.get_player_name(self.player)} "
                            f"to use the whole warp menu. Need {required_s1s - number_of_s1s} more.")

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
            itempool += [self.create_item(ItemName.special_two) for _ in range(number_of_s2s)]
            self.required_s2s = self.multiworld.special2s_required[self.player].value
            if self.required_s2s > number_of_s2s:
                raise Exception(f"More Special2 jewels required than there are for player {self.multiworld.get_player_name(self.player)}. "
                                f"Need {self.required_s2s - number_of_s2s} more.")

        extra_keys_dict = {ItemName.left_tower_key: 0, ItemName.storeroom_key: 0, ItemName.archives_key: 0,
                           ItemName.garden_key: 0, ItemName.copper_key: 0, ItemName.chamber_key: 0,
                           ItemName.execution_key: 0, ItemName.science_key_one: 0, ItemName.science_key_two: 0,
                           ItemName.science_key_three: 0, ItemName.clocktower_key_one: 0,
                           ItemName.clocktower_key_two: 0, ItemName.clocktower_key_three: 0, ItemName.magical_nitro: 0,
                           ItemName.mandragora: 0}

        if self.multiworld.extra_keys[self.player].value == 1:
            for item in extra_keys_dict:
                extra_keys_dict[item] = 1
        elif self.multiworld.extra_keys[self.player].value == 2:
            for item in extra_keys_dict:
                extra_count = self.multiworld.random.randint(0, 1)
                extra_keys_dict[item] = extra_count

        itempool += [self.create_item(ItemName.special_one) for _ in range(number_of_s1s)]
        itempool += [self.create_item(ItemName.roast_chicken) for _ in range(21)]
        itempool += [self.create_item(ItemName.roast_beef) for _ in range(24)]
        itempool += [self.create_item(ItemName.healing_kit) for _ in range(4)]
        itempool += [self.create_item(ItemName.purifying) for _ in range(14)]
        itempool += [self.create_item(ItemName.cure_ampoule) for _ in range(5)]
        itempool += [self.create_item(ItemName.powerup) for _ in range(10)]
        itempool += [self.create_item(ItemName.magical_nitro) for _ in range(2 + extra_keys_dict[ItemName.magical_nitro])]
        itempool += [self.create_item(ItemName.mandragora) for _ in range(2 + extra_keys_dict[ItemName.mandragora])]
        itempool += [self.create_item(ItemName.sun_card) for _ in range(9)]
        itempool += [self.create_item(ItemName.moon_card) for _ in range(8)]
        itempool += [self.create_item(ItemName.left_tower_key) for _ in range(1 + extra_keys_dict[ItemName.left_tower_key])]
        itempool += [self.create_item(ItemName.storeroom_key) for _ in range(1 + extra_keys_dict[ItemName.storeroom_key])]
        itempool += [self.create_item(ItemName.archives_key) for _ in range(1 + extra_keys_dict[ItemName.archives_key])]
        itempool += [self.create_item(ItemName.garden_key) for _ in range(1 + extra_keys_dict[ItemName.garden_key])]
        itempool += [self.create_item(ItemName.copper_key) for _ in range(1 + extra_keys_dict[ItemName.copper_key])]
        itempool += [self.create_item(ItemName.chamber_key) for _ in range(1 + extra_keys_dict[ItemName.chamber_key])]
        itempool += [self.create_item(ItemName.execution_key) for _ in range(1 + extra_keys_dict[ItemName.execution_key])]
        itempool += [self.create_item(ItemName.science_key_one) for _ in range(1 + extra_keys_dict[ItemName.science_key_one])]
        itempool += [self.create_item(ItemName.science_key_two) for _ in range(1 + extra_keys_dict[ItemName.science_key_two])]
        itempool += [self.create_item(ItemName.science_key_three) for _ in range(1 + extra_keys_dict[ItemName.science_key_three])]
        itempool += [self.create_item(ItemName.clocktower_key_one) for _ in range(1 + extra_keys_dict[ItemName.clocktower_key_one])]
        itempool += [self.create_item(ItemName.clocktower_key_two) for _ in range(1 + extra_keys_dict[ItemName.clocktower_key_two])]
        itempool += [self.create_item(ItemName.clocktower_key_three) for _ in range(1 + extra_keys_dict[ItemName.clocktower_key_three])]

        if self.multiworld.carrie_logic[self.player]:
            itempool += [self.create_item(ItemName.roast_beef)]
            itempool += [self.create_item(ItemName.moon_card)]
            total_required_locations += 2

        if self.multiworld.lizard_generator_items[self.player]:
            itempool += [self.create_item(ItemName.powerup)]
            itempool += [self.create_item(ItemName.sun_card)]
            total_required_locations += 6

        total_junk_count = total_required_locations - len(itempool)

        junk_pool = []
        for item_name in self.multiworld.random.choices(list(junk_table.keys()), k=total_junk_count):
            junk_pool.append(self.create_item(item_name))

        itempool += junk_pool

        connect_regions(self.multiworld, self.player, self.active_level_list, self.active_warp_list,
                        self.required_s2s)

        self.multiworld.itempool += itempool

        if self.multiworld.sub_weapon_shuffle[self.player]:
            sub_bytes = list(self.sub_weapon_dict.values())
            self.multiworld.random.shuffle(sub_bytes)
            self.sub_weapon_dict = dict(zip(self.sub_weapon_dict, sub_bytes))

    def pre_fill(self):
        if self.active_level_list[0] == LocationName.tower_of_science:
            if self.multiworld.special1s_per_warp[self.player].value > 3:
                self.multiworld.local_early_items[self.player][ItemName.science_key_two] = 1
        elif self.active_level_list[0] == LocationName.clock_tower:
            if self.multiworld.special1s_per_warp[self.player].value > 2:
                self.multiworld.local_early_items[self.player][ItemName.clocktower_key_one] = 1

    def generate_output(self, output_directory: str):
        try:
            world = self.multiworld
            player = self.player

            rom = LocalRom(get_base_rom_path())

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

            offsets_to_ids = {}
            for location_name in active_locations:
                loc = self.multiworld.get_location(location_name, self.player)
                if loc.item.name in rom_item_bytes or loc.item.game != "Castlevania 64":
                    if loc.item.player == self.player:
                        offsets_to_ids[loc.rom_offset] = loc.item.item_byte
                        if loc.loc_type == "npc":
                            if 0x19 < offsets_to_ids[loc.rom_offset] < 0x1D:
                                offsets_to_ids[loc.rom_offset] += 0x0D
                            elif offsets_to_ids[loc.rom_offset] > 0x1C:
                                offsets_to_ids[loc.rom_offset] -= 0x03
                    else:
                        if loc.item.classification == ItemClassification.progression:
                            offsets_to_ids[loc.rom_offset] = 0x11
                        else:
                            offsets_to_ids[loc.rom_offset] = 0x12

            patch_rom(self.multiworld, rom, self.player, offsets_to_ids, self.active_level_list, self.active_warp_list,
                      self.sub_weapon_dict, self.required_s2s)

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
            print("Oh no, something went wrong in CV64's generate_output!")
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
        for x in range(len(self.active_level_list)):
            if self.active_level_list[x - 2] == LocationName.villa or self.active_level_list[x - 3] \
                    == LocationName.castle_center or self.active_level_list[x - 4] == LocationName.castle_center:
                path = "'"
            else:
                path = " "

            if self.active_level_list[x - 2] == LocationName.villa:
                stage_count -= 1
            elif self.active_level_list[x - 3] == LocationName.castle_center:
                stage_count -= 2

            if stage_count < 10:
                text = "Stage {0}{1}:\t{2}\n"
            else:
                text = "Stage {0}:\t{2}\n"
            text = text.format(stage_count, path, self.active_level_list[x])
            spoiler_handle.writelines(text)
            stage_count += 1

        spoiler_handle.writelines("\nStart :\t" + self.active_level_list[0])
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
