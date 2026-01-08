from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class MarioParty3ArchipelagoOptions:
    pass


class MarioParty3Game(Game):
    name = "Mario Party 3"
    platform = KeymastersKeepGamePlatforms.N64

    platforms_other = [
        KeymastersKeepGamePlatforms.SW,
    ]

    is_adult_only_or_unrated = False

    options_cls = MarioParty3ArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Never use a ITEM",
                data={
                    "ITEM": (self.items_regular, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Never use a ITEM",
                data={
                    "ITEM": (self.items_rare, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Set the Computer Character skill levels individually in the following order: SKILL_LEVELS",
                data={
                    "SKILL_LEVELS": (self.skill_levels_duplicated, 3),
                },
            ),
            GameObjectiveTemplate(
                label="Set the Computer Character skill levels all the same to SKILL_LEVELS",
                data={
                    "SKILL_LEVELS": (self.skill_levels, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Do not use any items",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Say no the first time you are offered a Star in a board",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="For all Mini-Game objectives, include at least one Computer Player not on your team set"
                      " to Super Hard",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a COUNT turn game on BOARD with Bonus Stars TOGGLE",
                data={
                    "COUNT": (self.turn_counts_battle_royale, 1),
                    "BOARD": (self.boards_battle_royale, 1),
                    "TOGGLE": (self.off_on, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=15,
            ),
            GameObjectiveTemplate(
                label="Win COUNT turn game on BOARD",
                data={
                    "COUNT": (self.turn_counts_duel, 1),
                    "BOARD": (self.boards_duel, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=15,
            ),
            GameObjectiveTemplate(
                label="Win a COUNT-Win CATEGORIES Battle in Mini-Game Battle Room",
                data={
                    "COUNT": (self.minigame_battle_counts, 1),
                    "CATEGORIES": (self.base_minigame_categories, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=8,
            ),
            GameObjectiveTemplate(
                label="Win Mini-Game Game Guy's Room by reaching 1,000 coins",
                data=dict(),
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
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
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Win a ITEM in an Item Mini-Game",
                data={
                    "ITEM": (self.items_regular, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Obtain a ITEM from an Item Bag, Item Space Question, or Hidden Block",
                data={
                    "ITEM": (self.items_rare, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Have at least COUNT coins at once on BOARD",
                data={
                    "COUNT": (self.board_coin_counts, 1),
                    "BOARD": (self.boards_battle_royale, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win a BONUS on BOARD",
                data={
                    "BONUS": (self.bonus_star_types, 1),
                    "BOARD": (self.boards_battle_royale, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=5,
            ),
        ]

    @staticmethod
    def off_on() -> List[str]:
        return [
            "Off",
            "On",
        ]

    @staticmethod
    def boards_battle_royale() -> List[str]:
        return [
            "Chilly Waters",
            "Deep Bloober Sea",
            "Spiny Desert",
            "Woody Woods",
            "Creepy Cavern",
            "Waluigi's Island",
        ]

    @staticmethod
    def boards_duel() -> List[str]:
        return [
            "Gate Guy",
            "Arrowhead",
            "Pipesqueak",
            "Blowhard",
            "Mr. Mover",
            "Backtrack",
        ]

    @staticmethod
    def bonus_star_types() -> List[str]:
        return [
            "Coin Star",
            "Happening Star",
            "Minigame Star",
        ]

    @staticmethod
    def items_regular() -> List[str]:
        return [
            "Mushroom",
            "Skeleton Key",
            "Warp Block",
            "Cellular Shopper",
            "Dueling Glove",
            "Golden Mushroom",
            "Boo Repellent",
            "Magic Lamp",
            "Reverse Mushroom",
            "Poison Mushroom",
            "Bowser Phone",
            "Bowser Suit",
            "Lucky Lamp",
            "Plunder Chest",
            "Boo Bell",
        ]

    @staticmethod
    def items_rare() -> List[str]:
        return [
            "Wacky Watch",
            "Barter Box",
            "Koopa Kard",
            "Lucky Charm",
        ]

    @staticmethod
    def turn_counts_battle_royale() -> range:
        return range(10, 51, 5)

    @staticmethod
    def turn_counts_duel() -> List[str]:
        return [
            "a 20",
            "an Infinite",
        ]

    @staticmethod
    def skill_levels() -> List[str]:
        return [
            "Easy",
            "Normal",
            "Hard",
            "Super Hard",
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
            "Super Hard",
            "Super Hard",
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
            "Battle Game",
            "Battle Game",
            "Duel Game",
            "Duel Game",
        ]

    @staticmethod
    def minigame_battle_counts() -> range:
        return range(3, 8, 2)

    @staticmethod
    def minigames_4_players() -> List[str]:
        return [
            "Treadmill Grill",
            "Ice Rink Risk",
            "Messy Memory",
            "Picture Imperfect",
            "M.P.I.Q.",
            "Curtain Call",
            "Cheep Cheep Chase",
            "Snowball Summit",
            "Toadstool Titan",
            "Aces High",
            "Bounce 'n' Trounce",
            "Chip Shot Challenge",
            "Mario's Puzzle Party",
            "The Beat Goes On",
            "Water Whirled",
            "Frigid Bridges",
            "Awful Tower",
            "Pipe Cleaners",
            "Rockin' Raceway",
        ]

    @staticmethod
    def minigames_1_vs_3_as_1() -> List[str]:
        return [
            "Coconut Conk (as the 1)",
            "Spotlight Swim (as the 1)",
            "Boulder Ball (as the 1)",
            "Crazy Cogs (as the 1)",
            "Hide and Sneak (as the 1)",
            "Tidal Toss (as the 1)",
            "Hand, Line and Sinker (as the 1)",
            "Ridiculous Relay (as the 1)",
            "Thwomp Pull (as the 1)",
        ]

    @staticmethod
    def minigames_1_vs_3_as_3() -> List[str]:
        return [
            "Coconut Conk (as the 3)",
            "Spotlight Swim (as the 3)",
            "Boulder Ball (as the 3)",
            "Crazy Cogs (as the 3)",
            "Hide and Sneak (as the 3)",
            "Tidal Toss (as the 3)",
            "Hand, Line and Sinker (as the 3)",
            "Ridiculous Relay (as the 3)",
            "Thwomp Pull (as the 3)",
        ]

    @staticmethod
    def minigames_2_vs_2() -> List[str]:
        return [
            "Eatsa Pizza",
            "Baby Bowser Broadside",
            "Cosmic Coaster",
            "Log Jam",
            "Pump, Pump and Away",
            "Hyper Hydrants",
            "Picking Panic",
            "Etch 'n' Catch",
            "Slot Synch",
        ]

    @staticmethod
    def minigames_battle() -> List[str]:
        return [
            "Stacked Deck",
            "Three Door Monty",
            "Merry-Go-Chomp",
            "Slap Down",
            "Locked Out",
            "All Fired Up",
            "Storm Chasers",
            "Eye Sore",
        ]

    @staticmethod
    def minigames_duel() -> List[str]:
        return [
            "Vine With Me",
            "Popgun Pick-Off",
            "End of the Line",
            "Baby Bowser Bonkers",
            "Silly Screws",
            "Crowd Cover",
            "Tick Tock Hop",
            "Bowser Toss",
            "Motor Rooter",
            "Fowl Play",
        ]

    @staticmethod
    def minigames_item() -> List[str]:
        # Not in use. Keeping in case it's needed in the future.
        return [
            "Winner's Wheel",
            "Hey, Batter, Batter!",
            "Bobbing Bow-loons",
            "Dorrie Dip",
            "Swinging with Sharks",
            "Swing 'n' Swipe",
        ]

    @staticmethod
    def minigames_game_guy() -> List[str]:
        return [
            "Game Guy's Magic Boxes",
            "Game Guy's Sweet Surprise",
            "Game Guy's Roulette",
            "Game Guy's Lucky 7",
        ]

    @staticmethod
    def minigames_coin() -> List[str]:
        return [
            "Parasol Plummet",
            "River Raiders (as the 1)",
            "River Raiders (as the 3)",
            "Puddle Paddle",
        ]

    def minigame_list_winnable(self) -> List[str]:
        # Add all Mini-Games twice as weight against the different 1v3 variants
        minigames: List[str] = self.minigames_4_players()[:]

        minigames.extend(self.minigames_4_players()[:])
        minigames.extend(self.minigames_1_vs_3_as_1()[:])
        minigames.extend(self.minigames_1_vs_3_as_3()[:])
        minigames.extend(self.minigames_2_vs_2()[:])
        minigames.extend(self.minigames_2_vs_2()[:])
        minigames.extend(self.minigames_battle()[:])
        minigames.extend(self.minigames_battle()[:])
        minigames.extend(self.minigames_duel()[:])
        minigames.extend(self.minigames_duel()[:])
        minigames.extend(self.minigames_game_guy()[:])
        minigames.extend(self.minigames_game_guy()[:])

        return minigames

    @staticmethod
    def board_coin_counts() -> List[str]:
        return [
            "50",
            "100",
        ]


# Archipelago Options
# ...
