from worlds.mindustry.test import MindustryTestBase

serpulo_logistic = ["Conduit", "Liquid Junction", "Liquid Router", "Bridge Conduit", "Junction", "Router",
                     "Bridge Conveyor", "Power Node"]
erekir_logistic = ["Duct Bridge", "Reinforced Conduit", "Reinforced Liquid Junction", "Reinforced Bridge Conduit",
                   "Reinforced Liquid Router"]

serpulo_progressive_items = ["Pneumatic Drill", "Laser Drill", "Airblast Drill", "Combustion Generator",
                             "Steam Generator", "Thermal Generator", "Differential Generator", "Thorium Reactor",
                             "Impact Reactor", "RTG Generator"]
erekir_progressive_items = ["Impact Drill", "Large Plasma Bore", "Eruption Drill", "Chemical Combustion Chamber",
                            "Pyrolysis Generator", "Flux Reactor", "Neoplasia Reactor"]

class TestItemPlacementOptions(MindustryTestBase):
    """Unit test to validate item placement with various options."""

    def test_serpulo_starter_logistics(self) -> None:
        """Test that starter logistics are given to the player and removed from the item pool on Serpulo."""
        self.options["campaign_choice"] = 0
        self.options["logistic_distribution"] = 3
        self.world_setup()


        self.assertTrue(self.multiworld.state.has_all(serpulo_logistic, self.player))
        self.assertTrue(self.has_no_items_in_itempool(serpulo_logistic))

    def test_erekir_starter_logistics(self) -> None:
        """Test that starter logistics are given to the player and removed from the item pool on Erekir."""
        self.options["campaign_choice"] = 1
        self.options["logistic_distribution"] = 3
        self.world_setup()


        self.assertTrue(self.multiworld.state.has_all(erekir_logistic, self.player))
        self.assertTrue(self.has_no_items_in_itempool(erekir_logistic))


    def test_serpulo_progressive_items_options(self) -> None:
        """
        Test that Serpulo progressive items are in the item pool their non-progression counterpart are not present in the
        itempool.
        """
        self.options["campaign_choice"] = 0
        self.options["progressive_drills"] = True
        self.options["progressive_generators"] = True
        self.world_setup()

        self.assertTrue(self.has_no_items_in_itempool(serpulo_progressive_items))
        self.assertTrue(self.has_amount_in_itempool("Progressive Drills Serpulo", 3))
        self.assertTrue(self.has_amount_in_itempool("Progressive Generators Serpulo", 7))
        self.assertTrue(self.has_amount_in_itempool("Progressive Offensive Ground Unit", 5))
        self.assertTrue(self.has_amount_in_itempool("Progressive Support Ground Unit", 5))
        self.assertTrue(self.has_amount_in_itempool("Progressive Insectoid Ground Unit", 5))
        self.assertTrue(self.has_amount_in_itempool("Progressive Offensive Air Unit", 5))
        self.assertTrue(self.has_amount_in_itempool("Progressive Support Air Unit", 5))
        self.assertTrue(self.has_amount_in_itempool("Progressive Offensive Naval Unit", 5))
        self.assertTrue(self.has_amount_in_itempool("Progressive Support Naval Unit", 5))
        self.assertTrue(self.has_amount_in_itempool("Progressive Reconstructor", 4))

    def test_erekir_progressive_items_options(self) -> None:
        """
        Test that Erekir progressive items are in the item pool their non-progression counterpart are not present in the
        itempool.
        """
        self.options["campaign_choice"] = 1
        self.options["progressive_drills"] = True
        self.options["progressive_generators"] = True
        self.world_setup()

        self.assertTrue(self.has_no_items_in_itempool(erekir_progressive_items))
        self.assertTrue(self.has_amount_in_itempool("Progressive Drills Erekir", 3))
        self.assertTrue(self.has_amount_in_itempool("Progressive Generators Erekir", 4))
        self.assertTrue(self.has_amount_in_itempool("Progressive Tanks", 4))
        self.assertTrue(self.has_amount_in_itempool("Progressive Ships", 5))
        self.assertTrue(self.has_amount_in_itempool("Progressive Mechs", 5))