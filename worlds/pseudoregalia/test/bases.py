from test.bases import WorldTestBase
from Fill import fast_fill

from .. import PseudoregaliaWorld


class PseudoTestBase(WorldTestBase):
    game = "Pseudoregalia"
    world: PseudoregaliaWorld


class PseudoKeyHintsBase(PseudoTestBase):
    run_default_tests = False
    expect_hints: bool = True
    major_key_names = [
        "Major Key - Empty Bailey",
        "Major Key - The Underbelly",
        "Major Key - Tower Remains",
        "Major Key - Sansa Keep",
        "Major Key - Twilight Theatre",
    ]

    def test_key_hints(self):
        major_keys = sorted(self.get_items_by_name(self.major_key_names),
                            key=lambda item: self.major_key_names.index(item.name))
        locations = self.multiworld.get_unfilled_locations(self.player)[:5]
        fast_fill(self.multiworld, major_keys, locations)
        slot_data = self.world.fill_slot_data()
        if self.expect_hints:
            assert "key_hints" in slot_data, "Expected key_hints in slot_data"
            expected_key_hints = [
                [{
                    "player": self.player,
                    "location": location.address,
                }]
                for location in locations
            ]
            assert slot_data["key_hints"] == expected_key_hints, \
                   f"Expected {expected_key_hints} but found {slot_data["key_hints"]}"
        else:
            assert "key_hints" not in slot_data, "Expected no key_hints in slot_data"
