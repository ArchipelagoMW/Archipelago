from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import DefaultOnToggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class KingdomHeartsMelodyOfMemoryArchipelagoOptions:
    kingdom_hearts_melody_of_memory_include_world_tour: MelodyOfMemoryIncludeWorldTour


class KingdomHeartsMelodyOfMemoryGame(Game):
    name = "Kingdom Hearts: Melody of Memory"
    platform = KeymastersKeepGamePlatforms.SW

    platforms_other = [
        KeymastersKeepGamePlatforms.PC,
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.XONE,
    ]

    is_adult_only_or_unrated = False

    options_cls = KingdomHeartsMelodyOfMemoryArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play as TEAM using the following style: STYLE",
                data={
                    "TEAM": (self.teams, 1),
                    "STYLE": (self.styles, 1),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Complete SONG on DIFFICULTY difficulty",
                data={
                    "SONG": (self.songs, 1),
                    "DIFFICULTY": (self.difficulties, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Full Combo SONG on DIFFICULTY difficulty",
                data={
                    "SONG": (self.songs, 1),
                    "DIFFICULTY": (self.difficulties, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
        ]

        if self.include_world_tour:
            templates.append(
                GameObjectiveTemplate(
                    label="Complete all songs in WORLD",
                    data={
                        "WORLD": (self.world_modes, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                )
            )

            templates.append(
                GameObjectiveTemplate(
                    label="Complete all songs in WORLD, gaining at least COUNT Stars",
                    data={
                        "WORLD": (self.world_modes, 1),
                        "COUNT": (self.star_count_range, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                )
            )

        return templates

    @property
    def include_world_tour(self) -> bool:
        return bool(self.archipelago_options.kingdom_hearts_melody_of_memory_include_world_tour.value)

    @staticmethod
    def songs() -> List[str]:
        return [
            "[KH] Kairi I (Dive)",
            "[KH] Simple And Clean (Dive)",
            "[KH] Simple And Clean (Field)",
            "[KH] Destiny Islands",
            "[KH] Bustin' Up on the Beach",
            "[KH] Traverse Town",
            "[KH] Welcome to Wonderland",
            "[KH] To Our Surprise",
            "[KH] Olympus Coliseum",
            "[KH] Go for It!",
            "[KH] Hand in Hand",
            "[KH] A Day in Agrabah",
            "[KH] Arabian Dream",
            "[KH] A Very Small Wish",
            "[KH] Monstrous Monstro",
            "[KH] Under the Sea",
            "[KH] An Adventure in Atlantica",
            "[KH] This is Halloween",
            "[KH] Spooks of Halloween Town",
            "[KH] Captain Hook's Pirate Ship",
            "[KH] Pirate's Gique",
            "[KH] Hollow Bastion",
            "[KH] Scherzo Di Notte",
            "[KH] End of the World",
            "[KH] Fragments of Sorrow",
            "[KH] Night of Fate",
            "[KH] Destiny's Force",
            "[KH] Shrouding Dark Cloud",
            "[KH] Squirming Evil",
            "[KH] Guardando nel buio (Field)",
            "[KH] Guardando nel buio (Boss)",
            "[KH] One-Winged Angel (from FINAL FANTASY VII)",
            "[KH] Another Side",
            "[KHCOM] Naminé (Dive)",
            "[KHCOM] Castle Ovlivion",
            "[KHCOM] Forgotten Challenge",
            "[KHCOM] The Force in You",
            "[KHCOM] Lord of the Castle",
            "[KHII] Sora (Dive)",
            "[KHII] Riku (Dive)",
            "[KHII] Roxas (Dive)",
            "[KHII] Part of Your World (Dive)",
            "[KHII] Sanctuary ~opening version~ (Dive)",
            "[KHII] Sanctuary ~opening version~ (Field)",
            "[KHII] Lazy Afternoons",
            "[KHII] Sinister Sundown",
            "[KHII] The Afternoon Streets",
            "[KHII] Working Together",
            "[KHII] Magical Mystery",
            "[KHII] Reviving Hollow Bastion",
            "[KHII] Scherzo Di Notte",
            "[KHII] Waltz of the Damned",
            "[KHII] Dance of the Daring",
            "[KHII] The Home of Dragons",
            "[KHII] Fields of Honor",
            "[KHII] The Underworld",
            "[KHII] What Lies Beneath",
            "[KHII] Monochrome Dreams",
            "[KHII] Old Friends, Old Rivals",
            "[KHII] Adventures in the Savannah",
            "[KHII] Savannah Pride",
            "[KHII] Space Paranoids",
            "[KHII] Byte Bashing",
            "[KHII] Sacred Moon",
            "[KHII] Deep Drive",
            "[KHII] Tension Rising",
            "[KHII] The 13th Struggle",
            "[KHII] Desire for All That is Lost",
            "[KHII] Vim and Vigor",
            "[KHII] Rowdy Rumble",
            "[KHII] Sinister Shadows",
            "[KHII] The 13th Dilemma",
            "[KHII] Darkness of the Unknown (Field)",
            "[KHII] Darkness of the Unknown (Boss)",
            "[KHII] What A Surprise?!",
            "[KHII] Happy Holidays!",
            "[KHII] The Other Promise",
            "[KHII] Rage Awakened",
            "[KHII] Fate of the Unknown",
            "[KHDays] Musique pour la tristesse de Xion (Dive)",
            "[KHDays] Secret of Neverland",
            "[KHDays] Crossing to Neverland",
            "[KHDays] Fight and Away",
            "[KHDays] Vector to the Heavens",
            "[KHDays] Another Side -Battle Ver.-",
            "[KHCoded] Wonder of Electron",
            "[KHCoded] No More Bugs!!",
            "[KHBBS] Terra (Dive)",
            "[KHBBS] Ventus (Dive)",
            "[KHBBS] Aqua (Dive)",
            "[KHBBS] The Promised Beginning",
            "[KHBBS] Future Masters",
            "[KHBBS] The Secret Whispers",
            "[KHBBS] Risky Romp",
            "[KHBBS] Bibbidi-Bobbidi-Boo",
            "[KHBBS] Castle Escapade",
            "[KHBBS] The Silent Forest",
            "[KHBBS] The Rustling Forest",
            "[KHBBS] Radiant Garden",
            "[KHBBS] Black Garden",
            "[KHBBS] Mickey Mouse March",
            "[KHBBS] Up Down Adventure",
            "[KHBBS] Hau'oli, Hau'oli",
            "[KHBBS] Mákaukau?",
            "[KHBBS] Daydream upon Neverland",
            "[KHBBS] Neverland's Scherzo",
            "[KHBBS] The Tumbling",
            "[KHBBS] The Encounter -Birth by Sleep Version- (Field)",
            "[KHBBS] The Encounter -Birth by Sleep Version- (Boss)",
            "[KHBBS] Enter the Darkness",
            "[KHBBS] Black Powder",
            "[KHBBS] Rage Awakened -The Origin-",
            "[KHBBS] Dismiss",
            "[KH3D] Traverse in Trance",
            "[KH3D] Hand to Hand",
            "[KH3D] La Cloche",
            "[KH3D] Le Sanctuaire",
            "[KH3D] Access the Grid",
            "[KH3D] Digital Domination",
            "[KH3D] The Fun Fair",
            "[KH3D] Prankster's Party",
            "[KH3D] One for All",
            "[KH3D] All for One",
            "[KH3D] Sacred Distance",
            "[KH3D] Deep Drop",
            "[KH3D] Majestic Wings",
            "[KH3D] L'Oscurità dell'Ignoto",
            "[KH3D] L'Impeto Oscuro",
            "[KH3D] The Eye of Darkness",
            "[KH3D] CALLING -KINGDOM MIX-",
            "[KHBBS0.2] Wave of Darkness I",
            "[KHIII] You've Got a Friend in Me -KINGDOM HEARTS III Version-",
            "[KHIII] Happy Hair Day",
            "[KHIII] Monster Smash!",
            "[KHIII] Let It Go",
            "[KHIII] Robot Overdrive",
            "[KHIII] Don't Think Twice (Dive)",
            "[KHIII] Don't Think Twice (Field)",
            "[KHIII] Graveyard Labyrinth",
            "[KHIII] Rise of the Union",
            "[KHIII] Dark Domination (Field)",
            "[KHIII] Dark Domination (Boss)",
            "[OTHER] Hand in Hand",
            "[OTHER] Working Together - Allegro vivace",
            "[OTHER] Sora - Allegro con brio",
            "[OTHER] Medley of Conflict",
            "[OTHER] Destati",
            "[OTHER] Beauty and the Beast",
            "[OTHER] A Whole New World",
            "[OTHER] Circle Of Life",
        ]

    def world_modes(self) -> List[str]:
        world_modes: List[str] = [
            "[KHBBS0.2] Writhing Melody",
            "[KH] Destiny Islands",
            "[KH] Melody of Fate",
            "[KH] Melody of Destruction",
            "[KH] Traverse Town",
            "[KH] Melody of Beginnings",
            "[KH] Wonderland",
            "[KH] Agrabah",
            "[KH] Atlantica",
            "[KH] Halloween Town",
            "[KH] Never Land",
            "[KH] Olympus Coliseum",
            "[KH] Monstro",
            "[KH] Hollow Bastion",
            "[KH] Wicked Melody",
            "[KH] End of the World",
            "[KH] Seeker of Darkness",
            "[KHCOM] Castle Oblivion",
            "[KHCOM] Melody Without a Heart",
            "[KHCOM] False Melody",
            "[KHCOM] Melody of Oblivion",
            "[KHII] The Other Twilight Town",
            "[KHII] Melody of Waking",
            "[KHII] Twilight Town",
            "[KH358DAYS] Never Land",
            "[KH358DAYS] Soaring Melody",
            "[KH358DAYS] Melody of Returning",
            "[KH358DAYS] Melody of the Dark Path",
            "[KHII] The Mysterious Tower",
            "[KHII] Beast's Castle",
            "[KHII] Halloween Town",
            "[KHII] Dancing Melody",
            "[KHII] Tricksters' Melody",
            "[KHII] Timeless River",
            "[KHII] The Land Of Dragons",
            "[KHII] Melody of Lost Loyalty",
            "[KHII] Olympus Coliseum",
            "[KHII] Pride Lands",
            "[KHII] Radiant Garden",
            "[KHII] Crushing Melody",
            "[KHII] Space Paranoids",
            "[KHII] The World That Never Was",
            "[KHII] Melody of Betrayal",
            "[KHII] Superior of the In-Between",
            "[KHCODED] System Sector",
            "[KHBBS] The Land of Departure",
            "[KHBBS] Castle of Dreams",
            "[KHBBS] Negative Melody",
            "[KHBBS] Deep Space",
            "[KHBBS] Radiant Garden",
            "[KHBBS] Dwarf Woodlands",
            "[KHBBS] Disney Town",
            "[KHBBS] Enchanted Dominion",
            "[KHBBS] Never Land",
            "[KHBBS] Evil Fairy",
            "[KHBBS] Melody of Pure Darkness",
            "[KHBBS] Melody of Culmination",
            "[KHBBS] Melody of Will",
            "[KHBBS] Unwavering Melody",
            "[KH3D] Traverse Town",
            "[KH3D] The Grid",
            "[KH3D] La Cité des Cloches",
            "[KH3D] Reverent Melody",
            "[KH3D] Prankster's Paradise",
            "[KH3D] Country of the Musketeers",
            "[KH3D] The World That Never Was",
            "[KH3D] Temporal Melody",
            "[KH3D] Melody of Slumber",
            "[KH3D] Dreaming Melody",
            "[KHIII] Toy Box",
            "[KHIII] Kingdom of Corona",
            "[KHIII] Monstropolis",
            "[KHIII] San Fransokyo",
            "[KHIII] Arendelle",
            "[KHIII] The Keyblade Graveyard",
            "[KHIII] Melody of Past Light",
        ]

        if self.include_time_consuming_objectives:
            world_modes.append("[KHIII] Melody of Memory's End")

        if self.include_difficult_objectives:
            world_modes.extend([
                "[KHFM] One-Winged Melody",
                "[KHIIFM] Lingering Melody",
                "[KHIIFM] Melody of Clashing Keys",
            ])

        return world_modes

    @staticmethod
    def teams() -> List[str]:
        return [
            "Team Classic",
            "Team Days",
            "Team 3D",
            "Team BBS",
        ]

    @staticmethod
    def difficulties() -> List[str]:
        return [
            "Beginner",
            "Standard",
            "Proud",
        ]

    @staticmethod
    def styles() -> List[str]:
        return [
            "Basic",
            "One Button",
            "Performer",
        ]

    @staticmethod
    def star_count_range() -> range:
        return range(1, 4)


# Archipelago Options
class MelodyOfMemoryIncludeWorldTour(DefaultOnToggle):
    """
    Indicates whether the player wants to include World Tour objectives
    """

    display_name = "Kingdom Hearts Melody of Memory Include World Tour"
