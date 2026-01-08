from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class InsaniquariumDeluxeArchipelagoOptions:
    pass


class InsaniquariumDeluxeGame(Game):
    # Initial implementation by RoobyRoo.

    name = "Insaniquarium Deluxe"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.AND,
        KeymastersKeepGamePlatforms.IOS,
    ]

    is_adult_only_or_unrated = False

    options_cls = InsaniquariumDeluxeArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()
    
    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete Tank LEVEL with the following pets: PETS",
                data={
                    "LEVEL": (self.level, 1),
                    "PETS": (self.pets, 3)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            )
        ]

    @staticmethod
    def level() -> List[str]:
        return [
            "1-1",
            "1-2",
            "1-3",
            "1-4",
            "1-5",
            "2-1",
            "2-2",
            "2-3",
            "2-4",
            "2-5",
            "3-1",
            "3-2",
            "3-3",
            "3-4",
            "3-5",
            "4-1",
            "4-2",
            "4-3",
            "4-4",
            "4-5",
        ]
    
    @staticmethod
    def pets() -> List[str]:
        return [
            "Stinky",
            "Niko",
            "Itchy",
            "Prego",
            "Zorf",
            "Clyde",
            "Vert",
            "Rufus",
            "Meryl",
            "Wadsworth",
            "Seymour",
            "Shrapnel",
            "Gumbo",
            "Blip",
            "Rhubarb",
            "Nimbus",
            "Amp",
            "Gash",
            "Angie",
            "Presto",
            "Brinkley",
            "Nostradamus",
            "Stanley",
            "Walter",
        ]


# Archipelago Options
# ...
