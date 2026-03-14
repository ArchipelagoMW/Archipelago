from . import ZillionTestBase

from .. import ZillionWorld
from ..options import ZillionJumpLevels, ZillionGunLevels, ZillionOptions, ZillionPriorityDeadEnds, validate
from zilliandomizer.options import VBLR_CHOICES


class OptionsTest(ZillionTestBase):
    auto_construct = False

    def test_validate_default(self) -> None:
        self.world_setup()
        options = self.multiworld.worlds[1].options
        assert isinstance(options, ZillionOptions)
        validate(options)

    def test_vblr_ap_to_zz(self) -> None:
        """ all of the valid values for the AP options map to valid values for ZZ options """
        for option_name, vblr_class in (
            ("jump_levels", ZillionJumpLevels),
            ("gun_levels", ZillionGunLevels),
        ):
            for value in vblr_class.name_lookup.values():
                self.options = {option_name: value}
                self.world_setup()
                options = self.multiworld.worlds[1].options
                assert isinstance(options, ZillionOptions)
                zz_options, _item_counts = validate(options)
                assert getattr(zz_options, option_name) in VBLR_CHOICES

    # TODO: test validate with invalid combinations of options


class DeadEndsTest(ZillionTestBase):
    def test_vanilla_dead_end_names(self) -> None:
        z_world = self.multiworld.worlds[1]
        assert isinstance(z_world, ZillionWorld)
        for loc_name in ZillionPriorityDeadEnds.vanilla_dead_ends:
            assert any(loc.name == loc_name for loc in z_world.my_locations), f"{loc_name=} {z_world.my_locations=}"

    def test_always_dead_end_names(self) -> None:
        z_world = self.multiworld.worlds[1]
        assert isinstance(z_world, ZillionWorld)
        for loc_name in ZillionPriorityDeadEnds.always_dead_ends:
            assert any(loc.name == loc_name for loc in z_world.my_locations), f"{loc_name=} {z_world.my_locations=}"
