from typing import TYPE_CHECKING, List, NamedTuple, Union

from BaseClasses import CollectionState
from ..AutoWorld import LogicMixin
from ..generic.Rules import set_rule, add_rule

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
    keys: int = 0

class SpireLogic(LogicMixin):

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


class SpireHasPower:

    def __init__(self, world, prefix, power: PowerLevel):
        self.rules = []
        self.world = world
        self.prefix = prefix
        self.power = power
        if power.relic > 0:
            self.rules.append(SpireHasPower._spire_has_relics)
        if power.boss_relic > 0:
            self.rules.append(SpireHasPower._spire_has_boss_relics)
        if power.draw > 0:
            self.rules.append(SpireHasPower._spire_has_cards)
        if world.options.campfire_sanity.value != 0:
            if power.rest > 0:
                self.rules.append(SpireHasPower._spire_has_rests)
            if power.smith > 0:
                self.rules.append(SpireHasPower._spire_has_smiths)
        if world.options.shop_sanity.value != 0:
            if power.shop > 0:
                self.rules.append(SpireHasPower._spire_has_shop)
            if world.options.shop_remove_slots.value != 0 and power.shop_remove > 0:
                self.rules.append(SpireHasPower._spire_has_shop_removes)
        if world.options.gold_sanity.value != 0 and power.gold > 0:
            self.rules.append(SpireHasPower._spire_has_gold)

    @staticmethod
    def _spire_has_relics(state: CollectionState, world: 'SpireWorld', prefix: str, power: PowerLevel) -> bool:
        count: int = state.count(f"{prefix} Relic", world.player) + state.count(f"{prefix} Boss Relic", world.player)
        return count >= power.relic

    @staticmethod
    def _spire_has_boss_relics(state: CollectionState, world: 'SpireWorld', prefix: str, power: PowerLevel) -> bool:
        return state.count(f"{prefix} Boss Relic", world.player) >= power.boss_relic

    @staticmethod
    def _spire_has_cards(state: CollectionState, world: 'SpireWorld', prefix: str, power: PowerLevel) -> bool:
        count = state.count(f"{prefix} Card Reward", world.player) + state.count(f"{prefix} Rare Card Reward", world.player)
        return count >= power.draw

    @staticmethod
    def _spire_has_rests(state: CollectionState, world: 'SpireWorld', prefix: str, power: PowerLevel) -> bool:
        return state.count(f"{prefix} Progressive Rest", world.player) >= power.rest

    @staticmethod
    def _spire_has_smiths(state: CollectionState, world: 'SpireWorld', prefix: str, power: PowerLevel) -> bool:
        return state.count(f"{prefix} Progressive Smith", world.player) >= power.smith

    @staticmethod
    def _spire_has_shop(state: CollectionState, world: 'SpireWorld', prefix: str, power: PowerLevel) -> bool:
        player = world.player
        max_shop = world.total_shop_items
        return (state.count(f"{prefix} Shop Card Slot", player) +
                state.count(f"{prefix} Neutral Shop Card Slot", player) +
                state.count(f"{prefix} Shop Relic Slot", player) +
                state.count(f"{prefix} Shop Potion Slot", player) >= min(power.shop, max_shop))

    @staticmethod
    def _spire_has_shop_removes(state: CollectionState, world: 'SpireWorld', prefix: str, power: PowerLevel):
        return state.count(f"{prefix} Progressive Shop Remove", world.player) >= power.shop_remove

    @staticmethod
    def _spire_has_gold(state: CollectionState, world: 'SpireWorld', prefix: str, power: PowerLevel):
        return (state.count(f"{prefix} 30 Gold", world.player) * 30 + state.count(f"{prefix} Boss Gold", world.player) * 75) >= power.gold

    def __call__(self, state: Union[CollectionState, 'SpireLogic']) -> bool:
        for func in self.rules:
            if not func(state, self.world, self.prefix, self.power):
                return False
        return True

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
             SpireHasPower(world, prefix, PowerLevel(relic=1, rest=1)))
    set_rule(multiworld.get_location(f"{prefix} Card Reward 4", player),
             SpireHasPower(world, prefix, PowerLevel(relic=1, rest=1)))

    # Act 1 Relics
    set_rule(multiworld.get_location(f"{prefix} Relic 1", player),
             SpireHasPower(world, prefix, PowerLevel(draw=1)))
    set_rule(multiworld.get_location(f"{prefix} Relic 2", player),
             SpireHasPower(world, prefix, PowerLevel(draw=2, rest=1, shop=2)))
    set_rule(multiworld.get_location(f"{prefix} Relic 3", player),
             SpireHasPower(world, prefix, PowerLevel(draw=2, rest=1, shop=2)))

    set_rule(multiworld.get_entrance(f"{prefix} Late Act 1", player),
             SpireHasPower(world, prefix, PowerLevel(draw=2, rest=1, shop=2)))

    # Act 1 Boss Event
    set_rule(multiworld.get_entrance(f"{prefix} Act 1 Boss Arena", player),
             SpireHasPower(world, prefix, PowerLevel(draw=3, relic=2, smith=1, shop=3, shop_remove=1, gold=50)))

    # Act 1 Boss Rewards
    set_rule(multiworld.get_location(f"{prefix} Rare Card Reward 1", player),
             lambda state: state.has(f"{prefix} Beat Act 1 Boss", player))
    set_rule(multiworld.get_location(f"{prefix} Boss Relic 1", player),
             lambda state: state.has(f"{prefix} Beat Act 1 Boss", player))
    set_rule(multiworld.get_entrance(f"{prefix} Early Act 2", player),
             lambda state: state.has(f"{prefix} Beat Act 1 Boss", player))

    # Act 2 Card Rewards
    set_rule(multiworld.get_location(f"{prefix} Card Reward 7", player),
             SpireHasPower(world, prefix, PowerLevel(draw=6,relic=3)))
    set_rule(multiworld.get_location(f"{prefix} Card Reward 8", player),
             SpireHasPower(world, prefix, PowerLevel(draw=6, relic=4)))

    # Act 2 Relics
    set_rule(multiworld.get_location(f"{prefix} Relic 4", player),
             SpireHasPower(world, prefix, PowerLevel(draw=7, relic=2)))
    set_rule(multiworld.get_location(f"{prefix} Relic 5", player),
             SpireHasPower(world, prefix, PowerLevel(draw=7, relic=2)))
    set_rule(multiworld.get_location(f"{prefix} Relic 6", player),
             SpireHasPower(world, prefix, PowerLevel(draw=7, relic=3)))

    set_rule(multiworld.get_entrance(f"{prefix} Mid Act 2", player),
             SpireHasPower(world, prefix, PowerLevel(draw=6,relic=2,rest=2, shop=4)))

    set_rule(multiworld.get_entrance(f"{prefix} Late Act 2", player),
             SpireHasPower(world, prefix, PowerLevel(draw=6, relic=3, shop=5)))

    # Act 2 Boss Event
    set_rule(multiworld.get_entrance(f"{prefix} Act 2 Boss Arena", player),
             SpireHasPower(world, prefix, PowerLevel(draw=7, relic=4, boss_relic=1, smith=2, shop=6, shop_remove=2, gold=150)))

    # Act 2 Boss Rewards
    set_rule(multiworld.get_location(f"{prefix} Rare Card Reward 2", player),
             lambda state: state.has(f"{prefix} Beat Act 2 Boss", player))
    set_rule(multiworld.get_location(f"{prefix} Boss Relic 2", player),
             lambda state: state.has(f"{prefix} Beat Act 2 Boss", player))

    set_rule(multiworld.get_entrance(f"{prefix} Early Act 3", player),
             lambda state: state.has(f"{prefix} Beat Act 2 Boss", player))

    if world.options.shop_sanity:
        add_rule(multiworld.get_entrance(f"{prefix} Act 1 Shop", player),
                 SpireHasPower(world, prefix, PowerLevel(gold=50)))

        add_rule(multiworld.get_entrance(f"{prefix} Act 2 Shop", player),
                 SpireHasPower(world, prefix, PowerLevel(gold=150)))

        add_rule(multiworld.get_entrance(f"{prefix} Act 3 Shop", player),
                 SpireHasPower(world, prefix, PowerLevel(gold=270)))

    if world.options.gold_sanity:
        set_rule(multiworld.get_location(f"{prefix} Combat Gold 12", player),
                 SpireHasPower(world, prefix, PowerLevel(draw=6,relic=3)))
        set_rule(multiworld.get_location(f"{prefix} Combat Gold 13", player),
                 SpireHasPower(world, prefix, PowerLevel(draw=6, relic=3)))

        set_rule(multiworld.get_location(f"{prefix} Combat Gold 14", player),
                 SpireHasPower(world, prefix, PowerLevel(draw=6,relic=4)))
        set_rule(multiworld.get_location(f"{prefix} Combat Gold 15", player),
                 SpireHasPower(world, prefix, PowerLevel(draw=6,relic=4)))
        set_rule(multiworld.get_location(f"{prefix} Combat Gold 16", player),
                 SpireHasPower(world, prefix, PowerLevel(draw=6, relic=4)))

        set_rule(multiworld.get_location(f"{prefix} Combat Gold 4", player),
                 SpireHasPower(world, prefix, PowerLevel(relic=1, rest=1)))
        set_rule(multiworld.get_location(f"{prefix} Combat Gold 5", player),
                 SpireHasPower(world, prefix, PowerLevel(relic=1, rest=1)))
        set_rule(multiworld.get_location(f"{prefix} Combat Gold 6", player),
                 SpireHasPower(world, prefix, PowerLevel(relic=1, rest=1)))
        set_rule(multiworld.get_location(f"{prefix} Combat Gold 7", player),
                 SpireHasPower(world, prefix, PowerLevel(relic=1, rest=1)))

        set_rule(multiworld.get_location(f"{prefix} Boss Gold 1", player),
                 lambda state: state.has(f"{prefix} Beat Act 1 Boss", player))
        set_rule(multiworld.get_location(f"{prefix} Boss Gold 2", player),
                 lambda state: state.has(f"{prefix} Beat Act 2 Boss", player))

    # Act 3 Relics
    set_rule(multiworld.get_location(f"{prefix} Relic 7", player),
             SpireHasPower(world, prefix, PowerLevel(relic=4)))

    set_rule(multiworld.get_entrance(f"{prefix} Mid Act 3", player),
             SpireHasPower(world, prefix, PowerLevel(draw=8, relic=5, rest=3, shop=8)))

    set_rule(multiworld.get_entrance(f"{prefix} Late Act 3", player),
             SpireHasPower(world, prefix, PowerLevel(draw=9, relic=7, rest=3, shop=10)))

    # Act 3 Boss Event
    set_rule(multiworld.get_entrance(f"{prefix} Act 3 Boss Arena", player),
             SpireHasPower(world, prefix, PowerLevel(draw=10, relic=9, boss_relic=2, smith=3, shop=10, shop_remove=3, gold=270)))

    set_rule(multiworld.get_entrance(f"{prefix} Act 4", player),
             lambda state: state.has(f"{prefix} Beat Act 3 Boss", player))

    if config.key_sanity:
        add_rule(multiworld.get_location(f"{prefix} Sapphire Key", player),
                 SpireHasPower(world, prefix, PowerLevel(draw=1)))

        add_rule(multiworld.get_entrance(f"{prefix} Act 4", player),
                 lambda state: state.has(f"{prefix} Sapphire Key", player) and
                               state.has(f"{prefix} Ruby Key", player) and
                               state.has(f"{prefix} Emerald Key", player))