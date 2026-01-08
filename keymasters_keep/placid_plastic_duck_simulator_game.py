from __future__ import annotations

import functools

from typing import List, Set

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class PlacidPlasticDuckSimulatorArchipelagoOptions:
    placid_plastic_duck_simulator_dlc_owned: PlacidPlasticDuckSimulatorDLCOwned


class PlacidPlasticDuckSimulatorGame(Game):
    name = "Placid Plastic Duck Simulator"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = False

    options_cls = PlacidPlasticDuckSimulatorArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Obtain DUCK on LOCATION",
                data={"DUCK": (self.ducks, 1), "LOCATION": (self.locations, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Witness DUCK INTERACTION",
                data={"DUCK": (self.ducks, 1), "INTERACTION": (self.interactions, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
        ]

    @property
    def dlc_owned(self) -> Set[str]:
        return self.archipelago_options.placid_plastic_duck_simulator_dlc_owned.value

    @property
    def has_dlc_ducks_please(self) -> bool:
        return "Ducks, Please" in self.dlc_owned

    @property
    def has_dlc_quacking_the_ice(self) -> bool:
        return "Quacking the Ice" in self.dlc_owned

    @property
    def has_dlc_duck_addiction(self) -> bool:
        return "Duck Addiction" in self.dlc_owned

    @property
    def has_dlc_hippospace_download(self) -> bool:
        return "Hippospace Download" in self.dlc_owned

    @property
    def has_dlc_so_many_ducks(self) -> bool:
        return "So Many Ducks" in self.dlc_owned

    @property
    def has_dlc_rooftop_one_percent(self) -> bool:
        return "Rooftop One Percent" in self.dlc_owned

    @property
    def has_dlc_ducks_galore(self) -> bool:
        return "Ducks Galore" in self.dlc_owned

    @functools.cached_property
    def ducks_base(self) -> List[str]:
        return [
            "Normal Duck (PPD 1-1)",
            "Alien Duck (PPD 1-2)",
            "Moss Duck (PPD 1-3)",
            "Wood Duck (PPD 1-4)",
            "Plaid Duck (PPD 1-5)",
            "Stone Duck (PPD 1-6)",
            "Marble Duck (PPD 1-7)",
            "Red Duck (PPD 1-8)",
            "Propeller Hat Duck (PPD 1-9)",
            "Polka Dot Duck (PPD 1-10)",
            "Skeleton Duck (PPD 2-1)",
            "Zebra Duck (PPD 2-2)",
            "Purple Chrome Duck (PPD 2-3)",
            "Panda Duck (PPD 2-4)",
            "Daisy Duck (PPD 2-5)",
            "Electric Duck (PPD 2-6)",
            "Cactus Duck (PPD 2-7)",
            "KISS Duck (PPD 2-8)",
            "Leopard Duck (PPD 2-9)",
            "Anime Duck (PPD 2-10)",
            "Camo Duck (PPD 3-1)",
            "Duck You Duck (PPD 3-2)",
            "Rainbow Duck (PPD 3-3)",
            "Dirty Duck (PPD 3-4)",
            "Tiger Duck (PPD 3-5)",
            "Black Duck (PPD 3-6)",
            "Solar Panel Duck (PPD 3-7)",
            "Pink Lightning Duck (PPD 3-8)",
            "Scribble Duck (PPD 3-9)",
            "8-Ball Duck (PPD 3-10)",
            "Turquoise Duck (PPD 4-1)",
            "Submarine Duck (PPD 4-2)",
            "Glow Duck (PPD 4-3)",
            "Dragon Duck (PPD 4-4)",
            "Firefighter Duck (PPD 4-5)",
            "Lava Duck (PPD 4-6)",
            "Cow Duck (PPD 4-7)",
            "Calavera Duck (PPD 4-8)",
            "Cartoon Duck (PPD 4-9)",
            "Gentleman Duck (PPD 4-10)",
            "Cool Duck (PPD 5-1)",
            "Sakura Duck (PPD 5-2)",
            "Wireframe Duck (PPD 5-3)",
            "Knife Duck (PPD 5-4)",
            "Gold Duck (PPD 5-5)",
            "Grafitti Duck (PPD 5-6)",
            "Psychadelic Duck (PPD 5-7)",
        ]

    @functools.cached_property
    def ducks_ducks_please(self) -> List[str]:
        return [
            "Doodle Duck (DP 1-1)",
            "Chameleon Duck (DP 1-2)",
            "Watermelon Duck (DP 1-3)",
            "Negative Magnet Duck (DP 1-4)",
            "Flowerpot Duck (DP 1-5)",
            "Big Head Duck (DP 1-6)",
            "Strawberry Duck (DP 1-7)",
            "Sad Duck (DP 1-8)",
            "Band-Aid Duck (DP 1-9)",
            "Sponge Duck (DP 1-10)",
            "Donut Duck (DP 2-1)",
            "Crystal Duck (DP 2-2)",
            "Egg Duck (DP 2-3)",
            "Clown Duck (DP 2-4)",
            "Disco Duck (DP 2-5)",
            "Bee Duck (DP 2-6)",
            "Rocket Duck (DP 2-7)",
            "Positive Magnet Duck (DP 2-8)",
            "Tesla Duck (DP 2-9)",
            "Candle Duck (DP 2-10)",
            "Unicorn Duck (DP 3-1)",
            "Agent Duck (DP 3-2)",
            "Math Duck (DP 3-3)",
            "King of Hearts Duck (DP 3-4)",
            "Kintsugi Duck (DP 3-5)",
            "Baseball Duck (DP 3-6)",
            "Turbolento Duck (DP 3-7)",
        ]

    @functools.cached_property
    def ducks_duck_addiction(self) -> List[str]:
        return [
            "Shark Duck (DA 1-1)",
            "Cat Duck (DA 1-2)",
            "Bull Duck (DA 1-3)",
            "Knight Duck (DA 1-4)",
            "Party Duck (DA 1-5)",
            "Afro Duck (DA 1-6)",
            "Luchador Duck (DA 1-7)",
            "Surgery Duck (DA 1-8)",
            "Stamp Duck (DA 1-9)",
            "Star Duck (DA 1-10)",
            "Matrioska (L) Duck (DA 2-1)",
            "Matrioska (M) Duck (DA 2-2)",
            "Matrioska (S) Duck (DA 2-3)",
            "Pizza Duck (DA 2-4)",
            "Crossword Duck (DA 2-5)",
            "Ninja Duck (DA 2-6)",
            "Steampunk Duck (DA 2-7)",
            "Tron Duck (DA 2-8)",
            "Yatta Duck (DA 2-9)",
            "Ghost Duck (DA 2-10)",
            "Slime Duck (DA 3-1)",
            "Bubblegum Duck (DA 3-2)",
            "Bottle Duck (DA 3-3)",
            "King of Spades Duck (DA 3-4)",
            "Picasso Duck (DA 3-5)",
            "Pixel Duck (DA 3-6)",
            "Rave Duck (DA 3-7)",
        ]

    @functools.cached_property
    def ducks_so_many_ducks(self) -> List[str]:
        return [
            "Sushi Duck (SMD 1-1)",
            "Snail Duck (SMD 1-2)",
            "Parrot Duck (SMD 1-3)",
            "Unibrow Duck (SMD 1-4)",
            "Rain Duck (SMD 1-5)",
            "Pineapple Duck (SMD 1-6)",
            "Amigurumi Duck (SMD 1-7)",
            "Pajama Duck (SMD 1-8)",
            "Piggy Bank Duck (SMD 1-9)",
            "Thief Duck (SMD 1-10)",
            "Coffee Duck (SMD 2-1)",
            "Milk Duck (SMD 2-2)",
            "Nerd Duck (SMD 2-3)",
            "Crypto Duck (SMD 2-4)",
            "Red Jello Duck (SMD 2-5)",
            "Yellow Jello Duck (SMD 2-6)",
            "Blue Jello Duck (SMD 2-7)",
            "Boxer Duck (SMD 2-8)",
            "Ladybug Duck (SMD 2-9)",
            "Scuba Duck (SMD 2-10)",
            "Frog Duck (SMD 3-1)",
            "Puffer Duck (SMD 3-2)",
            "Strongbox Duck (SMD 3-3)",
            "Arcade Duck (SMD 3-4)",
            "90s Duck (SMD 3-5)",
            "Holo Duck (SMD 3-6)",
            "Superhero Duck (SMD 3-7)",
        ]

    @functools.cached_property
    def ducks_ducks_galore(self) -> List[str]:
        return [
            "Orange Duck (DG 1-1)",
            "Kick Me Duck (DG 1-2)",
            "Heart Duck (DG 1-3)",
            "Constellation Duck (DG 1-4)",
            "Clicker Duck (DG 1-5)",
            "Apple Duck (DG 1-6)",
            "Music Box Duck (DG 1-7)",
            "Pancake Duck (DG 1-8)",
            "Big Eyes Duck (DG 1-9)",
            "Sharpie Duck (DG 1-10)",
            "Peacock Duck (DG 2-1)",
            "Window Duck (DG 2-2)",
            "Koi Duck (DG 2-3)",
            "Trans Duck (DG 2-4)",
            "My Name is... Duck (DG 2-5)",
            "Watergun Duck (DG 2-6)",
            "Octopus Duck (DG 2-7)",
            "Mosaic Duck (DG 2-8)",
            "Toadstool Duck (DG 2-9)",
            "Juicebox Duck (DG 2-10)",
            "Balloon Duck (DG 3-1)",
            "Pincushion Duck (DG 3-2)",
            "Gumball Duck (DG 3-3)",
            "Tamagotchi Duck (DG 3-4)",
            "Raccoon Duck (DG 3-5)",
            "Neon Duck (DG 3-6)",
            "Dynamite Duck (DG 3-7)",
        ]

    def ducks(self) -> List[str]:
        ducks: List[str] = self.ducks_base[:]

        if self.has_dlc_ducks_please:
            ducks.extend(self.ducks_ducks_please[:])

        if self.has_dlc_duck_addiction:
            ducks.extend(self.ducks_duck_addiction[:])

        if self.has_dlc_so_many_ducks:
            ducks.extend(self.ducks_so_many_ducks[:])

        if self.has_dlc_ducks_galore:
            ducks.extend(self.ducks_ducks_galore[:])

        return ducks

    def locations(self) -> List[str]:
        locations: List[str] = ["Infinity Cool"]

        if self.has_dlc_quacking_the_ice:
            locations.append("Quacking the Ice")

        if self.has_dlc_hippospace_download:
            locations.append("Hippospace Download")

        if self.has_dlc_rooftop_one_percent:
            locations.append("Rooftop One Percent")

        return locations

    def interactions(self) -> List[str]:
        interactions: List[str] = [
            "going down the slide on Infinity Cool",
            "going up the tube on Infinity Cool",
        ]

        if self.has_dlc_quacking_the_ice:
            interactions.extend(
                [
                    "going down the slide on Quacking the Ice",
                    "taking the chairlift on Quacking the Ice",
                    "relaxing by the fire pit on Quacking the Ice",
                ]
            )

        if self.has_dlc_hippospace_download:
            interactions.extend(
                [
                    "going down the tunnel on Hippospace Download",
                    "floating up to the upper pool on Hippospace Download",
                    "floating in zero gravity on Hippospace Download",
                    "boarding the shuttle on Hippospace Download",
                ]
            )

        if self.has_dlc_rooftop_one_percent:
            interactions.extend(
                [
                    "taking the elevator on Rooftop One Percent",
                    "going down the gutter on Rooftop One Percent",
                ]
            )

        return interactions


# Archipelago Options
class PlacidPlasticDuckSimulatorDLCOwned(OptionSet):
    """
    Indicates which Placid Plastic Duck Simulator DLC the player owns, if any.
    """

    display_name = "Placid Plastic Duck Simulator DLC Owned"
    valid_keys = [
        "Ducks, Please",
        "Quacking the Ice",
        "Duck Addiction",
        "Hippospace Download",
        "So Many Ducks",
        "Rooftop One Percent",
        "Ducks Galore",
    ]

    default = valid_keys
