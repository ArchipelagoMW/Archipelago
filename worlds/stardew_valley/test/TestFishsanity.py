import unittest
from typing import ClassVar, Set

from .assertion import WorldAssertMixin
from .bases import SVTestBase
from ..content.feature import fishsanity
from ..mods.mod_data import ModNames
from ..options import Fishsanity, ExcludeGingerIsland, Mods, SpecialOrderLocations, Goal, QuestLocations
from ..strings.fish_names import Fish, SVEFish, DistantLandsFish

pelican_town_legendary_fishes = {Fish.angler, Fish.crimsonfish, Fish.glacierfish, Fish.legend, Fish.mutant_carp, }
pelican_town_hard_special_fishes = {Fish.lava_eel, Fish.octopus, Fish.scorpion_carp, Fish.ice_pip, Fish.super_cucumber, }
pelican_town_medium_special_fishes = {Fish.blobfish, Fish.dorado, }
pelican_town_hard_normal_fishes = {Fish.lingcod, Fish.pufferfish, Fish.void_salmon, }
pelican_town_medium_normal_fishes = {
    Fish.albacore, Fish.catfish, Fish.eel, Fish.flounder, Fish.ghostfish, Fish.goby, Fish.halibut, Fish.largemouth_bass, Fish.midnight_carp,
    Fish.midnight_squid, Fish.pike, Fish.red_mullet, Fish.salmon, Fish.sandfish, Fish.slimejack, Fish.stonefish, Fish.spook_fish, Fish.squid, Fish.sturgeon,
    Fish.tiger_trout, Fish.tilapia, Fish.tuna, Fish.woodskip,
}
pelican_town_easy_normal_fishes = {
    Fish.anchovy, Fish.bream, Fish.bullhead, Fish.carp, Fish.chub, Fish.herring, Fish.perch, Fish.rainbow_trout, Fish.red_snapper, Fish.sardine, Fish.shad,
    Fish.sea_cucumber, Fish.shad, Fish.smallmouth_bass, Fish.sunfish, Fish.walleye,
}
pelican_town_crab_pot_fishes = {
    Fish.clam, Fish.cockle, Fish.crab, Fish.crayfish, Fish.lobster, Fish.mussel, Fish.oyster, Fish.periwinkle, Fish.shrimp, Fish.snail,
}

ginger_island_hard_fishes = {Fish.pufferfish, Fish.stingray, Fish.super_cucumber, }
ginger_island_medium_fishes = {Fish.blue_discus, Fish.lionfish, Fish.tilapia, Fish.tuna, }
qi_board_legendary_fishes = {Fish.ms_angler, Fish.son_of_crimsonfish, Fish.glacierfish_jr, Fish.legend_ii, Fish.radioactive_carp, }

sve_pelican_town_hard_fishes = {
    SVEFish.grass_carp, SVEFish.king_salmon, SVEFish.kittyfish, SVEFish.meteor_carp, SVEFish.puppyfish, SVEFish.radioactive_bass, SVEFish.undeadfish,
    SVEFish.void_eel,
}
sve_pelican_town_medium_fishes = {
    SVEFish.bonefish, SVEFish.butterfish, SVEFish.frog, SVEFish.goldenfish, SVEFish.snatcher_worm, SVEFish.water_grub,
}
sve_pelican_town_easy_fishes = {SVEFish.bull_trout, SVEFish.minnow, }
sve_ginger_island_hard_fishes = {SVEFish.gemfish, SVEFish.shiny_lunaloo, }
sve_ginger_island_medium_fishes = {SVEFish.daggerfish, SVEFish.lunaloo, SVEFish.starfish, SVEFish.torpedo_trout, }
sve_ginger_island_easy_fishes = {SVEFish.baby_lunaloo, SVEFish.clownfish, SVEFish.seahorse, SVEFish.sea_sponge, }

distant_lands_hard_fishes = {DistantLandsFish.giant_horsehoe_crab, }
distant_lands_easy_fishes = {DistantLandsFish.void_minnow, DistantLandsFish.purple_algae, DistantLandsFish.swamp_leech, }


def complete_options_with_default(options):
    return {
        **{
            ExcludeGingerIsland: ExcludeGingerIsland.default,
            Mods: Mods.default,
            SpecialOrderLocations: SpecialOrderLocations.default,
        },
        **options
    }


class SVFishsanityTestBase(SVTestBase):
    expected_fishes: ClassVar[Set[str]] = set()

    @classmethod
    def setUpClass(cls) -> None:
        if cls is SVFishsanityTestBase:
            raise unittest.SkipTest("Base tests disabled")

        super().setUpClass()

    def test_fishsanity(self):
        with self.subTest("Locations are valid"):
            self.check_all_locations_match_expected_fishes()

    def check_all_locations_match_expected_fishes(self):
        location_fishes = {
            name
            for location_name in self.get_real_location_names()
            if (name := fishsanity.extract_fish_from_location_name(location_name)) is not None
        }

        self.assertEqual(location_fishes, self.expected_fishes)


class TestFishsanityNoneVanilla(SVFishsanityTestBase):
    options = complete_options_with_default({
        Fishsanity: Fishsanity.option_none,
    })

    @property
    def run_default_tests(self) -> bool:
        # None is default
        return False


class TestFishsanityLegendaries_Vanilla(SVFishsanityTestBase):
    options = complete_options_with_default({
        Fishsanity: Fishsanity.option_legendaries,
    })
    expected_fishes = pelican_town_legendary_fishes


class TestFishsanityLegendaries_QiBoard(SVFishsanityTestBase):
    options = complete_options_with_default({
        Fishsanity: Fishsanity.option_legendaries,
        SpecialOrderLocations: SpecialOrderLocations.option_board_qi,
        ExcludeGingerIsland: ExcludeGingerIsland.option_false
    })
    expected_fishes = pelican_town_legendary_fishes | qi_board_legendary_fishes


class TestFishsanitySpecial(SVFishsanityTestBase):
    options = complete_options_with_default({
        Fishsanity: Fishsanity.option_special,
    })
    expected_fishes = pelican_town_legendary_fishes | pelican_town_hard_special_fishes | pelican_town_medium_special_fishes


class TestFishsanityAll_Vanilla(SVFishsanityTestBase):
    options = complete_options_with_default({
        Fishsanity: Fishsanity.option_all,
    })
    expected_fishes = (
            pelican_town_legendary_fishes |
            pelican_town_hard_special_fishes |
            pelican_town_medium_special_fishes |
            pelican_town_hard_normal_fishes |
            pelican_town_medium_normal_fishes |
            pelican_town_easy_normal_fishes |
            pelican_town_crab_pot_fishes |
            ginger_island_hard_fishes |
            ginger_island_medium_fishes
    )


class TestFishsanityAll_ExcludeGingerIsland(SVFishsanityTestBase):
    options = complete_options_with_default({
        Fishsanity: Fishsanity.option_all,
        ExcludeGingerIsland: ExcludeGingerIsland.option_true,
    })
    expected_fishes = (
            pelican_town_legendary_fishes |
            pelican_town_hard_special_fishes |
            pelican_town_medium_special_fishes |
            pelican_town_hard_normal_fishes |
            pelican_town_medium_normal_fishes |
            pelican_town_easy_normal_fishes |
            pelican_town_crab_pot_fishes
    )


class TestFishsanityAll_SVE(SVFishsanityTestBase):
    options = complete_options_with_default({
        Fishsanity: Fishsanity.option_all,
        Mods: ModNames.sve,
    })
    expected_fishes = (
            pelican_town_legendary_fishes |
            pelican_town_hard_special_fishes |
            pelican_town_medium_special_fishes |
            pelican_town_hard_normal_fishes |
            pelican_town_medium_normal_fishes |
            pelican_town_easy_normal_fishes |
            pelican_town_crab_pot_fishes |
            ginger_island_hard_fishes |
            ginger_island_medium_fishes |
            sve_pelican_town_hard_fishes |
            sve_pelican_town_medium_fishes |
            sve_pelican_town_easy_fishes |
            sve_ginger_island_hard_fishes |
            sve_ginger_island_medium_fishes |
            sve_ginger_island_easy_fishes
    )


class TestFishsanityAll_ExcludeGingerIsland_SVE(SVFishsanityTestBase):
    options = complete_options_with_default({
        Fishsanity: Fishsanity.option_all,
        ExcludeGingerIsland: ExcludeGingerIsland.option_true,
        Mods: ModNames.sve,
    })
    expected_fishes = (
            pelican_town_legendary_fishes |
            pelican_town_hard_special_fishes |
            pelican_town_medium_special_fishes |
            pelican_town_hard_normal_fishes |
            pelican_town_medium_normal_fishes |
            pelican_town_easy_normal_fishes |
            pelican_town_crab_pot_fishes |
            sve_pelican_town_hard_fishes |
            sve_pelican_town_medium_fishes |
            sve_pelican_town_easy_fishes
    )


class TestFishsanityAll_DistantLands(SVFishsanityTestBase):
    options = complete_options_with_default({
        Fishsanity: Fishsanity.option_all,
        Mods: ModNames.distant_lands,
    })
    expected_fishes = (
            pelican_town_legendary_fishes |
            pelican_town_hard_special_fishes |
            pelican_town_medium_special_fishes |
            pelican_town_hard_normal_fishes |
            pelican_town_medium_normal_fishes |
            pelican_town_easy_normal_fishes |
            pelican_town_crab_pot_fishes |
            ginger_island_hard_fishes |
            ginger_island_medium_fishes |
            distant_lands_hard_fishes |
            distant_lands_easy_fishes
    )


class TestFishsanityAll_QiBoard(SVFishsanityTestBase):
    options = complete_options_with_default({
        Fishsanity: Fishsanity.option_all,
        SpecialOrderLocations: SpecialOrderLocations.option_board_qi,
        ExcludeGingerIsland: ExcludeGingerIsland.option_false
    })
    expected_fishes = (
            pelican_town_legendary_fishes |
            pelican_town_hard_special_fishes |
            pelican_town_medium_special_fishes |
            pelican_town_hard_normal_fishes |
            pelican_town_medium_normal_fishes |
            pelican_town_easy_normal_fishes |
            pelican_town_crab_pot_fishes |
            ginger_island_hard_fishes |
            ginger_island_medium_fishes |
            qi_board_legendary_fishes
    )


class TestFishsanityAll_ExcludeGingerIsland_QiBoard(SVFishsanityTestBase):
    options = complete_options_with_default({
        Fishsanity: Fishsanity.option_all,
        ExcludeGingerIsland: ExcludeGingerIsland.option_true,
        SpecialOrderLocations: SpecialOrderLocations.option_board_qi,
    })
    expected_fishes = (
            pelican_town_legendary_fishes |
            pelican_town_hard_special_fishes |
            pelican_town_medium_special_fishes |
            pelican_town_hard_normal_fishes |
            pelican_town_medium_normal_fishes |
            pelican_town_easy_normal_fishes |
            pelican_town_crab_pot_fishes
    )


class TestFishsanityExcludeLegendaries_Vanilla(SVFishsanityTestBase):
    options = complete_options_with_default({
        Fishsanity: Fishsanity.option_exclude_legendaries,
    })
    expected_fishes = (
            pelican_town_hard_special_fishes |
            pelican_town_medium_special_fishes |
            pelican_town_hard_normal_fishes |
            pelican_town_medium_normal_fishes |
            pelican_town_easy_normal_fishes |
            pelican_town_crab_pot_fishes |
            ginger_island_hard_fishes |
            ginger_island_medium_fishes
    )


class TestFishsanityExcludeLegendaries_QiBoard(SVFishsanityTestBase):
    options = complete_options_with_default({
        Fishsanity: Fishsanity.option_exclude_legendaries,
        SpecialOrderLocations: SpecialOrderLocations.option_board_qi,
        ExcludeGingerIsland: ExcludeGingerIsland.option_false
    })
    expected_fishes = (
            pelican_town_hard_special_fishes |
            pelican_town_medium_special_fishes |
            pelican_town_hard_normal_fishes |
            pelican_town_medium_normal_fishes |
            pelican_town_easy_normal_fishes |
            pelican_town_crab_pot_fishes |
            ginger_island_hard_fishes |
            ginger_island_medium_fishes
    )


class TestFishsanityExcludeHardFishes_Vanilla(SVFishsanityTestBase):
    options = complete_options_with_default({
        Fishsanity: Fishsanity.option_exclude_hard_fish,
    })
    expected_fishes = (
            pelican_town_medium_special_fishes |
            pelican_town_medium_normal_fishes |
            pelican_town_easy_normal_fishes |
            pelican_town_crab_pot_fishes |
            ginger_island_medium_fishes
    )


class TestFishsanityExcludeHardFishes_SVE(SVFishsanityTestBase):
    options = complete_options_with_default({
        Fishsanity: Fishsanity.option_exclude_hard_fish,
        Mods: ModNames.sve,
    })
    expected_fishes = (
            pelican_town_medium_special_fishes |
            pelican_town_medium_normal_fishes |
            pelican_town_easy_normal_fishes |
            pelican_town_crab_pot_fishes |
            ginger_island_medium_fishes |
            sve_pelican_town_medium_fishes |
            sve_pelican_town_easy_fishes |
            sve_ginger_island_medium_fishes |
            sve_ginger_island_easy_fishes
    )


class TestFishsanityExcludeHardFishes_DistantLands(SVFishsanityTestBase):
    options = complete_options_with_default({
        Fishsanity: Fishsanity.option_exclude_hard_fish,
        Mods: ModNames.distant_lands,
    })
    expected_fishes = (
            pelican_town_medium_special_fishes |
            pelican_town_medium_normal_fishes |
            pelican_town_easy_normal_fishes |
            pelican_town_crab_pot_fishes |
            ginger_island_medium_fishes |
            distant_lands_easy_fishes
    )


class TestFishsanityExcludeHardFishes_QiBoard(SVFishsanityTestBase):
    options = complete_options_with_default({
        Fishsanity: Fishsanity.option_exclude_hard_fish,
        SpecialOrderLocations: SpecialOrderLocations.option_board_qi,
        ExcludeGingerIsland: ExcludeGingerIsland.option_false
    })
    expected_fishes = (
            pelican_town_medium_special_fishes |
            pelican_town_medium_normal_fishes |
            pelican_town_easy_normal_fishes |
            pelican_town_crab_pot_fishes |
            ginger_island_medium_fishes
    )


class TestFishsanityOnlyEasyFishes_Vanilla(SVFishsanityTestBase):
    options = complete_options_with_default({
        Fishsanity: Fishsanity.option_only_easy_fish,
    })
    expected_fishes = (
            pelican_town_easy_normal_fishes |
            pelican_town_crab_pot_fishes
    )


class TestFishsanityOnlyEasyFishes_SVE(SVFishsanityTestBase):
    options = complete_options_with_default({
        Fishsanity: Fishsanity.option_only_easy_fish,
        Mods: ModNames.sve,
    })
    expected_fishes = (
            pelican_town_easy_normal_fishes |
            pelican_town_crab_pot_fishes |
            sve_pelican_town_easy_fishes |
            sve_ginger_island_easy_fishes
    )


class TestFishsanityOnlyEasyFishes_DistantLands(SVFishsanityTestBase):
    options = complete_options_with_default({
        Fishsanity: Fishsanity.option_only_easy_fish,
        Mods: ModNames.distant_lands,
    })
    expected_fishes = (
            pelican_town_easy_normal_fishes |
            pelican_town_crab_pot_fishes |
            distant_lands_easy_fishes
    )


class TestFishsanityOnlyEasyFishes_QiBoard(SVFishsanityTestBase):
    options = complete_options_with_default({
        Fishsanity: Fishsanity.option_only_easy_fish,
        SpecialOrderLocations: SpecialOrderLocations.option_board_qi,
        ExcludeGingerIsland: ExcludeGingerIsland.option_false
    })
    expected_fishes = (
            pelican_town_easy_normal_fishes |
            pelican_town_crab_pot_fishes
    )


class TestFishsanityMasterAnglerSVEWithoutQuests(WorldAssertMixin, SVTestBase):
    options = {
        Fishsanity: Fishsanity.option_all,
        Goal: Goal.option_master_angler,
        QuestLocations: -1,
        Mods: (ModNames.sve,),
    }

    def run_default_tests(self) -> bool:
        return True

    def test_fill(self):
        self.assert_basic_checks(self.multiworld)
