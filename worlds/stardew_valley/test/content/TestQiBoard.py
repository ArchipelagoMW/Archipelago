from . import SVContentPackTestBase
from ...content import content_packs
from ...strings.fish_names import Fish


class TestQiBoard(SVContentPackTestBase):
    vanilla_packs = SVContentPackTestBase.vanilla_packs + (content_packs.ginger_island_content_pack, content_packs.qi_board_content_pack)

    def test_extended_family_fishes_are_included(self):
        fish_names = self.content.fishes.keys()

        self.assertIn(Fish.ms_angler, fish_names)
        self.assertIn(Fish.son_of_crimsonfish, fish_names)
        self.assertIn(Fish.glacierfish_jr, fish_names)
        self.assertIn(Fish.legend_ii, fish_names)
        self.assertIn(Fish.radioactive_carp, fish_names)

        # 63 from pelican town + 3 ginger island exclusive + 5 extended family
        self.assertEqual(63 + 3 + 5, len(self.content.fishes))
