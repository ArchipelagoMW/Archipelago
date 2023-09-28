from BaseClasses import Region, Entrance, ItemClassification
from worlds.AutoWorld import World
from .static_logic import StaticLingoLogic, Room, RoomEntrance
from .locations import LingoLocation
from .player_logic import LingoPlayerLogic
from .rules import make_location_lambda
from worlds.generic.Rules import set_rule
from .items import LingoItem


def create_region(room: Room, world: World, player_logic: LingoPlayerLogic):
    new_region = Region(room.name, world.player, world.multiworld)

    if room.name in player_logic.LOCATIONS_BY_ROOM.keys():
        for location in player_logic.LOCATIONS_BY_ROOM[room.name]:
            new_loc = LingoLocation(world.player, location.name, location.code, new_region)
            set_rule(new_loc, make_location_lambda(location, room.name, world, player_logic))

            if location.name in player_logic.EVENT_LOC_TO_ITEM:
                event_item = LingoItem(player_logic.EVENT_LOC_TO_ITEM[location.name], ItemClassification.progression,
                                       None, player=world.player)
                new_loc.place_locked_item(event_item)

            new_region.locations.append(new_loc)

    world.multiworld.regions.append(new_region)


def connect(target: Room, entrance: RoomEntrance, world: World, player_logic: LingoPlayerLogic):
    target_region = world.multiworld.get_region(target.name, world.player)
    source_region = world.multiworld.get_region(entrance.room, world.player)
    connection = Entrance(world.player, f"{entrance.room} to {target.name}", source_region)
    connection.access_rule = lambda state: state.lingo_can_use_entrance(
        target.name, entrance.door, world.player, player_logic)

    source_region.exits.append(connection)
    connection.connect(target_region)


def handle_pilgrim_room(world: World, player_logic: LingoPlayerLogic):
    target_region = world.multiworld.get_region("Pilgrim Antechamber", world.player)
    source_region = world.multiworld.get_region("Outside The Agreeable", world.player)
    connection = Entrance(world.player, f"Pilgrimage", source_region)
    connection.access_rule = lambda state: state.lingo_can_use_pilgrimage(
        world.player, player_logic)

    source_region.exits.append(connection)
    connection.connect(target_region)


def connect_painting(warp_enter: str, warp_exit: str, world: World, static_logic: StaticLingoLogic,
                     player_logic: LingoPlayerLogic):
    source_painting = static_logic.PAINTINGS[warp_enter]
    target_painting = static_logic.PAINTINGS[warp_exit]

    target_region = world.multiworld.get_region(target_painting.room, world.player)
    source_region = world.multiworld.get_region(source_painting.room, world.player)
    connection = Entrance(world.player, f"{source_painting.room} to {target_painting.room} (Painting)", source_region)
    connection.access_rule = lambda state: state.lingo_can_use_entrance(
        target_painting.room, source_painting.required_door, world.player, player_logic)

    source_region.exits.append(connection)
    connection.connect(target_region)


def create_regions(world: World, static_logic: StaticLingoLogic, player_logic: LingoPlayerLogic):
    world.multiworld.regions += [
        Region("Menu", world.player, world.multiworld)
    ]

    for room in static_logic.ALL_ROOMS:
        create_region(room, world, player_logic)

    painting_shuffle = bool(getattr(world.multiworld, "shuffle_paintings")[world.player])

    for room in static_logic.ALL_ROOMS:
        for entrance in room.entrances:
            if entrance.painting and painting_shuffle:
                # Don't use the vanilla painting connections if we are shuffling paintings.
                continue

            connect(room, entrance, world, player_logic)

    handle_pilgrim_room(world, player_logic)

    if painting_shuffle:
        for warp_enter, warp_exit in player_logic.PAINTING_MAPPING.items():
            connect_painting(warp_enter, warp_exit, world, static_logic, player_logic)
