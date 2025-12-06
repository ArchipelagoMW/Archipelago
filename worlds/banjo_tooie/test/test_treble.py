from ..Options import RandomizeTrebleClefs
from .test_logic import EasyTricksLogic, GlitchesLogic, HardTricksLogic, IntendedLogic
from . import BanjoTooieTestBase
from ..Names import itemName
from .. import all_group_table


class TreblesEnabled(BanjoTooieTestBase):
    options = {
        "randomize_treble": RandomizeTrebleClefs.option_true
    }

    def test_item_pool(self) -> None:
        treble_amt = 0
        treble_count = 0
        for name, btitem in all_group_table["misc"].items():
            if name == itemName.TREBLE:
                treble_amt = btitem.qty
                break

        for item in self.world.multiworld.itempool:
            if itemName.TREBLE == item.name:
                treble_count += 1
        assert treble_amt == treble_count


class TreblesDisabled(BanjoTooieTestBase):
    options = {
        "randomize_treble": RandomizeTrebleClefs.option_false
    }

    def test_disabled_item_pool(self) -> None:
        adv_count = 0
        for item in self.world.multiworld.itempool:
            if itemName.TREBLE == item.name:
                print(f"Item: {item.name} Should not be here!")
                adv_count += 1
        assert 0 == adv_count

    def test_prefills(self) -> None:
        treble_amt = 0
        treble_count = 0
        for name, btitem in all_group_table["misc"].items():
            if name == itemName.TREBLE:
                treble_amt = btitem.qty
                break

        for name in self.world.location_name_to_id:
            if name.find(itemName.TREBLE) != -1:
                try:
                    location_item = self.multiworld.get_location(name, self.player).item.name
                    if location_item == itemName.TREBLE:
                        treble_count += 1
                except Exception:
                    print(f"Issue with Item: {name} Please Investigate")
                    treble_count += 0
        assert treble_amt == treble_count


class TestTreblesEnabledIntended(TreblesEnabled, IntendedLogic):
    options = {
        **TreblesEnabled.options,
        **IntendedLogic.options,
    }


class TestTreblesEnabledEasyTricks(TreblesEnabled, EasyTricksLogic):
    options = {
        **TreblesEnabled.options,
        **EasyTricksLogic.options,
    }


class TestTreblesEnabledHardTricks(TreblesEnabled, HardTricksLogic):
    options = {
        **TreblesEnabled.options,
        **HardTricksLogic.options,
    }


class TestTreblesEnabledGlitchesTricks(TreblesEnabled, GlitchesLogic):
    options = {
        **TreblesEnabled.options,
        **GlitchesLogic.options,
    }


class TestTreblesDisabledIntended(TreblesDisabled, IntendedLogic):
    options = {
        **TreblesDisabled.options,
        **IntendedLogic.options,
    }


class TestTreblesDisabledEasyTricks(TreblesDisabled, EasyTricksLogic):
    options = {
        **TreblesDisabled.options,
        **EasyTricksLogic.options,
    }


class TestTreblesDisabledHardTricks(TreblesDisabled, HardTricksLogic):
    options = {
        **TreblesDisabled.options,
        **HardTricksLogic.options,
    }


class TestTreblesDisabledGlitchesTricks(TreblesDisabled, GlitchesLogic):
    options = {
        **TreblesDisabled.options,
        **GlitchesLogic.options,
    }
