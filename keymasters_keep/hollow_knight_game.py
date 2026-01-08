from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class HollowKnightArchipelagoOptions:
    pass


class HollowKnightGame(Game):
    name = "Hollow Knight"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XONE,
    ]

    is_adult_only_or_unrated = False

    options_cls = HollowKnightArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Defeat Bosses on Radiant difficulty",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Activate BINDING before entering a Pantheon (when applicable)",
                data={
                    "BINDING": (self.bindings, 1),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Defeat BOSS",
                data={
                    "BOSS": (self.bosses, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=15,
            ),
            GameObjectiveTemplate(
                label="Defeat BOSS",
                data={
                    "BOSS": (self.bosses_difficult, 1)
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Complete the PANTHEON",
                data={
                    "PANTHEON": (self.pantheons, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete the PANTHEON",
                data={
                    "PANTHEON": (self.pantheons_difficult, 1)
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
        ]

    @staticmethod
    def bindings() -> List[str]:
        return [
            "NAIL BINDING",
            "SHELL BINDING",
            "CHARMS BINDING",
            "SOUL BINDING",
        ]

    @staticmethod
    def bosses() -> List[str]:
        return [
            "Gruz Mother, Attuned",
            "Vengefly King, Attuned",
            "Brooding Mawlek, Attuned",
            "False Knight, Attuned",
            "Failed Champion, Attuned",
            "Hornet Protector, Attuned",
            "Hornet Sentinel, Attuned",
            "Massive Moss Charger, Attuned",
            "Flukemarm, Attuned",
            "Mantis Lords, Attuned",
            "Sisters of Battle, Attuned",
            "Oblobble, Attuned",
            "Hive Knight, Attuned",
            "Broken Vessel, Attuned",
            "Lost Kin, Attuned",
            "Nosk, Attuned",
            "Winged Nosk, Attuned",
            "The Collector, Attuned",
            "God Tamer, Attuned",
            "Crystal Guardian, Attuned",
            "Enraged Guardian, Attuned",
            "Uumuu, Attuned",
            "Traitor Lord, Attuned",
            "Grey Prince Zote, Attuned",
            "Soul Warrior, Attuned",
            "Soul Master, Attuned",
            "Soul Tyrant, Attuned",
            "Dung Defender, Attuned",
            "White Defender, Attuned",
            "Watcher Knight, Attuned",
            "No Eyes, Attuned",
            "Xero, Attuned",
            "Marmu, Attuned",
            "Markoth, Attuned",
            "Galien, Attuned",
            "Gorb, Attuned",
            "Elder Hu, Attuned",
            "Oro & Markoth, Attuned",
            "Paintmaster Sheo, Attuned",
            "Nailsage Sly, Attuned",
            "Grimm, Attuned",
            "Gruz Mother, Ascended",
            "Vengefly King, Ascended",
            "Brooding Mawlek, Ascended",
            "False Knight, Ascended",
            "Hornet Protector, Ascended",
            "Massive Moss Charger, Ascended",
            "Flukemarm, Ascended",
            "Mantis Lords, Ascended",
            "Hive Knight, Ascended",
            "Broken Vessel, Ascended",
            "The Collector, Ascended",
            "Crystal Guardian, Ascended",
            "Enraged Guardian, Ascended",
            "Uumuu, Ascended",
            "Soul Warrior, Ascended",
            "Soul Master, Ascended",
            "Dung Defender, Ascended",
            "No Eyes, Ascended",
            "Xero, Ascended",
            "Marmu, Ascended",
            "Galien, Ascended",
            "Gorb, Ascended",
            "Elder Hu, Ascended",
        ]

    @staticmethod
    def bosses_difficult() -> List[str]:
        return [
            "Pure Vessel, Attuned",
            "Nightmare King, Attuned",
            "Radiance, Attuned",
            "Failed Champion, Ascended",
            "Hornet Sentinel, Ascended",
            "Sisters of Battle, Ascended",
            "Oblobble, Ascended",
            "Lost Kin, Ascended",
            "Nosk, Ascended",
            "Winged Nosk, Ascended",
            "God Tamer, Ascended",
            "Traitor Lord, Ascended",
            "Grey Prince Zote, Ascended",
            "Soul Tyrant, Ascended",
            "White Defender, Ascended",
            "Watcher Knight, Ascended",
            "Markoth, Ascended",
            "Oro & Markoth, Ascended",
            "Paintmaster Sheo, Ascended",
            "Nailsage Sly, Ascended",
            "Pure Vessel, Ascended",
            "Grimm, Ascended",
            "Nightmare King, Ascended",
            "Radiance, Ascended",
        ]

    @staticmethod
    def pantheons() -> List[str]:
        return [
            "Pantheon of the Master",
            "Pantheon of the Artist",
            "Pantheon of the Sage",
        ]

    @staticmethod
    def pantheons_difficult() -> List[str]:
        return [
            "Pantheon of the Knight",
            "Pantheon of Hallownest",
        ]


# Archipelago Options
# ...
