from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class TowerTacticsLiberationArchipelagoOptions:
    pass


class TowerTacticsLiberationGame(Game):
    name = "Tower Tactics: Liberation"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = TowerTacticsLiberationArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Unequip all Sanctuary items",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="You must choose only one reward to take from post-battle rewards",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="You cannot place towers on TILECOLOR tiles",
                data={
                    "TILECOLOR": (self.tilecolors, 1)
                },
            ),
            GameObjectiveTemplate(
                label="You cannot use towers that cost MANA",
                data={
                    "MANA": (self.manacosts, 1)
                },
            ),
            GameObjectiveTemplate(
                label="You cannot go to NODETYPE",
                data={
                    "NODETYPE": (self.nodetype, 1)
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a run with DECK",
                data={
                    "DECK": (self.decks, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Win a run with DECK on ascension ASCENSIONNUM",
                data={
                    "DECK": (self.decks, 1),
                    "ASCENSIONNUM": (self.ascensionnum, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
        ]

    @staticmethod
    def tilecolors() -> List[str]:
        return [
            "grey",
            "non-grey",
        ]

    @staticmethod
    def manacosts() -> List[str]:
        return [
            "0",
            "1",
            "2",
            "3+"
        ]

    @staticmethod
    def nodetype() -> List[str]:
        return [
            "elites",
            "shops",
            "rest sites",
            "forges",
            "events and hordes",
        ]

    @staticmethod
    def decks() -> List[str]:
        return [
            "Leading Legacy",
            "Wandering Colossus",
            "Holy Guild",
            "Everchanging",
            "Resonating Echoes",
            "Air Support",
            "Early Bird",
            "Ace in the Hole",
            "Deprived Soul",
            "Broken Legacy",
            "Ravenous Reaper",
            "Punished Martyr",
            "Singleton Master",
            "Arcane Master",
            "Antiquarian",
            "Summit Slayer",
            "Earth Fairy",
            "Lost Soul",
            "Fading Consciousness",
            "Illusionist",
            "Nuke Town",
            "Shield Master",
            "Wanted Fugitive",
            "Crimson Ascent",
            "The Duelist",
            "The Engineer",
            "Grand Master",
            "Twin Caster",
            "Disco Infinity",
        ]

    @staticmethod
    def ascensionnum() -> range:
        return range(1, 15)

# Archipelago Options
# ...
