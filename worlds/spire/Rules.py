from typing import TYPE_CHECKING, List, NamedTuple, Union

from BaseClasses import CollectionState
from ..AutoWorld import LogicMixin
from ..generic.Rules import set_rule

if TYPE_CHECKING:
    from . import SpireWorld, CharacterConfig


class PowerLevel(NamedTuple):
    draw: int = 0
    relic: int = 0
    boss_relic: int = 0
    rest: int = 0
    smith: int = 0
    shop: int = 0
    shop_remove: int = 0
    gold: int = 0

class SpireLogic(LogicMixin):
    def _spire_has_relics(self: CollectionState, player: int, prefix, amount: int) -> bool:
        count: int = self.count(f"{prefix} Relic", player) + self.count(f"{prefix} Boss Relic", player)
        return count >= amount

    def _spire_has_cards(self: CollectionState, player: int, prefix, amount: int) -> bool:
        count = self.count(f"{prefix} Card Reward", player) + self.count(f"{prefix} Rare Card Reward", player)
        return count >= amount

    def _spire_has_rests(self: CollectionState, player: int, prefix: str, amount: int, campsanity: int) -> bool:
        if campsanity:
            return self.count(f"{prefix} Progressive Rest", player) >= amount
        else:
            return True

    def _spire_has_smiths(self: CollectionState, player: int, prefix: str, amount: int, campsanity: int) -> bool:
        if campsanity:
            return self.count(f"{prefix} Progressive Smith", player) >= amount
        else:
            return True

    def _spire_has_shop(self: CollectionState, player: int, prefix: str, amount: int, world: 'SpireWorld') -> bool:
        if world.options.shop_sanity:
            max_shop = world.total_shop_items
            return (self.count(f"{prefix} Shop Card Slot", player) +
                    self.count(f"{prefix} Neutral Shop Card Slot", player) +
                    self.count(f"{prefix} Shop Relic Slot", player) +
                    self.count(f"{prefix} Shop Potion Slot", player) >= min(amount, max_shop))
        else:
            return True

    def _spire_has_shop_removes(self: CollectionState, player: int, prefix: str, amount: int, world: 'SpireWorld'):
        if world.options.shop_sanity and world.options.shop_remove_slots:
            return self.count(f"{prefix} Progressive Shop Remove", player) >= amount
        else:
            return True

    def _spire_has_gold(self: CollectionState, player: int, prefix: str, amount: int, world: 'SpireWorld'):
        if world.options.gold_sanity:
            return (self.count(f"{prefix} 30 Gold", player) * 30 + self.count(f"{prefix} Boss Gold", player) * 75) >= amount
        else:
            return True

    def _spire_has_victories(self: CollectionState, player: int, configs: List['CharacterConfig'], world: 'SpireWorld'):
        num_chars_goal = world.options.num_chars_goal.value
        count = 0
        for config in configs:
            if self.has(f"{config.name} Victory", player):
                count += 1
        if num_chars_goal == 0:
            return count >= len(configs)
        else:
            return count >= num_chars_goal


    def _spire_has_power(self: Union[CollectionState, 'SpireLogic'], world: 'SpireWorld', prefix: str, power: PowerLevel) -> bool:
        result: bool = True
        if power.relic > 0:
            result &= self._spire_has_relics(world.player, prefix, power.relic)
        if power.boss_relic > 0:
            result &= self.count(f"{prefix} Boss Relic", world.player) >= power.boss_relic
        if power.draw > 0:
            result &= self._spire_has_cards(world.player, prefix, power.draw)
        if world.options.campfire_sanity.value != 0:
            if power.rest > 0:
                result &= self.count(f"{prefix} Progressive Rest", world.player) >= power.rest
            if power.smith > 0:
                result &= self.count(f"{prefix} Progressive Smith", world.player) >= power.smith
        if power.shop > 0:
            result &= self._spire_has_shop(world.player, prefix, power.shop, world)
        if power.shop_remove > 0:
            result &= self._spire_has_shop_removes(world.player, prefix, power.shop_remove, world)
        if power.gold > 0:
            result &= self._spire_has_gold(world.player, prefix, power.gold, world)
        return result



def set_rules(world: 'SpireWorld', player: int):
    multiworld = world.multiworld
    for config in world.characters:
        _set_rules(world, player, config)

    multiworld.completion_condition[player] = lambda state: state._spire_has_victories(player, world.characters, world)

def _set_rules(world: 'SpireWorld', player: int, config: 'CharacterConfig'):
    multiworld = world.multiworld
    prefix = config.name
    if config.locked:
        set_rule(multiworld.get_entrance(f"{prefix} Early Act 1", player),
                 lambda state: state.has(f"{prefix} Unlock", player))
    # Act 1 Card Rewards
    set_rule(multiworld.get_location(f"{prefix} Card Reward 3", player),
             lambda state: state._spire_has_power(world, prefix, PowerLevel(relic=1,rest=1)))
    set_rule(multiworld.get_location(f"{prefix} Card Reward 4", player),
             lambda state: state._spire_has_power(world, prefix, PowerLevel(relic=1, rest=1)))



    # Act 1 Relics
    set_rule(multiworld.get_location(f"{prefix} Relic 1", player),
             lambda state: state._spire_has_power(world, prefix, PowerLevel(draw=1)))
    set_rule(multiworld.get_location(f"{prefix} Relic 2", player),
             lambda state: state._spire_has_power(world, prefix, PowerLevel(draw=2, rest=1, shop=2)))
    set_rule(multiworld.get_location(f"{prefix} Relic 3", player),
             lambda state: state._spire_has_power(world, prefix, PowerLevel(draw=2, rest=1, shop=2)))

    set_rule(multiworld.get_entrance(f"{prefix} Late Act 1", player),
             lambda state: state._spire_has_power(world, prefix, PowerLevel(draw=2, rest=1, shop=2)))

    # Act 1 Boss Event
    set_rule(multiworld.get_entrance(f"{prefix} Act 1 Boss Arena", player),
             lambda state: state._spire_has_power(world, prefix, PowerLevel(draw=3, relic=2, smith=1, shop=3, shop_remove=1, gold=50)))

    # Act 1 Boss Rewards
    set_rule(multiworld.get_location(f"{prefix} Rare Card Reward 1", player),
             lambda state: state.has(f"{prefix} Beat Act 1 Boss", player))
    set_rule(multiworld.get_location(f"{prefix} Boss Relic 1", player),
             lambda state: state.has(f"{prefix} Beat Act 1 Boss", player))
    set_rule(multiworld.get_entrance(f"{prefix} Early Act 2", player),
             lambda state: state.has(f"{prefix} Beat Act 1 Boss", player))


    # Act 2 Card Rewards
    set_rule(multiworld.get_location(f"{prefix} Card Reward 7", player),
             lambda state: state._spire_has_power(world, prefix, PowerLevel(draw=6,relic=3)))
    set_rule(multiworld.get_location(f"{prefix} Card Reward 8", player),
             lambda state: state._spire_has_power(world, prefix, PowerLevel(draw=6, relic=4)))

    # Act 2 Relics
    set_rule(multiworld.get_location(f"{prefix} Relic 4", player),
             lambda state: state._spire_has_power(world, prefix, PowerLevel(draw=7, relic=2)))
    set_rule(multiworld.get_location(f"{prefix} Relic 5", player),
             lambda state: state._spire_has_power(world, prefix, PowerLevel(draw=7, relic=2)))
    set_rule(multiworld.get_location(f"{prefix} Relic 6", player),
             lambda state: state._spire_has_power(world, prefix, PowerLevel(draw=7, relic=3)))

    set_rule(multiworld.get_entrance(f"{prefix} Mid Act 2", player),
             lambda state: state._spire_has_power(world, prefix, PowerLevel(draw=6,relic=2,rest=2, shop=4)))

    set_rule(multiworld.get_entrance(f"{prefix} Late Act 2", player),
             lambda state: state._spire_has_power(world, prefix, PowerLevel(draw=6, relic=3, shop=5)))

    # Act 2 Boss Event
    set_rule(multiworld.get_entrance(f"{prefix} Act 2 Boss Arena", player),
             lambda state: state._spire_has_power(world, prefix, PowerLevel(draw=7, relic=4, boss_relic=1, smith=2, shop=6, shop_remove=2, gold=150)))

    # Act 2 Boss Rewards
    set_rule(multiworld.get_location(f"{prefix} Rare Card Reward 2", player),
             lambda state: state.has(f"{prefix} Beat Act 2 Boss", player))
    set_rule(multiworld.get_location(f"{prefix} Boss Relic 2", player),
             lambda state: state.has(f"{prefix} Beat Act 2 Boss", player))

    set_rule(multiworld.get_entrance(f"{prefix} Early Act 3", player),
             lambda state: state.has(f"{prefix} Beat Act 2 Boss", player))

    if world.options.shop_sanity:
        total_shop = world.total_shop_locations + 1
        # Act 1 Shop
        for i in range(1, min(6, total_shop)):
            set_rule(multiworld.get_location(f"{prefix} Shop Slot {i}", player),
                     lambda state: state._spire_has_power(world, prefix, PowerLevel(gold=50)))

        # Act 2 Shop
        for i in range(min(6, total_shop), min(11, total_shop)):
            set_rule(multiworld.get_location(f"{prefix} Shop Slot {i}", player),
                     lambda state: state._spire_has_power(world, prefix, PowerLevel(gold=150)))

        # Act 3 Shop
        for i in range(min(11, total_shop), min(17, total_shop)):
            set_rule(multiworld.get_location(f"{prefix} Shop Slot {i}", player),
                     lambda state: state._spire_has_power(world, prefix, PowerLevel(gold=270)))

    if world.options.gold_sanity:
        set_rule(multiworld.get_location(f"{prefix} Combat Gold 9", player),
                 lambda state: state._spire_has_power(world, prefix, PowerLevel(draw=6,relic=3)))
        set_rule(multiworld.get_location(f"{prefix} Combat Gold 10", player),
                 lambda state: state._spire_has_power(world, prefix, PowerLevel(draw=6,relic=3)))

        set_rule(multiworld.get_location(f"{prefix} Combat Gold 11", player),
                 lambda state: state._spire_has_power(world, prefix, PowerLevel(draw=6,relic=4)))
        set_rule(multiworld.get_location(f"{prefix} Combat Gold 12", player),
                 lambda state: state._spire_has_power(world, prefix, PowerLevel(draw=6,relic=4)))

        set_rule(multiworld.get_location(f"{prefix} Elite Gold 1", player),
                 lambda state: state._spire_has_power(world, prefix, PowerLevel(draw=2, rest=1, shop=2)))
        set_rule(multiworld.get_location(f"{prefix} Elite Gold 2", player),
                 lambda state: state._spire_has_power(world, prefix, PowerLevel(draw=2, rest=1, shop=2)))
        set_rule(multiworld.get_location(f"{prefix} Elite Gold 3", player),
                 lambda state: state._spire_has_power(world, prefix, PowerLevel(draw=7, relic=2)))
        set_rule(multiworld.get_location(f"{prefix} Elite Gold 4", player),
                 lambda state: state._spire_has_power(world, prefix, PowerLevel(draw=7, relic=3)))
        set_rule(multiworld.get_location(f"{prefix} Boss Gold 1", player),
                 lambda state: state.has(f"{prefix} Beat Act 1 Boss", player))
        set_rule(multiworld.get_location(f"{prefix} Boss Gold 2", player),
                 lambda state: state.has(f"{prefix} Beat Act 2 Boss", player))


    # Act 3 Relics
    set_rule(multiworld.get_location(f"{prefix} Relic 7", player),
             lambda state: state._spire_has_power(world, prefix, PowerLevel(relic=4)))

    set_rule(multiworld.get_entrance(f"{prefix} Mid Act 3", player),
             lambda state: state._spire_has_power(world, prefix, PowerLevel(draw=8, relic=5, rest=3, shop=8)))

    set_rule(multiworld.get_entrance(f"{prefix} Late Act 3", player),
             lambda state: state._spire_has_power(world, prefix, PowerLevel(draw=9, relic=7, rest=3, shop=10)))

    # Act 3 Boss Event
    set_rule(multiworld.get_entrance(f"{prefix} Act 3 Boss Arena", player),
             lambda state: state._spire_has_power(world, prefix, PowerLevel(draw=10, relic=9, boss_relic=2, smith=3, shop=10, shop_remove=3, gold=270)))

    set_rule(multiworld.get_entrance(f"{prefix} Act 4", player),
             lambda state: state.has(f"{prefix} Beat Act 3 Boss", player))
