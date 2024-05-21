from copy import deepcopy
from typing import Dict, List

from BaseClasses import ItemClassification, Location, Region, Tutorial
from worlds.AutoWorld import WebWorld, World
from .Items import Celeste64Item, unlockable_item_data_table, move_item_data_table, item_data_table, item_table
from .Locations import Celeste64Location, strawberry_location_data_table, friend_location_data_table,\
                                          sign_location_data_table, car_location_data_table, location_table
from .Names import ItemName, LocationName
from .Options import Celeste64Options, celeste_64_option_groups


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
    goal_logic_mapping: Dict[str, List[List[str]]]


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

        if self.options.move_shuffle:
            move_items_for_itempool: List[str] = deepcopy(list(move_item_data_table.keys()))

            if self.options.logic_difficulty == "standard":
                # If the start_inventory already includes a move, don't worry about giving it one
                if not [move for move in move_items_for_itempool if move in self.options.start_inventory]:
                    chosen_start_move = self.random.choice(move_items_for_itempool)
                    move_items_for_itempool.remove(chosen_start_move)

                    if self.options.carsanity:
                        intro_car_loc: Location = self.multiworld.get_location(LocationName.car_1, self.player)
                        intro_car_loc.place_locked_item(self.create_item(chosen_start_move))
                        location_count -= 1
                    else:
                        self.multiworld.push_precollected(self.create_item(chosen_start_move))

            item_pool += [self.create_item(name)
                          for name in move_items_for_itempool
                          if name not in self.options.start_inventory]

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

            region.add_exits(region_data_table[region_name].connecting_regions)


    def get_filler_item_name(self) -> str:
        return ItemName.raspberry


    def set_rules(self) -> None:
        from .Rules import set_rules
        set_rules(self)


    def fill_slot_data(self):
        return {
            "death_link": self.options.death_link.value,
            "death_link_amnesty": self.options.death_link_amnesty.value,
            "strawberries_required": self.strawberries_required,
            "move_shuffle": self.options.move_shuffle.value,
            "friendsanity": self.options.friendsanity.value,
            "signsanity": self.options.signsanity.value,
            "carsanity": self.options.carsanity.value,
            "badeline_chaser_source": self.options.badeline_chaser_source.value,
            "badeline_chaser_frequency": self.options.badeline_chaser_frequency.value,
            "badeline_chaser_speed": self.options.badeline_chaser_speed.value,
        }
