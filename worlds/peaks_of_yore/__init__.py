from typing import Any

from Options import Toggle
from worlds.AutoWorld import World, WebWorld
from BaseClasses import Tutorial, Item, Region, ItemClassification, MultiWorld
from .options import PeaksOfYoreOptions, Goal, StartingBook, RopeUnlockMode
from .data import full_item_list, full_location_list, PeaksOfYoreRegion
from .locations import get_locations, get_location_names_by_type, PeaksOfYoreLocation


class PeaksOfYoreItem(Item):
    game = "Peaks of Yore"


class PeaksOfWeb(WebWorld):
    theme = "stone"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Peaks of Yore Mod.",
        "English",
        "setup_en.md",
        "setup/en",
        ["c0der23"]
    )]


class PeaksOfWorld(World):
    """
    Peaks of Yore is a first-person physics-based "climb-em-up" adventure set in 1887.
    Steel your nerves and perfect your climbing skills as you ascend the rock wall, traverse difficult routes, and encounter many challenges and obstacles.
    """
    game = "Peaks of Yore"
    options_dataclass = PeaksOfYoreOptions
    options: PeaksOfYoreOptions
    web = PeaksOfWeb()
    item_name_to_id = {item.name: item.id for item in full_item_list}
    location_name_to_id = {location.name: location.id for location in full_location_list}
    topology_present = True
    location_count: int
    peaks_in_pool: list[str]
    artefacts_in_pool: list[str]

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.location_count = 0
        self.peaks_in_pool = []
        self.artefacts_in_pool = []

    def create_item(self, name: str) -> Item:
        classification: ItemClassification = ItemClassification.filler
        item_entry = [item for item in full_item_list if item.name == name][0]
        if item_entry.type in ["Book", "Tool"]:
            classification = ItemClassification.progression
        return PeaksOfYoreItem(name, classification, self.item_name_to_id[name], self.player)

    def get_filler_item_name(self) -> str:
        choices = ["Extra Rope", "Extra Coffee", "Extra Chalk", "Extra Seed"]
        return self.random.choice(choices)

    def generate_early(self) -> None:
        if self.options.start_with_barometer:
            self.multiworld.push_precollected(self.create_item("Barometer"))

        if (not self.options.enable_fundamental.value) and (not self.options.enable_intermediate.value) \
                and (not self.options.enable_advanced.value) and (not self.options.enable_expert.value):
            raise Exception("Player " + self.player_name + " has not selected any books!")

        starting_book: Item = self.create_item(
            ["Fundamentals Book", "Intermediate Book", "Advanced Book", "Expert Book"][self.options.starting_book.value]
        )

        books: list[bool] = [self.options.enable_fundamental.value == 1, self.options.enable_intermediate.value == 1,
                             self.options.enable_advanced.value == 1, self.options.enable_expert.value == 1]
        if not books[self.options.starting_book.value]:
            if self.options.enable_fundamental.value:
                starting_book = self.create_item("Fundamentals Book")
                self.options.starting_book.value = StartingBook.option_fundamentals
                # not sure if ^changing options^ is allowed but this seems to work
                # this is to prevent generating this book as item later
            elif self.options.enable_intermediate.value:
                starting_book = self.create_item("Intermediate Book")
                self.options.starting_book.value = StartingBook.option_intermediate
            elif self.options.enable_advanced.value:
                starting_book = self.create_item("Advanced Book")
                self.options.starting_book.value = StartingBook.option_advanced
            else:
                starting_book = self.create_item("Expert Book")
                self.options.starting_book.value = StartingBook.option_expert
            # not sure how to raise a warning without failing generation will silently change to selected book for now
        self.multiworld.push_precollected(starting_book)

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        cabin_region = Region("Cabin", self.player, self.multiworld)
        self.multiworld.regions.append(cabin_region)
        menu_region.connect(cabin_region)

        if self.options.enable_fundamental:
            fundamentals_region = Region("Fundamentals", self.player, self.multiworld)

            self.peaks_in_pool.extend(get_location_names_by_type(PeaksOfYoreRegion.FUNDAMENTALS, "Peak"))
            self.artefacts_in_pool.extend(get_location_names_by_type(PeaksOfYoreRegion.FUNDAMENTALS, "Artefact"))

            fundamentals_region.add_locations(get_locations(PeaksOfYoreRegion.FUNDAMENTALS), PeaksOfYoreLocation)
            cabin_region.connect(fundamentals_region, "Fundamentals Book",
                                 lambda state: state.has("Fundamentals Book", self.player))
            self.location_count += len(fundamentals_region.locations)

        if self.options.enable_intermediate:
            intermediate_region = Region("Intermediate", self.player, self.multiworld)

            self.peaks_in_pool.extend(get_location_names_by_type(PeaksOfYoreRegion.INTERMEDIATE, "Peak"))
            self.artefacts_in_pool.extend(get_location_names_by_type(PeaksOfYoreRegion.INTERMEDIATE, "Artefact"))

            intermediate_region.add_locations(get_locations(PeaksOfYoreRegion.INTERMEDIATE), PeaksOfYoreLocation)
            cabin_region.connect(intermediate_region, "Intermediate Book",
                                 lambda state: state.has("Intermediate Book", self.player))
            self.location_count += len(intermediate_region.locations)

        if self.options.enable_advanced:
            advanced_region = Region("Advanced", self.player, self.multiworld)

            self.peaks_in_pool.extend(get_location_names_by_type(PeaksOfYoreRegion.ADVANCED, "Peak"))
            self.artefacts_in_pool.extend(get_location_names_by_type(PeaksOfYoreRegion.ADVANCED, "Artefact"))

            advanced_region.add_locations(get_locations(PeaksOfYoreRegion.ADVANCED), PeaksOfYoreLocation)
            cabin_region.connect(advanced_region, "Advanced Book",
                                 lambda state: state.has("Advanced Book", self.player))
            self.location_count += len(advanced_region.locations)

        if self.options.enable_expert:
            expert_region = Region("Expert", self.player, self.multiworld)
            expert_locations: dict[str, int] = {k: v for k, v in get_locations(PeaksOfYoreRegion.EXPERT).items() if
                                                (not self.options.disable_solemn_tempest) or v != 37}

            self.artefacts_in_pool.extend(get_location_names_by_type(PeaksOfYoreRegion.EXPERT, "Artefact"))
            self.peaks_in_pool.append("Great Bulwark")
            if not self.options.disable_solemn_tempest:
                self.peaks_in_pool.append("Solemn Tempest")

            expert_region.add_locations(expert_locations, PeaksOfYoreLocation)
            cabin_region.connect(expert_region, "Expert Book", lambda state: state.has("Expert Book", self.player))
            self.location_count += len(expert_region.locations)

    def create_items(self) -> None:
        # order: books, tools, ropes, bird seeds, artefacts, fill rest with extra Items


        books: dict[str, Toggle] = {
            "Fundamentals Book": self.options.enable_fundamental,
            "Intermediate Book": self.options.enable_intermediate,
            "Advanced Book": self.options.enable_advanced,
            "Expert Book": self.options.enable_expert
        }


        starting_book: Item = self.create_item([*books][self.options.starting_book.value])

        remaining_items = self.location_count

        for name, option in books.items():
            if (not option) or remaining_items <= 0 or starting_book.name == name:
                continue
            self.multiworld.itempool.append(self.create_item(name))
            remaining_items -= 1

        for tool in [item for item in full_item_list if item.type == "Tool"]:
            if remaining_items > 0 and (tool.name != "Barometer" or not self.options.start_with_barometer):
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
                        # else don't place rope unlock
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
                state.can_reach_location(artefact, self.player) for artefact in self.artefacts_in_pool)

        if self.options.goal.value == Goal.option_all_peaks:
            self.multiworld.completion_condition[self.player] = lambda state: all(
                state.can_reach_location(peak, self.player) for peak in self.peaks_in_pool)

        if self.options.goal.value == Goal.option_all_peaks:
            self.multiworld.completion_condition[self.player] = lambda state: all(
                state.can_reach_location(loc, self.player) for loc in [*self.peaks_in_pool, *self.artefacts_in_pool])

        if self.options.goal.value == Goal.option_all:
            self.multiworld.completion_condition[self.player] = lambda state: all(
                state.can_reach_location(loc.name, self.player) for loc in self.get_locations())

    def fill_slot_data(self) -> dict[str, Any]:
        return self.options.as_dict("death_link", "goal", "rope_unlock_mode", casing="camel")
