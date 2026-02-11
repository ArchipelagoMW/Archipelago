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
    milestones = world.milestone_processors

    for x in range(len(milestones)):
        proc = tuple(event_by_processor[p] for p in milestones[x])
        if all(p in world.starting_items for p in proc):
            world.starting_items.append(f"[ACCESS] Milestone {x+1}")
        else:
            loc = Shapez2Location(
                world.player, f"[ACCESS] Milestone {x+1}", None, reg, LocationProgressType.PRIORITY,
                get_rule(proc)
            )
            loc.place_locked_item(Shapez2Item(
                f"[ACCESS] Milestone {x+1}", ItemClassification.progression, None, world.player
            ))
            reg.locations.append(loc)
