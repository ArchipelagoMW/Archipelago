from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class WayfinderArchipelagoOptions:
    pass


class WayfinderGame(Game):
    name = "Wayfinder"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS5,
    ]

    is_adult_only_or_unrated = False

    options_cls = WayfinderArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Build primarily into STATS with echoes, armor, and accessories",
                data={
                    "STATS": (self.stats, 2),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="As WAYFINDER, complete EXPEDITION with WEAPON",
                data={
                    "WAYFINDER": (self.wayfinders, 1),
                    "EXPEDITION": (self.expeditions, 1),
                    "WEAPON": (self.weapons, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="As WAYFINDER, complete EXPEDITION with WEAPON and a IMBUEMENT imbuement",
                data={
                    "WAYFINDER": (self.wayfinders, 1),
                    "EXPEDITION": (self.expeditions, 1),
                    "WEAPON": (self.weapons, 1),
                    "IMBUEMENT": (self.imbuements, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="As WAYFINDER, complete EXPEDITION with WEAPON and IMBUEMENTS imbuements",
                data={
                    "WAYFINDER": (self.wayfinders, 1),
                    "EXPEDITION": (self.expeditions, 1),
                    "WEAPON": (self.weapons, 1),
                    "IMBUEMENTS": (self.imbuements, 2),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="As WAYFINDER, complete EXPEDITION with WEAPON and IMBUEMENTS imbuements",
                data={
                    "WAYFINDER": (self.wayfinders, 1),
                    "EXPEDITION": (self.expeditions, 1),
                    "WEAPON": (self.weapons, 1),
                    "IMBUEMENTS": (self.imbuements, 3),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="As WAYFINDER, complete HUNT with WEAPON",
                data={
                    "WAYFINDER": (self.wayfinders, 1),
                    "HUNT": (self.hunts, 1),
                    "WEAPON": (self.weapons, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="As WAYFINDER, complete HUNT with WEAPON and a IMBUEMENT imbuement",
                data={
                    "WAYFINDER": (self.wayfinders, 1),
                    "HUNT": (self.hunts, 1),
                    "WEAPON": (self.weapons, 1),
                    "IMBUEMENT": (self.imbuements, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="As WAYFINDER, complete HUNT with WEAPON and IMBUEMENTS imbuements",
                data={
                    "WAYFINDER": (self.wayfinders, 1),
                    "HUNT": (self.hunts, 1),
                    "WEAPON": (self.weapons, 1),
                    "IMBUEMENTS": (self.imbuements, 2),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="As WAYFINDER, complete HUNT with WEAPON and IMBUEMENTS imbuements",
                data={
                    "WAYFINDER": (self.wayfinders, 1),
                    "HUNT": (self.hunts, 1),
                    "WEAPON": (self.weapons, 1),
                    "IMBUEMENTS": (self.imbuements, 3),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="As WAYFINDER, complete Mythic Hunt: HUNT with WEAPON",
                data={
                    "WAYFINDER": (self.wayfinders, 1),
                    "HUNT": (self.mythic_hunts, 1),
                    "WEAPON": (self.weapons, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="As WAYFINDER, complete Mythic Hunt: HUNT with WEAPON and a IMBUEMENT imbuement",
                data={
                    "WAYFINDER": (self.wayfinders, 1),
                    "HUNT": (self.mythic_hunts, 1),
                    "WEAPON": (self.weapons, 1),
                    "IMBUEMENT": (self.imbuements, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="As WAYFINDER, complete Mythic Hunt: HUNT with WEAPON and IMBUEMENTS imbuements",
                data={
                    "WAYFINDER": (self.wayfinders, 1),
                    "HUNT": (self.mythic_hunts, 1),
                    "WEAPON": (self.weapons, 1),
                    "IMBUEMENTS": (self.imbuements, 2),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="As WAYFINDER, complete Mythic Hunt: HUNT with WEAPON and IMBUEMENTS imbuements",
                data={
                    "WAYFINDER": (self.wayfinders, 1),
                    "HUNT": (self.mythic_hunts, 1),
                    "WEAPON": (self.weapons, 1),
                    "IMBUEMENTS": (self.imbuements, 3),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="As WAYFINDER, complete all Favors on the job board with WEAPON equipped",
                data={
                    "WAYFINDER": (self.wayfinders, 1),
                    "WEAPON": (self.weapons, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="As WAYFINDER, complete all Labors on the job board with WEAPON equipped",
                data={
                    "WAYFINDER": (self.wayfinders, 1),
                    "WEAPON": (self.weapons, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
        ]

    @staticmethod
    def wayfinders() -> List[str]:
        return [
            "Grendel",
            "Lora",
            "Niss",
            "Kyros",
            "Senja",
            "Silo",
            "Wingrave",
            "Venomess",
        ]

    @staticmethod
    def weapons() -> List[str]:
        return [
            "Vanguard",
            "Radiant Dawn",
            "Tooth and Claw",
            "Warp & Weft",
            "Grim Harvest",
            "Bastion",
            "Legacy",
            "Dryades",
            "Unity",
            "Typhoon",
            "Draken Maw",
            "Eclipse",
            "Juggernaut",
            "Doldrum",
            "Windmother's Fang",
            "Titan's Bane",
            "Colossus",
            "Portent",
            "Bloodthirst",
            "Bloodsong",
            "Epitaph",
            "Queen's Pyre",
            "Blight",
            "Slicer & Dicer",
            "God Bleeder",
            "Harvest Moon",
            "Venom",
            "Night's Edge",
            "Umbros",
            "Rose & Thorn",
            "Maiden's Rime",
            "Hush",
            "Ransom",
            "Longshot",
            "Voidbinder",
            "Nightshade",
            "Last Ditch",
            "Tempest",
            "Hellswarm",
            "Covetous",
            "Arcstorm",
            "Requiem",
            "Vesper-III",
            "Duskbringer",
        ]

    @staticmethod
    def stats() -> List[str]:
        return [
            "Max Health",
            "Resilience",
            "Weapon Power",
            "Ability Power",
            "Crit Rating",
            "Crit Power",
            "Break Power",
            "Phys Defense",
            "Mag Defense",
        ]

    @staticmethod
    def expeditions() -> List[str]:
        return [
            "Codex Halls",
            "Undercroft",
            "Repository of Knowledge",
            "The Pit",
            "The Bloodworks",
            "Bal Duum",
            "The Shrouded Woods",
            "The Bone Orchard",
            "The Hollow Heart",
            "Void Dungeon",
            "Unraveling Aurelian",
            "Shattered Foundry",
            "Aegis Vault",
        ]

    @staticmethod
    def hunts() -> List[str]:
        return [
            "Broodmother S'ilreth",
            "The Trial of the Lingering Light",
            "Archon Commander",
            "The Argent Hand",
            "Ryv'n the Devourer",
            "The First",
            "The Bloodspawn",
            "The Bloodbore",
            "Grand Deceiver",
            "Dread Legion",
            "Storm Twins",
            "Kolaar the Beastmaster",
            "Wormwood",
            "The Reaver King",
            "The Unraveled",
            "Precursor Reborn",
            "Hollowlord Vendraal",
            "The Renegade",
            "AS-713 CONFLUX",
            "Teryssa the Silence",
        ]

    @staticmethod
    def mythic_hunts() -> List[str]:
        return [
            "Broodmother S'ilreth",
            "The Trial of the Lingering Light",
            "Archon Commander",
            "The Argent Hand",
            "Ryv'n the Devourer",
            "The First",
            "The Bloodspawn",
            "The Bloodbore",
            "Grand Deceiver",
            "Dread Legion",
            "Storm Twins",
            "Kolaar the Beastmaster",
            "Wormwood",
            "The Reaver King",
            "The Unraveled",
            "Precursor Reborn",
            "Hollowlord Vendraal",
            "The Renegade",
            "AS-713 CONFLUX",
            "Teryssa the Silence",
            "Dark Arbiter",
            "Bloodrage of Vuul",
            "Malefic Maw",
            "Slyv'r the Deathbringer",
        ]

    @staticmethod
    def imbuements() -> List[str]:
        return [
            "Solar",
            "Greed",
            "Chaos",
            "Flora",
            "Shadow",
        ]

# Archipelago Options
# ...
