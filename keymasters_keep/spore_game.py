from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import OptionSet, Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class SporeArchipelagoOptions:
    spore_include_galactic_adventures: SporeIncludeGalacticAdventures
    spore_stages: SporeStages
    spore_space_exclusive_missions: SporeSpaceExclusiveMissions
    spore_sporecast_exclusive_missions: SporeSporecastExclusiveMissions
    spore_custom_galactic_adventures: SporeCustomGalacticAdventures


class SporeGame(Game):
    name = "Spore"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = SporeArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play on DIFFICULTY difficulty",
                data={
                    "DIFFICULTY": (self.difficulties, 1),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = list()

        if "Cell" in self.stages:
            templates.append(
                GameObjectiveTemplate(
                    label="Complete the Cell stage as a DIET creature's path to BEHAVIOR",
                    data={
                        "DIET": (self.diets_cell, 1),
                        "BEHAVIOR": (self.behaviors_cell, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
            )

        if "Creature" in self.stages:
            templates.append(
                GameObjectiveTemplate(
                    label="Complete the Creature stage as a DIET creature's path to BEHAVIOR",
                    data={
                        "DIET": (self.diets, 1),
                        "BEHAVIOR": (self.behaviors_creature, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
            )

        if "Tribal" in self.stages:
            templates.append(
                GameObjectiveTemplate(
                    label="Complete the Tribal stage as a DIET creature's path to BEHAVIOR",
                    data={
                        "DIET": (self.diets, 1),
                        "BEHAVIOR": (self.behaviors_tribal, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
            )

        if "Civilization" in self.stages:
            templates.append(
                GameObjectiveTemplate(
                    label="Complete the Civilization stage as the EMPIRE empire's path to BEHAVIOR",
                    data={
                        "EMPIRE": (self.empires, 1),
                        "BEHAVIOR": (self.behaviors_civilization, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
            )

        if "Space" in self.stages:
            templates.extend([
                GameObjectiveTemplate(
                    label="Complete the Space stage",
                    data=dict(),
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="In the Space stage, get the BADGE badge",
                    data={
                        "BADGE": (self.badges, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="In the Space stage, get the Level LEVEL BADGE badge",
                    data={
                        "LEVEL": (self.badge_level_range, 1),
                        "BADGE": (self.badges_multiple, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        if self.include_galactic_adventures:
            templates.append(
                GameObjectiveTemplate(
                    label="Complete the 'ADVENTURE' adventure",
                    data={
                        "ADVENTURE": (self.adventures, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=4,
                ),
            )

        return templates

    @property
    def include_galactic_adventures(self) -> bool:
        return bool(self.archipelago_options.spore_include_galactic_adventures.value)

    @property
    def stages(self) -> List[str]:
        return sorted(self.archipelago_options.spore_stages.value)

    @property
    def space_exclusive_missions(self) -> List[str]:
        return sorted(self.archipelago_options.spore_space_exclusive_missions.value)

    @property
    def sporecast_exclusive_missions(self) -> List[str]:
        return sorted(self.archipelago_options.spore_sporecast_exclusive_missions.value)

    @property
    def custom_galactic_adventures(self) -> List[str]:
        return sorted(self.archipelago_options.spore_custom_galactic_adventures.value)

    @staticmethod
    def difficulties() -> List[str]:
        return [
            "Easy",
            "Normal",
            "Hard",
        ]

    @staticmethod
    def diets() -> List[str]:
        return [
            "Herbivore",
            "Carnivore",
            "Omnivore",
        ]

    @staticmethod
    def diets_cell() -> List[str]:
        return [
            "Herbivore",
            "Carnivore",
        ]

    @staticmethod
    def behaviors_cell() -> List[str]:
        return [
            "Herbivore",
            "Carnivore",
            "Omnivore",
        ]

    @staticmethod
    def behaviors_creature() -> List[str]:
        return [
            "Social",
            "Adaptable",
            "Predator",
        ]

    @staticmethod
    def behaviors_tribal() -> List[str]:
        return [
            "Friendly",
            "Industrious",
            "Aggressive",
        ]

    @staticmethod
    def behaviors_civilization() -> List[str]:
        return [
            "Religious",
            "Economic",
            "Aggressive",
        ]

    @staticmethod
    def empires() -> List[str]:
        return [
            "Military",
            "Economic",
            "Religious",
        ]

    @staticmethod
    def badges() -> List[str]:
        return [
            "Body Guard",
            "Brain Surgeon",
            "Captain's Badge",
            "Cleaner",
            "Collector",
            "Colonist",
            "Conqueror",
            "Diplomat",
            "Eco Hero",
            "Empire",
            "Explorer",
            "Frequent Flyer",
            "Golden Touch",
            "Gopher",
            "Jack Of All Trades",
            "Joker",
            "Merchant",
            "Missionista",
            "Planet Artiste",
            "Sightseer",
            "Split Personality",
            "Terra-Wrangler",
            "Trader",
            "Traveler",
            "Warmonger",
            "Wonderland Wanderer",
            "Zoologist",
            "Badge Outta Heck",
            "Dance With The Devil",
            "Near Encounters",
            "Diety Complex",
        ]

    @staticmethod
    def badges_multiple() -> List[str]:
        return [
            "Body Guard",
            "Brain Surgeon",
            "Cleaner",
            "Collector",
            "Colonist",
            "Conqueror",
            "Diplomat",
            "Eco Hero",
            "Empire",
            "Explorer",
            "Frequent Flyer",
            "Golden Touch",
            "Gopher",
            "Jack Of All Trades",
            "Merchant",
            "Missionista",
            "Planet Artiste",
            "Sightseer",
            "Split Personality",
            "Terra-Wrangler",
            "Trader",
            "Traveler",
            "Warmonger",
            "Wonderland Wanderer",
            "Zoologist",
            "Near Encounters",
            "Diety Complex",
        ]

    @staticmethod
    def badge_level_range() -> range:
        return range(2, 6)

    @functools.cached_property
    def adventures_base(self) -> List[str]:
        return [
            "Adventure Town",
            "Bahaha 500 Time Trials",
            "City Assault",
            "Defend the Crystal Mine",
            "Mothership Down",
            "Mr. Puzzle's Magic Gates",
            "The Arena of Oorama",
        ]

    def adventures(self) -> List[str]:
        adventures: List[str] = self.adventures_base[:]

        if len(self.space_exclusive_missions) and "Space" in self.stages:
            adventures.extend(self.space_exclusive_missions)
        if len(self.sporecast_exclusive_missions):
            adventures.extend(self.sporecast_exclusive_missions)
        if len(self.custom_galactic_adventures):
            adventures.extend(self.custom_galactic_adventures)

        return sorted(adventures)


# Archipelago Options
class SporeIncludeGalacticAdventures(Toggle):
    """
    Indicates whether to include Galactic Adventures content when generating Spore objectives.
    """

    display_name = "Spore Include Galactic Adventures"


class SporeStages(OptionSet):
    """
    Indicates which Spore stages to include when generating objectives.
    """

    display_name = "Spore Stages"
    valid_keys = [
        "Cell",
        "Creature",
        "Tribal",
        "Civilization",
        "Space",
    ]

    default = valid_keys


class SporeSpaceExclusiveMissions(OptionSet):
    """
    Indicates which Spore Space Exclusive Missions to include when generating objectives.
    """

    display_name = "Spore Space Exclusive Missions"
    valid_keys = [
        "Becoming a Space Captain",
        "Concert in the Park",
        "Delicate Negotiations",
        "Infestation",
        "It Came from the Sky",
        "Ruins of Doom",
        "Temple of Spode",
        "The Spirits are Restless",
        "TX-5000 Super Weapon",
    ]

    default = valid_keys


class SporeSporecastExclusiveMissions(OptionSet):
    """
    Indicates which Spore Sporecast Exclusive Missions to include when generating objectives.
    """

    display_name = "Spore Sporecast Exclusive Missions"
    valid_keys = [
        "Clark and Stanley Go Camping",
        "Clark and Stanley Go Stargazing",
        "Clark and Stanley Go Swimming",
        "Ghost Towne",
        "How a Bill Becomes a Law",
        "Illusioneering Industries",
        "Infestation - Dronox Invasion",
        "Monstered Town",
        "Mystery Race",
        "Protein Synthesis",
        "Robots vs Dragons",
        "Spoffit Calculator!",
        "SporeBall",
        "The Meaningless Turtle",
        "The Metamorphosis",
        "The Space Race!",
        "Welcome to Dancetopia",
        "Bloody Sundae",
        "Incontinent Continent",
        "Litterbox Gulch",
        "My Big Fat Pig Wedding",
        "Planet of Needin'",
        "Readerdome",
        "Shake It Up",
        "Shenanigans' Fun-Tasy Theme Park",
        "That's My Lunch!",
        "The Chicken and the Road",
        "Whiney and his Poo",
    ]

    default = valid_keys


class SporeCustomGalacticAdventures(OptionSet):
    """
    Indicates which custom Spore Galactic Adventures to include when generating objectives.
    """

    display_name = "Spore Custom Galactic Adventures"
    default = list()
