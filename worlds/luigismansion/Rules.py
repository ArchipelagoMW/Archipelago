from BaseClasses import CollectionState


FIRE_SPIRIT_SPOT = ("1F Hallway",
                    "Study",
                    "Butler's Room",
                    "Cold Storage",
                    "Mirror Room",
                    "Dining Room",
                    "2F Rear Hallway",
                    "Sitting Room",
                    "Graveyard",
                    "Roof")

WATER_SPIRIT_SPOT = ("Kitchen",
                     "Boneyard",
                     "Courtyard",
                     "1F Bathroom",
                     "2F Washroom",
                     "Sitting Room")

ICE_SPIRIT_SPOT = ("Kitchen",
                   "Pipe Room",
                   "Tea Room",
                   "Ceramics Studio")


def can_fst_fire(state: CollectionState, player: int):
    return state.has("Fire Element Medal", player) and (state.can_reach_region("1F Hallway", player) or
                                                        state.can_reach_region("Study", player) or
                                                        state.can_reach_region("Butler's Room", player) or
                                                        state.can_reach_region("Cold Storage", player) or
                                                        state.can_reach_region("Mirror Room", player) or
                                                        state.can_reach_region("Dining Room", player) or
                                                        state.can_reach_region("2F Rear Hallway", player) or
                                                        state.can_reach_region("Sitting Room", player) or
                                                        state.can_reach_region("Graveyard", player) or
                                                        state.can_reach_region("Roof", player))


def can_fst_water(state, player):
    return state.has("Water Element Medal", player) and (state.can_reach_region("Kitchen", player) or
                                                         state.can_reach_region("Boneyard", player) or
                                                         state.can_reach_region("Courtyard", player) or
                                                         state.can_reach_region("1F Bathroom", player) or
                                                         state.can_reach_region("2F Washroom", player) or
                                                         state.can_reach_region("Sitting Room", player))


def can_fst_ice(state, player):
    return state.has("Ice Element Medal", player) and (state.can_reach_region("Kitchen", player) or
                                                       state.can_reach_region("Pipe Room", player) or
                                                       state.can_reach_region("Tea Room", player) or
                                                       state.can_reach_region("Ceramics Studio", player))

