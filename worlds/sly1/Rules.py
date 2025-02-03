from worlds.generic.Rules import add_rule, set_rule
from .Types import episode_type_to_shortened_name
from .Locations import hourglass_locations, vault_locations, did_include_hourglasses, get_bundle_amount_for_level, bottle_amounts, strip_hourglass_from_keys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Sly1World

def set_rules(world: "Sly1World"):
    # Episode Access
    add_rule(world.multiworld.get_entrance("Hideout -> Stealthy Approach", world.player),
             lambda state: state.has("Tide of Terror", world.player))
    add_rule(world.multiworld.get_entrance("Hideout -> Rocky Start", world.player),
             lambda state: state.has("Sunset Snake Eyes", world.player))
    add_rule(world.multiworld.get_entrance("Hideout -> Dread Swamp Path", world.player),
             lambda state: state.has("Vicious Voodoo", world.player))
    add_rule(world.multiworld.get_entrance("Hideout -> Perilous Ascent", world.player),
             lambda state: state.has("Fire in the Sky", world.player))
    
    # Main Hub Access
    add_rule(world.multiworld.get_entrance("Hideout -> Prowling the Grounds", world.player),
             lambda state: state.has("ToT Key", world.player)
             and state.has("Tide of Terror", world.player))
    add_rule(world.multiworld.get_entrance("Hideout -> Muggshot's Turf", world.player),
             lambda state: state.has("SSE Key", world.player)
             and state.has("Sunset Snake Eyes", world.player))
    add_rule(world.multiworld.get_entrance("Hideout -> Swamp's Dark Center", world.player),
             lambda state: state.has("VV Key", world.player)
             and state.has("Vicious Voodoo", world.player))
    add_rule(world.multiworld.get_entrance("Hideout -> Inside the Stronghold", world.player),
             lambda state: state.has("FitS Key", world.player)
             and state.has("Fire in the Sky", world.player))
    
    add_rule(world.multiworld.get_entrance("Stealthy Approach -> Prowling the Grounds", world.player),
             lambda state: state.has("ToT Key", world.player))
    add_rule(world.multiworld.get_entrance("Rocky Start -> Muggshot's Turf", world.player),
             lambda state: state.has("SSE Key", world.player))
    add_rule(world.multiworld.get_entrance("Dread Swamp Path -> Swamp's Dark Center", world.player),
             lambda state: state.has("VV Key", world.player))
    add_rule(world.multiworld.get_entrance("Perilous Ascent -> Inside the Stronghold", world.player),
             lambda state: state.has("FitS Key", world.player))
    
    # Hub 2 Access
    add_rule(world.multiworld.get_entrance("Prowling the Grounds -> Prowling the Grounds - Second Gate", world.player),
             lambda state: state.has("ToT Key", world.player, 3))
    add_rule(world.multiworld.get_entrance("Muggshot's Turf -> Muggshot's Turf - Second Gate", world.player),
             lambda state: state.has("SSE Key", world.player, 3))
    add_rule(world.multiworld.get_entrance("Swamp's Dark Center -> Swamp's Dark Center - Second Gate", world.player),
             lambda state: state.has("VV Key", world.player, 3))
    add_rule(world.multiworld.get_entrance("Inside the Stronghold -> Inside the Stronghold - Second Gate", world.player),
             lambda state: state.has("FitS Key", world.player, 3))
    
    # Boss Access
    add_rule(world.multiworld.get_entrance("Prowling the Grounds - Second Gate -> Eye of the Storm", world.player),
             lambda state: state.has("ToT Key", world.player, 7))
    add_rule(world.multiworld.get_entrance("Muggshot's Turf - Second Gate -> Last Call", world.player),
             lambda state: state.has("SSE Key", world.player, 7))
    add_rule(world.multiworld.get_entrance("Swamp's Dark Center - Second Gate -> Deadly Dance", world.player),
             lambda state: state.has("VV Key", world.player, 7))
    add_rule(world.multiworld.get_entrance("Inside the Stronghold - Second Gate -> Flame Fu!", world.player),
             lambda state: state.has("FitS Key", world.player, 7))
    
    set_rule(world.multiworld.get_entrance("Hideout -> Cold Heart of Hate", world.player),
             lambda state: state.has("Beat Raleigh", world.player)
             and state.has("Beat Muggshot", world.player)
             and state.has("Beat Mz. Ruby", world.player)
             and state.has("Beat Panda King", world.player))
    
    # Hourglass Rules
    if did_include_hourglasses(world):
        for key, data in hourglass_locations.items():
            loc = world.multiworld.get_location(key, world.player)
            add_rule(loc, lambda state: state.has(f'{episode_type_to_shortened_name[data.key_type]} Key', world.player, data.key_requirement))

        add_rule(world.multiworld.get_location("Unseen Foe Hourglass", world.player),
             lambda state: state.has("Progressive Invisibility", world.player, 1))

    # Extra rules for Unseen Foe
    add_rule(world.multiworld.get_location("Unseen Foe Key", world.player),
             lambda state: state.has("Progressive Invisibility", world.player, 1))
    add_rule(world.multiworld.get_location("Unseen Foe Vault", world.player),
             lambda state: state.has("Progressive Invisibility", world.player, 1))
    for location in world.multiworld.get_locations(world.player):
        if "Unseen Foe" in location.name and "Bottle" in location.name:
            add_rule(location, lambda state: state.has("Progressive Invisibility", world.player, 1))
    
    # Cluesanity rules
    if world.options.CluesanityBundleSize.value > 0:
        for name, data in vault_locations.items():
            level_name = name.rsplit(' ', 1)[0]
            bundle_amount = get_bundle_amount_for_level(world, level_name)
            bottle_name = f'{level_name} Bottle(s)'
            
            set_rule(world.multiworld.get_location(name, world.player),
                     lambda state, bn=bottle_name, ba=bundle_amount: state.has(bn, world.player, ba))

        for name, data in hourglass_locations.items():
            level_name = name.rsplit(' ', 1)[0]
            bundle_amount = get_bundle_amount_for_level(world, level_name)
            bottle_name = f'{level_name} Bottle(s)'

            set_rule(world.multiworld.get_location(name, world.player),
                     lambda state, bn=bottle_name, ba=bundle_amount: state.has(bn, world.player, ba))

    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)