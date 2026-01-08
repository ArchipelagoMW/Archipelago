from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class JackboxPartyPacksArchipelagoOptions:
    jackbox_party_packs_games_owned: JackboxPartyPacksGamesOwned


class JackboxPartyPacksGame(Game):
    name = "Jackbox Party Packs"
    platform = KeymastersKeepGamePlatforms.META

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = JackboxPartyPacksArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play a round of MINIGAME",
                data={
                    "MINIGAME": (self.minigames, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Play a round of MINIGAMES",
                data={
                    "MINIGAMES": (self.minigames, 3)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Play a full game of GAME",
                data={
                    "GAME": (self.games_owned, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Play a round of your favorite game in GAME",
                data={
                    "GAME": (self.games_owned_no_singles, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
        ]

    @staticmethod
    def games() -> List[str]:
        return [
            "Fibbage",
            "Jackbox Naughty Pack",
            "Jackbox Survey Scramble",
            "The Jackbox Party Pack 1",
            "The Jackbox Party Pack 10",
            "The Jackbox Party Pack 2",
            "The Jackbox Party Pack 3",
            "The Jackbox Party Pack 4",
            "The Jackbox Party Pack 5",
            "The Jackbox Party Pack 6",
            "The Jackbox Party Pack 7",
            "The Jackbox Party Pack 8",
            "The Jackbox Party Pack 9",
            "You Don't Know Jack",
        ]

    def games_owned(self) -> List[str]:
        return sorted(self.archipelago_options.jackbox_party_packs_games_owned.value)

    def games_owned_no_singles(self) -> List[str]:
        games_owned: List[str] = self.games_owned()

        game: str
        return [game for game in games_owned if game != "Fibbage" and game != "You Don't Know Jack"]

    def minigames(self) -> List[str]:
        minigames: List[str] = list()
        games_owned: List[str] = self.games_owned()

        if "Fibbage" in games_owned:
            minigames.append("Fibbage")

        if "Jackbox Naughty Pack" in games_owned:
            minigames.extend([
                "Dirty Drawful (JNP)",
                "Fakin' It! All Night Long (JNP)",
                "Let Me Finish (JNP)",
            ])

        if "Jackbox Survey Scramble" in games_owned:
            minigames.extend([
                "Bounce (JSS)",
                "Dares (JSS)",
                "Dash (JSS)",
                "HiLo (JSS)",
                "Speed (JSS)",
                "Squares (JSS)",
                "Tour (JSS)",
            ])

        if "The Jackbox Party Pack 1" in games_owned:
            minigames.extend([
                "Drawful (JPP1)",
                "Fibbage XL (JPP1)",
                "Lie Swatter (JPP1)",
                "Word Spud (JPP1)",
                "You Don't Know Jack 2015 (JPP1)",
            ])

        if "The Jackbox Party Pack 2" in games_owned:
            minigames.extend([
                "Bidiots (JPP2)",
                "Bomb Corp. (JPP2)",
                "Earwax (JPP2)",
                "Fibbage 2 (JPP2)",
                "Quiplash XL (JPP2)",
            ])

        if "The Jackbox Party Pack 3" in games_owned:
            minigames.extend([
                "Fakin It! (JPP3)",
                "Guesspionage (JPP3)",
                "Quiplash 2 (JPP3)",
                "TEE K.O. (JPP3)",
                "Trivia Murder Party (JPP3)",
            ])

        if "The Jackbox Party Pack 4" in games_owned:
            minigames.extend([
                "Bracketeering (JPP4)",
                "Civic Doodle (JPP4)",
                "Fibbage 3 (JPP4)",
                "Monster Seeking Monster (JPP4)",
                "Survive The Internet (JPP4)",
            ])

        if "The Jackbox Party Pack 5" in games_owned:
            minigames.extend([
                "Mad Verse City (JPP5)",
                "Patently Stupid (JPP5)",
                "Split The Room (JPP5)",
                "You Don't Know Jack The Full Stream (JPP5)",
                "Zeeple Dome (JPP5)",
            ])

        if "The Jackbox Party Pack 6" in games_owned:
            minigames.extend([
                "Diction*arium (JPP6)",
                "Joke Boat (JPP6)",
                "Push The Button (JPP6)",
                "Role Models (JPP6)",
                "Trivia Murder Party 2 (JPP6)",
            ])

        if "The Jackbox Party Pack 7" in games_owned:
            minigames.extend([
                "Blather 'Round (JPP7)",
                "Champ'd Up (JPP7)",
                "Quiplash 3 (JPP7)",
                "Talking Points (JPP7)",
                "The Devils And The Details (JPP7)",
            ])

        if "The Jackbox Party Pack 8" in games_owned:
            minigames.extend([
                "Drawful Animate (JPP8)",
                "Job Job (JPP8)",
                "The Poll Mine (JPP8)",
                "The Wheel Of Enormous Proportion (JPP8)",
                "Weapons Drawn (JPP8)",
            ])

        if "The Jackbox Party Pack 9" in games_owned:
            minigames.extend([
                "Fibbage 4 (JPP9)",
                "Junktopia (JPP9)",
                "Nonsensory (JPP9)",
                "Quixort (JPP9)",
                "Roomerang (JPP9)",
            ])

        if "The Jackbox Party Pack 10" in games_owned:
            minigames.extend([
                "DodoReMi (JPP10)",
                "Fixy Text (JPP10)",
                "Hypnotorious (JPP10)",
                "TEE K.O. 2 (JPP10)",
                "Time Jinx (JPP10)",
            ])

        if "You Don't Know Jack" in games_owned:
            minigames.append("You Don't Know Jack")

        return sorted(minigames)


# Archipelago Options
class JackboxPartyPacksGamesOwned(OptionSet):
    """
    Indicates which games the players owns from the Jackbox Party Packs series.
    """

    display_name = "Jackbox Party Packs Games Owned"
    valid_keys = JackboxPartyPacksGame().games()

    default = valid_keys
