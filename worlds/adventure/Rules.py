from worlds.generic.Rules import add_rule, set_rule, forbid_item
from BaseClasses import LocationProgressType


def set_rules(self) -> None:
    world = self.multiworld
    set_rule(world.get_entrance("YellowCastlePort", self.player),
             lambda state: state.has("YellowKey", self.player))
    set_rule(world.get_entrance("BlackCastlePort", self.player),
             lambda state: state.has("BlackKey", self.player))
    set_rule(world.get_entrance("WhiteCastlePort", self.player),
             lambda state: state.has("WhiteKey", self.player))
    set_rule(world.get_entrance("WhiteCastleSecretPassage", self.player),
             lambda state: state.has("Bridge", self.player))
    set_rule(world.get_entrance("WhiteCastlePeekPassage", self.player),
             lambda state: state.has("Bridge", self.player) or
                           state.has("Magnet", self.player))
    set_rule(world.get_entrance("BlackCastleVaultEntrance", self.player),
             lambda state: state.has("Bridge", self.player) or
                           state.has("Magnet", self.player))

    # really this requires getting the dot item, and having another item or enemy
    # in the room, but the dot would be *super evil*
    # to actually make randomized, since it is invisible.  May add some options
    # for how that works in the distant future, but for now, just say you need
    # the bridge and black key to get to it, as that simplifies things a lot
    set_rule(world.get_entrance("CreditsWall", self.player),
             lambda state: state.has("Bridge", self.player) and
                           state.has("BlackKey", self.player))

    set_rule(world.get_entrance("CreditsToFarSide", self.player),
             lambda state: state.has("Magnet", self.player))

    # bridge literally does not fit in this space, I think
    # and if the magnet is in there, you're not getting it with the bridge!
    forbid_item(world.get_location("DungeonVault", self.player), "Bridge", self.player)
    forbid_item(world.get_location("DungeonVault", self.player), "Magnet", self.player)
    overworld = world.get_region("Overworld", self.player)
    white_castle_region = world.get_region("WhiteCastle", self.player)
    black_castle_region = world.get_region("WhiteCastle", self.player)
    for loc in overworld.locations:
        forbid_item(loc, "Chalice", self.player)
    if world.random.randint(0, 1) == 0:
        for loc in overworld.locations:
            forbid_item(loc, "WhiteKey", self.player)
        for loc in black_castle_region.locations:
            forbid_item(loc, "Chalice", self.player)
    else:
        for loc in overworld.locations:
            forbid_item(loc, "BlackKey", self.player)
        for loc in white_castle_region.locations:
            forbid_item(loc, "Chalice", self.player)

    # Assign some priority locations to try to get interesting stuff into the castles
    priority_index = world.random.randint(0, 4)
    if priority_index == 0:
        world.get_location("CreditsRightSide", self.player).progress_type = LocationProgressType.PRIORITY
    elif priority_index == 1:
        world.get_location("CreditsLeftSide", self.player).progress_type = LocationProgressType.PRIORITY
    world.get_location("DungeonVault", self.player).progress_type = LocationProgressType.PRIORITY
    priority_index = world.random.randint(0, 1)
    if priority_index == 0:
        world.get_location("RedMaze2", self.player).progress_type = LocationProgressType.PRIORITY
    else:
        world.get_location("RedMaze0a", self.player).progress_type = LocationProgressType.PRIORITY

    world.random.choice(overworld.locations).progress_type = LocationProgressType.PRIORITY

    # TODO: Add events for dragon_slay_check and trap_bat_check.  Here?  Elsewhere?
    # if self.dragon_slay_check == 1:
    # TODO - Randomize bat and dragon start rooms and use those to determine rules
    # TODO - for the requirements for the slay event (since we have to get to the
    # TODO - dragons and sword to kill them).  Unless the dragons are set to be items,
    # TODO - which might be a funny option, then they can just be randoed like normal
    # TODO - just forbidden from the vaults and all credits room locations
