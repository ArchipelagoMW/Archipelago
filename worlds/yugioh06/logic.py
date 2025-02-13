from BaseClasses import CollectionState
from worlds.AutoWorld import World


def yugioh06_difficulty(world, state: CollectionState, player: int, level: int):
    total_beaters = len(world.progression_cards["Beaters"])
    total_monster_removal = len(world.progression_cards["Monster Removal"])
    total_backrow_removal = len(world.progression_cards["Backrow Removal"])
    if level <= 0:
        return True
    elif level == 1:
        return (state.has_from_list_unique(world.progression_cards["Beaters"], player,
                                           total_beaters // 3, ) and
                state.has_from_list_unique(world.progression_cards["Monster Removal"], player,
                                           total_monster_removal // 3) and
                state.has_from_list_unique(world.progression_cards["Backrow Removal"], player,
                                           total_backrow_removal // 3))
    elif level == 2:
        return (state.has_from_list_unique(world.progression_cards["Beaters"], player,
                                           total_beaters * 2 // 3, ) and
                state.has_from_list_unique(world.progression_cards["Monster Removal"], player,
                                           total_monster_removal * 2 // 3) and
                state.has_from_list_unique(world.progression_cards["Backrow Removal"], player,
                                           total_backrow_removal * 2 // 3))
    elif level >= 3:
        return (state.has_all(world.progression_cards["Beaters"], player) and
                state.has_all(world.progression_cards["Monster Removal"], player) and
                state.has_all(world.progression_cards["Backrow Removal"], player))


def get_cards_in_first_pack(world: World, criteria: str):
    cards_of_criteria = list(world.progression_cards[criteria])
    min_cards = len(cards_of_criteria) // 3
    cards_in_start = [c for c in world.progression_cards_in_start if c in cards_of_criteria]
    cards_in_first_pack = []
    if min_cards > len(cards_in_start):
        # filter starting cards
        cards_of_criteria = [c for c in cards_of_criteria if c not in cards_in_start]
        world.random.shuffle(cards_of_criteria)
        for i in range(0, min_cards - len(cards_in_start)):
            cards_in_first_pack.append(cards_of_criteria[i])
    return cards_in_first_pack
