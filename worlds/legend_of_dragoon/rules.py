from ..generic.Rules import set_rule, add_rule
from ..AutoWorld import World

def lod_set_rule(lod_world: World, location: str, rule):
    player = lod_world.player

    locations = lod_world.created_multi_locations.get(location)
    if locations is None:
        try:
            locations = [lod_world.multiworld.get_location(location, player)]
        except KeyError:
            return

    for location in locations:
        set_rule(location, rule)

def set_rules(lod_world: World):
    player = lod_world.player
    set_generated_rules(lod_world, lod_set_rule)

    for location in lod_world.multiworld.get_locations(player):
        if location.costs:
            for term, amount in location.costs.items():
                add_rule(location, lambda state, term=term, amount=amount: state.count(term, player) >= amount)


