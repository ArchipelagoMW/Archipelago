from ..Names import itemName
from ..Options import RandomizeBigTentTickets
from .test_logic import EasyTricksLogic, GlitchesLogic, HardTricksLogic, IntendedLogic
from . import BanjoTooieTestBase


class TestRandomizedTickets(BanjoTooieTestBase):
    options = {
        "randomize_tickets": RandomizeBigTentTickets.option_true,
    }

    def test_item_pool(self) -> None:
        item_pool_names = [item.name for item in self.multiworld.itempool]
        assert item_pool_names.count(itemName.BTTICKET) == 4


class TestVanillaTickets(BanjoTooieTestBase):
    options = {
        "randomize_tickets": RandomizeBigTentTickets.option_false,
    }

    def test_item_pool(self) -> None:
        item_pool_names = [item.name for item in self.multiworld.itempool]
        assert item_pool_names.count(itemName.BTTICKET) == 0


class TestRandomizedTicketsIntended(TestRandomizedTickets, IntendedLogic):
    options = {
        **TestRandomizedTickets.options,
        **IntendedLogic.options,
    }


class TestRandomizedTicketsEasyTricks(TestRandomizedTickets, EasyTricksLogic):
    options = {
        **TestRandomizedTickets.options,
        **EasyTricksLogic.options,
    }


class TestRandomizedTicketsHardTricks(TestRandomizedTickets, HardTricksLogic):
    options = {
        **TestRandomizedTickets.options,
        **HardTricksLogic.options,
    }


class TestRandomizedTicketsGlitches(TestRandomizedTickets, GlitchesLogic):
    options = {
        **TestRandomizedTickets.options,
        **GlitchesLogic.options,
    }


class TestVanillaTicketsIntended(TestVanillaTickets, IntendedLogic):
    options = {
        **TestVanillaTickets.options,
        **IntendedLogic.options,
    }


class TestVanillaTicketsEasyTricks(TestVanillaTickets, EasyTricksLogic):
    options = {
        **TestVanillaTickets.options,
        **EasyTricksLogic.options,
    }


class TestVanillaTicketsHardTricks(TestVanillaTickets, HardTricksLogic):
    options = {
        **TestVanillaTickets.options,
        **HardTricksLogic.options,
    }


class TestVanillaTicketsGlitches(TestVanillaTickets, GlitchesLogic):
    options = {
        **TestVanillaTickets.options,
        **GlitchesLogic.options,
    }
