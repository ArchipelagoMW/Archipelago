from .. import TWWWorld
from ..Macros import can_defeat_ganondorf, has_heros_sword
from ..Enums import ItemName
from .Bases import WindWakerTestBase

class TestBattleGanondorfStartWithSword(WindWakerTestBase):
    options = {"sword_mode": 0}
    world: TWWWorld

    def test_battle_ganondorf_sword_not_enough(self) -> None:
        self.assertFalse(can_defeat_ganondorf(self.multiworld.state, self.player))

    def test_battle_ganondorf_sword_shield_victory(self) -> None:
        self.collect_by_name(ItemName.PROGRESSIVE_SHIELD)
        self.assertTrue(can_defeat_ganondorf(self.multiworld.state, self.player))

class TestBattleGanondorfNoStartingSword(WindWakerTestBase):
    options = {"sword_mode": 1}
    world: TWWWorld

    def test_battle_ganondorf_sword_not_enough(self) -> None:
        self.collect_by_name(ItemName.PROGRESSIVE_SWORD)
        self.assertFalse(can_defeat_ganondorf(self.multiworld.state, self.player))

    def test_battle_ganondorf_shield_not_enough(self) -> None:
        self.collect_by_name(ItemName.PROGRESSIVE_SHIELD)
        self.assertFalse(has_heros_sword(self.multiworld.state, self.player))
        self.assertFalse(can_defeat_ganondorf(self.multiworld.state, self.player))

    def test_battle_ganondorf_sword_shield_victory(self) -> None:
        self.collect_by_name(ItemName.PROGRESSIVE_SWORD)
        self.collect_by_name(ItemName.PROGRESSIVE_SHIELD)
        self.assertTrue(can_defeat_ganondorf(self.multiworld.state, self.player))

class TestBattleGanondorfSwordlessMode(WindWakerTestBase):
    options = {"sword_mode": 3}
    world: TWWWorld

    def test_battle_ganondorf_wits_not_enough(self) -> None:
        self.assertFalse(can_defeat_ganondorf(self.multiworld.state, self.player))

    def test_battle_ganondorf_shield_victory(self) -> None:
        self.collect_by_name(ItemName.PROGRESSIVE_SHIELD)
        self.assertTrue(can_defeat_ganondorf(self.multiworld.state, self.player))

    def test_battle_ganondorf_hammer_not_enough_usually(self) -> None:
        self.collect_by_name(ItemName.SKULL_HAMMER)
        self.assertFalse(can_defeat_ganondorf(self.multiworld.state, self.player))

    def test_battle_ganondorf_hammer_obscure_tech(self) -> None:
        self.collect_by_name(ItemName.SKULL_HAMMER)
        self.enable_glitched_item()
        self.assertTrue(can_defeat_ganondorf(self.multiworld.state, self.player))
