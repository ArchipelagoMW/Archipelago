from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .world import GatoRobotoWorld

def setup_options_from_slot_data(world: GatoRobotoWorld) -> None:
    # implement .yaml-less Universal Tracker support
    if hasattr(world.multiworld, "generation_is_fake"):
        if hasattr(world.multiworld, "re_gen_passthrough"):
            if "Gato Roboto B-Side" in world.multiworld.re_gen_passthrough:
                world.using_ut = True
                slot_data = world.multiworld.re_gen_passthrough["Gato Roboto B-Side"]
                world.options.use_smallmech.value = slot_data['use_smallmech']
                world.options.use_watermech.value = slot_data['use_watermech']
                world.options.gato_tech.value = slot_data['gato_tech']
                world.options.nexus_start.value = slot_data['nexus_start']

# for UT poptracker integration map tab switching
def map_page_index(data: Any) -> int:
    if type(data) is int:
        return data
    mapping: dict[str, int] = {
        "Landing Site": 0,
        "Aqueducts": 1,
        "Nexus": 2,
        "Heater Core": 3,
        "Ventilation": 4,
        "Incubator": 5,
        "Laboratory": 6,
    }
    return mapping.get(data, 0)