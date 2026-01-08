from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class OneDeckDungeonArchipelagoOptions:
    one_deck_dungeon_expansions_owned: OneDeckDungeonExpansionsOwned


class OneDeckDungeonGame(Game):
    name = "One Deck Dungeon"
    platform = KeymastersKeepGamePlatforms.BOARD

    platforms_other = [
        KeymastersKeepGamePlatforms.AND,
        KeymastersKeepGamePlatforms.IOS,
        KeymastersKeepGamePlatforms.PC,
        KeymastersKeepGamePlatforms.SW,
    ]

    is_adult_only_or_unrated = False

    options_cls = OneDeckDungeonArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Select SKILL as your Basic Skill",
                data={
                    "SKILL": (self.basic_skills, 1)
                },
            ),
        ]

        if self.has_expansion_forest_of_shadows:
            templates.append(
                GameObjectiveTemplate(
                    label="Select POTION as your Basic Potion",
                    data={
                        "POTION": (self.basic_potions, 1)
                    },
                )
            )

        return templates

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a game with CHARACTER in your party on DIFFICULTY Difficulty",
                data={
                    "CHARACTER": (self.characters, 1),
                    "DIFFICULTY": (self.difficulties, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Win a game with CHARACTER in your party on DIFFICULTY Difficulty",
                data={
                    "CHARACTER": (self.characters, 1),
                    "DIFFICULTY": (self.difficulties_hard, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Defeat BOSS with CHARACTER in your party",
                data={
                    "BOSS": (self.bosses, 1),
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Defeat BOSS on DIFFICULTY Difficulty",
                data={
                    "BOSS": (self.bosses, 1),
                    "DIFFICULTY": (self.difficulties, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Defeat BOSS on DIFFICULTY Difficulty",
                data={
                    "BOSS": (self.bosses, 1),
                    "DIFFICULTY": (self.difficulties_hard, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Defeat ELITE on the first floor of a dungeon",
                data={
                    "ELITE": (self.elites, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Defeat ELITE with CHARACTER in your party",
                data={
                    "ELITE": (self.elites, 1),
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Defeat ELITE on DIFFICULTY Difficulty",
                data={
                    "ELITE": (self.elites, 1),
                    "DIFFICULTY": (self.difficulties, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Defeat ELITE on DIFFICULTY Difficulty",
                data={
                    "ELITE": (self.elites, 1),
                    "DIFFICULTY": (self.difficulties_hard, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win a game CHALLENGE",
                data={
                    "CHALLENGE": (self.challenges, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Win a game CHALLENGE on DIFFICULTY Difficulty",
                data={
                    "CHALLENGE": (self.challenges, 1),
                    "DIFFICULTY": (self.difficulties_hard, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win a game CHALLENGE",
                data={
                    "CHALLENGE": (self.challenges_hard, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
        ]

    @property
    def expansions_owned(self) -> List[str]:
        return sorted(self.archipelago_options.one_deck_dungeon_expansions_owned.value)

    @property
    def has_expansion_forest_of_shadows(self) -> bool:
        return "Forest of Shadows" in self.expansions_owned

    @functools.cached_property
    def characters_base(self) -> List[str]:
        return [
            "Paladin",
            "Rogue",
            "Archer",
            "Warrior",
            "Mage",
        ]

    @functools.cached_property
    def characters_forest_of_shadows(self) -> List[str]:
        return [
            "Druid",
            "Warden",
            "Slayer",
            "Hunter",
            "Alchemist",
        ]

    def characters(self) -> List[str]:
        characters: List[str] = self.characters_base[:]

        if self.has_expansion_forest_of_shadows:
            characters.extend(self.characters_forest_of_shadows)

        return sorted(characters)

    @functools.cached_property
    def bosses_base(self) -> List[str]:
        return [
            "Dragon",
            "Yeti",
            "Hydra",
            "Lich",
            "Minotaur",
        ]

    @functools.cached_property
    def bosses_forest_of_shadows(self) -> List[str]:
        return [
            "Mud Golem",
            "Poison Elemental",
            "Phoenix",
            "Corrupted Tree",
            "Indrax",
            "Fire Giant",
        ]

    def bosses(self) -> List[str]:
        bosses: List[str] = self.bosses_base[:]

        if self.has_expansion_forest_of_shadows:
            bosses.extend(self.bosses_forest_of_shadows)

        return sorted(bosses)

    @functools.cached_property
    def elites_base(self) -> List[str]:
        return [
            "Fire Elemental",
            "Ogre",
            "Phantom",
            "Ice Elemental",
        ]

    @functools.cached_property
    def elites_forest_of_shadows(self) -> List[str]:
        return [
            "Moss Golem",
            "Razorbeak",
            "Rock Wyrm",
            "Shadowstalker",
        ]

    def elites(self) -> List[str]:
        elites: List[str] = self.elites_base[:]

        if self.has_expansion_forest_of_shadows:
            elites.extend(self.elites_forest_of_shadows)

        return sorted(elites)

    @staticmethod
    def difficulties() -> List[str]:
        return [
            "Novice",
            "Standard",
        ]

    @staticmethod
    def difficulties_hard() -> List[str]:
        return [
            "Veteran",
            "Fearless",
        ]

    @staticmethod
    def challenges() -> List[str]:
        return [
            "without drinking a potion",
            "at XP level 3 or lower",
            "after reaching XP level 4 and converting XP into a potion",
            "with 5 or more Agility dice for one character",
            "with 5 or more Strength dice for one character",
            "with 5 or more Magic dice for one character",
            "with 5 or more Skills for one character",
            "with 6 or more Health for one character",
        ]

    @staticmethod
    def challenges_hard() -> List[str]:
        return [
            "without claiming an item as loot (skills & XP only)",
            "without claiming a skill as loot (items & XP only)",
            "without facing any encounters that have fewer than 3 XP",
            "only claiming and using free skills",
            "without taking any damage from the boss",
        ]

    @functools.cached_property
    def basic_skills_base(self) -> List[str]:
        return [
            "Force Bolt",
            "Precision",
            "True Strike",
            "Ingenuity",
        ]

    @functools.cached_property
    def basic_skills_forest_of_shadows(self) -> List[str]:
        return [
            "Double Strike",
            "Inventiveness",
            "Piercing Blast",
            "Recovery",
        ]

    def basic_skills(self) -> List[str]:
        basic_skills: List[str] = self.basic_skills_base[:]

        if self.has_expansion_forest_of_shadows:
            basic_skills.extend(self.basic_skills_forest_of_shadows)

        return sorted(basic_skills)

    @functools.cached_property
    def basic_potions_base(self) -> List[str]:
        return list()

    @functools.cached_property
    def basic_potions_forest_of_shadows(self) -> List[str]:
        return [
            "Antidote",
            "Aid",
            "Rewind",
            "Luck",
        ]

    def basic_potions(self) -> List[str]:
        basic_potions: List[str] = self.basic_potions_base[:]

        if self.has_expansion_forest_of_shadows:
            basic_potions.extend(self.basic_potions_forest_of_shadows)

        return sorted(basic_potions)


# Archipelago Options
class OneDeckDungeonExpansionsOwned(OptionSet):
    """
    Indicates which One Deck Dungeon expansions the player owns, if any.
    """

    display_name = "One Deck Dungeon Expansions Owned"
    valid_keys = [
        "Forest of Shadows",
    ]

    default = valid_keys
