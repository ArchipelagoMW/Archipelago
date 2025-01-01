from typing import Any, Dict

MuseDashPresets: Dict[str, Dict[str, Any]] = {
    # An option to support Short Sync games. 40 songs.
    "No DLC - Short": {
        "dlc_packs": [],
        "starting_song_count": 5,
        "additional_song_count": 34,
        "music_sheet_count_percentage": 20,
        "music_sheet_win_count_percentage": 90,
    },
    # An option to support Short Sync games but adds variety. 40 songs.
    "DLC - Short": {
        "dlc_packs": ["Muse Plus"],
        "starting_song_count": 5,
        "additional_song_count": 34,
        "music_sheet_count_percentage": 20,
        "music_sheet_win_count_percentage": 90,
    },
    # An option to support Longer Sync/Async games. 100 songs.
    "DLC - Long": {
        "dlc_packs": ["Muse Plus"],
        "starting_song_count": 8,
        "additional_song_count": 91,
        "music_sheet_count_percentage": 20,
        "music_sheet_win_count_percentage": 90,
    },
}
