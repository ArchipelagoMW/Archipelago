from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class OctodadDadliestCatchArchipelagoOptions:
    pass


class OcotodadDadliestCatchGame(Game):
    name = "Octodad: Dadliest Catch"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.WIIU,
        KeymastersKeepGamePlatforms.XONE,
    ]

    is_adult_only_or_unrated = False

    options_cls = OctodadDadliestCatchArchipelagoOptions

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
        return [
            GameObjectiveTemplate(
                label="Complete the 'CHAPTER' Chapter",
                data={
                    "CHAPTER": (self.chapters, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Collect the following Ties: TIES",
                data={
                    "TIES": (self.ties, 3)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Complete the 'SHORT' Short",
                data={
                    "SHORT": (self.shorts, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete 'LEVEL' without being caught",
                data={
                    "LEVEL": (self.levels, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete the 'ACHIEVEMENT' Achivement",
                data={
                    "ACHIEVEMENT": (self.achievements, 1)
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
        ]

    @staticmethod
    def chapters() -> List[str]:
        return [
            "Wedding Bells",
            "Home, Sweet Home",
            "Gervason's Grocery",
            "Aquatic Fun Center",
            "World of Kelp",
            "The Deep Sea",
            "Amazon Arcade",
            "Sea Legs",
            "Toilet and Trouble",
            "Shark Naked",
            "Silent but Dadly",
            "Hot Concessions",
        ]

    @staticmethod
    def shorts() -> List[str]:
        return [
            "Dad Romance",
            "Medical Mess",
        ]

    def levels(self) -> List[str]:
        return sorted(self.chapters() + self.shorts())

    @staticmethod
    def ties_main_game() -> List[str]:
        return [
            "Classic Red (Wedding Bells)",
            "Wedding Cake (Wedding Bells)",
            "Piano Keys (Wedding Bells)",
            "Number One Dad (Home, Sweet Home)",
            "Flower Print (Home, Sweet Home)",
            "Sports Print (Home, Sweet Home)",
            "Banana (Gervason's Grocery)",
            "Hen Tie (Gervason's Grocery)",
            "Tasty Meat (Gervason's Grocery)",
            "Rainbow Dream (Aquatic Fun Center)",
            "Shark Attack (Aquatic Fun Center)",
            "Coral (Aquatic Fun Center)",
            "Green Paisley (World of Kelp)",
            "Sunrise (World of Kelp)",
            "Octopus Pattern (World of Kelp)",
            "The Question (The Deep Sea)",
            "Disco Floor (The Deep Sea)",
            "Pink Plaid (The Deep Sea)",
            "Fish Pattern (Amazon Arcade)",
            "Green Stripey (Amazon Arcade)",
            "Heart Pattern (Amazon Arcade)",
            "Tentacle (Sea Legs)",
            "Anchors Away (Sea Legs)",
            "Rising Tide (Sea Legs)",
            "Pi Tie (Silent but Dadly)",
            "Winter Season (Silent but Dadly)",
            "Tropical Night (Silent but Dadly)",
            "Sky High (Hot Concessions)",
            "Inferno (Hot Concessions)",
            "Zen Tie (Hot Concessions)",
        ]

    @staticmethod
    def ties_shorts() -> List[str]:
        return [
            "Brick House (Dad Romance)",
            "Cheesey Checker (Dad Romance)",
            "Pizza Pie (Dad Romance)",
            "Lime Time (Medical Mess)",
            "Bones (Medical Mess)",
            "Boo Boo (Medical Mess)",
        ]

    def ties(self) -> List[str]:
        return sorted(self.ties_main_game() + self.ties_shorts())

    @staticmethod
    def achievements() -> List[str]:
        return [
            "Be the Controller",
            "Trickshot-gun Wedding",
            "Domino Dynamo",
            "The Best Man",
            "Trim Your Moustache",
            "The Secret Gardener",
            "Smokey the Dad",
            "Secret Shopper",
            "Unacceptable Purchase!",
            "Person-al Shopper",
            "Oh Captain, My Captain",
            "Band of Blubbers",
            "Cod of Duty",
            "Around the World in Several Seconds",
            "Head Otter",
            "The Hero they Deserve",
            "Amazonian Antagonist",
            "Dunk Tank",
            "Stay True to Yourself",
            "Poor Workplace Etiquette",
            "Everybody Loves Joe",
            "Silent But Dadly",
            "Dancing in the Dark",
            "Secrets of the Deep",
            "Stairs with Attitude",
            "No Cutsies",
            "Independent Woman",
            "Au Naturel",
            "World's Best Dad",
            "Number 1 Dad",
            "Number 100 Dad",
            "Dadliest Wardrobe",
        ]

    @staticmethod
    def difficulties() -> List[str]:
        return [
            "Easy",
            "Medium",
            "Hard",
        ]


# Archipelago Options
# ...
