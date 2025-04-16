from copy import deepcopy
from typing import Dict, List, Tuple

from BaseClasses import ItemClassification, Location, Region, Tutorial
from worlds.AutoWorld import WebWorld, World
from .Items import Celeste64Item, unlockable_item_data_table, move_item_data_table, item_data_table,\
                                  checkpoint_item_data_table, item_table
from .Locations import Celeste64Location, strawberry_location_data_table, friend_location_data_table,\
                                          sign_location_data_table, car_location_data_table, checkpoint_location_data_table,\
                                          location_table
from .Names import ItemName, LocationName
from .Options import Celeste64Options, celeste_64_option_groups, resolve_options


class Celeste64WebWorld(WebWorld):
    theme = "ice"

    setup_en = Tutorial(
        tutorial_name="Start Guide",
        description="A guide to playing Celeste 64 in Archipelago.",
        language="English",
        file_name="guide_en.md",
        link="guide/en",
        authors=["PoryGone"]
    )

    tutorials = [setup_en]

    option_groups = celeste_64_option_groups


class Celeste64World(World):
    """Relive the magic of Celeste Mountain alongside Madeline in this small, heartfelt 3D platformer.
    Created in a week(ish) by the Celeste team to celebrate the game’s sixth anniversary 🍓✨"""

    # Class Data
    game = "Celeste 64"
    web = Celeste64WebWorld()
    options_dataclass = Celeste64Options
    options: Celeste64Options
    location_name_to_id = location_table
    item_name_to_id = item_table

    # Instance Data
    strawberries_required: int
    active_logic_mapping: Dict[str, List[List[str]]]
    active_region_logic_mapping: Dict[Tuple[str], List[List[str]]]

    madeline_one_dash_hair_color: int
    madeline_two_dash_hair_color: int
    madeline_no_dash_hair_color: int
    madeline_feather_hair_color: int

    def generate_early(self) -> None:
        resolve_options(self)

    def create_item(self, name: str) -> Celeste64Item:
        # Only make required amount of strawberries be Progression
        if getattr(self, "strawberries_required", None) and name == ItemName.strawberry:
            classification: ItemClassification = ItemClassification.filler
            self.prog_strawberries = getattr(self, "prog_strawberries", 0)
            if self.prog_strawberries < self.strawberries_required:
                classification = ItemClassification.progression_skip_balancing
                self.prog_strawberries += 1

            return Celeste64Item(name, classification, item_data_table[name].code, self.player)
        else:
            return Celeste64Item(name, item_data_table[name].type, item_data_table[name].code, self.player)

    def create_items(self) -> None:
        item_pool: List[Celeste64Item] = []

        location_count: int = 30

        if self.options.friendsanity:
            location_count += 9

        if self.options.signsanity:
            location_count += 5

        if self.options.carsanity:
            location_count += 2

        item_pool += [self.create_item(name)
                      for name in unlockable_item_data_table.keys()
                      if name not in self.options.start_inventory]

        chosen_start_item: str = ""

        if self.options.move_shuffle:
            if self.options.logic_difficulty == "standard":
                possible_unwalls: List[str] = [name for name in move_item_data_table.keys()
                                                if name != ItemName.skid_jump]

                if self.options.checkpointsanity:
                    possible_unwalls.extend([name for name in checkpoint_item_data_table.keys()
                                                if name != ItemName.checkpoint_1 and name != ItemName.checkpoint_10])

                # If the start_inventory already includes a move or checkpoint, don't worry about giving it one
                if not [item for item in possible_unwalls if item in self.multiworld.precollected_items[self.player]]:
                    chosen_start_item = self.random.choice(possible_unwalls)

                    if self.options.carsanity:
                        intro_car_loc: Location = self.multiworld.get_location(LocationName.car_1, self.player)
                        intro_car_loc.place_locked_item(self.create_item(chosen_start_item))
                        location_count -= 1
                    else:
                        self.multiworld.push_precollected(self.create_item(chosen_start_item))

            item_pool += [self.create_item(name)
                          for name in move_item_data_table.keys()
                          if name not in self.multiworld.precollected_items[self.player]
                          and name != chosen_start_item]
        else:
            for start_move in move_item_data_table.keys():
                self.multiworld.push_precollected(self.create_item(start_move))

        if self.options.checkpointsanity:
            location_count += 9
            goal_checkpoint_loc: Location = self.multiworld.get_location(LocationName.checkpoint_10, self.player)
            goal_checkpoint_loc.place_locked_item(self.create_item(ItemName.checkpoint_10))
            item_pool += [self.create_item(name)
                          for name in checkpoint_item_data_table.keys()
                          if name not in self.multiworld.precollected_items[self.player]
                          and name != ItemName.checkpoint_10
                          and name != chosen_start_item]
        else:
            for item_name in checkpoint_item_data_table.keys():
                checkpoint_loc: Location = self.multiworld.get_location(item_name, self.player)
                checkpoint_loc.place_locked_item(self.create_item(item_name))

        real_total_strawberries: int = min(self.options.total_strawberries.value, location_count - len(item_pool))
        self.strawberries_required = int(real_total_strawberries * (self.options.strawberries_required_percentage / 100))

        item_pool += [self.create_item(ItemName.strawberry) for _ in range(real_total_strawberries)]

        filler_item_count: int = location_count - len(item_pool)
        item_pool += [self.create_item(ItemName.raspberry) for _ in range(filler_item_count)]

        self.multiworld.itempool += item_pool


    def create_regions(self) -> None:
        from .Regions import region_data_table
        # Create regions.
        for region_name in region_data_table.keys():
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        # Create locations.
        for region_name, region_data in region_data_table.items():
            region = self.multiworld.get_region(region_name, self.player)
            region.add_locations({
                location_name: location_data.address for location_name, location_data in strawberry_location_data_table.items()
                if location_data.region == region_name
            }, Celeste64Location)

            if self.options.friendsanity:
                region.add_locations({
                    location_name: location_data.address for location_name, location_data in friend_location_data_table.items()
                    if location_data.region == region_name
                }, Celeste64Location)

            if self.options.signsanity:
                region.add_locations({
                    location_name: location_data.address for location_name, location_data in sign_location_data_table.items()
                    if location_data.region == region_name
                }, Celeste64Location)

            if self.options.carsanity:
                region.add_locations({
                    location_name: location_data.address for location_name, location_data in car_location_data_table.items()
                    if location_data.region == region_name
                }, Celeste64Location)

            region.add_locations({
                location_name: location_data.address for location_name, location_data in checkpoint_location_data_table.items()
                if location_data.region == region_name
            }, Celeste64Location)

            from .Rules import connect_region
            connect_region(self, region, region_data_table[region_name].connecting_regions)

        # Have to do this here because of other games using State in a way that's bad
        from .Rules import set_rules
        set_rules(self)


    def get_filler_item_name(self) -> str:
        return ItemName.raspberry


    def fill_slot_data(self):
        return {
            "death_link": self.options.death_link.value,
            "death_link_amnesty": self.options.death_link_amnesty.value,
            "strawberries_required": self.strawberries_required,
            "move_shuffle": self.options.move_shuffle.value,
            "friendsanity": self.options.friendsanity.value,
            "signsanity": self.options.signsanity.value,
            "carsanity": self.options.carsanity.value,
            "checkpointsanity": self.options.checkpointsanity.value,
            "madeline_one_dash_hair_color": self.madeline_one_dash_hair_color,
            "madeline_two_dash_hair_color": self.madeline_two_dash_hair_color,
            "madeline_no_dash_hair_color": self.madeline_no_dash_hair_color,
            "madeline_feather_hair_color": self.madeline_feather_hair_color,
            "badeline_chaser_source": self.options.badeline_chaser_source.value,
            "badeline_chaser_frequency": self.options.badeline_chaser_frequency.value,
            "badeline_chaser_speed": self.options.badeline_chaser_speed.value,
        }
