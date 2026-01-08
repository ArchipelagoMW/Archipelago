from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class MegaMan11ArchipelagoOptions:
    pass


class MegaMan11Game(Game):
    name = "Mega Man 11"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XONE,
    ]

    is_adult_only_or_unrated = False

    options_cls = MegaMan11ArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        constraints: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Don't use any E-Tanks",
                data=dict(),
            ),
        ]
        return constraints

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Defeat Block Man BLOCKMANCONDITION",
                data={
                    "BLOCKMANCONDITION": (self.blockmanconditions, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Defeat Acid Man ACIDMANCONDITION",
                data={
                    "ACIDMANCONDITION": (self.acidmanconditions, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Defeat Impact Man IMPACTMANCONDITION",
                data={
                    "IMPACTMANCONDITION": (self.impactmanconditions, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Defeat Bounce Man BOUNCEMANCONDITION",
                data={
                    "BOUNCEMANCONDITION": (self.bouncemanconditions, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Defeat Fuse Man FUSEMANCONDITION",
                data={
                    "FUSEMANCONDITION": (self.fusemanconditions, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Defeat Tundra Man TUNDRAMANCONDITION",
                data={
                    "TUNDRAMANCONDITION": (self.tundramanconditions, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Defeat Torch Man TORCHMANCONDITION",
                data={
                    "TORCHMANCONDITION": (self.torchmanconditions, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Defeat Blast Man BLASTMANCONDITION",
                data={
                    "BLASTMANCONDITION": (self.blastmanconditions, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete STAGE without dying",
                data={
                    "STAGE": (self.stages, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Get SHOPITEM from the Shop",
                data={
                    "SHOPITEM": (self.shopitems, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Get the UPGRADE from the Shop",
                data={
                    "UPGRADE": (self.upgrades, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
        ]

    @staticmethod
    def blockmanconditions() -> List[str]:
        return [
            "with only Mega Buster",
            "with Chain Blast",
            "with Double Gear active",
            "with only Speed Gear",
            "without using Gears",
        ]
        
    @staticmethod
    def acidmanconditions() -> List[str]:
        return [
            "with only Mega Buster",
            "with Block Dropper",
            "with Double Gear active",
            "with only Power Gear",
            "without using Gears",
        ]
        
    @staticmethod
    def impactmanconditions() -> List[str]:
        return [
            "with only Mega Buster",
            "with Acid Barrier",
            "with Double Gear active",
            "with only Speed Gear",
            "without using Gears",
        ]

    @staticmethod
    def bouncemanconditions() -> List[str]:
        return [
            "with only Mega Buster",
            "with Pile Driver",
            "with Double Gear active",
            "with only Power Gear",
            "without using Gears",
        ]
        
    @staticmethod
    def fusemanconditions() -> List[str]:
        return [
            "with only Mega Buster",
            "with Bounce Ball",
            "with Double Gear active",
            "with only Power Gear",
            "without using Gears",
        ]
        
    @staticmethod
    def tundramanconditions() -> List[str]:
        return [
            "with only Mega Buster",
            "with Scramble Thunder",
            "with Double Gear active",
            "with only Power Gear",
            "without using Gears",
        ]
        
    @staticmethod
    def torchmanconditions() -> List[str]:
        return [
            "with only Mega Buster",
            "with Tundra Storm",
            "with Double Gear active",
            "with only Speed Gear",
            "without using Gears",
        ]
        
    @staticmethod
    def blastmanconditions() -> List[str]:
        return [
            "with only Mega Buster",
            "with Blazing Torch",
            "with Double Gear active",
            "with only Speed Gear",
            "without using Gears",
        ]
        
    @staticmethod
    def stages() -> List[str]:
        return [
            "Block Man's Stage",
            "Acid Man's Stage",
            "Impact Man's Stage",
            "Bounce Man's Stage",
            "Fuse Man's Stage",
            "Tundra Man's Stage",
            "Torch Man's Stage",
            "Blast Man's Stage",
        ]
        
    @staticmethod
    def shopitems() -> List[str]:
        return [
            "3 Eddie Calls",
            "3 Beat Calls",
            "an Energy Tank",
            "a Weapon Tank",
            "a Mystery Tank",
            "a Life",
            "3 Pierce Protectors",
            "a Super Guard",
        ]
        
    @staticmethod
    def upgrades() -> List[str]:
        return [
            "Energy Balancer",
            "Energy Balancer Neo",
            "Auto Charge Chip",
            "Buster Plus Chip",
            "Power Shield",
            "Spike Boots",
            "Shock Absorber",
            "Speed Gear Booster",
            "Energy Dispenser",
            "Awakener Chip",
            "Bolt Catcher",
            "Energy Catcher",
            "Capsule Catcher",
            "Cooling System",
            "Cooling System Infinite",
            "Mystery Chip",
            "Buddy Call Plus",
            "Tank Container",
        ]

# Archipelago Options
# ...
