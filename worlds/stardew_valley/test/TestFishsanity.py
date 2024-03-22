import unittest
from typing import ClassVar, Set

from . import SVTestBase
from ..content.feature import fishsanity
from ..mods.mod_data import ModNames
from ..options import Fishsanity, ExcludeGingerIsland, Mods, SpecialOrderLocations
from ..strings.fish_names import Fish

pelican_town_legendary_fishes = {"Angler", "Crimsonfish", "Glacierfish", "Legend", "Mutant Carp", }
pelican_town_hard_special_fishes = {"Lava Eel", "Octopus", "Scorpion Carp", "Ice Pip", "Super Cucumber", }
pelican_town_medium_special_fishes = {"Blobfish", "Dorado", }
pelican_town_hard_normal_fishes = {"Lingcod", "Pufferfish", "Void Salmon", }
pelican_town_medium_normal_fishes = {
    "Albacore", "Catfish", "Eel", "Flounder", "Ghostfish", Fish.goby, "Halibut", "Largemouth Bass", "Midnight Carp", "Midnight Squid", "Pike", "Red Mullet", "Salmon",
    "Sandfish", "Slimejack", "Stonefish", "Spook Fish", "Squid", "Sturgeon", "Tiger Trout", "Tilapia", "Tuna", "Woodskip",
}
pelican_town_easy_normal_fishes = {
    "Anchovy", "Bream", "Bullhead", "Carp", "Chub", "Herring", "Perch", "Rainbow Trout", "Red Snapper", "Sardine", "Shad", "Sea Cucumber", "Shad",
    "Smallmouth Bass", "Sunfish", "Walleye",
}
pelican_town_crab_pot_fishes = {"Clam", "Cockle", "Crab", "Crayfish", "Lobster", "Mussel", "Oyster", "Periwinkle", "Shrimp", "Snail", }

ginger_island_hard_fishes = {"Pufferfish", "Stingray", "Super Cucumber", }
ginger_island_medium_fishes = {"Blue Discus", "Lionfish", "Tilapia", "Tuna", }
qi_board_legendary_fishes = {"Ms. Angler", "Son of Crimsonfish", "Glacierfish Jr.", "Legend II", "Radioactive Carp", }

sve_pelican_town_hard_fishes = {
    "Grass Carp", "King Salmon", "Kittyfish", "Meteor Carp", "Puppyfish", "Radioactive Bass", "Undeadfish", "Void Eel",
}
sve_pelican_town_medium_fishes = {"Bonefish", "Butterfish", "Frog", "Goldenfish", "Snatcher Worm", "Water Grub", "Dulse Seaweed", }
sve_pelican_town_easy_fishes = {"Bull Trout", "Minnow", }
sve_ginger_island_hard_fishes = {"Gemfish", "Shiny Lunaloo", }
sve_ginger_island_medium_fishes = {"Daggerfish", "Lunaloo", "Starfish", "Torpedo Trout", }
sve_ginger_island_easy_fishes = {"Baby Lunaloo", "Clownfish", "Seahorse", "Sea Sponge", }

distant_lands_hard_fishes = {"Giant Horsehoe Crab", }
distant_lands_easy_fishes = {"Void Minnow", "Purple Algae", "Swamp Leech", }


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
    options = {
        Fishsanity: Fishsanity.option_none,
    }

    @property
    def run_default_tests(self) -> bool:
        # None is default
        return False


class TestFishsanityLegendaries_Vanilla(SVFishsanityTestBase):
    options = {
        Fishsanity: Fishsanity.option_legendaries,
    }
    expected_fishes = pelican_town_legendary_fishes


class TestFishsanityLegendaries_QiBoard(SVFishsanityTestBase):
    options = {
        Fishsanity: Fishsanity.option_legendaries,
        SpecialOrderLocations: SpecialOrderLocations.option_board_qi,
    }
    expected_fishes = pelican_town_legendary_fishes | qi_board_legendary_fishes


class TestFishsanitySpecial(SVFishsanityTestBase):
    options = {
        Fishsanity: Fishsanity.option_special,
    }
    expected_fishes = pelican_town_legendary_fishes | pelican_town_hard_special_fishes | pelican_town_medium_special_fishes


class TestFishsanityAll_Vanilla(SVFishsanityTestBase):
    options = {
        Fishsanity: Fishsanity.option_all,
    }
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
    options = {
        Fishsanity: Fishsanity.option_all,
        ExcludeGingerIsland: ExcludeGingerIsland.option_true,
    }
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
    options = {
        Fishsanity: Fishsanity.option_all,
        Mods: ModNames.sve,
    }
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
    options = {
        Fishsanity: Fishsanity.option_all,
        ExcludeGingerIsland: ExcludeGingerIsland.option_true,
        Mods: ModNames.sve,
    }
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
    options = {
        Fishsanity: Fishsanity.option_all,
        Mods: ModNames.distant_lands,
    }
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
    options = {
        Fishsanity: Fishsanity.option_all,
        SpecialOrderLocations: SpecialOrderLocations.option_board_qi,
    }
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
    options = {
        Fishsanity: Fishsanity.option_all,
        ExcludeGingerIsland: ExcludeGingerIsland.option_true,
        SpecialOrderLocations: SpecialOrderLocations.option_board_qi,
    }
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
    options = {
        Fishsanity: Fishsanity.option_exclude_legendaries,
    }
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
    options = {
        Fishsanity: Fishsanity.option_exclude_legendaries,
        SpecialOrderLocations: SpecialOrderLocations.option_board_qi,
    }
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
    options = {
        Fishsanity: Fishsanity.option_exclude_hard_fish,
    }
    expected_fishes = (
            pelican_town_medium_special_fishes |
            pelican_town_medium_normal_fishes |
            pelican_town_easy_normal_fishes |
            pelican_town_crab_pot_fishes |
            ginger_island_medium_fishes
    )


class TestFishsanityExcludeHardFishes_SVE(SVFishsanityTestBase):
    options = {
        Fishsanity: Fishsanity.option_exclude_hard_fish,
        Mods: ModNames.sve,
    }
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
    options = {
        Fishsanity: Fishsanity.option_exclude_hard_fish,
        Mods: ModNames.distant_lands,
    }
    expected_fishes = (
            pelican_town_medium_special_fishes |
            pelican_town_medium_normal_fishes |
            pelican_town_easy_normal_fishes |
            pelican_town_crab_pot_fishes |
            ginger_island_medium_fishes |
            distant_lands_easy_fishes
    )


class TestFishsanityExcludeHardFishes_QiBoard(SVFishsanityTestBase):
    options = {
        Fishsanity: Fishsanity.option_exclude_hard_fish,
        SpecialOrderLocations: SpecialOrderLocations.option_board_qi,
    }
    expected_fishes = (
            pelican_town_medium_special_fishes |
            pelican_town_medium_normal_fishes |
            pelican_town_easy_normal_fishes |
            pelican_town_crab_pot_fishes |
            ginger_island_medium_fishes
    )


class TestFishsanityOnlyEasyFishes_Vanilla(SVFishsanityTestBase):
    options = {
        Fishsanity: Fishsanity.option_only_easy_fish,
    }
    expected_fishes = (
            pelican_town_easy_normal_fishes |
            pelican_town_crab_pot_fishes
    )


class TestFishsanityOnlyEasyFishes_SVE(SVFishsanityTestBase):
    options = {
        Fishsanity: Fishsanity.option_only_easy_fish,
        Mods: ModNames.sve,
    }
    expected_fishes = (
            pelican_town_easy_normal_fishes |
            pelican_town_crab_pot_fishes |
            sve_pelican_town_easy_fishes |
            sve_ginger_island_easy_fishes
    )


class TestFishsanityOnlyEasyFishes_DistantLands(SVFishsanityTestBase):
    options = {
        Fishsanity: Fishsanity.option_only_easy_fish,
        Mods: ModNames.distant_lands,
    }
    expected_fishes = (
            pelican_town_easy_normal_fishes |
            pelican_town_crab_pot_fishes |
            distant_lands_easy_fishes
    )


class TestFishsanityOnlyEasyFishes_QiBoard(SVFishsanityTestBase):
    options = {
        Fishsanity: Fishsanity.option_only_easy_fish,
        SpecialOrderLocations: SpecialOrderLocations.option_board_qi,
    }
    expected_fishes = (
            pelican_town_easy_normal_fishes |
            pelican_town_crab_pot_fishes
    )
