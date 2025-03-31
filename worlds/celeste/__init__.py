from copy import deepcopy
import math
from typing import Dict, List, Set

from BaseClasses import ItemClassification, Location, MultiWorld, Region, Tutorial
from Utils import visualize_regions
from worlds.AutoWorld import WebWorld, World

from .Items import CelesteItem, generate_item_table, generate_item_data_table, level_item_lists, trap_item_data_table
from .Locations import CelesteLocation, generate_location_table, checkpoint_location_data_table
from .Names import ItemName, LocationName
from .Options import CelesteOptions, celeste_option_groups, resolve_options
from .Levels import Level, load_logic_data


class CelesteWebWorld(WebWorld):
    theme = "ice"

    setup_en = Tutorial(
        tutorial_name="Start Guide",
        description="A guide to playing Celeste in Archipelago.",
        language="English",
        file_name="guide_en.md",
        link="guide/en",
        authors=["PoryGone"]
    )

    tutorials = [setup_en]

    option_groups = celeste_option_groups


class CelesteWorld(World):
    """TBD"""

    # Class Data
    game = "Celeste"
    web = CelesteWebWorld()
    options_dataclass = CelesteOptions
    options: CelesteOptions
    level_data: Dict[str, Level] = load_logic_data()
    location_name_to_id = generate_location_table(level_data)
    item_name_to_id = generate_item_table()


    # Instance Data
    madeline_one_dash_hair_color: int
    madeline_two_dash_hair_color: int
    madeline_no_dash_hair_color: int
    madeline_feather_hair_color: int

    active_levels: Set[str]
    active_items: Set[str]


    @classmethod
    def stage_assert_generate(cls, _multiworld: MultiWorld) -> None:
        with open("./worlds/celeste/data/IDs.txt", "w") as f:
            print("Items:", file=f)
            for name in sorted(CelesteWorld.item_name_to_id, key=CelesteWorld.item_name_to_id.get):
                id = CelesteWorld.item_name_to_id[name]
                print(f"{{ 0x{id:X}, \"{name}\" }},", file=f)
            print("\nLocations:", file=f)
            for name in sorted(CelesteWorld.location_name_to_id, key=CelesteWorld.location_name_to_id.get):
                id = CelesteWorld.location_name_to_id[name]
                print(f"{{ 0x{id:X}, \"{name}\" }},", file=f)
            print("\nLocations 2:", file=f)
            for name in sorted(CelesteWorld.location_name_to_id, key=CelesteWorld.location_name_to_id.get):
                id = CelesteWorld.location_name_to_id[name]
                print(f"{{ \"{name}\", 0x{id:X} }},", file=f)

    def generate_early(self) -> None:
        if not self.player_name.isascii():
            raise RuntimeError(f"Invalid player_name {self.player_name} for game {self.game}. Name must be ascii.")

        resolve_options(self)

        self.active_levels = {"0a", "1a", "2a", "3a", "4a", "5a"}
        #self.active_levels = {"0a", "1a", "2a", "3a", "4a", "5a", "6a", "7a", "8a"}
        if self.options.include_core:
            self.active_levels.add("9a")
        if self.options.include_farewell:
            self.active_levels.add("10a")
            self.active_levels.add("10b")
        if self.options.include_b_sides:
            self.active_levels.update({"1b", "2b", "3b", "4b", "5b", "6b", "7b"})
            if self.options.include_core:
                self.active_levels.add("9b")
        if self.options.include_c_sides:
            self.active_levels.update({"1c", "2c", "3c", "4c", "5c", "6c", "7c"})
            if self.options.include_core:
                self.active_levels.add("9c")

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
        item_pool: List[CelesteItem] = []

        location_count: int = len(self.get_locations())

        if self.options.checkpointsanity:
            item_pool += [self.create_item(item_name) for item_name in self.active_checkpoint_names]
        else:
            for item_name in self.active_checkpoint_names:
                checkpoint_loc: Location = self.multiworld.get_location(item_name, self.player)
                checkpoint_loc.place_locked_item(self.create_item(item_name))
                location_count -= 1

        if self.options.keysanity:
            item_pool += [self.create_item(item_name) for item_name in self.active_key_names]
        else:
            for item_name in self.active_key_names:
                key_loc: Location = self.multiworld.get_location(item_name, self.player)
                key_loc.place_locked_item(self.create_item(item_name))
                location_count -= 1

        for item_name in self.active_clutter_names:
            clutter_loc: Location = self.multiworld.get_location(item_name, self.player)
            clutter_loc.place_locked_item(self.create_item(item_name))
            location_count -= 1

        item_pool += [self.create_item(item_name) for item_name in sorted(self.active_items)]

        real_total_strawberries: int = min(self.options.total_strawberries.value, location_count - len(item_pool))
        self.strawberries_required = int(real_total_strawberries * (self.options.strawberries_required_percentage / 100))

        item_pool += [self.create_item(ItemName.strawberry) for _ in range(self.strawberries_required)]

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
        from .Rules import set_rules
        set_rules(self)

    #def generate_output(self, output_directory: str):
    #    visualize_regions(self.multiworld.get_region("Menu", self.player), f"Player{self.player}.puml", show_entrance_names=False,
    #                  regions_to_highlight=self.multiworld.get_all_state(self.player).reachable_regions[self.player])

    # TODO: More Options
    def fill_slot_data(self):
        return {
            "death_link": self.options.death_link.value,
            "death_link_amnesty": self.options.death_link_amnesty.value,
            "trap_link": self.options.trap_link.value,
            "strawberries_required": self.strawberries_required,

            "checkpointsanity": self.options.checkpointsanity.value,
            "binosanity": self.options.binosanity.value,
            "keysanity": self.options.keysanity.value,
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
        }

    def output_active_traps(self) -> Dict[int, int]:
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
