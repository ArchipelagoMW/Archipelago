from typing import NamedTuple


class CostTerm(NamedTuple):
    term: str
    option: str
    singular: str
    plural: str
    weight: int  # CostSanity
    sort: int


cost_terms = {x.term: x for x in (
    CostTerm("RANCIDEGGS", "Egg", "Rancid Egg", "Rancid Eggs", 1, 3),
    CostTerm("GRUBS", "Grub", "Grub", "Grubs", 1, 2),
    CostTerm("ESSENCE", "Essence", "Essence", "Essence", 1, 4),
    CostTerm("CHARMS", "Charm", "Charm", "Charms", 1, 1),
    CostTerm("GEO", "Geo", "Geo", "Geo", 8, 9999),
)}
