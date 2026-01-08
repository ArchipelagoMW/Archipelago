from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class RockOfAges2BiggerAndBoulderArchipelagoOptions:
    pass


class RockOfAges2BiggerAndBoulderGame(Game):
    name = "Rock of Ages 2: Bigger & Boulder"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XONE,
    ]

    is_adult_only_or_unrated = False

    options_cls = RockOfAges2BiggerAndBoulderArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a match of War in PLACE",
                data={
                    "PLACE": (self.places, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=8,
            ),
            GameObjectiveTemplate(
                label="Win a match of War in PLACE, bringing the following Boulder: BOULDER",
                data={
                    "PLACE": (self.places, 1),
                    "BOULDER": (self.boulders, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Win a match of War in PLACE, bringing the following Buildings: BUILDINGS",
                data={
                    "PLACE": (self.places, 1),
                    "BUILDINGS": (self.buildings, 2),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Win a match of War in PLACE, bringing the following Boulder and Buildings: BOULDER, BUILDINGS",
                data={
                    "PLACE": (self.places, 1),
                    "BOULDER": (self.boulders, 1),
                    "BUILDINGS": (self.buildings, 2),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win a match of Obstacle Course in PLACE",
                data={
                    "PLACE": (self.places, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Win a match of Obstacle Course in PLACE, using the following Boulder: BOULDER",
                data={
                    "PLACE": (self.places, 1),
                    "BOULDER": (self.boulders_no_block, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Score at least 600 points in Skee-Boulder Training in PLACE",
                data={
                    "PLACE": (self.places, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Score at least 600 points in Skee-Boulder Training in PLACE, using the following Boulder: BOULDER",
                data={
                    "PLACE": (self.places, 1),
                    "BOULDER": (self.boulders_no_block, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Earn a Bronze Medal or better in Time Trial in PLACE",
                data={
                    "PLACE": (self.places, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Earn a Silver Medal or better in Time Trial in PLACE",
                data={
                    "PLACE": (self.places, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Earn a Gold Medal in Time Trial in PLACE",
                data={
                    "PLACE": (self.places, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Defeat the CHARACTER",
                data={
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Defeat God in a match of Foosball",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
        ]

    @staticmethod
    def boulders() -> List[str]:
        return [
            "Rock of Ages",
            "Lion Boulder",
            "Medusa's Boulder",
            "Block of Ages",
            "Armored Boulder",
            "Globus Cruciger",
            "Gunpowder Boulder",
            "Fire Boulder",
            "Angel Boulder",
            "Globe",
            "Sand Boulder",
            "Prehistoric Wheel",
            "Tar Boulder",
            "Paint Boulder",
            "Balloon Boulder",
            "Cow",
        ]

    def boulders_no_block(self) -> List[str]:
        boulders = self.boulders()[:]

        if "Block of Ages" in boulders:
            boulders.remove("Block of Ages")

        return boulders

    @staticmethod
    def buildings() -> List[str]:
        return [
            "Bank",
            "Tower",
            "War Elephant",
            "Sticky Cows",
            "Anvil Bull",
            "Bull of Heaven",
            "Da Vinci Tank",
            "Catapult",
            "Ballista",
            "Cannon",
            "Trebuchet",
            "Explosives",
            "Fireworks Cannon",
            "Windmill Fan",
            "Whale",
            "Springboard Trap",
            "Phoenix Tree",
            "Balloon",
            "Battleship",
        ]

    @staticmethod
    def places() -> List[str]:
        return [
            "Oxfordshire",
            "Rennes",
            "Scotland",
            "Egypt",
            "Cadaques",
            "La Mancha",
            "Holland",
            "Lviv",
            "Oslo",
            "Delphi",
            "Sarpedon",
            "Pompeii",
            "Bologna",
            "Dover",
            "Garden of Eden",
        ]

    @staticmethod
    def characters() -> List[str]:
        return [
            "Thinker",
            "Dragon",
            "Sphinx",
        ]

# Archipelago Options
# ...
