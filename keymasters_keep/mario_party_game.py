from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class MarioPartyArchipelagoOptions:
    pass


class MarioPartyGame(Game):
    name = "Mario Party"
    platform = KeymastersKeepGamePlatforms.N64

    platforms_other = [
        KeymastersKeepGamePlatforms.SW,
    ]

    is_adult_only_or_unrated = False

    options_cls = MarioPartyArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Enable BLOCKs before playing a board",
                data={
                    "BLOCK": (self.extra_dice_blocks, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Win a board without using BLOCKs",
                data={
                    "BLOCK": (self.extra_dice_blocks, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Set the Computer Character skill levels individually in the following order: SKILLS",
                data={
                    "SKILLS": (self.skill_levels_duplicated, 3)
                },
            ),
            GameObjectiveTemplate(
                label="Set the Computer Character skill levels all the same to SKILL",
                data={
                    "SKILL": (self.skill_levels, 1)
                },
            ),
            GameObjectiveTemplate(
                label="Say no the first time you are offered a Star in a board",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="For all Mini-Game objectives, include at least one Computer Player not on your team set to Hard",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a TURNS turn game on BOARD",
                data={
                    "TURNS": (self.turn_count_range, 1),
                    "BOARD": (self.boards, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=15,
            ),
            GameObjectiveTemplate(
                label="Win a COUNT-Win CATEGORY Battle in Mini-Game House",
                data={
                    "COUNT": (self.minigame_battle_count_range, 1),
                    "CATEGORY": (self.base_minigame_categories, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=8,
            ),
            GameObjectiveTemplate(
                label="Win a COUNT turn Trial in Mini-Game Stadium",
                data={
                    "COUNT": (self.minigame_trial_turn_count_range, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Win at MINIGAME",
                data={
                    "MINIGAME": (self.minigame_list_winnable, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=30,
            ),
            GameObjectiveTemplate(
                label="Collect the most coins in MINIGAME",
                data={
                    "MINIGAME": (self.minigames_coin, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Complete Mini-Game Island completing COUNT set of Mini-Games",
                data={
                    "COUNT": (self.number_of_minigames, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Have at least COUNT coins at once on BOARD",
                data={
                    "COUNT": (self.board_coin_count_range, 1),
                    "BOARD": (self.boards, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win a STAR on BOARD",
                data={
                    "STAR": (self.bonus_star_types, 1),
                    "BOARD": (self.boards, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=5,
            ),
        ]

    @staticmethod
    def number_of_minigames() -> List[str]:
        return [
            "Any",
            "Every",
        ]

    @staticmethod
    def bonus_star_types() -> List[str]:
        return [
            "Coin Star",
            "Happening Star",
            "Minigame Star",
        ]

    @staticmethod
    def boards() -> List[str]:
        return [
            "DK's Jungle Adventure",
            "Peach's Birthday Cake",
            "Yoshi's Tropical Island",
            "Wario's Battle Canyon",
            "Luigi's Engine Room",
            "Mario's Rainbow Castle",
            "Bowser's Magma Mountain",
            "Eternal Star",
        ]

    @staticmethod
    def extra_dice_blocks() -> List[str]:
        return [
            "a Plus Block",
            "a Minus Block",
            "a Speed Block",
            "a Slow Block",
            "a Warp Block",
            "an Event Block",
        ]

    @staticmethod
    def turn_count_range() -> range:
        return range(20, 51, 15)

    @staticmethod
    def skill_levels() -> List[str]:
        return [
            "Easy",
            "Normal",
            "Hard",
        ]

    @staticmethod
    def skill_levels_duplicated() -> List[str]:
        return [
            "Easy",
            "Easy",
            "Normal",
            "Normal",
            "Hard",
            "Hard",
        ]

    @staticmethod
    def base_minigame_categories() -> List[str]:
        return [
            "4-Player Game",
            "4-Player Game",
            "1 VS 3 Game (as the 1)",
            "1 VS 3 Game (as the 3)",
            "2 VS 2 Game",
            "2 VS 2 Game",
            "1 Player Game",
            "1 Player Game",
        ]

    @staticmethod
    def minigame_battle_count_range() -> range:
        return range(1, 8, 2)

    @staticmethod
    def minigame_trial_turn_count_range() -> range:
        return range(10, 31, 10)

    @staticmethod
    def minigames_4_players() -> List[str]:
        return [
            "Buried Treasure",
            "Hot Bob-omb",
            "Musical Mushroom",
            "Crazy Cutter",
            "Face Lift",
            "Balloon Burst",
            "Skateboard Scamper",
            "Platform Peril",
            "Mushroom Mix-Up",
            "Bumper Balls",
            "Tipsy Tourney",
            "Bombs Away",
            "Mario Bandstand",
            "Shy Guy Says",
            "Key-pa-Way",
            "Running of the Bulb",
            "Hot Rope Jump",
            "Slot Car Derby",
        ]

    @staticmethod
    def minigames_1_vs_3_as_1() -> List[str]:
        return [
            "Bowl Over (as the 1)",
            "Tightrope Treachery (as the 1)",
            "Piranha's Pursuit (as the 1)",
            "Tug o' War (as the 1)",
        ]

    @staticmethod
    def minigames_1_vs_3_as_3() -> List[str]:
        return [
            "Bowl Over (as the 3)",
            "Tightrope Treachery (as the 3)",
            "Piranha's Pursuit (as the 3)",
            "Tug o' War (as the 3)",
        ]

    @staticmethod
    def minigames_2_vs_2() -> List[str]:
        return [
            "Bobsled Run",
            "Desert Dash",
            "Bombsketball",
            "Handcar Havoc",
        ]

    @staticmethod
    def minigames_1_player() -> List[str]:
        return [
            "Memory Match",
            "Slot Machine",
            "Shell Game",
            "Ghost Guess",
            "Pedal Power",
            "Ground Pound",
            "Teetering Towers",
            "Knock Block Tower",
            "Limbo Dance",
            "Whack-a-Plant",
        ]

    def minigame_list_winnable(self) -> List[str]:
        # Add all Mini-Games twice as weight against the different 1v3 variants
        minigames: List[str] = self.minigames_4_players()[:]

        minigames.extend(self.minigames_4_players()[:])
        minigames.extend(self.minigames_1_vs_3_as_1()[:])
        minigames.extend(self.minigames_1_vs_3_as_3()[:])
        minigames.extend(self.minigames_2_vs_2()[:])
        minigames.extend(self.minigames_2_vs_2()[:])
        minigames.extend(self.minigames_1_player()[:])
        minigames.extend(self.minigames_1_player()[:])

        return minigames

    @staticmethod
    def minigames_coin() -> List[str]:
        return [
            "Treasure Divers",
            "Coin Block Blitz",
            "Box Mountain Mayhem",
            "Grab Bag",
            "Cast Aways",
            "Hammer Drop",
            "Pipe Maze",
            "Coin Block Bash",
            "Crane Game (as the 1)",
            "Paddle Battle (as the 1)",
            "Coin Shower Flower (as the 1)",
            "Paddle Battle (as the 3)",
            "Coin Shower Flower (as the 3)",
            "Bash 'n' Cash (as the 3)",
            "Deep Sea Divers",
        ]

    @staticmethod
    def board_coin_count_range() -> range:
        return range(50, 101, 50)


# Archipelago Options
# ...
