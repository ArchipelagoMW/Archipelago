from ..roomEditor import RoomEditor, ObjectWarp
from ..worldSetup import ENTRANCE_INFO


def changeEntrances(rom, mapping):
    warp_to = {}
    warp_from_rooms = {}
    warp_vanilla = {}
    for key in mapping.keys():
        if key.endswith(":inside"):
            continue
        info = ENTRANCE_INFO[key]
        re = RoomEditor(rom, info.alt_room if info.alt_room is not None else info.room)
        warp = re.getWarps()[info.index if info.index not in (None, "all") else 0]
        warp_to[f"{key}:inside"] = warp
        warp_vanilla[key] = warp.room
        assert info.target == warp.room, "%s != %03x" % (key, warp.room)
        warp_from_rooms[f"{key}:inside"] = [info.target]
        if info.instrument_room:
            warp_from_rooms[f"{key}:inside"].append(info.instrument_room)

        re = RoomEditor(rom, warp.room)
        for warp in re.getWarps():
            if warp.room == info.room:
                warp_to[key] = warp
                warp_vanilla[f"{key}:inside"] = warp.room
            assert key in warp_to, "Missing warp to outdoor on %s" % (key)

            warp_from_rooms[key] = [info.room]
            if info.alt_room:
                warp_from_rooms[key].append(info.alt_room)

    # First collect all the changes we need to do per room
    changes_per_room = {}
    def addChange(source_room, target_room, new_warp):
        if source_room not in changes_per_room:
            changes_per_room[source_room] = {}
        changes_per_room[source_room][target_room] = new_warp
    for key, target in mapping.items():
        for room in warp_from_rooms[key]:
            addChange(room, warp_vanilla[key], warp_to[target])

    # Finally apply the changes, we need to do this once per room to prevent A->B->C issues.
    for room, changes in changes_per_room.items():
        re = RoomEditor(rom, room)
        for idx, obj in enumerate(re.objects):
            if isinstance(obj, ObjectWarp) and obj.room in changes:
                re.objects[idx] = changes[obj.room].copy()
        re.store(rom)


def readEntrances(rom):
    result = {}
    for key, info in ENTRANCE_INFO.items():
        re = RoomEditor(rom, info.alt_room if info.alt_room is not None else info.room)
        warp = re.getWarps()[info.index if info.index not in (None, "all") else 0]
        for other_key, other_info in ENTRANCE_INFO.items():
            if warp.room == other_info.target:
                result[key] = f"{other_key}:inside"
            if warp.room == other_info.room:
                result[key] = other_key
        
        re = RoomEditor(rom, info.target)
        warp = re.getWarps()[0]
        for other_key, other_info in ENTRANCE_INFO.items():
            if warp.room == other_info.target:
                result[f"{key}:inside"] = f"{other_key}:inside"
            if warp.room == other_info.room:
                result[f"{key}:inside"] = other_key
    return result
