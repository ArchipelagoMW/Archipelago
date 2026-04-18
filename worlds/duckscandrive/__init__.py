"""Archipelago world definition for *Ducks Can Drive* (Steam app 2472840).

First-pass content surface: the five `Garage.Upgrade*` tracks, each with five
tiers, giving 25 locations and 25 matching `Progressive <Stat>` items.
Goal: fully upgrade the car (all 25 progressives collected).

Books, time-trial finishes, and time-trial par-times will be added as later
passes; this file keeps the scope tight to validate the client's Connect
handshake and LocationChecks flow end to end.
"""
from __future__ import annotations

from BaseClasses import Item, ItemClassification, Location, Region, Tutorial

from worlds.AutoWorld import WebWorld, World

from .items import TIERS_PER_STAT, UPGRADE_STATS, item_name_groups, item_name_to_id, item_table
from .locations import (
    book_location_table,
    location_name_to_id,
    time_trial_location_table,
    upgrade_location_table,
)
from .options import DucksOptions


class DucksItem(Item):
    game = "Ducks Can Drive"


class DucksLocation(Location):
    game = "Ducks Can Drive"


class DucksWeb(WebWorld):
    theme = "ocean"
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up Ducks Can Drive for Archipelago.",
            "English",
            "setup_en.md",
            "setup/en",
            ["sebdevar"],
        ),
    ]


class DucksWorld(World):
    """Ducks Can Drive is a chaotic small-scale driving game by Joseph Cook (2023)."""

    game = "Ducks Can Drive"
    web = DucksWeb()

    options_dataclass = DucksOptions
    options: DucksOptions

    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id
    item_name_groups = item_name_groups

    required_client_version = (0, 5, 0)

    def create_item(self, name: str) -> DucksItem:
        data = item_table[name]
        classification = ItemClassification.progression if data.progression else ItemClassification.filler
        return DucksItem(name, classification, data.id, self.player)

    def create_regions(self) -> None:
        menu = Region("Menu", self.player, self.multiworld)
        city = Region("City", self.player, self.multiworld)
        time_trials = Region("Time Trials", self.player, self.multiworld)

        for name, data in upgrade_location_table.items():
            city.locations.append(DucksLocation(self.player, name, data.id, city))

        for name, loc_id in book_location_table.items():
            city.locations.append(DucksLocation(self.player, name, loc_id, city))

        for name, loc_id in time_trial_location_table.items():
            time_trials.locations.append(DucksLocation(self.player, name, loc_id, time_trials))

        victory = DucksLocation(self.player, "Fully Upgraded Car", None, city)
        victory.place_locked_item(DucksItem("Victory", ItemClassification.progression, None, self.player))
        city.locations.append(victory)

        menu.connect(city)
        menu.connect(time_trials)
        self.multiworld.regions += [menu, city, time_trials]

    def create_items(self) -> None:
        for name, data in item_table.items():
            for _ in range(data.count):
                self.multiworld.itempool.append(self.create_item(name))

    def set_rules(self) -> None:
        # Tier N requires N-1 progressives of its stat, so every Tier 1 location
        # is a free sphere-1 check (the player's starting money buys the first
        # upgrade without AP input). A circular rule — tier N requires N — would
        # leave sphere-1 empty and the seed unfillable. Book locations are free
        # pickups and get no access rule.
        for name, data in upgrade_location_table.items():
            progressive = f"Progressive {data.stat}"
            required = data.tier - 1
            location = self.multiworld.get_location(name, self.player)
            location.access_rule = lambda state, item=progressive, count=required: state.has(item, self.player, count)

        self.multiworld.completion_condition[self.player] = lambda state: state.has_all_counts(
            {f"Progressive {stat}": TIERS_PER_STAT for stat in UPGRADE_STATS},
            self.player,
        )

    def fill_slot_data(self) -> dict[str, object]:
        # Sent to the client in the Connected packet; read by the mod to
        # configure behaviour that has to live client-side (money top-up, etc).
        return {
            "starting_money": self.options.starting_money.value,
        }
