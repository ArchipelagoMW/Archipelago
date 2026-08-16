from collections import Counter
from typing import TYPE_CHECKING

from BaseClasses import CollectionState, MultiWorld, Region
from Utils import KeyedDefaultDict
from worlds.AutoWorld import LogicMixin

from .constants import BASE_HEALTH, BASE_NOTCHES, BASE_SOUL, NearbySoul  # noqa: F401
from .parse_data import effects_items_by_term, effects_prog_lookup, effects_terms_by_item
from .resource_state_vars import rs, rs_leq, rs_set_value

if TYPE_CHECKING:
    from . import HKClause
    from .classes import HKItem


# default_state = KeyedDefaultDict(lambda key: True if key == "NOFLOWER" else False)
class DefaultStateFactory:
    def __call__(self, defaults=None) -> rs:
        if defaults is None:
            defaults = {}
        ret = 0
        ret = rs_set_value(ret, "NOFLOWER", 1)
        ret = rs_set_value(ret, "NOPASSEDCHARMEQUIP", 1)
        for key, value in defaults.items():
            ret = rs_set_value(ret, key, value)
        return ret


default_state = DefaultStateFactory()


class HKLogicMixin(LogicMixin):
    multiworld: MultiWorld
    _hk_per_player_resource_states: dict[int, dict[str, list[rs]]]
    """resource state blob to map regions and their available resource states"""
    # state blob is an int bitfield

    _hk_per_player_sweepable_entrances: dict[int, set[str]]
    """mapping for entrances that need to be statefully swept"""

    _hk_stale: dict[int, bool]
    """TODO: make an item stale and a resource_state_stale difference"""

    _hk_free_entrances: dict[int, set[str]]
    """mapping for entrances that will not alter resource state no matter how many more items we get"""

    _hk_entrance_clause_cache: dict[int, dict[str, dict[int, bool]]]
    """mapping for clauses per entrance per player to short circuit non-resource state calculations"""

    _hk_checked_state_modifiers: dict[int, dict[str, set[str]]]
    """mapping for state modifiers per entrance per player to not try state modifiers which have already been tried"""

    _hk_processed_item_cache: dict[int, Counter]
    """cache of Item names already processes as not all of them end up in state.prog_items due to term handling"""

    _hk_charm_costs: dict[int, dict[str, int]]
    """mapping for charm costs per player"""

    _hk_soul_modes: dict[int, NearbySoul]
    """mapping of soul mode per player"""

    def init_mixin(self, multiworld: MultiWorld) -> None:
        from . import HKWorld
        players = multiworld.get_game_players(HKWorld.game)
        if not players:
            return
        self._hk_per_player_resource_states = {
            player: KeyedDefaultDict(lambda region: [default_state()] if region == "Menu" else [])
            for player in players
            }  # {player: {init_state: [start_region]} for player in players}
        self._hk_per_player_sweepable_entrances = {player: set() for player in players}
        self._hk_free_entrances = {player: {"Menu"} for player in players}
        self._hk_entrance_clause_cache = {player: {} for player in players}
        self._hk_checked_state_modifiers = {player: {} for player in players}
        self._hk_stale = dict.fromkeys(players, True)
        self._hk_sweeping = dict.fromkeys(players, False)
        self._hk_processed_item_cache = {player: Counter() for player in players}
        self._hk_charm_costs = KeyedDefaultDict(lambda player: multiworld.worlds[player].charm_names_and_costs)
        self._hk_soul_modes = KeyedDefaultDict(lambda player: multiworld.worlds[player].soul_modes)
        for player in players:
            self.prog_items[player]["MASKSHARDS"] = BASE_HEALTH*4
            self.prog_items[player]["NOTCHES"] = BASE_NOTCHES

    def copy_mixin(self, other) -> CollectionState:
        from . import HKWorld
        players = self.multiworld.get_game_players(HKWorld.game)
        if not players:
            return other
        # Copy sweepable data as state can be copied when stale
        for player in players:
            for entrance, rss in self._hk_per_player_resource_states[player].items():
                other._hk_per_player_resource_states[player][entrance] = rss.copy()
        other._hk_entrance_clause_cache = {
            player: {
                entrance: cache.copy()
                for entrance, cache in self._hk_entrance_clause_cache[player].items()
            }
            for player in players
        }
        other._hk_checked_state_modifiers = {
            player: {
                entrance: modifiers.copy()
                for entrance, modifiers in self._hk_checked_state_modifiers[player].items()
            }
            for player in players
        }
        other._hk_free_entrances = {player: self._hk_free_entrances[player].copy() for player in players}
        other._hk_processed_item_cache = {player: self._hk_processed_item_cache[player].copy() for player in players}
        other._hk_per_player_sweepable_entrances = {
            player: entrances.copy() for player, entrances in self._hk_per_player_sweepable_entrances.items()
        }
        return other

    def _hk_test_fake_state(self, clause: "HKClause", faux_parent: Region) -> bool:
        player = faux_parent.player
        available_states = list(self._hk_per_player_resource_states[player][faux_parent.name])

        for handler in clause.hk_state_requirements:
            available_states = [
                s
                for input_state in available_states
                for s in handler.modify_state(input_state, self)
            ]
        return bool(available_states)

    def _hk_apply_and_validate_state(self, clause: "HKClause", region: Region, target_region=None) -> bool:
        player = region.player
        available_states = list(self._hk_per_player_resource_states[player][region.name])

        if not available_states:
            # no valid parent states
            raise Exception("no parent state to apply")
            return False

        for handler in clause.hk_state_requirements:
            available_states = [
                s
                for input_state in available_states
                for s in handler.modify_state(input_state, self)
            ]

        if not available_states:
            return False
        if not target_region:
            # don't persist
            return True

        target_states = self._hk_per_player_resource_states[player][target_region.name]
        if target_states == [0]:
            # target resource state is already perfect
            return True

        if len(available_states) > 1:
            # sort states and clean up any subsets that won't help reachability
            available_states.sort()
            ind = 1
            while ind < len(available_states):
                for prev in range(ind):
                    if rs_leq(available_states[prev], available_states[ind]):
                        available_states.pop(ind)
                        break
                else:
                    ind += 1

        if available_states:
            if available_states == target_states:
                # TODO: is this an appropriate assumption?
                return True
            # mergesort-like merging
            target_index = 0
            available_index = 0
            new_useful_state = False
            while available_index < len(available_states) or target_index < len(target_states):
                if available_index == len(available_states):
                    check_available = False
                elif target_index == len(target_states):
                    check_available = True
                elif target_states[target_index] == available_states[available_index]:
                    # current available state is already present in target list
                    # since both available and target has already been sorted and reduced,
                    # it is safe to skip reducing either current index as both present proves
                    # they are not subsets of any state in either list
                    available_index += 1
                    target_index += 1
                    continue
                elif target_states[target_index] < available_states[available_index]:
                    check_available = False
                else:
                    check_available = True

                if not check_available:
                    for prev in range(target_index):
                        if rs_leq(target_states[prev], target_states[target_index]):
                            # a previous state invalidated current target state, remove
                            # target_index now points to a new state so break and rerun
                            target_states.pop(target_index)
                            break
                    else:
                        # no previous states invalidated the current target state, move to next
                        target_index += 1
                else:
                    for prev in range(target_index):
                        if rs_leq(target_states[prev], available_states[available_index]):
                            # a previous state invalidated current available state, break to not reach else clause
                            break
                    else:
                        # no previous states were found to invalidate current available state, add to target
                        new_useful_state = True
                        target_states.insert(target_index, available_states[available_index])
                        target_index += 1
                    # regardless we've checked current available state, increment index
                    available_index += 1

            if new_useful_state:
                # update state caches
                self.reachable_regions[player].add(target_region)
                for exit in target_region.exits:
                    self._hk_per_player_sweepable_entrances[player].add(exit.name)
                    self._hk_checked_state_modifiers[player][exit.name] = set()
                for exit in self.multiworld.indirect_connections.get(target_region, set()):
                    self._hk_per_player_sweepable_entrances[player].add(exit.name)
                    self._hk_checked_state_modifiers[player][exit.name] = set()
            # self._hk_stale[player] = True
        assert target_states
        return True

    def _hk_sweep(self, player: int):
        if self._hk_sweeping[player]:
            return
        self._hk_sweeping[player] = True
        world = self.multiworld.worlds[player]
        start = world.get_region(world.origin_region_name)
        if start not in self.reachable_regions[player]:
            self.reachable_regions[player].add(start)
            for start_exit in start.exits:
                self._hk_per_player_sweepable_entrances[player].add(start_exit.name)
        # assume not stale and only evaluate true clauses
        while self._hk_per_player_sweepable_entrances[player]:
            # print(self._hk_per_player_sweepable_entrances[player])
            # random pop but i don't really care
            entrance_name = self._hk_per_player_sweepable_entrances[player].pop()
            entrance = self.multiworld.get_entrance(entrance_name, player)
            if entrance.parent_region in self.reachable_regions[player]:
                # let normal sweep find new regions
                reachable = entrance.can_reach(self)
                if reachable and entrance.connected_region is not None:
                    new_region = entrance.connected_region
                    # Retry connections if the new region can unblock them
                    for new_entrance in self.multiworld.indirect_connections.get(new_region, set()):
                        self._hk_per_player_sweepable_entrances[player].add(new_entrance.name)
                    # also update metadata
                    if new_region not in self.path:
                        self.path[new_region] = (
                            new_region.name,
                            self.path.get(entrance, None)
                        )
        self._hk_stale[player] = False
        self._hk_sweeping[player] = False


# Requirements for state comparison:
# negative values won't exist
# best case is falsy
# keys in right that are not in left are inherently lt
# any key in left > right is a failure
# any key in left and not in right is a failure
# don't care about full equality because of codepath


def edit_effects(state, player: int, item_effects: dict[str, int], add: bool):
    if add:
        for effect_name, effect_value in item_effects.items():
            state.prog_items[player][effect_name] += effect_value
    else:
        for effect_name, effect_value in item_effects.items():
            state.prog_items[player][effect_name] -= effect_value
            if state.prog_items[player][effect_name] < 1:
                del (state.prog_items[player][effect_name])


def check_item_logic(condition, state, player) -> bool:
    assert not condition["location_requirements"]
    assert not condition["region_requirements"]
    assert not condition["state_modifiers"]
    item_requirements = condition["item_requirements"]
    result = True
    for req in item_requirements:
        if ">" in req:
            item, value = (*req.split(">"),)
            result = result and state.count(item, player) > int(value)
        elif "<" in req:
            item, value = (*req.split("<"),)
            result = result and state.count(item, player) < int(value)
        elif "=" in req:
            item, value = (*req.split("="),)
            assert value.isdigit(), f"requirement {req} not supported"
            result = result and state.count(item, player) == int(value)
        else:
            # assume entire req is term
            result = result and state.has(req, player)
    return result


def handle_effect(item_name, lookup, state, player):
    if lookup["type"] == "conditional":
        if any(
                check_item_logic(condition, state, player)
                for condition in lookup["condition"]
                ):
            ret = lookup["effect"]
        else:
            return {}
    elif lookup["type"] == "branching":
        for branch in lookup["conditionals"]:
            if any(
                    check_item_logic(condition, state, player)
                    for condition in branch["condition"]
                    ):
                ret = branch["effect"]
                break
        else:
            # if none true use the parent else instead
            ret = lookup["else"]

    elif lookup["type"] == "incrementTerms":
        return lookup["effects"]
    elif lookup["type"] == "threshold":
        count = state._hk_processed_item_cache[player][lookup["term"]]
        if count == lookup["threshold"]:
            ret = lookup["at_threshold"]
        elif count < lookup["threshold"]:
            ret = lookup["below_threshold"]
        else:
            ret = lookup["above_threshold"]
        return {lookup["term"]: 1, **ret}

    else:
        raise Exception(f"unknown type {lookup['type']}")

    if "type" in ret:
        return handle_effect(item_name, ret, state, player)
    else:  # noqa: RET505
        raise Exception(f"unknown effect {ret}")


def hk_collect(self, state, item: "HKItem") -> bool:
    if item.advancement:
        player = item.player
        if item.name == "Grub":
            # to make sure grub counting is consistent across Groups etc.
            state.prog_items[player][item.name] += 1

        if item.name not in effects_prog_lookup:
            # handle events that don't have effects by adding them as their own terms
            state.prog_items[player][item.name] += 1
            if item.name in self.event_locations:
                state._hk_per_player_sweepable_entrances[player].update(self.entrance_by_term[item.name])
                for entrance, modifier_id in self.entrance_state_modifier_by_term[item.name]:
                    if entrance in state._hk_checked_state_modifiers[player]:
                        state._hk_checked_state_modifiers[player][entrance].discard(modifier_id)
        else:
            lookup = effects_prog_lookup[item.name]
            add = True

            effects = handle_effect(item.name, lookup, state, player)
            edit_effects(state, player, effects, add)
            if lookup["type"] in ("conditional", "branching",):
                state._hk_processed_item_cache[player][item.name] += 1
            elif lookup["type"] == "threshold":
                # increment term before checking threshold
                state._hk_processed_item_cache[player][lookup["term"]] += 1

            for term in effects.keys():
                state._hk_per_player_sweepable_entrances[player].update(self.entrance_by_term[term])
                for entrance, modifier_id in self.entrance_state_modifier_by_term[term]:
                    if entrance in state._hk_checked_state_modifiers[player]:
                        state._hk_checked_state_modifiers[player][entrance].discard(modifier_id)
        state._hk_stale[item.player] = True
    return item.advancement


def hk_remove(self, state, item: "HKItem") -> bool:
    if item.advancement:
        player = item.player
        if item.name == "Grub":
            # to make sure grub counting is consistent across Groups etc.
            state.prog_items[player][item.name] -= 1

        if item.name not in effects_prog_lookup:
            # handle events that don't have effects by adding them as their own terms
            state.prog_items[player][item.name] -= 1
        else:
            lookup = effects_prog_lookup[item.name]
            add = False

            if lookup["type"] in ("conditional", "branching",):
                state._hk_processed_item_cache[player][item.name] -= 1
                reset_terms = effects_terms_by_item[item.name]
                for term in reset_terms:
                    state.prog_items[player][term] = 0
                recalc_items = {item for term in reset_terms for item in effects_items_by_term[term]}
                owned_relevant_items = [
                    item
                    for item, count in state._hk_processed_item_cache[player].items()
                    for count in range(count)
                    if item in recalc_items
                    ]
                for recalc_item in owned_relevant_items:
                    effects = handle_effect(item.name, effects_prog_lookup[recalc_item], state, player)
                    # filter effects to just the ones we reset then add them to state
                    edit_effects(
                        state,
                        player,
                        {key: effects[key] for key in effects if key in reset_terms},
                        True
                        )
            else:
                if lookup["type"] == "threshold":
                    # increment term before checking threshold
                    state._hk_processed_item_cache[player][lookup["term"]] -= 1
                edit_effects(state, player, handle_effect(item.name, lookup, state, player), add)

        state._hk_entrance_clause_cache[item.player] = {}
        state._hk_per_player_sweepable_entrances[item.player] = {
            entrance.name for entrance in self.get_region("Menu").exits
            }
        state._hk_checked_state_modifiers[item.player] = {}
        state._hk_per_player_resource_states[item.player] = KeyedDefaultDict(
            lambda region: [default_state()] if region == "Menu" else []
        )  # TODO: we have this code copied a couple different places, see if we can centralize it

        state._hk_stale[item.player] = True
    return item.advancement
