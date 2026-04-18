from __future__ import annotations

import hashlib
from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path
import random as randomlib
from typing import Any

import json

from .data.rooms import rooms as base_rooms
from .data.rooms import entrances_pairs, shuffling_data

CRESTS_ACCESS = {"LibraCrest", "GeminiCrest", "MobiusCrest"}

MAP_SHUFFLE_DUNGEON_MODES = {"DungeonsInternal", "DungeonsMixed", "Everything", 1, 2, 3}
LOCATION_ORDER = [
    "None",
    "ForestaSouthBattlefield",
    "ForestaWestBattlefield",
    "ForestaEastBattlefield",
    "AquariaBattlefield01",
    "AquariaBattlefield02",
    "AquariaBattlefield03",
    "WintryBattlefield01",
    "WintryBattlefield02",
    "PyramidBattlefield01",
    "LibraBattlefield01",
    "LibraBattlefield02",
    "FireburgBattlefield01",
    "FireburgBattlefield02",
    "FireburgBattlefield03",
    "MineBattlefield01",
    "MineBattlefield02",
    "MineBattlefield03",
    "VolcanoBattlefield01",
    "WindiaBattlefield01",
    "WindiaBattlefield02",
    "HillOfDestiny",
    "LevelForest",
    "Foresta",
    "SandTemple",
    "BoneDungeon",
    "FocusTowerForesta",
    "FocusTowerAquaria",
    "LibraTemple",
    "Aquaria",
    "WintryCave",
    "LifeTemple",
    "FallsBasin",
    "IcePyramid",
    "SpencersPlace",
    "WintryTemple",
    "FocusTowerFrozen",
    "FocusTowerFireburg",
    "Fireburg",
    "Mine",
    "SealedTemple",
    "Volcano",
    "LavaDome",
    "FocusTowerWindia",
    "RopeBridge",
    "AliveForest",
    "GiantTree",
    "KaidgeTemple",
    "Windia",
    "WindholeTemple",
    "MountGale",
    "PazuzusTower",
    "ShipDock",
    "DoomCastle",
    "LightTemple",
    "MacsShip",
    "MacsShipDoom",
]
BATTLEFIELD_LOCATIONS = LOCATION_ORDER[1:21]
NON_BATTLEFIELD_LOCATIONS = LOCATION_ORDER[22:]
FIXED_OVERWORLD_LOCATIONS = {
    "DoomCastle",
    "FocusTowerForesta",
    "FocusTowerAquaria",
    "FocusTowerFrozen",
    "FocusTowerFireburg",
    "FocusTowerWindia",
    "GiantTree",
    "HillOfDestiny",
    "LifeTemple",
    "LightTemple",
    "MacsShip",
    "MacsShipDoom",
    "None",
    "ShipDock",
    "SpencersPlace",
}
EXCLUDE_FROM_START = set(LOCATION_ORDER[9:21])
MAP_SUBREGIONS = {
    "ForestaSouthBattlefield": "Foresta",
    "ForestaWestBattlefield": "Foresta",
    "ForestaEastBattlefield": "Foresta",
    "AquariaBattlefield01": "Aquaria",
    "AquariaBattlefield02": "Aquaria",
    "AquariaBattlefield03": "Aquaria",
    "WintryBattlefield01": "Aquaria",
    "WintryBattlefield02": "Aquaria",
    "PyramidBattlefield01": "Aquaria",
    "LibraBattlefield01": "AquariaFrozenField",
    "LibraBattlefield02": "AquariaFrozenField",
    "FireburgBattlefield01": "Fireburg",
    "FireburgBattlefield02": "Fireburg",
    "FireburgBattlefield03": "Fireburg",
    "MineBattlefield01": "Fireburg",
    "MineBattlefield02": "Fireburg",
    "MineBattlefield03": "Fireburg",
    "VolcanoBattlefield01": "VolcanoBattlefield",
    "WindiaBattlefield01": "Windia",
    "WindiaBattlefield02": "Windia",
    "HillOfDestiny": "Foresta",
    "LevelForest": "Foresta",
    "Foresta": "Foresta",
    "SandTemple": "Foresta",
    "BoneDungeon": "Foresta",
    "FocusTowerForesta": "Foresta",
    "FocusTowerAquaria": "Aquaria",
    "LibraTemple": "Aquaria",
    "Aquaria": "Aquaria",
    "WintryCave": "Aquaria",
    "LifeTemple": "LifeTemple",
    "FallsBasin": "Aquaria",
    "IcePyramid": "Aquaria",
    "WintryTemple": "AquariaFrozenField",
    "FocusTowerFrozen": "AquariaFrozenField",
    "FocusTowerFireburg": "Fireburg",
    "Fireburg": "Fireburg",
    "Mine": "Fireburg",
    "SealedTemple": "Fireburg",
    "Volcano": "Fireburg",
    "LavaDome": "Fireburg",
    "FocusTowerWindia": "Windia",
    "RopeBridge": "Windia",
    "AliveForest": "Windia",
    "GiantTree": "Windia",
    "KaidgeTemple": "Windia",
    "Windia": "Windia",
    "WindholeTemple": "Windia",
    "MountGale": "Windia",
    "PazuzusTower": "Windia",
    "SpencersPlace": "SpencerCave",
    "ShipDock": "ShipDock",
    "DoomCastle": "DoomCastle",
    "LightTemple": "LightTemple",
    "MacsShip": "MacShip",
    "MacsShipDoom": "MacShip",
}
BATTLEFIELD_REWARDS = {
    "ForestaSouthBattlefield": "Xp54",
    "ForestaWestBattlefield": "Charm",
    "ForestaEastBattlefield": "Gp150",
    "AquariaBattlefield01": "Xp99",
    "AquariaBattlefield02": "Gp300",
    "AquariaBattlefield03": "MagicRing",
    "WintryBattlefield01": "Xp99",
    "WintryBattlefield02": "Gp600",
    "PyramidBattlefield01": "Xp540",
    "LibraBattlefield01": "ExitBook",
    "LibraBattlefield02": "Xp744",
    "FireburgBattlefield01": "Gp900",
    "FireburgBattlefield02": "GeminiCrest",
    "FireburgBattlefield03": "Xp816",
    "MineBattlefield01": "Gp1200",
    "MineBattlefield02": "ThunderSeal",
    "MineBattlefield03": "Xp1200",
    "VolcanoBattlefield01": "Xp1068",
    "WindiaBattlefield01": "Xp2808",
    "WindiaBattlefield02": "Xp2700",
}
GP_REWARD_ACCESS = {
    "Gp150": "Gp150",
    "Gp300": "Gp300",
    "Gp600": "Gp600",
    "Gp900": "Gp900",
    "Gp1200": "Gp1200",
}
STARTER_WEAPONS = {"Sword", "Axe", "Claw", "Bomb"}
ACCESS_REQ_VALUE_NAMES = {
    19: "Claw",
}
BOSSES = {
    "FlamerusRex",
    "Squidite",
    "SnowCrab",
    "IceGolem",
    "Medusa",
    "Jinn",
    "DualheadHydra",
    "Gidrah",
    "Dullahan",
    "Pazuzu",
}
FAVORED_COMPANIONS = {"Tristam", "Phoebe", "Reuben"}


@dataclass
class LogicLink:
    room: int
    current: dict[str, Any]
    origin: dict[str, Any]
    exit: bool = True
    priority_exit: bool = False
    entrance_only: bool = False
    force_dead_end: bool = False
    force_link_destination: bool = False
    force_link_origin: bool = False
    forced_destination: int = 0
    forbidden_destinations: list[int] = field(default_factory=list)


@dataclass
class ClusterRoom:
    rooms: list[int]
    links: list[LogicLink] = field(default_factory=list)
    size: int = 0
    location: str | None = None
    forbidden_destinations: list[int] = field(default_factory=list)

    def merge(self, room: "ClusterRoom") -> None:
        self.rooms += room.rooms
        self.links += room.links
        self.size += 1
        self.forbidden_destinations += room.forbidden_destinations
        if self.location is None:
            self.location = room.location

    def update_links(self, origin_link: LogicLink, random: randomlib.Random) -> None:
        if origin_link.force_link_origin:
            valid_origins = [x for x in self.links if not x.force_link_origin and not x.force_link_destination]
            if not valid_origins:
                raise RuntimeError("Floor Shuffle: One way Orientation Error")
            new_origin = random.choice(valid_origins)
            new_origin.force_link_origin = True
            new_origin.forced_destination = origin_link.forced_destination

        if origin_link.force_dead_end:
            valid_dead_ends = [x for x in self.links if not x.force_link_origin and not x.force_link_destination]
            for link in valid_dead_ends:
                link.force_dead_end = True

        for link in self.links:
            link.forbidden_destinations.extend(origin_link.forbidden_destinations)


@dataclass
class ClusterLocation:
    rooms: list[ClusterRoom]
    location: str | None = None
    initial_rooms: list[int] = field(default_factory=list)
    backup_rooms: list[ClusterRoom] = field(default_factory=list)

    @property
    def links(self) -> list[LogicLink]:
        return [link for room in self.rooms for link in room.links]

    @property
    def odd_links(self) -> bool:
        return any((len(room.links) % 2) == 1 for room in self.rooms)

    @property
    def dead_end_required(self) -> bool:
        return any(any(not link.exit for link in room.links) for room in self.rooms)

    def forbidden_destinations_for(self, link: LogicLink) -> list[int]:
        origin_room = next((room for room in self.rooms if link in room.links), None)
        if origin_room is None:
            raise RuntimeError("Couldn't find appropriate room.")
        return origin_room.forbidden_destinations + link.forbidden_destinations

    def merge(self, target_room: ClusterRoom, origin_link: LogicLink, target_link: LogicLink) -> None:
        origin_room = next((room for room in self.rooms if origin_link in room.links), None)
        if origin_room is None:
            raise RuntimeError("Couldn't find appropriate room.")

        copied_target = ClusterRoom(
            target_room.rooms.copy(),
            target_room.links.copy(),
            target_room.size,
            target_room.location,
            target_room.forbidden_destinations.copy(),
        )

        if not origin_link.exit:
            copied_target.forbidden_destinations.extend(self.forbidden_destinations_for(origin_link))
            self.rooms.append(copied_target)
            copied_target.links.remove(target_link)
            origin_room.links.remove(origin_link)
        else:
            origin_room.merge(copied_target)
            origin_room.links.remove(target_link)
            origin_room.links.remove(origin_link)

    def backup_state(self) -> None:
        self.backup_rooms = [
            ClusterRoom(
                room.rooms.copy(),
                room.links.copy(),
                room.size,
                room.location,
                room.forbidden_destinations.copy(),
            )
            for room in self.rooms
        ]

    def restore_backup(self) -> None:
        self.rooms = [
            ClusterRoom(
                room.rooms.copy(),
                room.links.copy(),
                room.size,
                room.location,
                room.forbidden_destinations.copy(),
            )
            for room in self.backup_rooms
        ]


def _seed_to_uint32(seed: int | str) -> int:
    seed_str = str(seed).strip()
    seed_hex = seed_str.rjust(8, "0")[:8]
    # Match latest C# GenerateRooms() behavior: parse 8-char hex seed into 4 bytes before hashing.
    seed_bytes = bytes.fromhex(seed_hex)
    digest = hashlib.sha256(seed_bytes).digest()
    words = [int.from_bytes(digest[i : i + 4], "little") for i in range(0, 32, 4)]
    return sum(words) & 0xFFFFFFFF


def _normalize_map_shuffle_mode(map_shuffle: str | int) -> int | str:
    if isinstance(map_shuffle, int):
        return map_shuffle

    normalized = map_shuffle.strip().lower()
    aliases = {
        "none": 0,
        "dungeonsinternal": 1,
        "dungeonsmixed": 2,
        "everything": 3,
    }
    return aliases.get(normalized, map_shuffle)


def _read_yaml(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _battlefield_reward_type(reward: str) -> str:
    if reward.startswith("Xp"):
        return "Experience"
    if reward.startswith("Gp"):
        return "Gold"
    return "Item"


def _take_random(seq: list[Any], random: randomlib.Random) -> Any:
    value = random.choice(seq)
    seq.remove(value)
    return value


def _shuffle_battlefield_rewards(rooms: list[dict[str, Any]], battlefield_shuffle: bool, random: randomlib.Random) -> dict[str, str]:
    rewards_by_location = dict(BATTLEFIELD_REWARDS)
    if battlefield_shuffle:
        rewards = [rewards_by_location[location] for location in BATTLEFIELD_LOCATIONS]
        for location in BATTLEFIELD_LOCATIONS:
            rewards_by_location[location] = _take_random(rewards, random)

    battlefield_types = {"BattlefieldGp", "BattlefieldXp", "BattlefieldItem"}
    type_by_reward = {"Gold": "BattlefieldGp", "Experience": "BattlefieldXp", "Item": "BattlefieldItem"}
    for room in rooms:
        for obj in room.get("game_objects", []):
            if obj.get("type") not in battlefield_types:
                continue
            location = LOCATION_ORDER[obj["object_id"]]
            reward = rewards_by_location[location]
            reward_type = _battlefield_reward_type(reward)
            obj["type"] = type_by_reward[reward_type]
            obj["on_trigger"] = []
            if reward_type == "Gold":
                obj["on_trigger"].append(GP_REWARD_ACCESS[reward])

    return rewards_by_location


def _companion_object(trigger: str, access: list[str] | None = None) -> dict[str, Any]:
    return {
        "name": f"{trigger} Companion" if trigger != "TreeWitherPerson" else "Tree Wither Person",
        "object_id": 0,
        "type": "Trigger",
        "on_trigger": [trigger],
        "access": list(access or []),
    }


def _companions_shuffle(
    rooms: list[dict[str, Any]],
    companion_shuffle: int | bool,
    kaeli_mom: bool,
    random: randomlib.Random,
) -> None:
    shuffle_type = int(companion_shuffle)
    if shuffle_type == 0:
        return

    companions = [
        _companion_object("Tristam"),
        _companion_object("Phoebe"),
        _companion_object("Reuben"),
        _companion_object("Kaeli", [] if kaeli_mom else ["TreeWither"]),
    ]
    tree_wither_person = _companion_object("TreeWitherPerson", ["TreeWither"])
    npc_triggers = {trigger for companion in companions for trigger in companion["on_trigger"]}
    if not kaeli_mom:
        npc_triggers.add("TreeWitherPerson")

    for room in rooms:
        room["game_objects"] = [
            obj
            for obj in room.get("game_objects", [])
            if not set(obj.get("on_trigger", [])).intersection(npc_triggers)
        ]

    valid_rooms = [
        ("Foresta", 17),
        ("Foresta", 24),
        ("Aquaria", 39),
        ("Fireburg", 77),
    ]
    if shuffle_type == 2:
        valid_rooms.extend(
            [
                ("Aquaria", 51),
                ("Aquaria", 41),
                ("Fireburg", 92),
                ("Fireburg", 75),
            ]
        )
        windia_rooms = [("Windia", 123), ("Windia", 153), ("Windia", 154), ("Windia", 185)]
        valid_rooms.append(_take_random(windia_rooms, random))
        valid_rooms.append(_take_random(windia_rooms, random))

    guaranteed_foresta = random.choice([room for room in valid_rooms if room[0] == "Foresta"])
    valid_rooms.remove(guaranteed_foresta)
    _room_by_id(rooms, guaranteed_foresta[1])["game_objects"].append(_take_random(companions, random))

    for companion in companions:
        region, room_id = _take_random(valid_rooms, random)
        room = _room_by_id(rooms, room_id)
        room["game_objects"].append(companion)
        if companion["on_trigger"] == ["Kaeli"] and not kaeli_mom:
            room["game_objects"].append(deepcopy(tree_wither_person))


def _room_by_id(rooms: list[dict[str, Any]], room_id: int) -> dict[str, Any]:
    for room in rooms:
        if room["id"] == room_id:
            return room
    raise KeyError(f"Room not found: {room_id}")


def _contains_identity(seq: list[Any], target: Any) -> bool:
    return any(item is target for item in seq)


def _remove_identity(seq: list[Any], target: Any) -> None:
    for index, item in enumerate(seq):
        if item is target:
            del seq[index]
            return
    raise ValueError("Target was not found by identity")


def _connect_link(rooms: list[dict[str, Any]], pending_links: list[tuple[int, dict[str, Any]]], link1: LogicLink, link2: LogicLink) -> None:
    room1_links = _room_by_id(rooms, link1.room)["links"]
    room2_links = _room_by_id(rooms, link2.room)["links"]
    if link1.current not in room1_links or link2.current not in room2_links:
        return
    room1_links.remove(link1.current)
    room2_links.remove(link2.current)

    pending_links.append(
        (
            link1.room,
            {
                "target_room": link2.room,
                "entrance": link1.current["entrance"],
                "teleporter": deepcopy(link2.origin["teleporter"]),
                "access": deepcopy(link1.current.get("access", [])),
            },
        )
    )
    pending_links.append(
        (
            link2.room,
            {
                "target_room": link1.room,
                "entrance": link2.current["entrance"],
                "teleporter": deepcopy(link1.origin["teleporter"]),
                "access": deepcopy(link2.current.get("access", [])),
            },
        )
    )


def _connect_overworld_link(
    rooms: list[dict[str, Any]],
    pending_links: list[tuple[int, dict[str, Any]]],
    location: str | None,
    link1: LogicLink,
    link2: LogicLink,
) -> None:
    room1_links = _room_by_id(rooms, link1.room)["links"]
    room2_links = _room_by_id(rooms, link2.room)["links"]
    if link1.current not in room1_links or link2.current not in room2_links:
        return
    room1_links.remove(link1.current)
    room2_links.remove(link2.current)

    resolved_location = location
    if resolved_location in (None, "None"):
        resolved_location = link1.current.get("location") or link1.current.get("location_slot")

    link1_payload = {
        "target_room": link2.room,
        "entrance": link1.current["entrance"],
        "teleporter": deepcopy(link2.origin["teleporter"]),
        "access": deepcopy(link1.current.get("access", [])),
    }
    if resolved_location not in (None, "None"):
        link1_payload["location"] = resolved_location
        link1_payload["location_slot"] = resolved_location

    pending_links.append((link1.room, link1_payload))
    pending_links.append(
        (
            link2.room,
            {
                "target_room": link1.room,
                "entrance": link2.current["entrance"],
                "teleporter": deepcopy(link1.origin["teleporter"]),
                "access": deepcopy(link2.current.get("access", [])),
            },
        )
    )


def _select_overworld_link(
    random: randomlib.Random,
    links_from_overworld: list[LogicLink],
    *,
    room_location: str | None,
    preferred_entrance: int | None,
    seed_links_locations: dict[int, str | None],
    fixed_overworld_links: list[LogicLink],
    switch_overworld_links: list[LogicLink],
    crystal_source_location: str | None,
) -> LogicLink:
    available = links_from_overworld.copy()
    if not available:
        raise ValueError("No overworld links available")

    available_ids = {id(l) for l in available}
    fixed_pool = [l for l in fixed_overworld_links if id(l) in available_ids]
    switch_pool = [l for l in switch_overworld_links if id(l) in available_ids]

    def by_location(pool: list[LogicLink], location: str | None) -> list[LogicLink]:
        if location in (None, "None"):
            return []
        return [l for l in pool if seed_links_locations.get(l.current.get("entrance")) == location]

    def by_preferred(pool: list[LogicLink]) -> list[LogicLink]:
        if preferred_entrance is None:
            return []
        return [l for l in pool if l.origin.get("entrance") == preferred_entrance]

    candidate_groups: list[list[LogicLink]] = []
    if crystal_source_location not in (None, "None"):
        candidate_groups.extend(
            [
                by_location(switch_pool, crystal_source_location),
                by_location(fixed_pool, crystal_source_location),
            ]
        )

    candidate_groups.extend(
        [
            by_preferred(switch_pool),
            by_preferred(fixed_pool),
            by_location(switch_pool, room_location),
            by_location(fixed_pool, room_location),
            switch_pool,
            fixed_pool,
            available,
        ]
    )

    for group in candidate_groups:
        if group:
            return random.choice(group)
    return random.choice(available)


def _shuffle_error(stage: str, **context: Any) -> RuntimeError:
    context_str = ", ".join(f"{k}={v}" for k, v in sorted(context.items()))
    return RuntimeError(f"Floor Shuffle: {stage} ({context_str})")


def _room_link_by_location(rooms: list[dict[str, Any]], location: str) -> dict[str, Any]:
    for room in rooms:
        if room.get("type") != "Subregion":
            continue
        for link in room.get("links", []):
            if link.get("location") == location:
                return link
    raise KeyError(f"Location not found: {location}")


def _find_trigger_location(rooms: list[dict[str, Any]], trigger: str) -> str | None:
    initial_room = next(
        (room for room in rooms if any(trigger in obj.get("on_trigger", []) for obj in room.get("game_objects", []))),
        None,
    )
    if initial_room is None:
        return None

    room_to_process = [initial_room["id"]]
    room_processed = {0}
    region_rooms = {room["id"] for room in rooms if room.get("type") == "Subregion"}

    while room_to_process:
        current_room_id = room_to_process.pop(0)
        current_room = _room_by_id(rooms, current_room_id)
        for link in current_room.get("links", []):
            if set(link.get("access", [])).intersection(CRESTS_ACCESS):
                continue
            if link["target_room"] in region_rooms:
                target_room = _room_by_id(rooms, link["target_room"])
                reverse = next((candidate for candidate in target_room.get("links", []) if candidate["target_room"] == current_room_id), None)
                return None if reverse is None else reverse.get("location")
            if link["target_room"] not in room_processed:
                room_to_process.append(link["target_room"])
        room_processed.add(current_room_id)
    return None


def _process_room_for_requirements(
    rooms: list[dict[str, Any]],
    room_id: int,
    access_list: list[str],
    visited_rooms: list[int],
) -> None:
    current_room = _room_by_id(rooms, room_id)
    visited_rooms.append(room_id)
    for link in current_room.get("links", []):
        if link["target_room"] in visited_rooms or set(link.get("access", [])).intersection(CRESTS_ACCESS):
            continue
        access_list.extend(link.get("access", []))
        _process_room_for_requirements(rooms, link["target_room"], access_list, visited_rooms)


def _crawl_for_requirements(rooms: list[dict[str, Any]], location: str) -> list[str]:
    initial_room = _room_link_by_location(rooms, location)["target_room"]
    access_list = []
    access_list.extend(
        access
        for link in _room_by_id(rooms, initial_room).get("links", [])
        for access in link.get("access", [])
    )
    visited_rooms = [room["id"] for room in rooms if room.get("type") == "Subregion"]
    _process_room_for_requirements(rooms, initial_room, access_list, visited_rooms)
    return access_list


def _process_room_for_companions(
    rooms: list[dict[str, Any]],
    req_count: int,
    room_id: int,
    companion_list: list[int],
    visited_rooms: list[int],
    include_kaeli: bool,
) -> None:
    current_room = _room_by_id(rooms, room_id)
    valid_companions = set(FAVORED_COMPANIONS)
    if include_kaeli:
        valid_companions.add("Kaeli")

    visited_rooms.append(room_id)
    for companion in current_room.get("game_objects", []):
        if companion.get("type") == "Trigger" and set(companion.get("on_trigger", [])).intersection(valid_companions):
            companion_list.append(req_count + len(companion.get("access", [])))

    for link in current_room.get("links", []):
        if link["target_room"] in visited_rooms or set(link.get("access", [])).intersection(CRESTS_ACCESS):
            continue
        _process_room_for_companions(
            rooms,
            req_count + len(link.get("access", [])),
            link["target_room"],
            companion_list,
            visited_rooms,
            include_kaeli,
        )


def _crawl_for_companion_rating(rooms: list[dict[str, Any]], location: str, include_kaeli: bool) -> tuple[str, int]:
    initial_room = _room_link_by_location(rooms, location)["target_room"]
    companion_list: list[int] = []
    visited_rooms = [room["id"] for room in rooms if room.get("type") == "Subregion"]
    _process_room_for_companions(rooms, 0, initial_room, companion_list, visited_rooms, include_kaeli)

    rating = 0
    for companion in companion_list:
        if companion == 0:
            rating += 10
        elif companion == 1:
            rating += 3
        else:
            rating += 1
    return location, rating


def _process_room_for_chests2(
    rooms: list[dict[str, Any]],
    room_id: int,
    accessed_chests: list[int],
    visited_rooms: list[int],
    access_acquired: list[str],
) -> bool:
    current_room = _room_by_id(rooms, room_id)
    new_access = True
    access_count = len(access_acquired)

    while new_access:
        new_access = False
        for link in current_room.get("links", []):
            if link["target_room"] in visited_rooms or set(link.get("access", [])).intersection(CRESTS_ACCESS):
                continue
            if not set(link.get("access", [])).difference(access_acquired):
                if _process_room_for_chests2(
                    rooms,
                    link["target_room"],
                    accessed_chests,
                    visited_rooms + [room_id],
                    access_acquired,
                ):
                    new_access = True

        for trigger in current_room.get("game_objects", []):
            if trigger.get("type") != "Trigger":
                continue
            trigger_access = trigger.get("access", [])
            trigger_reward = trigger.get("on_trigger", [])
            if set(trigger_reward).intersection(BOSSES):
                continue
            if not set(trigger_access).difference(access_acquired) and set(trigger_reward).difference(access_acquired):
                access_acquired.extend(trigger_reward)
                new_access = True

        for chest in current_room.get("game_objects", []):
            if chest.get("type") != "Chest" or chest.get("object_id") in accessed_chests:
                continue
            if not set(chest.get("access", [])).difference(access_acquired):
                accessed_chests.append(chest["object_id"])

    return access_count < len(access_acquired)


def _crawl_for_chest_rating2(rooms: list[dict[str, Any]], location: str) -> tuple[str, int]:
    initial_room = _room_link_by_location(rooms, location)["target_room"]
    region_rooms = [room["id"] for room in rooms if room.get("type") == "Subregion"]
    chest_count = 0
    for weapon in STARTER_WEAPONS:
        chests_list: list[int] = []
        _process_room_for_chests2(rooms, initial_room, chests_list, region_rooms, [weapon])
        chest_count += len(chests_list)
    return location, chest_count


def _shuffle_overworld(
    rooms: list[dict[str, Any]],
    map_shuffle: str | int,
    overworld_shuffle: bool,
    kaeli_mom: bool,
    battlefield_rewards: dict[str, str],
    random: randomlib.Random,
) -> None:
    if not overworld_shuffle:
        return

    region_rooms = [room for room in rooms if room.get("type") == "Subregion"]
    movable_locations: list[dict[str, Any]] = []
    for room in region_rooms:
        movable_locations.extend(
            {
                "region": room["region"],
                "origins": obj.get("location"),
                "destination": obj.get("location"),
                "room": 0,
                "type": "Battlefield",
                "object": obj,
            }
            for obj in room.get("game_objects", [])
            if obj.get("location") not in (None, "None")
        )
        movable_locations.extend(
            {
                "region": room["region"],
                "origins": link.get("location"),
                "destination": link.get("location"),
                "room": link["target_room"],
                "type": "Dungeon",
                "link": link,
            }
            for link in room.get("links", [])
            if link.get("entrance", -1) >= 0 and link.get("location") not in (None, "None")
        )

    region_location_pairs = {entry["origins"]: entry["region"] for entry in movable_locations}
    reward_types = [_battlefield_reward_type(battlefield_rewards[location]) for location in BATTLEFIELD_LOCATIONS]
    safe_gold_battlefield = LOCATION_ORDER[reward_types.index("Gold") + 1]

    movable_origins = {entry["origins"] for entry in movable_locations}
    shuffle_locations = list(LOCATION_ORDER)
    destination_locations = list(LOCATION_ORDER)
    shuffle_locations = [location for location in shuffle_locations if location not in FIXED_OVERWORLD_LOCATIONS and location in movable_origins]
    destination_locations = [location for location in destination_locations if location not in FIXED_OVERWORLD_LOCATIONS and location in movable_origins]
    placed_locations = set(FIXED_OVERWORLD_LOCATIONS)
    taken_locations = set(FIXED_OVERWORLD_LOCATIONS)

    companion_candidates = [location for location in NON_BATTLEFIELD_LOCATIONS if location in shuffle_locations]
    companions_rating = [_crawl_for_companion_rating(rooms, location, kaeli_mom) for location in companion_candidates]
    random.shuffle(companions_rating)
    companions_rating = [entry for entry in companions_rating if entry[1] > 0]
    if not companions_rating:
        return
    companions_rating.sort(key=lambda entry: entry[1], reverse=True)
    companion_location = companions_rating[0][0] if _normalize_map_shuffle_mode(map_shuffle) == 3 else random.choice(companions_rating)[0]

    location_rating = [_crawl_for_chest_rating2(rooms, location) for location in companion_candidates]
    location_rating = [entry for entry in location_rating if entry[0] != companion_location and entry[1] > 0]
    if not location_rating:
        return
    guaranteed_chest_locations = [random.choice(location_rating)[0]]

    special_regions_access = [
        {"subregion": "AquariaFrozenField", "access": "SummerAquaria", "barred_locations": []},
        {"subregion": "VolcanoBattlefield", "access": "DualheadHydra", "barred_locations": []},
    ]
    gating_locations_access = ["SummerAquaria", "DualheadHydra", "LavaDomePlate", "Gidrah"]
    gating_locations = [(_find_trigger_location(rooms, access), access) for access in gating_locations_access]
    gating_locations = [(location, access) for location, access in gating_locations if location is not None]

    for region in special_regions_access:
        location = next((gating_location for gating_location, access in gating_locations if access == region["access"]), None)
        if location is None:
            continue
        access_req = _crawl_for_requirements(rooms, location)
        common_access = [access for access in access_req if access in gating_locations_access]
        region["barred_locations"].extend(
            [gating_location for gating_location, access in gating_locations if access in common_access] + [location]
        )

    early_locations = [companion_location, safe_gold_battlefield]
    early_locations.extend(guaranteed_chest_locations)
    foresta_locations = [
        location
        for location in destination_locations
        if MAP_SUBREGIONS[location] == "Foresta" and location not in taken_locations
    ]
    while early_locations:
        loc1 = early_locations.pop(0)
        if not foresta_locations:
            break
        loc2 = random.choice(foresta_locations)
        next(entry for entry in movable_locations if entry["origins"] == loc1)["destination"] = loc2
        placed_locations.add(loc1)
        taken_locations.add(loc2)
        foresta_locations = [location for location in foresta_locations if location not in taken_locations]

    starting_locations = [
        location
        for location in shuffle_locations
        if location not in EXCLUDE_FROM_START and location not in placed_locations
    ]
    while foresta_locations:
        if not starting_locations:
            break
        loc1 = random.choice(starting_locations)
        loc2 = random.choice(foresta_locations)
        next(entry for entry in movable_locations if entry["origins"] == loc1)["destination"] = loc2
        placed_locations.add(loc1)
        taken_locations.add(loc2)
        foresta_locations = [location for location in foresta_locations if location not in taken_locations]
        starting_locations = [location for location in starting_locations if location not in placed_locations]

    gating_location_placed = False
    gating_locations_list = [location for location, _access in gating_locations]
    for region in special_regions_access:
        gated_region_locations = [
            location
            for location in destination_locations
            if MAP_SUBREGIONS[location] == region["subregion"] and location not in taken_locations
        ]
        for location in gated_region_locations:
            region_safe_locations = [
                candidate
                for candidate in shuffle_locations
                if candidate not in placed_locations
                and candidate not in region["barred_locations"]
                and ((not gating_location_placed) or candidate not in gating_locations_list)
            ]
            if not region_safe_locations:
                continue
            loc1 = random.choice(region_safe_locations)
            if loc1 in gating_locations_list:
                gating_location_placed = True
            next(entry for entry in movable_locations if entry["origins"] == loc1)["destination"] = location
            placed_locations.add(loc1)
            taken_locations.add(location)

    shuffle_locations = [location for location in shuffle_locations if location not in placed_locations]
    destination_locations = [location for location in destination_locations if location not in taken_locations]
    while shuffle_locations and destination_locations:
        loc1 = _take_random(shuffle_locations, random)
        loc2 = _take_random(destination_locations, random)
        next(entry for entry in movable_locations if entry["origins"] == loc1)["destination"] = loc2

    for room in region_rooms:
        room["game_objects"] = []
        room["links"] = [link for link in room.get("links", []) if link.get("entrance", -1) < 0]

    for location in movable_locations:
        target_region = next(room for room in region_rooms if room["region"] == region_location_pairs[location["destination"]])
        if location["type"] == "Battlefield":
            location["object"]["location_slot"] = location["destination"]
            target_region["game_objects"].append(location["object"])
            continue

        original_region = next(room for room in region_rooms if room["region"] == location["region"])
        location["link"]["location_slot"] = location["destination"]
        target_region["links"].append(location["link"])

        room_link_owner = _room_by_id(rooms, location["room"])
        link_to_update = next((link for link in room_link_owner.get("links", []) if link["target_room"] == original_region["id"]), None)
        if link_to_update is not None:
            link_to_update["target_room"] = target_region["id"]


def _crest_shuffle(rooms: list[dict[str, Any]], crest_shuffle: bool, random: randomlib.Random) -> None:
    crest_list = [
        {"entrance": [67, 8], "origins": [64, 8], "deadend": True, "priority": 0},
        {"entrance": [68, 8], "origins": [65, 8], "deadend": True, "priority": 0},
        {"entrance": [69, 8], "origins": [66, 8], "deadend": True, "priority": 0},
        {"entrance": [72, 8], "origins": [45, 8], "deadend": False, "priority": 1},
        {"entrance": [59, 8], "origins": [60, 8], "deadend": False, "priority": 0},
        {"entrance": [60, 8], "origins": [59, 8], "deadend": True, "priority": 0},
        {"entrance": [64, 8], "origins": [67, 8], "deadend": False, "priority": 0},
        {"entrance": [65, 8], "origins": [68, 8], "deadend": False, "priority": 0},
        {"entrance": [66, 8], "origins": [69, 8], "deadend": False, "priority": 0},
        {"entrance": [62, 8], "origins": [63, 8], "deadend": True, "priority": 0},
        {"entrance": [63, 8], "origins": [62, 8], "deadend": False, "priority": 0},
        {"entrance": [45, 8], "origins": [72, 8], "deadend": False, "priority": 1},
        {"entrance": [54, 8], "origins": [44, 8], "deadend": False, "priority": 2},
        {"entrance": [71, 8], "origins": [70, 8], "deadend": False, "priority": 0},
        {"entrance": [70, 8], "origins": [71, 8], "deadend": True, "priority": 0},
        {"entrance": [44, 8], "origins": [54, 8], "deadend": False, "priority": 0},
        {"entrance": [43, 8], "origins": [61, 8], "deadend": False, "priority": 2},
        {"entrance": [61, 8], "origins": [43, 8], "deadend": True, "priority": 0},
    ]

    if not crest_shuffle:
        return

    crest_tiles = [
        "LibraCrest",
        "LibraCrest",
        "GeminiCrest",
        "GeminiCrest",
        "GeminiCrest",
        "MobiusCrest",
        "MobiusCrest",
        "MobiusCrest",
        "MobiusCrest",
    ]

    random.shuffle(crest_list)
    crest_list.sort(key=lambda x: x["priority"], reverse=True)
    crest_priority: list[tuple[int, str]] = []
    new_link_to_process: list[tuple[int, dict[str, Any]]] = []

    while crest_list:
        deadend_count = sum(1 for x in crest_list if x["deadend"])
        passable_count = sum(1 for x in crest_list if not x["deadend"])

        crest1 = crest_list.pop(0)

        if crest1["deadend"]:
            non_deadend = [x for x in crest_list if not x["deadend"]]
            crest2 = random.choice(non_deadend)
            crest_list.remove(crest2)
        else:
            if deadend_count < passable_count:
                crest2 = _take_random(crest_list, random)
            else:
                crest2 = [x for x in crest_list if x["deadend"]][0]
                crest_list.remove(crest2)

        if crest1["priority"] > 0:
            existing = [x for x in crest_priority if x[0] == crest1["priority"]]
            if existing:
                crest1_crest = existing[0][1]
                if crest1_crest in crest_tiles:
                    crest_tiles.remove(crest1_crest)
            else:
                crest1_crest = _take_random(crest_tiles, random)
                crest_priority.append((crest1["priority"], crest1_crest))
        else:
            crest1_crest = _take_random(crest_tiles, random)

        crest2_crest = crest1_crest
        if crest2["priority"] > 0 and not any(x[0] == crest2["priority"] for x in crest_priority):
            crest_priority.append((crest2["priority"], crest1_crest))

        crest1room = next(r for r in rooms if any(l.get("teleporter") == crest1["entrance"] for l in r["links"]))
        crest1link = next(l for l in crest1room["links"] if l.get("teleporter") == crest1["entrance"])
        crest2room = next(r for r in rooms if any(l.get("teleporter") == crest2["entrance"] for l in r["links"]))
        crest2link = next(l for l in crest2room["links"] if l.get("teleporter") == crest2["entrance"])

        crest1room["links"].remove(crest1link)
        crest2room["links"].remove(crest2link)

        access1 = [a for a in crest1link.get("access", []) if a not in CRESTS_ACCESS] + [crest1_crest]
        access2 = [a for a in crest2link.get("access", []) if a not in CRESTS_ACCESS] + [crest2_crest]

        new_link_to_process.append((crest1room["id"], {"target_room": crest2room["id"], "entrance": crest1link["entrance"], "teleporter": crest2["origins"], "access": access1}))
        new_link_to_process.append((crest2room["id"], {"target_room": crest1room["id"], "entrance": crest2link["entrance"], "teleporter": crest1["origins"], "access": access2}))

    for room_id, link in new_link_to_process:
        _room_by_id(rooms, room_id)["links"].append(link)


def _floor_shuffle(
    rooms: list[dict[str, Any]],
    map_shuffle: str | int,
    random: randomlib.Random,
    overworld_shuffle: bool | None = None,
) -> None:
    map_shuffle = _normalize_map_shuffle_mode(map_shuffle)
    if map_shuffle not in MAP_SHUFFLE_DUNGEON_MODES:
        return

    _ = overworld_shuffle
    include_temples_towns = map_shuffle in {"Everything", 3}
    intradungeon = map_shuffle in {"DungeonsInternal", 1}
    pending_links: list[tuple[int, dict[str, Any]]] = []

    for room_id, target_room in shuffling_data.get("blocked_oneways", []):
        room = _room_by_id(rooms, room_id)
        room["links"] = [l for l in room["links"] if l.get("target_room") != target_room]

    for room_id, target_room, access_req in shuffling_data.get("added_links", []):
        _room_by_id(rooms, room_id)["links"].append({"target_room": target_room, "access": [int(access_req)]})

    room_links: list[tuple[int, dict[str, Any]]] = []
    for room in rooms:
        for link in room["links"]:
            if link.get("entrance", -1) >= 0:
                room_links.append((room["id"], link))

    def _find_entrance(eid: int):
        for rid, link in room_links:
            if link["entrance"] == eid:
                return rid, link
        raise KeyError(f"Entrance not found: {eid}")

    logic_links: list[LogicLink] = []
    for e0, e1 in entrances_pairs:
        r0, l0 = _find_entrance(e0)
        _, l1 = _find_entrance(e1)
        logic_links.append(LogicLink(r0, l0, l1))
    for e0, e1 in entrances_pairs:
        r1, l1 = _find_entrance(e1)
        _, l0 = _find_entrance(e0)
        logic_links.append(LogicLink(r1, l1, l0))

    doom_castle_rooms = {195, 196, 197, 198, 199, 200, 201}
    room_triggers = []
    rooms_req = []
    for room in rooms:
        if room["id"] in doom_castle_rooms:
            continue
        for obj in room.get("game_objects", []):
            if obj.get("type") == "Trigger":
                room_triggers.append((room["id"], obj.get("on_trigger", [])))
        for link in room["links"]:
            if link.get("access"):
                rooms_req.append((room["id"], link))

    forbidden_destinations = []
    for trigger_room_id, on_trigger in room_triggers:
        for room_id, link in rooms_req:
            if room_id != trigger_room_id and link.get("entrance", -1) != -1 and set(link.get("access", [])).intersection(on_trigger):
                forbidden_destinations.append((link["entrance"], trigger_room_id))

    if not include_temples_towns:
        towns_temples = set(shuffling_data["towns_temples"])
        logic_links = [x for x in logic_links if x.current["entrance"] not in towns_temples]

    forced_links = [(int(link[0]), int(link[1])) for link in shuffling_data.get("forced_links", [])]
    entrance_only = set(shuffling_data.get("entrance_only", []))
    forced_deadends = set(shuffling_data.get("forced_deadends", []))
    no_exits = set(shuffling_data.get("no_exits", []))
    priority_exits = set(shuffling_data.get("priority_exits", []))

    for link in logic_links:
        link.entrance_only = link.current["entrance"] in entrance_only
        link.force_dead_end = link.current["entrance"] in forced_deadends
        link.exit = link.current["entrance"] not in no_exits
        link.priority_exit = link.current["entrance"] in priority_exits

    for entrance, room in forbidden_destinations:
        target = next((l for l in logic_links if l.current["entrance"] == entrance), None)
        if target is not None:
            target.forbidden_destinations = [room]

    cluster_rooms: list[ClusterRoom] = []
    max_id = 0
    for room in rooms:
        internal_links = [x["target_room"] for x in room["links"] if x.get("entrance", -1) < 0] + [room["id"]]
        max_id = max(max_id, *internal_links)
        cluster_rooms.append(ClusterRoom(rooms=internal_links, links=[l for l in logic_links if l.room == room["id"]]))

    for i in range(max_id + 1):
        common = [x for x in cluster_rooms if i in x.rooms]
        if len(common) > 1:
            for room in common[1:]:
                cluster_rooms.remove(room)
                common[0].merge(room)

    # Crawl from each subregion entrance and stamp the reachable dungeon clusters with that logical location.
    room_to_clusters: dict[int, list[ClusterRoom]] = {}
    for cluster in cluster_rooms:
        for room_id in cluster.rooms:
            room_to_clusters.setdefault(room_id, []).append(cluster)

    def process_cluster_room(room_id: int, processed_rooms: set[int], current_location: str) -> None:
        current_room = _room_by_id(rooms, room_id)
        for cluster in room_to_clusters.get(room_id, []):
            cluster.location = current_location
        processed_rooms.add(room_id)

        child_links = sorted(current_room.get("links", []), key=lambda link: link.get("entrance", -1))
        for child in child_links:
            target_room = child["target_room"]
            if target_room in processed_rooms:
                continue
            if set(child.get("access", [])).intersection(CRESTS_ACCESS):
                continue
            if _room_by_id(rooms, target_room).get("type") == "Subregion":
                continue
            process_cluster_room(target_room, processed_rooms, current_location)

    processed_rooms: set[int] = {0}
    for room in rooms:
        if room.get("type") != "Subregion":
            continue
        for link in room.get("links", []):
            location = link.get("location")
            if location and location not in {"None", "GiantTree", "MacsShipDoom"}:
                process_cluster_room(link["target_room"], processed_rooms, location)

    # Forced links are direct entrance-to-entrance ties in latest C# shuffling data.
    for origin_entrance, destination_entrance in forced_links:
        origin_link = next((l for l in logic_links if l.current["entrance"] == origin_entrance), None)
        target_link = next((l for l in logic_links if l.current["entrance"] == destination_entrance), None)
        if origin_link is None or target_link is None:
            continue

        origin_cluster = next((c for c in cluster_rooms if origin_link in c.links), None)
        target_cluster = next((c for c in cluster_rooms if target_link in c.links), None)

        _connect_link(rooms, pending_links, origin_link, target_link)
        logic_links = [l for l in logic_links if l.current["entrance"] not in {origin_entrance, destination_entrance}]
        if origin_cluster is not None and origin_link in origin_cluster.links:
            origin_cluster.links.remove(origin_link)
        if target_cluster is not None and target_link in target_cluster.links:
            target_cluster.links.remove(target_link)

        if origin_cluster is not None and target_cluster is not None and origin_cluster is not target_cluster:
            origin_cluster.merge(target_cluster)
            cluster_rooms.remove(target_cluster)

    crest_rooms = [r["id"] for r in rooms if any(set(l.get("access", [])).intersection(CRESTS_ACCESS) for l in r["links"])]
    mac_ship_barred = set(crest_rooms + shuffling_data["mac_ship_exclusions"] + [x[1] for x in forbidden_destinations])
    mac_ship_deck = 187
    mac_ship_max_size = 4
    crystal_rooms = [
        {"location": "BoneDungeon", "target": 38, "base": 25},
        {"location": "IcePyramid", "target": 70, "base": 54},
        {"location": "LavaDome", "target": 121, "base": 100},
        {"location": "PazuzusTower", "target": 179, "base": 166},
    ]
    subregion_room_ids = {r["id"] for r in rooms if r.get("type") == "Subregion"}
    seed_links_locations = {
        int(link["entrance"]): link.get("location")
        for room in rooms
        if room.get("type") == "Subregion"
        for link in room.get("links", [])
        if link.get("entrance", -1) >= 0 and link.get("location") not in {None, "None"}
    }

    seed_rooms = [
        link["target_room"]
        for room in rooms
        if room.get("type") == "Subregion"
        for link in room.get("links", [])
        if link.get("entrance", -1) >= 0 and link["target_room"] != 125
    ]
    seed_cluster_rooms = [x for x in cluster_rooms if set(x.rooms).intersection(seed_rooms)]
    seed_shuffle = [x for x in seed_cluster_rooms if any(l.current["target_room"] in subregion_room_ids for l in x.links)]
    seed_overworld_entrance = {
        id(cluster): next((l.current["entrance"] for l in cluster.links if l.current["target_room"] == 0), None)
        for cluster in seed_shuffle
    }
    seed_fixed = [x for x in seed_cluster_rooms if not _contains_identity(seed_shuffle, x)]
    seed_prog = [x for x in seed_shuffle if len(x.links) > 1]
    seed_dead = [x for x in seed_shuffle if len(x.links) == 1]

    init_prog = [x for x in cluster_rooms if len(x.links) > 1 and not set(x.rooms).intersection(seed_rooms) and 0 not in x.rooms] + seed_prog
    init_dead = [x for x in cluster_rooms if len(x.links) == 1 and not set(x.rooms).intersection(seed_rooms) and 0 not in x.rooms] + seed_dead

    random.shuffle(init_prog)
    random.shuffle(init_dead)

    if intradungeon:
        core_cluster_rooms = []
        for progress_room in seed_prog:
            valid_rooms = [
                room
                for room in init_prog
                if room.location == progress_room.location and sum(1 for link in room.links if not link.forbidden_destinations) > 1
            ]
            core_cluster_rooms.append(random.choice(valid_rooms))
        core_cluster_rooms.extend(seed_dead)
    else:
        non_crystal_prog = [x for x in init_prog if not set(x.rooms).intersection([c["target"] for c in crystal_rooms])]
        non_crystal_dead = [x for x in init_dead if not set(x.rooms).intersection([c["target"] for c in crystal_rooms])]
        core_cluster_rooms = non_crystal_prog[: len(seed_prog)] + non_crystal_dead[: len(seed_dead)]
    valid_seed_switch = [x for x in core_cluster_rooms if not _contains_identity(seed_shuffle, x)]
    valid_seed_fixed = [x for x in core_cluster_rooms if _contains_identity(seed_shuffle, x)]

    for room in valid_seed_fixed:
        core_link = next((link for link in room.links if link.current["target_room"] in subregion_room_ids), None)
        if core_link is None:
            continue
        links_from_overworld = [
            link
            for cluster in cluster_rooms
            if set(cluster.rooms).intersection(subregion_room_ids)
            for link in cluster.links
        ]
        ow_link = next((link for link in links_from_overworld if link.origin["entrance"] == core_link.current["entrance"]), None)
        if ow_link is None:
            continue
        room.links.remove(core_link)
        ow_cluster = next((cluster for cluster in cluster_rooms if ow_link in cluster.links), None)
        if ow_cluster is not None:
            ow_cluster.links.remove(ow_link)
        _connect_overworld_link(
            rooms,
            pending_links,
            room.location,
            ow_link,
            core_link,
        )

    valid_crystal_source = [room for room in valid_seed_switch if len(room.links) > 1]
    for crystal in crystal_rooms:
        links_from_overworld = [
            link
            for cluster in cluster_rooms
            if set(cluster.rooms).intersection(subregion_room_ids)
            for link in cluster.links
        ]
        ow_link = next((link for link in links_from_overworld if link.current.get("location") == crystal["location"]), None)
        if ow_link is None:
            continue

        progress_room = next((room for room in valid_crystal_source if room.location == crystal["location"]), None)
        if progress_room is None:
            progress_room = random.choice(valid_crystal_source)

        valid_links = [link for link in progress_room.links if link.exit]
        priority_links = [link for link in valid_links if link.priority_exit]
        core_link = priority_links[0] if priority_links else random.choice(valid_links)
        crystal["base"] = progress_room.rooms[0]

        progress_room.links.remove(core_link)
        ow_cluster = next((cluster for cluster in cluster_rooms if ow_link in cluster.links), None)
        if ow_cluster is not None:
            ow_cluster.links.remove(ow_link)

        _connect_overworld_link(
            rooms,
            pending_links,
            seed_links_locations.get(ow_link.current["entrance"]),
            ow_link,
            core_link,
        )
        if _contains_identity(valid_crystal_source, progress_room):
            _remove_identity(valid_crystal_source, progress_room)
        if _contains_identity(valid_seed_switch, progress_room):
            _remove_identity(valid_seed_switch, progress_room)

    for room in valid_seed_switch:
        valid_links = [link for link in room.links if link.exit]
        priority_links = [link for link in valid_links if link.priority_exit]
        core_link = priority_links[0] if priority_links else random.choice(valid_links)
        links_from_overworld = [
            link
            for cluster in cluster_rooms
            if set(cluster.rooms).intersection(subregion_room_ids)
            for link in cluster.links
        ]
        ow_link = next((link for link in links_from_overworld if link.current.get("location") == room.location), None)
        if ow_link is None:
            ow_link = random.choice(links_from_overworld)
        room.links.remove(core_link)
        ow_cluster = next((cluster for cluster in cluster_rooms if ow_link in cluster.links), None)
        if ow_cluster is not None:
            ow_cluster.links.remove(ow_link)
        _connect_overworld_link(
            rooms,
            pending_links,
            seed_links_locations.get(ow_link.current["entrance"]),
            ow_link,
            core_link,
        )

    core_cluster_rooms = core_cluster_rooms + seed_fixed
    core_ids = set([0] + [rid for c in core_cluster_rooms for rid in c.rooms])
    progress_cluster_rooms = [x for x in cluster_rooms if len(x.links) > 1 and not set(x.rooms).intersection(core_ids)]
    deadend_cluster_rooms = [x for x in cluster_rooms if len(x.links) == 1 and not set(x.rooms).intersection(core_ids)]

    random.shuffle(core_cluster_rooms)
    core_cluster_rooms = [x for x in core_cluster_rooms if x.links]

    if intradungeon:
        # C# intradungeon mode resolves everything in this branch and does not
        # fall through to the non-intradungeon progress/deadend pipeline.
        for origin_room in core_cluster_rooms:
            if not origin_room.links or origin_room.location is None:
                continue

            loc_progress = [x for x in progress_cluster_rooms if x.location == origin_room.location]
            loc_dead = [x for x in deadend_cluster_rooms if x.location == origin_room.location]
            if not loc_progress and not loc_dead:
                continue

            valid_pairs: list[tuple[LogicLink, LogicLink]] | None = None
            chosen_progress = loc_progress.copy()
            chosen_dead = loc_dead.copy()

            for _attempt in range(120):
                origin_cluster = ClusterLocation(
                    rooms=[
                        ClusterRoom(
                            origin_room.rooms.copy(),
                            origin_room.links.copy(),
                            origin_room.size,
                            origin_room.location,
                            origin_room.forbidden_destinations.copy(),
                        )
                    ],
                    location=origin_room.location,
                    initial_rooms=origin_room.rooms.copy(),
                )
                pairs: list[tuple[LogicLink, LogicLink]] = []
                valid = True

                random.shuffle(chosen_progress)

                # Progress placement
                for dest in chosen_progress:
                    origin_candidates = origin_cluster.links.copy()
                    if not origin_candidates:
                        valid = False
                        break
                    origin_link = random.choice(origin_candidates)

                    if set(dest.rooms).intersection(origin_cluster.forbidden_destinations_for(origin_link)):
                        valid = False
                        break

                    dest_candidates = [l for l in dest.links if l.exit]
                    if not dest_candidates:
                        valid = False
                        break
                    priority_dest = next((l for l in dest_candidates if l.priority_exit), None)
                    dest_link = priority_dest if priority_dest is not None else random.choice(dest_candidates)

                    pairs.append((origin_link, dest_link))
                    origin_cluster.merge(dest, origin_link, dest_link)

                if not valid:
                    continue

                # Deadend placement
                random.shuffle(chosen_dead)
                for dest in chosen_dead:
                    available_locations = [room for room in origin_cluster.rooms if room.links]
                    odd_links_locations = [room for room in origin_cluster.rooms if (len(room.links) % 2) == 1]
                    no_exit_locations = [room for room in origin_cluster.rooms if any(not link.exit for link in room.links)]
                    no_exit = False
                    if no_exit_locations:
                        available_locations = no_exit_locations
                        no_exit = True
                    elif odd_links_locations:
                        available_locations = odd_links_locations

                    if not available_locations or not dest.links:
                        valid = False
                        break
                    origin_location = random.choice(available_locations)
                    origin_links = [link for link in origin_location.links if not link.exit] if no_exit else origin_location.links
                    origin_link = random.choice(origin_links)
                    if set(dest.rooms).intersection(origin_cluster.forbidden_destinations_for(origin_link)):
                        valid = False
                        break
                    dest_link = random.choice(dest.links)
                    pairs.append((origin_link, dest_link))
                    origin_cluster.merge(dest, origin_link, dest_link)

                if not valid:
                    continue

                # Validate leftovers (no forced deadends, even links), then pair leftovers.
                if origin_cluster.odd_links or origin_cluster.dead_end_required:
                    continue

                for room in origin_cluster.rooms:
                    while room.links:
                        first = _take_random(room.links, random)
                        second = _take_random(room.links, random)
                        pairs.append((first, second))

                valid_pairs = pairs
                break

            if valid_pairs is None:
                continue

            for link_a, link_b in valid_pairs:
                _connect_link(rooms, pending_links, link_a, link_b)

            for dest in chosen_progress:
                if _contains_identity(progress_cluster_rooms, dest):
                    _remove_identity(progress_cluster_rooms, dest)
                    origin_room.merge(dest)
            for dest in chosen_dead:
                if _contains_identity(deadend_cluster_rooms, dest):
                    _remove_identity(deadend_cluster_rooms, dest)
                    origin_room.merge(dest)

        for room_id, link in pending_links:
            _room_by_id(rooms, room_id)["links"].append(link)

        for room in rooms:
            if room.get("type") != "Subregion":
                continue
            for link in room.get("links", []):
                if link.get("entrance", -1) < 0 or link.get("location") not in (None, "None"):
                    continue
                fallback_location = seed_links_locations.get(link.get("entrance"))
                if fallback_location not in (None, "None"):
                    link["location"] = fallback_location
                    link["location_slot"] = fallback_location
        return

    origin_locations = [
        ClusterLocation(
            rooms=[
                ClusterRoom(
                    cluster.rooms.copy(),
                    cluster.links.copy(),
                    cluster.size,
                    cluster.location,
                    cluster.forbidden_destinations.copy(),
                )
            ],
            location=cluster.location,
            initial_rooms=cluster.rooms.copy(),
        )
        for cluster in core_cluster_rooms
    ]

    mac_ship_merging_count = 0
    mac_ship = next((location for location in origin_locations if mac_ship_deck in [room_id for room in location.rooms for room_id in room.rooms]), None)
    if mac_ship is not None:
        for room in mac_ship.rooms:
            room.forbidden_destinations.extend(mac_ship_barred)

    sky_crystal_room_placed = False
    sky_crystal = crystal_rooms[3]
    sky_crystal_room = next((cluster for cluster in progress_cluster_rooms if sky_crystal["target"] in cluster.rooms), None)
    if sky_crystal_room is not None:
        _remove_identity(progress_cluster_rooms, sky_crystal_room)
    else:
        sky_crystal_room_placed = True

    while progress_cluster_rooms:
        valid_origins = origin_locations
        if mac_ship is not None and mac_ship_merging_count >= (mac_ship_max_size - 2):
            valid_origins = [location for location in origin_locations if location is not mac_ship]
        origin_room = random.choice(valid_origins)
        origin_link = random.choice(origin_room.links)

        destination_rooms = [
            cluster
            for cluster in progress_cluster_rooms
            if not set(cluster.rooms).intersection(origin_room.forbidden_destinations_for(origin_link))
        ]
        if not destination_rooms:
            continue

        destination_room = random.choice(destination_rooms)
        _remove_identity(progress_cluster_rooms, destination_room)

        priority_link = next((link for link in destination_room.links if link.priority_exit), None)
        exit_links = [link for link in destination_room.links if link.exit]
        destination_link = priority_link if priority_link is not None else random.choice(exit_links)

        _connect_link(rooms, pending_links, origin_link, destination_link)
        origin_room.merge(destination_room, origin_link, destination_link)
        if origin_room is mac_ship:
            mac_ship_merging_count += 1

    if not sky_crystal_room_placed and sky_crystal_room is not None:
        sky_location = next(
            (
                location
                for location in origin_locations
                if any(sky_crystal["base"] in room.rooms for room in location.rooms)
            ),
            None,
        )
        if sky_location is not None:
            destination_link = random.choice(sky_crystal_room.links)
            origin_link = random.choice(sky_location.links)
            _connect_link(rooms, pending_links, origin_link, destination_link)
            sky_location.merge(sky_crystal_room, origin_link, destination_link)

    crystal_clusters = [
        cluster
        for cluster in deadend_cluster_rooms
        if set(cluster.rooms).intersection([crystal["target"] for crystal in crystal_rooms])
    ]
    deadend_cluster_rooms = [cluster for cluster in deadend_cluster_rooms if not _contains_identity(crystal_clusters, cluster)]

    for crystal_cluster in crystal_clusters:
        crystal_room = next(crystal for crystal in crystal_rooms if crystal["target"] in crystal_cluster.rooms)
        origin_room = next(
            location
            for location in origin_locations
            if any(crystal_room["base"] in room.rooms for room in location.rooms)
        )
        origin_link = random.choice(origin_room.links)
        destination_link = random.choice(crystal_cluster.links)
        _connect_link(rooms, pending_links, origin_link, destination_link)
        origin_room.merge(crystal_cluster, origin_link, destination_link)

    crest_clusters = [cluster for cluster in deadend_cluster_rooms if set(cluster.rooms).intersection(crest_rooms)]
    deadend_cluster_rooms = [cluster for cluster in deadend_cluster_rooms if not _contains_identity(crest_clusters, cluster)]

    while crest_clusters:
        valid_origins = [
            location
            for location in origin_locations
            if location is not mac_ship and any(link.exit for link in location.rooms[0].links)
        ]
        origin_room = random.choice(valid_origins)
        origin_links = [link for link in origin_room.rooms[0].links if link.exit]
        origin_link = random.choice(origin_links)

        destination_rooms = [
            cluster
            for cluster in crest_clusters
            if not set(cluster.rooms).intersection(origin_room.forbidden_destinations_for(origin_link))
        ]
        if not destination_rooms:
            continue

        destination_room = random.choice(destination_rooms)
        _remove_identity(crest_clusters, destination_room)
        destination_link = random.choice(destination_room.links)
        _connect_link(rooms, pending_links, origin_link, destination_link)
        origin_room.merge(destination_room, origin_link, destination_link)

    dead_end_link_pairs: list[tuple[LogicLink, LogicLink]] = []
    valid_deadends = False
    for location in origin_locations:
        location.backup_state()

    while not valid_deadends:
        for location in origin_locations:
            location.restore_backup()
        deadend_rooms_to_process = deadend_cluster_rooms.copy()
        dead_end_link_pairs = []
        deadend_insanity = 0
        abort_run = False

        while deadend_rooms_to_process:
            remove_mac_ship = (
                mac_ship is not None
                and mac_ship_merging_count >= mac_ship_max_size
                and not mac_ship.odd_links
                and not mac_ship.dead_end_required
            )
            available_locations = [
                location
                for location in origin_locations
                if any(room.links for room in location.rooms) and (not remove_mac_ship or location is not mac_ship)
            ]
            odd_links_locations = [location for location in available_locations if location.odd_links]
            no_exit_locations = [location for location in available_locations if location.dead_end_required]
            no_exit = False
            odd_links = False

            if no_exit_locations:
                available_locations = no_exit_locations
                no_exit = True
            elif odd_links_locations:
                available_locations = odd_links_locations
                odd_links = True

            origin_room = random.choice(available_locations)
            origin_links = origin_room.links
            if no_exit:
                origin_links = [link for link in origin_room.links if not link.exit]
            elif odd_links:
                origin_links = [link for room in origin_room.rooms if (len(room.links) % 2) == 1 for link in room.links]

            origin_link = random.choice(origin_links)
            destination_rooms = [
                cluster
                for cluster in deadend_rooms_to_process
                if not set(cluster.rooms).intersection(origin_room.forbidden_destinations_for(origin_link))
            ]
            mac_ship_allowed = [cluster for cluster in destination_rooms if not set(cluster.rooms).intersection(mac_ship_barred)]
            destination_rooms = mac_ship_allowed if mac_ship_allowed else destination_rooms

            if not destination_rooms:
                deadend_insanity += 1
                if deadend_insanity > 20:
                    abort_run = True
                else:
                    continue

            if abort_run:
                break

            destination_room = random.choice(destination_rooms)
            _remove_identity(deadend_rooms_to_process, destination_room)
            destination_link = random.choice(destination_room.links)
            dead_end_link_pairs.append((origin_link, destination_link))
            origin_room.merge(destination_room, origin_link, destination_link)
            if origin_room is mac_ship:
                mac_ship_merging_count += 1

        if not deadend_rooms_to_process:
            valid_deadends = True

    for link_a, link_b in dead_end_link_pairs:
        _connect_link(rooms, pending_links, link_a, link_b)

    orphaned_rooms = [room for location in origin_locations for room in location.rooms if (len(room.links) % 2) == 1]
    if len(orphaned_rooms) == 1:
        origin_link = {"target_room": 500, "entrance": 0, "teleporter": [141, 1], "access": []}
        destination_link = {"target_room": 0, "entrance": 481, "teleporter": [0, 10], "access": []}
        dummy_room = ClusterRoom([500], [LogicLink(500, destination_link, origin_link)], location=None)
        orphaned_room = orphaned_rooms[0]
        orphaned_location = next(location for location in origin_locations if orphaned_room in location.rooms)
        orphaned_link = random.choice(orphaned_room.links)
        dummy_room_link = dummy_room.links[0]
        _connect_link(rooms, pending_links, orphaned_link, dummy_room_link)
        orphaned_location.merge(dummy_room, orphaned_link, dummy_room_link)
        rooms.append({"name": "Dummy Room", "id": 500, "game_objects": [], "links": []})
    elif len(orphaned_rooms) > 1:
        raise RuntimeError("There's invalid loops left")

    for location in origin_locations:
        for room in location.rooms:
            while room.links:
                if (len(room.links) % 2) == 1:
                    raise RuntimeError("Floor Shuffle: Gap Connection Error")
                _connect_link(rooms, pending_links, _take_random(room.links, random), _take_random(room.links, random))

    for room_id, link in pending_links:
        _room_by_id(rooms, room_id)["links"].append(link)

    for room in rooms:
        if room.get("type") != "Subregion":
            continue
        for link in room.get("links", []):
            if link.get("entrance", -1) < 0 or link.get("location") not in (None, "None"):
                continue
            fallback_location = seed_links_locations.get(link.get("entrance"))
            if fallback_location not in (None, "None"):
                link["location"] = fallback_location
                link["location_slot"] = fallback_location


def _normalize_yaml_rooms(rooms: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized_rooms: list[dict[str, Any]] = []
    for room in rooms:
        normalized_objects = []
        for obj in room.get("game_objects", []):
            normalized_objects.append(
                {
                    "object_id": obj.get("object_id", 0),
                    "type": obj.get("type"),
                    "on_trigger": [ACCESS_REQ_VALUE_NAMES.get(value, value) for value in obj.get("on_trigger", [])],
                    "access": [ACCESS_REQ_VALUE_NAMES.get(value, value) for value in obj.get("access", [])],
                    "location": obj.get("location", "None"),
                    "location_slot": obj.get("location_slot", obj.get("location", "None")),
                    "name": obj.get("name"),
                }
            )

        normalized_links = []
        for link in room.get("links", []):
            normalized_links.append(
                {
                    "target_room": link.get("target_room"),
                    "entrance": link.get("entrance", -1),
                    "access": [ACCESS_REQ_VALUE_NAMES.get(value, value) for value in link.get("access", [])],
                    "location": link.get("location", "None"),
                    "location_slot": link.get("location_slot", link.get("location", "None")),
                    "teleporter": list(link.get("teleporter", [0, 0])),
                }
            )

        normalized_rooms.append(
            {
                "name": room.get("name"),
                "id": room.get("id"),
                "game_objects": normalized_objects,
                "links": normalized_links,
                "type": room.get("type") or ("Overworld" if room.get("id") == 0 else "Subregion" if room.get("id", 0) >= 220 else "Dungeon"),
                "location": room.get("location", "None"),
                "region": room.get("region", "Foresta"),
            }
        )
    return normalized_rooms



def generate_rooms(
    random: randomlib.Random,
    map_shuffle: str | int,
    crest_shuffle: bool,
    battlefield_shuffle: bool,
    companion_shuffle: int | bool,
    kaeli_mom: bool,
    overworld_shuffle: bool,
) -> list[dict[str, Any]]:

    rooms = deepcopy(base_rooms)
    battlefield_rewards = _shuffle_battlefield_rewards(rooms, battlefield_shuffle=battlefield_shuffle, random=random)
    _companions_shuffle(rooms, companion_shuffle=companion_shuffle, kaeli_mom=kaeli_mom, random=random)

    _crest_shuffle(rooms, crest_shuffle=crest_shuffle, random=random)
    _floor_shuffle(rooms, map_shuffle=map_shuffle, random=random, overworld_shuffle=overworld_shuffle)
    _shuffle_overworld(
        rooms,
        map_shuffle=map_shuffle,
        overworld_shuffle=overworld_shuffle,
        kaeli_mom=kaeli_mom,
        battlefield_rewards=battlefield_rewards,
        random=random,
    )

    return _normalize_yaml_rooms(rooms)

