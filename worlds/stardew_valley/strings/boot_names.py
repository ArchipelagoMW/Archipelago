from typing import Dict, List

boots_by_tier: Dict[int, List[str]] = dict()
tier_by_boots: Dict[str, int] = dict()


def create_boots(tier: int, name: str) -> str:
    if tier not in boots_by_tier:
        boots_by_tier[tier] = []
    boots_by_tier[tier].append(name)
    tier_by_boots[name] = tier
    return name


def tier_4_boots(name: str) -> str:
    return create_boots(4, name)


class Boots:
    mermaid_boots = tier_4_boots("Mermaid Boots")
