import logging
from typing import Any

from Options import Toggle, OptionError
from worlds.AutoWorld import World, WebWorld
from BaseClasses import Tutorial, Item
from .options import PeaksOfYoreOptions, Goal, StartingBook, RopeUnlockMode, StartingHands, poy_option_groups
from .data import *

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
    item_name_to_id = {item.name: item.id for item in full_item_table.values()}
    location_name_to_id = {location.name: location.id for location in full_location_table.values()}
    topology_present = True
    artefacts_peaks_in_pool: RegionLocationInfo

    def create_item(self, name: str) -> Item:
        item_entry = full_item_table[name]
        return PeaksOfYoreItem(name, item_entry.classification, self.item_name_to_id[name], self.player)

    def get_filler_item_name(self) -> str:
        choices = ("Extra Rope", "Extra Coffee", "Extra Chalk", "Extra Seed")
        return self.random.choice(choices)

    def generate_early(self) -> None:
        if self.options.start_with_barometer:
            self.multiworld.push_precollected(self.create_item("Barometer"))

        if self.options.start_with_oil_lamp:
            self.multiworld.push_precollected(self.create_item("Oil Lamp"))

        if self.options.start_with_hands.value == 0:
            self.multiworld.push_precollected(self.create_item("Right Hand"))
            self.multiworld.push_precollected(self.create_item("Left Hand"))
        elif self.options.start_with_hands.value == 1:
            self.multiworld.push_precollected(self.create_item("Left Hand"))
        else:
            self.multiworld.push_precollected(self.create_item("Right Hand"))

        starting_book_options: dict[str, Toggle] = {
            "Fundamentals Book": self.options.enable_fundamental,
            "Intermediate Book": self.options.enable_intermediate,
            "Advanced Book": self.options.enable_advanced,
            "Expert Book": self.options.enable_expert,
        }

        book_names: list[str] = list(starting_book_options)
        enabled_books: list[str] = [b for b, v in starting_book_options.items() if v]
        start_book: str = self.options.starting_book.get_selected_book()

        if not enabled_books:
            # enabled_books.append("Fundamentals Book")
            # self.options.enable_fundamental.value = True
            # self.options.starting_book.value = StartingBook.option_fundamentals
            logging.error("Player " + self.player_name + " has not selected any books!")
            raise OptionError("Player " + self.player_name + " has not selected any books!")

        if start_book not in enabled_books:
            logging.warning(start_book)
            logging.warning(enabled_books)
            logging.warning("book " + start_book + " not enabled, selecting random book")
            start_book = self.random.choice(enabled_books)
            logging.warning("selected book: " + start_book)

        self.options.starting_book.value = book_names.index(start_book)
        if self.options.starting_book.value == StartingBook.option_expert:
            self.multiworld.push_precollected(self.create_item("Progressive Crampons"))
            # make sure player gets at least 6pt crampons before expert books
        self.multiworld.push_precollected(self.create_item(start_book))

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

        starting_book: Item = self.create_item(self.options.starting_book.get_selected_book())

        remaining_items: int = len(self.multiworld.get_unfilled_locations(self.player))

        local_itempool: list[Item] = []

        for name, option in books.items():
            if (not option) or name == starting_book.name:
                continue
            local_itempool.append(self.create_item(name))

        for tool in get_all_items_or_locations(tools_list):
            if (tool.name != "Barometer" or not self.options.start_with_barometer) \
                    and (tool.name != "Oil Lamp" or not self.options.start_with_oil_lamp):
                if tool.name == "Progressive Crampons":
                    local_itempool.append(self.create_item(tool.name))

                    if self.options.starting_book.value != StartingBook.option_expert:
                        local_itempool.append(self.create_item(tool.name))

                elif tool.name == "Rope Unlock":
                    if self.options.rope_unlock_mode == RopeUnlockMode.option_early:
                        self.multiworld.early_items[self.player][tool.name] = 1
                        local_itempool.append(self.create_item(tool.name))

                    elif self.options.rope_unlock_mode == RopeUnlockMode.option_normal:
                        local_itempool.append(self.create_item(tool.name))
                        # else don't place rope unlock as it will be unlocked with any rope pick-up
                elif tool.name == "Left Hand":
                    if self.options.start_with_hands.value == StartingHands.option_right:
                        local_itempool.append(self.create_item(tool.name))
                        if self.options.early_hands:
                            self.multiworld.early_items[self.player][tool.name] = 1
                elif tool.name == "Right Hand":
                    if self.options.start_with_hands.value == StartingHands.option_left:
                        local_itempool.append(self.create_item(tool.name))
                        if self.options.early_hands:
                            self.multiworld.early_items[self.player][tool.name] = 1
                else:
                    local_itempool.append(self.create_item(tool.name))

        for rope in get_all_items_or_locations(ropes_list):
            local_itempool.append(self.create_item(rope.name))

        for birdSeed in get_all_items_or_locations(bird_seeds_list):
            local_itempool.append(self.create_item(birdSeed.name))

        for artefact in get_all_items_or_locations(artefacts_list):
            local_itempool.append(self.create_item(artefact.name))

        if len(local_itempool) < remaining_items:
            local_itempool += [self.create_filler() for _ in range(remaining_items - len(local_itempool))]

        self.multiworld.itempool += local_itempool[:remaining_items]

    def set_rules(self) -> None:
        if self.options.goal.value == Goal.option_all_artefacts:
            self.multiworld.completion_condition[self.player] = lambda state: all(
                state.can_reach_location(artefact, self.player) for artefact in
                self.artefacts_peaks_in_pool.artefacts_in_pool)

        elif self.options.goal.value == Goal.option_all_peaks:
            self.multiworld.completion_condition[self.player] = lambda state: all(
                state.can_reach_location(peak, self.player) for peak in self.artefacts_peaks_in_pool.peaks_in_pool)

        elif self.options.goal.value == Goal.option_all_artefacts_all_peaks:
            self.multiworld.completion_condition[self.player] = lambda state: all(
                state.can_reach_location(loc, self.player) for loc in [*self.artefacts_peaks_in_pool.peaks_in_pool,
                                                                       *self.artefacts_peaks_in_pool.artefacts_in_pool])

        elif self.options.goal.value == Goal.option_all:
            self.multiworld.completion_condition[self.player] = lambda state: all(
                state.can_reach_location(loc.name, self.player) for loc in self.multiworld.get_locations(self.player))

    def fill_slot_data(self) -> dict[str, Any]:
        return self.options.as_dict("death_link", "goal", "rope_unlock_mode", casing="camel")
