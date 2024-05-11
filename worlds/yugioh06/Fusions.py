from typing import List, NamedTuple


class FusionData(NamedTuple):
    name: str
    materials: List[str]
    replaceable: bool
    additional_spells: List[str]


fusions = {
    "Elemental Hero Flame Wingman": FusionData(
        "Elemental Hero Flame Wingman",
        ["Elemental Hero Avian", "Elemental Hero Burstinatrix"],
        True,
        ["Miracle Fusion"]),
    "Elemental Hero Madballman": FusionData(
        "Elemental Hero Madballman",
        ["Elemental Hero Bubbleman", "Elemental Hero Clayman"],
        True,
        ["Miracle Fusion"]),
    "Elemental Hero Rampart Blaster": FusionData(
        "Elemental Hero Rampart Blaster",
        ["Elemental Hero Burstinatrix", "Elemental Hero Clayman"],
        True,
        ["Miracle Fusion"]),
    "Elemental Hero Shining Flare Wingman": FusionData(
        "Elemental Hero Shining Flare Wingman",
        ["Elemental Hero Flame Wingman", "Elemental Hero Sparkman"],
        True,
        ["Miracle Fusion"]),
    "Elemental Hero Steam Healer": FusionData(
        "Elemental Hero Steam Healer",
        ["Elemental Hero Burstinatrix", "Elemental Hero Bubbleman"],
        True,
        ["Miracle Fusion"]),
    "Elemental Hero Wildedge": FusionData(
        "Elemental Hero Wildedge",
        ["Elemental Hero Wildheart", "Elemental Hero Bladedge"],
        True,
        ["Miracle Fusion"])
}

fusion_subs = ["The Dark - Hex-Sealed Fusion",
               "The Earth - Hex-Sealed Fusion",
               "The Light - Hex-Sealed Fusion",
               "Goddess with the Third Eye",
               "King of the Swamp",
               "Versago the Destroyer",
               # Only in All-packs
               "Beastking of the Swamps",
               "Mystical Sheep #1"]


def has_all_materials(state, monster, player):
    data = fusions.get(monster)
    if not state.has(monster, player):
        return False
    if data is None:
        return True
    else:
        materials = data.replaceable and state.has_any(fusion_subs, player)
        for material in data.materials:
            materials += has_all_materials(state, material, player)
        return materials >= len(data.materials)


def count_has_materials(state, monsters, player):
    amount = 0
    for monster in monsters:
        amount += has_all_materials(state, monster, player)
    return amount
