from typing import List
from Fill import distribute_items_restrictive
from ..Enum import StartRoomDifficulty
from ..PrimeOptions import BlastShieldRandomization
from ..Items import SuitUpgrade
from ..data.RoomNames import RoomName
from ..data.StartRoomData import all_start_rooms
from . import MetroidPrimeTestBase, MetroidPrimeWithOverridesTestBase
from .. import MetroidPrimeWorld


class TestStartingRoomsGenerate(MetroidPrimeWithOverridesTestBase):
    auto_construct = False

    def test_starting_room_rando_bulk(self):
        for room_name in all_start_rooms:
            with self.subTest(f"Starting Room: {room_name}", room_name=room_name):
                self.options = {
                    "elevator_randomization": False,
                    "missile_launcher": 1,
                }
                self.overrides = {
                    "starting_room_name": room_name,
                }
                try:
                    self.world_setup()  # type: ignore
                    distribute_items_restrictive(self.multiworld)
                    self.assertBeatable(True)
                except Exception:
                    self.fail(
                        f"Failed to generate beatable game with start room: {room_name}. "
                    )


class TestStartingRoomsGenerateWithElevatorRando(MetroidPrimeWithOverridesTestBase):
    auto_construct = False

    def test_starting_room_rando_with_elevator_rando(self):
        failures: List[str] = []
        for room_name in all_start_rooms:
            # Landing site is not viable for elevator randomization w/o tricks
            if room_name == RoomName.Landing_Site.value:
                continue
            with self.subTest(f"Starting Room: {room_name}", room_name=room_name):
                self.options = {
                    "elevator_randomization": True,
                    "missile_launcher": 1,
                }
                self.overrides = {
                    "starting_room_name": room_name,
                }
                try:
                    self.world_setup()  # type: ignore
                    distribute_items_restrictive(self.multiworld)
                    self.assertBeatable(True)
                except Exception:
                    failures.append(room_name)
        if len(failures):
            self.fail(
                "Failed to generate beatable game with start rooms: "
                + ", ".join(failures)
            )


class TestStartRoomBKPreventionDisabled(MetroidPrimeWithOverridesTestBase):
    run_default_tests = False  # type: ignore
    options = {
        "starting_room_name": RoomName.Save_Station_B.value,
        "elevator_randomization": False,
        "disable_starting_room_bk_prevention": True,
    }
    overrides = {"starting_room_name": RoomName.Save_Station_B.value}

    def test_disabling_bk_prevention_does_not_give_items_or_pre_fill(self):
        self.world.generate_early()
        world: MetroidPrimeWorld = self.world
        assert world.starting_room_data.selected_loadout
        self.assertTrue(
            SuitUpgrade.Missile_Expansion
            not in world.starting_room_data.selected_loadout.loadout
        )
        self.assertEqual(len(world.prefilled_item_map.keys()), 0)
        self.assertEqual(
            world.starting_room_data.selected_loadout.starting_beam,
            SuitUpgrade.Plasma_Beam,
        )


class TestPrePlacedItemsWithStartFromPool(MetroidPrimeWithOverridesTestBase):
    options = {"start_inventory_from_pool": {SuitUpgrade.Morph_Ball.value: 1}}
    overrides = {"starting_room_name": RoomName.Save_Station_1.value}

    def test_bk_prevention_should_not_add_items_when_in_start_inventory(
        self,
    ):
        self.assertNotIn(
            SuitUpgrade.Morph_Ball.value,
            self.world.prefilled_item_map.values(),
        )


class TestPreCollectedItemsWithStartInventoryFromPool(
    MetroidPrimeWithOverridesTestBase
):
    run_default_tests = False  # type: ignore
    options = {"start_inventory": {SuitUpgrade.Missile_Expansion.value: 1}}
    overrides = {"starting_room_name": RoomName.Arboretum.value}

    def test_should_not_double_collect_items_when_using_start_items(
        self,
    ):
        count = len(
            [
                item
                for item in self.multiworld.precollected_items[self.player]
                if item.name == SuitUpgrade.Missile_Expansion.value
            ]
        )
        self.assertEqual(count, 1, "Should only be one missile in precolelcted items")


class TestPreCollectedItemsWithStartInventory(MetroidPrimeWithOverridesTestBase):
    run_default_tests = False  # type: ignore
    options = {"start_inventory": {SuitUpgrade.Missile_Expansion.value: 1}}
    overrides = {"starting_room_name": RoomName.Arboretum.value}

    def test_should_not_double_collect_items_when_using_start_items(
        self,
    ):
        count = len(
            [
                item
                for item in self.multiworld.precollected_items[self.player]
                if item.name == SuitUpgrade.Missile_Expansion.value
            ]
        )
        self.assertEqual(count, 1, "Should only be one missile in precolelcted items")


class TestStartRoomBKPreventionEnabled(MetroidPrimeWithOverridesTestBase):
    run_default_tests = False  # type: ignore
    options = {
        "elevator_randomization": False,
        "disable_starting_room_bk_prevention": False,
    }
    overrides = {"starting_room_name": RoomName.Save_Station_B.value}

    def test_enabling_bk_prevention_gives_items_and_pre_fills_locations(self):
        self.world.generate_early()
        world: MetroidPrimeWorld = self.world
        assert world.starting_room_data.selected_loadout
        self.assertIn(
            SuitUpgrade.Missile_Expansion,
            world.starting_room_data.selected_loadout.loadout,
        )
        self.assertEqual(len(world.prefilled_item_map.keys()), 1)
        self.assertEqual(
            world.starting_room_data.selected_loadout.starting_beam,
            SuitUpgrade.Plasma_Beam,
        )


class TestBuckleUpStartingRoom(MetroidPrimeTestBase):
    run_default_tests = False  # type: ignore
    options = {"starting_room": StartRoomDifficulty.Buckle_Up.value}

    def test_buckle_up(self):
        available_room_names = [
            name
            for name, room in all_start_rooms.items()
            if room.difficulty.value == StartRoomDifficulty.Buckle_Up.value
        ]
        self.assertTrue(self.world.starting_room_name in available_room_names)


class TestNormalStartingRoom(MetroidPrimeTestBase):
    run_default_tests = False  # type: ignore
    options = {"starting_room": StartRoomDifficulty.Normal.value}

    def test_normal(self):
        self.assertTrue(self.world.starting_room_name == RoomName.Landing_Site.value)


class TestNormalStartingRoomWithBlastShieldRandoMixItUp(MetroidPrimeTestBase):
    run_default_tests = False  # type: ignore
    options = {
        "starting_room": StartRoomDifficulty.Normal.value,
        "blast_shield_randomization": BlastShieldRandomization.option_mix_it_up,
        "elevator_randomization": True,
    }

    def test_starting_room_is_not_landing_site_when_elevator_rando_is_enabled_and_mix_it_up(
        self,
    ):
        self.assertTrue(self.world.starting_room_name != RoomName.Landing_Site.value)


class TestStartRoomArboretum(MetroidPrimeWithOverridesTestBase):
    run_default_tests = False  # type: ignore
    options = {
        "elevator_randomization": True,
    }
    overrides = {
        "starting_room_name": RoomName.Arboretum.value,
    }

    def test_starting_in_arboretum(self):
        self.world.generate_early()
        distribute_items_restrictive(self.multiworld)
        self.assertBeatable(True)
        self.assertTrue(
            self.can_reach_location("Chozo Ruins: Watery Hall - Scan Puzzle")
        )


class TestPrefilledItemsNotPlaced(MetroidPrimeWithOverridesTestBase):
    run_default_tests = False  # type: ignore
    options = {"start_inventory_from_pool": {SuitUpgrade.Morph_Ball.value: 1}}
    overrides = {"starting_room_name": RoomName.Save_Station_1.value}

    def test_prefilled_items_should_not_be_placed_when_in_start_inventory(
        self,
    ):
        self.assertNotIn(
            SuitUpgrade.Morph_Ball.value,
            self.world.prefilled_item_map.values(),
        )
        self.assertIn(
            SuitUpgrade.Missile_Expansion.value,
            self.world.prefilled_item_map.values(),
        )
