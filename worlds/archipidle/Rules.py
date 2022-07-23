from BaseClasses import MultiWorld
from ..AutoWorld import LogicMixin
from ..generic.Rules import set_rule


class ArchipIDLELogic(LogicMixin):
    def _archipidle_location_is_accessible(self, player_id, items_required, world):
        found: int = 0
        for item_name in world.worlds[player_id].prog_items:
            found += self.prog_items[item_name, player_id]
            if found >= items_required:
                return True
        return False


def set_rules(world: MultiWorld, player: int):
    for i in range(16, 31):
        set_rule(
            world.get_location(f"IDLE for at least {int(i / 2)} minutes {30 if (i % 2) else 0} seconds", player),
            lambda state: state._archipidle_location_is_accessible(player, 4, world)
        )

    for i in range(31, 51):
        set_rule(
            world.get_location(f"IDLE for at least {int(i / 2)} minutes {30 if (i % 2) else 0} seconds", player),
            lambda state: state._archipidle_location_is_accessible(player, 10, world)
        )

    for i in range(51, 101):
        set_rule(
            world.get_location(f"IDLE for at least {int(i / 2)} minutes {30 if (i % 2) else 0} seconds", player),
            lambda state: state._archipidle_location_is_accessible(player, 20, world)
        )

    world.completion_condition[player] = lambda state: \
        state.can_reach(world.get_location(f"IDLE for at least 50 minutes 0 seconds", player), "Location", player)
