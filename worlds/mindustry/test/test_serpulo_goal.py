from worlds.mindustry.test import MindustryTestBase

power = ["Combustion Generator"]
graphite = ["Graphite Press"]
titanium = ["Pneumatic Drill"]
thorium = ["Laser Drill"]
surge_alloy = ["Surge Smelter"]
phase_fabric = ["Phase Weaver"]
metaglass = ["Kiln"]
silicon = ["Silicon Smelter"]
pyratite = ["Pyratite Mixer"]
blast_compound = ["Blast Mixer"]
spore_pod = ["Cultivator"]
plastanium = ["Plastanium Compressor"]
oil = ["Mechanical Pump", "Conduit"]
resources_requirement = power + graphite + titanium + thorium + surge_alloy + phase_fabric + metaglass + silicon + pyratite + blast_compound + spore_pod + plastanium + oil
conquest_requirement = ["Ground Factory", "Progressive Offensive Ground Unit", "Naval Factory", "Progressive Offensive Naval Unit"]

class TestSerpuloGoal(MindustryTestBase):
    """Unit test to validate that the game can be completed on Serpulo with both goal option. """


    def test_serpulo_resources_goal(self) -> None:
        """Test that the goal can be reached with resources goal requirement"""
        self.options["campaign_choice"] = 0
        self.options["goal"] = 0
        self.options["military_level_tracking"] = False
        self.options["progressive_drills"] = False
        self.options["progressive_generators"] = False
        self.world_setup()

        self.collect_by_name(resources_requirement)
        self.assertTrue(self.can_reach_region("Victory Serpulo"))

    def test_serpulo_conquest_goal(self) -> None:
        """Test that the goal can be reached with conquest goal requirements."""
        self.options["campaign_choice"] = 0
        self.options["goal"] = 1
        self.options["military_level_tracking"] = False
        self.options["progressive_drills"] = False
        self.options["progressive_generators"] = False
        self.world_setup()

        self.collect_by_name(resources_requirement)
        self.assertFalse(self.can_reach_region("Victory Serpulo"))
        self.collect_by_name(conquest_requirement)
        self.assertTrue(self.can_reach_region("Victory Serpulo"))
