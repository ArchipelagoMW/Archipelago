from Options import Toggle

from .RulesData import location_rules

options = {
    "open" : Toggle,
    "openworld": Toggle
}

for logic_set in location_rules:
    if logic_set != "casual-core":
        options[logic_set.replace("-", "_")] = Toggle
