from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class CobaltCoreArchipelagoOptions:
    pass


class CobaltCoreGame(Game):
    name = "Cobalt Core"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.SW,
    ]

    is_adult_only_or_unrated = False

    options_cls = CobaltCoreArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a game with CHARACTERS in the SHIP on DIFFICULTY difficulty or higher",
                data={
                    "CHARACTERS": (self.characters, 3),
                    "SHIP": (self.ships, 1),
                    "DIFFICULTY": (self.difficulties, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Win a game with CHARACTER in the SHIP on DIFFICULTY difficulty or higher",
                data={
                    "CHARACTER": (self.characters, 1),
                    "SHIP": (self.ships, 1),
                    "DIFFICULTY": (self.difficulties_more, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win a game CHALLENGE",
                data={
                    "CHALLENGE": (self.challenges, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Finish ZONE with CHARACTERS on DIFFICULTY difficulty or higher",
                data={
                    "ZONE": (self.zones, 1),
                    "CHARACTERS": (self.characters, 2),
                    "DIFFICULTY": (self.difficulties, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Finish ZONE with SHIP on DIFFICULTY difficulty or higher",
                data={
                    "ZONE": (self.zones, 1),
                    "SHIP": (self.ships, 1),
                    "DIFFICULTY": (self.difficulties, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Finish ZONE with CHARACTERS on DIFFICULTY difficulty or higher",
                data={
                    "ZONE": (self.zones, 1),
                    "CHARACTERS": (self.characters, 2),
                    "DIFFICULTY": (self.difficulties_more, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Finish ZONE with SHIP on DIFFICULTY difficulty or higher",
                data={
                    "ZONE": (self.zones, 1),
                    "SHIP": (self.ships, 1),
                    "DIFFICULTY": (self.difficulties_more, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Defeat BOSS with CHARACTER in the SHIP",
                data={
                    "BOSS": (self.bosses, 1),
                    "CHARACTER": (self.characters, 1),
                    "SHIP": (self.ships, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Defeat ELITE with CHARACTER in the SHIP",
                data={
                    "ELITE": (self.elites, 1),
                    "CHARACTER": (self.characters, 1),
                    "SHIP": (self.ships, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete MOD with the SHIP",
                data={
                    "MOD": (self.ship_mods, 1),
                    "SHIP": (self.ships, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete EVENT with CHARACTER",
                data={
                    "EVENT": (self.events, 1),
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
        ]

    @staticmethod
    def characters() -> List[str]:
        return [
            "Dizzy",
            "Riggs",
            "Peri",
            "Isaac",
            "Drake",
            "Max",
            "Books",
            "//cat.exe",
        ]

    @staticmethod
    def ships() -> List[str]:
        return [
            "Artemis",
            "Ares",
            "Jupiter",
            "Gemini",
            "Tiderunner",
        ]

    @staticmethod
    def zones() -> List[str]:
        return [
            "Zone 1: Lazuli Nebula",
            "Zone 2: Sapphire Cluster",
            "Zone 3: Void's Cradle",
        ]

    @staticmethod
    def bosses() -> List[str]:
        return [
            "Crystalline Entity",
            "The Dreadnought",
            "The Cobalt",
        ]

    @staticmethod
    def elites() -> List[str]:
        return [
            "The Humble Approach",
            "Fireball",
            "Needler",
            "Crystalline Offshoot",
            "Rogue Starnacle",
            "Rusting Colossus",
            "Buried(?) Relic",
        ]

    @staticmethod
    def events() -> List[str]:
        return [
            "Sports!",
            "Missile Mayhem",
            "Grandma's Bakery and Weapons Market",
            "Upcycling Program",
            "Crystallized Crew",
            "Extra-Planar Being",
            "Your Old Friend Dracula",
            "Offering from Another Timeline",
            "The Duplitron",
            "Annoying Debate",
        ]

    @staticmethod
    def challenges() -> List[str]:
        return [
            "removing 5 or more cards from your deck",
            "with maximum hull of 20 or more",
        ]

    @staticmethod
    def ship_mods() -> List[str]:
        return [
            "Abandoned Shipyard",
            "Extra Scaffold",
            "Ship Shuffler",
            "Worthwhile Trade Repairs",
        ]

    @staticmethod
    def difficulties() -> List[str]:
        return [
            "Normal",
            "Hard",
        ]

    @staticmethod
    def difficulties_more() -> List[str]:
        return [
            "Harder",
            "Hardest",
        ]

# Archipelago Options
# ...
