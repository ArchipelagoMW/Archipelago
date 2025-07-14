from BaseClasses import MultiWorld, Region, Entrance, LocationProgressType
from Options import PerGameCommonOptions
from .Locations import location_table, AdventureLocation, dragon_room_to_region


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


def create_regions(options: PerGameCommonOptions, multiworld: MultiWorld, player: int, dragon_rooms: []) -> None:

    menu = Region("Menu", player, multiworld)

    menu.exits.append(Entrance(player, "GameStart", menu))
    multiworld.regions.append(menu)

    overworld = Region("Overworld", player, multiworld)
    overworld.exits.append(Entrance(player, "YellowCastlePort", overworld))
    overworld.exits.append(Entrance(player, "WhiteCastlePort", overworld))
    overworld.exits.append(Entrance(player, "BlackCastlePort", overworld))
    overworld.exits.append(Entrance(player, "CreditsWall", overworld))
    multiworld.regions.append(overworld)

    yellow_castle = Region("YellowCastle", player, multiworld, "Yellow Castle")
    yellow_castle.exits.append(Entrance(player, "YellowCastleExit", yellow_castle))
    multiworld.regions.append(yellow_castle)

    white_castle = Region("WhiteCastle", player, multiworld, "White Castle")
    white_castle.exits.append(Entrance(player, "WhiteCastleExit", white_castle))
    white_castle.exits.append(Entrance(player, "WhiteCastleSecretPassage", white_castle))
    white_castle.exits.append(Entrance(player, "WhiteCastlePeekPassage", white_castle))
    multiworld.regions.append(white_castle)

    white_castle_pre_vault_peek = Region("WhiteCastlePreVaultPeek", player, multiworld, "White Castle Secret Peek")
    white_castle_pre_vault_peek.exits.append(Entrance(player, "WhiteCastleFromPeek", white_castle_pre_vault_peek))
    multiworld.regions.append(white_castle_pre_vault_peek)

    white_castle_secret_room = Region("WhiteCastleVault", player, multiworld, "White Castle Vault",)
    white_castle_secret_room.exits.append(Entrance(player, "WhiteCastleReturnPassage", white_castle_secret_room))
    multiworld.regions.append(white_castle_secret_room)

    black_castle = Region("BlackCastle", player, multiworld, "Black Castle")
    black_castle.exits.append(Entrance(player, "BlackCastleExit", black_castle))
    black_castle.exits.append(Entrance(player, "BlackCastleVaultEntrance", black_castle))
    multiworld.regions.append(black_castle)

    black_castle_secret_room = Region("BlackCastleVault", player, multiworld, "Black Castle Vault")
    black_castle_secret_room.exits.append(Entrance(player, "BlackCastleReturnPassage", black_castle_secret_room))
    multiworld.regions.append(black_castle_secret_room)

    credits_room = Region("CreditsRoom", player, multiworld, "Credits Room")
    credits_room.exits.append(Entrance(player, "CreditsExit", credits_room))
    credits_room.exits.append(Entrance(player, "CreditsToFarSide", credits_room))
    multiworld.regions.append(credits_room)

    credits_room_far_side = Region("CreditsRoomFarSide", player, multiworld, "Credits Far Side")
    credits_room_far_side.exits.append(Entrance(player, "CreditsFromFarSide", credits_room_far_side))
    multiworld.regions.append(credits_room_far_side)

    dragon_slay_check = options.dragon_slay_check.value
    priority_locations = determine_priority_locations()

    for name, location_data in location_table.items():
        if location_data.region == "Varies":
            if location_data.name == "Slay Yorgle":
                if not dragon_slay_check:
                    continue
                region_name = dragon_room_to_region(dragon_rooms[0])
            elif location_data.name == "Slay Grundle":
                if not dragon_slay_check:
                    continue
                region_name = dragon_room_to_region(dragon_rooms[1])
            elif location_data.name == "Slay Rhindle":
                if not dragon_slay_check:
                    continue
                region_name = dragon_room_to_region(dragon_rooms[2])
            else:
                raise Exception(f"Unknown location region for {location_data.name}")
            r = multiworld.get_region(region_name, player)
        else:
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


# Placeholder for adding sets of priority locations at generation, possibly as an option in the future
# def determine_priority_locations(multiworld: MultiWorld, dragon_slay_check: bool) -> {}:
def determine_priority_locations() -> {}:
    priority_locations = {}
    return priority_locations
