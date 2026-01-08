from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class SynthetikLegionRisingArchipelagoOptions:
    pass


class SynthetikLegionRisingGame(Game):
    name = "Synthetik: Legion Rising"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = SynthetikLegionRisingArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Don't purchase shop items",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Instead of VR Chambers, survive the Armageddon Chamber",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="You YODA use WEAPONTYPE weapons",
                data={
                    "YODA": (self.yoda, 1),
                    "WEAPONTYPE": (self.weapontype, 3),
                },
            ),
            GameObjectiveTemplate(
                label="Enable DIFFICULTY",
                data={
                    "DIFFICULTY": (self.difficulty, 3),
                },
            ),
            GameObjectiveTemplate(
                label="Replace your starting items and modules with module cores",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="You must take two starting items. Trash both at the start of the run",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Randomize your starting modules: Take modules MODNUM",
                data={
                    "MODNUM": (self.modnum, 2),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Clear the VR Chambers with CLASS",
                data={
                    "CLASS": (self.classes, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
        ]

    @staticmethod
    def classes() -> List[str]:
        return [
            "Riot Guard",
            "Breacher",
            "Sniper",
            "Assassin",
            "Raider",
            "Heavy Gunner",
            "Engineer",
            "Demolitionist",
        ]

    @staticmethod
    def modnum() -> range:
        return range(1, 15)

    @staticmethod
    def difficulty() -> List[str]:
        return [
            "Flinch",
            "Scorching",
            "Haste",
            "Deflect",
            "Hard Core 1",
            "Critical",
            "Fragile",
            "Lightning Start",
        ]

    @staticmethod
    def weapontype() -> List[str]:
        return [
            "Pistols",
            "SMGs",
            "Assault Rifles",
            "Shotguns",
            "Marksman/Sniper Rifles",
            "Machine Guns",
            "Launchers",
            "Special",
        ]

    @staticmethod
    def yoda() -> List[str]:
        return [
            "can only",
            "cannot",
        ]

# Archipelago Options
# ...
