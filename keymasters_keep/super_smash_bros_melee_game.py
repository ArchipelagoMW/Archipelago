from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class SuperSmashBrosMeleeArchipelagoOptions:
    super_smash_bros_melee_include_multi_man_melee: SuperSmashBrosMeleeIncludeMultiManMelee
    super_smash_bros_melee_include_playable_master_hand: SuperSmashBrosMeleeIncludePlayableMasterHand


class SuperSmashBrosMeleeGame(Game):
    name = "Super Smash Bros. Melee"
    platform = KeymastersKeepGamePlatforms.GC

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = SuperSmashBrosMeleeArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Pick CHARACTER for events (when applicable)",
                data={
                    "CHARACTER": (self.characters, 1)
                },
            ),
            GameObjectiveTemplate(
                label="Set all CPU Levels to LEVEL (when applicable)",
                data={
                    "LEVEL": (self.cpu_levels, 1)
                },
            ),
            GameObjectiveTemplate(
                label="Set the CPU Levels to LEVELS (when applicable)",
                data={
                    "LEVELS": (self.cpu_levels, 3)
                },
            ),
            GameObjectiveTemplate(
                label="Hit an opponent over 400 meters in Home-Run Contest (when applicable)",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Finish Break the Targets in under 1 minute (when applicable)",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Play with competitive rules: 4 Stocks, No Items (when applicable)",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Play with all items active (when applicable)",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Play with only Pokeball items set to High (when applicable)",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Play with only 3 Stocks in Singleplayer Mode (when applicable)",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Don't Continue (when applicable)",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Win a Vs. Melee TYPE with CHARACTER against OPPONENT CPU Level LEVEL in STAGE",
                data={
                    "TYPE": (self.match_types, 1),
                    "CHARACTER": (self.characters, 1),
                    "OPPONENT": (self.characters_no_glitched, 1),
                    "LEVEL": (self.cpu_levels, 1),
                    "STAGE": (self.stages, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Win a Vs. Special Melee MODE TYPE with CHARACTER against OPPONENT in STAGE",
                data={
                    "MODE": (self.special_modes, 1),
                    "TYPE": (self.match_types, 1),
                    "CHARACTER": (self.characters, 1),
                    "OPPONENT": (self.characters_no_glitched, 1),
                    "STAGE": (self.stages, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win a Vs. Melee Free For All TYPE with CHARACTER against OPPONENTS in STAGE",
                data={
                    "TYPE": (self.match_types, 1),
                    "CHARACTER": (self.characters, 1),
                    "OPPONENTS": (self.characters_no_glitched, 3),
                    "STAGE": (self.stages, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Win a Vs. Melee Team Battle TYPE with a team of CHARACTERS against OPPONENTS in STAGE",
                data={
                    "TYPE": (self.match_types, 1),
                    "CHARACTERS": (self.characters, 2),
                    "OPPONENTS": (self.characters_no_glitched, 2),
                    "STAGE": (self.stages, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win a Vs. Melee Team Battle TYPE with CHARACTER against OPPONENTS in STAGE",
                data={
                    "TYPE": (self.match_types, 1),
                    "CHARACTER": (self.characters, 1),
                    "OPPONENTS": (self.characters_no_glitched, 3),
                    "STAGE": (self.stages, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete MODE with CHARACTER in DIFFICULTY difficulty",
                data={
                    "MODE": (self.single_player_modes, 1),
                    "CHARACTER": (self.characters_no_glitched, 1),
                    "DIFFICULTY": (self.difficulties, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete STADIUM with CHARACTER",
                data={
                    "STADIUM": (self.stadiums, 1),
                    "CHARACTER": (self.characters_no_glitched, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete the following Event: EVENT",
                data={
                    "EVENT": (self.events, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Collect COUNT Trophies",
                data={
                    "COUNT": (self.trophy_count_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Collect COUNT different Trophies",
                data={
                    "COUNT": (self.trophy_different_count_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Collect COUNT different Bonuses",
                data={
                    "COUNT": (self.bonus_count_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
        ]

        if self.include_multi_man_melee:
            templates.append(
                GameObjectiveTemplate(
                    label="Complete MULTIMAN with CHARACTER",
                    data={
                        "MULTIMAN": (self.multi_man_melees, 1),
                        "CHARACTER": (self.characters, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                )
            )

        return templates

    @property
    def include_multi_man_melee(self) -> bool:
        return bool(self.archipelago_options.super_smash_bros_melee_include_multi_man_melee.value)

    @property
    def include_playable_master_hand(self) -> bool:
        return bool(self.archipelago_options.super_smash_bros_melee_include_playable_master_hand.value)

    @functools.cached_property
    def characters_base(self) -> List[str]:
        return [
            "Mario",
            "Donkey Kong",
            "Link",
            "Samus",
            "Yoshi",
            "Kirby",
            "Fox",
            "Pikachu",
            "Ness",
            "Captain Falcon",
            "Bowser",
            "Peach",
            "Ice Climbers",
            "Zelda/Sheik",
            "Luigi",
            "Jigglypuff",
            "Mewtwo",
            "Marth",
            "Mr. Game & Watch",
            "Dr. Mario",
            "Ganondorf",
            "Falco Lombardi",
            "Young Link",
            "Pichu",
            "Roy",
        ]

    @functools.cached_property
    def characters_glitched(self) -> List[str]:
        return [
            "Master Hand",
        ]

    def characters(self) -> List[str]:
        characters: List[str] = self.characters_base[:]

        if self.include_playable_master_hand:
            characters.extend(self.characters_glitched)

        return sorted(characters)

    def characters_no_glitched(self) -> List[str]:
        characters: List[str] = self.characters_base[:]

        return sorted(characters)

    @functools.cached_property
    def stages_base(self) -> List[str]:
        return [
            "Brinstar",
            "Corneria",
            "Venom",
            "Fountain of Dreams",
            "Great Bay",
            "Green Greens",
            "Temple",
            "Icicle Mountain",
            "Jungle Japes",
            "Kongo Jungle",
            "Mushroom Kingdom",
            "Mute City",
            "Onett",
            "Pokémon Stadium",
            "Princess Peach's Castle",
            "Rainbow Cruise",
            "Yoshi's Island",
            "Yoshi's Story",
            "Brinstar Depths",
            "Fourside",
            "Big Blue",
            "Poké Floats",
            "Mushroom Kingdom 2",
            "Flat Zone",
            "Battlefield",
            "Final Destination",
            "Dream Land 64",
            "Kongo Jungle 64",
            "Yoshi's Story 64",
        ]

    def stages(self) -> List[str]:
        stages: List[str] = self.stages_base[:]

        return sorted(stages)

    @staticmethod
    def cpu_levels() -> List[int]:
        return sorted(
            list(range(1, 10))
            + list(range(1, 10))
            + list(range(1, 10))
        )

    @staticmethod
    def match_types() -> List[str]:
        return [
            "Time Match",
            "Stock Match",
            "Coin Match",
        ]

    @staticmethod
    def special_modes() -> List[str]:
        return [
            "Stamina Mode",
            "Super Sudden Death",
            "Giant Melee",
            "Tiny Melee",
            "Invisible Melee",
            "Fixed Camera",
            "Single Button Mode",
            "Lightning Melee",
            "Slo-Mo Melee",
        ]

    @staticmethod
    def events_character_select() -> List[str]:
        return [
            "Bomb-Fest",
            "Dino-Wrangling",
            "Kirbys on Parade",
            "Pokémon Battle",
            "Hot Date on Brinstar",
            "Hide 'n' Sheik",
            "All-Star Match 1",
            "King of the Mountain",
            "Seconds, Anyone?",
            "Trophy Tussle 1",
            "Girl Power",
            "All-Star Match 2",
            "Ice Breaker",
            "Super Mario 128",
            "Slippy's Invention",
            "The Yoshi Herd",
            "Trophy Tussle 2",
            "Puffballs Unite!",
            "All-Star Match 3",
            "Mario Bros. Madness",
            "Legendary Pokémon",
            "Super Mario Bros. 2",
            "All-Star Match 4",
            "Mewtwo Strikes!",
            "Fire Emblem Pride",
            "Trophy Tussle 3",
            "Pikachu and Pichu",
            "All-Star Match Deluxe",
            "Final Destination Match",
            "The Showdown",
        ]

    @staticmethod
    def events_forced_character() -> List[str]:
        return [
            "Trouble King",
            "Lord of the Jungle",
            "Spare Change",
            "Yoshi's Egg",
            "Kirby's Air-raid",
            "Bounty Hunters",
            "Link's Adventure",
            "Peach's Peril",
            "Gargantuans",
            "Triforce Gathering",
            "Target Acquired",
            "Lethal Marathon",
            "Seven Years",
            "Time for a Checkup",
            "Space Travelers",
            "Jigglypuff Live!",
            "En Garde!",
            "Trouble King 2",
            "Birds of Prey",
            "Game & Watch Forever!",
        ]

    def events(self) -> List[str]:
        return sorted(self.events_character_select() + self.events_forced_character())

    @staticmethod
    def single_player_modes() -> List[str]:
        return [
            "Classic",
            "Adventure",
            "All-Stars",
        ]

    @staticmethod
    def stadiums() -> List[str]:
        return [
            "Break the Targets",
            "Home-Run Contest",
        ]

    @staticmethod
    def multi_man_melees() -> List[str]:
        return [
            "10-Man",
            "100-Man",
            "3-Minute",
            "15-Minute",
        ]

    @staticmethod
    def difficulties() -> List[str]:
        return [
            "Very Easy",
            "Easy",
            "Normal",
            "Hard",
            "Very Hard",
        ]

    @staticmethod
    def trophy_count_range() -> range:
        return range(10, 31)

    @staticmethod
    def trophy_different_count_range() -> range:
        return range(5, 11)

    @staticmethod
    def bonus_count_range() -> range:
        return range(5, 11)


# Archipelago Options
class SuperSmashBrosMeleeIncludeMultiManMelee(Toggle):
    """
    Indicates whether to include Multi-Man Melee Super Smash Bros. Melee objectives.
    """

    display_name = "Super Smash Bros. Melee Include Multi-Man Melee"


class SuperSmashBrosMeleeIncludePlayableMasterHand(Toggle):
    """
    Indicates whether to include Playable Master Hand when generating Super Smash Bros. Melee objectives.
    """

    display_name = "Super Smash Bros. Melee Include Playable Master Hand"
