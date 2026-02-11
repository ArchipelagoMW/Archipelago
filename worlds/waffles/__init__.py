import os
import typing
import math
import settings
import threading
import pkgutil

from BaseClasses import MultiWorld, Tutorial, ItemClassification, LocationProgressType, Location, CollectionState, Entrance, Region
from Options import OptionError
from worlds.LauncherComponents import launch as launch_component, components, Component, Type
from worlds.AutoWorld import WebWorld, World

from .Client import WaffleSNIClient
from .Items import WaffleItem, item_table, junk_table, option_name_to_item_unlock
from .Levels import full_level_list, generate_level_list, generate_swapped_exits, generate_carryless_exits, special_zone_tile_regions, switch_palace_locations, castle_locations, ghost_house_locations
from .Locations import all_locations, location_groups, setup_locations, level_location_table, \
                       egg_location_table, castle_location_table, switch_palace_location_table, ghost_house_location_table
from .Names import ItemName, LocationName
from .Options import WaffleOptions, waffle_option_groups, Goal
from .Presets import waffle_options_presets
from .Regions import create_regions, connect_regions, add_location_to_region
from .Rom import patch_rom, WaffleProcedurePatch, USHASH
from .Rules import WaffleBasicRules
from .Teleports import generate_entrance_rando
from .Tracker import setup_options_from_slot_data, reconnect_found_entrance, disconnect_entrances

def launch_manager(*args):
    from .Manager import launch
    launch_component(launch, "Waffles Manager")

components.append(Component(display_name="Waffles Manager", component_type=Type.ADJUSTER, func=launch_manager))

class WaffleSetings(settings.Group):
    class RomFile(settings.SNESRomPath):
        """File name of the SMW US rom"""
        description = "Super Mario World (USA) ROM File"
        copy_to = "Super Mario World (USA).sfc"
        md5s = [USHASH]

    class GraphicsPath(settings.OptionalUserFilePath):
        """
        File name of the graphics pack to be used.
        Preferably point it to a .zip file in /data/sprites/smw/
        """

    rom_file: RomFile = RomFile(RomFile.copy_to)
    graphics_file: GraphicsPath = "data/sprites/smw/"


class WaffleWeb(WebWorld):
    theme = "grass"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Spicy Mycena Waffles randomizer connected to an Archipelago Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["PoryGone"]
    )
    
    tutorials = [setup_en]
    
    option_groups = waffle_option_groups
    options_presets = waffle_options_presets


class WaffleWorld(World):
    """
    Spicy Mycena Waffles (SMW) is an extension of the original Super Mario World Archipelago implementation
    that features several core changes for better or for worse.
    """
    game: str = "SMW: Spicy Mycena Waffles"

    settings: typing.ClassVar[WaffleSetings]

    options_dataclass = WaffleOptions
    options: WaffleOptions

    topology_present = False
    required_client_version = (0, 6, 5)

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = all_locations
    location_name_groups = location_groups

    using_ut: bool
    ut_can_gen_without_yaml = True
    glitches_item_name = ItemName.glitched
    disconnected_entrances: dict[Entrance, Region]
    found_entrances_datastorage_key: list[str]

    active_level_dict: typing.Dict[int,int]
    active_location_table: typing.Dict[str,int]

    web = WaffleWeb()
    
    def __init__(self, multiworld: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(multiworld, player)
    
    def generate_early(self):
        self.ordered_double_exits = list()
        self.teleport_data = dict()
        self.teleport_pairs = dict()
        self.reverse_teleport_pairs = dict()
        self.cached_connections = dict()
        self.transition_pairs = dict()
        self.reverse_transition_pairs = dict()
        self.transition_data = dict()
        self.local_mapping = dict()
        self.local_region_mapping = dict()
        self.swapped_exits = list()
        self.carryless_exits = list()
        self.special_zone_egg_locations = list()
        self.boss_token_requirements = {
            LocationName.yi_to_ysp: 0,
            LocationName.yi_to_dp: 1,
            LocationName.dp_to_vd: 2,
            LocationName.tw_to_foi: 4,
            LocationName.foi_to_ci: 4,
            LocationName.foi_to_sr: 4,
            LocationName.ci_to_vob: 6,
            LocationName.donut_plains_star_road: 1,
            LocationName.vanilla_dome_star_road: 2,
            LocationName.twin_bridges_star_road: 3,
            LocationName.forest_star_road: 5,
            LocationName.valley_star_road: 6,
            LocationName.star_road_special: 1,
            LocationName.special_complete: 1,
            LocationName.donut_plains_entrance_pipe: 1,
            LocationName.valley_donut_entrance_pipe: 1,
            LocationName.vanilla_dome_top_entrance_pipe: 2,
            LocationName.vanilla_dome_bottom_entrance_pipe: 3,
            LocationName.chocolate_island_entrance_pipe: 5,
            LocationName.valley_chocolate_entrance_pipe: 5,
        }

        # Handle UT support
        setup_options_from_slot_data(self)

        if not self.using_ut:
            # Bonk non level shuffle users trying to do something weird
            if self.options.starting_location.value != 0 and not self.options.level_shuffle.value:
                raise OptionError(f"{self.player_name} has a very weird combination of settings that will result in a failed generation.\n"
                                f"  Please enable level_shuffle if you desire to change the starting location.")
            if self.options.starting_location.value == 0x04 and self.options.map_teleport_shuffle != "on_both_mix":
                raise OptionError(f"{self.player_name} has a very weird combination of settings that will result in a failed generation.\n"
                                f"  Please enable map_teleport_shuffle with the option 'on_both_mix'.")
            if self.options.starting_location.value == 0x02 and self.options.map_teleport_shuffle != "on_both_mix":
                raise OptionError(f"{self.player_name} has a very weird combination of settings that will result in a failed generation.\n"
                                f"  Please enable map_teleport_shuffle with the option 'on_both_mix'.")

            # Bonk "minimal" accesibility users if they go full derp with their settings
            if self.options.accessibility == "minimal" and self.options.percentage_of_yoshi_eggs.value < 90:
                self.options.percentage_of_yoshi_eggs.value = 90
                valid_loc_count = int(self.count_locations()/10) 
                egg_count = min(self.count_egg_locations() + self.options.yoshi_egg_count.value, 255)
                if valid_loc_count < egg_count:
                    raise OptionError(f"{self.player_name} has a very weird combination of settings that will result in a failed generation.\n"
                                    f"  Please set less Yoshi Eggs your YAML file or DON'T use minimal accessibility.")
                
            # Enforce disabling DeathLink for now
            if self.options.death_link:
                print(f"Enforcing non-DeathLink session for \"{self.player_name}\" (option doesn't work).")
                self.options.death_link.value = False

            # Enforce disabling RingLink for now
            if self.options.death_link:
                print(f"Enforcing non-RingLink session for \"{self.player_name}\" (option requires some design adjustments).")
                self.options.ring_link.value = False

            if self.options.early_climb:
                self.multiworld.local_early_items[self.player][ItemName.mario_climb] = 1

            # Only randomize data if not using UT
            generate_entrance_rando(self)
            self.active_level_dict = dict(zip(generate_level_list(self), full_level_list))
            generate_swapped_exits(self)
            generate_carryless_exits(self)

        self.reverse_teleport_pairs = {y: x for x, y in self.teleport_pairs.items()}
        self.reverse_transition_pairs = {y: x for x, y in self.transition_pairs.items()}

    
    def create_regions(self):
        location_table = setup_locations(self)
        create_regions(self, location_table)
        self.active_location_table = location_table

        self.topology_present = self.options.level_shuffle

        connect_regions(self, self.active_level_dict)

        if "Every Level" in self.options.yoshi_egg_placement.value:
            for egg_loc_name in egg_location_table.keys():
                loc_name = egg_loc_name.replace(" (Hidden Egg)", "")
                add_location_to_region(self, self.active_location_table, loc_name, egg_loc_name)
        else:
            if "Castles" in self.options.yoshi_egg_placement.value:
                for egg_loc_name in castle_location_table.keys():
                    loc_name = egg_loc_name.replace(" (Hidden Egg)", "")
                    add_location_to_region(self, self.active_location_table, loc_name, egg_loc_name)

            if "Switch Palaces" in self.options.yoshi_egg_placement.value:
                for egg_loc_name in switch_palace_location_table.keys():
                    loc_name = egg_loc_name.replace(" (Hidden Egg)", "")
                    add_location_to_region(self, self.active_location_table, loc_name, egg_loc_name)

            if "Ghost Houses" in self.options.yoshi_egg_placement.value:
                for egg_loc_name in ghost_house_location_table.keys():
                    loc_name = egg_loc_name.replace(" (Hidden Egg)", "")
                    add_location_to_region(self, self.active_location_table, loc_name, egg_loc_name)

            if "Special Zone" in self.options.yoshi_egg_placement.value:
                for tile in special_zone_tile_regions:
                    tile_region = self.multiworld.get_region(tile, self.player)
                    level_region = tile_region.exits[0].connected_region
                    level_exit = level_region.exits[0].connected_region
                    for location in level_exit.get_locations():
                        location: Location
                        egg_loc_name = f"{location.name} (Hidden Egg)"
                        if "(Hidden Egg)" not in location.name and egg_loc_name not in self.active_location_table.keys():
                            self.active_location_table[egg_loc_name] = egg_location_table[egg_loc_name] | 0x01
                            add_location_to_region(self, self.active_location_table, location.name, egg_loc_name)
                            self.special_zone_egg_locations.append(egg_loc_name)


    # UT Stuff, will be worked on later lol
    def connect_entrances(self):
        if self.using_ut and self.multiworld.enforce_deferred_connections in ("on", "default"):
            disconnect_entrances(self)

    def reconnect_found_entrances(self, key: str, value: typing.Any) -> None:
        if not value:
            return
        else:
            reconnect_found_entrance(self, key)


    def set_rules(self):
        rules = WaffleBasicRules(self)
        rules.set_smw_rules()

        if self.using_ut:
            game_difficulty = self.options.game_logic_difficulty.value
            if game_difficulty != 2:
                rules.set_glitched_rules()

        return     
        # Debug
        from Utils import visualize_regions
        state = CollectionState(self.multiworld)
        state.update_reachable_regions(self.player)
        visualize_regions(self.get_region("Menu"), "my_world.puml", show_entrance_names=True,
                        regions_to_highlight=state.reachable_regions[self.player])

    
    def create_items(self):
        if self.using_ut:
            return
        
        itempool: typing.List[WaffleItem] = []

        total_required_locations = self.count_locations()

        if "Powerups" in self.options.ability_shuffle.value:
            itempool += [self.create_item(ItemName.progressive_powerup) for _ in range(3)]
        else:
            self.multiworld.push_precollected(self.create_item(ItemName.progressive_powerup))
            self.multiworld.push_precollected(self.create_item(ItemName.progressive_powerup))
            self.multiworld.push_precollected(self.create_item(ItemName.progressive_powerup))

        if "Yoshi" in self.options.ability_shuffle.value:
            itempool += [self.create_item(ItemName.yoshi) for _ in range(2)]
        else:
            self.multiworld.push_precollected(self.create_item(ItemName.yoshi))
            self.multiworld.push_precollected(self.create_item(ItemName.yoshi))

        if "Run" in self.options.ability_shuffle.value:
            itempool += [self.create_item(ItemName.mario_run) for _ in range(2)]
        else:
            itempool += [self.create_item(ItemName.mario_run)]
            self.multiworld.push_precollected(self.create_item(ItemName.mario_run))

        if "Carry" in self.options.ability_shuffle.value:
            itempool += [self.create_item(ItemName.mario_carry)]
        else:
            self.multiworld.push_precollected(self.create_item(ItemName.mario_carry))

        if "Swim" in self.options.ability_shuffle.value:
            itempool += [self.create_item(ItemName.mario_swim) for _ in range(2)]
        else:
            itempool += [self.create_item(ItemName.mario_swim)]
            self.multiworld.push_precollected(self.create_item(ItemName.mario_swim))

        if "Spin Jump" in self.options.ability_shuffle.value:
            itempool += [self.create_item(ItemName.mario_spin_jump)]
        else:
            self.multiworld.push_precollected(self.create_item(ItemName.mario_spin_jump))

        if "Climb" in self.options.ability_shuffle.value:
            itempool += [self.create_item(ItemName.mario_climb)]
        else:
            self.multiworld.push_precollected(self.create_item(ItemName.mario_climb))

        if "P-Switch" in self.options.ability_shuffle.value:
            itempool += [self.create_item(ItemName.p_switch)]
        else:
            self.multiworld.push_precollected(self.create_item(ItemName.p_switch))

        if "P-Balloon" in self.options.ability_shuffle.value:
            itempool += [self.create_item(ItemName.p_balloon)]
        else:
            self.multiworld.push_precollected(self.create_item(ItemName.p_balloon))

        if "Super Star" in self.options.ability_shuffle.value:
            itempool += [self.create_item(ItemName.super_star_active) for _ in range(9)]
        else:
            itempool += [self.create_item(ItemName.super_star_active) for _ in range(7)]
            self.multiworld.push_precollected(self.create_item(ItemName.super_star_active))
            self.multiworld.push_precollected(self.create_item(ItemName.super_star_active))

        if "Yellow Switch Palace" in self.options.ability_shuffle.value:
            if "Yellow Switch Palace Blocks" in self.options.block_checks.value:
                itempool += [self.create_item(ItemName.yellow_switch_palace)]
            else:
                itempool += [self.create_item(ItemName.yellow_switch_palace, ItemClassification.progression)]
        else:
            self.multiworld.push_precollected(self.create_item(ItemName.yellow_switch_palace))

        if "Green Switch Palace" in self.options.ability_shuffle.value:
            if "Green Switch Palace Blocks" in self.options.block_checks.value:
                itempool += [self.create_item(ItemName.green_switch_palace)]
            else:
                itempool += [self.create_item(ItemName.green_switch_palace, ItemClassification.progression)]
        else:
            self.multiworld.push_precollected(self.create_item(ItemName.green_switch_palace))

        if "Red Switch Palace" in self.options.ability_shuffle.value:
            itempool += [self.create_item(ItemName.red_switch_palace)]
        else:
            self.multiworld.push_precollected(self.create_item(ItemName.red_switch_palace))

        if "Blue Switch Palace" in self.options.ability_shuffle.value:
            itempool += [self.create_item(ItemName.blue_switch_palace)]
        else:
            self.multiworld.push_precollected(self.create_item(ItemName.blue_switch_palace))

        if "Midway Points" in self.options.ability_shuffle.value:
            if self.options.midway_point_checks:
                itempool += [self.create_item(ItemName.midway_point, ItemClassification.progression | ItemClassification.useful)]
            else:
                if self.options.game_logic_difficulty == "hard":
                    itempool += [self.create_item(ItemName.midway_point, ItemClassification.useful)]
                else:
                    itempool += [self.create_item(ItemName.midway_point)]
        else:
            self.multiworld.push_precollected(self.create_item(ItemName.midway_point))
            
        if "Special World" in self.options.ability_shuffle.value:
            itempool += [self.create_item(ItemName.special_world_clear)]
        else:
            self.multiworld.push_precollected(self.create_item(ItemName.special_world_clear))

        itempool += [self.create_item(ItemName.better_timer) for _ in range(3)]

        if "Item Box" in self.options.ability_shuffle.value:
            if self.options.game_logic_difficulty != "hard":
                itempool += [self.create_item(ItemName.item_box, ItemClassification.progression)]
            else:
                itempool += [self.create_item(ItemName.item_box)]
        else:
            self.multiworld.push_precollected(self.create_item(ItemName.item_box))

        if self.options.game_logic_difficulty == "easy":
            itempool += [self.create_item(ItemName.extra_defense, ItemClassification.progression)]
        else:
            itempool += [self.create_item(ItemName.extra_defense)]
        
        # Create Golden Yoshi Eggs
        processed_levels = set()
        egg_classsification = ItemClassification.progression_deprioritized_skip_balancing
        placed_eggs = 0
        if "Every Level" in self.options.yoshi_egg_placement.value:
            for loc_name in level_location_table.keys():
                processed_levels.add(f"{loc_name} (Hidden Egg)")
                location = self.multiworld.get_location(f"{loc_name} (Hidden Egg)", self.player)
                if location.progress_type is not LocationProgressType.EXCLUDED:
                    if self.options.ungolden_eggs:
                        location.place_locked_item(self.create_item(ItemName.yoshi_egg, egg_classsification))
                    else:
                        location.place_locked_item(self.create_item(ItemName.yoshi_egg))
                    placed_eggs += 1
        else:
            if "Castles" in self.options.yoshi_egg_placement.value:
                for level in castle_locations:
                    processed_levels.add(f"{level} (Hidden Egg)")
                    location = self.multiworld.get_location(f"{level} (Hidden Egg)", self.player)
                    if location.progress_type is not LocationProgressType.EXCLUDED:
                        if self.options.ungolden_eggs:
                            location.place_locked_item(self.create_item(ItemName.yoshi_egg, egg_classsification))
                        else:
                            location.place_locked_item(self.create_item(ItemName.yoshi_egg))
                        placed_eggs += 1
            if "Switch Palaces" in self.options.yoshi_egg_placement.value:
                for level in switch_palace_locations:
                    processed_levels.add(f"{level} (Hidden Egg)")
                    location = self.multiworld.get_location(f"{level} (Hidden Egg)", self.player)
                    if location.progress_type is not LocationProgressType.EXCLUDED:
                        if self.options.ungolden_eggs:
                            location.place_locked_item(self.create_item(ItemName.yoshi_egg, egg_classsification))
                        else:
                            location.place_locked_item(self.create_item(ItemName.yoshi_egg))
                        placed_eggs += 1
            if "Ghost Houses" in self.options.yoshi_egg_placement.value:
                for level in ghost_house_locations:
                    processed_levels.add(f"{level} (Hidden Egg)")
                    location = self.multiworld.get_location(f"{level} (Hidden Egg)", self.player)
                    if location.progress_type is not LocationProgressType.EXCLUDED:
                        if self.options.ungolden_eggs:
                            location.place_locked_item(self.create_item(ItemName.yoshi_egg, egg_classsification))
                        else:
                            location.place_locked_item(self.create_item(ItemName.yoshi_egg))
                        placed_eggs += 1
            if "Special Zone" in self.options.yoshi_egg_placement.value:
                for loc_name in self.special_zone_egg_locations:
                    if loc_name in processed_levels:
                        continue
                    processed_levels.add(f"{loc_name}")
                    location = self.multiworld.get_location(loc_name, self.player)
                    if location.progress_type is not LocationProgressType.EXCLUDED:
                        if self.options.ungolden_eggs:
                            location.place_locked_item(self.create_item(ItemName.yoshi_egg, egg_classsification))
                        else:
                            location.place_locked_item(self.create_item(ItemName.yoshi_egg))
                        placed_eggs += 1

        raw_egg_count = max(0, min(total_required_locations - self.options.yoshi_egg_count.value + len(processed_levels), 255))
        total_egg_count = min(raw_egg_count, self.options.yoshi_egg_count.value + len(processed_levels), 255)
        if total_egg_count > len(processed_levels):
            if self.options.ungolden_eggs:
                itempool += [self.create_item(ItemName.yoshi_egg, egg_classsification) for _ in range(total_egg_count - len(processed_levels))]
            else:
                itempool += [self.create_item(ItemName.yoshi_egg) for _ in range(total_egg_count - len(processed_levels))]

        self.actual_egg_count = total_egg_count
        self.required_egg_count = max(math.floor(total_egg_count * (self.options.percentage_of_yoshi_eggs.value / 100.0)), 0)

        if self.options.goal == Goal.option_yoshi_house:
            self.multiworld.get_location(LocationName.yoshis_house, self.player).place_locked_item(self.create_item(ItemName.victory))
        else:
            self.multiworld.get_location(LocationName.bowser, self.player).place_locked_item(self.create_item(ItemName.victory))

        junk_count = total_required_locations - len(itempool)
        trap_weights = []
        trap_weights += ([ItemName.ice_trap] * self.options.ice_trap_weight.value)
        trap_weights += ([ItemName.stun_trap] * self.options.stun_trap_weight.value)
        trap_weights += ([ItemName.literature_trap] * self.options.literature_trap_weight.value)
        trap_weights += ([ItemName.timer_trap] * self.options.timer_trap_weight.value)
        trap_weights += ([ItemName.reverse_controls_trap] * self.options.reverse_trap_weight.value)
        trap_weights += ([ItemName.thwimp_trap] * self.options.thwimp_trap_weight.value)
        trap_weights += ([ItemName.fishin_trap] * self.options.fishin_trap_weight.value)
        trap_weights += ([ItemName.screen_flip_trap] * self.options.screen_flip_trap_weight.value)
        trap_weights += ([ItemName.sticky_floor_trap] * self.options.sticky_floor_trap_weight.value)
        trap_weights += ([ItemName.sticky_hands_trap] * self.options.sticky_hands_trap_weight.value)
        trap_weights += ([ItemName.pixelate_trap] * self.options.pixelate_trap_weight.value)
        trap_weights += ([ItemName.spotlight_trap] * self.options.spotlight_trap_weight.value)
        trap_weights += ([ItemName.bullet_time_trap] * self.options.bullet_time_trap_weight.value)
        trap_weights += ([ItemName.invisibility_trap] * self.options.invisibility_trap_weight.value)
        trap_weights += ([ItemName.empty_item_box_trap] * self.options.empty_item_box_trap_weight.value)
        trap_count = 0 if (len(trap_weights) == 0) else math.ceil(junk_count * (self.options.trap_fill_percentage.value / 100.0))
        junk_count -= trap_count

        trap_pool = []
        for _ in range(trap_count):
            trap_item = self.random.choice(trap_weights)
            trap_pool.append(self.create_item(trap_item))

        itempool += trap_pool

        junk_weights = []
        junk_weights += ([ItemName.one_coin] * 3)
        junk_weights += ([ItemName.five_coins] * 4)
        junk_weights += ([ItemName.ten_coins] * 5)
        junk_weights += ([ItemName.fifty_coins] * 7)
        junk_weights += ([ItemName.heart_inventory] * 25)
        junk_weights += ([ItemName.mushroom_inventory] * 25)
        junk_weights += ([ItemName.fire_flower_inventory] * 15)
        junk_weights += ([ItemName.feather_inventory] * 15)
        junk_weights += ([ItemName.star_inventory] * 20)
        junk_weights += ([ItemName.green_yoshi_inventory] * 10)
        junk_weights += ([ItemName.red_yoshi_inventory] * 10)
        junk_weights += ([ItemName.blue_yoshi_inventory] * 10)
        junk_weights += ([ItemName.yellow_yoshi_inventory] * 10)
        junk_weights += ([ItemName.trap_repellent] * 8)

        junk_pool = [self.create_item(self.random.choice(junk_weights)) for _ in range(junk_count)]
        
        itempool += junk_pool

        self.multiworld.itempool += itempool


    def create_item(self, name: str, force_classification: ItemClassification | bool = False) -> WaffleItem:
        classification = item_table[name].type
        if force_classification:
            classification = force_classification
        return WaffleItem(name, classification, item_table[name].code, self.player)


    def count_locations(self):
        from . import Locations

        total_required_locations = 96
        if self.options.dragon_coin_checks:
            total_required_locations += len(Locations.dragon_coin_location_table.keys())
        if self.options.moon_checks:
            total_required_locations += len(Locations.moon_location_table.keys())
        if self.options.hidden_1up_checks:
            total_required_locations += len(Locations.hidden_1ups_location_table.keys())
        if self.options.star_block_checks:
            total_required_locations += len(Locations.prize_location_table.keys())
        if self.options.midway_point_checks:
            total_required_locations += len(Locations.midway_point_location_table.keys())
        if self.options.room_checks:
            total_required_locations += len(Locations.room_location_table.keys())
        block_checks = self.options.block_checks.value
        if "Coin Blocks" in block_checks:
            total_required_locations += len(Locations.coin_block_location_table.keys())
        if "Item Blocks" in block_checks:
            total_required_locations += len(Locations.item_block_location_table.keys())
        if "Yellow Switch Palace Blocks" in block_checks:
            total_required_locations += len(Locations.ysp_block_location_table.keys())
        if "Green Switch Palace Blocks" in block_checks:
            total_required_locations += len(Locations.gsp_block_location_table.keys())
        if "Invisible Blocks" in block_checks:
            total_required_locations += len(Locations.invisible_block_location_table.keys())
        if "P-Switch Blocks" in block_checks:
            total_required_locations += len(Locations.pswitch_block_location_table.keys())
        if "Flying Blocks" in block_checks:
            total_required_locations += len(Locations.flying_block_location_table.keys())
        
        return total_required_locations

    def count_egg_locations(self):
        if "Every Level" in self.options.yoshi_egg_placement.value:
            return 96
        else:
            total_required_locations = 0
            if "Castles" in self.options.yoshi_egg_placement.value:
                total_required_locations += len(castle_location_table.keys())

            if "Switch Palaces" in self.options.yoshi_egg_placement.value:
                total_required_locations += len(switch_palace_location_table.keys())

            if "Ghost Houses" in self.options.yoshi_egg_placement.value:
                total_required_locations += len(ghost_house_location_table.keys())

            if "Special Zone" in self.options.yoshi_egg_placement.value:
                total_required_locations += 8
        
        return total_required_locations


    def generate_output(self, output_directory: str):
        try:
            patch = WaffleProcedurePatch(player=self.player, player_name=self.multiworld.player_name[self.player])
            patch.write_file("smw_sa1_basepatch.bsdiff4", pkgutil.get_data(__name__, "data/smw_sa1_basepatch.bsdiff4"))
            patch.write_file("sprite_graphics.bsdiff4", pkgutil.get_data(__name__, "data/sprite_graphics.bsdiff4"))
            patch.write_file("sprite_page_1.bsdiff4", pkgutil.get_data(__name__, "data/sprite_page_1.bsdiff4"))
            patch.write_file("sprite_page_2.bsdiff4", pkgutil.get_data(__name__, "data/sprite_page_2.bsdiff4"))
            patch.write_file("map_sprites.bsdiff4", pkgutil.get_data(__name__, "data/map_sprites.bsdiff4"))
            patch.write_file("midway_point.bsdiff4", pkgutil.get_data(__name__, "data/midway_point.bsdiff4"))
            patch_rom(self, patch, self.player, self.active_level_dict)

            self.rom_name = patch.name

            patch.write(os.path.join(output_directory,
                                     f"{self.multiworld.get_out_file_name_base(self.player)}{patch.patch_file_ending}"))
            patch.write()
        except:
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

    def extend_hint_information(self, hint_data: typing.Dict[int, typing.Dict[int, str]]):
        if self.topology_present:
            world_names = [
                LocationName.yoshis_island_region,
                LocationName.donut_plains_region,
                LocationName.vanilla_dome_region,
                LocationName.twin_bridges_region,
                LocationName.forest_of_illusion_region,
                LocationName.chocolate_island_region,
                LocationName.valley_of_bowser_region,
                LocationName.star_road_region,
                LocationName.special_zone_region,
            ]
            world_cutoffs = [
                0x07,
                0x13,
                0x1F,
                0x26,
                0x30,
                0x39,
                0x44,
                0x4F,
                0x59
            ]
            er_hint_data = {}
            for loc_name, loc_id in self.active_location_table.items():
                level_id = loc_id >> 24

                if level_id not in self.active_level_dict:
                    continue

                keys_list = list(self.active_level_dict.keys())
                level_index = keys_list.index(level_id)
                for i in range(len(world_cutoffs)):
                    if level_index >= world_cutoffs[i]:
                        continue

                    location = self.multiworld.get_location(loc_name, self.player)
                    er_hint_data[location.address] = world_names[i]
                    break

            hint_data[self.player] = er_hint_data


    def write_spoiler_header(self, spoiler_handle: typing.TextIO) -> None:
        from .Levels import level_info_dict, possible_starting_entrances, banned_spoiler_levels

        if self.options.level_shuffle.value:
            spoiler_handle.write(f"\nLevel Shuffle Results:\n")
            for level_id, tile_id in self.active_level_dict.items():
                if level_id >= 0x60 or level_id in banned_spoiler_levels:
                    continue
                shuffled_level = level_info_dict[level_id]
                original_level = level_info_dict[tile_id]
                spoiler_handle.write(f"    {original_level.levelName} -> {shuffled_level.levelName}\n")
        
        spoiler_handle.write(f"\nStarting Location: {possible_starting_entrances[self.options.starting_location.value]}\n")

        if self.options.map_teleport_shuffle.value != 0:
            spoiler_handle.write(f"\nMap Teleport Shuffle Results:\n")
            for entrance, exit in self.teleport_pairs.items():
                spoiler_handle.write(f"    {entrance} -> {exit}\n")

        if self.options.map_transition_shuffle.value != 0:
            spoiler_handle.write(f"\nMap Transition Shuffle Results:\n")
            for entrance, exit in self.transition_pairs.items():
                spoiler_handle.write(f"    {entrance[13:]} -> {exit[13:]}\n")


    def get_filler_item_name(self) -> str:
        return self.random.choice(list(junk_table.keys()))


    def fill_slot_data(self) -> dict:
        slot_data = self.options.as_dict(
            "dragon_coin_checks",
            "moon_checks",
            "hidden_1up_checks",
            "star_block_checks",
            "midway_point_checks",
            "room_checks",
            "block_checks",
            "energy_link",
            "swap_level_exits",
            "game_logic_difficulty",
            "inventory_yoshi_logic",
            "goal",
            "yoshi_egg_count",
            "enemy_shuffle",
            "yoshi_egg_placement",
            "starting_location",
            "ability_shuffle",
        )
        slot_data["active_levels"] = self.active_level_dict
        slot_data["teleport_pairs"] = self.teleport_pairs
        slot_data["transition_pairs"] = self.transition_pairs
        slot_data["swapped_exits"] = self.swapped_exits
        slot_data["carryless_exits"] = self.carryless_exits
        slot_data["required_egg_count"] = self.required_egg_count
        slot_data["actual_egg_count"] = self.actual_egg_count
        slot_data["trap_weights"] = self.output_trap_weights()

        return slot_data

    def output_trap_weights(self) -> typing.Dict[int, int]:
        trap_data = {}

        trap_data[0xBC0080] = self.options.ice_trap_weight.value
        trap_data[0xBC0081] = self.options.stun_trap_weight.value
        trap_data[0xBC0082] = self.options.literature_trap_weight.value
        trap_data[0xBC0083] = self.options.timer_trap_weight.value
        trap_data[0xBC0084] = self.options.reverse_trap_weight.value
        trap_data[0xBC0085] = self.options.thwimp_trap_weight.value
        trap_data[0xBC0086] = self.options.fishin_trap_weight.value
        trap_data[0xBC0087] = self.options.screen_flip_trap_weight.value
        trap_data[0xBC0088] = self.options.sticky_floor_trap_weight.value
        trap_data[0xBC0089] = self.options.sticky_hands_trap_weight.value
        trap_data[0xBC008A] = self.options.pixelate_trap_weight.value
        trap_data[0xBC008B] = self.options.spotlight_trap_weight.value
        trap_data[0xBC008C] = self.options.bullet_time_trap_weight.value
        trap_data[0xBC008D] = self.options.invisibility_trap_weight.value
        trap_data[0xBC008E] = self.options.empty_item_box_trap_weight.value

        return trap_data
    
    @staticmethod
    def interpret_slot_data(slot_data):
        # Thesse are meant to be a Dict[int, int], not Dict[str, int]
        local_active_levels = dict()
        for x, y in slot_data["active_levels"].items():
            local_active_levels[int(x)] = y
        slot_data["active_levels"] = local_active_levels

        return slot_data
