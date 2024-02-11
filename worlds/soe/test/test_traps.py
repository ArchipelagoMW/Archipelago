import typing
from dataclasses import fields

from . import SoETestBase
from ..options import SoEOptions

if typing.TYPE_CHECKING:
    from .. import SoEWorld


class Bases:
    # class in class to avoid running tests for TrapTest class
    class TrapTestBase(SoETestBase):
        """Test base for trap tests"""
        option_name_to_item_name = {
            # filtering by name here validates that there is no confusion between name and type
            field.name: field.type.item_name for field in fields(SoEOptions) if field.name.startswith("trap_chance_")
        }

        def test_dataclass(self) -> None:
            """Test that the dataclass helper property returns the expected sequence"""
            self.assertGreater(len(self.option_name_to_item_name), 0, "Expected more than 0 trap types")
            world: "SoEWorld" = typing.cast("SoEWorld", self.multiworld.worlds[1])
            item_name_to_rolled_option = {option.item_name: option for option in world.options.trap_chances}
            # compare that all fields are present - that is property in dataclass and selector code in test line up
            self.assertEqual(sorted(self.option_name_to_item_name.values()), sorted(item_name_to_rolled_option),
                             "field names probably do not match field types")
            # sanity check that chances are correctly set and returned by property
            for option_name, item_name in self.option_name_to_item_name.items():
                self.assertEqual(item_name_to_rolled_option[item_name].value,
                                 self.options.get(option_name, item_name_to_rolled_option[item_name].default))

        def test_trap_count(self) -> None:
            """Test that total trap count is correct"""
            self.assertEqual(self.options["trap_count"],
                             len(self.get_items_by_name(self.option_name_to_item_name.values())))


class TestTrapAllZeroChance(Bases.TrapTestBase):
    """Tests all zero chances still gives traps if trap_count is set."""
    options: typing.Dict[str, typing.Any] = {
        "trap_count": 1,
        **{name: 0 for name in Bases.TrapTestBase.option_name_to_item_name}
    }


class TestTrapNoConfound(Bases.TrapTestBase):
    """Tests that one zero chance does not give that trap."""
    options: typing.Dict[str, typing.Any] = {
        "trap_count": 99,
        "trap_chance_confound": 0,
    }

    def test_no_confound_trap(self) -> None:
        self.assertEqual(self.option_name_to_item_name["trap_chance_confound"], "Confound Trap")
        self.assertEqual(len(self.get_items_by_name("Confound Trap")), 0)
