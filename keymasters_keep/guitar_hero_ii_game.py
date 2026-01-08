from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class GuitarHeroIIArchipelagoOptions:
    guitar_hero_ii_bonus_tracks: GuitarHeroIIBonusTracks
    guitar_hero_ii_x360_tracks: GuitarHeroIIX360Tracks


class GuitarHeroIIGame(Game):
    # Initial implementation by JCBoorgo

    name = "Guitar Hero II"
    platform = KeymastersKeepGamePlatforms.PS2

    platforms_other = [KeymastersKeepGamePlatforms.X360]

    is_adult_only_or_unrated = False

    options_cls = GuitarHeroIIArchipelagoOptions

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
        track_list = self.tracks_base

        if self.archipelago_options.guitar_hero_ii_bonus_tracks.value:
            track_list += self.tracks_bonus

        if self.archipelago_options.guitar_hero_ii_x360_tracks.value:
            track_list += self.tracks_x360

        if (
            self.archipelago_options.guitar_hero_ii_bonus_tracks.value
            and self.archipelago_options.guitar_hero_ii_x360_tracks.value
        ):
            track_list += self.tracks_x360_bonus

        return sorted(track_list)

    @functools.cached_property
    def tracks_base(self) -> List[str]:
        # Some songs moved tiers between PS2 and X360, did my best to write these cleanly
        return [
            "Shout at the Devil (tier 1)",
            "Mother (tier 1/2)",
            "Surrender (tier 1)",
            "Woman (tier 1/2)",
            "Tonight I'm Gonna Rock You Tonight (tier 1/2)",
            "Strutter (tier 2/1)",
            "Heart-Shaped Box (tier 2/1)",
            "Message in a Bottle (tier 2/3)",
            "You Really Got Me (tier 2)",
            "Carry On Wayward Son (tier 2/3)",
            "Monkey Wrench (tier 3/4)",
            "Them Bones (tier 3)",
            "Search and Destroy (tier 3)",
            "Tattooed Love Boys (tier 3/5)",
            "War Pigs (tier 3)",
            "Cherry Pie (tier 4/2)",
            "Who Was in My Room Last Night? (tier 4)",
            "Girlfriend (tier 4)",
            "Can't You Hear Me Knockin' (tier 4)",
            "Sweet Child o' Mine (tier 4)",
            "Killing in the Name (tier 5/6)",
            "John the Fisherman (tier 5)",
            "Freya (tier 5/6)",
            "Bad Reputation (tier 5)",
            "Last Child (tier 5)",
            "Crazy on You (tier 6)",
            "Trippin' on a Hole in a Paper Heart (tier 6)",
            "Rock This Town (tier 6/7)",
            "Jessica (tier 6/5)",
            "Stop (tier 6)",
            "Madhouse (tier 7)",
            "Carry Me Home (tier 7/8)",
            "Laid to Rest (tier 7)",
            "Psychobilly Freakout (tier 7)",
            "YYZ (tier 7)",
            "Beast and the Harlot (tier 8)",
            "Institutionalized (tier 8)",
            "Misirlou (tier 8)",
            "Hangar 18 (tier 8)",
            "Free Bird (tier 8)",
        ]

    @functools.cached_property
    def tracks_bonus(self) -> List[str]:
        return [
            "Arterial Black (bonus)",
            "Collide (bonus)",
            "Elephant Bones (bonus)",
            "Fall of Pangea (bonus)",
            "FTK (bonus)",
            "Gemini (bonus)",
            "Jordan (bonus)",
            "Laughtrack (bonus)",
            "Less Talk More Rokk (bonus)",
            "Mr. Fix It (bonus)",
            "One for the Road (bonus)",
            "Parasite (bonus)",
            "Push Push (Lady Lightning) (bonus)",
            "Radium Eyes (bonus)",
            "Raw Dog (bonus)",
            "Red Lottery (bonus)",
            "Six (bonus)",
            "Soy Bomb (bonus)",
            "The Light That Blinds (bonus)",
            "The New Black (bonus)",
            "Thunderhorse (bonus)",
            "Trogdor (bonus)",
            "X-Stream (bonus)",
            "Yes We Can (bonus)",
        ]

    @functools.cached_property
    def tracks_x360(self) -> List[str]:
        return [
            "Possum Kingdom (tier 1)",
            "Salvation (tier 1)",
            "Life Wasted (tier 2)",
            "Billion Dollar Babies (tier 3)",
            "Hush (tier 4)",
            "Rock and Roll, Hoochie Koo (tier 5)",
            "Dead! (tier 6)",
            "The Trooper (tier 7)",
        ]

    @functools.cached_property
    def tracks_x360_bonus(self) -> List[str]:
        return ["Drink Up (bonus)", "Kicked to the Curb (bonus)"]


# Archipelago Options
class GuitarHeroIIBonusTracks(Toggle):
    """
    Indicates whether to include the bonus tracks in the list for Guitar Hero II.
    """

    display_name = "Guitar Hero II Bonus Tracks"


class GuitarHeroIIX360Tracks(Toggle):
    """
    Indicates whether to include the XBox 360 exclusive tracks in the list for Guitar Hero II.
    """

    display_name = "Guitar Hero II X360 Tracks"
