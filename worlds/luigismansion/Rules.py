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
    return state.has("Fire Element Medal", player) and (state.can_reach("1F Hallway", "Region", player) or
                                                        state.can_reach("Study", "Region", player) or
                                                        state.can_reach("Butler's Room", "Region", player) or
                                                        state.can_reach("Cold Storage", "Region", player) or
                                                        state.can_reach("Mirror Room", "Region", player) or
                                                        state.can_reach("Dining Room", "Region", player) or
                                                        state.can_reach("2F Rear Hallway", "Region", player) or
                                                        state.can_reach("Sitting Room", "Region", player) or
                                                        state.can_reach("Graveyard", "Region", player) or
                                                        state.can_reach("Roof", "Region", player))


def can_fst_water(state, player):
    return state.has("Water Element Medal", player) and (state.can_reach("Kitchen", "Region", player) or
                                                         state.can_reach("Boneyard", "Region", player) or
                                                         state.can_reach("Courtyard", "Region", player) or
                                                         state.can_reach("1F Bathroom", "Region", player) or
                                                         state.can_reach("2F Washroom", "Region", player) or
                                                         state.can_reach("Sitting Room", "Region", player))


def can_fst_ice(state, player):
    return state.has("Ice Element Medal", player) and (state.can_reach("Kitchen", "Region", player) or
                                                       state.can_reach("Pipe Room", "Region", player) or
                                                       state.can_reach("Tea Room", "Region", player) or
                                                       state.can_reach("Ceramics Studio", "Region", player))

