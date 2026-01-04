from BaseClasses import MultiWorld
from .Names import LocationName, ItemName
from worlds.AutoWorld import World
from worlds.generic.Rules import add_rule, set_rule

def set_rules(world: World):
    player = world.player
    
    # Victory condition: Defeat Zenith
    world.multiworld.completion_condition[player] = lambda state: state.has(ItemName.victory, player)

    # Place Victory item at world spark beyond Zenith
    world.multiworld.get_location(LocationName.apex_world_spark_interacted, player).place_locked_item(world.create_item(ItemName.victory))

    # For now, we rely on region connections for general access.

    # Fishing Rules
    fish_locations = [
        LocationName.forest_fish_upstream,
        LocationName.mountain_underpass_fish_oceanic,
        LocationName.mountain_fish_flying,
        LocationName.cultist_compound_fish_deep,
        LocationName.mines_fish_star,
        LocationName.apex_fish_rich,
        LocationName.apex_fish_glitch,
        LocationName.swamp_fish_frog,
        LocationName.swamp_fish_sick,
    ]

    for fish_loc in fish_locations:
        set_rule(world.multiworld.get_location(fish_loc, player), lambda state: state.has(ItemName.fishing_rod, player))

    # Relic of Mycology Rule
    # Requires 5 mushrooms to access. Silver Pouch acts as +1 mushroom count.
    set_rule(world.multiworld.get_location(LocationName.forest_item_pickup_relic_mycology, player),
             lambda state: state.has(ItemName.mysterious_mushroom_x1, player, 5) or
                           (state.has(ItemName.mysterious_mushroom_x1, player, 4) and state.has(ItemName.silver_pouch, player)))

    # Prison Key Rules
    # The Prison Key unlocks a door in the Prison.
    # Locations behind this door need the Prison Key.
    prison_locked_locations = [
        LocationName.prison_item_pickup_ruby_phial,
        LocationName.prison_torch_entry_hall,
        LocationName.prison_item_pickup_map_b,
        LocationName.prison_spark_entry_hall,
        LocationName.prison_warden_defeated,
    ]

    for loc_name in prison_locked_locations:
        set_rule(world.multiworld.get_location(loc_name, player), lambda state: state.has(ItemName.prison_key, player))

    # Furnace Rule
    set_rule(world.multiworld.get_location(LocationName.prison_yard_misc_furnace, player),
             lambda state: state.has(ItemName.flaming_torch_x1, player) or state.has(ItemName.flaming_torch_x2, player)
             or state.has(ItemName.fire_talisman, player))

    # Apex Horn Rule
    set_rule(world.multiworld.get_location(LocationName.apex_blow_horn, player), lambda state: state.has(ItemName.blizzard_talisman))
