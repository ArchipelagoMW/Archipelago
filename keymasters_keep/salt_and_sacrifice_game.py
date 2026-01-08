from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class SaltAndSacrificeArchipelagoOptions:
    pass


class SaltAndSacrificeGame(Game):
    name = "Salt and Sacrifice"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.SW,
    ]

    is_adult_only_or_unrated = False

    options_cls = SaltAndSacrificeArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Cannot use these Weapon Types: WEAPON_TYPES",
                data={
                    "WEAPON_TYPES": (self.weapon_types, 5),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Defeat a Mage in WORLD",
                data={
                    "WORLD": (self.worlds, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Defeat BOSS in the Heart of Altarstone",
                data={
                    "BOSS": (self.bosses_altarstone, 1)
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Defeat BOSS in Ashbourne Village",
                data={
                    "BOSS": (self.bosses_ashbourne, 1)
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Defeat BOSS in Bol Gerahn",
                data={
                    "BOSS": (self.bosses_bol, 1)
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Defeat BOSS in Corvius' Mire",
                data={
                    "BOSS": (self.bosses_corvius, 1)
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Defeat BOSS in Dreadstone Peak",
                data={
                    "BOSS": (self.bosses_dreadstone, 1)
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Defeat BOSS in Elder Copse",
                data={
                    "BOSS": (self.bosses_elder, 1)
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Defeat BOSS using WEAPON_TYPE",
                data={
                    "BOSS": (self.bosses, 1),
                    "WEAPON_TYPE": (self.weapon_types, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Defeat BOSS using a weapon you aren't proficient with",
                data={
                    "BOSS": (self.bosses, 1)
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Locate the TOOLS and pick it up",
                data={
                    "TOOLS": (self.tools, 1)
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
        ]

    @staticmethod
    def worlds() -> List[str]:
        return [
            "Ashbourne Village",
            "Bol Gerahn",
            "Corvius' Mire",
            "Dreadstone Peak",
            "Elder Copse",
            "Hallowed Hill",
            "Heart of Altarstone",
        ]

    @staticmethod
    def bosses_altarstone() -> List[str]:
        return [
            "The Keeper and the Kin",
            "Shirenna, True Herbalist",
            "The Four Divines",
            "Barix, First of the Marked",
        ]

    @staticmethod
    def bosses_ashbourne() -> List[str]:
        return [
            "Arzhan-Tin, The Ceaseless Fury",
            "Celus Zend, The Mourning Winter",
            "Ekriks Graycloud, The Precipice of Chaos",
            "Kundry Kahn, The Drowned Behemoth",
            "The Green Huntsman",
            "Uryks Necklace-of-Ears",
        ]

    @staticmethod
    def bosses_bol() -> List[str]:
        return [
            "Aur Cyrus, the Wild Pandemonium",
            "Nix Ocifiris, Caretaker of Dry Bones",
            "Padra Sakrev, Bearer of Guilt",
            "Sto'h Karrig, The Immovable Bastion",
            "The Hate-Cursed Matriarch",
            "The Tireless Exalted",
            "Ture Vasari, The Blood-Drunk Blade",
        ]

    @staticmethod
    def bosses_corvius() -> List[str]:
        return [
            "Anamus Kane, The Infernal Machine",
            "Ghor Lorhotha, Wearer of Tortured Flesh",
            "Luxian Steel-Glass, The Blind and Blinding",
            "Marega Gredanya",
            "Por Myec, The Encroaching Rot",
            "Sapblood Heart",
        ]

    @staticmethod
    def bosses_dreadstone() -> List[str]:
        return [
            "Draeaxenerion, The Scaled Nobility",
            "Nephael Mos, Knight of the Chasm",
            "Inquisitor Selet",
            "Kraeaxenar, Wyrm of Sky",
            "The Two That Remain",
            "Vodin Tenebre, The Lurking Shadow",
            "Zaruman Tam, The Wraith Temporal",
            "Zyzak Zuun, The Curse-Riddle Mind",
        ]

    @staticmethod
    def bosses_elder() -> List[str]:
        return [
            "Icon of Pandemonium",
            "Inquisitor Amben",
            "Logostus Rime, Undying Scholar",
            "Parxa Krass, Force Incarnate",
            "The Undone Sacrifice",
            "The Worm That Does Not Die",
        ]

    def bosses(self) -> List[str]:
        return sorted(
            self.bosses_altarstone()
            + self.bosses_ashbourne()
            + self.bosses_bol()
            + self.bosses_corvius()
            + self.bosses_dreadstone()
            + self.bosses_elder()
        )

    @staticmethod
    def weapon_types() -> List[str]:
        return [
            "Bludgeons",
            "Glaives",
            "Greatblades",
            "Greathammers",
            "Halfspears",
            "Highblades",
            "Rapiers",
            "Sickles",
            "Staves",
            "Twindaggers",
            "Twohanders",
            "Vanguards",
            "Whips",
            "Channeling Rods",
            "Crossbows",
            "Shortbows",
            "Divine Glyphs (Prayer)",  # The distinction between the two magics are important, as they required skills to use.
            "Forbidden Glyphs (Arcane)",
            "Thrown Weapons",  # Includes Axes, Daggers, and other objects under the Thrown class.
        ]

    @staticmethod
    def tools() -> List[str]:
        return [
            "Grappling Hook",  # Ashbourne Village
            "Magnesin Supply",  # Bol Gerahn
            "Luminstone",  # Corvius' Mire
            "Ethercloth Bolt",  # Dreadstone Peak
        ]

# Archipelago Options
# ...
