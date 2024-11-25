from ..data.StartRoomData import StartRoomDifficulty
from ..Items import SuitUpgrade
from ..data.RoomNames import RoomName
from typing import Any, TYPE_CHECKING, Dict
from . import MetroidPrimeTestBase

if TYPE_CHECKING:
    from .. import MetroidPrimeWorld
options: Dict[str, Any] = {
    "door_color_randomization": "regional",
    "starting_room": StartRoomDifficulty.Safe.value,
    "include_power_beam_doors": True,
    "include_bomb_doors": True,
    "starting_room_name": RoomName.Save_Station_B.value,
    "starting_beam": SuitUpgrade.Plasma_Beam.value,
    "door_color_mapping": {
        "Phendrana Drifts": {
            "area": "Phendrana Drifts",
            "type_mapping": {
                "Wave Beam": "Power Beam Only",
                "Ice Beam": "Wave Beam",
                "Plasma Beam": "Ice Beam",
            },
        },
        "Chozo Ruins": {
            "area": "Chozo Ruins",
            "type_mapping": {
                "Wave Beam": "Power Beam Only",
                "Ice Beam": "Wave Beam",
                "Plasma Beam": "Ice Beam",
            },
        },
        "Magmoor Caverns": {
            "area": "Magmoor Caverns",
            "type_mapping": {
                "Wave Beam": "Power Beam Only",
                "Ice Beam": "Wave Beam",
                "Plasma Beam": "Ice Beam",
            },
        },
        "Tallon Overworld": {
            "area": "Tallon Overworld",
            "type_mapping": {
                "Wave Beam": "Power Beam Only",
                "Ice Beam": "Wave Beam",
                "Plasma Beam": "Ice Beam",
            },
        },
        "Phazon Mines": {
            "area": "Phazon Mines",
            "type_mapping": {
                "Wave Beam": "Power Beam Only",
                "Ice Beam": "Wave Beam",
                "Plasma Beam": "Ice Beam",
            },
        },
        "Impact Crater": {
            "area": "Impact Crater",
            "type_mapping": {
                "Wave Beam": "Power Beam Only",
                "Ice Beam": "Wave Beam",
                "Plasma Beam": "Ice Beam",
            },
        },
    },
    "elevator_randomization": "true",
    "elevator_mapping": {
        "Tallon Overworld": {
            "Transport to Magmoor Caverns East": "Phazon Mines: Transport to Magmoor Caverns South",
            "Transport to Chozo Ruins East": "Transport to Tallon Overworld West",
            "Transport to Chozo Ruins West": "Chozo Ruins: Transport to Tallon Overworld South",
            "Transport to Chozo Ruins South": "Transport to Chozo Ruins North",
            "Transport to Phazon Mines East": "Phendrana Drifts: Transport to Magmoor Caverns South",
        },
        "Chozo Ruins": {
            "Transport to Tallon Overworld East": "Transport to Magmoor Caverns West",
            "Chozo Ruins: Transport to Tallon Overworld South": "Transport to Chozo Ruins West",
            "Transport to Magmoor Caverns North": "Transport to Phendrana Drifts North",
            "Transport to Tallon Overworld North": "Transport to Phendrana Drifts South",
        },
        "Magmoor Caverns": {
            "Transport to Tallon Overworld West": "Transport to Chozo Ruins East",
            "Transport to Phazon Mines West": "Phazon Mines: Transport to Tallon Overworld South",
            "Transport to Phendrana Drifts North": "Transport to Magmoor Caverns North",
            "Transport to Chozo Ruins North": "Transport to Chozo Ruins South",
            "Transport to Phendrana Drifts South": "Transport to Tallon Overworld North",
        },
        "Phendrana Drifts": {
            "Transport to Magmoor Caverns West": "Transport to Tallon Overworld East",
            "Phendrana Drifts: Transport to Magmoor Caverns South": "Transport to Phazon Mines East",
        },
        "Phazon Mines": {
            "Phazon Mines: Transport to Magmoor Caverns South": "Transport to Magmoor Caverns East",
            "Phazon Mines: Transport to Tallon Overworld South": "Transport to Phazon Mines West",
        },
    },
}


class TestUniversalTracker(MetroidPrimeTestBase):
    auto_construct = False
    run_default_tests = False  # type: ignore
    options = options

    def test_door_randomization_is_preserved(self):
        self.world_setup()  # type: ignore
        world: "MetroidPrimeWorld" = self.world
        self.world.generate_early()
        assert world.door_color_mapping
        for area in world.door_color_mapping.keys():
            self.assertEqual(
                world.door_color_mapping[area].type_mapping,
                self.options["door_color_mapping"][area]["type_mapping"],
            )

    def test_starting_room_info_is_preserved(self):
        self.world_setup()  # type: ignore
        world: "MetroidPrimeWorld" = self.world
        assert world.starting_room_data.selected_loadout
        self.world.generate_early()
        self.assertEqual(
            world.starting_room_data.name, self.options["starting_room_name"]
        )
        self.assertEqual(
            SuitUpgrade(self.options["starting_beam"]),
            world.starting_room_data.selected_loadout.starting_beam,
        )

    def test_starting_room_info_is_preserved_with_progressive_beams(self):
        self.options["progressive_beam_upgrades"] = 1
        self.world_setup()  # type: ignore
        world: "MetroidPrimeWorld" = self.world
        assert world.starting_room_data.selected_loadout
        self.world.generate_early()
        self.assertEqual(
            world.starting_room_data.name, self.options["starting_room_name"]
        )
        self.assertEqual(
            SuitUpgrade(self.options["starting_beam"]),
            world.starting_room_data.selected_loadout.starting_beam,
        )

    def test_elevator_mapping_is_preserved(self):
        self.world_setup()  # type: ignore
        world: "MetroidPrimeWorld" = self.world
        self.world.generate_early()
        self.assertEqual(world.elevator_mapping, self.options["elevator_mapping"])
