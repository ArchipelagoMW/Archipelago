from BaseClasses import Item, ItemClassification

from worlds.AutoWorld import World, WebWorld

from .Items import (
    GAME_NAME,
    PokemonHGSSItem,
    create_item,
    item_name_to_id,
)
from .Locations import (
    PokemonHGSSLocation,
    location_name_to_id,
    LOCATION_TABLE,
)
from .Options import PokemonHGSSOptions
from .Regions import create_region
from .Rules import set_hgss_rules


class PokemonHGSSWebWorld(WebWorld):
    theme = "grass"


class PokemonHGSSWorld(World):
    """
    Experimental Archipelago support for Pokemon HeartGold and SoulSilver.

    This is currently a tiny proof-of-concept world used to test generation,
    regions, locations, progression items, and basic completion logic.
    """

    game = GAME_NAME
    author = "EyeballSweat"
    options_dataclass = PokemonHGSSOptions
    options: PokemonHGSSOptions

    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id

    web = PokemonHGSSWebWorld()

    def create_regions(self) -> None:
        menu = create_region(self, "Menu")

        new_bark = create_region(
            self,
            "New Bark Town",
            {
                "New Bark Town - Receive Starter":
                    LOCATION_TABLE["New Bark Town - Receive Starter"],
            },
        )

        violet = create_region(
            self,
            "Violet City",
            {
                "Violet City - Defeat Falkner":
                    LOCATION_TABLE["Violet City - Defeat Falkner"],
            },
        )

        azalea = create_region(
            self,
            "Azalea Town",
            {
                "Azalea Town - Defeat Bugsy":
                    LOCATION_TABLE["Azalea Town - Defeat Bugsy"],
            },
        )

        goldenrod = create_region(
            self,
            "Goldenrod City",
            {
                "Goldenrod City - Defeat Whitney":
                    LOCATION_TABLE["Goldenrod City - Defeat Whitney"],
            },
        )

        pokemon_league = create_region(self, "Pokemon League")

        victory_location = PokemonHGSSLocation(
            self.player,
            "Pokemon League - Defeat Lance",
            None,
            pokemon_league,
        )

        victory_location.place_locked_item(
            PokemonHGSSItem(
                "Victory",
                ItemClassification.progression,
                None,
                self.player,
            )
        )

        pokemon_league.locations.append(victory_location)

        self.multiworld.regions += [
            menu,
            new_bark,
            violet,
            azalea,
            goldenrod,
            pokemon_league,
        ]

        menu.connect(new_bark)
        new_bark.connect(violet)
        violet.connect(azalea)
        azalea.connect(goldenrod)
        goldenrod.connect(pokemon_league)

    def create_items(self) -> None:
        for item_name in self.item_name_to_id:
            self.multiworld.itempool.append(
                self.create_item(item_name)
            )

    def create_item(self, name: str) -> Item:
        return create_item(self.player, name)

    def set_rules(self) -> None:
        set_hgss_rules(self)