from worlds.mindustry.test import MindustryTestBase

caldera_requirement = ["Surge Crucible", "Reinforced Pump", "Reinforced Conduit", "Electrolyzer", "Beam Tower",
                       "Ship Refabricator", "Reinforced Container","Payload Loader", "Payload Unloader",
                       "Progressive Ships", "Chemical Combustion Chamber", "Payload Mass Driver", "Mech Fabricator",
                       "Progressive Mechs", "Ship Fabricator", "Oxidation Chamber", "Impact Drill"]

class TestErekirResourcesAccess(MindustryTestBase):
    """Unit test to validate rules for resources production on Erekir."""
    options = {
        "campaign_choice": 1,
        "logistic_distribution": 0,
        "military_level_tracking": False
    }


    def test_erekir_sphere_0_resource(self) -> None:
        """Test that validate that sphere 0 resources can be produced without items"""
        self.world_setup()

        self.assertTrue(self.can_reach_region("Beryllium"))
        self.assertTrue(self.can_reach_region("Sand Erekir"))
        self.assertTrue(self.can_reach_region("Silicon Erekir"))
        self.assertTrue(self.can_reach_region("Water Erekir"))
        self.assertTrue(self.can_reach_region("Graphite Erekir"))

    def test_erekir_oxide_access(self) -> None:
        """Test that validate if oxide is accessible on Erekir"""
        self.world_setup()
        oxide_requirement = ["Oxidation Chamber", "Impact Drill", "Reinforced Conduit"]

        self.assertFalse(self.can_reach_location("Produce Oxide on Erekir"))
        self.collect_by_name(oxide_requirement)
        self.assertTrue(self.can_reach_location("Produce Oxide on Erekir"))

    def test_erekir_ozone_access(self) -> None:
        """Test that validate if Ozone is accessible on Erekir"""
        self.world_setup()
        ozone_requirement = ["Electrolyzer", "Impact Drill", "Reinforced Conduit"]

        self.assertFalse(self.can_reach_location("Produce Ozone on Erekir"))
        self.collect_by_name(ozone_requirement)
        self.assertTrue(self.can_reach_location("Produce Ozone on Erekir"))

    def test_erekir_hydrogen_access(self) -> None:
        """Test that validate if Hydrogen is accessible on Erekir"""
        self.world_setup()
        hydrogen_requirement = ["Electrolyzer", "Impact Drill", "Reinforced Conduit"]

        self.assertFalse(self.can_reach_location("Produce Hydrogen on Erekir"))
        self.collect_by_name(hydrogen_requirement)
        self.assertTrue(self.can_reach_location("Produce Hydrogen on Erekir"))

    def test_erekir_nitrogen_access(self) -> None:
        """Test that validate if Nitrogen is accessible on Erekir"""
        self.world_setup()
        nitrogen_requirement = ["Atmospheric Concentrator", "Carbide Crucible", "Large Plasma Bore"]

        self.assertFalse(self.can_reach_location("Produce Nitrogen on Erekir"))
        self.collect_by_name(caldera_requirement)
        self.assertFalse(self.can_reach_location("Produce Nitrogen on Erekir"))
        self.collect_by_name(nitrogen_requirement)
        self.assertTrue(self.can_reach_location("Produce Nitrogen on Erekir"))

    def test_erekir_cyanogen_access(self) -> None:
        """Test that validate if Cyanogen is accessible on Erekir"""
        self.world_setup()
        cyanogen_requirement = ["Cyanogen Synthesizer", "Carbide Crucible", "Large Plasma Bore"]

        self.assertFalse(self.can_reach_location("Produce Cyanogen on Erekir"))
        self.collect_by_name(cyanogen_requirement)
        self.assertFalse(self.can_reach_location("Produce Cyanogen on Erekir"))
        self.collect_by_name(caldera_requirement)
        self.assertTrue(self.can_reach_location("Produce Cyanogen on Erekir"))

    def test_erekir_tungsten_access(self) -> None:
        """Test that validate if Tungsten is accessible on Erekir"""
        self.world_setup()
        tungsten_requirement = ["Impact Drill", "Reinforced Conduit"]

        self.assertFalse(self.can_reach_location("Produce Tungsten on Erekir"))
        self.collect_by_name(tungsten_requirement)
        self.assertTrue(self.can_reach_location("Produce Tungsten on Erekir"))


    def test_erekir_slag_access(self) -> None:
        """Test that validate if Slag is accessible on Erekir"""
        self.world_setup()
        slag_requirement = ["Reinforced Pump", "Reinforced Conduit", "Impact Drill", "Electrolyzer"]

        self.assertFalse(self.can_reach_location("Produce Slag on Erekir"))
        self.collect_by_name(slag_requirement)
        self.assertTrue(self.can_reach_location("Produce Slag on Erekir"))

    def test_erekir_arkycite_access(self) -> None:
        """Test that validate if Arkycite is accessible on Erekir"""
        self.world_setup()
        arkycite_requirement = ["Impact Drill", "Reinforced Conduit", "Reinforced Pump", "Electrolyzer"]

        self.assertFalse(self.can_reach_location("Produce Arkycite on Erekir"))
        self.collect_by_name(arkycite_requirement)
        self.assertTrue(self.can_reach_location("Produce Arkycite on Erekir"))

    def test_erekir_thorium_access(self) -> None:
        """Test that validate if Thorium is accessible on Erekir"""
        self.world_setup()
        thorium_requirement = ["Large Plasma Bore"]

        self.assertFalse(self.can_reach_location("Produce Thorium on Erekir"))
        self.collect_by_name(caldera_requirement)
        self.assertFalse(self.can_reach_location("Produce Thorium on Erekir"))
        self.collect_by_name(thorium_requirement)
        self.assertTrue(self.can_reach_location("Produce Thorium on Erekir"))

    def test_erekir_carbide_access(self) -> None:
        """Test that validate if Carbide is accessible on Erekir"""
        self.world_setup()
        carbide_requirement = ["Large Plasma Bore", "Carbide Crucible"]

        self.assertFalse(self.can_reach_location("Produce Carbide on Erekir"))
        self.collect_by_name(caldera_requirement)
        self.assertFalse(self.can_reach_location("Produce Carbide on Erekir"))
        self.collect_by_name(carbide_requirement)
        self.assertTrue(self.can_reach_location("Produce Carbide on Erekir"))

    def test_erekir_surge_alloy_access(self) -> None:
        """Test that validate if Surge Alloy is accessible on Erekir"""
        self.world_setup()
        surge_alloy_requirement = ["Reinforced Pump", "Reinforced Conduit", "Impact Drill", "Electrolyzer", "Surge Crucible", "Oxidation Chamber"]

        self.assertFalse(self.can_reach_location("Produce Surge Alloy on Erekir"))
        self.collect_by_name(surge_alloy_requirement)
        self.assertTrue(self.can_reach_location("Produce Surge Alloy on Erekir"))

    def test_erekir_phase_fabric_access(self) -> None:
        """Test that validate if Phase Fabric is accessible on Erekir"""
        self.world_setup()
        phase_fabric_requirement = ["Large Plasma Bore", "Carbide Crucible", "Phase Synthesizer"]

        self.assertFalse(self.can_reach_location("Produce Phase Fabric on Erekir"))
        self.collect_by_name(caldera_requirement)
        self.assertFalse(self.can_reach_location("Produce Phase Fabric on Erekir"))
        self.collect_by_name(phase_fabric_requirement)
        self.assertTrue(self.can_reach_location("Produce Phase Fabric on Erekir"))
