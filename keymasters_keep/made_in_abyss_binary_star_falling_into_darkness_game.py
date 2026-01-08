from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class MadeInAbyssBinaryStarFallingIntoDarknessArchipelagoOptions:
    pass


class MadeInAbyssBinaryStarFallingIntoDarknessGame(Game):
    name = "Made in Abyss: Binary Star Falling into Darkness"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.SW,
    ]

    is_adult_only_or_unrated = True

    options_cls = MadeInAbyssBinaryStarFallingIntoDarknessArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Only use melee against creatures",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Only use ranged against creatures",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Do not use any consumables",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Do not fast travel",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Defeat COUNTx CREATURE in Layer 1",
                data={
                    "COUNT": (self.creature_count_range, 1),
                    "CREATURE": (self.creatures_layer_1, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Defeat COUNTx CREATURE in Layer 2",
                data={
                    "COUNT": (self.creature_count_range, 1),
                    "CREATURE": (self.creatures_layer_2, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Defeat COUNTx CREATURE in Layer 3",
                data={
                    "COUNT": (self.creature_count_range, 1),
                    "CREATURE": (self.creatures_layer_3, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Defeat COUNTx CREATURE in Layer 4",
                data={
                    "COUNT": (self.creature_count_range, 1),
                    "CREATURE": (self.creatures_layer_4, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Defeat COUNTx CREATURE in Layer 5",
                data={
                    "COUNT": (self.creature_count_range, 1),
                    "CREATURE": (self.creatures_layer_5, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Obtain COUNTx RELIC in Layer 1",
                data={
                    "COUNT": (self.relic_count_range, 1),
                    "RELIC": (self.relics_layer_1, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Obtain COUNTx RELIC in Layer 2",
                data={
                    "COUNT": (self.relic_count_range, 1),
                    "RELIC": (self.relics_layer_2, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Obtain COUNTx RELIC in Layer 3",
                data={
                    "COUNT": (self.relic_count_range, 1),
                    "RELIC": (self.relics_layer_3, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Obtain COUNTx RELIC in Layer 4",
                data={
                    "COUNT": (self.relic_count_range, 1),
                    "RELIC": (self.relics_layer_4, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Obtain COUNTx RELIC in Layer 5",
                data={
                    "COUNT": (self.relic_count_range, 1),
                    "RELIC": (self.relics_layer_5, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Defeat COUNTx CREATURE",
                data={
                    "COUNT": (self.creature_count_range, 1),
                    "CREATURE": (self.creatures_difficult, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
        ]

    @staticmethod
    def creatures_layer_1() -> List[str]:
        return [
            "Man-toyer",
            "Strength-sucker",
            "Vine-stopper",
            "Stinger",
            "Hammerbeak",
            "Tachikanata",
            "Horncier",
            "Silkfang",
            "Vine-binder",
            "Vine-binder (Subspecies)",
        ]

    @staticmethod
    def creatures_layer_2() -> List[str]:
        return [
            "Foreign Cave Raiders",
            "Strength-sucker",
            "Vine-stopper",
            "Stinger (Ancestor)",
            "Tachikanata (Azure)",
            "Horncier (Ancestor)",
            "Akatsuso",
            "Aotsuso",
            "Yomotsubi",
            "Vine-binder",
            "Vine-binder (Subspecies)",
            "Vine-blaster (Green)",
            "Vine-blaster (Blue)",
            "Pupa-carrier",
            "Spikewalker",
            "Inbyo",
            "Valley Croaker",
            "Valley Croaker (Jumper)",
            "Valley Croaker (Extreme)",
            "Giant-hammerbeak",
            "Ottabas",
            "Corpse-weeper",
        ]

    @staticmethod
    def creatures_layer_3() -> List[str]:
        return [
            "Strength-sucker",
            "Tachikanata (Ancestor)",
            "Yomotsubi (Ancestor)",
            "Vine-binder (Subspecies)",
            "Rock-licker",
            "End-jumper",
            "Neritantan",
            "Rock-walker",
            "Mountain-spinner",
            "Mountain-spinner (Fire)",
            "Mountain-spinner (Ice)",
        ]

    @staticmethod
    def creatures_layer_4() -> List[str]:
        return [
            "Man-toyer (Rare)",
            "Vine-stopper",
            "Stinger (Subspecies)",
            "Horncier (Subspecies)",
            "Akatsutsuso",
            "Aotsutsuso",
            "Yomotsubi (Rare)",
            "Vine-blaster (Red)",
            "Pupa-carrier (Rare)",
            "Head-tail",
            "End-jumper",
            "Amaranthine-deceptor",
            "Shroombear",
            "Light-eater",
            "Kudara",
            "Orb Piercer",
        ]

    @staticmethod
    def creatures_layer_5() -> List[str]:
        return [
            "Foreign Cave Raiders",
            "Pupa-carrier (Rare)",
            "Head-tail (Subspecies)",
            "Amaranthine-deceptor",
            "Kudara (Shadow)",
            "Octoliar",
            "Swarm Shocker (Blue)",
            "Swarm Shocker (Purple)",
            "Swarm Shocker (Orange)",
            "Footing Slicer",
            "Stingerhead",
            "Tidal-freezer",
            "Ink Flower",
            "Inter. Device",
        ]

    @staticmethod
    def creatures_difficult() -> List[str]:
        return [
            "Crimson Splitjaw",
            "Madojak",
        ]

    @staticmethod
    def relics_layer_1() -> List[str]:
        return [
            "Sun Sphere (1st Layer)",
            "Princess Bosom",
            "Horizontal Layer Board",
            "Vertical Layer Board",
        ]

    @staticmethod
    def relics_layer_2() -> List[str]:
        return [
            "Sun Sphere (2nd Layer)",
            "Fox Bone",
            "Pulled Teeth",
            "Mushroom Ball",
        ]

    @staticmethod
    def relics_layer_3() -> List[str]:
        return [
            "Sun Sphere (3rd Layer)",
            "Offering",
            "Stress Ball",
            "Tangled Fluid",
        ]

    @staticmethod
    def relics_layer_4() -> List[str]:
        return [
            "Sun Sphere (4th Layer)",
            "Ferrous Sphere",
            "Shatter Pot",
            "Ugly Spinner",
            "Ivy Badge",
        ]

    @staticmethod
    def relics_layer_5() -> List[str]:
        return [
            "Sun Sphere (5th Layer)",
            "Double-Bell Ball",
            "Maze Twine",
            "Spiraling Heat Stone",
        ]

    @staticmethod
    def creature_count_range() -> range:
        return range(1, 7)

    @staticmethod
    def relic_count_range() -> range:
        return range(1, 6)


# Archipelago Options
# ...
