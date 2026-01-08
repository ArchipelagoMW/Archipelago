from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import OptionSet, Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class DeemoRebornArchipelagoOptions:
    deemo_reborn_dlc_owned: DeemoRebornDLCOwned
    deemo_reborn_platform_exclusive_content: DeemoRebornPlatformExclusiveContent
    deemo_reborn_include_stone_monument_songs: DeemoRebornIncludeStoneMonumentSongs


class DeemoRebornGame(Game):
    name = "Deemo -Reborn-"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.AND,
        KeymastersKeepGamePlatforms.IOS,
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.SW,
    ]

    is_adult_only_or_unrated = False

    options_cls = DeemoRebornArchipelagoOptions

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
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Play SONGS on DIFFICULTY difficulty",
                data={
                    "SONGS": (self.songs, 3),
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
                is_difficult=True,
                weight=1,
            ),
        ]

    @property
    def dlc_owned(self) -> List[str]:
        return sorted(self.archipelago_options.deemo_reborn_dlc_owned.value)

    @property
    def has_dlc_aioi_collection(self) -> bool:
        return "Aioi collection" in self.dlc_owned

    @property
    def has_dlc_eshen_chen_collection_vol_1_transmission(self) -> bool:
        return "Eshen Chen collection Vol.1:Transmission" in self.dlc_owned

    @property
    def has_dlc_greatest_hits_vol_1(self) -> bool:
        return "Greatest Hits Vol.1" in self.dlc_owned

    @property
    def has_dlc_greatest_hits_vol_2(self) -> bool:
        return "Greatest Hits Vol.2" in self.dlc_owned

    @property
    def has_dlc_knight_iris_collection(self) -> bool:
        return "Knight Iris collection" in self.dlc_owned

    @property
    def has_dlc_knight_rosabell_collection(self) -> bool:
        return "Knight Rosabell collection" in self.dlc_owned

    @property
    def has_dlc_m2u_x_nicode_collection(self) -> bool:
        return "M2U x Nicode Collection" in self.dlc_owned

    @property
    def has_dlc_mili_collection(self) -> bool:
        return "MILI collection" in self.dlc_owned

    @property
    def has_dlc_n_m_s_t_collection(self) -> bool:
        return "N.M.S.T. collection" in self.dlc_owned

    @property
    def has_dlc_rayark_selection_vol_1(self) -> bool:
        return "Rayark Selection Vol.1" in self.dlc_owned

    @property
    def has_dlc_rayark_selection_vol_2(self) -> bool:
        return "Rayark Selection Vol.2" in self.dlc_owned

    @property
    def has_dlc_taiko_no_tatsujin_collection(self) -> bool:
        return "Taiko no Tatsujin Collection" in self.dlc_owned

    @property
    def platform_exclusive_content(self) -> List[str]:
        return sorted(self.archipelago_options.deemo_reborn_platform_exclusive_content.value)

    @property
    def include_stone_monument_songs(self) -> bool:
        return bool(self.archipelago_options.deemo_reborn_include_stone_monument_songs.value)

    @functools.cached_property
    def songs_deemos_collection_vol_1(self) -> List[str]:
        return [
            "[Vol.1] Dream",
            "[Vol.1] Jumpy star",
            "[Vol.1] Nine point eight",
            "[Vol.1] Run Go Run",
            "[Vol.1] YUBIKIRI-GENMAN",
            "[Vol.1] Walking by the sea",
            "[Vol.1] Entrance",
            "[Vol.1] Magnolia",
            "[Vol.1] Saika",
            "[Vol.1] Beyond The Stratus",
            "[Vol.1] Light pollution",
            "[Vol.1] Utopiosphere",
            "[Vol.1] Angelic Sphere",
            "[Vol.1] Electron",
            "[Vol.1] Untitled2",
            "[Vol.1] Undo",
            "[Vol.1] I hate to tell you",
            "[Vol.1] Platinum",
            "[Vol.1] Leviathan",
            "[Vol.1] Invite",
            "[Vol.1] Pulses",
            "[Vol.1] SAIRAI",
        ]

    @functools.cached_property
    def songs_deemos_collection_vol_2(self) -> List[str]:
        return [
            "[Vol.2] Suspenseful Third Day",
            "[Vol.2] Legacy",
            "[Vol.2] Myosotis",
            "[Vol.2] ANiMA",
            "[Vol.2] Fluquor",
            "[Vol.2] Living In The One",
            "[Vol.2] La Promesse",
            "[Vol.2] The Beautiful Moonlight",
            "[Vol.2] Sunset",
            "[Vol.2] Ark of Desire",
            "[Vol.2] Starting Wind",
        ]

    @functools.cached_property
    def songs_vocal_collection(self) -> List[str]:
        return [
            "[Vocal] Pharmacy of heart",
            "[Vocal] Aurarobe",
            "[Vocal] Red Storm Sentiment",
            "[Vocal] Ukakuf Kins",
            "[Vocal] Faith, Hope & Love",
            "[Vocal] vandarhythm",
            "[Vocal] Re:you ~Even if the one knew the world~",
            "[Vocal] Chance",
            "[Vocal] My Dear, Deemo",
        ]

    @functools.cached_property
    def songs_golden_sheets_collection(self) -> List[str]:
        return [
            "[Golden Sheets] Nier Fluquor",
            "[Golden Sheets] Mayoizuki",
            "[Golden Sheets] Prélude de l'adieu",
            "[Golden Sheets] Aitai",
            "[Golden Sheets] Für Alice",
            "[Golden Sheets] Mirai",
        ]

    @functools.cached_property
    def songs_reborn_collection(self) -> List[str]:
        return [
            "[Reborn] Me",
            "[Reborn] Blue evenfall",
            "[Reborn] Dawn of the ruins",
            "[Reborn] The Last Bloom",
            "[Reborn] Code:11",
            "[Reborn] Delphinium",
            "[Reborn] Accelerando",
            "[Reborn] Tempestuous",
            "[Reborn] Exodus",
            "[Reborn] eterno",
            "[Reborn] liar",
            "[Reborn] Squeaky Mind",
            "[Reborn] Place Your Bets",
        ]

    @functools.cached_property
    def songs_stone_monument(self) -> List[str]:
        return [
            "[Stone Monument] Etude",
            "[Stone Monument] Xing-Lai Heaven",
            "[Stone Monument] Creation of Fighters",
            "[Stone Monument] Interstellar Exploration",
            "[Stone Monument] saihate",
        ]

    @functools.cached_property
    def songs_egoist_special_selection(self) -> List[str]:
        return [
            "[EGOIST (PS4)] All Alone With You",
            "[EGOIST (PS4)] Planetes",
            "[EGOIST (PS4)] KIMI SORA KISEKI",
            "[EGOIST (PS4)] DEPARTURES ANATANI OKURU AINO UTA",
            "[EGOIST (PS4)] Ghost of a smile",
        ]

    @functools.cached_property
    def songs_rayark_selection_vol_1(self) -> List[str]:
        return [
            "[Rayark Selection Vol.1] Metal Hypnotized",
            "[Rayark Selection Vol.1] Rainy Memory",
            "[Rayark Selection Vol.1] Peach Lady",
            "[Rayark Selection Vol.1] Pilot",
            "[Rayark Selection Vol.1] vivere la vita",
            "[Rayark Selection Vol.1] The Letter",

        ]

    @functools.cached_property
    def songs_mili_collection(self) -> List[str]:
        return [
            "[MILI] Fable",
            "[MILI] Past the Stargazing Season",
            "[MILI] Ephemeral",
            "[MILI] Rosetta",
            "[MILI] Witch's Invitation",
        ]

    @functools.cached_property
    def songs_eshen_chen_collection_vol_1_transmission(self) -> List[str]:
        return [
            "[Eshen Chen collection Vol.1:Transmission] Sea Side Road",
            "[Eshen Chen collection Vol.1:Transmission] Run Away Run",
            "[Eshen Chen collection Vol.1:Transmission] Falling Ears",
            "[Eshen Chen collection Vol.1:Transmission] Flowers Above Your Head",
            "[Eshen Chen collection Vol.1:Transmission] Almost Morning",
        ]

    def songs_rayark_selection_vol_2(self) -> List[str]:
        songs: List[str] = [
            "[Rayark Selection Vol.2] Friction",
            "[Rayark Selection Vol.2] I race the dawn",
            "[Rayark Selection Vol.2] Moon without the stars",
            "[Rayark Selection Vol.2] Sanctity",
            "[Rayark Selection Vol.2] Altale",
        ]

        if "PC" in self.platform_exclusive_content:
            songs.append("[Rayark Selection Vol.2] Veritas")

        return songs

    def songs_n_m_s_t_collection(self) -> List[str]:
        songs: List[str] = [
            "[N.M.S.T.] Farewell",
            "[N.M.S.T.] Winter (Deemo ver.)",
            "[N.M.S.T.] Fluffie Partie",
            "[N.M.S.T.] Snowflakes",
        ]

        if "iOS" in self.platform_exclusive_content or "PlayStation 4" in self.platform_exclusive_content:
            songs.append("[N.M.S.T.] kouyou")

        return songs

    @functools.cached_property
    def songs_aioi_collection(self) -> List[str]:
        return [
            "[Aioi] CREAM STEW (Deemo Ver.)",
            "[Aioi] I can not say (DEEMO Ver.)",
            "[Aioi] Image (DEEMO Ver.)",
            "[Aioi] kireigoto (DEEMO Ver.)",
            "[Aioi] NEW WORLD (DEEMO Ver.)",
        ]

    @functools.cached_property
    def songs_knight_rosabell_collection(self) -> List[str]:
        return [
            "[Knight Rosabell] Lord Of Crimson Rose",
            "[Knight Rosabell] Predawn",
            "[Knight Rosabell] The Fallen Bloom",
            "[Knight Rosabell] Where You Are Not",
            "[Knight Rosabell] Music. The Eternity of Us",
        ]

    @functools.cached_property
    def songs_knight_iris_collection(self) -> List[str]:
        return [
            "[Knight Iris] The Way We Were",
            "[Knight Iris] The Sanctuary",
            "[Knight Iris] The Red Coronation",
            "[Knight Iris] Forbidden Codex",
            "[Knight Iris] Knight Of Firmament",
        ]

    @functools.cached_property
    def songs_greatest_hits_vol_1(self) -> List[str]:
        return [
            "[Greatest Hits Vol.1] Revival",
            "[Greatest Hits Vol.1] Oceanus",
            "[Greatest Hits Vol.1] Lifill",
            "[Greatest Hits Vol.1] LILI",
            "[Greatest Hits Vol.1] Wish upon a shooting star",
        ]

    @functools.cached_property
    def songs_greatest_hits_vol_2(self) -> List[str]:
        return [
            "[Greatest Hits Vol.2] AngelFalse",
            "[Greatest Hits Vol.2] Farewell Waltz",
            "[Greatest Hits Vol.2] Toys Etude",
            "[Greatest Hits Vol.2] Like Asian Spirit",
            "[Greatest Hits Vol.2] Infinite Puzzle",
        ]

    @functools.cached_property
    def songs_taiko_no_tatsujin_collection(self) -> List[str]:
        return [
            "[Taiko no Tatsujin] 3piece-JazzParty!",
            "[Taiko no Tatsujin] RIN",
            "[Taiko no Tatsujin] No Gravity",
            "[Taiko no Tatsujin] Toryu",
            "[Taiko no Tatsujin] KAICHUTEIEN WO MOTSU SYOUJO",
        ]

    @functools.cached_property
    def songs_m2u_x_nicode_collection(self) -> List[str]:
        return [
            "[M2U x Nicode] Loadstar",
            "[M2U x Nicode] LUNE",
            "[M2U x Nicode] Moon Halo",
            "[M2U x Nicode] Stellar",
            "[M2U x Nicode] Wicked Fate",
        ]

    def songs(self) -> List[str]:
        songs: List[str] = list()

        songs.extend(self.songs_deemos_collection_vol_1[:])
        songs.extend(self.songs_deemos_collection_vol_2[:])
        songs.extend(self.songs_vocal_collection[:])
        songs.extend(self.songs_golden_sheets_collection[:])
        songs.extend(self.songs_reborn_collection[:])

        if self.include_stone_monument_songs:
            songs.extend(self.songs_stone_monument[:])
        if "PlayStation 4" in self.platform_exclusive_content:
            songs.extend(self.songs_egoist_special_selection[:])
        if self.has_dlc_rayark_selection_vol_1:
            songs.extend(self.songs_rayark_selection_vol_1[:])
        if self.has_dlc_mili_collection:
            songs.extend(self.songs_mili_collection[:])
        if self.has_dlc_eshen_chen_collection_vol_1_transmission:
            songs.extend(self.songs_eshen_chen_collection_vol_1_transmission[:])
        if self.has_dlc_rayark_selection_vol_2:
            songs.extend(self.songs_rayark_selection_vol_2()[:])
        if self.has_dlc_n_m_s_t_collection:
            songs.extend(self.songs_n_m_s_t_collection()[:])
        if self.has_dlc_aioi_collection:
            songs.extend(self.songs_aioi_collection[:])
        if self.has_dlc_knight_rosabell_collection:
            songs.extend(self.songs_knight_rosabell_collection[:])
        if self.has_dlc_knight_iris_collection:
            songs.extend(self.songs_knight_iris_collection[:])
        if self.has_dlc_greatest_hits_vol_1:
            songs.extend(self.songs_greatest_hits_vol_1[:])
        if self.has_dlc_greatest_hits_vol_2:
            songs.extend(self.songs_greatest_hits_vol_2[:])
        if self.has_dlc_taiko_no_tatsujin_collection:
            songs.extend(self.songs_taiko_no_tatsujin_collection[:])
        if self.has_dlc_m2u_x_nicode_collection:
            songs.extend(self.songs_m2u_x_nicode_collection[:])

        return sorted(songs)

    @staticmethod
    def difficulties() -> List[str]:
        return [
            "Easy",
            "Normal",
            "Hard",
        ]


# Archipelago Options
class DeemoRebornDLCOwned(OptionSet):
    """
    Indicates which Deemo -Reborn- DLC the player owns, if any.
    """

    display_name = "Deemo -Reborn- DLC Owned"
    valid_keys = [
        "Aioi collection",
        "Eshen Chen collection Vol.1:Transmission",
        "Greatest Hits Vol.1",
        "Greatest Hits Vol.2",
        "Knight Iris collection",
        "Knight Rosabell collection",
        "M2U x Nicode Collection",
        "MILI collection",
        "N.M.S.T. collection",
        "Rayark Selection Vol.1",
        "Rayark Selection Vol.2",
        "Taiko no Tatsujin Collection",
    ]

    default = valid_keys


class DeemoRebornPlatformExclusiveContent(OptionSet):
    """
    Indicates which platform-exclusive content the player has access to in Deemo -Reborn-.
    """

    display_name = "Deemo -Reborn- Platform Exclusive Content"
    valid_keys = [
        "iOS",
        "PC",
        "PlayStation 4",
    ]

    default = valid_keys


class DeemoRebornIncludeStoneMonumentSongs(Toggle):
    """
    Indicates whether the player wants to include the Stone Monument Songs in their Deemo -Reborn- objectives.
    """

    display_name = "Deemo -Reborn- Include Stone Monument Songs"
