import logging
from typing import Any

from Options import Toggle
from worlds.AutoWorld import World, WebWorld
from BaseClasses import Tutorial, Item, MultiWorld
from .options import PeaksOfYoreOptions, Goal, StartingBook, RopeUnlockMode, poy_option_groups
from . import options
from .data import full_item_list, full_location_list, PeaksOfYoreRegion
from .locations import get_locations, get_location_names_by_type, PeaksOfYoreLocation
from .regions import create_poy_regions, RegionLocationInfo


class PeaksOfYoreItem(Item):
    game = "Peaks of Yore"


class PeaksOfWeb(WebWorld):
    rich_text_options_doc = True
    theme = "stone"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Peaks of Yore Mod.",
        "English",
        "setup_en.md",
        "setup/en",
        ["c0der23"]
    )]
    option_groups = poy_option_groups


class PeaksOfWorld(World):
    """
    Peaks of Yore is a first-person physics-based "climb-em-up" adventure set in 1887.
    Steel your nerves and perfect your climbing skills as you ascend the rock wall, traverse difficult routes,
    and encounter many challenges and obstacles.
    """
    game = "Peaks of Yore"
    options_dataclass = PeaksOfYoreOptions
    options: PeaksOfYoreOptions
    web = PeaksOfWeb()
    item_name_to_id = {item.name: item.id for item in full_item_list}
    location_name_to_id = {location.name: location.id for location in full_location_list}
    topology_present = True
    artefacts_peaks_in_pool: RegionLocationInfo

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)

    def create_item(self, name: str) -> Item:
        item_entry = [item for item in full_item_list if item.name == name][0]
        return PeaksOfYoreItem(name, item_entry.classification, self.item_name_to_id[name], self.player)

    def get_filler_item_name(self) -> str:
        choices = ["Extra Rope", "Extra Coffee", "Extra Chalk", "Extra Seed"]
        return self.random.choice(choices)

    def generate_early(self) -> None:
        if self.options.start_with_barometer:
            self.options.start_inventory_from_pool.value.update({"Barometer": 1})

        if self.options.start_with_oil_lamp:
            self.options.start_inventory_from_pool.value.update({"Oil Lamp": 1})

        starting_book_options: dict[str, Toggle] = {
            "Fundamentals Book": self.options.enable_fundamental,
            "Intermediate Book": self.options.enable_intermediate,
            "Advanced Book": self.options.enable_advanced,
            "Expert Book": self.options.enable_expert,
            "Random": None
        }

        book_names: list[str] = [s for s, t in starting_book_options.items()]
        enabled_books: list[str] = [b for b, v in starting_book_options.items() if b != "Random" and v.value]
        start_book: str = ""

        if len(enabled_books) == 0:
            logging.error("Player " + self.player_name + " has not selected any books!")
            raise Exception("Player " + self.player_name + " has not selected any books!")

        if self.options.starting_book.value == StartingBook.option_random_book:
            start_book = self.random.choice(enabled_books)
        else:
            start_book = book_names[self.options.starting_book.value]

        if start_book not in enabled_books:
            logging.warning("book " + start_book + "not enabled")
            start_book = enabled_books[0]
            logging.warning("selecting " + start_book)

        self.options.starting_book.value = book_names.index(start_book)
        if self.options.starting_book.value == StartingBook.option_expert:
            self.options.start_inventory_from_pool.value.update({"Progressive Crampons": 1})
            # make sure player gets at least 6pt crampons before expert books
        self.options.start_inventory_from_pool.value.update({start_book: 1})

    def create_regions(self) -> None:
        self.artefacts_peaks_in_pool = create_poy_regions(self, self.options)

    def create_items(self) -> None:
        # order: books, tools, ropes, bird seeds, artefacts, fill rest with extra Items

        books: dict[str, Toggle] = {
            "Fundamentals Book": self.options.enable_fundamental,
            "Intermediate Book": self.options.enable_intermediate,
            "Advanced Book": self.options.enable_advanced,
            "Expert Book": self.options.enable_expert
        }

        starting_book: Item = self.create_item([*books][self.options.starting_book.value])

        remaining_items: int = len(self.multiworld.get_unfilled_locations(self.player))

        for name, option in books.items():
            if (not option) or remaining_items <= 0:
                continue
            self.multiworld.itempool.append(self.create_item(name))
            remaining_items -= 1

        for tool in [item for item in full_item_list if item.type == "Tool"]:
            if remaining_items > 0:
                if tool.name == "Progressive Crampons":
                    self.multiworld.itempool.append(self.create_item(tool.name))
                    self.multiworld.itempool.append(self.create_item(tool.name))
                    remaining_items -= 2
                elif tool.name == "Rope Unlock":
                    if self.options.rope_unlock_mode == RopeUnlockMode.option_early:
                        self.multiworld.early_items[self.player][tool.name] = 1
                        self.multiworld.itempool.append(self.create_item(tool.name))
                        remaining_items -= 1
                    elif self.options.rope_unlock_mode == RopeUnlockMode.option_normal:
                        self.multiworld.itempool.append(self.create_item(tool.name))
                        remaining_items -= 1
                        # else don't place rope unlock as it will be unlocked with any rope pick-up
                else:
                    self.multiworld.itempool.append(self.create_item(tool.name))
                    remaining_items -= 1

        for rope in [item for item in full_item_list if item.type == "Rope"]:
            if remaining_items > 0:
                self.multiworld.itempool.append(self.create_item(rope.name))
                remaining_items -= 1

        for birdSeed in [item for item in full_item_list if item.type == "Bird Seed"]:
            if remaining_items > 0:
                self.multiworld.itempool.append(self.create_item(birdSeed.name))
                remaining_items -= 1

        for artefact in [item for item in full_item_list if item.type == "Artefact"]:
            if remaining_items > 0:
                self.multiworld.itempool.append(self.create_item(artefact.name))
                remaining_items -= 1

        self.multiworld.itempool += [self.create_item(self.get_filler_item_name()) for _ in range(remaining_items)]

    def set_rules(self) -> None:
        if self.options.goal.value == Goal.option_all_artefacts:
            self.multiworld.completion_condition[self.player] = lambda state: all(
                state.can_reach_location(artefact, self.player) for artefact in
                self.artefacts_peaks_in_pool.artefacts_in_pool)

        if self.options.goal.value == Goal.option_all_peaks:
            self.multiworld.completion_condition[self.player] = lambda state: all(
                state.can_reach_location(peak, self.player) for peak in self.artefacts_peaks_in_pool.peaks_in_pool)

        if self.options.goal.value == Goal.option_all_peaks:
            self.multiworld.completion_condition[self.player] = lambda state: all(
                state.can_reach_location(loc, self.player) for loc in [*self.artefacts_peaks_in_pool.peaks_in_pool,
                                                                       *self.artefacts_peaks_in_pool.artefacts_in_pool])

        if self.options.goal.value == Goal.option_all:
            self.multiworld.completion_condition[self.player] = lambda state: all(
                state.can_reach_location(loc.name, self.player) for loc in self.get_locations())

    def fill_slot_data(self) -> dict[str, Any]:
        return self.options.as_dict("death_link", "goal", "rope_unlock_mode", casing="camel")
