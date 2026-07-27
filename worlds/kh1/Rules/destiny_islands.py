from rule_builder.field_resolvers import FromOption
from rule_builder.rules import Has, Rule

from ..Options import Day2Materials
from ._context import RuleContext


def build_rules(ctx: RuleContext, enabled: bool) -> dict[str, Rule]:
    raft_materials_rule = Has("Raft Materials", count=FromOption(Day2Materials))

    return {
        "Destiny Islands Seashore Capture Fish 1 (Day 2)": raft_materials_rule,
        "Destiny Islands Seashore Capture Fish 2 (Day 2)": raft_materials_rule,
        "Destiny Islands Seashore Capture Fish 3 (Day 2)": raft_materials_rule,
        "Destiny Islands Seashore Gather Seagull Egg (Day 2)": raft_materials_rule,
        "Destiny Islands Secret Place Gather Mushroom (Day 2)": raft_materials_rule,
        "Destiny Islands Cove Gather Mushroom Near Zip Line (Day 2)": raft_materials_rule,
        "Destiny Islands Cove Gather Mushroom in Small Cave (Day 2)": raft_materials_rule,
        "Destiny Islands Cove Talk to Kairi (Day 2)": raft_materials_rule,
        "Destiny Islands Gather Drinking Water (Day 2)": raft_materials_rule,
        "Destiny Islands Chest": raft_materials_rule,
    } if enabled else {}
