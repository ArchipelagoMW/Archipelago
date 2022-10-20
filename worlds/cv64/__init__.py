import os
import typing
# import math
import threading

from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification
from .Items import CV64Item, ItemData, item_table, junk_table
from .Locations import CV64Location, all_locations, setup_locations
from .Options import cv64_options
from .Regions import create_regions, connect_regions
from .Levels import char_level_list
from .Rules import set_rules
from .Names import ItemName, LocationName
from ..AutoWorld import WebWorld, World
from .Rom import LocalRom, patch_rom, get_base_rom_path, CV64DeltaPatch, rom_item_bytes
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
    topology_present = False
    data_version = 0
    # hint_blacklist = {}
    remote_items = False

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = all_locations

    active_level_list: typing.List[str]
    villa_cc_ids = [2, 3]
    warp_level_list: typing.List[str]
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
            "death_link": self.world.death_link[self.player].value,
            "active_levels": self.active_level_list,
        }

    def create_regions(self):
        location_table = setup_locations(self.world, self.player)
        create_regions(self.world, self.player, location_table)

    def create_item(self, name: str, force_non_progression=False) -> Item:
        data = item_table[name]

        if force_non_progression:
            classification = ItemClassification.filler
        elif data.progression:
            classification = ItemClassification.progression
        else:
            classification = ItemClassification.filler

        created_item = CV64Item(name, classification, data.code, self.player)
        if name in rom_item_bytes:
            created_item.item_byte = rom_item_bytes[name]

        return created_item

    def lookup_table(self):
        pass

    def _create_items(self, name: str):
        data = item_table[name]
        return [self.create_item(name)] * data.quantity

    def set_rules(self):
        set_rules(self.world, self.player)

    def generate_basic(self):
        itempool: typing.List[CV64Item] = []

        # Levels
        total_required_locations = 212

        # number_of_specials = 0
        self.world.get_location(LocationName.the_end, self.player).place_locked_item(self.create_item(ItemName.victory))

        self.world.get_location(LocationName.forest_boss_one, self.player)\
            .place_locked_item(self.create_item(ItemName.bone_mom_one))
        self.world.get_location(LocationName.forest_boss_two, self.player)\
            .place_locked_item(self.create_item(ItemName.forest_weretiger))
        self.world.get_location(LocationName.forest_boss_three, self.player)\
            .place_locked_item(self.create_item(ItemName.bone_mom_two))
        self.world.get_location(LocationName.cw_boss, self.player)\
            .place_locked_item(self.create_item(ItemName.w_dragons))
        self.world.get_location(LocationName.villa_boss, self.player)\
            .place_locked_item(self.create_item(ItemName.vamp_couple))
        self.world.get_location(LocationName.cc_boss_one, self.player)\
            .place_locked_item(self.create_item(ItemName.behemoth))
        self.world.get_location(LocationName.cc_boss_two, self.player)\
            .place_locked_item(self.create_item(ItemName.rosamilla))
        self.world.get_location(LocationName.dt_boss_one, self.player)\
            .place_locked_item(self.create_item(ItemName.werejaguar))
        self.world.get_location(LocationName.dt_boss_two, self.player)\
            .place_locked_item(self.create_item(ItemName.werewolf))
        self.world.get_location(LocationName.dt_boss_three, self.player)\
            .place_locked_item(self.create_item(ItemName.werebull))
        self.world.get_location(LocationName.dt_boss_four, self.player)\
            .place_locked_item(self.create_item(ItemName.weretiger))
        self.world.get_location(LocationName.roc_boss, self.player)\
            .place_locked_item(self.create_item(ItemName.deathtrice))

        itempool += [self.create_item(ItemName.special_one)] * self.world.total_special1s[self.player].value
        itempool += [self.create_item(ItemName.roast_chicken)] * 21
        itempool += [self.create_item(ItemName.roast_beef)] * 24
        itempool += [self.create_item(ItemName.healing_kit)] * 4
        itempool += [self.create_item(ItemName.purifying)] * 14
        itempool += [self.create_item(ItemName.cure_ampoule)] * 5
        itempool += [self.create_item(ItemName.powerup)] * 10
        itempool += [self.create_item(ItemName.magical_nitro)] * 2
        itempool += [self.create_item(ItemName.mandragora)] * 2
        itempool += [self.create_item(ItemName.sun_card)] * 9
        itempool += [self.create_item(ItemName.moon_card)] * 8
        itempool += [self.create_item(ItemName.left_tower_key)] * 1
        itempool += [self.create_item(ItemName.storeroom_key)] * 1
        itempool += [self.create_item(ItemName.archives_key)] * 1
        itempool += [self.create_item(ItemName.garden_key)] * 1
        itempool += [self.create_item(ItemName.copper_key)] * 1
        itempool += [self.create_item(ItemName.chamber_key)] * 1
        itempool += [self.create_item(ItemName.execution_key)] * 1
        itempool += [self.create_item(ItemName.science_key_one)] * 1
        itempool += [self.create_item(ItemName.science_key_two)] * 1
        itempool += [self.create_item(ItemName.science_key_three)] * 1
        itempool += [self.create_item(ItemName.clocktower_key_one)] * 1
        itempool += [self.create_item(ItemName.clocktower_key_two)] * 1
        itempool += [self.create_item(ItemName.clocktower_key_three)] * 1

        if self.world.draculas_condition[self.player].value == 3:
            itempool += [self.create_item(ItemName.special_two)] * self.world.total_special2s[self.player].value

        if self.world.carrie_logic[self.player]:
            itempool += [self.create_item(ItemName.roast_beef)] * 1
            itempool += [self.create_item(ItemName.moon_card)] * 1
            total_required_locations += 2

        if self.world.lizard_generator_items[self.player]:
            itempool += [self.create_item(ItemName.powerup)] * 1
            itempool += [self.create_item(ItemName.sun_card)] * 1
            total_required_locations += 6

        total_junk_count = total_required_locations - len(itempool)

        junk_pool = []
        for item_name in self.world.random.choices(list(junk_table.keys()), k=total_junk_count):
            junk_pool += [self.create_item(item_name)]

        itempool += junk_pool

        self.active_level_list = char_level_list.copy()

        if self.world.stage_shuffle[self.player]:
            self.world.random.shuffle(self.active_level_list)
            self.villa_cc_ids = self.world.random.sample(range(0, 5), 2)

        if self.villa_cc_ids[0] < self.villa_cc_ids[1]:
            self.active_level_list.insert(self.villa_cc_ids[0], LocationName.villa)
            self.active_level_list.insert(self.villa_cc_ids[1] + 2, LocationName.castle_center)
        else:
            self.active_level_list.insert(self.villa_cc_ids[1], LocationName.castle_center)
            self.active_level_list.insert(self.villa_cc_ids[0] + 4, LocationName.villa)

        self.active_level_list.append(LocationName.castle_keep)

        connect_regions(self.world, self.player, self.active_level_list)

        self.world.itempool += itempool

    def generate_output(self, output_directory: str):
        try:
            world = self.world
            player = self.player

            rom = LocalRom(get_base_rom_path())

            offsets_to_ids = {}
            for location_name in self.location_name_to_id:
                loc = self.world.get_location(location_name, self.player)
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

            patch_rom(self.world, rom, self.player, offsets_to_ids)  # self.active_level_list

            outfilepname = f'_P{player}'
            outfilepname += f"_{world.player_name[player].replace(' ', '_')}" \
                if world.player_name[player] != 'Player%d' % player else ''

            rompath = os.path.join(output_directory, f'AP_{world.seed_name}{outfilepname}.sfc')
            rom.write_to_file(rompath)
            self.rom_name = rom.name

            patch = CV64DeltaPatch(os.path.splitext(rompath)[0]+CV64DeltaPatch.patch_file_ending, player=player,
                                   player_name=world.player_name[player], patched_path=rompath)
            patch.write()
        except:
            raise
        finally:
            if os.path.exists(rompath):
                os.unlink(rompath)
            self.rom_name_available_event.set()  # make sure threading continues and errors are collected

    def fill_slot_data(self) -> dict:
        slot_data = self._get_slot_data()
        for option_name in cv64_options:
            option = getattr(self.world, option_name)[self.player]
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
            multidata["connect_names"][new_name] = multidata["connect_names"][self.world.player_name[self.player]]
