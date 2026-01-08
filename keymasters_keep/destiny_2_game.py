from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class Destiny2ArchipelagoOptions:
    destiny_2_subclasses: Destiny2Subclasses


class Destiny2Game(Game):
    name = "Destiny 2"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = False

    options_cls = Destiny2ArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Must use only the following Weapon Archetypes: PRIMARY/SPECIAL, HEAVY",
                data={
                    "PRIMARY/SPECIAL": (self.primary_special, 2),
                    "HEAVY": (self.heavy, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Must equip an Exotic Weapon of Type 'TYPE' and an Exotic Armor in one of the following Slots: SLOTS",
                data={
                    "TYPE": (self.energy_type, 1),
                    "SLOTS": (self.armor_slot, 2),
                },
            ),
            GameObjectiveTemplate(
                label="Cannot use TYPE Weapons",
                data={
                    "TYPE": (self.ammo_type, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Cannot use TYPES Weapons",
                data={
                    "TYPES": (self.energy_type, 3),
                },
            ),
            GameObjectiveTemplate(
                label="Cannot use the WORDS Aspects for your Subclass (left to right, top to bottom)",
                data={
                    "WORDS": (self.aspect_number_word, 2),
                },
            ),
            GameObjectiveTemplate(
                label="Cannot use the following Mod Types: TYPES",
                data={
                    "TYPES": (self.mod_type, 3),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win 3 Crucible matches in any mode while playing the following Subclass: SUBCLASS",
                data={
                    "SUBCLASS": (self.subclasses, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete a Pathfinder in the PLAYLIST playlist",
                data={
                    "PLAYLIST": (self.playlists, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete a Nightfall on Expert difficulty while playing the following Subclass: SUBCLASS",
                data={
                    "SUBCLASS": (self.subclasses, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete a solo Legend difficulty Lost Sector while playing the following Subclass: SUBCLASS",
                data={
                    "SUBCLASS": (self.subclasses, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win a match of Gambit while: CHALLENGES",
                data={
                    "CHALLENGES": (self.gambit_challenges, 2),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete the 'MISSION' campaign mission on Legendary difficulty, solo, while CHALLENGE",
                data={
                    "MISSION": (self.campaign_missions, 1),
                    "CHALLENGE": (self.campaign_challenges, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete a Dares of Eternity run with over 100K score while playing the following Subclass: SUBCLASS",
                data={
                    "SUBCLASS": (self.subclasses, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete either of DUNGEONS while CHALLENGE",
                data={
                    "DUNGEONS": (self.dungeons, 2),
                    "CHALLENGE": (self.dungeon_challenges, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win a Crucible match while CHALLENGE",
                data={
                    "CHALLENGE": (self.crucible_challenges, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
        ]

    def subclasses(self) -> List[str]:
        return sorted(self.archipelago_options.destiny_2_subclasses.value)

    @staticmethod
    def primary_special() -> List[str]:
        return [
            "Hand Cannon",
            "Bow",
            "Auto Rifle",
            "Scout Rifle",
            "Pulse Rifle",
            "Bullet Sidearm",
            "SMG",
            "Shotgun",
            "Breach-loaded Grenade Launcher",
            "Sniper Rifle",
            "Fusion Rifle",
            "Trace Rifle",
            "Glaive",
            "Rocket Sidearm",
        ]

    @staticmethod
    def heavy() -> List[str]:
        return [
            "Heavy Grenade Launcher",
            "Linear Fusion Rifle",
            "Machine Gun",
            "Rocket Launcher",
            "Sword",
        ]

    @staticmethod
    def energy_type() -> List[str]:
        return [
            "Kinetic",
            "Arc",
            "Solar",
            "Void",
            "Stasis",
            "Strand",
        ]

    @staticmethod
    def armor_slot() -> List[str]:
        return [
            "Helmet",
            "Chestplate",
            "Legs",
            "Boots",
            "Class Item",
        ]

    @staticmethod
    def ammo_type() -> List[str]:
        return [
            "Primary",
            "Special",
            "Heavy",
        ]
    
    @staticmethod
    def aspect_number_word() -> List[str]:
        return [
            "First",
            "Second",
            "Third",
            "Fourth",
            "Fifth",
        ]

    @staticmethod
    def mod_type() -> List[str]:
        return [
            "Ammo Mods",
            "Melee Mods",
            "Grenade Mods",
            "Green Mods",
            "Yellow Mods",
            "Blue Mods",
            "Elemental Resistance Mods",
            "Non-Elemental Resistance Mods",
            "Orb Generation Mods",
            "Orb Pickup Mods",
        ]
    
    @staticmethod
    def playlists() -> List[str]:
        return [
            "Vanguard",
            "Gambit",
            "Crucible",
        ]
    
    @staticmethod
    def gambit_challenges() -> List[str]:
        return [
            "never dying",
            "invading at every opportunity",
            "banking at least 30 motes",
            "killing 5+ guardians",
            "using your Super twice",
            "avoiding half of the ammo crates",
            "only using Primary weapons on guardians",
            "killing a guardian with a non-Super ability",
            "dealing at least 40 percent of your team's Primeval damage",
            "summoning your Primeval after the enemy team",
            "not using a Primary weapon while you have any other weapons available",
            "not using your class ability",
            "not using Heavy weapons once your Primeval spawns",
            "not using your class jump",
        ]
    
    @staticmethod
    def campaign_challenges() -> List[str]:
        return [
            "never dying",
            "not using Kinetic or Energy slot weapons",
            "using no healing other than natural regeneration",
            "running 50 or less Resilience",
            "using weapons from the corresponding expansion",
            "using world drop weapons (source:legendaryengram)",
            "taking under 20 minutes",
        ]
        
    @staticmethod
    def campaign_missions() -> List[str]:
        return [
            "The Arrival (Witch Queen)",
            "The Investigation (Witch Queen)",
            "The Ghosts (Witch Queen)",
            "The Communion (Witch Queen)",
            "The Mirror (Witch Queen)",
            "The Cunning (Witch Queen)",
            "The Last Chance (Witch Queen)",
            "The Ritual (Witch Queen)",
            "Transmigration (Final Shape)",
            "Temptation (Final Shape)",
            "Exegesis (Final Shape)",
            "Requiem (Final Shape)",
            "Ascent (Final Shape)",
            "Dissent (Final Shape)",
            "Iconoclasm (Final Shape)",
            "First Contact (Lightfall)",
            "Under Siege (Lightfall)",
            "Downfall (Lightfall)",
            "Breakneck (Lightfall)",
            "On The Verge (Lightfall)",
            "No Time Left (Lightfall)",
            "Headlong (Lightfall)",
            "Desperate Measures (Lightfall)",
        ]
            
    @staticmethod
    def dungeon_challenges() -> List[str]:
        return [
            "dying less than 5 times",
            "not using your Super",
            "using no healing other than natural regeneration",
            "running 50 or less Resilience",
            "using weapons from either/both dungeons",
            "using world drop weapons (source:legendaryengram)",
            "taking under 40 minutes",
            "not using your class jump",
        ]
                
    @staticmethod
    def dungeons() -> List[str]:
        return [
           "Shattered Throne",
           "Pit of Heresy",
           "Prophecy",
           "Grasp of Avarice",
           "Duality",
           "Spire of the Watcher",
           "Ghosts of the Deep",
           "Warlord's Ruin",
           "Vesper's Host", 
        ]
                
    @staticmethod
    def crucible_challenges() -> List[str]:
        return [
            "getting a combat efficiency score of 3 or higher",
            "getting 25+ kills",
            "after winning two other Crucible matches in a row",
            "getting at least 5 precision kills with Sniper Rifles or Linear Fusion Rifles",
            "getting at least 5 kills with melee weapons",
            "randomizing your loadout after each match",
            "not using armor mods that modify weapon stats",
            "never landing a precision hit",
            "using no Legendary weapons or armor",
        ]


# Archipelago Options
class Destiny2Subclasses(OptionSet):
    """
    Indicates which Destiny 2 Subclasses can be used when generating objectives.
    """

    display_name = "Available Subclasses"
    valid_keys = [
            "Solar Hunter",
            "Arc Hunter",
            "Void Hunter",
            "Stasis Hunter",
            "Strand Hunter",
            "Prismatic Hunter",
            "Solar Titan",
            "Arc Titan",
            "Void Titan",
            "Stasis Titan",
            "Strand Titan",
            "Prismatic Titan",
            "Solar Warlock",
            "Arc Warlock",
            "Void Warlock",
            "Stasis Warlock",
            "Strand Warlock",
            "Prismatic Warlock",
        ]

    default = valid_keys
