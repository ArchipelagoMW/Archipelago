from rule_builder.field_resolvers import FromOption
from rule_builder.rules import Has, Rule

from ..Options import Day1Materials, Day2Materials


def build_rules() -> dict[str, Rule]:
    day_1_materials_rule = Has("Raft Materials", count=FromOption(Day1Materials))
    day_2_materials_rule = Has("Raft Materials", count=FromOption(Day2Materials))

    return {
        "Destiny Islands Seashore Capture Fish 1 (Day 2)": day_1_materials_rule,
        "Destiny Islands Seashore Capture Fish 2 (Day 2)": day_1_materials_rule,
        "Destiny Islands Seashore Capture Fish 3 (Day 2)": day_1_materials_rule,
        "Destiny Islands Seashore Gather Seagull Egg (Day 2)": day_1_materials_rule,
        "Destiny Islands Secret Place Gather Mushroom (Day 2)": day_1_materials_rule,
        "Destiny Islands Cove Gather Mushroom Near Zip Line (Day 2)": day_1_materials_rule,
        "Destiny Islands Cove Gather Mushroom in Small Cave (Day 2)": day_1_materials_rule,
        "Destiny Islands Cove Talk to Kairi (Day 2)": day_1_materials_rule,
        "Destiny Islands Gather Drinking Water (Day 2)": day_1_materials_rule & Has("Empty Bottle"),
        "Destiny Islands Chest": day_1_materials_rule,
        "Destiny Islands Gather Coconut (Day 2)": day_1_materials_rule,
        "Destiny Islands Seashore Talk to Kairi Potion Reward (Day 1)": day_1_materials_rule,
        "Destiny Islands Seashore Talk to Kairi Hi-Potion Reward (Day 1)": day_1_materials_rule,
        "Destiny Islands Cove Race Riku (Day 2)": day_1_materials_rule,
        "Destiny Islands Cove Talk to Kairi Potion Reward (Day 2)": day_2_materials_rule,
        "Destiny Islands Cove Talk to Kairi Hi-Potion Reward (Day 2)": day_2_materials_rule,
    }
