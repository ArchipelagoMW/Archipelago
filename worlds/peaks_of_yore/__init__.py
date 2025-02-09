from typing import Any

from worlds.AutoWorld import World, WebWorld
from BaseClasses import Tutorial, Item, Region, ItemClassification
from .options import PeaksOfYoreOptions, Goal
from .data import full_item_list, full_location_list
from .items import PeaksOfYoreItem
from .locations import get_locations, get_location_names_by_type, PeaksOfYoreLocation


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
    location_count = 0
    peaks_in_pool = []
    artefacts_in_pool = []

    def create_item(self, name: str) -> Item:
        classification: ItemClassification = ItemClassification.filler
        item_entry = [item for item in full_item_list if item.name == name][0]
        if item_entry.type in ["Book", "Tool"]:
            classification = ItemClassification.progression
        return PeaksOfYoreItem(name, classification, self.item_name_to_id[name], self.player)

    def create_extra_item(self):
        choices = ["Extra Rope", "Extra Coffee", "Extra Chalk", "Extra Seed"]
        return self.create_item(self.random.choice(choices))

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        cabin_region = Region("Cabin", self.player, self.multiworld)
        self.multiworld.regions.append(cabin_region)
        menu_region.connect(cabin_region)

        if self.options.enable_fundamental:
            fundamentals_region = Region("Fundamentals", self.player, self.multiworld)

            self.peaks_in_pool.extend(get_location_names_by_type(0, "Peak"))
            self.artefacts_in_pool.extend(get_location_names_by_type(0, "Artefact"))

            fundamentals_region.add_locations(get_locations(0), PeaksOfYoreLocation)
            cabin_region.connect(fundamentals_region, "Fundamentals Book",
                                 lambda state: state.has("Fundamentals Book", self.player))
            self.location_count += len(fundamentals_region.locations)

        if self.options.enable_intermediate:
            intermediate_region = Region("Intermediate", self.player, self.multiworld)

            self.peaks_in_pool.extend(get_location_names_by_type(1, "Peak"))
            self.artefacts_in_pool.extend(get_location_names_by_type(1, "Artefact"))

            intermediate_region.add_locations(get_locations(1), PeaksOfYoreLocation)
            cabin_region.connect(intermediate_region, "Intermediate Book",
                                 lambda state: state.has("Intermediate Book", self.player))
            self.location_count += len(intermediate_region.locations)

        if self.options.enable_advanced:
            advanced_region = Region("Advanced", self.player, self.multiworld)

            self.peaks_in_pool.extend(get_location_names_by_type(2, "Peak"))
            self.artefacts_in_pool.extend(get_location_names_by_type(2, "Artefact"))

            advanced_region.add_locations(get_locations(2), PeaksOfYoreLocation)
            cabin_region.connect(advanced_region, "Advanced Book",
                                 lambda state: state.has("Advanced Book", self.player))
            self.location_count += len(advanced_region.locations)

        if self.options.enable_expert:
            expert_region = Region("Expert", self.player, self.multiworld)
            expert_locations: dict[str, int] = {k: v for k, v in get_locations(3).items() if
                                                (not self.options.disable_solemn_tempest) or v != 37}

            self.artefacts_in_pool.extend(get_location_names_by_type(3, "Artefact"))
            self.peaks_in_pool.append("Great Bulwark")
            if not self.options.disable_solemn_tempest:
                self.peaks_in_pool.append("Solemn Tempest")

            expert_region.add_locations(expert_locations, PeaksOfYoreLocation)
            cabin_region.connect(expert_region, "Expert Book", lambda state: state.has("Expert Book", self.player))
            self.location_count += len(expert_region.locations)

    def create_items(self) -> None:
        # order: books, tools, ropes, bird seeds, artefacts, fill rest with extra Items
        starting_book: Item = self.create_item(
            ["Fundamentals Book", "Intermediate Book", "Advanced Book", "Expert Book"][
                self.options.starting_book.value])
        self.multiworld.push_precollected(starting_book)

        if self.options.start_with_barometer:
            self.multiworld.push_precollected(self.create_item("Barometer"))

        remaining_items = self.location_count

        for book in [item for item in full_item_list if item.type == "Book"]:
            if remaining_items > 0:
                item = self.create_item(book.name)
                if starting_book.name == item.name:
                    continue
                self.multiworld.itempool.append(item)
                remaining_items -= 1

        for tool in [item for item in full_item_list if item.type == "Tool"]:
            if remaining_items > 0 and (tool.name != "Barometer" or not self.options.start_with_barometer):
                self.multiworld.itempool.append(self.create_item(tool.name))
                remaining_items -= 1

        remaining_items -= 1
        self.multiworld.itempool.append(self.create_item("Progressive Crampons"))

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

        self.multiworld.itempool += [self.create_extra_item() for _ in range(remaining_items)]

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
        return self.options.as_dict("death_link", "goal", "starting_book", "enable_fundamental", "enable_intermediate",
                                    "enable_advanced", "enable_expert", "disable_solemn_tempest", casing="camel",
                                    toggles_as_bools=True)
