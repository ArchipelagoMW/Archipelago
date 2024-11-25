from ..Items import SuitUpgrade
from ..data.RoomNames import RoomName
from .. import MetroidPrimeWorld
from . import MetroidPrimeTestBase


class TestNonVariaHeatDamageFalse(MetroidPrimeTestBase):
    run_default_tests = False  # type: ignore
    options = {"non_varia_heat_damage": False}

    def test_can_access_heated_rooms_when_any_suit_is_given(self):
        world: "MetroidPrimeWorld" = self.world
        test_region = RoomName.Lava_Lake.value
        menu = world.get_region("Menu")
        menu.connect(world.get_region(RoomName.Burning_Trail.value))
        self.assertFalse(self.can_reach_region(test_region))

        self.collect_by_name(SuitUpgrade.Phazon_Suit.value)
        self.assertTrue(self.can_reach_region(test_region))


class TestNonVariaHeatDamageTrue(MetroidPrimeTestBase):
    run_default_tests = False  # type: ignore
    options = {"non_varia_heat_damage": True}

    def test_can_access_heated_rooms_only_with_varia(self):
        world: "MetroidPrimeWorld" = self.world
        test_region = RoomName.Lava_Lake.value
        menu = world.get_region("Menu")
        menu.connect(world.get_region(RoomName.Burning_Trail.value))
        self.assertFalse(self.can_reach_region(test_region))

        self.collect_by_name(SuitUpgrade.Phazon_Suit.value)
        self.assertFalse(self.can_reach_region(test_region))

        self.collect_by_name(SuitUpgrade.Varia_Suit.value)
        self.assertTrue(self.can_reach_region(test_region))
