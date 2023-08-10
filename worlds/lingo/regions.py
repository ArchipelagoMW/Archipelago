from BaseClasses import MultiWorld, Region, Entrance, ItemClassification
from .static_logic import StaticLingoLogic, Room, RoomEntrance
from .locations import LingoLocation
from .player_logic import LingoPlayerLogic
from .rules import make_location_lambda
from worlds.generic.Rules import set_rule
from .items import LingoItem


def create_region(room: Room, multiworld: MultiWorld, player: int, player_logic: LingoPlayerLogic):
    new_region = Region(room.name, player, multiworld)

    if room.name in player_logic.LOCATIONS_BY_ROOM.keys():
        for location in player_logic.LOCATIONS_BY_ROOM[room.name]:
            new_loc = LingoLocation(player, location.name, location.code, new_region)
            set_rule(new_loc, make_location_lambda(location, room.name, multiworld, player, player_logic))

            if location.name in player_logic.EVENT_LOC_TO_ITEM:
                event_item = LingoItem(player_logic.EVENT_LOC_TO_ITEM[location.name], ItemClassification.progression,
                                       None, player=player)
                new_loc.place_locked_item(event_item)

            new_region.locations.append(new_loc)

    multiworld.regions.append(new_region)


def connect(target: Room, entrance: RoomEntrance, multiworld: MultiWorld, player: int, player_logic: LingoPlayerLogic):
    target_region = multiworld.get_region(target.name, player)
    source_region = multiworld.get_region(entrance.room, player)
    connection = Entrance(player, f"{entrance.room} to {target.name}", source_region)
    connection.access_rule = lambda state: state.lingo_can_use_entrance(
        target.name, entrance.door, player, player_logic)

    source_region.exits.append(connection)
    connection.connect(target_region)


def handle_pilgrim_room(multiworld: MultiWorld, player: int, player_logic: LingoPlayerLogic):
    target_region = multiworld.get_region("Pilgrim Antechamber", player)
    source_region = multiworld.get_region("Outside The Agreeable", player)
    connection = Entrance(player, f"Pilgrimage", source_region)
    connection.access_rule = lambda state: state.lingo_can_use_pilgrimage(
        player, player_logic)

    source_region.exits.append(connection)
    connection.connect(target_region)


def connect_painting(warp_enter: str, warp_exit: str, multiworld: MultiWorld, player: int,
                     static_logic: StaticLingoLogic, player_logic: LingoPlayerLogic):
    source_painting = static_logic.PAINTINGS[warp_enter]
    target_painting = static_logic.PAINTINGS[warp_exit]

    target_region = multiworld.get_region(target_painting.room, player)
    source_region = multiworld.get_region(source_painting.room, player)
    connection = Entrance(player, f"{source_painting.room} to {target_painting.room} (Painting)", source_region)
    connection.access_rule = lambda state: state.lingo_can_use_entrance(
        target_painting.room, source_painting.required_door, player, player_logic)

    source_region.exits.append(connection)
    connection.connect(target_region)


def create_regions(multiworld: MultiWorld, player: int, static_logic: StaticLingoLogic, player_logic: LingoPlayerLogic):
    multiworld.regions += [
        Region("Menu", player, multiworld)
    ]

    for room in static_logic.ALL_ROOMS:
        create_region(room, multiworld, player, player_logic)

    painting_shuffle = bool(getattr(multiworld, "shuffle_paintings")[player])

    for room in static_logic.ALL_ROOMS:
        for entrance in room.entrances:
            if entrance.painting and painting_shuffle:
                # Don't use the vanilla painting connections if we are shuffling paintings.
                continue

            connect(room, entrance, multiworld, player, player_logic)

    handle_pilgrim_room(multiworld, player, player_logic)

    if painting_shuffle:
        for warp_enter, warp_exit in player_logic.PAINTING_MAPPING.items():
            connect_painting(warp_enter, warp_exit, multiworld, player, static_logic, player_logic)
