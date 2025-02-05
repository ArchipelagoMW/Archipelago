from ..Items import SuitUpgrade, artifact_table
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


class TestRequiredArtifactCount(MetroidPrimeTestBase):
    run_default_tests = False  # type: ignore
    options = {"required_artifacts": 3}

    def test_required_artifact_count(self):
        self.assertFalse(self.can_reach_region("Impact Crater"))
        self.collect_all_but(artifact_table.keys())
        self.assertFalse(self.can_reach_region("Impact Crater"))
        self.collect_by_name("Artifact of Truth")
        self.assertFalse(self.can_reach_region("Impact Crater"))
        self.collect_by_name("Artifact of Warrior")
        self.assertFalse(self.can_reach_region("Impact Crater"))
        self.collect_by_name("Artifact of Chozo")
        self.assertTrue(self.can_reach_region("Impact Crater"))


class TestMainPowerBomb(MetroidPrimeTestBase):
    options = {"main_power_bomb": 1}

    def test_main_power_bomb_required(self):
        self.collect_all_but([SuitUpgrade.Main_Power_Bomb.value])
        self.assertFalse(self.can_reach_location("Chozo Ruins: Magma Pool"))
        self.collect_by_name(SuitUpgrade.Main_Power_Bomb.value)
        self.assertTrue(self.can_reach_location("Chozo Ruins: Magma Pool"))


class TestNoMainPowerBomb(MetroidPrimeTestBase):
    options = {"main_power_bomb": 0}

    def test_main_power_bomb_not_required(self):
        self.assertFalse(self.can_reach_location("Chozo Ruins: Magma Pool"))
        self.collect_all_but([SuitUpgrade.Main_Power_Bomb.value])
        self.assertTrue(self.can_reach_location("Chozo Ruins: Magma Pool"))
