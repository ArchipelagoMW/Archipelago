from Fill import distribute_items_restrictive
from ..PrimeOptions import DoorColorRandomization
from ..Items import SuitUpgrade
from ..DoorRando import DoorLockType
from ..BlastShieldRando import BlastShieldType, WorldBlastShieldMapping

from ..Config import make_config, starting_inventory
from ..data.AreaNames import MetroidPrimeArea
from ..data.RoomNames import RoomName
from . import MetroidPrimeTestBase, MetroidPrimeWithOverridesTestBase
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .. import MetroidPrimeWorld


class TestNoDoorRando(MetroidPrimeTestBase):
    options = {
        "door_color_randomization": DoorColorRandomization.option_none,
    }

    def test_all_door_types_are_not_randomized(self):
        self.world.generate_early()
        world: "MetroidPrimeWorld" = self.world
        self.assertEqual(world.door_color_mapping, None)

    def test_starting_beam_is_power(self):
        self.world.generate_early()
        world: "MetroidPrimeWorld" = self.world
        distribute_items_restrictive(world.multiworld)
        config = make_config(world)
        self.assertTrue(config["gameConfig"]["startingItems"]["powerBeam"] == 1)
        self.assertEqual(
            config["gameConfig"]["startingBeam"],
            "Power",
            "Starting beam should be Power",
        )


class TestStartingBeamRandoWithNoDoorRando(MetroidPrimeTestBase):
    options = {
        "door_color_randomization": DoorColorRandomization.option_none,
        "randomize_starting_beam": True,
        "include_power_beam_doors": True,
    }


class TestGlobalDoorRando(MetroidPrimeTestBase):
    options = {
        "door_color_randomization": DoorColorRandomization.option_global,
    }

    def test_all_door_types_are_randomized_globally(self):
        self.world.generate_early()
        world: "MetroidPrimeWorld" = self.world
        first_mapping = None
        assert world.door_color_mapping
        self.assertTrue(
            len(world.door_color_mapping) > 0, "Door color mapping should not be empty"
        )
        for area in MetroidPrimeArea:
            if not world.door_color_mapping[area.value].type_mapping:
                continue
            if first_mapping is None:
                first_mapping = world.door_color_mapping[area.value].type_mapping
                for original, new in first_mapping.items():
                    self.assertNotEqual(
                        original, new, "Door color should be randomized"
                    )
            else:
                self.assertEqual(
                    first_mapping,
                    world.door_color_mapping[area.value].type_mapping,
                    "Door color should be the same for all areas",
                )

    def test_door_colors_are_updated_in_config(self):
        self.world.generate_early()
        world: "MetroidPrimeWorld" = self.world
        distribute_items_restrictive(world.multiworld)
        config = make_config(world)
        self.assertNotEqual(
            config["levelData"]["Chozo Ruins"]["rooms"]["Ruined Shrine"]["doors"]["0"][
                "shieldType"
            ],
            DoorLockType.Wave.value,
        )


class TestRegionalDoorRando(MetroidPrimeTestBase):
    options = {
        "door_color_randomization": DoorColorRandomization.option_regional,
    }

    def test_all_door_types_are_randomized_across_a_region(self):
        self.world.generate_early()
        world: "MetroidPrimeWorld" = self.world
        first_mapping = None
        assert world.door_color_mapping
        self.assertTrue(
            len(world.door_color_mapping) > 0, "Door color mapping should not be empty"
        )
        same_areas: List[MetroidPrimeArea] = []
        for area in MetroidPrimeArea:
            if not world.door_color_mapping[area.value].type_mapping:
                continue
            if first_mapping is None:
                first_mapping = world.door_color_mapping[area.value].type_mapping
                for original, new in first_mapping.items():
                    self.assertNotEqual(
                        original, new, "Door color should be randomized"
                    )
            elif first_mapping == world.door_color_mapping[area.value].type_mapping:
                same_areas.append(area)
        self.assertTrue(
            len(same_areas) < 4,
            "Door color should be different for each area generally",
        )

    def test_door_colors_are_updated_in_config(self):
        self.world.generate_early()
        world: "MetroidPrimeWorld" = self.world
        distribute_items_restrictive(world.multiworld)
        config = make_config(world)
        self.assertNotEqual(
            config["levelData"]["Chozo Ruins"]["rooms"]["Ruined Shrine"]["doors"]["0"][
                "shieldType"
            ],
            DoorLockType.Wave.value,
        )


class TestDoorRandoWithDifferentStartRoomNonRequiredBeam(
    MetroidPrimeWithOverridesTestBase
):
    run_default_tests = False  # type: ignore
    options = {
        "door_color_randomization": DoorColorRandomization.option_global,
    }
    overrides = {
        "starting_room_name": RoomName.Tower_Chamber.value,
    }

    def test_starting_beam_is_not_wave_for_non_required_beam(self):
        self.world.generate_early()
        self.assertEqual(starting_inventory(self.world, SuitUpgrade.Wave_Beam.value), 0)


class TestDoorRandoWithDifferentStartRoomWithRequiredBeam(
    MetroidPrimeWithOverridesTestBase
):
    run_default_tests = False  # type: ignore
    options = {
        "door_color_randomization": DoorColorRandomization.option_global,
    }
    overrides = {
        "starting_room_name": RoomName.Save_Station_B.value,
    }

    def test_starting_beam_is_not_wave_for_required_start_beam(self):
        self.world.generate_early()
        self.world.generate_early()
        self.assertEqual(
            starting_inventory(self.world, SuitUpgrade.Plasma_Beam.value), 1
        )
        self.assertEqual(starting_inventory(self.world, SuitUpgrade.Wave_Beam.value), 0)


class TestGlobalDoorRandoWithBombAndPowerDoors(MetroidPrimeTestBase):
    options = {
        "door_color_randomization": DoorColorRandomization.option_global,
        "include_morph_ball_bomb_doors": True,
        "include_power_beam_doors": True,
    }

    def test_bomb_doors_are_applied_to_single_region_that_is_not_start(self):
        world: "MetroidPrimeWorld" = self.world
        world.generate_early()
        bomb_door_region = None

        assert world.door_color_mapping
        for area, mapping in world.door_color_mapping.items():
            if DoorLockType.Bomb.value in mapping.type_mapping.values():
                if bomb_door_region is None:
                    bomb_door_region = area
                else:
                    self.fail("Bomb doors should only be applied to a single region")

        self.assertIsNotNone(
            bomb_door_region, "Bomb doors should be applied to one region"
        )
        self.assertNotEqual(
            bomb_door_region,
            MetroidPrimeArea.Tallon_Overworld.value,
            "Bomb doors should not be applied to the starting region",
        )

    def test_power_beam_doors_are_included_in_at_least_one_region(self):
        self.world.generate_early()
        world: "MetroidPrimeWorld" = self.world
        power_beam_door_found = False

        assert world.door_color_mapping
        for mapping in world.door_color_mapping.values():
            if DoorLockType.Power_Beam.value in mapping.type_mapping.values():
                power_beam_door_found = True
                break

        self.assertTrue(
            power_beam_door_found,
            "Power beam doors should be included in at least one region",
        )


class TestRegionalobalDoorRandoWithBombAndPowerDoors(MetroidPrimeTestBase):
    options = {
        "door_color_randomization": DoorColorRandomization.option_regional,
        "include_morph_ball_bomb_doors": True,
        "include_power_beam_doors": True,
    }

    def test_bomb_doors_are_applied_to_single_region_that_is_not_start(self):
        world: "MetroidPrimeWorld" = self.world
        world.generate_early()
        bomb_door_region = None

        assert world.door_color_mapping
        for area, mapping in world.door_color_mapping.items():
            if DoorLockType.Bomb.value in mapping.type_mapping.values():
                if bomb_door_region is None:
                    bomb_door_region = area
                else:
                    self.fail("Bomb doors should only be applied to a single region")

        self.assertIsNotNone(
            bomb_door_region, "Bomb doors should be applied to one region"
        )
        self.assertNotEqual(
            bomb_door_region,
            MetroidPrimeArea.Tallon_Overworld.value,
            "Bomb doors should not be applied to the starting region",
        )


class TestBeamRandoWithDoorRando(MetroidPrimeTestBase):
    options = {
        "door_color_randomization": DoorColorRandomization.option_regional,
        "include_power_beam_doors": True,
        "randomize_starting_beam": True,
    }

    def test_when_power_beam_is_not_starting_beam_and_power_beam_doors_are_included_the_new_starting_beam_doors_are_not_included(
        self,
    ):
        world: "MetroidPrimeWorld" = self.world
        world.generate_early()

        assert world.starting_room_data.selected_loadout
        # Check if the starting beam is not the power beam
        starting_beam = world.starting_room_data.selected_loadout.starting_beam
        self.assertNotEqual(
            starting_beam,
            SuitUpgrade.Power_Beam.value,
            "Starting beam should not be the power beam",
        )

        new_starting_beam_doors_found = False

        assert world.door_color_mapping
        for _, mapping in world.door_color_mapping.items():
            if starting_beam.value in mapping.type_mapping.values():
                new_starting_beam_doors_found = True
                break

        self.assertFalse(
            new_starting_beam_doors_found,
            "New starting beam doors should not be included when power beam doors are included",
        )


class TestDisabledBlastShieldConnections(MetroidPrimeWithOverridesTestBase):
    """Test that doors with disabled blast shields do not create connections between regions"""
    
    run_default_tests = False  # type: ignore
    options = {
        "trick_difficulty": "medium",
    }
    overrides = {
        "blast_shield_mapping": WorldBlastShieldMapping.from_option_value(
            {
                "Tallon Overworld": {
                    "area": "Tallon Overworld",
                    "type_mapping": {
                        "Landing Site": {
                            0: "Disabled",  # Door to Gully
                        }
                    },
                }
            }
        ),
    }

    def test_normal_door_connections_not_created_for_disabled_blast_shields(self):
        """Verify that no connection exists between Landing Site and Gully when door has disabled blast shield"""
        world: "MetroidPrimeWorld" = self.world
        
        # Get the regions
        landing_site = world.get_region(RoomName.Landing_Site.value)
        gully = world.get_region(RoomName.Gully.value)
        
        # Check that there's no direct connection from Landing Site to Gully
        landing_to_gully_found = False
        for exit in landing_site.exits:
            if exit.connected_region == gully:
                landing_to_gully_found = True
                break
                
        self.assertFalse(
            landing_to_gully_found,
            "Connection from Landing Site to Gully should not exist when door has disabled blast shield"
        )
        
        # Also verify the reverse connection doesn't exist
        gully_to_landing_found = False
        for exit in gully.exits:
            if exit.connected_region == landing_site:
                gully_to_landing_found = True
                break
                
        self.assertFalse(
            gully_to_landing_found,
            "Connection from Gully to Landing Site should not exist when door has disabled blast shield"
        )


class TestDisabledBlastShieldSubRegionConnections(MetroidPrimeWithOverridesTestBase):
    """Test that sub-region connections are not created when doors have disabled blast shields"""
    
    run_default_tests = False  # type: ignore
    options = {
        "trick_difficulty": "medium",
    }
    overrides = {
        "blast_shield_mapping": WorldBlastShieldMapping.from_option_value(
            {
                "Phendrana Drifts": {
                    "area": "Phendrana Drifts",
                    "type_mapping": {
                        "Plaza Walkway": {
                            0: "Disabled",  # Sub-region door to Phendrana Shorelines
                        }
                    },
                }
            }
        ),
    }

    def test_sub_region_connections_not_created_for_disabled_blast_shields(self):
        """Verify that sub-region connections are not created when doors have disabled blast shields"""
        world: "MetroidPrimeWorld" = self.world
        
        # Get the regions - Plaza Walkway connects to Phendrana Shorelines via sub-region door
        plaza_walkway = world.get_region(RoomName.Plaza_Walkway.value)
        phendrana_shorelines = world.get_region(RoomName.Phendrana_Shorelines.value)
        ruins_entryway = world.get_region(RoomName.Ruins_Entryway.value)
        
        # Check that there's no connection from Plaza Walkway to Phendrana Shorelines
        plaza_to_shorelines_found = False
        for exit in plaza_walkway.exits:
            if exit.connected_region == phendrana_shorelines:
                plaza_to_shorelines_found = True
                break
                
        self.assertFalse(
            plaza_to_shorelines_found,
            "Sub-region connection from Plaza Walkway to Phendrana Shorelines should not exist when door has disabled blast shield"
        )
        
        # Also check that the paired sub-region connection doesn't exist
        # (Plaza Walkway door 0 connects to Phendrana Shorelines door 3, which connects to Ruins Entryway)
        plaza_to_ruins_found = False
        for exit in plaza_walkway.exits:
            if exit.connected_region == ruins_entryway:
                plaza_to_ruins_found = True
                break
                
        self.assertFalse(
            plaza_to_ruins_found,
            "Sub-region connection from Plaza Walkway to Ruins Entryway should not exist when door has disabled blast shield"
        )
        
        # The intermediate connection through sub-regions should also not exist
        # Plaza Walkway normally has 2 exits: Ice Ruins East and Phendrana Shorelines (then to Ruins Entryway)
        # With the disabled door, it should only have 1 exit
        expected_exit_count = 1
        actual_exit_count = len(plaza_walkway.exits)
        
        self.assertEqual(
            actual_exit_count,
            expected_exit_count,
            f"Plaza Walkway should have {expected_exit_count} exit when sub-region door is disabled. Found {actual_exit_count} exits"
        )
