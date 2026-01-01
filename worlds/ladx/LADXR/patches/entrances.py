from ..roomEditor import RoomEditor, ObjectWarp
from ..worldSetup import ENTRANCE_INFO


def changeEntrances(rom, mapping):
    warp_to_indoor = {}
    warp_to_outdoor = {}
    for key in mapping.keys():
        info = ENTRANCE_INFO[key]
        re = RoomEditor(rom, info.alt_room if info.alt_room is not None else info.room)
        warp = re.getWarps()[info.index if info.index not in (None, "all") else 0]
        warp_to_indoor[key] = warp
        assert info.target == warp.room, "%s != %03x" % (key, warp.room)

        re = RoomEditor(rom, warp.room)
        for warp in re.getWarps():
            if warp.room == info.room:
                warp_to_outdoor[key] = warp
        assert key in warp_to_outdoor, "Missing warp to outdoor on %s" % (key)

    # First collect all the changes we need to do per room
    changes_per_room = {}
    def addChange(source_room, target_room, new_warp):
        if source_room not in changes_per_room:
            changes_per_room[source_room] = {}
        changes_per_room[source_room][target_room] = new_warp
    for key, target in mapping.items():
        if key == target:
            continue
        info = ENTRANCE_INFO[key]
        # Change the entrance to point to the new indoor room
        addChange(info.room, warp_to_indoor[key].room, warp_to_indoor[target])
        if info.alt_room:
            addChange(info.alt_room, warp_to_indoor[key].room, warp_to_indoor[target])

        # Change the exit to point to the right outside
        addChange(warp_to_indoor[target].room, ENTRANCE_INFO[target].room, warp_to_outdoor[key])
        if ENTRANCE_INFO[target].instrument_room is not None:
            addChange(ENTRANCE_INFO[target].instrument_room, ENTRANCE_INFO[target].room, warp_to_outdoor[key])

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
                result[key] = other_key
    return result
