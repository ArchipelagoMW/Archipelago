from . import BombRushCyberfunkTestBase
from ..Rules import build_access_cache, spots_s_glitchless, spots_s_glitched, spots_m_glitchless, spots_m_glitched, \
    spots_l_glitchless, spots_l_glitched, spots_xl_glitched, spots_xl_glitchless


class TestSpotsGlitchless(BombRushCyberfunkTestBase):
    @property
    def run_default_tests(self) -> bool:
        return False

    def test_spots_glitchless(self) -> None:
        player = self.player

        self.collect_by_name([
            "Graffiti (M - OVERWHELMME)",
            "Graffiti (L - WHOLE SIXER)",
            "Graffiti (XL - Gold Rush)"
        ])
        access_cache = build_access_cache(self.multiworld.state, player, 2, False, False)

        # chapter 1 - hideout
        self.assertEqual(10, spots_s_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(4, spots_m_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(7, spots_l_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(3, spots_xl_glitchless(self.multiworld.state, player, False, access_cache))


        self.collect_by_name("Inline Skates (Glaciers)")
        access_cache = build_access_cache(self.multiworld.state, player, 2, False, False)
        self.assertEqual(8, spots_l_glitchless(self.multiworld.state, player, False, access_cache))


        self.multiworld.state.prog_items[player]["rep"] = 20
        access_cache = build_access_cache(self.multiworld.state, player, 2, False, False)

        # chapter 1 - VH1-2
        self.assertEqual(22, spots_s_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(20, spots_m_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(23, spots_l_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(9, spots_xl_glitchless(self.multiworld.state, player, False, access_cache))


        self.multiworld.state.prog_items[player]["rep"] = 65
        access_cache = build_access_cache(self.multiworld.state, player, 2, False, False)

        # chapter 1 - VH3
        self.assertEqual(23, spots_m_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(24, spots_l_glitchless(self.multiworld.state, player, False, access_cache))


        self.multiworld.state.prog_items[player]["rep"] = 90
        access_cache = build_access_cache(self.multiworld.state, player, 2, False, False)

        # chapter 1 - VH4
        self.assertEqual(10, spots_xl_glitchless(self.multiworld.state, player, False, access_cache))


        self.multiworld.state.prog_items[player]["Chapter Completed"] = 1
        access_cache = build_access_cache(self.multiworld.state, player, 2, False, False)

        # chapter 2 - MS + MA1
        self.assertEqual(34, spots_s_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(39, spots_m_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(38, spots_l_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(19, spots_xl_glitchless(self.multiworld.state, player, False, access_cache))


        self.multiworld.state.prog_items[player]["rep"] = 120
        access_cache = build_access_cache(self.multiworld.state, player, 2, False, False)

        # chapter 2 - VHO
        self.assertEqual(35, spots_s_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(43, spots_m_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(40, spots_l_glitchless(self.multiworld.state, player, False, access_cache))


        self.collect_by_name("Bel")
        self.multiworld.state.prog_items[player]["rep"] = 180
        access_cache = build_access_cache(self.multiworld.state, player, 2, False, False)

        # chapter 2 - BT1
        self.assertEqual(44, spots_s_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(56, spots_m_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(50, spots_l_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(22, spots_xl_glitchless(self.multiworld.state, player, False, access_cache))


        self.multiworld.state.prog_items[player]["rep"] = 220
        access_cache = build_access_cache(self.multiworld.state, player, 2, False, False)

        # chapter 2 - BT2
        self.assertEqual(47, spots_s_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(60, spots_m_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(52, spots_l_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(23, spots_xl_glitchless(self.multiworld.state, player, False, access_cache))


        self.multiworld.state.prog_items[player]["rep"] = 250
        access_cache = build_access_cache(self.multiworld.state, player, 2, False, False)

        # chapter 2 - BTO1
        self.assertEqual(53, spots_l_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(24, spots_xl_glitchless(self.multiworld.state, player, False, access_cache))


        self.multiworld.state.prog_items[player]["rep"] = 280
        access_cache = build_access_cache(self.multiworld.state, player, 2, False, False)

        # chapter 2 - BT3 / chapter 3 - MS
        self.assertEqual(58, spots_l_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(28, spots_xl_glitchless(self.multiworld.state, player, False, access_cache))


        self.multiworld.state.prog_items[player]["rep"] = 320
        self.multiworld.state.prog_items[player]["Chapter Completed"] = 2
        access_cache = build_access_cache(self.multiworld.state, player, 2, False, False)

        # chapter 2 - BTO2 / chapter 3 - MS
        self.assertEqual(54, spots_s_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(67, spots_m_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(62, spots_l_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(30, spots_xl_glitchless(self.multiworld.state, player, False, access_cache))


        self.multiworld.state.prog_items[player]["rep"] = 380
        access_cache = build_access_cache(self.multiworld.state, player, 2, False, False)

        # chapter 3 - MM1-2
        self.assertEqual(61, spots_s_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(78, spots_m_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(73, spots_l_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(37, spots_xl_glitchless(self.multiworld.state, player, False, access_cache))


        self.multiworld.state.prog_items[player]["rep"] = 491
        access_cache = build_access_cache(self.multiworld.state, player, 2, False, False)

        # chapter 3 - MM3
        self.assertEqual(64, spots_s_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(82, spots_m_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(77, spots_l_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(42, spots_xl_glitchless(self.multiworld.state, player, False, access_cache))


        self.multiworld.state.prog_items[player]["Chapter Completed"] = 3
        access_cache = build_access_cache(self.multiworld.state, player, 2, False, False)

        # chapter 4 - MS / BT / MMO1 / PI1
        self.assertEqual(66, spots_s_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(85, spots_m_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(85, spots_l_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(46, spots_xl_glitchless(self.multiworld.state, player, False, access_cache))


        self.multiworld.state.prog_items[player]["rep"] = 620
        access_cache = build_access_cache(self.multiworld.state, player, 2, False, False)

        # chapter 4 - PI2
        self.assertEqual(71, spots_s_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(88, spots_m_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(89, spots_l_glitchless(self.multiworld.state, player, False, access_cache))


        self.multiworld.state.prog_items[player]["rep"] = 660
        access_cache = build_access_cache(self.multiworld.state, player, 2, False, False)

        # chapter 4 - PI3
        self.assertEqual(79, spots_s_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(96, spots_m_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(94, spots_l_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(51, spots_xl_glitchless(self.multiworld.state, player, False, access_cache))


        self.multiworld.state.prog_items[player]["rep"] = 730
        self.multiworld.state.prog_items[player]["Chapter Completed"] = 4
        access_cache = build_access_cache(self.multiworld.state, player, 2, False, False)

        # chapter 5 - PI4
        self.assertEqual(98, spots_m_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(96, spots_l_glitchless(self.multiworld.state, player, False, access_cache))


        self.multiworld.state.prog_items[player]["rep"] = 780
        access_cache = build_access_cache(self.multiworld.state, player, 2, False, False)

        # chapter 5 - PIO
        self.assertEqual(81, spots_s_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(103, spots_m_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(98, spots_l_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(54, spots_xl_glitchless(self.multiworld.state, player, False, access_cache))


        self.multiworld.state.prog_items[player]["rep"] = 850
        access_cache = build_access_cache(self.multiworld.state, player, 2, False, False)

        # chapter 5 - MA2
        self.assertEqual(84, spots_s_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(99, spots_l_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(56, spots_xl_glitchless(self.multiworld.state, player, False, access_cache))


        self.multiworld.state.prog_items[player]["rep"] = 864
        access_cache = build_access_cache(self.multiworld.state, player, 2, False, False)

        # chapter 5 - MA3
        self.assertEqual(89, spots_s_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(111, spots_m_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(102, spots_l_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(58, spots_xl_glitchless(self.multiworld.state, player, False, access_cache))


        self.multiworld.state.prog_items[player]["rep"] = 935
        access_cache = build_access_cache(self.multiworld.state, player, 2, False, False)

        # chapter 5 - MAO
        self.assertEqual(92, spots_s_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(112, spots_m_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(104, spots_l_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(60, spots_xl_glitchless(self.multiworld.state, player, False, access_cache))


        self.multiworld.state.prog_items[player]["rep"] = 960
        access_cache = build_access_cache(self.multiworld.state, player, 2, False, False)

        # chapter 5 - MA4-5
        self.assertEqual(94, spots_s_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(123, spots_m_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(111, spots_l_glitchless(self.multiworld.state, player, False, access_cache))
        self.assertEqual(62, spots_xl_glitchless(self.multiworld.state, player, False, access_cache))


class TestSpotsGlitched(BombRushCyberfunkTestBase):
    options = {
        "logic": "glitched"
    }

    @property
    def run_default_tests(self) -> bool:
        return False
    
    def test_spots_glitched(self) -> None:
        player = self.player

        self.collect_by_name([
            "Graffiti (M - OVERWHELMME)",
            "Graffiti (L - WHOLE SIXER)",
            "Graffiti (XL - Gold Rush)"
        ])
        access_cache = build_access_cache(self.multiworld.state, player, 2, False, True)

        self.assertEqual(75, spots_s_glitched(self.multiworld.state, player, False, access_cache))
        self.assertEqual(99, spots_m_glitched(self.multiworld.state, player, False, access_cache))
        self.assertEqual(88, spots_l_glitched(self.multiworld.state, player, False, access_cache))
        self.assertEqual(51, spots_xl_glitched(self.multiworld.state, player, False, access_cache))


        self.collect_by_name("Bel")
        self.multiworld.state.prog_items[player]["Chapter Completed"] = 1
        self.multiworld.state.prog_items[player]["rep"] = 180
        access_cache = build_access_cache(self.multiworld.state, player, 2, False, True)

        # brink terminal
        self.assertEqual(88, spots_s_glitched(self.multiworld.state, player, False, access_cache))
        self.assertEqual(120, spots_m_glitched(self.multiworld.state, player, False, access_cache))
        self.assertEqual(106, spots_l_glitched(self.multiworld.state, player, False, access_cache))
        self.assertEqual(58, spots_xl_glitched(self.multiworld.state, player, False, access_cache))


        self.multiworld.state.prog_items[player]["Chapter Completed"] = 2
        access_cache = build_access_cache(self.multiworld.state, player, 2, False, True)

        # chapter 3
        self.assertEqual(94, spots_s_glitched(self.multiworld.state, player, False, access_cache))
        self.assertEqual(123, spots_m_glitched(self.multiworld.state, player, False, access_cache))
        self.assertEqual(110, spots_l_glitched(self.multiworld.state, player, False, access_cache))
        self.assertEqual(61, spots_xl_glitched(self.multiworld.state, player, False, access_cache))


        self.multiworld.state.prog_items[player]["Chapter Completed"] = 3
        access_cache = build_access_cache(self.multiworld.state, player, 2, False, True)

        # chapter 4
        self.assertEqual(111, spots_l_glitched(self.multiworld.state, player, False, access_cache))
        self.assertEqual(62, spots_xl_glitched(self.multiworld.state, player, False, access_cache))