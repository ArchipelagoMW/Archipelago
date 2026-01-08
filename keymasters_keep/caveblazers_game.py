from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class CaveblazersArchipelagoOptions:
    pass


class CaveblazersGame(Game):
    name = "Caveblazers"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.SW,
    ]

    is_adult_only_or_unrated = False

    options_cls = CaveblazersArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Set Game Speed to 150%, and CHALLENGE",
                data={
                    "CHALLENGE": (self.challenge, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Set Enemy STAT to max, and CHALLENGE",
                data={
                    "STAT": (self.enemystat, 1),
                    "CHALLENGE": (self.challenge, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Set ITEMBLESSING count to Less/More, and CHALLENGE",
                data={
                    "ITEMBLESSING": (self.itemblessing, 1),
                    "CHALLENGE": (self.challenge, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Set boss damage to 150%, boss rewards to Less, and CHALLENGE",
                data={
                    "CHALLENGE": (self.challenge, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Use the Adventurer perk, discarding the items it gives you, and CHALLENGE",
                data={
                    "CHALLENGE": (self.challenge, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Disable Slime, Large Slime, Bat, Jumper, Hobgoblin, and Goblin. Enable all other enemies, as well as Monster Mashup",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a run using the PERK perk",
                data={
                    "PERK": (self.perks, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Win a run using the PERK perk and RELICS enabled",
                data={
                    "PERK": (self.perks, 1),
                    "RELICS": (self.relics, 2),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=4,
            ),
        ]

    @staticmethod
    def challenge() -> List[str]:
        return [
            "enable More Orcs",
            "enable Time Limit",
            "enable Less Food",
            "enable Less Treasure",
            "enable No Altars",
            "enable No Health Shrines",
            "enable Pay For Blessings",
            "enable Take More Damage",
            "enable Gatekeeper",
            "enable Larger Levels, and increase Level Count to 3",
            "enable Experimental Items",
            "decrease Level Count to 1",
        ]

    @staticmethod
    def perks() -> List[str]:
        return [
            "Adventurer",
            "Archer",
            "Twofold",
            "Sorcerer",
            "Sticky Pete",
            "Juggernaut",
            "Elementalist",
            "Cleric",
            "Dashy Joe",
            "Springy",
            "Slasher",
            "Trader",
            "Traditionalist",
            "Explosive",
            "Heavy Hitter",
            "Vampire",
            "Reaper",
            "Protection",
            "Dual Wield",
            "Vortex",
            "Swordsman",
            "Brimstone",
            "Nimrod",
            "Runemaster",
        ]

    @staticmethod
    def relics() -> List[str]:
        return [
            "Arrowhead",
            "Paragon",
            "Twilight",
            "Blackjack",
            "Oblivion",
        ]

    @staticmethod
    def enemystat() -> List[str]:
        return [
            "Frequency",
            "Health",
            "Damage",
            "Reactions",
        ]

    @staticmethod
    def itemblessing() -> List[str]:
        return [
            "Item/Blessing",
            "Blessing/Item",
        ]

# Archipelago Options
# ...
