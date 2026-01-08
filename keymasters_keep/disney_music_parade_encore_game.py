from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class DisneyMusicParadeEncoreArchipelagoOptions:
    pass


class DisneyMusicParadeEncoreGame(Game):
    name = "Disney Music Parade Encore"
    platform = KeymastersKeepGamePlatforms.SW

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = DisneyMusicParadeEncoreArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play SONG on DIFFICULTY difficulty",
                data={
                    "SONG": (self.songs, 1),
                    "DIFFICULTY": (self.difficulties, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Play SONGS on DIFFICULTY difficulty",
                data={
                    "SONGS": (self.songs, 2),
                    "DIFFICULTY": (self.difficulties, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Play all songs from 'CATEGORY' category on DIFFICULTY difficulty",
                data={
                    "CATEGORY": (self.categories, 1),
                    "DIFFICULTY": (self.difficulties, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
        ]

    @staticmethod
    def songs() -> List[str]:
        return [
            "Mickey Mouse Club March",
            "Disney Music Parade Encore Themesong",
            "Steamboat Bill (Disney Music Parade Version)",
            "The Sorcerer's Apprentice",
            "Someday My Prince Will Come",
            "Heigh Ho",
            "When You Wish Upon a Star",
            "Hi Diddle Dee Dee",
            "A Dream is a Wish Your Heart Makes",
            "Bibbidi-Bobbidi-Boo",
            "Alice in Wonderland",
            "The Unbirthday Song",
            "I'm Late",
            "You Can Fly! You Can Fly! You Can Fly!",
            "The Second Star to the Right",
            "Once Upon a Dream",
            "I Wonder",
            "Winnie the Pooh",
            "The Wonderful Thing about Tiggers",
            "Under the Sea",
            "Part of Your World",
            "Beauty and the Beast",
            "Be Our Guest",
            "Something There",
            "A Whole New World",
            "Friend like Me",
            "Prince Ali",
            "This is Halloween (Original Movie Version)",
            "Circle of Life",
            "Hakuna Matata",
            "You've Got a Friend in Me (Original Movie Version)",
            "Woody's Roundup",
            "Go the Distance",
            "Zero to Hero",
            "Reflection",
            "I'll Make a Man Out of You",
            "If I Didn't Have You",
            "The Scare Floor",
            "Monsters, Inc.",
            "Hawaiian Roller Coaster Ride",
            "Aloha, E Komo Mai",
            "I See the Light",
            "When Will My Life Begin",
            "Let it Go",
            "Do You Want to Build a Snowman",
            "Into the Unknown (original Movie Version)",
            "When I am Older (Original Movie Version)",
            "Immortals (Original Movie Version)",
            "First Flight",
            "Try Everything (Original Movie Version)",
            "How Far I'll Go (End Credit Version)",
            "You're Welcome",
            "Remember Me (End Credit Version)",
            "Un Poco Loco (Original Movie Version)",
            "This Wish (Original Movie Version)",
            "This Is The Thanks I Get (Original Movie Version)",
            "Main Theme from Main Street Electrical Parade",
            "Mickey's PhilharMagic",
            "Fantasmic",
            "It's a Small World",
        ]

    @staticmethod
    def difficulties() -> List[str]:
        return [
            "Easy",
            "Normal",
            "Hard",
            "Expert",
        ]

    @staticmethod
    def categories() -> List[str]:
        return [
            "Mickey Mouse and Friends",
            "Snow White and the Seven Dwarfs",
            "Pinocchio",
            "Cinderella",
            "Alice in Wonderland",
            "Peter Pan",
            "Sleeping Beauty",
            "Winnie the Pooh",
            "The Little Mermaid",
            "Beauty and the Beast",
            "Aladdin",
            "Tim Burton's The Nightmare Before Christmas",
            "The Lion King",
            "Toy Story",
            "Hercules",
            "Mulan",
            "Monsters, Inc.",
            "Lilo and Stitch",
            "Tangled",
            "Frozen",
            "Big Hero 6",
            "Zootopia",
            "Moana",
            "Coco",
            "Wish",
            "Parks",
        ]


# Archipelago Options
# ...
