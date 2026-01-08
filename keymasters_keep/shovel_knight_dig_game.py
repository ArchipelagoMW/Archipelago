from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class ShovelKnightDigArchipelagoOptions:
    pass


class ShovelKnightDigGame(Game):
    name = "Shovel Knight Dig"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.IOS,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = False

    options_cls = ShovelKnightDigArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play on Knightmare LEVEL",
                data={
                    "LEVEL": (self.knightmare_level_range, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Cannot use Relics (except Omega Driver)",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete a run with the ARMOR equipped",
                data={
                    "ARMOR": (self.armors, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Defeat BOSS with the ARMOR equipped",
                data={
                    "BOSS": (self.bosses_non_final, 1),
                    "ARMOR": (self.armors, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Collect every Cog in WORLD in a single run",
                data={
                    "WORLD": (self.worlds, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete a True Ending run with the ARMOR equipped",
                data={
                    "ARMOR": (self.armors_no_streamline, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
        ]

    @staticmethod
    def armors() -> List[str]:
        return [
            "Stalwart Plate",
            "Final Guard",
            "Pandemonium Plate",
            "Ornate Plate",
            "Scrounger's Suit",
            "Ballistic Armor",
            "Conjurer's Coat",
            "Brash Bracers",
            "Combo Cuirass",
            "Streamline Mail",
        ]

    @staticmethod
    def armors_no_streamline() -> List[str]:
        return [
            "Stalwart Plate",
            "Final Guard",
            "Pandemonium Plate",
            "Ornate Plate",
            "Scrounger's Suit",
            "Ballistic Armor",
            "Conjurer's Coat",
            "Brash Bracers",
            "Combo Cuirass",
        ]

    @staticmethod
    def bosses_non_final() -> List[str]:
        return [
            "Spore Knight",
            "Tinker Knight",
            "Mole Knight",
            "Hive Knight",
            "Scrap Knight",
        ]

    @staticmethod
    def worlds() -> List[str]:
        return [
            "Mushroom Mines",
            "Secret Fountain",
            "Smeltworks",
            "The Grub Pit",
            "Magic Landfill",
            "Drill Knight's Castle",
        ]

    @staticmethod
    def knightmare_level_range() -> range:
        return range(1, 11)


# Archipelago Options
# ...
