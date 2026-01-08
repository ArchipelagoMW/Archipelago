from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class LayersOfFearArchipelagoOptions:
    pass


class LayersOfFearGame(Game):
    name = "Layers of Fear (2023)"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = False

    options_cls = LayersOfFearArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play through The Painter's Story and get the following Ending: ENDING",
                data={
                    "ENDING": (self.endings_painter, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Play through The Daughter's Story and get the following Ending: ENDING",
                data={
                    "ENDING": (self.endings_daughter, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Play through The Musician's Story and get the following Ending: ENDING",
                data={
                    "ENDING": (self.endings_musician, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Play through The Actor's Story and get the following Ending: ENDING",
                data={
                    "ENDING": (self.endings_actor, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Play through The Director's Story",
                data={
                    "ENDING": (self.endings_actor, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Collect COUNT COLLECTIBLE from the Painter's Story",
                data={
                    "COUNT": (self.collectibles_painter_count_range, 1),
                    "COLLECTIBLE": (self.collectibles_painter, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="In the Painter's Story, collect one of the following Rat Sketches: RAT_SKETCHES",
                data={
                    "RAT_SKETCHES": (self.rat_sketches, 3),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Collect COUNT COLLECTIBLE from the Actor's Story",
                data={
                    "COUNT": (self.collectibles_actor_low_count_range, 1),
                    "COLLECTIBLE": (self.collectibles_actor_low, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Collect COUNT COLLECTIBLE from the Actor's Story",
                data={
                    "COUNT": (self.collectibles_actor_high_count_range, 1),
                    "COLLECTIBLE": (self.collectibles_actor_high, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="In the Actor's Story, collect one of the following Movie Posters: MOVIE_POSTERS",
                data={
                    "MOVIE_POSTERS": (self.movie_posters, 3),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
        ]

    @staticmethod
    def endings_painter() -> List[str]:
        return [
            "Family",
            "Art",
            "Loop",
        ]

    @staticmethod
    def endings_daughter() -> List[str]:
        return [
            "Forgiveness",
            "Resentment",
            "Truth",
        ]

    @staticmethod
    def endings_musician() -> List[str]:
        return [
            "Acceptance",
            "Loneliness",
        ]

    @staticmethod
    def endings_actor() -> List[str]:
        return [
            "The Flame",
            "Always",
            "Formless",
        ]

    @staticmethod
    def collectibles_painter() -> List[str]:
        return [
            "Family Mementos",
            "Rat Sketches",
        ]

    @staticmethod
    def collectibles_painter_count_range() -> range:
        return range(3, 9)

    @staticmethod
    def rat_sketches() -> List[str]:
        return [
            "Prosthesis Snatchers",
            "Lice Mice",
            "Canvas Crawlers",
            "Plague Breeders",
            "Silent Floaters",
            "Flapping Horror",
            "Fluffy Fakers",
            "Screeching Arsonists",
            "Rodent Seeds",
            "Floor Creepers",
            "Vermin Growth",
            "Haunting Mimics",
            "Body Borrowers",
        ]

    @staticmethod
    def collectibles_actor_low() -> List[str]:
        return [
            "Phonograph Interviews",
            "Spyglass Items",
            "Mysterious Items",
        ]

    @staticmethod
    def collectibles_actor_low_count_range() -> range:
        return range(2, 5)

    @staticmethod
    def collectibles_actor_high() -> List[str]:
        return [
            "Movie Posters",
            "Photo Slides",
        ]

    @staticmethod
    def collectibles_actor_high_count_range() -> range:
        return range(3, 9)

    @staticmethod
    def movie_posters() -> List[str]:
        return [
            "Remember Her",
            "Double Shadows",
            "Twelfth Night",
            "Hamlet",
            "The Night Fiend",
            "Metropolis",
            "The Pirate Prince and The Cyclops King",
            "A Wondrous Voyage",
            "The Tempest",
            "The Trial of a Martyr",
            "Shizo",
            "King Lear",
        ]

# Archipelago Options
# ...
