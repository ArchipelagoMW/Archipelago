from typing import NamedTuple, TYPE_CHECKING

from worlds.generic.Rules import set_rule

from .constants import base_id
from .logic_helpers import has_melee


if TYPE_CHECKING:
    from . import TunicWorld


class TunicLocationData(NamedTuple):
    region: str
    er_region: str


bell_location_table: dict[str, TunicLocationData] = {
    "Forest Belltower - Ring the East Bell": TunicLocationData("Forest Belltower", "Forest Belltower Upper"),
    "Overworld - [West] Ring the West Bell": TunicLocationData("Overworld", "Overworld Belltower at Bell"),
}

bell_location_base_id = base_id + 11000
bell_location_name_to_id: dict[str, int] = {name: bell_location_base_id + index
                                            for index, name in enumerate(bell_location_table)}

bell_location_groups: dict[str, set[str]] = {}
for location_name, location_data in bell_location_table.items():
    bell_location_groups.setdefault(location_data.region, set()).add(location_name)
    bell_location_groups.setdefault("Bells", set()).add(location_name)


def set_bell_location_rules(world: "TunicWorld") -> None:
    player = world.player

    set_rule(world.get_location("Forest Belltower - Ring the East Bell"),
             lambda state: has_melee(state, player) or state.has("Magic Wand", player))
    set_rule(world.get_location("Overworld - [West] Ring the West Bell"),
             lambda state: has_melee(state, player) or state.has("Magic Wand", player))
