from worlds.adventure import get_num_items
from worlds.generic.Rules import add_rule, set_rule, forbid_item
from BaseClasses import LocationProgressType


def set_rules(self) -> None:
    world = self.multiworld
    set_rule(world.get_entrance("YellowCastlePort", self.player),
             lambda state: state.has("Yellow Key", self.player))
    set_rule(world.get_entrance("BlackCastlePort", self.player),
             lambda state: state.has("Black Key", self.player))
    set_rule(world.get_entrance("WhiteCastlePort", self.player),
             lambda state: state.has("White Key", self.player))
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
                           state.has("Black Key", self.player))

    set_rule(world.get_entrance("CreditsToFarSide", self.player),
             lambda state: state.has("Magnet", self.player))

    # bridge literally does not fit in this space, I think
    # and if the magnet is in there, you're not getting it with the bridge!
    forbid_item(world.get_location("Dungeon Vault", self.player), "Bridge", self.player)
    forbid_item(world.get_location("Dungeon Vault", self.player), "Magnet", self.player)
    forbid_item(world.get_location("Inside Yellow Castle", self.player), "Chalice", self.player)
    overworld = world.get_region("Overworld", self.player)
    white_castle_region = world.get_region("WhiteCastle", self.player)
    black_castle_region = world.get_region("WhiteCastle", self.player)
    for loc in overworld.locations:
        forbid_item(loc, "Chalice", self.player)

    add_rule(world.get_location("Chalice Home", self.player),
                   lambda state: state.has("Chalice", self.player) and state.has("Yellow Key", self.player))

    # world.random.choice(overworld.locations).progress_type = LocationProgressType.PRIORITY

    # all_locations = world.get_locations(self.player).copy()
    # while priority_count < get_num_items():
    #    loc = world.random.choice(all_locations)
    #    if loc.progress_type == LocationProgressType.DEFAULT:
    #        loc.progress_type = LocationProgressType.PRIORITY
    #        priority_count += 1
    #    all_locations.remove(loc)

    # TODO: Add events for dragon_slay_check and trap_bat_check.  Here?  Elsewhere?
    # if self.dragon_slay_check == 1:
    # TODO - Randomize bat and dragon start rooms and use those to determine rules
    # TODO - for the requirements for the slay event (since we have to get to the
    # TODO - dragons and sword to kill them).  Unless the dragons are set to be items,
    # TODO - which might be a funny option, then they can just be randoed like normal
    # TODO - just forbidden from the vaults and all credits room locations
