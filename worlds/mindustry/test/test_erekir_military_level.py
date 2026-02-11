from worlds.mindustry.test import MindustryTestBase

tungsten = ["Tungsten produced on Erekir", "Impact Drill"]
ozone = ["Ozone produced on Erekir", "Electrolyzer"] + tungsten
oxide = ["Oxide produced on Erekir"] + ozone
hydrogen = ["Hydrogen produced on Erekir", "Electrolyzer"]
thorium = ["Thorium produced on Erekir", "Large Plasma Bore"]
carbide = ["Carbide produced on Erekir", "Carbide Crucible"] + thorium
nitrogen = ["Nitrogen produced on Erekir", "Atmospheric Concentrator"] + carbide
cyanogen = ["Cyanogen produced on Erekir", "Cyanogen Synthesizer"] + carbide
pump = ["Reinforced Pump", "Reinforced Conduit"]
arkycite = ["Arkycite produced on Erekir"] + pump
slag = ["Slag produced on Erekir"] + pump
surge_alloy = ["Surge Alloy produced on Erekir", "Surge Crucible", "Mech Fabricator", "Progressive Mechs"] + tungsten + oxide + pump #Mechs for intersect capture
phase_fabric = ["Phase Fabric produced on Erekir", "Phase Synthesizer"] + thorium + tungsten + carbide
pre_ravine_requirements = ["Chemical Combustion Chamber", "Mech Fabricator", "Progressive Mechs", "Ship Fabricator", "Progressive Ships", "Impact Drill", "Payload Mass Driver", "Oxidation Chamber", "Beam Tower", "Ship Refabricator", "Reinforced Container", "Payload Loader", "Payload Unloader"] + pump
all_resources = tungsten + ozone + oxide + hydrogen + thorium + carbide + nitrogen + cyanogen + arkycite + slag + surge_alloy + phase_fabric


class TestErekirMilitaryLevel(MindustryTestBase):
    """Unit test to validate access to capturing a sector when military level option is turned on."""
    options = {
        "campaign_choice": 1,
        "military_level_tracking": True
    }


    def test_erekir_ravine_military_level(self) -> None:
        """Test Ravine military level requirement"""
        self.world_setup()
        military = ["Diffuse", "Sublimate", "Reinforced Conduit"] # Def level 3
        material_requirement = tungsten + oxide + ozone

        self.collect_by_name(material_requirement)
        self.assertFalse(self.can_reach_location('Capture Ravine'))
        self.collect_by_name(military)
        self.assertFalse(self.can_reach_location('Capture Ravine'))
        self.collect_by_name(pre_ravine_requirements)
        self.assertTrue(self.can_reach_location('Capture Ravine'))

    def test_erekir_caldera_military_level(self) -> None:
        """Test Caldera military level requirement"""
        self.world_setup()
        military = ["Diffuse", "Sublimate", "Reinforced Conduit"] # Def level 3
        material_requirement = tungsten + oxide + ozone + surge_alloy

        self.collect_by_name(pre_ravine_requirements)
        self.assertFalse(self.can_reach_location('Capture Caldera'))
        self.collect_by_name(material_requirement)
        self.assertFalse(self.can_reach_location('Capture Caldera'))
        self.collect_by_name(military)
        self.assertTrue(self.can_reach_location('Capture Caldera'))

    def test_erekir_stronghold_military_level(self) -> None:
        """Test Stronghold military level requirement"""
        self.world_setup()
        military = ["Diffuse", "Sublimate", "Disperse"] # Def lvl 6
        unit_requirement = ["Mech Refrabricator", "Progressive Tanks", "Tank Refabricator"] # Unit lvl 8

        self.collect_by_name(all_resources)
        self.assertFalse(self.can_reach_location('Capture Stronghold'))
        self.collect_by_name(pre_ravine_requirements)
        self.assertFalse(self.can_reach_location('Capture Stronghold'))
        self.collect_by_name(unit_requirement)
        self.assertFalse(self.can_reach_location('Capture Stronghold'))
        self.collect_by_name(military)
        self.assertTrue(self.can_reach_location('Capture Stronghold'))


    def test_erekir_crevice_military_level(self) -> None:
        """Test Crevice military level requirement"""
        self.world_setup()
        military = ["Diffuse", "Sublimate", "Disperse", "Tungsten Wall", "Reinforced Surge Wall"]  # Def lvl 10
        unit_requirement = ["Mech Refrabricator", "Progressive Tanks", "Tank Refabricator"] # Unit lvl 8

        self.collect_by_name(all_resources)
        self.assertFalse(self.can_reach_location('Capture Crevice'))
        self.collect_by_name(pre_ravine_requirements)
        self.assertFalse(self.can_reach_location('Capture Crevice'))
        self.collect_by_name(unit_requirement)
        self.assertFalse(self.can_reach_location('Capture Crevice'))
        self.collect_by_name(military)
        self.assertTrue(self.can_reach_location('Capture Crevice'))

    def test_erekir_siege_military_level(self) -> None:
        """Test Siege military level requirement"""
        self.world_setup()
        military = ["Diffuse", "Sublimate", "Disperse", "Tungsten Wall", "Reinforced Surge Wall"]  # Def lvl 10
        unit_requirement = ["Mech Refrabricator", "Progressive Tanks", "Tank Refabricator", "Prime Refabricator", ]  # Unit lvl 17

        self.collect_by_name(all_resources)
        self.assertFalse(self.can_reach_location('Capture Siege'))
        self.collect_by_name(pre_ravine_requirements)
        self.assertFalse(self.can_reach_location('Capture Siege'))
        self.collect_by_name(unit_requirement)
        self.assertFalse(self.can_reach_location('Capture Siege'))
        self.collect_by_name(military)
        self.assertTrue(self.can_reach_location('Capture Siege'))

    def test_erekir_crossroads_military_level(self) -> None:
        """Test Crossroads military level requirement"""
        self.world_setup()
        military = ["Diffuse", "Sublimate", "Disperse", "Tungsten Wall", "Reinforced Surge Wall", "Carbide Wall"]  # Def lvl 15
        unit_requirement = ["Mech Refrabricator", "Prime Refabricator", "Ship Assembler", "Mech Assembler",
                            "Large Beryllium Wall", "Constructor", "Large Tungsten Wall"]  # Unit lvl 20

        self.collect_by_name(all_resources)
        self.assertFalse(self.can_reach_location('Capture Crossroads'))
        self.collect_by_name(pre_ravine_requirements)
        self.assertFalse(self.can_reach_location('Capture Crossroads'))
        self.collect_by_name(unit_requirement)
        self.assertFalse(self.can_reach_location('Capture Crossroads'))
        self.collect_by_name(military)
        self.assertTrue(self.can_reach_location('Capture Crossroads'))

    def test_erekir_karst_military_level(self) -> None:
        """Test Karst military level requirement"""
        self.world_setup()
        military = ["Diffuse", "Sublimate", "Disperse", "Tungsten Wall", "Reinforced Surge Wall",
                    "Carbide Wall", "Afflict", "Scathe", "Titan", "Shielded Wall", "Regen Projector"]  # Def lvl 40
        unit_requirement = ["Mech Refrabricator", "Prime Refabricator", "Ship Assembler", "Mech Assembler",
                            "Large Beryllium Wall", "Constructor", "Large Tungsten Wall", "Progressive Tanks",
                            "Tank Refabricator"]  # Unit lvl 25

        self.collect_by_name(all_resources)
        self.assertFalse(self.can_reach_location('Capture Karst'))
        self.collect_by_name(pre_ravine_requirements)
        self.assertFalse(self.can_reach_location('Capture Karst'))
        self.collect_by_name(unit_requirement)
        self.assertFalse(self.can_reach_location('Capture Karst'))
        self.collect_by_name(military)
        self.assertTrue(self.can_reach_location('Capture Karst'))

    def test_erekir_origin_military_level(self) -> None:
        """Test Origin military level requirement"""
        self.world_setup()
        military = ["Diffuse", "Sublimate", "Disperse", "Tungsten Wall", "Reinforced Surge Wall",
                    "Carbide Wall", "Afflict", "Scathe", "Titan", "Shielded Wall", "Regen Projector",
                    "Build Tower", "Shockwave Tower"]  # Def lvl 52
        unit_requirement = ["Mech Refrabricator", "Prime Refabricator", "Ship Assembler", "Mech Assembler",
                            "Large Beryllium Wall", "Constructor", "Large Tungsten Wall", "Progressive Tanks",
                            "Tank Refabricator", "Basic Assembler Module", "Large Carbide Wall"]  # Unit lvl 35

        self.collect_by_name(all_resources)
        self.assertFalse(self.can_reach_location('Capture Origin'))
        self.collect_by_name(pre_ravine_requirements)
        self.assertFalse(self.can_reach_location('Capture Origin'))
        self.collect_by_name(unit_requirement)
        self.assertFalse(self.can_reach_location('Capture Origin'))
        self.collect_by_name(military)
        self.assertTrue(self.can_reach_location('Capture Origin'))
