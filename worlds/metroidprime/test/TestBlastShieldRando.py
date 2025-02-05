import math
from Fill import distribute_items_restrictive
from ..PrimeOptions import BlastShieldRandomization, DoorColorRandomization
from ..data.DoorData import get_door_data_by_room_names
from ..data.BlastShieldRegions import get_valid_blast_shield_regions_by_area
from ..data.RoomData import AreaData
from ..data.AreaNames import MetroidPrimeArea
from ..BlastShieldRando import (
    MAX_BEAM_COMBO_DOORS_PER_AREA,
    AreaBlastShieldMapping,
    BlastShieldType,
    WorldBlastShieldMapping,
)
from ..DoorRando import DoorLockType, WorldDoorColorMapping
from ..Config import make_config
from ..data.RoomNames import RoomName
from ..Items import ProgressiveUpgrade, SuitUpgrade
from . import MetroidPrimeTestBase, MetroidPrimeWithOverridesTestBase
from typing import Any, Dict, TYPE_CHECKING, List, Tuple
from ..data.PhazonMines import PhazonMinesAreaData
from ..data.PhendranaDrifts import PhendranaDriftsAreaData
from ..data.MagmoorCaverns import MagmoorCavernsAreaData
from ..data.ChozoRuins import ChozoRuinsAreaData
from ..data.TallonOverworld import TallonOverworldAreaData

if TYPE_CHECKING:
    from .. import MetroidPrimeWorld


def _get_default_area_data(
    area: MetroidPrimeArea, world: "MetroidPrimeWorld"
) -> AreaData:
    mapping: Dict[MetroidPrimeArea, Any] = {
        MetroidPrimeArea.Tallon_Overworld: TallonOverworldAreaData,
        MetroidPrimeArea.Chozo_Ruins: ChozoRuinsAreaData,
        MetroidPrimeArea.Magmoor_Caverns: MagmoorCavernsAreaData,
        MetroidPrimeArea.Phendrana_Drifts: PhendranaDriftsAreaData,
        MetroidPrimeArea.Phazon_Mines: PhazonMinesAreaData,
    }

    return mapping[area](world)


beam_combo_items = [
    BlastShieldType.Flamethrower,
    BlastShieldType.Ice_Spreader,
    BlastShieldType.Wavebuster,
]


class TestNoBlastShieldRando(MetroidPrimeTestBase):
    options = {"blast_shield_randomization": BlastShieldRandomization.option_none}

    def test_all_blast_shields_are_not_randomized(self):
        """Verify that the blast shield to ruined shrine access is still there and not randomized"""
        test_region = RoomName.Ruined_Shrine_Access.value
        self.assertFalse(self.can_reach_region(test_region))
        self.collect_by_name(SuitUpgrade.Missile_Expansion.value)
        self.assertTrue(self.can_reach_region(test_region))

    def test_output_generates_correctly_with_paired_blast_shields(self):
        world: "MetroidPrimeWorld" = self.world
        distribute_items_restrictive(self.multiworld)
        config = make_config(world)
        level_key = config["levelData"]["Chozo Ruins"]["rooms"]
        self.assertTrue(
            level_key[RoomName.Main_Plaza.value]["doors"]["2"]["blastShieldType"]
            == BlastShieldType.Missile.value
        )
        self.assertTrue(
            level_key[RoomName.Ruined_Shrine_Access.value]["doors"]["1"][
                "blastShieldType"
            ]
            == BlastShieldType.Missile.value
        )

        self.assertTrue(
            level_key[RoomName.Reflecting_Pool.value]["doors"]["3"]["blastShieldType"]
            == BlastShieldType.Missile.value
        )
        self.assertTrue(
            level_key[RoomName.Antechamber.value]["doors"]["0"]["blastShieldType"]
            == BlastShieldType.Missile.value,
            "Paired mapping is not set",
        )
        self.assertTrue(
            level_key[RoomName.Antechamber.value]["doors"]["0"]["shieldType"]
            == DoorLockType.Blue.value,
            "Existing shield type override is not preserved",
        )


class TestReplaceBlastShieldRando(MetroidPrimeTestBase):
    options = {
        "blast_shield_randomization": BlastShieldRandomization.option_replace_existing
    }

    def test_blast_shield_mapping_is_generated_for_each_vanilla_door(self):
        world: "MetroidPrimeWorld" = self.world
        assert world.blast_shield_mapping
        for area, mapping in world.blast_shield_mapping.items():
            blast_shield_doors = [
                door_id
                for room in _get_default_area_data(
                    MetroidPrimeArea(area), self.world
                ).rooms.values()
                for door_id, door_data in room.doors.items()
                if door_data.blast_shield
            ]
            mapped_doors = [
                door for room in mapping.type_mapping.values() for door in room.keys()
            ]
            self.assertCountEqual(
                blast_shield_doors, mapped_doors, f"Missing doors in mapping for {area}"
            )
            for room in mapping.type_mapping.values():
                for shield_type in room.values():
                    self.assertIn(
                        shield_type,
                        [shield for shield in BlastShieldType],
                        "Invalid shield type",
                    )
                    self.assertNotEqual(
                        shield_type,
                        BlastShieldType.Missile,
                        "Missile should not be included in mapping for replace_existing",
                    )

    def test_blast_shields_are_replaced_in_config(self):
        """Verify that the blast shield to ruined shrine access is replaced"""
        world: "MetroidPrimeWorld" = self.world
        distribute_items_restrictive(self.multiworld)

        config = make_config(world)
        level_key = config["levelData"]["Chozo Ruins"]["rooms"]
        self.assertTrue(
            level_key[RoomName.Reflecting_Pool.value]["doors"]["3"]["blastShieldType"]
            != BlastShieldType.Missile.value
        )
        self.assertTrue(
            level_key[RoomName.Antechamber.value]["doors"]["0"]["blastShieldType"]
            != BlastShieldType.Missile.value,
            "Paired mapping is not set",
        )
        self.assertTrue(
            level_key[RoomName.Antechamber.value]["doors"]["0"]["shieldType"]
            == DoorLockType.Blue.value,
            "Existing shield type override is not preserved",
        )

    def test_beam_combos_are_not_included_in_mapping_by_default(self):
        world: "MetroidPrimeWorld" = self.world
        assert world.blast_shield_mapping
        for mapping in world.blast_shield_mapping.values():
            for room in mapping.type_mapping.values():
                for door in room.values():
                    self.assertNotIn(door, beam_combo_items)


class TestBlastShieldMapping(MetroidPrimeWithOverridesTestBase):
    run_default_tests = False  # type: ignore
    options = {
        "blast_shield_randomization": BlastShieldRandomization.option_replace_existing,
        "blast_shield_available_types": "all",
    }
    overrides = {
        "blast_shield_mapping": WorldBlastShieldMapping.from_option_value(
            {
                "Tallon Overworld": {
                    "area": "Tallon Overworld",
                    "type_mapping": {
                        "Landing Site": {
                            1: "Bomb",
                            2: "Flamethrower",
                        }
                    },
                }
            }
        )
    }

    def test_blast_shield_mapping_applies_to_logic(self):
        test_region = RoomName.Canyon_Cavern.value
        world: "MetroidPrimeWorld" = self.world
        assert world.blast_shield_mapping
        self.assertEqual(
            world.blast_shield_mapping[MetroidPrimeArea.Tallon_Overworld.value],
            AreaBlastShieldMapping(MetroidPrimeArea.Tallon_Overworld.value, {"Landing Site": {1: BlastShieldType.Bomb, 2: BlastShieldType.Flamethrower}}),  # type: ignore
        )
        self.assertFalse(self.can_reach_region(test_region))
        self.collect_by_name(
            [SuitUpgrade.Morph_Ball_Bomb.value, SuitUpgrade.Morph_Ball.value]
        )
        self.assertTrue(self.can_reach_region(test_region))

    def test_beam_combos_are_included_in_logic_without_progressive_beams(self):
        test_region = RoomName.Temple_Hall.value
        missile_item = self.get_item_by_name(SuitUpgrade.Missile_Expansion.value)
        self.assertFalse(self.can_reach_region(test_region))

        self.collect_by_name([SuitUpgrade.Flamethrower.value])
        self.assertFalse(self.can_reach_region(test_region))

        self.collect_by_name(
            [
                SuitUpgrade.Plasma_Beam.value,
                SuitUpgrade.Charge_Beam.value,
            ]
        )
        self.assertFalse(self.can_reach_region(test_region))

        self.collect(missile_item)
        self.assertFalse(self.can_reach_region(test_region))

        self.collect(missile_item)
        self.assertFalse(self.can_reach_region(test_region))

        # Flamethrower Beam combo requires 11 missiles
        self.collect(missile_item)
        self.assertTrue(self.can_reach_region(test_region))


class TestBlastShieldMappingWithProgressiveBeams(MetroidPrimeWithOverridesTestBase):
    run_default_tests = False  # type: ignore
    options = {
        "blast_shield_randomization": BlastShieldRandomization.option_replace_existing,
        "blast_shield_available_types": "all",
        "missile_launcher": 1,
        "progressive_beam_upgrades": True,
    }
    overrides = {
        "blast_shield_mapping": WorldBlastShieldMapping.from_option_value(
            {
                "Tallon Overworld": {
                    "area": "Tallon Overworld",
                    "type_mapping": {
                        "Landing Site": {
                            0: "Ice Spreader",
                            1: "Ice Spreader",
                            2: "Flamethrower",
                            3: "Ice Spreader",
                            4: "Ice Spreader",
                        }
                    },
                }
            }
        )
    }

    def test_beam_combos_are_included_in_logic_with_progressive_beams(self):
        test_region = RoomName.Temple_Hall.value
        self.assertFalse(self.can_reach_region(test_region))
        progressive_item = self.get_item_by_name(
            ProgressiveUpgrade.Progressive_Plasma_Beam.value
        )
        missile_item = self.get_item_by_name(SuitUpgrade.Missile_Expansion.value)
        missile_launcher_item = self.get_item_by_name(
            SuitUpgrade.Missile_Launcher.value
        )
        self.collect(
            [
                progressive_item,
                progressive_item,
                progressive_item,
            ]
        )
        self.assertFalse(self.can_reach_region(test_region))

        self.collect(missile_launcher_item)
        self.assertFalse(self.can_reach_region(test_region))

        # Beam combos require 10 missiles
        self.collect(missile_item)
        self.assertFalse(self.can_reach_region(test_region))

        self.collect(missile_item)
        self.assertTrue(self.can_reach_region(test_region))


class TestIncludeBeamCombos(MetroidPrimeTestBase):
    options = {
        "blast_shield_randomization": BlastShieldRandomization.option_replace_existing,
        "blast_shield_available_types": "all",
        "trick_difficulty": "easy",
    }

    def test_beam_combos_are_included_within_limits(self):
        world: "MetroidPrimeWorld" = self.world
        assert world.blast_shield_mapping
        for area, mapping in world.blast_shield_mapping.items():
            beam_combo_count = 0
            for room in mapping.type_mapping.values():
                for shieldType in room.values():
                    if shieldType in beam_combo_items:
                        beam_combo_count += 1
            self.assertLessEqual(
                beam_combo_count,
                MAX_BEAM_COMBO_DOORS_PER_AREA,
                f"Too many beam combos in {area}, {beam_combo_count} found",
            )


class TestMixItUpBlastShieldRando(MetroidPrimeTestBase):
    options = {
        "blast_shield_randomization": BlastShieldRandomization.option_mix_it_up,
        "blast_shield_frequency": "low",
        "trick_difficulty": "easy",
    }

    def test_blast_shields_are_placed_in_regions_with_appropriate_quantities(self):
        world: "MetroidPrimeWorld" = self.world
        assert world.blast_shield_mapping
        for area, mapping in world.blast_shield_mapping.items():
            blast_shield_count = 0
            total_available_blast_shield_options = len(
                get_valid_blast_shield_regions_by_area(
                    self.world, MetroidPrimeArea(area)
                )
            )
            for room in mapping.type_mapping.values():
                blast_shield_count += len(room.values())
                for shieldType in room.values():
                    self.assertNotEqual(
                        shieldType,
                        BlastShieldType.Disabled,
                        "Disabled should not be included in mapping",
                    )
            self.assertGreater(
                blast_shield_count, 0, f"No blast shields found in {area}"
            )
            self.assertEqual(
                blast_shield_count,
                math.ceil(
                    total_available_blast_shield_options
                    * world.options.blast_shield_frequency
                    * 0.1
                ),
                f"Invalid number of blast shields in {area}, {blast_shield_count} found",
            )

    def test_vanilla_blast_shields_are_not_included(self):
        distribute_items_restrictive(self.multiworld)
        config = make_config(self.world)
        level_key = config["levelData"]["Chozo Ruins"]["rooms"]
        self.assertEqual(
            level_key[RoomName.Dynamo_Access.value]["doors"]["0"]["blastShieldType"],
            BlastShieldType.No_Blast_Shield.value,
        )


class TestBlastShieldRegionMapping(MetroidPrimeTestBase):
    """These mappings are manually entered, so we need to verify that they are valid"""

    run_default_tests = False  # type: ignore

    def test_each_room_is_paired_to_a_valid_room(self):
        invalid_rooms: List[Tuple[RoomName, RoomName, MetroidPrimeArea]] = []
        for area in MetroidPrimeArea:
            blast_shield_mapping = get_valid_blast_shield_regions_by_area(
                self.world, area
            )
            for region in blast_shield_mapping:
                for source_room, target_room in region.doors.items():
                    door_data = get_door_data_by_room_names(
                        source_room, target_room, area, self.world
                    )
                    if not door_data:
                        invalid_rooms.append((source_room, target_room, area))
        self.assertFalse(invalid_rooms, f"Invalid room pairings found: {invalid_rooms}")


class TestLockedDoorsNoBlastShieldOrDoorColorRando(MetroidPrimeTestBase):
    options = {"locked_door_count": 1, "trick_difficulty": "easy"}

    def test_locked_doors_are_added_to_blast_shield_mapping_when_no_other_door_rando_is_enabled(
        self,
    ):
        world: "MetroidPrimeWorld" = self.world
        total_locked_doors = 0
        assert world.blast_shield_mapping
        for area, mapping in world.blast_shield_mapping.items():
            area_locked_doors = 0
            for room in mapping.type_mapping.values():
                for door in room.values():
                    if door == BlastShieldType.Disabled:
                        total_locked_doors += 1
                        area_locked_doors += 1
            self.assertLessEqual(
                area_locked_doors, 1, f"Areas should have a max of 1 door {area}"
            )
        self.assertEqual(
            total_locked_doors,
            world.options.locked_door_count,
            "Invalid number of locked doors, received {total_locked_doors} expected {world.options.locked_door_count}",
        )


class TestLockedDoorsInBlastShieldMapping(MetroidPrimeWithOverridesTestBase):
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
                            0: "Disabled",
                        }
                    },
                }
            }
        ),
    }

    def test_locked_doors_are_added_to_blast_shield_mapping(self):
        world: "MetroidPrimeWorld" = self.world
        assert world.blast_shield_mapping
        mapped_value = world.blast_shield_mapping[
            MetroidPrimeArea.Tallon_Overworld.value
        ].type_mapping["Landing Site"][0]
        self.assertEqual(
            mapped_value, BlastShieldType.Disabled, "Locked door not added to mapping"
        )

    def test_locked_doors_are_added_to_config(self):
        world: "MetroidPrimeWorld" = self.world
        distribute_items_restrictive(self.multiworld)
        config = make_config(world)
        level_key = config["levelData"]["Tallon Overworld"]["rooms"]
        self.assertTrue(
            level_key[RoomName.Landing_Site.value]["doors"]["0"]["shieldType"]
            == BlastShieldType.Disabled.value
        )

    def test_locked_doors_are_respected_in_logic(self):
        test_region = RoomName.Gully.value
        self.assertFalse(self.can_reach_region(test_region))


class TestLockedDoorsWithDoorColorRandoAndBlastShieldRandomization(
    MetroidPrimeTestBase
):
    options = {
        "locked_door_count": 1,
        "blast_shield_frequency": "low",
        "blast_shield_randomization": BlastShieldRandomization.option_mix_it_up,
        "door_color_randomization": DoorColorRandomization.option_global,
        "trick_difficulty": "medium",
    }

    def test_locked_doors_are_not_overwritten(self):
        world: "MetroidPrimeWorld" = self.world
        total_locked_doors = 0
        assert world.blast_shield_mapping
        for _, mapping in world.blast_shield_mapping.items():
            for room in mapping.type_mapping.values():
                for door in room.values():
                    if door == BlastShieldType.Disabled:
                        total_locked_doors += 1
        self.assertEqual(
            total_locked_doors,
            world.options.locked_door_count,
            "Invalid number of locked doors, received {total_locked_doors} expected {world.options.locked_door_count}",
        )


class TestSubRegionUsesBlastShields(MetroidPrimeWithOverridesTestBase):
    run_default_tests = False  # type: ignore
    options = {
        "blast_shield_randomization": BlastShieldRandomization.option_mix_it_up,
        "blast_shield_frequency": "low",
        "blast_shield_available_types": "all",
    }
    overrides = {
        "blast_shield_mapping": WorldBlastShieldMapping.from_option_value(
            {
                "Tallon Overworld": {
                    "area": "Tallon Overworld",
                    "type_mapping": {
                        "Landing Site": {
                            3: "Bomb",
                        },
                        "Gully": {1: "Missile"},
                        "Transport Tunnel E": {1: "Missile"},
                    },
                },
                "Phendrana Drifts": {
                    "area": "Phendrana Drifts",
                    "type_mapping": {
                        "Phendrana Shorelines": {3: "Power Bomb", 5: "Missile"}
                    },
                },
            }
        )
    }

    def test_cannot_reach_alcove_sub_region_that_has_blast_shield(self):
        world: "MetroidPrimeWorld" = self.world
        test_region = RoomName.Alcove.value
        menu = world.get_region("Menu")
        menu.connect(world.get_region(RoomName.Gully.value))
        self.assertFalse(self.can_reach_region(test_region))

        self.collect_by_name(SuitUpgrade.Morph_Ball.value)
        self.collect_by_name(SuitUpgrade.Morph_Ball_Bomb.value)
        self.assertFalse(self.can_reach_region(test_region))

        self.collect_by_name(SuitUpgrade.Missile_Expansion.value)
        self.assertTrue(self.can_reach_region(test_region))

    def test_cannot_reach_ruins_entry_sub_region_that_has_blast_shield(self):
        world: "MetroidPrimeWorld" = self.world
        test_region = RoomName.Ruins_Entryway.value
        menu = world.get_region("Menu")
        menu.connect(world.get_region(RoomName.Plaza_Walkway.value))
        self.assertFalse(self.can_reach_region(test_region))

        self.collect_by_name(SuitUpgrade.Morph_Ball.value)
        self.collect_by_name(SuitUpgrade.Power_Bomb_Expansion.value)
        self.assertTrue(self.can_reach_region(test_region))

    def test_cannot_reach_plaza_walkway_sub_region_that_has_blast_shield(self):
        world: "MetroidPrimeWorld" = self.world
        test_region = RoomName.Plaza_Walkway.value
        menu = world.get_region("Menu")
        menu.connect(world.get_region(RoomName.Ruins_Entryway.value))
        self.assertFalse(self.can_reach_region(test_region))

        self.collect_by_name(SuitUpgrade.Morph_Ball.value)
        self.collect_by_name(SuitUpgrade.Power_Bomb_Expansion.value)
        self.assertTrue(self.can_reach_region(test_region))

    def test_cannot_reach_transport_tunnel_e_sub_region_that_has_blast_shield(self):
        world: "MetroidPrimeWorld" = self.world
        test_region = "Tallon Overworld: " + RoomName.Transport_Tunnel_E.value
        other_test_region = RoomName.Great_Tree_Hall.value
        menu = world.get_region("Menu")
        menu.connect(world.get_region(RoomName.Hydro_Access_Tunnel.value))

        self.collect_by_name(
            [
                SuitUpgrade.Space_Jump_Boots.value,
                SuitUpgrade.Morph_Ball.value,
                SuitUpgrade.Morph_Ball_Bomb.value,
                SuitUpgrade.Gravity_Suit.value,
                SuitUpgrade.Wave_Beam.value,
                SuitUpgrade.Thermal_Visor.value,
            ]
        )

        self.assertFalse(self.can_reach_region(test_region))

        self.collect_by_name(SuitUpgrade.Missile_Expansion.value)
        self.assertTrue(self.can_reach_region(test_region))
        self.assertFalse(
            self.can_reach_region(other_test_region),
            "boost ball should be required to access this",
        )

    def test_cannot_reach_hydro_tunnel_sub_region_that_has_blast_shield(self):
        world: "MetroidPrimeWorld" = self.world
        source_region = "Tallon Overworld: " + RoomName.Transport_Tunnel_E.value
        test_region = RoomName.Hydro_Access_Tunnel.value
        other_test_region = RoomName.Great_Tree_Hall.value
        menu = world.get_region("Menu")
        menu.connect(world.get_region(source_region))
        self.assertFalse(self.can_reach_region(test_region))

        self.collect_by_name(SuitUpgrade.Missile_Expansion.value)
        self.assertTrue(self.can_reach_region(test_region))
        self.assertFalse(
            self.can_reach_region(other_test_region),
            "boost ball should be required to access this",
        )


# Blast shields open the door when destroyed when set via randomprime. Setting them to blue ensures no one way locks


class TestBlastShieldsAndDoorColorRando(MetroidPrimeWithOverridesTestBase):
    run_default_tests = False  # type: ignore
    options = {
        "blast_shield_randomization": BlastShieldRandomization.option_mix_it_up,
        "blast_shield_frequency": "low",
        "blast_shield_available_types": "all",
        "door_color_randomization": DoorColorRandomization.option_regional,
    }

    overrides = {
        "blast_shield_mapping": WorldBlastShieldMapping.from_option_value(
            {
                "Phendrana Drifts": {
                    "area": "Phendrana Drifts",
                    "type_mapping": {
                        "Ice Ruins West": {
                            1: "Missile",
                        }
                    },
                }
            },
        ),
        "door_color_mapping": WorldDoorColorMapping.from_option_value(
            {
                "Chozo Ruins": {
                    "area": "Chozo Ruins",
                    "type_mapping": {
                        "Wave Beam": "Ice Beam",
                        "Ice Beam": "Plasma Beam",
                        "Plasma Beam": "Wave Beam",
                    },
                },
                "Magmoor Caverns": {
                    "area": "Magmoor Caverns",
                    "type_mapping": {
                        "Wave Beam": "Plasma Beam",
                        "Ice Beam": "Wave Beam",
                        "Plasma Beam": "Ice Beam",
                    },
                },
                "Phendrana Drifts": {
                    "area": "Phendrana Drifts",
                    "type_mapping": {
                        "Wave Beam": "Plasma Beam",
                        "Ice Beam": "Wave Beam",
                        "Plasma Beam": "Ice Beam",
                    },
                },
                "Tallon Overworld": {
                    "area": "Tallon Overworld",
                    "type_mapping": {
                        "Wave Beam": "Plasma Beam",
                        "Ice Beam": "Wave Beam",
                        "Plasma Beam": "Ice Beam",
                    },
                },
                "Phazon Mines": {
                    "area": "Phazon Mines",
                    "type_mapping": {
                        "Wave Beam": "Plasma Beam",
                        "Ice Beam": "Wave Beam",
                        "Plasma Beam": "Ice Beam",
                    },
                },
            }
        ),
    }

    def test_color_is_set_to_blue_when_door_has_blast_shield(self):
        world: "MetroidPrimeWorld" = self.world
        self.assertEqual(
            world.game_region_data[MetroidPrimeArea.Phendrana_Drifts]
            .rooms[RoomName.Ice_Ruins_West]
            .doors[1]
            .blast_shield,
            BlastShieldType.Missile,
        )
        self.assertEqual(
            world.game_region_data[MetroidPrimeArea.Phendrana_Drifts]
            .rooms[RoomName.Ice_Ruins_West]
            .doors[1]
            .lock,
            DoorLockType.Blue,
        )

    def test_color_is_updated_in_config(self):
        world: "MetroidPrimeWorld" = self.world
        distribute_items_restrictive(self.multiworld)
        config = make_config(world)
        level_key = config["levelData"]["Phendrana Drifts"]["rooms"]
        self.assertTrue(
            level_key[RoomName.Ice_Ruins_West.value]["doors"]["1"]["shieldType"]
            == DoorLockType.Blue.value
        )
