from BaseClasses import MultiWorld
from ..AutoWorld import LogicMixin
from .Options import EnergyCore
from typing import Set
# TODO: Options may preset certain progress steps (i.e. P_ROCK_SKIP), set in generate_early?

from . import pyevermizer

# TODO: resolve/flatten/expand rules to get rid of recursion below where possible
# Logic.rules are all rules including locations, excluding those with no progress (i.e. locations that only drop items)
rules = [rule for rule in pyevermizer.get_logic() if len(rule.provides) > 0]
# Logic.items are all items and extra items excluding non-progression items and duplicates
item_names: Set[str] = set()
items = [item for item in filter(lambda item: item.progression, pyevermizer.get_items() + pyevermizer.get_extra_items())
         if item.name not in item_names and not item_names.add(item.name)]


# when this module is loaded, this mixin will extend BaseClasses.CollectionState
class SecretOfEvermoreLogic(LogicMixin):
    def _soe_count(self, progress: int, world: MultiWorld, player: int, max_count: int = 0) -> int:
        """
        Returns reached count of one of evermizer's progress steps based on collected items.
        i.e. returns 0-3 for P_DE based on items providing CHECK_BOSS,DIAMOND_EYE_DROP
        """
        n = 0
        for item in items:
            for pvd in item.provides:
                if pvd[1] == progress:
                    if self.has(item.name, player):
                        n += self.item_count(item.name, player) * pvd[0]
                        if n >= max_count > 0:
                            return n
        for rule in rules:
            for pvd in rule.provides:
                if pvd[1] == progress and pvd[0] > 0:
                    has = True
                    for req in rule.requires:
                        if not self._soe_has(req[1], world, player, req[0]):
                            has = False
                            break
                    if has:
                        n += pvd[0]
                        if n >= max_count > 0:
                            return n
        return n

    def _soe_has(self, progress: int, world: MultiWorld, player: int, count: int = 1) -> bool:
        """
        Returns True if count of one of evermizer's progress steps is reached based on collected items. i.e. 2 * P_DE
        """
        if progress == pyevermizer.P_ENERGY_CORE:  # logic is shared between worlds, so we override in the call
            w = world.worlds[player]
            if w.energy_core == EnergyCore.option_fragments:
                progress = pyevermizer.P_CORE_FRAGMENT
                count = w.required_fragments
        return self._soe_count(progress, world, player, count) >= count
