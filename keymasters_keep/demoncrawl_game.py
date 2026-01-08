from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class DemoncrawlArchipelagoOptions:
    demoncrawl_masteries_unlocked: DemoncrawlMasteriesUnlocked


class DemoncrawlGame(Game):
    name = "DemonCrawl"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = DemoncrawlArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a DIFFICULTY QUEST quest using the following Mastery: MASTERY",
                data={
                    "DIFFICULTY": (self.difficulties_quest, 1),
                    "QUEST": (self.quests, 1),
                    "MASTERY": (self.masteries, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Win a Hero Trial",
                data=dict(),
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win DIFFICULTY Classic Board",
                data={
                    "DIFFICULTY": (self.difficulties_classic, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win a Beyond quest using the following Mastery: MASTERY",
                data={
                    "MASTERY": (self.masteries, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Enter a Metagate in Endless Multiverse",
                data=dict(),
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Enter COUNT Metagates in Endless Multiverse",
                data={
                    "COUNT": (self.gate_number_range, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Clear a Stage after using a Mystic Statue",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Succeed in an Obelisk's Challenge",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
        ]

    def masteries(self) -> List[str]:
        return sorted(self.archipelago_options.demoncrawl_masteries_unlocked.value)

    @staticmethod
    def quests() -> List[str]:
        return [
            "Glory Days",
            "Respite's End",
            "Another Way",
            "Around the Bend",
            "Shadowman",
        ]

    @staticmethod
    def difficulties_quest() -> List[str]:
        return [
            "Casual",
            "Normal",
            "Hard",
        ]

    @staticmethod
    def difficulties_classic() -> List[str]:
        return [
            "an Easy",
            "a Medium",
            "a Hard",
            "an Insane",
        ]

    @staticmethod
    def masteries_all() -> List[str]:
        return [
            "No Mastery",
            "Novice",
            "Survivor",
            "Guardian",
            "Knight",
            "Hunter",
            "Wizard",
            "Witch",
            "Warlock",
            "Spy",
            "Barbarian",
            "Commander",
            "Firefly",
            "Snowflake",
            "Spark",
            "Scholar",
            "Bubbler",
            "Mutant",
            "Detective",
            "Scout",
            "Banker",
            "Marksman",
            "Lumberjack",
            "Exorcist",
            "Undertaker",
            "Demolitionist",
            "Protagonist",
            "Human",
            "Hypnotist",
            "Ninja",
            "Bookworm",
            "Auramancer",
            "Immortal",
            "Poisoner",
            "Ghost",
            "Prophet",
        ]

    @staticmethod
    def gate_number_range() -> range:
        return range(2, 5)


# Archipelago Options
class DemoncrawlMasteriesUnlocked(OptionSet):
    """
    Indicates which masteries the player has unlocked in DemonCrawl.
    """

    display_name = "DemonCrawl Masteries Unlocked"
    valid_keys = DemoncrawlGame().masteries_all()

    default = valid_keys
