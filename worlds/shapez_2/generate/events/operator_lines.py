from typing import TYPE_CHECKING
from BaseClasses import Region, LocationProgressType, ItemClassification

if TYPE_CHECKING:
    from ... import Shapez2World
    from ...data import AccessRule


def get_events(world: "Shapez2World",
               regions: dict[str, Region],
               processor_rules_dict: dict[tuple[str, ...], "AccessRule"]) -> None:
    from ..shapes import event_by_processor
    from ...items import Shapez2Item
    from ...locations import Shapez2Location
    from ..rules import extended_has_all

    def get_rule(proc_: tuple[str, ...]) -> "AccessRule":
        if proc_ not in processor_rules_dict:
            processor_rules_dict[proc_] = lambda state: extended_has_all(world, state, *proc_)
        return processor_rules_dict[proc_]

    reg = regions["Events"]
    lines = world.operator_processors
    all_unlocked = "Lock operator lines" not in world.options.location_modifiers
    tab_unlocked = "Lock operator levels tab" not in world.options.location_modifiers

    if tab_unlocked or "Operator Levels" in world.starting_items:
        world.starting_items.append("[ACCESS] Operator levels")
    else:
        loc = Shapez2Location(
            world.player, "[ACCESS] Operator levels", None, reg, LocationProgressType.PRIORITY,
            lambda state: state.has("Operator Levels", world.player)
        )
        loc.place_locked_item(Shapez2Item(
            "[ACCESS] Operator levels", ItemClassification.progression, None, world.player
        ))
        reg.locations.append(loc)

    for x in range(len(lines)):
        proc = tuple(event_by_processor[p] for p in lines[x])
        if all_unlocked or all(p in world.starting_items for p in proc):
            world.starting_items.append(f"[ACCESS] Operator line {x+1}")
        else:
            loc = Shapez2Location(
                world.player, f"[ACCESS] Operator line {x+1}", None, reg, LocationProgressType.PRIORITY,
                get_rule(proc)
            )
            loc.place_locked_item(Shapez2Item(
                f"[ACCESS] Operator line {x+1}", ItemClassification.progression, None, world.player
            ))
            reg.locations.append(loc)
