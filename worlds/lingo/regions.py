from BaseClasses import Region, Entrance, ItemClassification
from worlds.AutoWorld import World
from worlds.generic.Rules import set_rule

from .items import LingoItem
from .locations import LingoLocation
from .player_logic import LingoPlayerLogic
from .rules import make_location_lambda
from .static_logic import Room, RoomEntrance, PAINTINGS, ALL_ROOMS


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

    source_region.connect(target_region, f"{entrance.room} to {target.name}",
                          lambda state: state.lingo_can_use_entrance(target.name, entrance.door, world.player,
                                                                     player_logic))


def handle_pilgrim_room(world: World, player_logic: LingoPlayerLogic):
    target_region = world.multiworld.get_region("Pilgrim Antechamber", world.player)
    source_region = world.multiworld.get_region("Outside The Agreeable", world.player)

    source_region.connect(target_region, "Pilgrimage", lambda state: state.lingo_can_use_pilgrimage(world.player,
                                                                                                    player_logic))


def connect_painting(warp_enter: str, warp_exit: str, world: World, player_logic: LingoPlayerLogic):
    source_painting = PAINTINGS[warp_enter]
    target_painting = PAINTINGS[warp_exit]

    target_region = world.multiworld.get_region(target_painting.room, world.player)
    source_region = world.multiworld.get_region(source_painting.room, world.player)

    source_region.connect(target_region, f"{source_painting.room} to {target_painting.room} (Painting)",
                          lambda state: state.lingo_can_use_entrance(target_painting.room,
                                                                     source_painting.required_door, world.player,
                                                                     player_logic))


def create_regions(world: World, player_logic: LingoPlayerLogic):
    world.multiworld.regions += [
        Region("Menu", world.player, world.multiworld)
    ]

    for room in ALL_ROOMS:
        create_region(room, world, player_logic)

    painting_shuffle = bool(getattr(world.multiworld, "shuffle_paintings")[world.player])
    early_color_hallways = bool(getattr(world.multiworld, "early_color_hallways")[world.player])

    for room in ALL_ROOMS:
        for entrance in room.entrances:
            if entrance.painting and painting_shuffle:
                # Don't use the vanilla painting connections if we are shuffling paintings.
                continue

            connect(room, entrance, world, player_logic)

    handle_pilgrim_room(world, player_logic)

    if early_color_hallways:
        world.multiworld.get_region("Starting Room", world.player)\
            .connect(world.multiworld.get_region("Outside The Undeterred", world.player), "Early Color Hallways")

    if painting_shuffle:
        for warp_enter, warp_exit in player_logic.PAINTING_MAPPING.items():
            connect_painting(warp_enter, warp_exit, world, player_logic)
