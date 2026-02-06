from worlds.void_sols.test.bases import VoidSolsTestBase
from worlds.void_sols.Names import ItemName, LocationName

class TestRules(VoidSolsTestBase):
    
    # Common access items to reach most regions
    world_access_items = [
        ItemName.prison_warden_defeated_event,
        ItemName.gate_key,
        ItemName.forest_bridge_key,
        ItemName.mountain_outpost_key,
        ItemName.mine_entrance_lift_key,
        ItemName.minecart_wheel,
        ItemName.lift_key,
        ItemName.pit_catwalk_key,
        ItemName.temple_of_the_deep_key,
        ItemName.apex_outskirts_key,
        ItemName.apex_gatekeeper_defeated_event,
        ItemName.greater_void_worm_defeated_event,
        ItemName.east_wing_key,
        ItemName.forest_poacher_defeated_event,
        ItemName.central_cell_key,
        ItemName.minor_cell_key,
        ItemName.false_book,
        ItemName.sol_forge_lab_key,
        ItemName.infernal_key,
    ]

    def test_prison_key_access(self) -> None:
        """Test locations that require the Prison Key"""
        locations = [
            LocationName.prison_item_pickup_ruby_phial,
            LocationName.prison_torch_entry_hall,
            LocationName.prison_item_pickup_map_b,
            LocationName.prison_spark_entry_hall,
            LocationName.prison_warden_defeated,
            LocationName.prison_wall_entry_hall
        ]
        items = [[ItemName.prison_key]]
        self.assertAccessDependency(locations, items, only_check_listed=True)

    def test_furnace_access(self) -> None:
        """Test access to the furnace which requires fire"""
        locations = [LocationName.prison_yard_misc_furnace]
        # Requires Prison Warden Defeated Event to reach Prison Yard
        base_items = [ItemName.prison_warden_defeated_event]
        
        items = [
            base_items + [ItemName.flaming_torch_x1],
            base_items + [ItemName.flaming_torch_x2],
            base_items + [ItemName.fire_talisman]
        ]
        self.assertAccessDependency(locations, items, only_check_listed=True)

    def test_fishing_access(self) -> None:
        """Test fishing locations require Fishing Rod"""
        locations = [
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
        # Need world access to reach all these locations
        items = [self.world_access_items + [ItemName.fishing_rod]]
        self.assertAccessDependency(locations, items, only_check_listed=True)

    def test_forest_bridge_access(self) -> None:
        """Test locations behind the forest bridge"""
        locations = [
            LocationName.forest_poacher_defeated,
            LocationName.forest_item_pickup_major_sol_shard_4,
        ]
        # Need access to Forest (Gate Key + Warden Event)
        base_items = [ItemName.prison_warden_defeated_event, ItemName.gate_key]
        items = [base_items + [ItemName.forest_bridge_key]]
        self.assertAccessDependency(locations, items, only_check_listed=True)

    def test_mycology_relic_access(self) -> None:
        """Test access to Relic of Mycology which requires mushrooms"""
        location = LocationName.forest_item_pickup_relic_mycology
        # Need access to Forest
        base_items = [ItemName.prison_warden_defeated_event, ItemName.gate_key]
        
        # Test with 5 mushrooms
        self.assertAccessDependency([location], [base_items + [ItemName.mysterious_mushroom_x1] * 5], only_check_listed=True)
        
        # Test with 4 mushrooms + silver pouch
        self.assertAccessDependency([location], [base_items + [ItemName.mysterious_mushroom_x1] * 4 + [ItemName.silver_pouch]], only_check_listed=True)

    def test_kings_emblem_access(self) -> None:
        """Test locations requiring King's Emblem (both halves)"""
        locations = [
            LocationName.apex_item_pickup_data_disc_g,
            LocationName.apex_item_pickup_potions_increased_6,
        ]
        # Locations in Apex (requires Gatekeeper Event + Outskirts Key + Forest Access)
        base_items = [
            ItemName.prison_warden_defeated_event, ItemName.gate_key, 
            ItemName.apex_outskirts_key, ItemName.apex_gatekeeper_defeated_event
        ]
        items = [base_items + [ItemName.kings_emblem_left_half, ItemName.kings_emblem_right_half]]
        self.assertAccessDependency(locations, items, only_check_listed=True)

    def test_apex_outskirts_access(self) -> None:
        """Test access to Apex Outskirts via various methods"""
        location = LocationName.apex_outskirts_item_pickup_golden_clover
        
        # Access to Forest
        forest_access = [ItemName.prison_warden_defeated_event, ItemName.gate_key]
        
        # Access to Mines (for Mine Entrance Lift Key path)
        mines_access = forest_access + [ItemName.mine_entrance_lift_key]
        
        self.assertAccessDependency([location], [
            forest_access + [ItemName.apex_outskirts_key],
            forest_access + [ItemName.dynamite_x1],
            mines_access 
        ], only_check_listed=True)

    def test_east_wing_key_access(self) -> None:
        """Test locations requiring East Wing Key"""
        locations = [
            LocationName.supermax_prison_item_pickup_relic_dousing,
            LocationName.supermax_prison_item_pickup_stale_bread,
            LocationName.supermax_prison_item_pickup_major_sol_shard_13,
            LocationName.supermax_prison_infernal_warden_defeated,
        ]
        # Supermax Prison West requires Greater Void Worm Event + Forest Access
        base_items = [
            ItemName.prison_warden_defeated_event, ItemName.gate_key,
            ItemName.greater_void_worm_defeated_event
        ]
        items = [base_items + [ItemName.east_wing_key]]
        self.assertAccessDependency(locations, items, only_check_listed=True)

    def test_codebearer_puzzle(self) -> None:
        """Test Codebearer Puzzle access which requires Infernal Key AND specific weapons"""
        locations = [
            LocationName.supermax_prison_item_pickup_pet_worm,
            LocationName.supermax_prison_item_pickup_major_sol_shard_18,
            LocationName.supermax_prison_item_pickup_major_sol_shard_19,
            LocationName.supermax_prison_item_pickup_major_sol_shard_20,
        ]
        
        # Supermax Prison West requires Greater Void Worm Event + Forest Access
        base_items = [
            ItemName.prison_warden_defeated_event, ItemName.gate_key,
            ItemName.greater_void_worm_defeated_event
        ]
        
        # Requires Infernal Key AND (Sword AND Dagger AND Great Hammer)
        items = [base_items + [ItemName.infernal_key, ItemName.sword, ItemName.dagger, ItemName.great_hammer]]
        self.assertAccessDependency(locations, items, only_check_listed=True)

    def test_trader_trades(self) -> None:
        """Test Trader Trades which require specific fish"""
        # Forest Access
        base_items = [ItemName.prison_key, ItemName.prison_warden_defeated_event, ItemName.gate_key, ItemName.flaming_torch_x1]
        
        # Test Star Fish trade
        self.collect_by_name(base_items + [ItemName.star_fish])
        self.assertTrue(self.can_reach_location(LocationName.forest_trader_trade_star_fish))
        self.remove_by_name([ItemName.star_fish])
        self.assertFalse(self.can_reach_location(LocationName.forest_trader_trade_star_fish))
        
        # Test Flying Fish trade
        self.collect_by_name([ItemName.flying_fish])
        self.assertTrue(self.can_reach_location(LocationName.forest_trader_trade_flying_fish))
        self.remove_by_name([ItemName.flying_fish])
        self.assertFalse(self.can_reach_location(LocationName.forest_trader_trade_flying_fish))

    def test_trader_items(self) -> None:
        """Test Trader Items which require Fire AND Fish Tokens"""
        location = LocationName.forest_trader_item_potions_increased
        
        # Forest Access
        base_items = [ItemName.prison_warden_defeated_event, ItemName.gate_key]
        
        # Needs Fire + 2 packs of tokens
        items = [base_items + [ItemName.flaming_torch_x1, ItemName.fish_tokens_x2, ItemName.fish_tokens_x2]]
        self.assertAccessDependency([location], items, only_check_listed=True)

    def test_relics_improved(self) -> None:
        """Test Relics Improved locations which require Strange Curios"""
        # Village Access (Forest Access)
        base_items = [ItemName.prison_warden_defeated_event, ItemName.gate_key]
        
        # Slot 1 requires Curio 1
        self.assertAccessDependency([LocationName.village_relics_improved_1], [base_items + [ItemName.strange_curio_1]], only_check_listed=True)
        # Slot 2 requires Curio 2
        self.assertAccessDependency([LocationName.village_relics_improved_2], [base_items + [ItemName.strange_curio_2]], only_check_listed=True)
        # Slot 3 requires Curio 3
        self.assertAccessDependency([LocationName.village_relics_improved_3], [base_items + [ItemName.strange_curio_3]], only_check_listed=True)
        # Slot 4 requires Curio 4
        self.assertAccessDependency([LocationName.village_relics_improved_4], [base_items + [ItemName.strange_curio_4]], only_check_listed=True)

        # Slot 5 requires all 4 Curios
        all_curios = [ItemName.strange_curio_1, ItemName.strange_curio_2, ItemName.strange_curio_3, ItemName.strange_curio_4]
        self.assertAccessDependency([LocationName.village_relics_improved_5], [base_items + all_curios], only_check_listed=True)

    def test_zenith_access(self) -> None:
        """Test Zenith access requires all 3 data discs"""
        locations = [
            LocationName.apex_zenith_defeated,
            LocationName.apex_zenith_defeated_event,
        ]
        # Apex Hub requires Gatekeeper Event
        base_items = self.world_access_items + [ItemName.apex_gatekeeper_defeated_event]
        
        # Should require all 3 data discs
        items = [base_items + [ItemName.data_disc_r, ItemName.data_disc_g, ItemName.data_disc_b]]
        self.assertAccessDependency(locations, items, only_check_listed=True)

    def test_supermax_prison_access(self) -> None:
        """Test that Supermax Prison West requires East Wing Key and has an exit"""
        locations = [LocationName.supermax_prison_item_pickup_map_a]
        
        # Should require East Wing Key + Greater Void Worm
        base_items = [ItemName.prison_warden_defeated_event, ItemName.gate_key, ItemName.greater_void_worm_defeated_event]
        items = [base_items + [ItemName.east_wing_key]]
        self.assertAccessDependency(locations, items, only_check_listed=True)
        
        # Verify region access directly
        self.collect_all_but([ItemName.east_wing_key])
        self.assertFalse(self.can_reach_region("Supermax Prison West"))
        self.collect_by_name([ItemName.east_wing_key])
        self.assertTrue(self.can_reach_region("Supermax Prison West"))
        self.assertTrue(self.can_reach_region("Supermax Prison East"))

    def test_iron_pineapple_access(self) -> None:
        """Test locations that require Iron Pineapple"""
        locations = [
            LocationName.iron_pineapple_breaking_item_1,
            LocationName.iron_pineapple_breaking_item_2,
            LocationName.iron_pineapple_breaking_item_3,
            LocationName.iron_pineapple_breaking_item_4,
            LocationName.iron_pineapple_breaking_item_5,
        ]
        # We also need access to the Village (Gate Key + Warden Event)
        base_items = [ItemName.prison_warden_defeated_event, ItemName.gate_key]
        items = [base_items + [ItemName.iron_pineapple]]
        self.assertAccessDependency(locations, items, only_check_listed=True)

    def test_alchemist_upgrade_requirements(self) -> None:
        """Test Alchemist Upgrades require Sol Alembics"""
        base_items = [
            ItemName.prison_warden_defeated_event, ItemName.gate_key,
            ItemName.forest_bridge_key, ItemName.alchemist_cage_key
        ]
        # Upgrade 1 requires 1 Alembic
        self.assertAccessDependency([LocationName.village_alchemist_upgrade_1], 
                                    [base_items + [ItemName.sol_alembic]], only_check_listed=True)
        # Upgrade 3 requires 3 Alembics
        self.assertAccessDependency([LocationName.village_alchemist_upgrade_3], 
                                    [base_items + [ItemName.sol_alembic] * 3], only_check_listed=True)

    def test_blacksmith_upgrade_requirements(self) -> None:
        """Test Blacksmith Upgrades require Metamorphic Alloys"""
        base_items = [ItemName.prison_warden_defeated_event, ItemName.gate_key]
        # Upgrade 1 requires 1 Alloy
        self.assertAccessDependency([LocationName.village_blacksmith_upgrade_1], 
                                    [base_items + [ItemName.metamorphic_alloy]], only_check_listed=True)
        # Upgrade 2 requires 3 Alloys
        self.assertAccessDependency([LocationName.village_blacksmith_upgrade_2], 
                                    [base_items + [ItemName.metamorphic_alloy] * 3], only_check_listed=True)
        # Upgrade 3 requires 6 Alloys
        self.assertAccessDependency([LocationName.village_blacksmith_upgrade_3], 
                                    [base_items + [ItemName.metamorphic_alloy] * 6], only_check_listed=True)

    def test_hall_of_heroes_restored_access(self) -> None:
        """Test Hall of Heroes Restored requires Greater Void Worm Defeated"""
        locations = [
            LocationName.village_misc_hall_of_heroes_restored,
            LocationName.village_torch_forgotten_reliquary,
        ]
        # Village Access
        base_items = [ItemName.prison_warden_defeated_event, ItemName.gate_key, ItemName.prison_key]
        
        # Check Village access generally
        self.collect_by_name(base_items)
        self.assertTrue(self.can_reach_region("Village"))
        self.assertTrue(self.can_reach_location(LocationName.village_item_pickup_map))

        # Re-initialize state to be sure
        self.remove(self.get_item_by_name(ItemName.greater_void_worm_defeated_event))

        for loc in locations:
             self.assertFalse(self.can_reach_location(loc), f"{loc} should not be reachable without Worm Defeated")
        
        self.collect_by_name([ItemName.greater_void_worm_defeated_event])
        for loc in locations:
             self.assertTrue(self.can_reach_location(loc), f"{loc} should be reachable with Worm Defeated. Region: {self.multiworld.get_location(loc, self.player).parent_region}")
