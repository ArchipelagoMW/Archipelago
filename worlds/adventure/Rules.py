from .Options import BatLogic, DifficultySwitchB
from worlds.generic.Rules import add_rule, set_rule, forbid_item


def set_rules(self) -> None:
    world = self.multiworld
    use_bat_logic = self.options.bat_logic.value == BatLogic.option_use_logic

    set_rule(world.get_entrance("YellowCastlePort", self.player),
             lambda state: state.has("Yellow Key", self.player))
    set_rule(world.get_entrance("BlackCastlePort", self.player),
             lambda state: state.has("Black Key", self.player))
    set_rule(world.get_entrance("WhiteCastlePort", self.player),
             lambda state: state.has("White Key", self.player))

    # a future thing would be to make the bat an actual item, or at least allow it to
    # be placed in a castle, which would require some additions to the rules when
    # use_bat_logic is true
    if not use_bat_logic:
        set_rule(world.get_entrance("WhiteCastleSecretPassage", self.player),
                 lambda state: state.has("Bridge", self.player))
        set_rule(world.get_entrance("WhiteCastlePeekPassage", self.player),
                 lambda state: state.has("Bridge", self.player) or
                               state.has("Magnet", self.player))
        set_rule(world.get_entrance("BlackCastleVaultEntrance", self.player),
                 lambda state: state.has("Bridge", self.player) or
                               state.has("Magnet", self.player))

    dragon_slay_check = self.options.dragon_slay_check.value
    if dragon_slay_check:
        if self.difficulty_switch_b == DifficultySwitchB.option_hard_with_unlock_item:
            set_rule(world.get_location("Slay Yorgle", self.player),
                     lambda state: state.has("Sword", self.player) and
                                   state.has("Right Difficulty Switch", self.player))
            set_rule(world.get_location("Slay Grundle", self.player),
                     lambda state: state.has("Sword", self.player) and
                                   state.has("Right Difficulty Switch", self.player))
            set_rule(world.get_location("Slay Rhindle", self.player),
                     lambda state: state.has("Sword", self.player) and
                                   state.has("Right Difficulty Switch", self.player))
        else:
            set_rule(world.get_location("Slay Yorgle", self.player),
                     lambda state: state.has("Sword", self.player))
            set_rule(world.get_location("Slay Grundle", self.player),
                     lambda state: state.has("Sword", self.player))
            set_rule(world.get_location("Slay Rhindle", self.player),
                     lambda state: state.has("Sword", self.player))

    # really this requires getting the dot item, and having another item or enemy
    # in the room, but the dot would be *super evil*
    # to actually make randomized, since it is invisible.  May add some options
    # for how that works in the distant future, but for now, just say you need
    # the bridge and black key to get to it, as that simplifies things a lot
    set_rule(world.get_entrance("CreditsWall", self.player),
             lambda state: state.has("Bridge", self.player) and
                           state.has("Black Key", self.player))

    if not use_bat_logic:
        set_rule(world.get_entrance("CreditsToFarSide", self.player),
                 lambda state: state.has("Magnet", self.player))

    # bridge literally does not fit in this space, I think.  I'll just exclude it
    forbid_item(world.get_location("Dungeon Vault", self.player), "Bridge", self.player)
    # don't put magnet in locations that can pull in-logic items out of reach unless the bat is in play
    if not use_bat_logic:
        forbid_item(world.get_location("Dungeon Vault", self.player), "Magnet", self.player)
        forbid_item(world.get_location("Red Maze Vault Entrance", self.player), "Magnet", self.player)
        forbid_item(world.get_location("Credits Right Side", self.player), "Magnet", self.player)

    # and obviously we don't want to start with the game already won
    forbid_item(world.get_location("Inside Yellow Castle", self.player), "Chalice", self.player)
    overworld = world.get_region("Overworld", self.player)

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
