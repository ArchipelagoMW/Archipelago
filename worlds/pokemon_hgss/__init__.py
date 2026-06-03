from typing import Any

from BaseClasses import Item

from worlds.AutoWorld import World, WebWorld

from .Items import (
    GAME_NAME,
    create_item,
    get_item_pool_names,
    item_name_groups,
    item_name_to_id,
)
from .Locations import (
    location_name_groups,
    location_name_to_id,
)
from .Options import PokemonHGSSOptions
from .Output import write_hgss_output
from .Regions import create_hgss_regions
from .Rules import set_hgss_rules


class PokemonHGSSWebWorld(WebWorld):
    theme = "grass"


class PokemonHGSSWorld(World):
    """
    Experimental Archipelago support for Pokemon HeartGold and SoulSilver.

    This is currently a Johto progression prototype used to test
    generation, locations, progression items, and basic completion logic.
    """

    game = GAME_NAME
    author = "EyeballSweat"
    options_dataclass = PokemonHGSSOptions
    options: PokemonHGSSOptions

    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id

    item_name_groups = item_name_groups
    location_name_groups = location_name_groups

    web = PokemonHGSSWebWorld()

    def create_regions(self) -> None:
        create_hgss_regions(self)

        victory_location = self.multiworld.get_location(
            "Pokemon League - Defeat Lance",
            self.player,
        )

        victory_location.place_locked_item(
            create_item(self.player, "Victory")
        )

    def create_items(self) -> None:
        location_count = len(self.location_name_to_id)

        for item_name in get_item_pool_names(self.random, location_count):
            self.multiworld.itempool.append(
                self.create_item(item_name)
            )

    def create_item(self, name: str) -> Item:
        return create_item(self.player, name)

    def set_rules(self) -> None:
        set_hgss_rules(self)

    def fill_slot_data(self) -> dict[str, Any]:
        return {
            "goal": int(self.options.goal.value),
            "hm_badge_requirements": bool(
                self.options.hm_badge_requirements.value
            ),
            "item_name_to_id": self.item_name_to_id,
            "location_name_to_id": self.location_name_to_id,
        }

    def generate_output(self, output_directory: str) -> None:
        write_hgss_output(self, output_directory)