from worlds.mindustry.test import MindustryTestBase

tungsten = ["Impact Drill", "Reinforced Conduit"]
ozone = ["Electrolyzer"]
oxide = ["Oxidation Chamber"]
thorium = ["Large Plasma Bore"]
carbide = ["Carbide Crucible"]
surge_alloy = ["Surge Crucible", "Reinforced Pump", "Reinforced Conduit"]
phase_fabric = ["Phase Synthesizer"]
caldera_requirement = ["Ship Fabricator", "Ship Refabricator", "Progressive Ships", "Mech Fabricator",
                       "Progressive Mechs", "Payload Mass Driver", "Chemical Combustion Chamber", "Beam Tower",
                       "Reinforced Container", "Payload Loader", "Payload Unloader"]
resources_requirement = tungsten + ozone + oxide + thorium + carbide + surge_alloy + phase_fabric



class TestErekirGoal(MindustryTestBase):
    """Unit test to validate that the game can be completed on Erekir with both goal option."""


    def test_erekir_resources_goal(self) -> None:
        """Test that the goal can be reached with resources goal requirements."""
        self.options["campaign_choice"] = 1
        self.options["goal"] = 0
        self.options["military_level_tracking"] = False
        self.world_setup()

        self.collect_by_name(resources_requirement)
        self.assertFalse(self.can_reach_region("Victory Erekir"))
        self.collect_by_name(caldera_requirement)
        self.assertTrue(self.can_reach_region("Victory Erekir"))

    def test_erekir_conquest_goal(self) -> None:
        """Test that the goal can be reached with conquest goal requirements."""
        #Same test as resources goal since without the military tracking option turned on, there are no additional requirements.
        self.options["campaign_choice"] = 1
        self.options["goal"] = 1
        self.options["military_level_tracking"] = False
        self.world_setup()

        self.collect_by_name(resources_requirement)
        self.assertFalse(self.can_reach_region("Victory Erekir"))
        self.collect_by_name(caldera_requirement)
        self.assertTrue(self.can_reach_region("Victory Erekir"))
