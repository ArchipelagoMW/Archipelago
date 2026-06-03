from BaseClasses import Item

from worlds.AutoWorld import World, WebWorld

from .Items import (
    GAME_NAME,
    create_item,
    item_name_to_id,
)
from .Locations import location_name_to_id
from .Options import PokemonHGSSOptions
from .Regions import create_hgss_regions
from .Rules import set_hgss_rules


class PokemonHGSSWebWorld(WebWorld):
    theme = "grass"


class PokemonHGSSWorld(World):
    """
    Experimental Archipelago support for Pokemon HeartGold and SoulSilver.

    This is currently a Johto badge progression prototype used to test
    generation, regions, locations, progression items, and basic completion
    logic.
    """

    game = GAME_NAME
    author = "EyeballSweat"
    options_dataclass = PokemonHGSSOptions
    options: PokemonHGSSOptions

    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id

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
        for item_name in self.item_name_to_id:
            self.multiworld.itempool.append(
                self.create_item(item_name)
            )

    def create_item(self, name: str) -> Item:
        return create_item(self.player, name)

    def set_rules(self) -> None:
        set_hgss_rules(self)