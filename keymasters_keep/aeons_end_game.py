from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class AeonsEndArchipelagoOptions:
    aeons_end_expansions_owned: AeonsEndExpansionsOwned


class AeonsEndGame(Game):
    name = "Aeon's End"
    platform = KeymastersKeepGamePlatforms.CARD

    platforms_other = [
        KeymastersKeepGamePlatforms.IOS,
        KeymastersKeepGamePlatforms.PC,
    ]

    is_adult_only_or_unrated = False

    options_cls = AeonsEndArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Select one or both of RELICS as your Supply Relics",
                data={
                    "RELICS": (self.relics, 2)
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a game with MAGE in your party on DIFFICULTY difficulty or harder",
                data={
                    "MAGE": (self.mages, 1),
                    "DIFFICULTY": (self.difficulties, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Win a game with MAGE in your party on DIFFICULTY difficulty or harder",
                data={
                    "MAGE": (self.mages, 1),
                    "DIFFICULTY": (self.difficulties_hard, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win a game with MAGE and SPELLS in your Supply",
                data={
                    "MAGE": (self.mages, 1),
                    "SPELLS": (self.spells, 2),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Win a game with SPELLS in your Supply on DIFFICULTY difficulty or harder",
                data={
                    "SPELLS": (self.spells, 3),
                    "DIFFICULTY": (self.difficulties, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Defeat NEMESIS with MAGE in your party",
                data={
                    "NEMESIS": (self.nemeses, 1),
                    "MAGE": (self.mages, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Defeat NEMESIS on DIFFICULTY difficulty or harder",
                data={
                    "NEMESIS": (self.nemeses, 1),
                    "DIFFICULTY": (self.difficulties, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Defeat NEMESIS on DIFFICULTY difficulty or harder",
                data={
                    "NEMESIS": (self.nemeses, 1),
                    "DIFFICULTY": (self.difficulties_hard, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Defeat NEMESIS with SPELLS in your Supply",
                data={
                    "NEMESIS": (self.nemeses, 1),
                    "SPELLS": (self.spells, 2),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Over two or more games, defeat NEMESES with the same set of Mages and initial Supply",
                data={
                    "NEMESES": (self.nemeses, 2),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="CHALLENGE",
                data={
                    "CHALLENGE": (self.challenges_midgame, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="CHALLENGE with MAGE in your party",
                data={
                    "CHALLENGE": (self.challenges_midgame, 1),
                    "MAGE": (self.mages, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="CHALLENGE with SPELLS in your initial Supply",
                data={
                    "CHALLENGE": (self.challenges_midgame, 1),
                    "SPELLS": (self.spells, 2),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="CHALLENGE on DIFFICULTY difficulty or harder",
                data={
                    "CHALLENGE": (self.challenges_midgame, 1),
                    "DIFFICULTY": (self.difficulties, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="CHALLENGE on DIFFICULTY difficulty or harder",
                data={
                    "CHALLENGE": (self.challenges_midgame, 1),
                    "DIFFICULTY": (self.difficulties_hard, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win a game CHALLENGE",
                data={
                    "CHALLENGE": (self.challenges_victory, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Win a game CHALLENGE on DIFFICULTY",
                data={
                    "CHALLENGE": (self.challenges_victory, 1),
                    "DIFFICULTY": (self.difficulties, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win a game CHALLENGE on DIFFICULTY",
                data={
                    "CHALLENGE": (self.challenges_victory, 1),
                    "DIFFICULTY": (self.difficulties_hard, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win a game CHALLENGE",
                data={
                    "CHALLENGE": (self.challenges_victory_hard, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
        ]

    @property
    def expansions_owned(self) -> List[str]:
        return sorted(self.archipelago_options.aeons_end_expansions_owned.value)

    @property
    def has_expansion_the_depths(self) -> bool:
        return "The Depths" in self.expansions_owned

    @property
    def has_expansion_the_nameless(self) -> bool:
        return "The Nameless" in self.expansions_owned

    @property
    def has_expansion_the_new_age(self) -> bool:
        return "The New Age" in self.expansions_owned

    @functools.cached_property
    def mages_base(self) -> List[str]:
        return [
            "Adelheim",
            "Brama",
            "Jian",
            "Kadir",
            "Lash",
            "Mist",
            "Phaedraxa",
            "Xaxos",
        ]

    @functools.cached_property
    def mages_the_depths(self) -> List[str]:
        return [
            "Nym",
            "Reeve",
            "Zhana",
        ]

    @functools.cached_property
    def mages_the_nameless(self) -> List[str]:
        return [
            "Malastar",
        ]

    @functools.cached_property
    def mages_the_new_age(self) -> List[str]:
        return [
            "Claudia",
            "Gygar",
            "Lost",
            "Rhia",
            "Sahala",
            "Soskel",
            "Talix",
            "Taqren",
        ]

    def mages(self) -> List[str]:
        mages: List[str] = self.mages_base[:]

        if self.has_expansion_the_depths:
            mages.extend(self.mages_the_depths)
        if self.has_expansion_the_nameless:
            mages.extend(self.mages_the_nameless)
        if self.has_expansion_the_new_age:
            mages.extend(self.mages_the_new_age)

        return sorted(mages)

    @functools.cached_property
    def nemeses_base(self) -> List[str]:
        return [
            "Carapace Queen",
            "Crooked Mask",
            "Prince of Gluttons",
            "Rageborne",
        ]

    @functools.cached_property
    def nemeses_the_depths(self) -> List[str]:
        return [
            "Horde-Crone",
        ]

    @functools.cached_property
    def nemeses_the_nameless(self) -> List[str]:
        return [
            "Blight Lord",
            "Wayward One",
            "Malastar",
        ]

    @functools.cached_property
    def nemeses_the_new_age(self) -> List[str]:
        return [
            "Maggoth",
            "Arachnos",
            "Ageless Walker",
            "Fenrix",
        ]

    def nemeses(self) -> List[str]:
        nemeses: List[str] = self.nemeses_base[:]

        if self.has_expansion_the_depths:
            nemeses.extend(self.nemeses_the_depths)
        if self.has_expansion_the_nameless:
            nemeses.extend(self.nemeses_the_nameless)
        if self.has_expansion_the_new_age:
            nemeses.extend(self.nemeses_the_new_age)

        return sorted(nemeses)

    @functools.cached_property
    def spells_base(self) -> List[str]:
        return [
            "Amplify Vision",
            "Arcane Nexus",
            "Chaos Arc",
            "Consuming Void",
            "Dark Fire",
            "Essence Theft",
            "Feral Lightning",
            "Ignite",
            "Lava Tendril",
            "Oblivion Swell",
            "Planar Insight",
            "Phoenix Flame",
            "Spectral Echo",
            "Wildfire Whip",
        ]

    @functools.cached_property
    def spells_the_depths(self) -> List[str]:
        return [
            "Combustion",
            "Devouring Shadow",
            "Disintegrating Scythe",
            "Monstrous Inferno",
            "Void Bond",
        ]

    @functools.cached_property
    def spells_the_nameless(self) -> List[str]:
        return [
            "Blaze",
            "Sage's Brand",
            "Scrying Bolt",
            "Radiance",
        ]

    @functools.cached_property
    def spells_the_new_age(self) -> List[str]:
        return [
            "Bouncing Boom",
            "Deluge of Power",
            "Fatal Harmony",
            "Force Amplifier",
            "Imbued Smash",
            "Pattern Strike",
            "Reverberating Shock",
            "Spirit Lift",
            "Tethered Dart",
        ]

    def spells(self) -> List[str]:
        spells: List[str] = self.spells_base[:]

        if self.has_expansion_the_depths:
            spells.extend(self.spells_the_depths)
        if self.has_expansion_the_nameless:
            spells.extend(self.spells_the_nameless)
        if self.has_expansion_the_new_age:
            spells.extend(self.spells_the_new_age)

        return sorted(spells)

    @staticmethod
    def difficulties() -> List[str]:
        return [
            "Beginner",
            "Standard",
        ]

    @staticmethod
    def difficulties_hard() -> List[str]:
        return [
            "Expert",
            "Extinction",
        ]

    @staticmethod
    def challenges_midgame() -> List[str]:
        return [
            "Have 8 sparks prepped at once",
            "Gain 15 or more Aether in a single turn",
            "Deal 10 or more damage in a single attack",
            "Have 2 mages cast 4 spells each during back-to-back turns",
        ]

    @staticmethod
    def challenges_victory() -> List[str]:
        return [
            "with a solo breach mage",
            "with a two mage team",
            "with two or less gems in your initial Supply piles",
            "with four or more relics in your initial Supply piles",
            "with three or fewer spells in your initial Supply piles",
        ]

    @staticmethod
    def challenges_victory_hard() -> List[str]:
        return [
            "with Gravehold at 1 life",
            "with Gravehold at full life",
            "with all mages at 1 or 0 life",
            "with all mages at full life",
        ]

    @functools.cached_property
    def relics_base(self) -> List[str]:
        return [
            "Blasting Staff",
            "Bottled Vortex",
            "Flexing Dagger",
            "Focusing Orb",
            "Mages Talisman",
            "Unstable Prism",
        ]

    @functools.cached_property
    def relics_the_depths(self) -> List[str]:
        return [
            "Transmogrifier",
            "Vim Dynamo",
        ]

    @functools.cached_property
    def relics_the_nameless(self) -> List[str]:
        return [
            "Molten Hammer",
            "Temporal Helix",
        ]

    @functools.cached_property
    def relics_the_new_age(self) -> List[str]:
        return [
            "Aether Conduit",
            "Caged Fire",
            "Galvanized Bauble",
            "Link Conduit",
            "Marble Galaxy",
            "Pain Conduit",
            "Well of Energy",
        ]

    def relics(self) -> List[str]:
        relics: List[str] = self.relics_base[:]

        if self.has_expansion_the_depths:
            relics.extend(self.relics_the_depths)
        if self.has_expansion_the_nameless:
            relics.extend(self.relics_the_nameless)
        if self.has_expansion_the_new_age:
            relics.extend(self.relics_the_new_age)

        return sorted(relics)


# Archipelago Options
class AeonsEndExpansionsOwned(OptionSet):
    """
    Indicates which Aeon's End expansions the player owns, if any.
    """

    display_name = "Aeon's End Expansions Owned"
    valid_keys = [
        "The Depths",
        "The Nameless",
        "The New Age",
    ]

    default = valid_keys
