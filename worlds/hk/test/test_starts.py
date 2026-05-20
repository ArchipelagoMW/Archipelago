from typing import ClassVar

from .bases import NoStepHK


class StartsBase:
    valid_starts: ClassVar[list[str]]
    invalid_starts: ClassVar[list[str]]

    def test_valid_starts(self):
        for start in self.valid_starts:
            with self.subTest(start=start):
                self.assertFalse(self.world.validate_start(start))

    def test_invalid_starts(self):
        for start in self.invalid_starts:
            with self.subTest(start=start):
                self.assertTrue(self.world.validate_start(start))


class TestSwimRandoStarts(StartsBase, NoStepHK):
    options: ClassVar[dict[str, str]] = {
        "RandomizeSwim": "true",

        "EnemyPogos": "true",
    }
    valid_starts: ClassVar[list[str]] = []
    invalid_starts: ClassVar[list[str]] = ["kingdoms_edge"]


class TestSwimRandolessStarts(StartsBase, NoStepHK):
    options: ClassVar[dict[str, str]] = {
        "RandomizeSwim": "false",

        "EnemyPogos": "true",
    }
    valid_starts: ClassVar[list[str]] = ["kingdoms_edge"]
    invalid_starts: ClassVar[list[str]] = []


class TestEnemyPogoStarts(StartsBase, NoStepHK):
    options: ClassVar[dict[str, str]] = {
        "EnemyPogos": "true",

        "PreciseMovement": "false",
        "RandomizeSwim": "false",
        "DangerousSkips": "true",
        "ShadeSkips": "true",
    }
    valid_starts: ClassVar[list[str]] = ["mantis_village", "kingdoms_edge", "queens_gardens"]
    invalid_starts: ClassVar[list[str]] = ["west_waterways"]


class TestPreciseEnemyPogoStarts(StartsBase, NoStepHK):
    options: ClassVar[dict[str, str]] = {
        "EnemyPogos": "true",
        "PreciseMovement": "true",

        "RandomizeSwim": "false",
        "DangerousSkips": "true",
        "ShadeSkips": "true",
    }
    valid_starts: ClassVar[list[str]] = ["mantis_village", "kingdoms_edge", "west_waterways", "queens_gardens"]
    invalid_starts: ClassVar[list[str]] = []


class TestEnemyPogolessStarts(StartsBase, NoStepHK):
    options: ClassVar[dict[str, str]] = {
        "EnemyPogos": "false",

        "RandomizeSwim": "false",
        "DangerousSkips": "true",
        "ShadeSkips": "true",
    }
    valid_starts: ClassVar[list[str]] = []
    invalid_starts: ClassVar[list[str]] = ["mantis_village", "kingdoms_edge", "west_waterways", "queens_gardens"]


class TestDarkroomOnStarts(StartsBase, NoStepHK):
    options: ClassVar[dict[str, str]] = {
        "DarkRooms": "true",
    }
    valid_starts: ClassVar[list[str]] = ["hallownests_crown"]
    invalid_starts: ClassVar[list[str]] = []


class TestDarkroomOffStarts(StartsBase, NoStepHK):
    options: ClassVar[dict[str, str]] = {
        "DarkRooms": "false",
    }
    valid_starts: ClassVar[list[str]] = []
    invalid_starts: ClassVar[list[str]] = ["hallownests_crown"]
