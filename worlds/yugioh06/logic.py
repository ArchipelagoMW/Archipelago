from BaseClasses import CollectionState


def yugioh06_difficulty(world, state: CollectionState, player: int, level: int):
    total_beaters = len(world.progression_cards["Beaters"])
    total_monster_removal = len(world.progression_cards["Monster Removal"])
    total_backrow_removal = len(world.progression_cards["Backrow Removal"])
    if level <= 0:
        return True
    elif level == 1:
        return state.has_from_list_unique(world.progression_cards["Beaters"], player,
                                          int(total_beaters / 3),) and \
            state.has_from_list_unique(world.progression_cards["Monster Removal"], player,
                                       int(total_monster_removal / 3)) and \
            state.has_from_list_unique(world.progression_cards["Backrow Removal"], player,
                                       int(total_backrow_removal / 3))
    elif level == 2:
        return state.has_from_list_unique(world.progression_cards["Beaters"], player,
                                          int(total_beaters * 2 / 3), ) and \
            state.has_from_list_unique(world.progression_cards["Monster Removal"], player,
                                       int(total_monster_removal * 2 / 3)) and \
            state.has_from_list_unique(world.progression_cards["Backrow Removal"], player,
                                       int(total_backrow_removal * 2 / 3))
    elif level >= 3:
        return state.has_all(world.progression_cards["Beaters"], player) and \
            state.has_all(world.progression_cards["Monster Removal"], player) and \
            state.has_all(world.progression_cards["Backrow Removal"], player)
