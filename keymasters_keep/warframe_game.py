from __future__ import annotations

import functools

from typing import List

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class WarframeArchipelagoOptions:
    warframe_warframes_owned: WarframeWarframesOwned
    warframe_weapon_types_owned: WarframeWeaponTypesOwned


class WarframeGame(Game):
    # Initial Proposal by @pantscada on Discord

    name = "Warframe"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.AND,
        KeymastersKeepGamePlatforms.IOS,
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = True

    options_cls = WarframeArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete a Bounty for SYNDICATE",
                data={
                    "SYNDICATE": (self.syndicates, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Last 20 minutes in any Survival mission as WARFRAME",
                data={
                    "WARFRAME": (self.warframes, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Last 20 waves in any Defense mission as WARFRAME",
                data={
                    "WARFRAME": (self.warframes, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete a Kuva Siphon as WARFRAME using a WEAPON_TYPE weapon",
                data={
                    "WARFRAME": (self.warframes, 1),
                    "WEAPON_TYPE": (self.weapon_types, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Open a relic in a Void Storm",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete a Nightmare Mode mission as WARFRAME",
                data={
                    "WARFRAME": (self.warframes, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Hijack or destroy a Crewship in Empyrean",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Open COUNT VOID_RELICS relic(s)",
                data={
                    "COUNT": (self.void_relic_count_range, 1),
                    "VOID_RELICS": (self.void_relics, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete 8 stages of (Elite) Sanctuary Onslaught as WARFRAME",
                data={
                    "WARFRAME": (self.warframes, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete 4 stages of The Circuit as WARFRAME",
                data={
                    "WARFRAME": (self.warframes, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Catch a fish in OPEN_WORLD",
                data={
                    "OPEN_WORLD": (self.open_worlds, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete a MISSION_TYPE mission with only a WEAPON_TYPE weapon equipped",
                data={
                    "MISSION_TYPE": (self.mission_types, 1),
                    "WEAPON_TYPE": (self.weapon_types, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Complete Capture mission in under 2 minutes as WARFRAME",
                data={
                    "WARFRAME": (self.warframes, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete a MISSION_TYPE mission in the Steel Path",
                data={
                    "MISSION_TYPE": (self.mission_types, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Defeat a Kuva Lich with progenitor WARFRAME",
                data={
                    "WARFRAME": (self.warframes, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Defeat a Sister of Parvos with progenitor WARFRAME",
                data={
                    "WARFRAME": (self.warframes, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete an Arbitration mission as WARFRAME with the currently buffed items (if possible)",
                data={
                    "WARFRAME": (self.warframes, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
        ]

    @property
    def warframes_owned(self) -> List[str]:
        return sorted(self.archipelago_options.warframe_warframes_owned.value)

    @property
    def weapon_types_owned(self) -> List[str]:
        return sorted(self.archipelago_options.warframe_weapon_types_owned.value)

    @functools.cached_property
    def warframes_all(self) -> List[str]:
        return [
            "Ash",
            "Atlas",
            "Banshee",
            "Baruuk",
            "Caliban",
            "Chroma",
            "Citrine",
            "Cyte-09",
            "Dagath",
            "Dante",
            "Ember",
            "Equinox",
            "Excalibur (Umbra)",
            "Frost",
            "Gara",
            "Garuda",
            "Gauss",
            "Grendel",
            "Gyre",
            "Harrow",
            "Hildryn",
            "Hydroid",
            "Inaros",
            "Ivara",
            "Jade",
            "Khora",
            "Koumei",
            "Kullervo",
            "Lavos",
            "Limbo",
            "Loki",
            "Mag",
            "Mesa",
            "Mirage",
            "Nekros",
            "Nezha",
            "Nidus",
            "Nova",
            "Nyx",
            "Oberon",
            "Octavia",
            "Protea",
            "Qorvex",
            "Revenant",
            "Rhino",
            "Saryn",
            "Sevagoth",
            "Styanax",
            "Titania",
            "Trinity",
            "Valkyr",
            "Vauban",
            "Volt",
            "Voruna",
            "Wisp",
            "Wukong",
            "Xaku",
            "Yareli",
            "Zephyr",
        ]

    def warframes(self) -> List[str]:
        return self.warframes_owned

    @functools.cached_property
    def weapon_types_all(self) -> List[str]:
        return [
            "Automatic",
            "Beam",
            "Blade and Whip",
            "Bow",
            "Burst Fire",
            "Charge",
            "Claws",
            "Dagger",
            "Dual Daggers",
            "Dual Held Secondary",
            "Dual Swords",
            "Fists",
            "Glaive",
            "Gunblade",
            "Hammer",
            "Heavy Blade",
            "Machete",
            "Nikana",
            "Nunchaku",
            "Polearm",
            "Rapier",
            "Rifle",
            "Scythe",
            "Semi-Automatic",
            "Shotgun",
            "Single Held Secondary",
            "Sniper",
            "Sparring",
            "Speargun",
            "Staff",
            "Sword and Shield",
            "Sword",
            "Thrown",
            "Tonfa",
            "Whip",
        ]

    def weapon_types(self) -> List[str]:
        return self.weapon_types_owned

    @staticmethod
    def syndicates() -> List[str]:
        return [
            "Cavia",
            "Entrati",
            "Ostron",
            "Solaris United",
            "The Hex",
            "The Holdfasts",
        ]

    @staticmethod
    def void_relics() -> List[str]:
        return [
            "Axi",
            "Kuva",
            "Lith",
            "Meso",
            "Neo",
        ]

    @staticmethod
    def void_relic_count_range() -> range:
        return range(1, 6)

    @staticmethod
    def open_worlds() -> List[str]:
        return [
            "Cambion Drift",
            "Duviri",
            "Orb Vallis",
            "Plains of Eidolon",
        ]

    @staticmethod
    def mission_types() -> List[str]:
        return [
            "(Elite) Sanctuary Onslaught",
            "(Mirror) Defense",
            "Alchemy",
            "Ascension",
            "Assassination",
            "Assault",
            "Capture",
            "Disruption",
            "Excavation",
            "Exterminate",
            "Faceoff",
            "Hijack",
            "Infested Salvage",
            "Interception",
            "Mobile Defense",
            "Nightmare",
            "Rescue",
            "Sabotage (Any Variant)",
            "Shrine Defense",
            "Skirmish",
            "Spy",
            "Survival (Any Variant)",
            "Void Armageddon",
            "Void Cascade",
            "Void Flood",
            "Volatile",
        ]


# Archipelago Options
class WarframeWarframesOwned(OptionSet):
    """
    Indicates which Warframe warframes the player owns and wants to possibly play as.
    """

    display_name = "Warframe Warframes Owned"
    valid_keys = WarframeGame().warframes_all

    default = valid_keys


class WarframeWeaponTypesOwned(OptionSet):
    """
    Indicates which Warframe weapon types the player owns and wants to possibly use.
    """

    display_name = "Warframe Weapon Types Owned"
    valid_keys = WarframeGame().weapon_types_all

    default = valid_keys
