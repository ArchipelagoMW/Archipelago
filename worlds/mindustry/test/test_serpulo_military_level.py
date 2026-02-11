from worlds.mindustry.test import MindustryTestBase

graphite = ["Graphite produced on Serpulo", "Graphite Press"]
silicon = ["Silicon produced on Serpulo", "Silicon Smelter"]
power = ["Combustion Generator"]
pump = ["Mechanical Pump", "Conduit"]
oil = ["Conduit", "Oil produced on Serpulo"] + pump
titanium = ["Titanium produced on Serpulo", "Pneumatic Drill"]
plastanium = ["Plastanium produced on Serpulo", "Plastanium Compressor"] + oil
metaglass = ["Metaglass produced on Serpulo", "Kiln"]
pyratite = ["Pyratite produced on Serpulo", "Pyratite Mixer"]
thorium = ["Thorium produced on Serpulo", "Laser Drill", "Windswept Islands captured"]
surge_alloy = ["Surge Alloy produced on Serpulo", "Surge Smelter"]
phase_fabric = ["Phase Fabric produced on Serpulo", "Phase Weaver"]

class TestSerpuloMilitaryLevel(MindustryTestBase):
    """Unit test to validate access to capturing a sector when military level option is turned on."""
    options = {
        "campaign_choice": 0,
        "military_level_tracking": True
    }


    def test_serpulo_ruinous_shores_military_level(self) -> None:
        """Test Ruinous Shores military level requirement"""
        self.world_setup()
        military = ["Hail", "Arc", "Salvo"]
        material_requirement = power + graphite + silicon + titanium

        self.collect_by_name(material_requirement)
        self.assertFalse(self.can_reach_location('Capture Ruinous Shores'))
        self.collect_by_name(military) # level 5
        self.assertTrue(self.can_reach_location('Capture Ruinous Shores'))

    def test_serpulo_windswept_islands_military_level(self) -> None:
        """Test Windswept Islands military level requirement"""
        self.world_setup()
        military = ["Hail", "Arc", "Salvo", "Scorch"]
        material_requirement = power + graphite + silicon + titanium

        self.collect_by_name(material_requirement)
        self.assertFalse(self.can_reach_location('Capture Windswept Islands'))
        self.collect_by_name(military)  # level 6
        self.assertTrue(self.can_reach_location('Capture Windswept Islands'))

    def test_tar_fields_military_level(self) -> None:
        """Test Tar Fields military level requirement"""
        self.world_setup()
        military = ["Hail", "Arc", "Salvo", "Swarmer"]
        material_requirement = power + graphite + silicon + titanium + plastanium + metaglass + pyratite

        self.collect_by_name(material_requirement)
        self.assertFalse(self.can_reach_location('Capture Tar Fields'))
        self.collect_by_name(military)  # level 10
        self.assertTrue(self.can_reach_location('Capture Tar Fields'))

    def test_impact_0078_military_level(self) -> None:
        """Test Impact 0078 military level requirement"""
        self.world_setup()
        military = ["Hail", "Arc", "Salvo", "Swarmer", "Lancer"]
        material_requirement = power + graphite + silicon + titanium + plastanium + metaglass + pyratite

        self.collect_by_name(material_requirement)
        self.assertFalse(self.can_reach_location('Capture Impact 0078'))
        self.collect_by_name(military)  # level 13
        self.assertTrue(self.can_reach_location('Capture Impact 0078'))

    def test_desolate_rift_military_level(self) -> None:
        """Test Desolate Rift military level requirement"""
        self.world_setup()
        military = ["Hail", "Arc", "Scorch", "Salvo", "Swarmer", "Lancer", "Parallax", "Wave", "Ripple", "Meltdown"]
        material_requirement = (power + graphite + silicon + titanium + plastanium + metaglass + pyratite + thorium +
                                surge_alloy)

        self.collect_by_name(material_requirement)
        self.assertFalse(self.can_reach_location('Capture Desolate Rift'))
        self.collect_by_name(military)  # level 20
        self.assertTrue(self.can_reach_location('Capture Desolate Rift'))

    def test_planetary_launch_terminal_military_level(self) -> None:
        """Test Planetary Launch Terminal military level requirement"""
        self.world_setup()
        military = ["Hail", "Arc", "Scorch", "Salvo", "Swarmer", "Lancer", "Parallax", "Wave", "Ripple", "Meltdown",
                    "Foreshadow", "Spectre", "Segment", "Fuse", "Mender"]
        material_requirement = (power + graphite + silicon + titanium + plastanium + metaglass + pyratite + thorium +
                                surge_alloy + phase_fabric)

        self.collect_by_name(material_requirement)
        self.assertFalse(self.can_reach_location('Capture Planetary Launch Terminal'))
        self.collect_by_name(military)  # level 56
        self.assertTrue(self.can_reach_location('Capture Planetary Launch Terminal'))

    def test_extraction_outpost_military_level(self) -> None:
        """Test Extraction Outpost military level requirement"""
        self.world_setup()
        military = ["Hail", "Arc", "Salvo", "Swarmer"]
        material_requirement = power + graphite + silicon + titanium + plastanium + metaglass + pyratite

        self.collect_by_name(material_requirement)
        self.assertFalse(self.can_reach_location('Capture Extraction Outpost'))
        self.collect_by_name(military)  # level 10
        self.assertFalse(self.can_reach_location('Capture Extraction Outpost'))
        self.collect_by_name(["Progressive Offensive Ground Unit", "Ground Factory"]) # Sector has enemy base
        self.assertTrue(self.can_reach_location('Capture Extraction Outpost'))

    def test_salt_flats_military_level(self) -> None:
        """Test Salt Flats military level requirement"""
        self.world_setup()
        self.world_setup()
        military = ["Hail", "Arc", "Salvo", "Swarmer"]
        material_requirement = power + graphite + silicon + titanium + plastanium + metaglass + pyratite

        self.collect_by_name(material_requirement)
        self.assertFalse(self.can_reach_location('Capture Salt Flats'))
        self.collect_by_name(military)  # level 10
        self.assertFalse(self.can_reach_location('Capture Salt Flats'))
        self.collect_by_name(["Progressive Offensive Ground Unit", "Ground Factory"]) # Sector has enemy base
        self.assertTrue(self.can_reach_location('Capture Salt Flats'))

    def test_coastline_military_level(self) -> None:
        """Test Coastline military level requirement"""
        self.world_setup()
        military = ["Hail", "Arc", "Salvo", "Swarmer"]
        material_requirement = power + graphite + silicon + titanium + plastanium + metaglass + pyratite

        self.collect_by_name(material_requirement)
        self.assertFalse(self.can_reach_location('Capture Coastline'))
        self.collect_by_name(military)  # level 10
        self.assertFalse(self.can_reach_location('Capture Coastline'))
        self.collect_by_name(["Progressive Offensive Ground Unit", "Ground Factory"])  # Sector has enemy base
        self.assertTrue(self.can_reach_location('Capture Coastline'))

    def test_naval_fortress_military_level(self) -> None:
        """Test Naval Fortress military level requirement"""
        self.world_setup()
        military = ["Hail", "Arc", "Scorch", "Salvo", "Swarmer", "Lancer", "Parallax", "Wave", "Ripple", "Meltdown"]
        material_requirement = (power + graphite + silicon + titanium + plastanium + metaglass + pyratite + thorium +
                                surge_alloy)

        self.collect_by_name(material_requirement)
        self.assertFalse(self.can_reach_location('Capture Naval Fortress'))
        self.collect_by_name(military)  # level 30
        self.assertFalse(self.can_reach_location('Capture Naval Fortress'))
        self.collect_by_name(["Progressive Offensive Ground Unit", "Ground Factory"]) # Previous sector requirement
        self.assertFalse(self.can_reach_location('Capture Naval Fortress'))
        self.collect_by_name(["Progressive Offensive Naval Unit", "Naval Factory"])  # Sector has enemy base
        self.assertTrue(self.can_reach_location('Capture Naval Fortress'))

    def test_overgrowth_military_level(self) -> None:
        """Test Overgrowth military level requirement"""
        self.world_setup()
        military = ["Hail", "Arc", "Salvo", "Swarmer"]
        material_requirement = power + graphite + silicon + titanium + plastanium + metaglass + pyratite

        self.collect_by_name(material_requirement)
        self.assertFalse(self.can_reach_location('Capture Overgrowth'))
        self.collect_by_name(military)  # level 10
        self.assertTrue(self.can_reach_location('Capture Overgrowth'))

    def test_biomass_synthesis_facility_military_level(self) -> None:
        """Test Biomass Synthesis Facility military level requirement"""
        self.world_setup()
        military = ["Hail", "Arc", "Salvo", "Scorch"]
        material_requirement = power + graphite + silicon + titanium

        self.collect_by_name(material_requirement)
        self.assertFalse(self.can_reach_location('Capture Biomass Synthesis Facility'))
        self.collect_by_name(military)  # level 6
        self.assertTrue(self.can_reach_location('Capture Biomass Synthesis Facility'))

    def test_stained_mountains_military_level(self) -> None:
        """Test Stained Mountains military level requirement"""
        self.world_setup()
        military = ["Hail", "Arc", "Salvo", "Scorch", "Parallax"]
        material_requirement = power + graphite + silicon + titanium

        self.collect_by_name(material_requirement)
        self.assertFalse(self.can_reach_location('Capture Stained Mountains'))
        self.collect_by_name(military)  # level 7
        self.assertTrue(self.can_reach_location('Capture Stained Mountains'))

    def test_fungal_pass_military_level(self) -> None:
        """Test Fungal Pass military level requirement"""
        self.world_setup()
        military = ["Hail", "Arc", "Salvo", "Scorch", "Parallax", "Wave"]
        material_requirement = power + graphite + silicon + titanium + metaglass + pump

        self.collect_by_name(material_requirement)
        self.assertFalse(self.can_reach_location('Capture Fungal Pass'))
        self.collect_by_name(military)  # level 8
        self.assertFalse(self.can_reach_location('Capture Fungal Pass'))
        self.collect_by_name(["Progressive Offensive Ground Unit", "Ground Factory"])  # Sector has enemy base
        self.assertTrue(self.can_reach_location('Capture Fungal Pass'))


    def test_nuclear_production_complex_military_level(self) -> None:
        """Test Nuclear Production Complex military level requirement"""
        self.world_setup()
        military = ["Arc", "Salvo", "Swarmer", "Lancer"]
        material_requirement = power + graphite + silicon + titanium + plastanium + metaglass + pyratite

        self.collect_by_name(material_requirement)
        self.assertFalse(self.can_reach_location('Capture Nuclear Production Complex'))
        self.collect_by_name(military)  # level 12
        self.assertFalse(self.can_reach_location('Capture Nuclear Production Complex'))
        self.collect_by_name(["Progressive Offensive Ground Unit", "Ground Factory"])  # Sector has enemy base
        self.assertTrue(self.can_reach_location('Capture Nuclear Production Complex'))
