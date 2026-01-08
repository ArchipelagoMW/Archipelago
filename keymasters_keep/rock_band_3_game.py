from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class RockBand3ArchipelagoOptions:
    rock_band_3_nds_only: RockBand3NDSOnly


class RockBand3Game(Game):
    # Initial implementation by JCBoorgo

    name = "Rock Band 3"
    platform = KeymastersKeepGamePlatforms.PS3

    platforms_other = [
        KeymastersKeepGamePlatforms.X360,
        KeymastersKeepGamePlatforms.WII,
        KeymastersKeepGamePlatforms.NDS
    ]

    is_adult_only_or_unrated = False

    options_cls = RockBand3ArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play TRACK",
                data={"TRACK": (self.tracks, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Get a Full Combo on TRACK",
                data={"TRACK": (self.tracks, 1)},
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
        ]

    def tracks(self) -> List[str]:
        track_list = self.tracks_nds

        if not self.archipelago_options.rock_band_3_nds_only.value:
            track_list += self.tracks_base

        return sorted(track_list)

    @functools.cached_property
    def tracks_base(self) -> List[str]:
        return [
            "20th Century Boy",
            "25 or 6 to 4",
            "Antibodies",
            "Beast and the Harlot",
            "The Beautiful People",
            "Before I Forget",
            "Caught in a Mosh",
            "Centerfold",
            "The Con",
            "Dead End Friends",
            "Don't Bury Me... I'm Still Not Dead",
            "Don't Stand So Close to Me",
            "Du Hast",
            "Everybody Wants to Rule the World",
            "False Alarm",
            "Fly Like an Eagle",
            "Foolin'",
            "Free Bird",
            "Get Up, Stand Up",
            "Good Vibrations (Live)",
            "Heart of Glass",
            "Hey Man, Nice Shot",
            "I Can See for Miles",
            "I Got You (I Feel Good) (Alternative Version)",
            "I Need to Know",
            "I Wanna Be Sedated",
            "Imagine",
            "In a Big Country",
            "In the Meantime",
            "Jerry Was a Race Car Driver",
            "Killing Loneliness",
            "The Killing Moon",
            "King George",
            "Last Dance",
            "Living in America",
            "Llama",
            "Low Rider",
            "Me Enamora",
            "No One Knows",
            "One Armed Scissor",
            "Outer Space",
            "Oye Mi Amor",
            "Plush",
            "The Power of Love",
            "Radar Love",
            "Rainbow in the Dark",
            "Rehab",
            "Saturday Night's Alright for Fighting",
            "Smoke on the Water",
            "Something Bigger, Something Brighter",
            "Space Oddity",
            "Stop Me If You Think You've Heard This One Before",
            "This Bastard's Life",
            "Viva la Resistance",
            "Walk of Life",
            "Werewolves of London",
            "Whip It",
            "Yoshimi Battles the Pink Robots Pt. 1"
        ]

    @functools.cached_property
    def tracks_nds(self) -> List[str]:
        return [
            "Been Caught Stealing",
            "Bohemian Rhapsody",
            "Break on Through (To the Other Side)",
            "China Grove",
            "Cold as Ice",
            "Combat Baby",
            "Crazy Train",
            "Crosstown Traffic",
            "Get Free",
            "The Hardest Button to Button",
            "Here I Go Again",
            "Humanoid",
            "I Love Rock N' Roll",
            "Just Like Heaven",
            "Lasso",
            "The Look",
            "Midlife Crisis",
            "Misery Business",
            "Need You Tonight",
            "Oh My God",
            "Portions for Foxes",
            "Rock Lobster",
            "Roundabout",
            "Sister Christian",
            "Walkin' on the Sun"
        ]


# Archipelago Options
class RockBand3NDSOnly(Toggle):
    """
    Indicates whether to only include the Nintendo DS tracks in the list for Rock Band 3.
    """

    display_name = "Rock Band 3 NDS Only"
