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

    This is currently a Johto badge progression prototype used to test
    generation, regions, locations, progression items, and basic completion
    logic.
    """

    game = GAME_NAME
    author = "prcecilio02"
    options_dataclass = PokemonHGSSOptions
    options: PokemonHGSSOptions

    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id

    web = PokemonHGSSWebWorld()

    def create_regions(self) -> None:
        menu = create_region(self, "Menu")

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

        ecruteak = create_region(
            self,
            "Ecruteak City",
            {
                "Ecruteak City - Defeat Morty":
                    LOCATION_TABLE["Ecruteak City - Defeat Morty"],
            },
        )

        cianwood = create_region(
            self,
            "Cianwood City",
            {
                "Cianwood City - Defeat Chuck":
                    LOCATION_TABLE["Cianwood City - Defeat Chuck"],
            },
        )

        olivine = create_region(
            self,
            "Olivine City",
            {
                "Olivine City - Defeat Jasmine":
                    LOCATION_TABLE["Olivine City - Defeat Jasmine"],
            },
        )

        mahogany = create_region(
            self,
            "Mahogany Town",
            {
                "Mahogany Town - Defeat Pryce":
                    LOCATION_TABLE["Mahogany Town - Defeat Pryce"],
            },
        )

        blackthorn = create_region(
            self,
            "Blackthorn City",
            {
                "Blackthorn City - Defeat Clair":
                    LOCATION_TABLE["Blackthorn City - Defeat Clair"],
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
            violet,
            azalea,
            goldenrod,
            ecruteak,
            cianwood,
            olivine,
            mahogany,
            blackthorn,
            pokemon_league,
        ]

        menu.connect(violet)
        violet.connect(azalea)
        azalea.connect(goldenrod)
        goldenrod.connect(ecruteak)
        ecruteak.connect(cianwood)
        cianwood.connect(olivine)
        olivine.connect(mahogany)
        mahogany.connect(blackthorn)
        blackthorn.connect(pokemon_league)

    def create_items(self) -> None:
        for item_name in self.item_name_to_id:
            self.multiworld.itempool.append(
                self.create_item(item_name)
            )

    def create_item(self, name: str) -> Item:
        return create_item(self.player, name)

    def set_rules(self) -> None:
        set_hgss_rules(self)