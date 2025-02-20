from ..Enum import StartRoomDifficulty
from ..data.AreaNames import MetroidPrimeArea
from ..data.RoomNames import RoomName
from ..data.StartRoomData import StartRoomData
from ..data.Transports import get_random_elevator_mapping
from . import MetroidPrimeTestBase

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .. import MetroidPrimeWorld


class TestNonRandomStartingRoomWithElevatorRando(MetroidPrimeTestBase):
    run_default_tests = False  # type: ignore
    options = {"elevator_randomization": True, "starting_room": "normal"}

    def test_start_room_gets_set_to_save_1_when_normal_start(self):
        # When start room is normal then it should be set to save_station_1 since landing site isn't viable for most seeds
        self.world.generate_early()
        world: "MetroidPrimeWorld" = self.world
        assert world.starting_room_data.name == RoomName.Save_Station_1.value


class TestRandomStartingRoomWithElevatorRando(MetroidPrimeTestBase):
    run_default_tests = False  # type: ignore
    options = {"elevator_randomization": True, "starting_room": "safe"}

    def test_start_room_is_not_landing_site_with_safe_start(self):
        # When start room is normal then it should be set to save_station_1 since landing site isn't viable for most seeds
        self.world.generate_early()
        world: "MetroidPrimeWorld" = self.world
        assert world.starting_room_data.name != RoomName.Landing_Site.value


class AllowListElevatorRando(MetroidPrimeTestBase):
    run_default_tests = False  # type: ignore
    options = {
        "elevator_randomization": True,
        "starting_room_name": "Save Station B",
    }

    def test_start_rooms_with_allow_list_correctly_chooses_elevators(self):
        fake_start = StartRoomData(
            difficulty=StartRoomDifficulty.Safe,
            area=MetroidPrimeArea.Tallon_Overworld,
            allowed_elevators={
                MetroidPrimeArea.Tallon_Overworld.value: {
                    RoomName.Transport_to_Chozo_Ruins_West.value: [
                        RoomName.Transport_to_Magmoor_Caverns_North.value
                    ],
                    RoomName.Transport_to_Magmoor_Caverns_East.value: [
                        RoomName.Transport_to_Phendrana_Drifts_South.value
                    ],
                }
            },
        )
        self.world.starting_room_data = fake_start
        mapping = get_random_elevator_mapping(self.world)
        assert (
            mapping[MetroidPrimeArea.Tallon_Overworld.value][
                RoomName.Transport_to_Chozo_Ruins_West.value
            ]
            == RoomName.Transport_to_Magmoor_Caverns_North.value
        )
        assert (
            mapping[MetroidPrimeArea.Tallon_Overworld.value][
                RoomName.Transport_to_Magmoor_Caverns_East.value
            ]
            == RoomName.Transport_to_Phendrana_Drifts_South.value
        )
