from typing import Any

from . import build_rule_dicts


def export_rules_to_dict(kh1world) -> dict[str, Any]:
    location_rules, entrance_rules = build_rule_dicts(kh1world)
    return {
        "locations": {name: rule.to_dict() for name, rule in location_rules.items()},
        "entrances": {name: rule.to_dict() for name, rule in entrance_rules.items()},
    }
