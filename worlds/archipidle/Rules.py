from BaseClasses import MultiWorld
from ..AutoWorld import LogicMixin
from ..generic.Rules import set_rule


class ArchipIDLELogic(LogicMixin):
    def _archipidle_location_is_accessible(self, player_id, items_required):
        items_received = 0
        for item in self.prog_items:
            if item[1] == player_id:
                items_received += 1

        return items_received >= items_required


def set_rules(world: MultiWorld, player: int):
    for i in range(1, 11):
        set_rule(
            world.get_location(f"Location {i}", player),
            lambda state: state._archipidle_location_is_accessible(player, 0)
        )

    for i in range(11, 31):
        set_rule(
            world.get_location(f"Location {i}", player),
            lambda state: state._archipidle_location_is_accessible(player, 4)
        )

    for i in range(31, 51):
        set_rule(
            world.get_location(f"Location {i}", player),
            lambda state: state._archipidle_location_is_accessible(player, 20)
        )
