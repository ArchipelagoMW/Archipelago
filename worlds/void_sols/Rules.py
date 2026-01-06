from BaseClasses import MultiWorld
from .Names import LocationName, ItemName
from worlds.AutoWorld import World
from worlds.generic.Rules import add_rule, set_rule

def set_rules(world: World):
    player = world.player
    
    # Helper functions
    def can_light_fire(state):
        return state.has(ItemName.flaming_torch_x1, player) or \
               state.has(ItemName.flaming_torch_x2, player) or \
               state.has(ItemName.fire_talisman, player)

    # Victory condition: Defeat Zenith and interact with world light spark
    world.multiworld.completion_condition[player] = lambda state: state.has(ItemName.victory, player)

    # Place Victory item at world spark beyond Zenith
    world.multiworld.get_location(LocationName.apex_world_spark_interacted, player).place_locked_item(world.create_item(ItemName.victory))

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
        LocationName.prison_wall_entry_hall
    ]

    for loc_name in prison_locked_locations:
        set_rule(world.multiworld.get_location(loc_name, player), lambda state: state.has(ItemName.prison_key, player))

    # Furnace Rule
    set_rule(world.multiworld.get_location(LocationName.prison_yard_misc_furnace, player), can_light_fire)

    # Gate Key Rule
    gate_locked_items = [
        LocationName.prison_yard_torch_prisoner_intake,
        LocationName.prison_yard_torch_stables,
    ]

    for loc in gate_locked_items:
        set_rule(world.multiworld.get_location(loc, player), lambda state: state.has(ItemName.gate_key, player))

    # --- Forest Rules ---
    # Riverside Shack (Fishing Rod)
    set_rule(world.multiworld.get_location(LocationName.forest_item_pickup_fishing_rod, player),
             lambda state: state.has(ItemName.riverside_shack_key, player))

    # Items locked behind the forest bridge (Forest Bridge Key Needed)
    forest_bridge_locations = [
        LocationName.forest_poacher_defeated,
        LocationName.forest_item_pickup_major_sol_shard_4,
        LocationName.forest_item_pickup_alchemist_cage_key,
    ]

    for loc in forest_bridge_locations:
        set_rule(world.multiworld.get_location(loc, player),
                 lambda state: state.has(ItemName.forest_bridge_key, player))
        
    # Apex Horn Rule
    set_rule(world.multiworld.get_location(LocationName.apex_blow_horn, player), lambda state: state.has(ItemName.blizzard_talisman))

    # Trader Rules
    # Trader appears when the campfire is lit.
    
    # 1. Trader Trades (Require Fire + Specific Fish)
    fish_trades = {
        LocationName.forest_trader_trade_star_fish: ItemName.star_fish,
        LocationName.forest_trader_trade_upstream_fish: ItemName.upstream_fish,
        LocationName.forest_trader_trade_deep_fish: ItemName.deep_fish,
        LocationName.forest_trader_trade_glitch_fish: ItemName.glitch_fish,
        LocationName.forest_trader_trade_flying_fish: ItemName.flying_fish,
        LocationName.forest_trader_trade_sick_fish: ItemName.sick_fish,
        LocationName.forest_trader_trade_frog_fish: ItemName.frog_fish,
        LocationName.forest_trader_trade_rich_fish: ItemName.rich_fish,
        LocationName.forest_trader_trade_oceanic_fish: ItemName.oceanic_fish,
    }

    for loc, fish_item in fish_trades.items():
        set_rule(world.multiworld.get_location(loc, player),
                 lambda state: can_light_fire(state) and state.has(fish_item, player))

    # 2. Trader Items (Require Fire + Fish Tokens)
    # Fish Tokens come in packs of 2 (ItemName.fish_tokens_x2)
    # Costs:
    # - Major Sol Shard #35: 2 tokens
    # - Major Sol Shard #36: 2 tokens
    # - Potions Increased: 4 tokens
    # - Condemned Shack Key: 3 tokens
    # - Frying Pan: 4 tokens
    # - Silver Pouch: 3 tokens

    trader_items_costs = {
        LocationName.forest_trader_item_major_sol_shard_35: 2,
        LocationName.forest_trader_item_major_sol_shard_36: 2,
        LocationName.forest_trader_item_potions_increased: 4,
        LocationName.forest_trader_item_condemned_shack_key: 3,
        LocationName.forest_trader_item_frying_pan: 4,
        LocationName.forest_trader_item_silver_pouch: 3,
    }

    for loc, cost in trader_items_costs.items():
        # Note: fish_tokens_x2 gives 2 tokens. We need to check if player has enough tokens.
        # Since the item is "Fish Tokens x2", state.count(ItemName.fish_tokens_x2, player) returns the number of items,
        # so total tokens = count * 2.
        set_rule(world.multiworld.get_location(loc, player),
                 lambda state, c=cost: can_light_fire(state) and (state.count(ItemName.fish_tokens_x2, player) * 2) >= c)

    # --- Village Rules ---

    # Poacher Rewards (Mines Lift Key, Mountain Outpost Key)
    # Accessible after beating Poacher (requires Forest Bridge Key)
    poacher_rewards = [
        LocationName.village_item_pickup_mines_lift_key,
        LocationName.village_item_pickup_mountain_outpost_key,
        LocationName.forest_item_pickup_alchemist_cage_key
    ]
    for loc in poacher_rewards:
        set_rule(world.multiworld.get_location(loc, player),
                 lambda state: state.has(ItemName.forest_poacher_defeated_event, player))

    # Condemned Shack (Iron Pineapple, Strange Totem)
    condemned_shack_items = [
        LocationName.village_item_pickup_iron_pineapple,
        LocationName.village_item_pickup_strange_totem,
    ]
    for loc in condemned_shack_items:
        set_rule(world.multiworld.get_location(loc, player),
                 lambda state: state.has(ItemName.condemned_shack_key, player))

    # Quiver of Holding (Village)
    # Locked by getting to the first level of the mines (Mines Lift Key)
    set_rule(world.multiworld.get_location(LocationName.village_item_pickup_quiver_of_holding, player),
             lambda state: state.has(ItemName.mine_entrance_lift_key, player))

    # Alchemist Upgrades (Village)
    # Requires freeing the alchemist (Forest Bridge Key + Alchemist Cage Key) AND Potion Mixing Unlocked
    alchemist_upgrades = [
        LocationName.village_alchemist_upgrade_1,
        LocationName.village_alchemist_upgrade_2,
        LocationName.village_alchemist_upgrade_3,
    ]
    
    for loc in alchemist_upgrades:
        location = world.multiworld.get_location(loc, player)
        set_rule(location,
                 lambda state: state.has(ItemName.forest_bridge_key, player) and
                               state.has(ItemName.alchemist_cage_key, player) and
                               state.has(ItemName.potion_mixing_unlocked, player))
        # Item Restriction: Cannot be Sol Alembic
        location.item_rule = lambda item: item.name != ItemName.sol_alembic

    # Blacksmith Upgrades (Village)
    # Item Restriction: Cannot be Metamorphic Alloy
    blacksmith_upgrades = [
        LocationName.village_blacksmith_upgrade_1,
        LocationName.village_blacksmith_upgrade_2,
        LocationName.village_blacksmith_upgrade_3,
    ]

    for loc in blacksmith_upgrades:
        location = world.multiworld.get_location(loc, player)
        location.item_rule = lambda item: item.name != ItemName.metamorphic_alloy

    # Relics Improved (Village Undercroft Forgotten Reliquary)
    # Requires Strange Curios.
    # There are 4 Strange Curios in the world.
    # Slots 1-4 require 1, 2, 3, 4 Curios respectively (progressive).
    # Slot 5 opens after all 4 are turned in, so it also requires 4.
    # Locations requiring 4 Curios cannot contain a Strange Curio to prevent softlocks.
    
    relics_improved_map = {
        LocationName.village_relics_improved_1: 1,
        LocationName.village_relics_improved_2: 2,
        LocationName.village_relics_improved_3: 3,
        LocationName.village_relics_improved_4: 4,
        LocationName.village_relics_improved_5: 4,
    }

    for loc, count in relics_improved_map.items():
        location = world.multiworld.get_location(loc, player)
        set_rule(location, lambda state, c=count: state.has(ItemName.strange_curio, player, c))
        
        # Prevent Strange Curio from being placed in locations requiring 4 Curios
        if count == 4:
            add_rule(location, lambda state: True)
            location.item_rule = lambda item: item.name != ItemName.strange_curio

    # --- Boss Events ---
    # Place Event Items on Event Locations
    
    # Warden
    world.multiworld.get_location(LocationName.prison_warden_defeated_event, player).place_locked_item(
        world.create_item(ItemName.prison_warden_defeated_event))
    # Rule: Can reach the physical boss location (which requires Prison Key)
    set_rule(world.multiworld.get_location(LocationName.prison_warden_defeated_event, player),
             lambda state: state.has(ItemName.prison_key, player))

    # Poacher
    world.multiworld.get_location(LocationName.forest_poacher_defeated_event, player).place_locked_item(
        world.create_item(ItemName.forest_poacher_defeated_event))
    # Rule: Can reach the physical boss location (which requires Forest Bridge Key)
    set_rule(world.multiworld.get_location(LocationName.forest_poacher_defeated_event, player),
             lambda state: state.has(ItemName.forest_bridge_key, player))

    # Groundskeeper
    world.multiworld.get_location(LocationName.mountain_groundskeeper_defeated_event, player).place_locked_item(
        world.create_item(ItemName.mountain_groundskeeper_defeated_event))
    # Rule: Can reach the physical boss location (Mountain Outpost Key)
    set_rule(world.multiworld.get_location(LocationName.mountain_groundskeeper_defeated_event, player),
             lambda state: state.has(ItemName.mountain_outpost_key, player))

    # Greater Void Worm
    world.multiworld.get_location(LocationName.mines_worm_defeated_event, player).place_locked_item(
        world.create_item(ItemName.greater_void_worm_defeated_event))
    # Rule: Can reach the physical boss location (Pit Catwalk Key)
    set_rule(world.multiworld.get_location(LocationName.mines_worm_defeated_event, player),
             lambda state: state.has(ItemName.pit_catwalk_key, player))

    # Amalgamate
    world.multiworld.get_location(LocationName.cultist_amalgamate_defeated_event, player).place_locked_item(
        world.create_item(ItemName.cultist_amalgamate_defeated_event))
    # Rule: Can reach the physical boss location (Central Cell Key + Minor Cell Key)
    set_rule(world.multiworld.get_location(LocationName.cultist_amalgamate_defeated_event, player),
             lambda state: state.has(ItemName.central_cell_key, player) and state.has(ItemName.minor_cell_key, player)
                           and state.has(ItemName.false_book, player))

    # Infernal Warden
    world.multiworld.get_location(LocationName.supermax_prison_infernal_warden_defeated_event, player).place_locked_item(
        world.create_item(ItemName.supermax_prison_infernal_warden_defeated_event))
    # Rule: Can reach the physical boss location (Greater Void Worm Defeated)
    set_rule(world.multiworld.get_location(LocationName.supermax_prison_infernal_warden_defeated_event, player),
             lambda state: state.has(ItemName.greater_void_worm_defeated_event, player))

    # Immaculate
    world.multiworld.get_location(LocationName.factory_immaculate_defeated_event, player).place_locked_item(
        world.create_item(ItemName.factory_immaculate_defeated_event))
    # Rule: Can reach the physical boss location (Poacher Defeated)
    set_rule(world.multiworld.get_location(LocationName.factory_immaculate_defeated_event, player),
             lambda state: state.has(ItemName.forest_poacher_defeated_event, player))

    # Gatekeeper
    world.multiworld.get_location(LocationName.apex_gatekeeper_defeated_event, player).place_locked_item(
        world.create_item(ItemName.apex_gatekeeper_defeated_event))
    # Rule: Can reach the physical boss location (Apex Outskirts Key)
    set_rule(world.multiworld.get_location(LocationName.apex_gatekeeper_defeated_event, player),
             lambda state: state.has(ItemName.apex_outskirts_key, player))

    # Zenith
    world.multiworld.get_location(LocationName.apex_zenith_defeated_event, player).place_locked_item(
        world.create_item(ItemName.apex_zenith_defeated_event))
    # Rule: Can reach the physical boss location (Gatekeeper Defeated)
    set_rule(world.multiworld.get_location(LocationName.apex_zenith_defeated_event, player),
             lambda state: state.has(ItemName.apex_gatekeeper_defeated_event, player))


    # Mines 1F Map requires Minecart Wheel
    set_rule(world.multiworld.get_location(LocationName.mines_item_pickup_map_1, player),
                 lambda state: state.has(ItemName.minecart_wheel, player))

    # Mines 3F Pit Catwalk Key Rules
    # These locations are locked behind the door requiring the Pit Catwalk Key
    mines_pit_catwalk_locked_locations = [
        LocationName.mines_item_pickup_courage_hero,
        LocationName.mines_item_pickup_map_3,
        LocationName.mines_item_pickup_crossbow,
        LocationName.mines_item_pickup_lightning_talisman,
        LocationName.mines_fish_star,
        LocationName.mines_torch_condemned_lift,
        LocationName.mines_torch_mining_frontier,
    ]

    for loc_name in mines_pit_catwalk_locked_locations:
        set_rule(world.multiworld.get_location(loc_name, player), lambda state: state.has(ItemName.pit_catwalk_key, player))

    # Mines 4F Temple of the Deep Key Rules
    mines_temple_locked_locations = [
        LocationName.mines_wall_puzzle_half,
        LocationName.mines_torch_restricted_cultist_reliquary,
    ]
    for loc_name in mines_temple_locked_locations:
        set_rule(world.multiworld.get_location(loc_name, player), lambda state: state.has(ItemName.temple_of_the_deep_key, player))

    # Cultist Compound False Book Rules
    cultist_false_book_locked_locations = [
        LocationName.cultist_torch_forbidden_study,
        LocationName.cultist_compound_item_pickup_brass_knuckles,
    ]
    for loc_name in cultist_false_book_locked_locations:
        set_rule(world.multiworld.get_location(loc_name, player), lambda state: state.has(ItemName.false_book, player))

    # Cultist Compound Central Cell Key Rules
    cultist_central_cell_locked_locations = [
        LocationName.cultist_compound_item_pickup_guile_rogue,
        LocationName.cultist_compound_item_pickup_purifying_needle,
    ]
    for loc_name in cultist_central_cell_locked_locations:
        set_rule(world.multiworld.get_location(loc_name, player), lambda state: state.has(ItemName.central_cell_key, player))

    # Cultist Compound Minor Cell Key Rules
    cultist_minor_cell_locked_locations = [
        LocationName.cultist_compound_item_pickup_metamorphic_alloy,
        LocationName.cultist_compound_item_pickup_central_cell_key,
        LocationName.cultist_torch_infinity_chasm,
        LocationName.cultist_compound_wall_elevator,
        LocationName.cultist_compound_item_pickup_garnet_aegis,
    ]
    for loc_name in cultist_minor_cell_locked_locations:
        set_rule(world.multiworld.get_location(loc_name, player), lambda state: state.has(ItemName.minor_cell_key, player))

    # Cultist Compound Sol Forge Lab Key Rule
    set_rule(world.multiworld.get_location(LocationName.cultist_compound_item_pickup_sol_forge_lab_key, player),
             lambda state: state.has(ItemName.central_cell_key, player) and state.has(ItemName.minor_cell_key, player))

    # Cultist Tamper Armament Rule
    set_rule(world.multiworld.get_location(LocationName.cultist_tamper_armament, player),
             lambda state: state.has(ItemName.sol_forge_lab_key, player) and state.has(ItemName.minor_cell_key, player))

    # Cultist Amalgamate Defeated Rule
    set_rule(world.multiworld.get_location(LocationName.cultist_compound_item_pickup_sol_forge_lab_key , player),
             lambda state: state.has(ItemName.central_cell_key, player) and state.has(ItemName.minor_cell_key, player))

    # Mushroom Access Rules
    # These locations require at least one mushroom to access
    mushroom_access_locations = [
        LocationName.mountain_item_pickup_mushroom,
        LocationName.mines_item_pickup_mushroom,
        LocationName.swamp_item_pickup_mushroom,
    ]

    for loc_name in mushroom_access_locations:
        set_rule(world.multiworld.get_location(loc_name, player), lambda state: state.has(ItemName.mysterious_mushroom_x1, player))
