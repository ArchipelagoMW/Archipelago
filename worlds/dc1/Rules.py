from BaseClasses import CollectionState

def xiao_available_ut(state: CollectionState, player: int) -> bool:
    return state.has("Stray Cat", player)

def xiao_available(state: CollectionState, player: int) -> bool:
    return state.has_all(["Stray Cat", "Gaffer's Lamp", "Pike"], player)

def goro_available(state: CollectionState, player: int) -> bool:
    return state.has("Matataki River H", player) and state.has("Cacao's Laundry", player) and \
        xiao_available(state, player)

# Use _only when pairing item logic with region logic
def goro_available_only(state: CollectionState, player: int) -> bool:
    return state.has("Matataki River H", player) and state.has("Cacao's Laundry", player)

def goro_available_items(state: CollectionState, player: int) -> bool:
    return (goro_available(state, player) and state.has("Fluffy Doughnut", player, 1) and
            state.has("Fish Candy", player, 1) and state.has("Fruit of Eden", player, 2) and
            state.has("Pocket", player, 1))

def ruby_available(state: CollectionState, player: int) -> bool:
    return state.has("King's Lamp", player) and goro_available(state, player)

# Use _only when pairing item logic with region logic
def ruby_available_only(state: CollectionState, player: int) -> bool:
    return state.has("King's Lamp", player)

def ruby_available_items(state: CollectionState, player: int) -> bool:
    return (ruby_available(state, player) and state.has("Fluffy Doughnut", player,2) and
            state.has("Fish Candy", player, 2) and state.has("Grass Cake", player, 1) and
            state.has("Fruit of Eden", player, 6) and state.has("Pocket", player, 2))

def ungaga_available(state: CollectionState, player: int) -> bool:
    return state.has("Sisters' Odds & Ends", player) and ruby_available(state, player)

# Use _only when pairing item logic with region logic
def ungaga_available_only(state: CollectionState, player: int) -> bool:
    return state.has("Sisters' Odds & Ends", player)

def ungaga_available_items(state: CollectionState, player: int) -> bool:
    return (ungaga_available(state, player) and state.has("Fluffy Doughnut", player,3) and
            state.has("Fish Candy", player, 3) and state.has("Grass Cake", player, 2) and
            state.has("Witch Parfait", player, 1) and state.has("Fruit of Eden", player, 10) and
            state.has("Pocket", player, 3))

def osmond_available(state: CollectionState, player: int) -> bool:
    return ungaga_available(state, player)

def osmond_available_items(state: CollectionState, player: int) -> bool:
    return (osmond_available(state, player) and state.has("Fluffy Doughnut", player,4) and
            state.has("Fish Candy", player, 4) and state.has("Grass Cake", player, 3) and
            state.has("Witch Parfait", player, 2) and state.has("Scorpion Jerky", player, 1) and
            state.has("Fruit of Eden", player, 10))

def got_accessible(state: CollectionState, player: int) -> bool:
    return osmond_available(state, player)

def got_accessible_items(state: CollectionState, player: int) -> bool:
    return osmond_available_items(state, player)

def dran_access(state: CollectionState, player: int) -> bool:
    return state.has("Dran's Sign", player)

# TODO not sure if I want logic for items on bosses.  Items for characters should be enough
# def dran_access_items(state: CollectionState, player: int) -> bool:
#     return dran_access(state, player) and state.has("Fluffy Doughnut", player, 1) and \
#         state.has("Fish Candy", player, 1) and state.has("Fruit of Eden", player, 2)

def utan_access(state: CollectionState, player: int) -> bool:
    return state.has("Mushroom Balcony", player)

# def utan_access_items(state: CollectionState, player: int) -> bool:
#     return (utan_access(state, player) and state.has("Sundew", player) and
#             state.has("Fluffy Doughnut", player, 2) and
#             state.has("Fish Candy", player, 2) and
#             state.has("Grass Cake", player, 1) and
#             state.has("Fruit of Eden", player, 5))

def saia_access(state: CollectionState, player: int) -> bool:
    return state.has("Cathedral's Holy Mark", player) and state.has("Divining House Sign", player)

# def saia_access_items(state: CollectionState, player: int) -> bool:
#     return state.has("Fluffy Doughnut", player, 3) and state.has("Fish Candy", player, 3) and \
#         state.has("Grass Cake", player, 2) and state.has("Witch Parfait", player, 1) and \
#         state.has("Fruit of Eden", player, 8)

def curse_access(state: CollectionState, player: int) -> bool:
    return state.has("Chief Bonka's Cabin 2", player) and state.has("Zabo's Hay", player) and \
        state.has("Enga's Roof", player)

# def curse_access_items(state: CollectionState, player: int) -> bool:
#     return curse_access(state, player) and state.has("Fluffy Doughnut", player, 4) and \
#         state.has("Fish Candy", player, 4) and state.has("Grass Cake", player, 3) and \
#         state.has("Witch Parfait", player, 2) and state.has("Scorpion Jerky", player, 1) and \
#         state.has("Fruit of Eden", player, 11)

def joe_access(state: CollectionState, player: int) -> bool:
    # Just need to finish the head for the admission ticket.
    return state.has("Eye (HD)", player)

# def joe_access_items(state: CollectionState, player: int) -> bool:
#     return joe_access(state, player) and state.has("Fluffy Doughnut", player, 4) and \
#         state.has("Fish Candy", player, 4) and state.has("Grass Cake", player, 3) and \
#         state.has("Witch Parfait", player, 2) and state.has("Scorpion Jerky", player, 1) and \
#         state.has("Carrot Cookie", player, 1) and state.has("Fruit of Eden", player, 14)

def genie_access(state: CollectionState, player: int) -> bool:
    return state.has_all(["Book of Curses (Departure)", "The Broken Sword (Things Lost)", "Black Blood (Demon)",
                          "Bloody Dress (Protected)", "Assassin (Assassin)", "Sophia (Dark Power)",
                          "Bloody Agreement (The Deal)", "Sophia (Menace)", "Crown (Campaign)",
                          "Buggy (Reunion)", "Sophia (Ceremony)", "Crown (Crowning Day)"], player)

#
# def genie_access_items(state: CollectionState, player: int) -> bool:
#     return genie_access(state, player) and state.has("Fluffy Doughnut", player, 5) and \
#         state.has("Fish Candy", player, 5) and state.has("Grass Cake", player, 4) and \
#         state.has("Witch Parfait", player, 3) and state.has("Scorpion Jerky", player, 2) and \
#         state.has("Carrot Cookie", player, 1) and state.has("Fruit of Eden", player, 18)

def two_bosses(state: CollectionState, player: int) -> bool:
    return utan_access(state, player) and dran_access(state, player) and goro_available(state, player)

def three_bosses(state: CollectionState, player: int) -> bool:
    return saia_access(state, player) and utan_access(state, player) and dran_access(state, player) and \
        ruby_available(state, player)

def four_bosses(state: CollectionState, player: int) -> bool:
    return curse_access(state, player) and saia_access(state, player) and utan_access(state, player) and \
        dran_access(state, player) and ungaga_available(state, player)

def five_bosses(state: CollectionState, player: int) -> bool:
    return joe_access(state, player) and curse_access(state, player) and saia_access(state, player) and \
        utan_access(state, player) and dran_access(state, player) and osmond_available(state, player)

def six_bosses(state: CollectionState, player: int) -> bool:
    return genie_access(state, player) and five_bosses(state, player)

def two_bosses_items(state: CollectionState, player: int) -> bool:
    return utan_access(state, player) and dran_access(state, player) and goro_available_items(state, player)

def three_bosses_items(state: CollectionState, player: int) -> bool:
    return saia_access(state, player) and utan_access(state, player) and dran_access(state, player) and \
        ruby_available_items(state, player)

def four_bosses_items(state: CollectionState, player: int) -> bool:
    return curse_access(state, player) and saia_access(state, player) and utan_access(state, player) and \
        dran_access(state, player) and ungaga_available_items(state, player)

def five_bosses_items(state: CollectionState, player: int) -> bool:
    return joe_access(state, player) and curse_access(state, player) and saia_access(state, player) and \
        utan_access(state, player) and dran_access(state, player) and osmond_available_items(state, player)

def six_bosses_items(state: CollectionState, player: int) -> bool:
    return genie_access(state, player) and five_bosses_items(state, player)

#
# def two_bosses_items(state: CollectionState, player: int) -> bool:
#     return utan_access_items(state, player) and dran_access_items(state, player)
#
# def three_bosses_items(state: CollectionState, player: int) -> bool:
#     return saia_access_items(state, player) and two_bosses_items(state, player)
#
# def four_bosses_items(state: CollectionState, player: int) -> bool:
#     return curse_access_items(state, player) and three_bosses_items(state, player)
#
# def five_bosses_items(state: CollectionState, player: int) -> bool:
#     return joe_access_items(state, player) and four_bosses_items(state, player)
#
# def six_bosses_items(state: CollectionState, player: int) -> bool:
#     return genie_access_items(state, player) and five_bosses_items(state, player)

def chest_test(state: CollectionState, player: int, character: str = None, geo: list[str] = None) -> bool:
    r = True

    if geo:
        for g in geo:
            r = state.has(g, player)
            if not r:
                break

    # Use _only methods when pairing item logic with region logic. Those methods don't account for items since
    # MCs aren't dangerous to get
    if r and character:
        if character == "xiao":
            r = xiao_available(state, player)
        elif character == "goro":
            r = goro_available_only(state, player)
        elif character == "ruby":
            r = ruby_available_only(state, player)
        elif character == "ungaga":
            r = ungaga_available_only(state, player)
        # Osmond is redundant with the region check currently since only Ungaga's checks are required (at least for now?)
        # elif character == "osmond":
        #     r = osmond_available(state, player)

    return r
