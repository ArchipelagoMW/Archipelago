from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class EnterTheGungeonArchipelagoOptions:
    pass


class EnterTheGungeonGame(Game):
    name = "Enter the Gungeon"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XONE,
    ]

    is_adult_only_or_unrated = False

    options_cls = EnterTheGungeonArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Use Turbo Mode",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Beat PAST",
                data={
                    "PAST": (self.gungeoneers_past, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Obtain the Master Round in AREA",
                data={
                    "AREA": (self.areas, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Beat the Lich as GUNGEONEER",
                data={
                    "GUNGEONEER": (self.gungeoneers, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Beat the High Dragun as GUNGEONEER",
                data={
                    "GUNGEONEER": (self.gungeoneers, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Beat the High Dragun in Challenge Mode as GUNGEONEER",
                data={
                    "GUNGEONEER": (self.gungeoneers, 1)
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Beat the Resourceful Rat as GUNGEONEER",
                data={
                    "GUNGEONEER": (self.gungeoneers, 1)
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Beat the High Dragun after activating the shrine in the first room as GUNGEONEER",
                data={
                    "GUNGEONEER": (self.gungeoneers, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Destroy COUNT chests as GUNGEONEER and beat the High Dragun",
                data={
                    "COUNT": (self.chest_count_range, 1),
                    "GUNGEONEER": (self.gungeoneers, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Beat the Advanced Dragun as GUNGEONEER",
                data={
                    "GUNGEONEER": (self.gungeoneers, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Beat the High Dragun while having the Sorceress' Blessing as GUNGEONEER",
                data={
                    "GUNGEONEER": (self.gungeoneers, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Buy all items in one of SHOPKEEPER",
                data={
                    "SHOPKEEPER": (self.shopkeepers, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Beat the High Dragun during a Rainbow Run as GUNGEONEER",
                data={
                    "GUNGEONEER": (self.gungeoneers, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Use the Gun Muncher as GUNGEONEER",
                data={
                    "GUNGEONEER": (self.gungeoneers, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Get up to COUNT Blanks as GUNGEONEER",
                data={
                    "COUNT": (self.blank_count_range, 1),
                    "GUNGEONEER": (self.gungeoneers, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Get up to COUNT Junk as GUNGEONEER",
                data={
                    "COUNT": (self.junk_count_range, 1),
                    "GUNGEONEER": (self.gungeoneers, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Give COUNT Hearts to the vampire as GUNGEONEER",
                data={
                    "COUNT": (self.heart_count_range, 1),
                    "GUNGEONEER": (self.gungeoneers, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Beat the Lich in Challenge Mode as GUNGEONEER",
                data={
                    "GUNGEONEER": (self.gungeoneers, 1)
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Beat the Lich after activating the shrine in the first room as GUNGEONEER",
                data={
                    "GUNGEONEER": (self.gungeoneers, 1)
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Beat the Lich during a Rainbow Run as GUNGEONEER",
                data={
                    "GUNGEONEER": (self.gungeoneers, 1)
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Get up to COUNT Armor as GUNGEONEER",
                data={
                    "COUNT": (self.junk_count_range, 1),
                    "GUNGEONEER": (self.gungeoneers_no_robot, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete a Boss Rush as GUNGEONEER",
                data={
                    "GUNGEONEER": (self.gungeoneers_no_robot, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
        ]

    @staticmethod
    def gungeoneers() -> List[str]:
        return [
            "The Bullet",
            "The Convict",
            "The Gunslinger",
            "The Hunter",
            "The Marine",
            "The Paradox",
            "The Pilot",
            "The Robot",
        ]

    @staticmethod
    def gungeoneers_past() -> List[str]:
        return [
            "The Bullet's Past",
            "The Convict's Past",
            "The Gunslinger's Past",
            "The Hunter's Past",
            "The Marine's Past",
            "The Pilot's Past",
            "The Robot's Past",
        ]

    @staticmethod
    def gungeoneers_no_robot() -> List[str]:
        return [
            "The Bullet",
            "The Convict",
            "The Gunslinger",
            "The Hunter",
            "The Marine",
            "The Paradox",
            "The Pilot",
        ]

    @staticmethod
    def areas() -> List[str]:
        return [
            "Keep Of The Lead Lord",
            "Gungeon Proper",
            "Black Powder Mine",
            "Hollow",
            "Forge",
        ]

    @staticmethod
    def areas_no_forge() -> List[str]:
        return [
            "Keep Of The Lead Lord",
            "Gungeon Proper",
            "Black Powder Mine",
            "Hollow",
        ]

    @staticmethod
    def shopkeepers() -> List[str]:
        return [
            "Trorc's Shops",
            "Professor Goopton's Shops",
            "Old Red's Shops",
            "Cursula's Shops",
            "Flint's Shops",
            "Bello's Shops",
        ]

    @staticmethod
    def chests() -> List[str]:
        return [
            "Brown Chest",
            "Blue Chest",
            "Green Chest",
            "Red Chest",
            "Black Chest",
        ]

    @staticmethod
    def chest_count_range() -> range:
        return range(2, 5)

    @staticmethod
    def blank_count_range() -> range:
        return range(4, 7)

    @staticmethod
    def junk_count_range() -> range:
        return range(2, 5)

    @staticmethod
    def heart_count_range() -> range:
        return range(2, 5)

    @staticmethod
    def armor_count_range() -> range:
        return range(3, 5)


# Archipelago Options
# ...
