from typing import TYPE_CHECKING

from BaseClasses import CollectionState, Item, MultiWorld
from worlds.generic.Rules import add_rule, set_rule, CollectionRule
from worlds.AutoWorld import LogicMixin
from . import locations, items, regions, game_data, options

if TYPE_CHECKING:
    from . import MkddWorld


class MkddRules:
    def __init__(self, world: "MkddWorld") -> None:
        self.player = world.player
        self.world = world
    
    def set_loc_rule(self, location_name: str, rule: CollectionRule) -> None:
        location = self.world.multiworld.get_location(location_name, self.player)
        set_rule(location, rule)

    def add_loc_rule(self, location_name: str, rule: CollectionRule, combine: str = "and") -> None:
        location = self.world.multiworld.get_location(location_name, self.player)
        add_rule(location, rule, combine)

    def set_ent_rule(self, entrance_name: str, rule: CollectionRule) -> None:
        if not entrance_name in self.world.current_entrances:
            return
        entrance = self.world.multiworld.get_entrance(entrance_name, self.player)
        set_rule(entrance, rule)

    def set_rules(self) -> None:
        for location in self.world.current_locations:
            if len(location.required_items) > 0:
                self.add_loc_rule(location.name,
                        lambda state, items = location.required_items: state.has_all_counts(items, self.player))
            if locations.TAG_TT in location.tags:
                self.add_loc_rule(location.name,
                        lambda state, difficulty = location.difficulty:
                            calculate_player_level(state, self.player, kart_only = True) + 
                            self.world.options.logic_difficulty +
                            state.count(items.PROGRESSIVE_TIME_TRIAL_ITEM, self.player) * 4 >= difficulty)
            elif location.difficulty > 0:
                required_items_data = [items.data_table[items.name_to_id[item]] for item in location.required_items]
                req_characters = [game_data.CHARACTERS[item.address] for item in required_items_data if item.item_type == items.ItemType.CHARACTER]
                req_karts = [game_data.KARTS[item.address] for item in required_items_data if item.item_type == items.ItemType.KART]
                character_1 = req_characters[0] if len(req_characters) > 0 else None
                character_2 = req_characters[1] if len(req_characters) > 1 else None
                kart = req_karts[0] if len(req_karts) > 0 else None
                self.add_loc_rule(location.name,
                        lambda state, difficulty = location.difficulty, 
                        kart = kart, character_1 = character_1, character_2 = character_2:
                            calculate_player_level(state, self.player, kart, character_1, character_2) +
                            self.world.options.logic_difficulty >= difficulty)
 
        for cup in game_data.CUPS:
            self.set_ent_rule(f"Menu -> {cup}",
                    lambda state, cup = cup: state.has(cup, self.player))
        
        self.set_loc_rule(locations.TROPHY_GOAL,
                lambda state: state.has(items.TROPHY, self.player, self.world.options.trophy_requirement))

        for course in game_data.RACE_COURSES:
            self.set_ent_rule(f"Menu -> {course.name} TT",
                    lambda state, course = course.name: state.has(f"{course} Time Trial", self.player))

        self.add_loc_rule(locations.GOLD_LIGHT,
            lambda state: calculate_player_level(state, self.player, 0) + self.world.options.logic_difficulty >= 50)
        self.add_loc_rule(locations.GOLD_MEDIUM,
            lambda state: calculate_player_level(state, self.player, 1) + self.world.options.logic_difficulty >= 50)
        self.add_loc_rule(locations.GOLD_HEAVY,
            lambda state: calculate_player_level(state, self.player, 2) + self.world.options.logic_difficulty >= 50)


class MkddState(LogicMixin):
    mkdd_kart_levels: dict[int, list[int]]
    mkdd_unlocked_karts: dict[int, list[int]]
    mkdd_character_levels: dict[int, list[int]]
    mkdd_unlocked_characters: dict[int, list[int]]
    mkdd_best_combo_level: dict[int, int]
    mkdd_state_is_stale: dict[int, bool]

    def init_mixin(self, multiworld: MultiWorld) -> None:
        self.mkdd_kart_levels = {}
        self.mkdd_unlocked_karts = {}
        self.mkdd_character_levels = {}
        self.mkdd_unlocked_characters = {}
        self.mkdd_best_combo_level = {}
        self.mkdd_state_is_stale = {}
        for player in multiworld.get_game_players("Mario Kart Double Dash"):
            self.mkdd_kart_levels[player] = [0] * len(game_data.KARTS)
            self.mkdd_unlocked_karts[player] = [0] * len(game_data.KARTS)
            self.mkdd_character_levels[player] = [0] * len(game_data.CHARACTERS)
            self.mkdd_unlocked_characters[player] = [0] * len(game_data.CHARACTERS)
            self.mkdd_best_combo_level[player] = 0
            self.mkdd_state_is_stale[player] = False
    
    def copy_mixin(self, new_state: CollectionState) -> CollectionState:
        new_state.mkdd_kart_levels = {}
        new_state.mkdd_unlocked_karts = {}
        new_state.mkdd_character_levels = {}
        new_state.mkdd_unlocked_characters = {}
        new_state.mkdd_best_combo_level = {}
        for player in self.mkdd_kart_levels.keys():
            new_state.mkdd_kart_levels[player] = self.mkdd_kart_levels[player].copy()
            new_state.mkdd_unlocked_karts[player] = self.mkdd_unlocked_karts[player].copy()
            new_state.mkdd_character_levels[player] = self.mkdd_character_levels[player].copy()
            new_state.mkdd_unlocked_characters[player] = self.mkdd_unlocked_characters[player].copy()
            new_state.mkdd_best_combo_level[player] = self.mkdd_best_combo_level[player]
            new_state.mkdd_state_is_stale[player] = self.mkdd_state_is_stale[player]
        return new_state


def add_item(state: CollectionState, player: int, item: Item, count: int = 1) -> None:
    item_data = items.data_table[items.name_to_id[item.name]]
    if item_data.item_type == items.ItemType.KART:
        state.mkdd_unlocked_karts[player][item_data.address] += count
    elif item_data.item_type == items.ItemType.CHARACTER:
        state.mkdd_unlocked_characters[player][item_data.address] += count
    elif item_data.item_type == items.ItemType.KART_UPGRADE:
        state.mkdd_kart_levels[player][item_data.address] += item_data.meta.usefulness * count
    elif item_data.item_type == items.ItemType.ITEM_UNLOCK:
        item_value = item_data.meta["item"].usefulness
        if item_data.meta["character"] == None:
            for i in range(len(game_data.CHARACTERS)):
                state.mkdd_character_levels[player][i] += item_value * count
        else:
            char_id = game_data.CHARACTERS.index(item_data.meta["character"])
            state.mkdd_character_levels[player][char_id] += item_value * count
    elif item_data.name == items.PROGRESSIVE_ENGINE:
        state.mkdd_best_combo_level[player] += game_data.ENGINE_UPGRADE_USEFULNESS * count
        # Engine upgrade applies to all combos equally so no need to recalculate.
        return
    elif item_data.name == items.SKIP_DIFFICULTY:
        # Used for Universal Tracker glitched logic.
        state.mkdd_best_combo_level[player] += game_data.SKIP_DIFFICULTY_USEFULNESS * count
        return
    else:
        return
    state.mkdd_state_is_stale[player] = True


def calculate_player_level(state: CollectionState, player: int,
                            kart: game_data.Kart|int|None = None,
                            character_1: game_data.Character|None = None,
                            character_2: game_data.Character|None = None,
                            *, recalculate: bool = False, iterative_characters: bool = False, kart_only: bool = False) -> int:
    """
    Evaluate the best possible combination the player has with given constraints.

    :param kart: Restrict the search to a certain kart or weight class (0-2).
    :param character_1: Restrict the search to a certain character.
    :param character_2: Restrict the search to a certain character.
    """
    # First try to fetch precalculated result.
    # Only unrestricted selection is cached as it's the most taxing to calculate and most often needed.
    if kart == None and character_1 == None and character_2 == None and not kart_only and not recalculate:
        if state.mkdd_state_is_stale[player]:
            state.mkdd_best_combo_level[player] = calculate_player_level(state, player, recalculate = True)
            state.mkdd_state_is_stale[player] = False
        return state.mkdd_best_combo_level[player]
    
    # This is a recursive algorithm which optimizes the characters + kart combo by selecting each one in order
    # and trying all the combatible alternatives and taking max amount on each iteration.
    if kart == None:
        # If no characters are predetermined then the weight class can be anything.
        min_weight = 0
        max_weight = 2
        # If both characters are predetermined then the weight class is also predetermined.
        if character_1 != None and character_2 != None:
            min_weight = max(character_1.weight, character_2.weight)
            max_weight = min_weight
        # If only one character is predetermined then minimum weight is predetermined, but it can be heavier.
        elif character_1 != None:
            min_weight = max(min_weight, character_1.weight)
        elif character_2 != None:
            min_weight = max(min_weight, character_2.weight)
        return max([
            calculate_player_level(state, player, weight, character_1, character_2, iterative_characters = True, kart_only = kart_only) for weight in range(min_weight, max_weight + 1)
        ])
    
    # Kart's weight class is determined, check each kart individually (don't forget to include Parade Kart, weight -1).
    # TODO: Calculate first the best kart in its class and then only the characters!
    if kart == 0 or kart == 1 or kart == 2 or kart == -1:
        karts = [kart2 for kart2 in game_data.KARTS if kart2.weight == kart]
        if iterative_characters:
            karts += [kart2 for kart2 in game_data.KARTS if kart2.weight == -1]
        best_kart: game_data.Kart = None
        best_points: int = -1000
        for k in karts:
            if not state.mkdd_unlocked_karts[player][k.id]:
                continue
            if state.mkdd_kart_levels[player][k.id] > best_points:
                best_kart = k
                best_points = state.mkdd_kart_levels[player][k.id]
        if best_kart == None:
            return -1000
        if kart_only:
            return (
                best_points + 
                state.count(items.PROGRESSIVE_ENGINE, player) * game_data.ENGINE_UPGRADE_USEFULNESS +
                state.count(items.SKIP_DIFFICULTY, player) * game_data.SKIP_DIFFICULTY_USEFULNESS
            )
        else:
            return calculate_player_level(state, player, best_kart, character_1, character_2)
    
    # Try to pick characters which can fit in the correct vehicle. The first character will determine the weight.
    if character_1 == None:
        characters = [character for character in game_data.CHARACTERS if character.weight == kart.weight or kart.weight == -1]
        return max([
            calculate_player_level(state, player, kart, character, None, iterative_characters = True) for character in characters
        ])

    # The second character can be lighter than the first.
    if character_2 == None:
        if iterative_characters:
            # Don't check further than the first character as those combos will be checked by parent function.
            characters = [
                character for character in game_data.CHARACTERS if (
                    character.weight < character_1.weight or 
                    (character.weight == character_1.weight and character.id < character_1.id)
                )
            ]
        else:
            # The character_1 was predetermined by caller, so check all possibilities.
            characters = [
                character for character in game_data.CHARACTERS if (
                    (character.weight <= kart.weight or kart.weight == -1) and
                    character.id != character_1.id
                )
            ]
        if len(characters) == 0:
            return -1000
        return max([
            calculate_player_level(state, player, kart, character_1, character) for character in characters
        ])
    
    if (not state.mkdd_unlocked_karts[player][kart.id] or
        not state.mkdd_unlocked_characters[player][character_1.id] or
        not state.mkdd_unlocked_characters[player][character_2.id]):
        return -1000
    return (
        state.mkdd_kart_levels[player][kart.id] +
        state.mkdd_character_levels[player][character_1.id] +
        state.mkdd_character_levels[player][character_2.id] +
        state.count(items.PROGRESSIVE_ENGINE, player) * game_data.ENGINE_UPGRADE_USEFULNESS +
        state.count(items.SKIP_DIFFICULTY, player) * game_data.SKIP_DIFFICULTY_USEFULNESS
    )