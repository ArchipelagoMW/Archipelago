from worlds.generic.Rules import set_rule
from BaseClasses import MultiWorld


items = ["Map Width", "Map Height", "Map Bombs"]


# Sets rules on entrances and advancements that are always applied
def set_rules(multiworld: MultiWorld, player: int):
    for i in range(20):
        set_rule(multiworld.get_location(f"Tile {i+6}", player), lambda state, i=i: state.has_from_list(items, player, i+1))


# Sets rules on completion condition
def set_completion_rules(multiworld: MultiWorld, player: int):
    width_req = 5  # 10 - 5
    height_req = 5  # 10 - 5
    bomb_req = 15  # 20 - 5
    multiworld.completion_condition[player] = lambda state: state.has_all_counts(
        {
            "Map Width": width_req,
            "Map Height": height_req,
            "Map Bombs": bomb_req,
        }, player)
