from BaseClasses import MultiWorld
from ..AutoWorld import LogicMixin
from ..generic.Rules import set_rule


class SpireLogic(LogicMixin):
    def _spire_has_relics(self, player: int, amount: int) -> bool:
        count: int = self.item_count("Relic", player) + self.item_count("Boss Relic", player)
        return count >= amount

    def _spire_has_cards(self, player: int, amount: int) -> bool:
        count = self.item_count("Card Draw", player) + self.item_count("Rare Card Draw", player)
        return count >= amount


def set_rules(world: MultiWorld, player: int):

    # Act 1 Card Draws
    set_rule(world.get_location("Card Draw 1", player), lambda state: True)
    set_rule(world.get_location("Card Draw 2", player), lambda state: True)
    set_rule(world.get_location("Card Draw 3", player), lambda state: True)
    set_rule(world.get_location("Card Draw 4", player), lambda state: state._spire_has_relics(player, 1))
    set_rule(world.get_location("Card Draw 5", player), lambda state: state._spire_has_relics(player, 1))

    # Act 1 Relics
    set_rule(world.get_location("Relic 1", player), lambda state: state._spire_has_cards(player, 1))
    set_rule(world.get_location("Relic 2", player), lambda state: state._spire_has_cards(player, 2))
    set_rule(world.get_location("Relic 3", player), lambda state: state._spire_has_cards(player, 2))

    # Act 1 Boss Event
    set_rule(world.get_location("Act 1 Boss", player), lambda state: state._spire_has_cards(player, 3) and state._spire_has_relics(player, 2))

    # Act 1 Boss Rewards
    set_rule(world.get_location("Rare Card Draw 1", player), lambda state: state.has("Beat Act 1 Boss", player))
    set_rule(world.get_location("Boss Relic 1", player), lambda state: state.has("Beat Act 1 Boss", player))

    # Act 2 Card Draws
    set_rule(world.get_location("Card Draw 6", player), lambda state: state.has("Beat Act 1 Boss", player))
    set_rule(world.get_location("Card Draw 7", player), lambda state: state.has("Beat Act 1 Boss", player))
    set_rule(world.get_location("Card Draw 8", player), lambda state: state.has("Beat Act 1 Boss", player) and state._spire_has_cards(player, 6) and state._spire_has_relics(player, 3))
    set_rule(world.get_location("Card Draw 9", player), lambda state: state.has("Beat Act 1 Boss", player) and state._spire_has_cards(player, 6) and state._spire_has_relics(player, 4))
    set_rule(world.get_location("Card Draw 10", player), lambda state: state.has("Beat Act 1 Boss", player) and state._spire_has_cards(player, 7) and state._spire_has_relics(player, 4))

    # Act 2 Relics
    set_rule(world.get_location("Relic 4", player), lambda state: state.has("Beat Act 1 Boss", player) and state._spire_has_cards(player, 7) and state._spire_has_relics(player, 2))
    set_rule(world.get_location("Relic 5", player), lambda state: state.has("Beat Act 1 Boss", player) and state._spire_has_cards(player, 7) and state._spire_has_relics(player, 2))
    set_rule(world.get_location("Relic 6", player), lambda state: state.has("Beat Act 1 Boss", player) and state._spire_has_cards(player, 7) and state._spire_has_relics(player, 3))

    # Act 2 Boss Event
    set_rule(world.get_location("Act 2 Boss", player), lambda state: state.has("Beat Act 1 Boss", player) and state._spire_has_cards(player, 7) and state._spire_has_relics(player, 4) and state.has("Boss Relic", player))

    # Act 2 Boss Rewards
    set_rule(world.get_location("Rare Card Draw 2", player), lambda state: state.has("Beat Act 2 Boss", player))
    set_rule(world.get_location("Boss Relic 2", player), lambda state: state.has("Beat Act 2 Boss", player))

    # Act 3 Card Draws
    set_rule(world.get_location("Card Draw 11", player), lambda state: state.has("Beat Act 2 Boss", player))
    set_rule(world.get_location("Card Draw 12", player), lambda state: state.has("Beat Act 2 Boss", player))
    set_rule(world.get_location("Card Draw 13", player), lambda state: state.has("Beat Act 2 Boss", player) and state._spire_has_relics(player, 4))
    set_rule(world.get_location("Card Draw 14", player), lambda state: state.has("Beat Act 2 Boss", player) and state._spire_has_relics(player, 4))
    set_rule(world.get_location("Card Draw 15", player), lambda state: state.has("Beat Act 2 Boss", player) and state._spire_has_relics(player, 4))

    # Act 3 Relics
    set_rule(world.get_location("Relic 7", player), lambda state: state.has("Beat Act 2 Boss", player) and state._spire_has_relics(player, 4))
    set_rule(world.get_location("Relic 8", player), lambda state: state.has("Beat Act 2 Boss", player) and state._spire_has_relics(player, 5))
    set_rule(world.get_location("Relic 9", player), lambda state: state.has("Beat Act 2 Boss", player) and state._spire_has_relics(player, 5))
    set_rule(world.get_location("Relic 10", player), lambda state: state.has("Beat Act 2 Boss", player) and state._spire_has_relics(player, 5))

    # Act 3 Boss Event
    set_rule(world.get_location("Act 3 Boss", player), lambda state: state.has("Beat Act 2 Boss", player) and state._spire_has_relics(player, 7) and state.has("Boss Relic", player, 2))

    set_rule(world.get_location("Heart Room", player), lambda state: state.has("Beat Act 3 Boss", player))

    world.completion_condition[player] = lambda state: state.has("Victory", player)
