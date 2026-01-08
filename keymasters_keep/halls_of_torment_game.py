from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class HallsOfTormentArchipelagoOptions:
    pass


class HallsOfTormentGame(Game):
    name = "Halls of Torment"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.AND,
        KeymastersKeepGamePlatforms.IOS,
    ]

    is_adult_only_or_unrated = False

    options_cls = HallsOfTormentArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Enable the following artifacts: ARTIFACTS",
                data={"ARTIFACTS": (self.artifacts, 3)},
            ),
            GameObjectiveTemplate(
                label="Refund all BLESSING blessings",
                data={"BLESSING": (self.blessings, 1)},
            ),
            GameObjectiveTemplate(
                label="Keep your SLOT slot(s) empty",
                data={"SLOT": (self.equipment_slots, 1)},
            )
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Survive X minutes in HALL with CHARACTER",
                data={
                    "X": (self.minute_range, 1),
                    "HALL": (self.halls, 1),
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Survive a full HALL run with CHARACTER",
                data={
                    "HALL": (self.halls, 1),
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Survive X minutes in HALL with CHARACTER. Forced Abilities: ABILITIES",
                data={
                    "X": (self.minute_range, 1),
                    "HALL": (self.halls, 1),
                    "CHARACTER": (self.characters, 1),
                    "ABILITIES": (self.abilities, 3),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Survive a full HALL run with CHARACTER. Forced Abilities: ABILITIES",
                data={
                    "HALL": (self.halls, 1),
                    "CHARACTER": (self.characters, 1),
                    "ABILITIES": (self.abilities, 3),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Survive X minutes in HALL with CHARACTER. Banned Abilities: ABILITIES",
                data={
                    "X": (self.minute_range, 1),
                    "HALL": (self.halls, 1),
                    "CHARACTER": (self.characters, 1),
                    "ABILITIES": (self.abilities, 3),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Survive a full HALL run with CHARACTER. Banned Abilities: ABILITIES",
                data={
                    "HALL": (self.halls, 1),
                    "CHARACTER": (self.characters, 1),
                    "ABILITIES": (self.abilities, 3),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Survive X minutes in HALL with CHARACTER. Take every TRAIT trait you are offered",
                data={
                    "X": (self.minute_range, 1),
                    "HALL": (self.halls, 1),
                    "CHARACTER": (self.characters, 1),
                    "TRAIT": (self.traits, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Survive a full HALL run with CHARACTER. Take every TRAIT trait you are offered",
                data={
                    "HALL": (self.halls, 1),
                    "CHARACTER": (self.characters, 1),
                    "TRAIT": (self.traits, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Survive X minutes in HALL with CHARACTER. Start on Agony AGONY",
                data={
                    "X": (self.minute_range, 1),
                    "HALL": (self.halls_no_vault, 1),
                    "CHARACTER": (self.characters, 1),
                    "AGONY": (self.agony_range, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Survive a full HALL run with CHARACTER. Start on Agony AGONY",
                data={
                    "HALL": (self.halls_no_vault, 1),
                    "CHARACTER": (self.characters, 1),
                    "AGONY": (self.agony_range, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Trigger the secret in HALL",
                data={"HALL": (self.halls_no_vault, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Recover an uncommon item in HALL using the well (Requires Archaelogist's Thread)",
                data={"HALL": (self.halls_no_vault, 1)},
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
        ]

    @staticmethod
    def artifacts() -> List[str]:
        return [
            "Apocryphal Curse",
            "Archaeologist's Thread",
            "Burdening Stone",
            "Confusing Lens",
            "Curse of Commitment",
            "Demonic Cube",
            "Face of Regret",
            "Fallen Star",
            "Flagellant's Foot Cuff",
            "Golden Scarab",
            "Hastening Sands",
            "Hiltless Dagger",
            "Idol of Hunger",
            "Ivory Dice",
            "Killing Gaze",
            "Living Darkness",
            "Magma Vessel",
            "Malignant Mirror",
            "Master's Vice",
            "Mind Veil",
            "Mountain Idol",
            "Obsidian Dice",
            "Primordial Edict",
            "Restless Wheel",
            "Scales of Pain",
            "Scorched Hand",
            "Silver Cut",
            "Torment Banner",
            "Trickster's Chime",
            "Urn of the Damned",
        ]

    @staticmethod
    def blessings() -> List[str]:
        return [
            "Ability Drop Chance",
            "Area / Projectile Size",
            "Attack Range",
            "Attack Speed",
            "Base Crit Chance",
            "Block Strength",
            "Burn Damage",
            "Chest Drop Chance",
            "Crit Bonus",
            "Crit Chance",
            "Damage",
            "Defense",
            "Effect on Hit Chance",
            "Force",
            "Frost Damage",
            "Gold Gain",
            "Health Capacity",
            "Health Regeneration",
            "Magic Damage",
            "Movement Speed",
            "Multistrike",
            "Physical Damage",
            "Pickup Range",
            "Revives",
            "Spark Damage",
        ]

    @staticmethod
    def equipment_slots() -> List[str]:
        return [
            "Amulet",
            "Body Armor",
            "Boots",
            "Gloves",
            "Helmet",
            "Helmet",
            "Ring",
        ]

    @staticmethod
    def minute_range() -> range:
        return range(10, 26)

    @staticmethod
    def halls() -> List[str]:
        return [
            "Haunted Caverns",
            "Ember Grounds",
            "Forgotten Viaduct",
            "Frozen Depths",
            "Chambers of Dissonance",
            "The Vault",
        ]

    @staticmethod
    def halls_no_vault() -> List[str]:
        return [
            "Haunted Caverns",
            "Ember Grounds",
            "Forgotten Viaduct",
            "Frozen Depths",
            "Chambers of Dissonance",
        ]

    @staticmethod
    def characters() -> List[str]:
        return [
            "Archer",
            "Beast Huntress",
            "Cleric",
            "Exterminator",
            "Landsknecht",
            "Norseman",
            "Sage",
            "Shield Maiden",
            "Sorceress",
            "Swordsman",
            "Warlock",
        ]

    @staticmethod
    def abilities() -> List[str]:
        return [
            "Arcane Rift",
            "Arcane Splinters",
            "Astronomer's Orbs",
            "Clay Golem",
            "Dragon's Breath",
            "Flame Strike",
            "Frost Avalanche",
            "Hailstorm",
            "Kugelblitz",
            "Lightning Strikes",
            "Meteor Strike",
            "Morning Star",
            "Phantom Needles",
            "Radiant Aura",
            "Ring Blades",
            "Spectral Fists",
            "Spirit Warrior",
            "Transfixion",
        ]

    @staticmethod
    def traits() -> List[str]:
        return [
            "Channeling",
            "Collateral Damage",
            "Cunning Technique",
            "Long Fingers",
            "Metabolism",
            "Parry",
            "Quick Hands",
            "Ruthlessness",
            "Strength",
            "Swift Feet",
            "Thick Hide",
            "Vanguard",
            "Vitality",
        ]

    @staticmethod
    def agony_range() -> range:
        return range(1, 13)


# Archipelago Options
# ...
