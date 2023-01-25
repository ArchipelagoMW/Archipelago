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

    for name, location_data in location_table.items():
        r = multiworld.get_region(location_data.region, player)
        r.locations.append(AdventureLocation(player, location_data.name, location_data.location_id, r))

    # in the future, I will randomize the map some, and that will require moving
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