from enum import Enum
from random import Random

from .options import RandomizeDarkBrambleLayout


# In the stringified layout format we want to output for slot data, the vanilla DB layout is:
# "H->SCEA|C->PX|E->A|A->V"

# Explicit goals/non-goals of this randomization approach include:
# - All 8 vanilla DB rooms are accessible in at least one way
# - The intended default logic is the same as the vanilla game: find Pioneer, EscapePod
# and Vessel by following Signalscope signals and/or a Scout launched into a seed portal.
# DB layout randomization does not change this logic at all.
# - Multiple routes to the same room are possible, in fact more likely than in vanilla
# - The number of distinct warps in each room is unchanged. For example, the many portals
# in Cluster still form two "warp groups", while Hub's four portals are all separate warps.
# - Only the one main entrance from space into Dark Bramble is considered. Entering through
# the Jellyfish/Feldspar vine is out of logic, and the "vine warp" is unchanged.
# - The only seed warp being randomized is Cluster's, because it matches normal warps you
# can go through in the same room. The Elsinore seed, TH seed, and Feldspar Camp seeds
# will not be touched.
# - Going back out of a DB room instead of into one of its smaller portals will take you
# either out into space, or into the "previous" room. This is handled on the client,
# and is not an explicit part of the randomized "layout".


class DBRoom(Enum):
    Hub = 1,  # the first room in vanilla, with 1 fish and 4 separate warps
    EscapePod = 2,  # Escape Pod 3 and the Nomai Grave
    AnglerNest = 3,  # 3 "guard" anglerfish at the entrance and the anglerfish eggs
    Pioneer = 4,  # Feldspar's Camp, and the vine warp to frozen jellyfish
    ExitOnly = 5,  # the recursive room with the Elsinore seed Easter egg
    Vessel = 6,  # has The Vessel, of course
    Cluster = 7,  # the room with lots of warps, though they only go to 2 different places
    SmallNest = 8,  # small room with 1 fish


def room_to_letter(room: DBRoom) -> str:
    if room == DBRoom.Hub:
        return 'H'
    if room == DBRoom.EscapePod:
        return 'E'
    if room == DBRoom.AnglerNest:
        return 'A'
    if room == DBRoom.Pioneer:
        return 'P'
    if room == DBRoom.ExitOnly:
        return 'X'
    if room == DBRoom.Vessel:
        return 'V'
    if room == DBRoom.Cluster:
        return 'C'
    if room == DBRoom.SmallNest:
        return 'S'


class DBWarp(Enum):
    Hub1 = 1,
    Hub2 = 2,
    Hub3 = 3,
    Hub4 = 4,
    Cluster1 = 11,
    Cluster2 = 12,
    EscapePod1 = 21,
    AnglerNest1 = 31,
    AnglerNest2 = 32,


warps_in_room = {
    DBRoom.Hub: [DBWarp.Hub1, DBWarp.Hub2, DBWarp.Hub3, DBWarp.Hub4],
    DBRoom.EscapePod: [DBWarp.EscapePod1],
    DBRoom.AnglerNest: [DBWarp.AnglerNest1, DBWarp.AnglerNest2],
    DBRoom.Pioneer: [],
    DBRoom.ExitOnly: [],
    DBRoom.Vessel: [],
    DBRoom.Cluster: [DBWarp.Cluster1, DBWarp.Cluster2],
    DBRoom.SmallNest: [],
}


def generate_random_db_layout(random: Random, db_option: RandomizeDarkBrambleLayout) -> str:
    # If we needed a "Dark Bramble layout" class, these would be its members:
    entrance: DBRoom
    mapped_warps: dict[DBWarp, DBRoom] = {}

    # we'll use "transit room" to mean a non-dead end; a room with at least one warp to another room
    unused_transit_rooms = [DBRoom.Hub, DBRoom.Cluster, DBRoom.EscapePod, DBRoom.AnglerNest]
    unused_dead_end_rooms = [DBRoom.Pioneer, DBRoom.ExitOnly, DBRoom.Vessel, DBRoom.SmallNest]

    unmapped_warps = []

    # Step 1: Select an entrance

    if db_option == RandomizeDarkBrambleLayout.option_hub_start:
        entrance = DBRoom.Hub
    else:
        entrance = random.choice(unused_transit_rooms)
    unused_transit_rooms.remove(entrance)

    unmapped_warps.extend(warps_in_room[entrance])

    # Step 2: Assign every room to a reachable warp
    # (transit rooms first, to guarantee we won't get stuck)

    while len(unused_transit_rooms) > 0:
        warp = random.choice(unmapped_warps)
        unmapped_warps.remove(warp)

        room = random.choice(unused_transit_rooms)
        unused_transit_rooms.remove(room)

        mapped_warps[warp] = room

        unmapped_warps.extend(warps_in_room[room])

    while len(unused_dead_end_rooms) > 0:
        warp = random.choice(unmapped_warps)
        unmapped_warps.remove(warp)

        room = random.choice(unused_dead_end_rooms)
        unused_dead_end_rooms.remove(room)

        mapped_warps[warp] = room

        unmapped_warps.extend(warps_in_room[room])

    # Step 3: Now that we've guaranteed every room is reachable,
    # randomly choose rooms for any remaining warps

    all_rooms = [r for r in DBRoom]
    for warp in unmapped_warps:
        mapped_warps[warp] = random.choice(all_rooms)

    # Step 4: Serialize our DB layout
    def serialize_room(r: DBRoom) -> str:
        room_string = room_to_letter(r) + "->"
        for w in warps_in_room[r]:
            room_string += room_to_letter(mapped_warps[w])
        return room_string

    unserialized_transit_rooms = [DBRoom.Hub, DBRoom.Cluster, DBRoom.EscapePod, DBRoom.AnglerNest]
    unserialized_transit_rooms.remove(entrance)

    room_strings = [serialize_room(entrance)]
    for room in unserialized_transit_rooms:
        room_strings.append(serialize_room(room))

    return "|".join(room_strings)
