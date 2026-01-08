import os
import math
import settings
import threading
import pkgutil

from BaseClasses import MultiWorld, Tutorial, ItemClassification, CollectionState
from worlds.AutoWorld import World, WebWorld
from .Items import DKCItem, item_table, misc_table, item_groups, STARTING_ID, option_name_to_world_name, items_that_open_checks
from .Locations import setup_locations, all_locations, location_groups
from .Regions import create_regions, connect_regions
from .Names import ItemName, LocationName
from .Options import DKCOptions, Logic, StartingKong, dkc_option_groups
from .Client import DKCSNIClient
from .Levels import generate_level_list, level_map, location_id_to_level_id
from .Rules import DKCStrictRules, DKCLooseRules, DKCExpertRules
from .Rom import patch_rom, DKCProcedurePatch, HASH_US

from typing import Dict, Set, List, ClassVar

class DKCSettings(settings.Group):
    class RomFile(settings.SNESRomPath):
        """File name of the Donkey Kong Country US v1.0 ROM"""
        description = "Donkey Kong Country (USA) ROM File"
        copy_to = "Donkey Kong Country (USA).sfc"
        md5s = [HASH_US]

    rom_file: RomFile = RomFile(RomFile.copy_to)


class DKCWeb(WebWorld):
    theme = "grass"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Donkey Kong Country with Archipelago",
        "English",
        "setup_en.md",
        "setup/en",
        ["lx5"]
    )
    
    setup_es = Tutorial(
        "Guía de configuración de Multiworld",
        "Guía para jugar Donkey Kong Country en Archipelago",
        "Spanish",
        "setup_es.md",
        "setup/es",
        ["lx5"]
    )

    tutorials = [setup_en]

    option_groups = dkc_option_groups


class DKCWorld(World):
    """
    monke
    """
    game = "Donkey Kong Country"
    web = DKCWeb()

    settings: ClassVar[DKCSettings]
    
    options_dataclass = DKCOptions
    options: DKCOptions
    
    required_client_version = (0, 6, 3)
    
    using_ut: bool
    ut_can_gen_without_yaml = True
    glitches_item_name = ItemName.glitched

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = all_locations
    item_name_groups = item_groups
    location_name_groups = location_groups
    hint_blacklist = {
        LocationName.defeated_gnawty_1,
        LocationName.defeated_necky_1,
        LocationName.defeated_bumble_b,
        LocationName.defeated_gnawty_2,
        LocationName.defeated_boss_dumb_drum,
        LocationName.defeated_necky_2,
    }

    def __init__(self, multiworld: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(multiworld, player)


    def create_regions(self) -> None:
        location_table = setup_locations(self)
        create_regions(self, location_table)
        
        connect_regions(self)
       

    def set_rules(self):
        logic = self.options.logic
        if logic == Logic.option_loose:
            DKCLooseRules(self).set_dkc_rules()
        elif logic == Logic.option_strict:
            DKCStrictRules(self).set_dkc_rules()
        elif logic == Logic.option_expert:
            DKCExpertRules(self).set_dkc_rules()
        else:
            raise ValueError(f"Somehow you have a logic option that's currently invalid."
                             f" {logic} for {self.multiworld.get_player_name(self.player)}")
        
        if not self.using_ut:
            # Test if sphere 1 has at least 2 reachable locations
            state = CollectionState(self.multiworld)
            initial_world = option_name_to_world_name[self.options.starting_world.current_option_name]
            available_items = items_that_open_checks[initial_world].copy()
            self.random.shuffle(available_items)
            available_items.append(initial_world)
            loc_count = 0
            while loc_count < 2:
                if len(available_items) == 0 and initial_world != ItemName.kongo_jungle:
                    available_items.append(ItemName.kongo_jungle)
                selected_item = available_items.pop()
                item = self.create_item(selected_item)
                state.collect(item, True)
                loc_count = self.test_starting_world(state)
                self.multiworld.push_precollected(item)
            
            self.create_item_late()

        # Universal Tracker: If we're using UT, scan the rules again to build "glitched logic" during the regen
        else:
            if logic == Logic.option_strict:
                DKCLooseRules(self).set_dkc_glitched_rules()
            elif logic == Logic.option_loose:
                DKCExpertRules(self).set_dkc_glitched_rules()


    def test_starting_world(self, state: CollectionState):
        loc_count = 0
        state.update_reachable_regions(self.player)
        regions = state.reachable_regions[self.player]
        for region in regions:
            for location in region.locations:
                if location.can_reach(state) and "(Event)" not in location.name:
                    loc_count += 1

        return loc_count
    
 
    def create_items(self) -> None:
        return 
    

    def create_item_late(self) -> None:
        itempool: List[DKCItem] = []

        self.total_required_locations = 106
        if self.options.kong_checks:
            self.total_required_locations += 33
        if self.options.token_checks:
            self.total_required_locations += 29
        if self.options.balloon_checks:
            self.total_required_locations += 12
        if self.options.banana_checks:
            self.total_required_locations += 183

        # Set starting kong
        if self.options.starting_kong == StartingKong.option_donkey:
            self.multiworld.push_precollected(self.create_item(ItemName.donkey))
            itempool += [self.create_item(ItemName.diddy)]
        elif self.options.starting_kong == StartingKong.option_diddy:
            self.multiworld.push_precollected(self.create_item(ItemName.diddy))
            itempool += [self.create_item(ItemName.donkey)]
        elif self.options.starting_kong == StartingKong.option_both:
            self.multiworld.push_precollected(self.create_item(ItemName.donkey))
            self.multiworld.push_precollected(self.create_item(ItemName.diddy))

        # Submit item pool
        for world_ in item_groups["Worlds"]:
            if world_ in self.multiworld.precollected_items[self.player]:
                continue
            else:
                itempool.append(self.create_item(world_))
                
        for item in item_groups["Abilities"]:
            if item in self.multiworld.precollected_items[self.player]:
                continue
            elif item in self.options.shuffle_abilities.value:
                classification = False
                if self.options.banana_checks.value and item == ItemName.slap:
                    classification = ItemClassification.progression | ItemClassification.useful
                itempool += [self.create_item(item, classification)]
            else:
                self.multiworld.push_precollected(self.create_item(item))

        for item in item_groups["Animals"]:
            if item in self.options.shuffle_animals.value:
                itempool += [self.create_item(item)]
            else:
                self.multiworld.push_precollected(self.create_item(item))
                
        for item in item_groups["Objects"]:
            if item in self.options.shuffle_objects.value:
                itempool += [self.create_item(item)]
            else:
                self.multiworld.push_precollected(self.create_item(item))

        if self.options.energy_link:
            itempool += [self.create_item(ItemName.extractinator) for _ in range(3)]

        itempool += [self.create_item(ItemName.radar)]

        # Add trap items into the pool
        junk_count = self.total_required_locations - len(itempool)
        trap_weights = []
        trap_weights += ([ItemName.jump_trap] * self.options.jump_trap_weight.value)
        trap_weights += ([ItemName.nut_trap] * self.options.nut_trap_weight.value)
        trap_weights += ([ItemName.army_trap] * self.options.army_trap_weight.value)
        trap_weights += ([ItemName.bonus_trap] * self.options.animal_bonus_trap_weight.value)
        trap_weights += ([ItemName.sticky_floor_trap] * self.options.sticky_floor_trap_weight.value)
        trap_weights += ([ItemName.stun_trap] * self.options.stun_trap_weight.value)
        trap_weights += ([ItemName.ice_trap] * self.options.ice_trap_weight.value)
        trap_count = 0 if (len(trap_weights) == 0) else math.ceil(junk_count * (self.options.trap_fill_percentage.value / 100.0))
        junk_count -= trap_count

        trap_pool = []
        for _ in range(trap_count):
            trap_item = self.random.choice(trap_weights)
            trap_pool.append(self.create_item(trap_item))
        
        itempool += trap_pool

        # Add junk items into the pool
        junk_weights = []
        junk_weights += ([ItemName.dk_barrel] * 60)
        junk_weights += ([ItemName.red_balloon] * 40)

        junk_pool = []
        for _ in range(junk_count):
            junk_item = self.random.choice(junk_weights)
            junk_pool.append(self.create_item(junk_item))

        itempool += junk_pool

        boss_locations = [
            LocationName.defeated_gnawty_1,
            LocationName.defeated_necky_1,
            LocationName.defeated_bumble_b,
            LocationName.defeated_gnawty_2,
            LocationName.defeated_boss_dumb_drum,
            LocationName.defeated_necky_2,
        ]
        for location in boss_locations:
            self.multiworld.get_location(location, self.player).place_locked_item(self.create_item(ItemName.boss_token))

        self.multiworld.itempool += itempool


    def create_item(self, name: str, force_classification=False) -> DKCItem:
        data = item_table[name]

        if force_classification:
            classification = force_classification
        else:
            classification = data.classsification
        
        created_item = DKCItem(name, classification, data.code, self.player)

        return created_item


    def interpret_slot_data(self, slot_data):
        return slot_data
    
    
    def fill_slot_data(self):
        slot_data = {}
        slot_data["level_connections"] = self.level_connections
        slot_data["boss_connections"] = self.boss_connections
        slot_data["logic"] = self.options.logic.value
        slot_data["glitched_world_access"] = self.options.glitched_world_access.value
        slot_data["starting_kong"] = self.options.starting_kong.value
        slot_data["gangplank_tokens"] = self.options.gangplank_tokens.value
        slot_data["starting_world"] = self.options.starting_world.value
        slot_data["kong_checks"] = self.options.kong_checks.value
        slot_data["balloon_checks"] = self.options.balloon_checks.value
        slot_data["banana_checks"] = self.options.banana_checks.value
        slot_data["token_checks"] = self.options.token_checks.value
        slot_data["energy_link"] = self.options.energy_link.value
        slot_data["required_jungle_levels"] = self.options.required_jungle_levels.value
        slot_data["required_mines_levels"] = self.options.required_mines_levels.value
        slot_data["required_valley_levels"] = self.options.required_valley_levels.value
        slot_data["required_glacier_levels"] = self.options.required_glacier_levels.value
        slot_data["required_industries_levels"] = self.options.required_industries_levels.value
        slot_data["required_caverns_levels"] = self.options.required_caverns_levels.value
        slot_data["trap_weights"] = self.output_trap_weights()

        return slot_data

    def output_trap_weights(self) -> Dict[int, int]:
        trap_data = {}

        trap_data[STARTING_ID + 0x0080] = self.options.nut_trap_weight.value
        trap_data[STARTING_ID + 0x0081] = self.options.army_trap_weight.value
        trap_data[STARTING_ID + 0x0082] = self.options.jump_trap_weight.value
        trap_data[STARTING_ID + 0x0083] = self.options.animal_bonus_trap_weight.value
        trap_data[STARTING_ID + 0x0084] = self.options.sticky_floor_trap_weight.value
        trap_data[STARTING_ID + 0x0085] = self.options.stun_trap_weight.value
        trap_data[STARTING_ID + 0x0086] = self.options.ice_trap_weight.value

        return trap_data

    def generate_early(self):
        # Shuffle levels
        self.level_connections: Dict[str, str] = dict()
        self.boss_connections: Dict[str, str] = dict()
        self.rom_connections: Dict[str, str] = dict()
        self.lost_world_levels: Set[str] = set()
        generate_level_list(self)

        # Handle Universal Tracker support, doesn't do anything during regular generation
        if hasattr(self.multiworld, "re_gen_passthrough"):
            if "Donkey Kong Country" in self.multiworld.re_gen_passthrough:
                self.using_ut = True
                passthrough = self.multiworld.re_gen_passthrough["Donkey Kong Country"]
                self.level_connections = passthrough["level_connections"]
                self.boss_connections = passthrough["boss_connections"]
                self.options.logic.value = passthrough["logic"]
                self.options.glitched_world_access.value = passthrough["glitched_world_access"]
                self.options.starting_kong.value = passthrough["starting_kong"]
                self.options.gangplank_tokens.value = passthrough["gangplank_tokens"]
                self.options.starting_world.value = passthrough["starting_world"]
                self.options.kong_checks.value = passthrough["kong_checks"]
                self.options.token_checks.value = passthrough["token_checks"]
                self.options.balloon_checks.value = passthrough["balloon_checks"]
                self.options.banana_checks.value = passthrough["banana_checks"]
                self.options.required_jungle_levels.value = passthrough["required_jungle_levels"]
                self.options.required_mines_levels.value = passthrough["required_mines_levels"]
                self.options.required_valley_levels.value = passthrough["required_valley_levels"]
                self.options.required_glacier_levels.value = passthrough["required_glacier_levels"]
                self.options.required_industries_levels.value = passthrough["required_industries_levels"]
                self.options.required_caverns_levels.value = passthrough["required_caverns_levels"]
            else:
                self.using_ut = False
        else:
            self.using_ut = False


    def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]):
        er_hint_data = {}
        map_connections = {**self.level_connections, **self.boss_connections}
        for loc_name in location_id_to_level_id.keys():
            level_name = loc_name.split(' - ')[0] + ": Level"
            for map_spot, level in map_connections.items():
                if level != level_name:
                    continue
                if "KONG" in loc_name and not self.options.kong_checks:
                    continue
                if "Token" in loc_name and not self.options.token_checks:
                    continue
                if "Balloon" in loc_name and not self.options.balloon_checks:
                    continue
                if "Banana Bunch" in loc_name and not self.options.banana_checks:
                    continue
                location = self.multiworld.get_location(loc_name, self.player)
                er_hint_data[location.address] = level_map[map_spot]
        
        hint_data[self.player] = er_hint_data


    def get_filler_item_name(self) -> str:
        return self.random.choice(list(misc_table.keys()))


    def generate_output(self, output_directory: str):
        try:
            patch = DKCProcedurePatch(player=self.player, player_name=self.multiworld.player_name[self.player])
            patch.write_file("dkc_basepatch.bsdiff4", pkgutil.get_data(__name__, "data/dkc_basepatch.bsdiff4"))
            patch_rom(self, patch)

            self.rom_name = patch.name

            patch.write(os.path.join(output_directory,
                                     f"{self.multiworld.get_out_file_name_base(self.player)}{patch.patch_file_ending}"))
        except Exception:
            raise
        finally:
            self.rom_name_available_event.set()  # make sure threading continues and errors are collected


    def modify_multidata(self, multidata: dict):
        import base64
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]
