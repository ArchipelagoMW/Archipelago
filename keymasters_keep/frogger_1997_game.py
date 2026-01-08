from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class Frogger1997ArchipelagoOptions:
    pass


class Frogger1997Game(Game):
    name = "Frogger (1997)"
    platform = KeymastersKeepGamePlatforms.PS1

    platforms_other = [
        KeymastersKeepGamePlatforms.PC,
    ]

    is_adult_only_or_unrated = False

    options_cls = Frogger1997ArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Find the COLOR Frog in STAGE",
                data={
                    "COLOR": (self.colors, 1),
                    "STAGE": (self.stages, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Find the COLOR Frog in STAGE",
                data={
                    "COLOR": (self.colors_with_gold, 1),
                    "STAGE": (self.stages_gold, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete STAGE",
                data={
                    "STAGE": (self.stages_all, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
        ]

    @staticmethod
    def colors() -> List[str]:
        return [
            "Red",
            "Blue",
            "Orange",
            "Purple",
            "Green",
        ]

    @staticmethod
    def colors_with_gold() -> List[str]:
        return [
            "Red",
            "Blue",
            "Orange",
            "Purple",
            "Green",
            "Gold",
        ]

    @staticmethod
    def stages() -> List[str]:
        return [
            "Level 1-1 - Retro Level 1",
            "Level 1-2 - Retro Level 2",
            "Level 1-3 - Retro Level 3",
            "Level 1-4 - Retro Level 4",
            "Level 2-1 - Lily Islands",
            "Level 2-2 - Bow Wow Falls",
            "Level 2-3 - Mower Mania",
            "Level 2-5 - Bow Wow Revenge",
            "Level 3-1 - Honey Bee Hollow",
            "Level 3-2 - Canopy Capers",
            "Level 4-2 - Platform Madness",
            "Level 4-3 - Lava Crush",
            "Level 5-1 - Dark Dark Cavern",
            "Level 5-2 - Frogger Goes Skiing",
            "Level 6-1 - Looney Balloons",
            "Level 6-2 - Time Flies",
            "Level 6-3 - Loonier Balloons",
            "Level 7-1 - Bang Bang Barrel",
            "Level 7-2 - Slime Sliding",
            "Level 7-4 - Boom Boom Barrel",
            "Level 7-5 - Reservoir Frogs",
            "Level 8-1 - Cactus Point",
            "Level 8-2 - Boulder Alley",
            "Level 8-3 - Tumbling Alley",
            "Level 8-5 - Big Boulder Alley",
        ]

    @staticmethod
    def stages_gold() -> List[str]:
        return [
            "Level 1-5 - Retro Level 5",
            "Level 2-4 - Spinning Lilies",
            "Level 4-1 - Scorching Switches",
            "Level 5-3 - Webs Cavern",
            "Level 6-4 - Airshow Antics",
            "Level 7-3 - Uncanny Crusher",
            "Level 8-4 - Crumbled Point",
            "Level 9-1 - Tropical Trouble",
        ]

    def stages_all(self) -> List[str]:
        return sorted(self.stages() + self.stages_gold())


# Archipelago Options
# ...
