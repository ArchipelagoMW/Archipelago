from __future__ import annotations

from typing import NamedTuple, Optional


class RoomGroupRequirementData(NamedTuple):
    group_id: Optional[int]
    subgroup_0: Optional[int]
    subgroup_1: Optional[int]
    subgroup_2: Optional[int]
    subgroup_3: Optional[int]
    rooms: tuple[int, ...]

SHUTTER_ROOM_IDS = frozenset((184,
 11,
 27,
 75,
 4,
 36,
 182,
 40,
 14,
 46,
 62,
 110,
 49,
 135,
 68,
 69,
 83,
 117,
 133,
 61,
 93,
 107,
 109,
 123,
 125,
 141,
 150,
 165,
 113,
 168,
 216,
 176,
 192,
 224,
 178,
 210,
 239,
 268,
 291))
WATER_ROOM_IDS = frozenset((22, 40, 52, 54, 56, 70, 102))
DONT_RANDOMIZE_ROOM_IDS = frozenset((0, 1, 3, 13, 20, 32, 48, 127))
NO_SPECIAL_ENEMIES_STANDARD_ROOM_IDS = frozenset((1, 2, 17, 33, 34, 50, 65, 66, 80, 81, 82, 85, 96, 97, 98, 112, 113, 114, 128, 129, 130))
BOSS_ROOM_IDS = frozenset((200, 51, 108, 7, 77, 90, 6, 41, 172, 222, 144, 164, 32, 13, 0))

ROOM_GROUP_REQUIREMENTS = (
    RoomGroupRequirementData(group_id=1, subgroup_0=70, subgroup_1=73, subgroup_2=28, subgroup_3=82, rooms=(228, 240)),
    RoomGroupRequirementData(group_id=5, subgroup_0=75, subgroup_1=77, subgroup_2=74, subgroup_3=90, rooms=(243, 265, 270, 271, 272, 273, 282, 284, 290)),
    RoomGroupRequirementData(group_id=None, subgroup_0=75, subgroup_1=None, subgroup_2=None, subgroup_3=None, rooms=(255, 274, 287)),
    RoomGroupRequirementData(group_id=None, subgroup_0=None, subgroup_1=77, subgroup_2=None, subgroup_3=21, rooms=(289,)),
    RoomGroupRequirementData(group_id=7, subgroup_0=75, subgroup_1=77, subgroup_2=57, subgroup_3=54, rooms=(8, 44, 276, 277)),
    RoomGroupRequirementData(group_id=13, subgroup_0=81, subgroup_1=None, subgroup_2=None, subgroup_3=None, rooms=(85, 258, 260)),
    RoomGroupRequirementData(group_id=14, subgroup_0=71, subgroup_1=73, subgroup_2=76, subgroup_3=80, rooms=(18, 261, 266)),
    RoomGroupRequirementData(group_id=None, subgroup_0=None, subgroup_1=None, subgroup_2=None, subgroup_3=80, rooms=(264,)),
    RoomGroupRequirementData(group_id=15, subgroup_0=79, subgroup_1=77, subgroup_2=74, subgroup_3=80, rooms=(244, 245, 257, 259, 262, 280, 281)),
    RoomGroupRequirementData(group_id=18, subgroup_0=85, subgroup_1=61, subgroup_2=66, subgroup_3=67, rooms=(32, 48)),
    RoomGroupRequirementData(group_id=24, subgroup_0=85, subgroup_1=26, subgroup_2=66, subgroup_3=67, rooms=(13,)),
    RoomGroupRequirementData(group_id=34, subgroup_0=33, subgroup_1=65, subgroup_2=69, subgroup_3=51, rooms=(0,)),
    RoomGroupRequirementData(group_id=40, subgroup_0=14, subgroup_1=None, subgroup_2=74, subgroup_3=80, rooms=(225, 256, 293, 292, 294)),
    RoomGroupRequirementData(group_id=None, subgroup_0=14, subgroup_1=30, subgroup_2=None, subgroup_3=None, rooms=(291,)),
    RoomGroupRequirementData(group_id=23, subgroup_0=64, subgroup_1=None, subgroup_2=None, subgroup_3=63, rooms=()),
    RoomGroupRequirementData(group_id=9, subgroup_0=None, subgroup_1=None, subgroup_2=None, subgroup_3=29, rooms=(227,)),
    RoomGroupRequirementData(group_id=11, subgroup_0=None, subgroup_1=None, subgroup_2=None, subgroup_3=61, rooms=()),
    RoomGroupRequirementData(group_id=22, subgroup_0=None, subgroup_1=None, subgroup_2=None, subgroup_3=49, rooms=()),
    RoomGroupRequirementData(group_id=22, subgroup_0=None, subgroup_1=None, subgroup_2=60, subgroup_3=None, rooms=()),
    RoomGroupRequirementData(group_id=21, subgroup_0=None, subgroup_1=None, subgroup_2=58, subgroup_3=62, rooms=()),
    RoomGroupRequirementData(group_id=28, subgroup_0=None, subgroup_1=None, subgroup_2=38, subgroup_3=82, rooms=(14, 126, 142, 158, 190)),
    RoomGroupRequirementData(group_id=12, subgroup_0=None, subgroup_1=None, subgroup_2=48, subgroup_3=None, rooms=()),
    RoomGroupRequirementData(group_id=26, subgroup_0=None, subgroup_1=None, subgroup_2=56, subgroup_3=None, rooms=()),
    RoomGroupRequirementData(group_id=20, subgroup_0=None, subgroup_1=None, subgroup_2=57, subgroup_3=None, rooms=()),
    RoomGroupRequirementData(group_id=32, subgroup_0=None, subgroup_1=44, subgroup_2=59, subgroup_3=None, rooms=()),
    RoomGroupRequirementData(group_id=3, subgroup_0=93, subgroup_1=None, subgroup_2=None, subgroup_3=None, rooms=(81,)),
    RoomGroupRequirementData(group_id=42, subgroup_0=21, subgroup_1=None, subgroup_2=None, subgroup_3=None, rooms=(286,)),
    RoomGroupRequirementData(group_id=10, subgroup_0=47, subgroup_1=None, subgroup_2=46, subgroup_3=None, rooms=(92, 117, 185, 217)),
    RoomGroupRequirementData(group_id=None, subgroup_0=None, subgroup_1=None, subgroup_2=34, subgroup_3=None, rooms=(54, 70, 102, 118)),
    RoomGroupRequirementData(group_id=None, subgroup_0=None, subgroup_1=32, subgroup_2=None, subgroup_3=None, rooms=(62, 159)),
    RoomGroupRequirementData(group_id=None, subgroup_0=31, subgroup_1=None, subgroup_2=None, subgroup_3=None, rooms=(127,)),
    RoomGroupRequirementData(group_id=None, subgroup_0=None, subgroup_1=None, subgroup_2=35, subgroup_3=None, rooms=(57, 73, 86, 87, 104, 141)),
    RoomGroupRequirementData(group_id=37, subgroup_0=31, subgroup_1=None, subgroup_2=39, subgroup_3=82, rooms=(36, 180, 181, 198, 199, 214)),
    RoomGroupRequirementData(group_id=None, subgroup_0=None, subgroup_1=None, subgroup_2=None, subgroup_3=82, rooms=(23, 42, 68, 76, 86, 88, 89, 103, 104, 126, 139, 235, 251)),
    RoomGroupRequirementData(group_id=None, subgroup_0=None, subgroup_1=None, subgroup_2=None, subgroup_3=83, rooms=(23, 42, 76, 89, 103, 104, 126, 139, 235, 251)),
    RoomGroupRequirementData(group_id=None, subgroup_0=None, subgroup_1=None, subgroup_2=None, subgroup_3=82, rooms=(11, 19, 27, 30, 42, 43, 49, 61, 62, 91, 107, 119, 135, 139, 145, 146, 155, 157, 161, 171, 182, 191, 193, 196, 239)),
    RoomGroupRequirementData(group_id=None, subgroup_0=None, subgroup_1=None, subgroup_2=None, subgroup_3=83, rooms=(11, 19, 27, 30, 42, 43, 49, 53, 62, 91, 107, 119, 135, 139, 145, 146, 155, 157, 161, 171, 182, 191, 193, 196, 239)),
    RoomGroupRequirementData(group_id=None, subgroup_0=None, subgroup_1=None, subgroup_2=None, subgroup_3=82, rooms=(19, 35, 150, 165, 195, 197, 213)),
    RoomGroupRequirementData(group_id=None, subgroup_0=None, subgroup_1=None, subgroup_2=None, subgroup_3=83, rooms=(19, 35, 150, 165, 197, 213)),
    RoomGroupRequirementData(group_id=None, subgroup_0=None, subgroup_1=None, subgroup_2=None, subgroup_3=82, rooms=(26, 38, 43, 64, 74, 87, 107, 123)),
    RoomGroupRequirementData(group_id=None, subgroup_0=None, subgroup_1=None, subgroup_2=None, subgroup_3=83, rooms=(38, 43, 64, 74, 87, 107, 123, 206)),
    RoomGroupRequirementData(group_id=None, subgroup_0=None, subgroup_1=None, subgroup_2=None, subgroup_3=82, rooms=(2, 88, 100, 140, 267)),
    RoomGroupRequirementData(group_id=None, subgroup_0=None, subgroup_1=None, subgroup_2=None, subgroup_3=82, rooms=(26, 61, 68, 86, 94, 124, 149, 195)),
    RoomGroupRequirementData(group_id=None, subgroup_0=None, subgroup_1=None, subgroup_2=None, subgroup_3=83, rooms=(4, 63, 206)),
    RoomGroupRequirementData(group_id=None, subgroup_0=None, subgroup_1=None, subgroup_2=None, subgroup_3=83, rooms=(53, 55, 118)),
    RoomGroupRequirementData(group_id=None, subgroup_0=None, subgroup_1=None, subgroup_2=34, subgroup_3=None, rooms=(40,)),
    RoomGroupRequirementData(group_id=None, subgroup_0=None, subgroup_1=None, subgroup_2=37, subgroup_3=None, rooms=(151,)),
)
