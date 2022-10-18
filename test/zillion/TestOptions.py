from test.zillion import ZillionTestBase

from worlds.zillion.options import ZillionJumpLevels, ZillionGunLevels, validate
from zilliandomizer.options import VBLR_CHOICES


class OptionsTest(ZillionTestBase):

    def test_vblr_values(self) -> None:
        for vblr_class in (ZillionJumpLevels, ZillionGunLevels):
            for name in vblr_class.name_lookup.values():
                assert name.lower() in VBLR_CHOICES

    def test_validate_default(self) -> None:
        _zz_options, _item_counts = validate(self.world, 1)

    # TODO: test validate with invalid combinations of options
