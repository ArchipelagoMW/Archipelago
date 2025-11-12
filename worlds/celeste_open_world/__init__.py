from copy import deepcopy
import math
from typing import TextIO

from BaseClasses import ItemClassification, Location, MultiWorld, Region, Tutorial
from Utils import visualize_regions
from worlds.AutoWorld import WebWorld, World

from .Items import CelesteItem, generate_item_table, generate_item_data_table, generate_item_groups, level_item_lists, level_cassette_items,\
                                cassette_item_data_table, crystal_heart_item_data_table, trap_item_data_table
from .Locations import CelesteLocation, location_data_table, generate_location_groups, checkpoint_location_data_table, location_id_offsets
from .Names import ItemName
from .Options import CelesteOptions, celeste_option_groups, resolve_options
from .Levels import Level, LocationType, load_logic_data, goal_area_option_to_name, goal_area_option_to_display_name, goal_area_to_location_name


class CelesteOpenWebWorld(WebWorld):
    theme = "ice"

    setup_en = Tutorial(
        tutorial_name="Start Guide",
        description="A guide to playing Celeste (Open World) in Archipelago.",
        language="English",
        file_name="guide_en.md",
        link="guide/en",
        authors=["PoryGone"]
    )

    tutorials = [setup_en]

    option_groups = celeste_option_groups


class CelesteOpenWorld(World):
    """
    Celeste (Open World) is a randomizer for the original Celeste. In this acclaimed platformer created by ExOK Games, you control Madeline as she attempts to climb the titular mountain, meeting friends and obstacles along the way.  Progression is found in unlocking the ability to interact with various objects in the areas, such as springs, traffic blocks, feathers, and many more. Please be safe on the climb.
    """

    # Class Data
    game = "Celeste (Open World)"
    web = CelesteOpenWebWorld()
    options_dataclass = CelesteOptions
    options: CelesteOptions

    apworld_version = 10005

    level_data: dict[str, Level] = load_logic_data()

    location_name_to_id: dict[str, int] = location_data_table
    location_name_groups: dict[str, list[str]] = generate_location_groups()
    item_name_to_id: dict[str, int] = generate_item_table()
    item_name_groups: dict[str, list[str]] = generate_item_groups()


    # Instance Data
    madeline_one_dash_hair_color: int
    madeline_two_dash_hair_color: int
    madeline_no_dash_hair_color: int
    madeline_feather_hair_color: int

    active_levels: set[str]
    active_items: set[str]


    def generate_early(self) -> None:
        if not self.player_name.isascii():
            raise RuntimeError(f"Invalid player_name {self.player_name} for game {self.game}. Name must be ascii.")

        resolve_options(self)

        self.goal_area: str = goal_area_option_to_name[self.options.goal_area.value]

        self.active_levels = {"0a", "1a", "2a", "3a", "4a", "5a", "6a", "7a", "8a"}
        if self.options.include_core:
            self.active_levels.add("9a")
        if self.options.include_farewell >= 1:
            self.active_levels.add("10a")
        if self.options.include_farewell == 2:
            self.active_levels.add("10b")
        if self.options.include_b_sides:
            self.active_levels.update({"1b", "2b", "3b", "4b", "5b", "6b", "7b"})
            if self.options.include_core:
                self.active_levels.add("9b")
        if self.options.include_c_sides:
            self.active_levels.update({"1c", "2c", "3c", "4c", "5c", "6c", "7c"})
            if self.options.include_core:
                self.active_levels.add("9c")

        self.active_levels.add(self.goal_area)
        if self.goal_area == "10c":
            self.active_levels.add("10a")
            self.active_levels.add("10b")
        elif self.goal_area == "10b":
            self.active_levels.add("10a")

        self.active_items = set()
        for level in self.active_levels:
            self.active_items.update(level_item_lists[level])


    def create_regions(self) -> None:
        from .Locations import create_regions_and_locations

        create_regions_and_locations(self)


    def create_item(self, name: str, force_useful: bool = False) -> CelesteItem:
        item_data_table = generate_item_data_table()

        if name == ItemName.strawberry and force_useful:
            return CelesteItem(name, ItemClassification.useful, item_data_table[name].code, self.player)
        elif name in item_data_table:
            return CelesteItem(name, item_data_table[name].type, item_data_table[name].code, self.player)
        else:
            return CelesteItem(name, ItemClassification.progression, None, self.player)

    def create_items(self) -> None:
        item_pool: list[CelesteItem] = []

        location_count: int = len(self.get_locations())
        goal_area_location_count: int = sum(goal_area_option_to_display_name[self.options.goal_area] in loc.name for loc in self.get_locations())

        # Goal Items
        goal_item_loc: Location = self.get_location(goal_area_to_location_name[self.goal_area])
        goal_item_loc.place_locked_item(self.create_item(ItemName.house_keys))
        location_count -= 1

        epilogue_region: Region = self.get_region(self.epilogue_start_region)
        epilogue_region.add_locations({ItemName.victory: None }, CelesteLocation)
        victory_loc: Location = self.get_location(ItemName.victory)
        victory_loc.place_locked_item(self.create_item(ItemName.victory))

        # Checkpoints
        for item_name in self.active_checkpoint_names:
            if self.options.checkpointsanity:
                if not self.options.goal_area_checkpointsanity and goal_area_option_to_display_name[self.options.goal_area] in item_name:
                    checkpoint_loc: Location = self.get_location(item_name)
                    checkpoint_loc.place_locked_item(self.create_item(item_name))
                    location_count -= 1
                else:
                    item_pool.append(self.create_item(item_name))
            else:
                checkpoint_loc: Location = self.get_location(item_name)
                checkpoint_loc.place_locked_item(self.create_item(item_name))
                location_count -= 1

        # Keys
        if self.options.keysanity:
            item_pool += [self.create_item(item_name) for item_name in self.active_key_names]
        else:
            for item_name in self.active_key_names:
                key_loc: Location = self.get_location(item_name)
                key_loc.place_locked_item(self.create_item(item_name))
                location_count -= 1

        # Summit Gems
        if self.options.gemsanity:
            item_pool += [self.create_item(item_name) for item_name in self.active_gem_names]
        else:
            for item_name in self.active_gem_names:
                gem_loc: Location = self.get_location(item_name)
                gem_loc.place_locked_item(self.create_item(item_name))
                location_count -= 1

        # Clutter Events
        for item_name in self.active_clutter_names:
            clutter_loc: Location = self.get_location(item_name)
            clutter_loc.place_locked_item(self.create_item(item_name))
            location_count -= 1

        # Interactables
        item_pool += [self.create_item(item_name) for item_name in sorted(self.active_items)]

        # Strawberries
        real_total_strawberries: int = min(self.options.total_strawberries.value, location_count - goal_area_location_count - len(item_pool))
        self.strawberries_required = int(real_total_strawberries * (self.options.strawberries_required_percentage / 100))

        menu_region = self.get_region("Menu")
        if getattr(self, "goal_start_region", None):
            menu_region.add_exits([self.goal_start_region], {self.goal_start_region: lambda state: state.has(ItemName.strawberry, self.player, self.strawberries_required)})
        if getattr(self, "goal_checkpoint_names", None):
            for region_name, location_name in self.goal_checkpoint_names.items():
                checkpoint_rule = lambda state, location_name=location_name: state.has(location_name, self.player) and state.has(ItemName.strawberry, self.player, self.strawberries_required)
                menu_region.add_exits([region_name], {region_name: checkpoint_rule})

        menu_region.add_exits([self.epilogue_start_region], {self.epilogue_start_region: lambda state: (state.has(ItemName.strawberry, self.player, self.strawberries_required) and state.has(ItemName.house_keys, self.player))})

        item_pool += [self.create_item(ItemName.strawberry) for _ in range(self.strawberries_required)]

        # Filler and Traps
        non_required_strawberries = (real_total_strawberries - self.strawberries_required)
        replacement_filler_count = math.floor(non_required_strawberries * (self.options.junk_fill_percentage.value / 100.0))
        remaining_extra_strawberries = non_required_strawberries - replacement_filler_count
        item_pool += [self.create_item(ItemName.strawberry, True) for _ in range(remaining_extra_strawberries)]

        trap_weights = []
        trap_weights += ([ItemName.bald_trap] * self.options.bald_trap_weight.value)
        trap_weights += ([ItemName.literature_trap] * self.options.literature_trap_weight.value)
        trap_weights += ([ItemName.stun_trap] * self.options.stun_trap_weight.value)
        trap_weights += ([ItemName.invisible_trap] * self.options.invisible_trap_weight.value)
        trap_weights += ([ItemName.fast_trap] * self.options.fast_trap_weight.value)
        trap_weights += ([ItemName.slow_trap] * self.options.slow_trap_weight.value)
        trap_weights += ([ItemName.ice_trap] * self.options.ice_trap_weight.value)
        trap_weights += ([ItemName.reverse_trap] * self.options.reverse_trap_weight.value)
        trap_weights += ([ItemName.screen_flip_trap] * self.options.screen_flip_trap_weight.value)
        trap_weights += ([ItemName.laughter_trap] * self.options.laughter_trap_weight.value)
        trap_weights += ([ItemName.hiccup_trap] * self.options.hiccup_trap_weight.value)
        trap_weights += ([ItemName.zoom_trap] * self.options.zoom_trap_weight.value)

        total_filler_count: int = (location_count - len(item_pool))

        # Cassettes
        if self.options.require_cassettes:
            shuffled_active_levels = sorted(self.active_levels)
            self.random.shuffle(shuffled_active_levels)
            for level_name in shuffled_active_levels:
                if level_name == "10b" or level_name == "10c":
                    continue
                if level_name not in self.multiworld.precollected_items[self.player]:
                    if total_filler_count > 0:
                        item_pool.append(self.create_item(level_cassette_items[level_name]))
                        total_filler_count -= 1
                    else:
                        self.multiworld.push_precollected(self.create_item(level_cassette_items[level_name]))

        # Crystal Hearts
        for name in crystal_heart_item_data_table.keys():
            if total_filler_count > 0:
                if name not in self.multiworld.precollected_items[self.player]:
                    item_pool.append(self.create_item(name))
                    total_filler_count -= 1

        trap_count = 0 if (len(trap_weights) == 0) else math.ceil(total_filler_count * (self.options.trap_fill_percentage.value / 100.0))
        total_filler_count -= trap_count

        item_pool += [self.create_item(ItemName.raspberry) for _ in range(total_filler_count)]

        trap_pool = []
        for i in range(trap_count):
            trap_item = self.random.choice(trap_weights)
            trap_pool.append(self.create_item(trap_item))

        item_pool += trap_pool

        self.multiworld.itempool += item_pool

    def get_filler_item_name(self) -> str:
        return ItemName.raspberry


    def set_rules(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: state.has(ItemName.victory, self.player)


    def fill_slot_data(self):
        return {
            "apworld_version": self.apworld_version,
            "min_mod_version": 10000,

            "death_link": self.options.death_link.value,
            "death_link_amnesty": self.options.death_link_amnesty.value,
            "trap_link": self.options.trap_link.value,

            "active_levels": self.active_levels,
            "goal_area": self.goal_area,
            "lock_goal_area": self.options.lock_goal_area.value,
            "strawberries_required": self.strawberries_required,

            "checkpointsanity": self.options.checkpointsanity.value,
            "binosanity": self.options.binosanity.value,
            "keysanity": self.options.keysanity.value,
            "gemsanity": self.options.gemsanity.value,
            "carsanity": self.options.carsanity.value,
            "roomsanity": self.options.roomsanity.value,
            "include_goldens": self.options.include_goldens.value,

            "include_core": self.options.include_core.value,
            "include_farewell": self.options.include_farewell.value,
            "include_b_sides": self.options.include_b_sides.value,
            "include_c_sides": self.options.include_c_sides.value,

            "trap_expiration_action": self.options.trap_expiration_action.value,
            "trap_expiration_amount": self.options.trap_expiration_amount.value,
            "active_traps": self.output_active_traps(),

            "madeline_hair_length": self.options.madeline_hair_length.value,
            "madeline_one_dash_hair_color": self.madeline_one_dash_hair_color,
            "madeline_two_dash_hair_color": self.madeline_two_dash_hair_color,
            "madeline_no_dash_hair_color": self.madeline_no_dash_hair_color,
            "madeline_feather_hair_color": self.madeline_feather_hair_color,

            "music_shuffle": self.options.music_shuffle.value,
            "music_map": self.generate_music_data(),
            "require_cassettes": self.options.require_cassettes.value,
            "chosen_poem": self.random.randint(0, 119),
        }

    @classmethod
    def stage_write_spoiler_header(cls, multiworld: MultiWorld, spoiler_handle: TextIO):
        major: int = cls.apworld_version // 10000
        minor: int = (cls.apworld_version % 10000) // 100
        bugfix: int = (cls.apworld_version % 100)
        spoiler_handle.write(f"\nCeleste (Open World) APWorld v{major}.{minor}.{bugfix}\n")

    def output_active_traps(self) -> dict[int, int]:
        trap_data = {}

        trap_data[0x20] = self.options.bald_trap_weight.value
        trap_data[0x21] = self.options.literature_trap_weight.value
        trap_data[0x22] = self.options.stun_trap_weight.value
        trap_data[0x23] = self.options.invisible_trap_weight.value
        trap_data[0x24] = self.options.fast_trap_weight.value
        trap_data[0x25] = self.options.slow_trap_weight.value
        trap_data[0x26] = self.options.ice_trap_weight.value
        trap_data[0x28] = self.options.reverse_trap_weight.value
        trap_data[0x29] = self.options.screen_flip_trap_weight.value
        trap_data[0x2A] = self.options.laughter_trap_weight.value
        trap_data[0x2B] = self.options.hiccup_trap_weight.value
        trap_data[0x2C] = self.options.zoom_trap_weight.value

        return trap_data

    def generate_music_data(self) -> dict[int, int]:
        if self.options.music_shuffle == "consistent":
            musiclist_o = list(range(0, 48))
            musiclist_s = musiclist_o.copy()
            self.random.shuffle(musiclist_s)

            return dict(zip(musiclist_o, musiclist_s))
        elif self.options.music_shuffle == "singularity":
            musiclist_o = list(range(0, 48))
            musiclist_s = [self.random.choice(musiclist_o)] * len(musiclist_o)

            return dict(zip(musiclist_o, musiclist_s))
        else:
            musiclist_o = list(range(0, 48))
            musiclist_s = musiclist_o.copy()

            return dict(zip(musiclist_o, musiclist_s))


    # Useful Debugging tools, kept around for later.
    #@classmethod
    #def stage_assert_generate(cls, _multiworld: MultiWorld) -> None:
    #    with open("./worlds/celeste_open_world/data/IDs.txt", "w") as f:
    #        print("Items:", file=f)
    #        for name in sorted(CelesteOpenWorld.item_name_to_id, key=CelesteOpenWorld.item_name_to_id.get):
    #            id = CelesteOpenWorld.item_name_to_id[name]
    #            print(f"{{ 0x{id:X}, \"{name}\" }},", file=f)
    #        print("\nLocations:", file=f)
    #        for name in sorted(CelesteOpenWorld.location_name_to_id, key=CelesteOpenWorld.location_name_to_id.get):
    #            id = CelesteOpenWorld.location_name_to_id[name]
    #            print(f"{{ 0x{id:X}, \"{name}\" }},", file=f)
    #        print("\nLocations 2:", file=f)
    #        for name in sorted(CelesteOpenWorld.location_name_to_id, key=CelesteOpenWorld.location_name_to_id.get):
    #            id = CelesteOpenWorld.location_name_to_id[name]
    #            print(f"{{ \"{name}\", 0x{id:X} }},", file=f)
    #
    #def generate_output(self, output_directory: str):
    #    visualize_regions(self.get_region("Menu"), f"Player{self.player}.puml", show_entrance_names=False,
    #                  regions_to_highlight=self.multiworld.get_all_state(self.player).reachable_regions[self.player])
