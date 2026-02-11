from worlds.mindustry.test import MindustryTestBase

power = ["Combustion Generator"]

class TestSerpuloResourcesAccess(MindustryTestBase):
    """Unit test to validate rules for resources production on Serpulo."""
    options = {
        "campaign_choice": 0,
        "logistic_distribution": 0,
        "military_level_tracking": False
    }

    def test_serpulo_sphere_0_resource(self) -> None:
        """Test that validate that sphere 0 resources can be produced without items"""
        self.world_setup()

        self.assertTrue(self.can_reach_region("Copper"))
        self.assertTrue(self.can_reach_region("Lead"))
        self.assertTrue(self.can_reach_region("Coal"))
        self.assertTrue(self.can_reach_region("Sand Serpulo"))
        self.assertTrue(self.can_reach_region("Scrap"))

    def test_serpulo_graphite_access(self) -> None:
        """Test that validate if graphite is accessible on Serpulo"""
        self.world_setup()

        self.assertFalse(self.can_reach_location("Produce Graphite on Serpulo"))
        self.collect_by_name("Graphite Press")
        self.assertTrue(self.can_reach_location("Produce Graphite on Serpulo"))

    def test_serpulo_silicon_access(self) -> None:
        """Test that validate if silicon is accessible on Serpulo"""
        self.world_setup()
        silicon_requirements = power + ["Silicon Smelter"]

        self.assertFalse(self.can_reach_location("Produce Silicon on Serpulo"))
        self.collect_by_name(silicon_requirements)
        self.assertTrue(self.can_reach_location("Produce Silicon on Serpulo"))

    def test_serpulo_metaglass_access(self) -> None:
        """Test that validate if Metaglass is accessible on Serpulo"""
        self.world_setup()
        metaglass_requirement = power + ["Kiln", "Graphite Press"]

        self.assertFalse(self.can_reach_location("Produce Metaglass on Serpulo"))
        self.collect_by_name(metaglass_requirement)
        self.assertTrue(self.can_reach_location("Produce Metaglass on Serpulo"))

    def test_serpulo_titanium_access(self) -> None:
        """Test that validate if Titanium is accessible on Serpulo"""
        self.world_setup()
        titanium_requirement = power + ["Pneumatic Drill", "Graphite Press"]

        self.assertFalse(self.can_reach_location("Produce Titanium on Serpulo"))
        self.collect_by_name(titanium_requirement)
        self.assertTrue(self.can_reach_location("Produce Titanium on Serpulo"))


    def test_serpulo_thorium_access(self) -> None:
        """Test that validate if Thorium is accessible on Serpulo"""
        self.world_setup()
        thorium_requirement = power + ["Laser Drill", "Graphite Press", "Silicon Smelter", "Pneumatic Drill"]

        self.assertFalse(self.can_reach_location("Produce Thorium on Serpulo"))
        self.collect_by_name(thorium_requirement)
        self.assertTrue(self.can_reach_location("Produce Thorium on Serpulo"))

    def test_serpulo_plastanium_access(self) -> None:
        """Test that validate if Plastanium is accessible on Serpulo"""
        self.world_setup()
        plastanium_requirement = power + ["Mechanical Pump", "Conduit", "Kiln", "Graphite Press", "Silicon Smelter", "Pneumatic Drill", "Plastanium Compressor"]

        self.assertFalse(self.can_reach_location("Produce Plastanium on Serpulo"))
        self.collect_by_name(plastanium_requirement)
        self.assertTrue(self.can_reach_location("Produce Plastanium on Serpulo"))

    def test_serpulo_phase_fabric_access(self) -> None:
        """Test that validate if Phase Fabric is accessible on Serpulo"""
        self.world_setup()
        phase_fabric_requirement = power + ["Phase Weaver", "Silicon Smelter", "Laser Drill", "Pneumatic Drill", "Graphite Press"]

        self.assertFalse(self.can_reach_location("Produce Phase Fabric on Serpulo"))
        self.collect_by_name(phase_fabric_requirement)
        self.assertTrue(self.can_reach_location("Produce Phase Fabric on Serpulo"))

    def test_serpulo_surge_alloy_access(self) -> None:
        """Test that validate if Surge Alloy is accessible on Serpulo"""
        self.world_setup()
        surge_alloy_requirement = power + ["Surge Smelter", "Silicon Smelter", "Laser Drill", "Pneumatic Drill",
                                            "Graphite Press"]

        self.assertFalse(self.can_reach_location("Produce Surge Alloy on Serpulo"))
        self.collect_by_name(surge_alloy_requirement)
        self.assertTrue(self.can_reach_location("Produce Surge Alloy on Serpulo"))

    def test_serpulo_spore_pod_access(self) -> None:
        """Test that validate if Spore Pod is accessible on Serpulo"""
        self.world_setup()
        spore_pod_requirement = power + ["Cultivator", "Silicon Smelter", "Mechanical Pump", "Conduit", "Kiln", "Graphite Press"]

        self.assertFalse(self.can_reach_location("Produce Spore Pod on Serpulo"))
        self.collect_by_name(spore_pod_requirement)
        self.assertTrue(self.can_reach_location("Produce Spore Pod on Serpulo"))

    def test_serpulo_slag_access(self) -> None:
        """Test that validate if Slag is accessible on Serpulo"""
        self.world_setup()
        slag_requirement = power + ["Melter", "Graphite Press"]

        self.assertFalse(self.can_reach_location("Produce Slag on Serpulo"))
        self.collect_by_name(slag_requirement)
        self.assertTrue(self.can_reach_location("Produce Slag on Serpulo"))

    def test_serpulo_pyratite_access(self) -> None:
        """Test that validate if Pyratite is accessible on Serpulo"""
        self.world_setup()
        pyratite_requirement = power + ["Pyratite Mixer"]

        self.assertFalse(self.can_reach_location("Produce Pyratite on Serpulo"))
        self.collect_by_name(pyratite_requirement)
        self.assertTrue(self.can_reach_location("Produce Pyratite on Serpulo"))

    def test_serpulo_blast_compound_access(self) -> None:
        """Test that validate if Blast Compound is accessible on Serpulo"""
        self.world_setup()
        blast_compound_requirement = power + ["Blast Mixer", "Pneumatic Drill", "Graphite Press", "Pyratite Mixer"]

        self.assertFalse(self.can_reach_location("Produce Blast Compound on Serpulo"))
        self.collect_by_name(blast_compound_requirement)
        self.assertTrue(self.can_reach_location("Produce Blast Compound on Serpulo"))