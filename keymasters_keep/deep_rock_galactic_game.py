from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class DeepRockGalacticArchipelagoOptions:
    pass


class DeepRockGalacticGame(Game):
    name = "Deep Rock Galactic"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = False

    options_cls = DeepRockGalacticArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Set Hazard Level to LEVEL",
                data={
                    "LEVEL": (self.hazard_levels, 1),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Beat 1x MISSION_TYPE mission as Driller. Primary: PRIMARY  Secondary: SECONDARY  Throwable: THROWABLE",
                data={
                    "MISSION_TYPE": (self.mission_types, 1),
                    "PRIMARY": (self.weapons_primary_driller, 1),
                    "SECONDARY": (self.weapons_secondary_driller, 1),
                    "THROWABLE": (self.throwables_driller, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Beat 1x MISSION_TYPE mission as Engineer. Primary: PRIMARY  Secondary: SECONDARY  Throwable: THROWABLE",
                data={
                    "MISSION_TYPE": (self.mission_types, 1),
                    "PRIMARY": (self.weapons_primary_engineer, 1),
                    "SECONDARY": (self.weapons_secondary_engineer, 1),
                    "THROWABLE": (self.throwables_engineer, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Beat 1x MISSION_TYPE mission as Gunner. Primary: PRIMARY  Secondary: SECONDARY  Throwable: THROWABLE",
                data={
                    "MISSION_TYPE": (self.mission_types, 1),
                    "PRIMARY": (self.weapons_primary_gunner, 1),
                    "SECONDARY": (self.weapons_secondary_gunner, 1),
                    "THROWABLE": (self.throwables_gunner, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Beat 1x MISSION_TYPE mission as Scout. Primary: PRIMARY  Secondary: SECONDARY  Throwable: THROWABLE",
                data={
                    "MISSION_TYPE": (self.mission_types, 1),
                    "PRIMARY": (self.weapons_primary_scout, 1),
                    "SECONDARY": (self.weapons_secondary_scout, 1),
                    "THROWABLE": (self.throwables_scout, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Beat a random mission with the following mutators: MUTATORS",
                data={
                    "MUTATORS": (self.mutators, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Beat a Deep Dive with the CLASS",
                data={
                    "CLASS": (self.classes, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Beat an Elite Deep Dive with the CLASS",
                data={
                    "CLASS": (self.classes, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
        ]

    @staticmethod
    def hazard_levels() -> range:
        return range(1, 6)

    @staticmethod
    def mission_types() -> List[str]:
        return [
            "Deep Scan",
            "Egg Hunt",
            "Elimination",
            "Escort Duty",
            "Industrial Sabotage",
            "Mining Expedition",
            "On-site Refining",
            "Point Extraction",
            "Salvage Operation",
        ]

    @staticmethod
    def weapons_primary_driller() -> List[str]:
        return [
            "CRSPR Flamethrower",
            "Corrosive Sludge Pump",
            "Cryo Cannon",
        ]

    @staticmethod
    def weapons_secondary_driller() -> List[str]:
        return [
            "Colette Wave Cooker",
            "Experimental Plasma Charger",
            "Subata 120",
        ]

    @staticmethod
    def throwables_driller() -> List[str]:
        return [
            "High Explosive Grenade",
            "Impact Axe",
            "Neurotoxin Grenade",
            "Springloaded Ripper",
        ]

    @staticmethod
    def weapons_primary_engineer() -> List[str]:
        return [
            "'Stubby' Voltaic SMG",
            "'Warthog' Auto 210",
            "LOK-1 Smart Rifle",
        ]

    @staticmethod
    def weapons_secondary_engineer() -> List[str]:
        return [
            "Breach Cutter",
            "Deepcore 40mm PGL",
            "Shard Diffractor",
        ]

    @staticmethod
    def throwables_engineer() -> List[str]:
        return [
            "L.U.R.E.",
            "Plasma Burster",
            "Proximity Mine",
            "Shredder Swarm",
        ]

    @staticmethod
    def weapons_primary_gunner() -> List[str]:
        return [
            "'Hurricane' Guided Rocket System",
            "'Lead Storm' Powered Minigun",
            "'Thunderhead' Heavy Autocannon",
        ]

    @staticmethod
    def weapons_secondary_gunner() -> List[str]:
        return [
            "'Bulldog' Heavy Revolver",
            "ArmsKore Coil Gun",
            "BRT7 Burst Fire Gun",
        ]

    @staticmethod
    def throwables_gunner() -> List[str]:
        return [
            "Cluster Grenade",
            "Incendiary Grenade",
            "Sticky Grenade",
            "Tactical Leadburster",
        ]

    @staticmethod
    def weapons_primary_scout() -> List[str]:
        return [
            "DRAK-25 Plasma Carbine",
            "Deepcore GK2",
            "M1000 Classic",
        ]

    @staticmethod
    def weapons_secondary_scout() -> List[str]:
        return [
            "Jury-Rigged Boomstick",
            "Nishanka Boltshark X-80",
            "Zhukov NUK17",
        ]

    @staticmethod
    def throwables_scout() -> List[str]:
        return [
            "Cryo Grenade",
            "Inhibitor-Field Generator",
            "Pheromone Canister",
            "Voltaic Stun SweepeR",
        ]

    @staticmethod
    def mutators() -> List[str]:
        return [
            "1 Warning",
            "1 Anomaly",
            "1 Warning, 1 Anomaly",
            "2 Warnings",
        ]

    @staticmethod
    def classes() -> List[str]:
        return [
            "Driller",
            "Engineer",
            "Gunner",
            "Scout",
        ]


# Archipelago Options
# ...
