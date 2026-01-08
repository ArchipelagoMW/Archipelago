from __future__ import annotations

import functools
from typing import List, Set

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class TromboneChampArchipelagoOptions:
    trombone_champ_custom_tracks: TromboneChampCustomTracks


class TromboneChampGame(Game):
    name = "Trombone Champ"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.SW,
    ]

    is_adult_only_or_unrated = False

    options_cls = TromboneChampArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Get at least a RANK rank on TRACK",
                data={"RANK": (self.ranks, 1), "TRACK": (self.tracks, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Get an S rank on TRACK",
                data={"TRACK": (self.tracks, 1)},
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Play TRACKS and get at least 1 RANK rank",
                data={"TRACKS": (self.tracks, 3), "RANK": (self.ranks, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Play TRACKS and get at least 1 S rank",
                data={"TRACKS": (self.tracks, 3)},
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Play TRACK and finish with less than 10 Nasties",
                data={"TRACK": (self.tracks, 1)},
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Play TRACK on Turbo Mode",
                data={"TRACK": (self.tracks, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Unsack a CARD card",
                data={"CARD": (self.cards, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
        ]

    @property
    def custom_tracks(self) -> Set[str]:
        return self.archipelago_options.trombone_champ_custom_tracks.value

    @functools.cached_property
    def tracks_base(self) -> List[str]:
        return [
            "ARE U READY",
            "ARIRANG",
            "AULD LANG SYNE",
            "BABOONS!",
            "BALD MOUNTAIN",
            "BALL GAME",
            "BARBER OF SEVILLE",
            "BEETHOVEN'S FIFTH",
            "BLUE DANUBE",
            "BUMBLEBEE",
            "CAROL OF THE BELLS",
            "CHOP WALTZ",
            "COMMANDER TOKYO",
            "DANNY BOY",
            "EINE (CHAMP MIX)",
            "EINE KLEINE",
            "ENTERTAINER",
            "FOUR SEASONS (SUMMER)",
            "FUNICULI FUNICULA",
            "GLADIATORS",
            "GOD SAVE THE KING",
            "GYMNOPEDIE",
            "HABANERA",
            "HAPPY BIRTHDAY",
            "HAVA NAGILA",
            "HELLO! MA BABY",
            "HINO DO BRASIL",
            "HUNGARIAN RHAPSODY",
            "JARABE TAPATIO",
            "JASMINE FLOWER",
            "JINGLE BELLS",
            "KOROBEINIKI",
            "LONG-TAIL LIMBO",
            "MARS",
            "MARSEILLAISE",
            "MARTIAN KILLBOTS",
            "MERRY GENTLEMEN",
            "MOUNTAIN KING",
            "O CANADA",
            "O CHRISTMAS TREE",
            "ODE TO JOY",
            "OH HANUKKAH!",
            "OLD GRAY MARE",
            "OLD MACDONALD",
            "PUTTIN' ON THE RITZ",
            "RISING SUN BLUES",
            "ROSAMUNDE",
            "ROUND THE MOUNTAIN",
            "SAILOR'S HORNPIPE",
            "SAKURA",
            "SILENT NIGHT",
            "SKABIRD",
            "SKIP TO MY LOU",
            "ST JAMES TROMBONERY",
            "STARS & STRIPES",
            "STAR-SPANGLED",
            "SUGAR PLUM FAIRY",
            "T. CHAMP MEDLEY",
            "TAPS",
            "THE CAN-CAN",
            "THE RIVERSIDE",
            "THE SAINTS",
            "TOCCATE & FUGUE",
            "TROMBONE FUERTE",
            "TROMBONE SKYZE",
            "TROMBONE SKYZE (NASTY)",
            "W. POST MARCH",
            "WARM-UP",
            "WILLIAM TELL",
            "ZARATHUSTRA",
        ]

    def tracks(self) -> List[str]:
        return sorted(self.tracks_base + list(self.custom_tracks))

    @staticmethod
    def ranks() -> List[str]:
        return ["C", "B", "A"]

    @staticmethod
    def cards() -> List[str]:
        return [
            "Al Grey",
            "Arthur Pryor",
            "Babi",
            "Baboon",
            "Bass Clef",
            "Beethoven",
            "Bela Bartok",
            "Bill Watrous",
            "Blue-Eyes White Baboon",
            "Brass",
            "C.W. Gluck",
            "Claude Debussy",
            "Design your own",
            "Dick 'Slyde' Hyde",
            "Don Drummond",
            "Franz Schubert",
            "Glenn Miller",
            "Glissando",
            "Gustav Holst",
            "Gustav Mahler",
            "Hot Dog",
            "Igor Stravinsky",
            "J. Strauss II",
            "J.J. Johnson",
            "J.S. Bach",
            "Jack Teagarden",
            "John Philip Sousa",
            "Max Thundra",
            "Melba Liston",
            "Mouthpiece",
            "Mozart Musicstorm",
            "Mozart",
            "Music",
            "Mussorgsky",
            "Polidoro da Caravaggio",
            "Rachmaninoff",
            "Red-Eyes Black Baboon",
            "Richard Strauss",
            "Rimsky-Korsakov",
            "Roswell Rudd",
            "Sackbut",
            "Sergei Prokofiev",
            "Slide",
            "Tchaikovsky",
            "Tommy Dorsey",
            "Trazom",
            "Treble Clef",
            "Trombone",
            "Tromboner Cards",
            "Trumpet",
        ]


# Archipelago Options
class TromboneChampCustomTracks(OptionSet):
    """
    Indicates which Trombone Champ custom tracks the player has installed.
    """

    display_name = "Trombone Champ Custom Tracks"
    default = list()
