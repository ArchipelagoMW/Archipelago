
from . import RegionConnectionData, ExtendedRule
from ..generate.rules import extended_has, extended_has_from_list_unique


def get_milestone_rule(x: int) -> ExtendedRule:
    return lambda state, world: extended_has(world, state, f"[ACCESS] Milestone {x}")


def get_task_line_rule(x: int) -> ExtendedRule:
    return lambda state, world: extended_has(world, state, f"[ACCESS] Task line {x}")


def get_operator_section_rule(x: int) -> ExtendedRule:
    rule: ExtendedRule = lambda state, world: extended_has_from_list_unique(
        world, state, x,
        *(f"[ACCESS] Operator line {y}" for y in range(1, world.options.location_adjustments["Operator lines"] + 1))
    )
    if x != 1:
        return rule
    else:
        return lambda state, world: extended_has(world, state, "[ACCESS] Operator levels") and rule(state, world)


connections: dict[str, RegionConnectionData] = {
    "To Events": RegionConnectionData("Menu", "Events", None),
    "To Milestone 1": RegionConnectionData("Menu", "Milestone 1", get_milestone_rule(1)),
    "To Operator levels (section 1)": RegionConnectionData(
        "Menu", "Operator levels (section 1)",
        get_operator_section_rule(1)
    ),
} | {
    f"To Milestone {x}": RegionConnectionData(
        f"Milestone {x-1}",
        f"Milestone {x}",
        get_milestone_rule(x)
    ) for x in range(2, 21)
} | {
    f"To Task line {x}": RegionConnectionData(
        "Menu",
        f"Task line {x}",
        get_task_line_rule(x)
    ) for x in range(1, 201)
} | {
    f"To Operator levels (section {x})": RegionConnectionData(
        f"Operator levels (section {x-1})",
        f"Operator levels (section {x})",
        get_operator_section_rule(x)
    ) for x in range(2, 41)
}
