from .Names import LocationName, ItemName
from worlds.AutoWorld import World
from worlds.generic.Rules import add_rule, set_rule

# Helper functions
def can_light_fire(state, player):
    return state.has(ItemName.flaming_torch_x1, player) or \
           state.has(ItemName.flaming_torch_x2, player) or \
           state.has(ItemName.fire_talisman, player)

def can_blow_up_wall(state, player):
    return state.has(ItemName.dynamite_x1, player) or state.has(ItemName.mine_entrance_lift_key, player)

def set_rules(world: World):
    player = world.player
    
    # Victory condition: Defeat Zenith and interact with world light spark
    world.multiworld.completion_condition[player] = lambda state: state.has(ItemName.victory, player)

    # Place Victory item at world spark beyond Zenith
    try:
        set_rule(world.multiworld.get_location(LocationName.apex_world_spark_interacted, player),
                 lambda state: state.has(ItemName.apex_zenith_defeated_event, player))
    except KeyError:
        pass

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
        try:
            set_rule(world.multiworld.get_location(fish_loc, player), lambda state: state.has(ItemName.fishing_rod, player))
        except KeyError:
            pass

    # Relic of Mycology Rule
    # Requires 5 mushrooms to access. Silver Pouch acts as +1 mushroom count.
    try:
        set_rule(world.multiworld.get_location(LocationName.forest_item_pickup_relic_mycology, player),
                 lambda state: state.has(ItemName.mysterious_mushroom_x1, player, 5) or
                               (state.has(ItemName.mysterious_mushroom_x1, player, 4) and state.has(ItemName.silver_pouch, player)))
    except KeyError:
        pass

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
        # Check if location exists (it might be disabled by options)
        try:
            location = world.multiworld.get_location(loc_name, player)
            set_rule(location, lambda state: state.has(ItemName.prison_key, player))
        except KeyError:
            pass

    # Furnace Rule and Gate Key Pickup
    yard_fire_items = [
        LocationName.prison_yard_misc_furnace,
        LocationName.prison_yard_item_pickup_gate_key,
    ]

    for loc in yard_fire_items:
        try:
            set_rule(world.multiworld.get_location(loc, player), lambda state: can_light_fire(state, player))
        except KeyError:
            pass

    # Gate Key Rule
    gate_locked_items = [
        LocationName.prison_yard_torch_prisoner_intake,
        LocationName.prison_yard_torch_stables,
    ]

    for loc in gate_locked_items:
        try:
            set_rule(world.multiworld.get_location(loc, player), lambda state: state.has(ItemName.gate_key, player))
        except KeyError:
            pass

    # --- Forest Rules ---
    # Riverside Shack (Fishing Rod)
    try:
        set_rule(world.multiworld.get_location(LocationName.forest_item_pickup_fishing_rod, player),
                 lambda state: state.has(ItemName.riverside_shack_key, player))
    except KeyError:
        pass

    # Items locked behind the forest bridge (Forest Bridge Key Needed)
    forest_bridge_locations = [
        LocationName.forest_poacher_defeated,
        LocationName.forest_item_pickup_major_sol_shard_4,
        LocationName.forest_item_pickup_alchemist_cage_key,
    ]

    for loc in forest_bridge_locations:
        try:
            set_rule(world.multiworld.get_location(loc, player),
                     lambda state: state.has(ItemName.forest_bridge_key, player))
        except KeyError:
            pass
        
    # Apex Horn Rule
    try:
        set_rule(world.multiworld.get_location(LocationName.apex_blow_horn, player), lambda state: state.has(ItemName.blizzard_talisman, player))
    except KeyError:
        pass

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
        try:
            set_rule(world.multiworld.get_location(loc, player),
                     lambda state, f=fish_item: can_light_fire(state, player) and state.has(f, player))
        except KeyError:
            pass

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

    for loc in trader_items_costs:
        try:
            set_rule(world.multiworld.get_location(loc, player),
                     lambda state: can_light_fire(state, player) and state.has(ItemName.fish_tokens_x2, player, 9))
        except KeyError:
            pass

    # --- Village Rules ---

    # Poacher Rewards (Mines Lift Key, Mountain Outpost Key)
    # Accessible after beating Poacher (requires Forest Bridge Key)
    poacher_rewards = [
        LocationName.village_item_pickup_mines_lift_key,
        LocationName.village_item_pickup_mountain_outpost_key,
        LocationName.forest_item_pickup_alchemist_cage_key
    ]
    for loc in poacher_rewards:
        try:
            set_rule(world.multiworld.get_location(loc, player),
                     lambda state: state.has(ItemName.forest_poacher_defeated_event, player))
        except KeyError:
            pass

    # Condemned Shack (Iron Pineapple, Strange Totem)
    condemned_shack_items = [
        LocationName.village_item_pickup_iron_pineapple,
        LocationName.village_item_pickup_strange_totem,
    ]
    for loc in condemned_shack_items:
        try:
            set_rule(world.multiworld.get_location(loc, player),
                     lambda state: state.has(ItemName.condemned_shack_key, player))
        except KeyError:
            pass

    # Quiver of Holding (Village)
    # Locked by getting to the first level of the mines (Mines Lift Key)
    try:
        set_rule(world.multiworld.get_location(LocationName.village_item_pickup_quiver_of_holding, player),
                 lambda state: state.has(ItemName.mine_entrance_lift_key, player))
    except KeyError:
        pass

    # Alchemist Upgrades (Village)
    # Requires freeing the alchemist (Forest Bridge Key + Alchemist Cage Key) AND Potion Mixing Unlocked
    alchemist_upgrades = {
        LocationName.village_alchemist_upgrade_1: 1,
        LocationName.village_alchemist_upgrade_2: 2,
        LocationName.village_alchemist_upgrade_3: 3,
    }
    
    for loc, count in alchemist_upgrades.items():
        try:
            location = world.multiworld.get_location(loc, player)
            set_rule(location,
                     lambda state, c=count: state.has(ItemName.forest_bridge_key, player) and
                                   state.has(ItemName.alchemist_cage_key, player) and
                                   state.has(ItemName.potion_mixing_unlocked, player) and
                                   state.has(ItemName.sol_alembic, player, c))
            # Item Restriction: Cannot be Sol Alembic
            location.item_rule = lambda item: item.name != ItemName.sol_alembic
        except KeyError:
            pass

    # Blacksmith Upgrades (Village)
    # Item Restriction: Cannot be Metamorphic Alloy
    blacksmith_upgrades = {
        LocationName.village_blacksmith_upgrade_1: 1,
        LocationName.village_blacksmith_upgrade_2: 3,
        LocationName.village_blacksmith_upgrade_3: 6,
    }

    for loc, count in blacksmith_upgrades.items():
        try:
            location = world.multiworld.get_location(loc, player)
            set_rule(location, lambda state, c=count: state.has(ItemName.metamorphic_alloy, player, c))
            location.item_rule = lambda item: item.name != ItemName.metamorphic_alloy
        except KeyError:
            pass

    # Iron Pineapple breaking item pickups
    iron_pineapple_locations = [
        LocationName.iron_pineapple_breaking_item_1,
        LocationName.iron_pineapple_breaking_item_2,
        LocationName.iron_pineapple_breaking_item_3,
        LocationName.iron_pineapple_breaking_item_4,
        LocationName.iron_pineapple_breaking_item_5,
    ]
    for loc in iron_pineapple_locations:
        try:
            set_rule(world.multiworld.get_location(loc, player),
                     lambda state: state.has(ItemName.iron_pineapple, player))
        except KeyError:
            pass

    # Relics Improved (Village Undercroft Forgotten Reliquary)
    # There are 4 unique Strange Curios in the world.
    # Each of the first 4 slots requires a specific Curio.
    # Slot 5 opens after all 4 are turned in.
    # All require Greater Void Worm Defeated to access the room.

    curio_map = {
        LocationName.village_relics_improved_1: ItemName.strange_curio_1,
        LocationName.village_relics_improved_2: ItemName.strange_curio_2,
        LocationName.village_relics_improved_3: ItemName.strange_curio_3,
        LocationName.village_relics_improved_4: ItemName.strange_curio_4,
    }

    for loc, item_name in curio_map.items():
        try:
            location = world.multiworld.get_location(loc, player)
            set_rule(location, lambda state, i=item_name: state.has(i, player) and
                                                          state.has(ItemName.greater_void_worm_defeated_event, player))
            location.item_rule = lambda item, i=item_name: item.name != i
        except KeyError:
            pass

    try:
        location = world.multiworld.get_location(LocationName.village_relics_improved_5, player)
        set_rule(location,
                 lambda state: state.has(ItemName.strange_curio_1, player) and
                               state.has(ItemName.strange_curio_2, player) and
                               state.has(ItemName.strange_curio_3, player) and
                               state.has(ItemName.strange_curio_4, player) and
                               state.has(ItemName.greater_void_worm_defeated_event, player))
        location.item_rule = lambda item: item.name not in {ItemName.strange_curio_1, ItemName.strange_curio_2, ItemName.strange_curio_3, ItemName.strange_curio_4}
    except KeyError:
        pass

    # Hall of Heroes Restored
    hall_of_heroes_locations = [
        LocationName.village_misc_hall_of_heroes_restored,
        LocationName.village_torch_forgotten_reliquary,
    ]
    for loc in hall_of_heroes_locations:
        try:
            set_rule(world.multiworld.get_location(loc, player),
                     lambda state: state.has(ItemName.greater_void_worm_defeated_event, player))
        except KeyError:
            pass

    # --- Boss Events ---
    # Place Event Items on Event Locations
    
    # Warden
    try:
        # Rule: Can reach the physical boss location (which requires Prison Key)
        set_rule(world.multiworld.get_location(LocationName.prison_warden_defeated_event, player),
                 lambda state: state.has(ItemName.prison_key, player))
    except KeyError:
        pass

    # Poacher
    try:
        # Rule: Can reach the physical boss location (which requires Forest Bridge Key)
        set_rule(world.multiworld.get_location(LocationName.forest_poacher_defeated_event, player),
                 lambda state: state.has(ItemName.forest_bridge_key, player))
    except KeyError:
        pass

    # Groundskeeper
    try:
        # Rule: Can reach the physical boss location (Access to Mountain Region)
        set_rule(world.multiworld.get_location(LocationName.mountain_groundskeeper_defeated_event, player),
                 lambda state: True)
    except KeyError:
        pass

    # Greater Void Worm
    try:
        # Rule: Can reach the physical boss location (Pit Catwalk Key)
        set_rule(world.multiworld.get_location(LocationName.mines_worm_defeated_event, player),
                 lambda state: state.has(ItemName.pit_catwalk_key, player))
    except KeyError:
        pass

    # Amalgamate
    try:
        # Rule: Can reach the physical boss location (Central Cell Key + Minor Cell Key + False Book)
        set_rule(world.multiworld.get_location(LocationName.cultist_amalgamate_defeated_event, player),
                 lambda state: state.has(ItemName.central_cell_key, player) and state.has(ItemName.minor_cell_key, player)
                               and state.has(ItemName.false_book, player))
    except KeyError:
        pass

    # Infernal Warden
    try:
        # Rule: Can reach the physical boss location (East Wing Key)
        set_rule(world.multiworld.get_location(LocationName.supermax_prison_infernal_warden_defeated_event, player),
                 lambda state: state.has(ItemName.east_wing_key, player))
    except KeyError:
        pass

    # Immaculate
    try:
        # Rule: Can reach the physical boss location (Poacher Defeated)
        set_rule(world.multiworld.get_location(LocationName.factory_immaculate_defeated_event, player),
                 lambda state: state.has(ItemName.forest_poacher_defeated_event, player))
    except KeyError:
        pass

    # Gatekeeper
    try:
        # Rule: Can reach the physical boss location (Access to Apex Outskirts)
        set_rule(world.multiworld.get_location(LocationName.apex_gatekeeper_defeated_event, player),
                 lambda state: True)
    except KeyError:
        pass

    # Zenith needs to be locked behind having all 3 data discs
    zenith_locations = [
        LocationName.apex_zenith_defeated,
        LocationName.apex_zenith_defeated_event,
    ]
    for loc in zenith_locations:
        try:
            # Rule: Can reach the physical boss location (Gatekeeper Defeated) and has all 3 data discs
            set_rule(world.multiworld.get_location(loc, player),
                     lambda state: state.has(ItemName.apex_gatekeeper_defeated_event, player) and
                                   state.has(ItemName.data_disc_r, player) and
                                   state.has(ItemName.data_disc_g, player) and
                                   state.has(ItemName.data_disc_b, player))
        except KeyError:
            pass


    # Mines 1F Map requires Minecart Wheel
    try:
        set_rule(world.multiworld.get_location(LocationName.mines_item_pickup_map_1, player),
                     lambda state: state.has(ItemName.minecart_wheel, player))
    except KeyError:
        pass

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
        try:
            add_rule(world.multiworld.get_location(loc_name, player), lambda state: state.has(ItemName.pit_catwalk_key, player))
        except KeyError:
            pass

    # Mines 4F Temple of the Deep Key Rules
    mines_temple_locked_locations = [
        LocationName.mines_wall_puzzle_half,
        LocationName.mines_torch_restricted_cultist_reliquary,
    ]
    for loc_name in mines_temple_locked_locations:
        try:
            set_rule(world.multiworld.get_location(loc_name, player), lambda state: state.has(ItemName.temple_of_the_deep_key, player))
        except KeyError:
            pass

    # Cultist Compound False Book Rules
    cultist_false_book_locked_locations = [
        LocationName.cultist_torch_forbidden_study,
        LocationName.cultist_compound_item_pickup_brass_knuckles,
    ]
    for loc_name in cultist_false_book_locked_locations:
        try:
            set_rule(world.multiworld.get_location(loc_name, player), lambda state: state.has(ItemName.false_book, player))
        except KeyError:
            pass

    # Cultist Compound Central Cell Key Rules
    cultist_central_cell_locked_locations = [
        LocationName.cultist_compound_item_pickup_guile_rogue,
        LocationName.cultist_compound_item_pickup_purifying_needle,
    ]
    for loc_name in cultist_central_cell_locked_locations:
        try:
            set_rule(world.multiworld.get_location(loc_name, player), lambda state: state.has(ItemName.central_cell_key, player))
        except KeyError:
            pass

    # Cultist Compound Minor Cell Key Rules
    cultist_minor_cell_locked_locations = [
        LocationName.cultist_compound_item_pickup_metamorphic_alloy,
        LocationName.cultist_compound_item_pickup_central_cell_key,
        LocationName.cultist_torch_infinity_chasm,
        LocationName.cultist_compound_wall_elevator,
        LocationName.cultist_compound_item_pickup_garnet_aegis,
    ]
    for loc_name in cultist_minor_cell_locked_locations:
        try:
            set_rule(world.multiworld.get_location(loc_name, player), lambda state: state.has(ItemName.minor_cell_key, player))
        except KeyError:
            pass

    # Cultist Compound Sol Forge Lab Key Rule
    try:
        set_rule(world.multiworld.get_location(LocationName.cultist_compound_item_pickup_sol_forge_lab_key, player),
                 lambda state: state.has(ItemName.central_cell_key, player) and state.has(ItemName.minor_cell_key, player))
    except KeyError:
        pass

    # Cultist Tamper Armament Rule
    try:
        set_rule(world.multiworld.get_location(LocationName.cultist_tamper_armament, player),
                 lambda state: state.has(ItemName.sol_forge_lab_key, player) and state.has(ItemName.minor_cell_key, player))
    except KeyError:
        pass

    # Cultist Amalgamate Defeated Rule
    try:
        set_rule(world.multiworld.get_location(LocationName.cultist_compound_item_pickup_sol_forge_lab_key , player),
                 lambda state: state.has(ItemName.central_cell_key, player) and state.has(ItemName.minor_cell_key, player))
    except KeyError:
        pass

    # --- Supermax Prison Rules ---
    # Codebearer Puzzle
    # Entry to the puzzle area requires the Infernal Key.
    try:
        set_rule(world.multiworld.get_location(LocationName.supermax_prison_spark_hidden, player),
                 lambda state: state.has(ItemName.infernal_key, player))
    except KeyError:
        pass

    # The puzzle itself requires either a sword, dagger, or hammer to complete.
    codebearer_puzzle_locations = [
        LocationName.supermax_prison_item_pickup_pet_worm,
        LocationName.supermax_prison_item_pickup_major_sol_shard_18,
        LocationName.supermax_prison_item_pickup_major_sol_shard_19,
        LocationName.supermax_prison_item_pickup_major_sol_shard_20,
    ]

    def can_solve_codebearer_puzzle(state):
        return state.has(ItemName.sword, player) and \
               state.has(ItemName.dagger, player) and \
               state.has(ItemName.great_hammer, player)

    for loc_name in codebearer_puzzle_locations:
        try:
            set_rule(world.multiworld.get_location(loc_name, player),
                     lambda state: state.has(ItemName.infernal_key, player) and can_solve_codebearer_puzzle(state))
        except KeyError:
            pass

    # Infernal Key Pickup Rule
    # The infernal key pickup is dropped by the infernal warden boss
    try:
        set_rule(world.multiworld.get_location(LocationName.supermax_prison_item_pickup_infernal_key, player),
                 lambda state: state.has(ItemName.supermax_prison_infernal_warden_defeated_event, player))
    except KeyError:
        pass

    # East Wing Key Rules
    # These locations are locked behind the door requiring the East Wing Key
    east_wing_locked_locations = [
        LocationName.supermax_prison_item_pickup_relic_dousing,
        LocationName.supermax_prison_item_pickup_stale_bread,
        LocationName.supermax_prison_item_pickup_major_sol_shard_13,
        LocationName.supermax_prison_item_pickup_major_sol_shard_14,
        LocationName.supermax_prison_item_pickup_metamorphic_alloy,
        LocationName.supermax_prison_item_pickup_major_sol_shard_15,
        LocationName.supermax_prison_item_pickup_map_b,
        LocationName.supermax_prison_item_pickup_map_c,
        LocationName.supermax_prison_wall_security_corridor,
        LocationName.supermax_prison_torch_torture_chamber,
        LocationName.supermax_prison_torch_east_wing_office,
        LocationName.supermax_prison_torch_security_corridor,
        LocationName.supermax_prison_torch_north_storage_room,
        LocationName.supermax_prison_torch_prison_rear_entrance,
        LocationName.supermax_prison_torch_improvised_camp,
        LocationName.supermax_prison_infernal_warden_defeated,
    ]

    for loc_name in east_wing_locked_locations:
        try:
            set_rule(world.multiworld.get_location(loc_name, player), lambda state: state.has(ItemName.east_wing_key, player))
        except KeyError:
            pass

    # Mushroom Access Rules
    # These locations require at least one mushroom to access
    mushroom_access_locations = [
        LocationName.mountain_item_pickup_mushroom,
        LocationName.mines_item_pickup_mushroom,
        LocationName.swamp_item_pickup_mushroom,
    ]

    for loc_name in mushroom_access_locations:
        try:
            set_rule(world.multiworld.get_location(loc_name, player), lambda state: state.has(ItemName.mysterious_mushroom_x1, player))
        except KeyError:
            pass

    # Breakable Wall Rules
    # Factory Dual Handaxes and Cracked Wall Outside Factory require blowing up the wall
    breakable_wall_locations = [
        LocationName.factory_item_pickup_dual_handaxes,
        LocationName.factory_wall_cracked_outside,
        LocationName.mines_wall_cracked_entrance,
    ]

    for loc_name in breakable_wall_locations:
        try:
            set_rule(world.multiworld.get_location(loc_name, player), lambda state: can_blow_up_wall(state, player))
        except KeyError:
            pass

    # Apex Outskirts Key Pickup Rule
    # The apex outskirts key pickup is dropped by the immaculate boss
    try:
        set_rule(world.multiworld.get_location(LocationName.factory_item_pickup_apex_outskirts_key, player),
                 lambda state: state.has(ItemName.factory_immaculate_defeated_event, player))
    except KeyError:
        pass

    # Apex Relic of Power Plus Rule
    try:
        set_rule(world.multiworld.get_location(LocationName.apex_outskirts_item_pickup_relic_power_plus, player),
                 lambda state: state.has(ItemName.apex_outskirts_key, player))
    except KeyError:
        pass

    # Apex Outskirts Light Spark
    try:
        set_rule(world.multiworld.get_location(LocationName.apex_spark_outskirts, player),
                 lambda state: state.has(ItemName.apex_outskirts_key, player))
    except KeyError:
        pass

    # Apex Unknown Light Spark
    try:
        set_rule(world.multiworld.get_location(LocationName.apex_spark_unknown, player),
                 lambda state: state.has(ItemName.data_disc_r, player) and
                               state.has(ItemName.data_disc_g, player) and
                               state.has(ItemName.data_disc_b, player))
    except KeyError:
        pass

    # Apex King's Emblem Rules
    # Data Disc G and Potions Increased #6 require both halves of the King's Emblem
    kings_emblem_locked_locations = [
        LocationName.apex_item_pickup_data_disc_g,
        LocationName.apex_item_pickup_potions_increased_6,
    ]

    for loc_name in kings_emblem_locked_locations:
        try:
            set_rule(world.multiworld.get_location(loc_name, player),
                     lambda state: state.has(ItemName.kings_emblem_left_half, player) and
                                   state.has(ItemName.kings_emblem_right_half, player))
        except KeyError:
            pass

    # Apex Master Bedroom Key Rules
    # Restricted Access Key and Data Disc R require Master Bedroom Key
    master_bedroom_locked_locations = [
        LocationName.apex_item_pickup_restricted_access_key,
        LocationName.apex_item_pickup_data_disc_r,
    ]

    for loc_name in master_bedroom_locked_locations:
        try:
            set_rule(world.multiworld.get_location(loc_name, player),
                     lambda state: state.has(ItemName.master_bedroom_key, player))
        except KeyError:
            pass

    # Apex East Wing Key Rules
    apex_east_wing_locked_locations = [
        LocationName.apex_item_pickup_master_bedroom_key,
        LocationName.apex_item_pickup_minor_sol_shard_31,
        LocationName.apex_item_pickup_minor_sol_shard_32,
        LocationName.apex_torch_dav1phlfyz,
        LocationName.apex_torch_acwis58fl9,
        LocationName.apex_torch_m4upnnpvqe,
    ]

    for loc_name in apex_east_wing_locked_locations:
        try:
            set_rule(world.multiworld.get_location(loc_name, player),
                     lambda state: state.has(ItemName.apex_east_wing_key, player))
        except KeyError:
            pass

    # Apex Restricted Access Key Rules
    restricted_access_locked_locations = [
        LocationName.apex_item_pickup_minor_sol_shard_30,
        LocationName.apex_item_pickup_minor_sol_shard_33,
        LocationName.apex_item_pickup_brass_knuckles_plus,
        LocationName.apex_torch_sparring_hall,
    ]

    for loc_name in restricted_access_locked_locations:
        try:
            set_rule(world.multiworld.get_location(loc_name, player),
                     lambda state: state.has(ItemName.restricted_access_key, player))
        except KeyError:
            pass

    # Apex Guard Captain's Key Rules
    guard_captains_locked_locations = [
        LocationName.apex_item_pickup_corroded_key,
        LocationName.apex_wall_immunity_torch_1,
        LocationName.apex_wall_immunity_torch_2,
    ]

    for loc_name in guard_captains_locked_locations:
        try:
            set_rule(world.multiworld.get_location(loc_name, player),
                     lambda state: state.has(ItemName.guard_captains_key, player))
        except KeyError:
            pass

    # Apex Corroded Key Rules
    try:
        set_rule(world.multiworld.get_location(LocationName.apex_item_pickup_kings_emblem_left, player),
                 lambda state: state.has(ItemName.corroded_key, player))
    except KeyError:
        pass