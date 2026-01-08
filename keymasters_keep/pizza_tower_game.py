from __future__ import annotations


from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class PizzaTowerArchipelagoOptions:
    pass


class PizzaTowerGame(Game):
    # Initial Proposal by @bowsercrusher on Discord

    name = "Pizza Tower"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.SW,
    ]

    is_adult_only_or_unrated = False

    options_cls = PizzaTowerArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete LEVEL as CHARACTER",
                data={
                    "LEVEL": (self.levels, 1),
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=8,
            ),
            GameObjectiveTemplate(
                label="Defeat BOSS as CHARACTER",
                data={
                    "BOSS": (self.bosses, 1),
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Collect the Treasure in LEVEL as CHARACTER",
                data={
                    "LEVEL": (self.levels_no_tower, 1),
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Find Secret SECRET in LEVEL as CHARACTER",
                data={
                    "SECRET": (self.secret_range, 1),
                    "LEVEL": (self.levels_no_tower, 1),
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete Chef Task TASK in LEVEL as CHARACTER",
                data={
                    "TASK": (self.task_range, 1),
                    "LEVEL": (self.levels_no_tower, 1),
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="S-Rank LEVEL as CHARACTER",
                data={
                    "LEVEL": (self.levels_no_tower, 1),
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="P-Rank LEVEL as CHARACTER",
                data={
                    "LEVEL": (self.levels, 1),
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="P-Rank BOSS as CHARACTER",
                data={
                    "BOSS": (self.bosses, 1),
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
        ]

    @staticmethod
    def levels() -> List[str]:
        return [
            "Ancient Cheese",
            "Bloodsauce Dungeon",
            "Crust Cove",
            "Deep Dish 9",
            "Don't Make a Sound",
            "Fastfood Saloon",
            "Fun Farm",
            "GOLF!",
            "Gnome Forest",
            "John Gutter",
            "Oh Shit!",
            "Oregano Desert",
            "Peppibot Factory",
            "Pizzascape",
            "Pizzascare",
            "Refrigerator-Refrigerador-Freezerator",
            "The Crumbling Tower of Pizza",
            "The Pig City",
            "WAR",
            "Wasteyard",
        ]

    def levels_no_tower(self) -> List[str]:
        levels: List[str] = self.levels()

        if "The Crumbling Tower of Pizza" in levels:
            levels.remove("The Crumbling Tower of Pizza")

        return levels

    @staticmethod
    def characters() -> List[str]:
        return [
            "Noise",
            "Peppino",
        ]

    @staticmethod
    def bosses() -> List[str]:
        return [
            "Fake Peppino",
            "Pepperman",
            "Pizzaface",
            "The Noise/Doise",
            "The Vigilante",
        ]

    @staticmethod
    def secret_range() -> range:
        return range(1, 4)

    @staticmethod
    def task_range() -> range:
        return range(1, 4)


# Archipelago Options
# ...
