from BaseClasses import MultiWorld, Region, Entrance, RegionType, LocationProgressType
from .Locations import location_table, LocationData, AdventureLocation


def connect(world: MultiWorld, player: int, source: str, target: str, rule: callable = lambda state: True,
            one_way=False, name=None):
    source_region = world.get_region(source, player)
    target_region = world.get_region(target, player)

    if name is None:
        name = source + " to " + target

    connection = Entrance(
        player,
        name,
        source_region
    )

    connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)
    if not one_way:
        connect(world, player, target, source, rule, True)


def create_regions(multiworld: MultiWorld, player: int) -> None:
    for name, locdata in location_table.items():
        locdata.get_position(multiworld.random)

    # TODO: I guess these names are player facing.  I should adjust them to have spaces and stuff
    # TODO: And check the names against what's in the manual, it might have some official names
    menu = Region("Menu", RegionType.Generic, "Menu", player, multiworld)

    menu.exits.append(Entrance(player, "GameStart", menu))
    multiworld.regions.append(menu)

    overworld = Region("Overworld", RegionType.Generic, "Overworld", player, multiworld)
    overworld.exits.append(Entrance(player, "YellowCastlePort", overworld))
    overworld.exits.append(Entrance(player, "WhiteCastlePort", overworld))
    overworld.exits.append(Entrance(player, "BlackCastlePort", overworld))
    overworld.exits.append(Entrance(player, "CreditsWall", overworld))
    multiworld.regions.append(overworld)

    yellow_castle = Region("YellowCastle", RegionType.Generic, "Yellow Castle", player, multiworld)
    yellow_castle.exits.append(Entrance(player, "YellowCastleExit", yellow_castle))
    multiworld.regions.append(yellow_castle)

    white_castle = Region("WhiteCastle", RegionType.Generic, "White Castle", player, multiworld)
    white_castle.exits.append(Entrance(player, "WhiteCastleExit", white_castle))
    white_castle.exits.append(Entrance(player, "WhiteCastleSecretPassage", white_castle))
    white_castle.exits.append(Entrance(player, "WhiteCastlePeekPassage", white_castle))
    multiworld.regions.append(white_castle)

    white_castle_pre_vault_peek = Region("WhiteCastlePreVaultPeek", RegionType.Generic,
                                         "White Castle Secret Peek", player, multiworld)
    white_castle_pre_vault_peek.exits.append(Entrance(player, "WhiteCastleFromPeek", white_castle_pre_vault_peek))
    multiworld.regions.append(white_castle_pre_vault_peek)

    white_castle_secret_room = Region("WhiteCastleVault", RegionType.Generic, "White Castle Vault",
                                      player, multiworld)
    white_castle_secret_room.exits.append(Entrance(player, "WhiteCastleReturnPassage", white_castle_secret_room))
    multiworld.regions.append(white_castle_secret_room)

    black_castle = Region("BlackCastle", RegionType.Generic, "Black Castle", player, multiworld)
    black_castle.exits.append(Entrance(player, "BlackCastleExit", black_castle))
    black_castle.exits.append(Entrance(player, "BlackCastleVaultEntrance", black_castle))
    multiworld.regions.append(black_castle)

    black_castle_secret_room = Region("BlackCastleVault", RegionType.Generic, "Black Castle Vault",
                                      player, multiworld)
    black_castle_secret_room.exits.append(Entrance(player, "BlackCastleReturnPassage", black_castle_secret_room))
    multiworld.regions.append(black_castle_secret_room)

    credits_room = Region("CreditsRoom", RegionType.Generic, "Credits Room", player, multiworld)
    credits_room.exits.append(Entrance(player, "CreditsExit", credits_room))
    credits_room.exits.append(Entrance(player, "CreditsToFarSide", credits_room))
    multiworld.regions.append(credits_room)

    credits_room_far_side = Region("CreditsRoomFarSide", RegionType.Generic, "Credits Far Side", player, multiworld)
    credits_room_far_side.exits.append(Entrance(player, "CreditsFromFarSide", credits_room_far_side))
    multiworld.regions.append(credits_room_far_side)

    priority_locations = determine_priority_locations(multiworld)
    for name, location_data in location_table.items():
        r = multiworld.get_region(location_data.region, player)
        adventure_loc = AdventureLocation(player, location_data.name, location_data.location_id, r)
        if adventure_loc.name in priority_locations:
            adventure_loc.progress_type = LocationProgressType.PRIORITY
        r.locations.append(adventure_loc)

    # In a tracker and plando-free world, I'd determine unused locations here and not add them.
    # But that would cause problems with both plandos and trackers.  So I guess I'll stick
    # with filling in with 'nothing' in pre_fill.

    # in the future, I may randomize the map some, and that will require moving
    # connections to later, probably

    multiworld.get_entrance("GameStart", player) \
        .connect(multiworld.get_region("Overworld", player))

    multiworld.get_entrance("YellowCastlePort", player) \
        .connect(multiworld.get_region("YellowCastle", player))
    multiworld.get_entrance("YellowCastleExit", player) \
        .connect(multiworld.get_region("Overworld", player))

    multiworld.get_entrance("WhiteCastlePort", player) \
        .connect(multiworld.get_region("WhiteCastle", player))
    multiworld.get_entrance("WhiteCastleExit", player) \
        .connect(multiworld.get_region("Overworld", player))

    multiworld.get_entrance("WhiteCastleSecretPassage", player) \
        .connect(multiworld.get_region("WhiteCastleVault", player))
    multiworld.get_entrance("WhiteCastleReturnPassage", player) \
        .connect(multiworld.get_region("WhiteCastle", player))
    multiworld.get_entrance("WhiteCastlePeekPassage", player) \
        .connect(multiworld.get_region("WhiteCastlePreVaultPeek", player))
    multiworld.get_entrance("WhiteCastleFromPeek", player) \
        .connect(multiworld.get_region("WhiteCastle", player))

    multiworld.get_entrance("BlackCastlePort", player) \
        .connect(multiworld.get_region("BlackCastle", player))
    multiworld.get_entrance("BlackCastleExit", player) \
        .connect(multiworld.get_region("Overworld", player))
    multiworld.get_entrance("BlackCastleVaultEntrance", player) \
        .connect(multiworld.get_region("BlackCastleVault", player))
    multiworld.get_entrance("BlackCastleReturnPassage", player) \
        .connect(multiworld.get_region("BlackCastle", player))

    multiworld.get_entrance("CreditsWall", player) \
        .connect(multiworld.get_region("CreditsRoom", player))
    multiworld.get_entrance("CreditsExit", player) \
        .connect(multiworld.get_region("Overworld", player))

    multiworld.get_entrance("CreditsToFarSide", player) \
        .connect(multiworld.get_region("CreditsRoomFarSide", player))
    multiworld.get_entrance("CreditsFromFarSide", player) \
        .connect(multiworld.get_region("CreditsRoom", player))


# Assign some priority locations to try to get interesting stuff into the castles, most of the time
# occasionally some interesting things are generated without that, so I want to leave some chance of
# that happening.  The downside to leaving it out is sometimes not needing to visit all castles,
# at least in solo world.
def determine_priority_locations(world: MultiWorld) -> {}:
    locations = []
    priority_locations = {}
    for name, location_data in location_table.items():
        if location_data.room_id is not None:
            locations.append(name)

    do_priority = world.random.randint(0, 4) < 3
    if not do_priority:
        return priority_locations

    priority_index = world.random.randint(0, 4)
    hard_location_score = 0
    priority_count = 0
    if priority_index == 0:
        priority_locations["Credits Right Side"] = True
        hard_location_score = 2
        priority_count += 1
    elif priority_index == 1:
        priority_locations["Credits Left Side"] = True
        hard_location_score = 2
        priority_count += 1
    priority_index = world.random.randint(hard_location_score, 7)
    if priority_index < 3:
        priority_locations["Dungeon Vault"] = True
        hard_location_score += 2
        priority_count += 1
    elif priority_index == 4:
        priority_locations["Dungeon3"] = True
        priority_count += 1
    elif priority_index == 5:
        priority_locations["Dungeon1"] = True
        priority_count += 1
    elif priority_index == 6:
        priority_locations["Dungeon0"] = True
        priority_count += 1

    priority_index = world.random.randint(0, 7)
    if priority_index < 2:
        priority_locations["RedMaze2"] = True
        priority_count += 1
    elif priority_index < 4:
        priority_locations["Red Maze Vault"] = True
        priority_count += 1
    elif priority_index == 4:
        priority_locations["RedMaze1"] = True
        priority_count += 1
    elif priority_index == 5:
        priority_locations["RedMaze0"] = True
        priority_count += 1
    else:
        priority_locations["RedMaze3"] = True
        priority_count += 1

    return priority_locations