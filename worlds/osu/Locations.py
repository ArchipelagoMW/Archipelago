from typing import Callable, Dict, NamedTuple, Optional

from BaseClasses import Location, MultiWorld

from .Items import osu_song_max


class OsuLocation(Location):
    game: str = "osu!"


class OsuLocationData(NamedTuple):
    address: Optional[int] = None
    locked_item: Optional[str] = None


location_data_table: Dict[str, OsuLocationData] = {
}

for i in range(osu_song_max):
    location_data_table[f"Song {i+1} (Item 1)"] = OsuLocationData(
        address=727000000 + (2 * i),
    )
    location_data_table[f"Song {i + 1} (Item 2)"] = OsuLocationData(
        address=727000000 + (2 * i) + 1,
    )

location_table = {name: data.address for name, data in location_data_table.items() if data.address is not None}