from typing import List, Tuple, Optional, Callable, NamedTuple
from BaseClasses import MultiWorld

EventId: Optional[int] = None


class LocationData(NamedTuple):
    region: str
    name: str
    code: Optional[int]
    rule: Callable = lambda state: True


def get_locations(world: Optional[MultiWorld], player: Optional[int]) -> Tuple[LocationData, ...]:
    # 1337000 - 1337155 Generic locations
    # 1337171 - 1337175 New Pickup checks
    # 1337246 - 1337249 Ancient Pyramid
    location_table: List[LocationData] = [
        # Forest of Silence locations
        LocationData('Forest of Silence - start', 'Forest of Silence - Grab Practice Pillars - Right',  0xC64001),
        # LocationData('Forest of Silence - start', 'Forest of Silence - Grab Practice Pillars - Left',  10001), #sub
        LocationData('Forest of Silence - start', 'Forest of Silence - Grab Practice Pillars - Top',  0xC64002),
        LocationData('Forest of Silence - start', 'Forest of Silence - Bone Mom\'s Bridge Start',  0xC64003),
        LocationData('Forest of Silence - switch 1', 'Forest of Silence - Lower Gazebo - Inside',  0xC64004),
        LocationData('Forest of Silence - switch 1', 'Forest of Silence - Lower Gazebo - Top',  0xC64005),
        LocationData('Forest of Silence - switch 1', 'Forest of Silence - Higher Gazebo - Inside',  0xC64006),
        LocationData('Forest of Silence - switch 1', 'Forest of Silence - Higher Gazebo - Top',  0xC64007),
        LocationData('Forest of Silence - switch 1', 'Forest of Silence - Weretiger Switch', 0xC64008),
        LocationData('Forest of Silence - switch 2', 'Forest of Silence - Beyond Weretiger Gate', 0xC64009),
        # LocationData('Forest of Silence - switch 2', 'Forest of Silence - Dirge Maiden Statue Plaque', 10010), #freestanding
        LocationData('Forest of Silence - switch 2', 'Forest of Silence - Dirge Maiden Tomb - Upper', 0xC6400A),
        LocationData('Forest of Silence - switch 2', 'Forest of Silence - Tri-Corpse Save Junction', 0xC6400B),
        LocationData('Forest of Silence - switch 2', 'Forest of Silence - Descending Bridge - Wall Side', 0xC6400C),
        LocationData('Forest of Silence - switch 2', 'Forest of Silence - Descending Bridge - Switch Side',  0xC6400D),
        LocationData('Forest of Silence - switch 3', 'Forest of Silence - Beyond Descending Bridge Gate - Left',  0xC6400E),
        LocationData('Forest of Silence - switch 3', 'Forest of Silence - Descending Bridge Gate Path Tomb - Upper-Top',  0xC6400F),
        LocationData('Forest of Silence - switch 3', 'Forest of Silence - Backfacing Tomb Lower-Front',  0xC64010),
        LocationData('Forest of Silence - switch 3', 'Forest of Silence - Invisible Bridge Platform',  0xC64011),
        # LocationData('Forest of Silence - switch 3', 'Forest of Silence - Werewolf Statue Plaque', 10020), #freestanding
        LocationData('Forest of Silence - switch 3', 'Forest of Silence - Werewolf Tomb - Right',  0xC64012),
        LocationData('Forest of Silence - switch 3', 'Forest of Silence - Werewolf Path - Near Tree', 0xC64013),
        LocationData('Forest of Silence - switch 3', 'Forest of Silence - Final Switch',  0xC64014),
        # LocationData('Forest of Silence - switch 2', 'Forest of Silence - Dirge Maiden Statue Pedestal', 10010), #sub
        # LocationData('Forest of Silence - switch 2', 'Forest of Silence - Dirge Maiden Tomb - Lower', 10011), #nothing
        # LocationData('Forest of Silence - switch 3', 'Forest of Silence - Beyond Descending Bridge Gate - Right',  10015), #sub
        # LocationData('Forest of Silence - switch 3', 'Forest of Silence - Descending Bridge Gate Path Tomb - Lower', 10016), #nothing
        # LocationData('Forest of Silence - switch 3', 'Forest of Silence - Descending Bridge Gate Path Tomb - Upper-Bottom', 10020), #nothing
        # LocationData('Forest of Silence - switch 3', 'Forest of Silence - Backfacing Tomb Lower-Rear',  10022), #nothing
        # LocationData('Forest of Silence - switch 3', 'Forest of Silence - Werewolf Tomb - Top-Left', 10026), #nothing
        # LocationData('Forest of Silence - switch 3', 'Forest of Silence - Werewolf Tomb - Bottom-Left', 10027), #nothing
        # LocationData('Forest of Silence - switch 3', 'Forest of Silence - Werewolf Path - Near Island Switch Platforms', 10029), #sub
        LocationData('Castle Wall - right tower', 'Castle Wall right tower - Above Bottom Door', 0xC64015),
        LocationData('Castle Wall - left tower', 'Castle Wall left tower - Above Bottom Door', 0xC64016),
        LocationData('Castle Wall - left tower', 'Castle Wall left tower - Flipping Green Bridge Ledge', 0xC64017),
        LocationData('Castle Wall main - exit to Villa', 'Castle Wall main - Bottom Middle Torch', 0xC64018),
        LocationData('Castle Wall main - descent', 'Castle Wall main - Right Rampart', 0xC64019),
        LocationData('Castle Wall main - descent', 'Castle Wall main - Left Rampart', 0xC6401A),
        LocationData('Castle Wall main - Bone Dragon switch', 'Castle Wall main - White Dragon Switch Door', 0xC6401B),
        LocationData('Castle Wall main - Dracula switch', 'Castle Wall main - Dracula Switch Door', 0xC6401C),
        LocationData('Castle Wall main - exit to Villa', 'Youre Winner', EventId)

        # To-do: Add the rest of the locations
    ]

    return tuple(location_table)
