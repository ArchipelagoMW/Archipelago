from BaseClasses import LocationProgressType
from . import LTTPOptionsTestBase


class ExcludeDungeonsTest(LTTPOptionsTestBase):
    options = {
        "excluded_dungeons": ["Hyrule Castle", "Agahnims Tower", "pAlaCe Of DaRkneSs"]
    }
    dungeon_names = ["Hyrule Castle", "Agahnims Tower", "Palace of Darkness"]

    def testCaseInsensitivity(self):
        self.assertEqual(self.dungeon_names,
                         self.multiworld.excluded_dungeons[1].value)

    def testDungeonsExcluded(self):
        excluded_dungeons = [self.multiworld.get_dungeon(dungeon_name, 1) for dungeon_name in self.dungeon_names]
        excluded_regions = [region for dungeon in excluded_dungeons for region in dungeon.regions]
        for region in excluded_regions:
            with self.subTest("region excluded", region=region.name):
                self.assertTrue(region.progress_type == LocationProgressType.EXCLUDED)
            for loc in region.locations:
                if not loc.item:
                    with self.subTest("location excluded", location=loc.name):
                        self.assertTrue(loc.progress_type == LocationProgressType.EXCLUDED)


class ExcludeInvertedDungeonsTest(LTTPOptionsTestBase):
    options = {
        "mode": "inverted",
        "excluded_dungeons": ["Hyrule Castle", "Agahnims Tower", "Ganons Tower"]
    }
    dungeon_names = ["Hyrule Castle", "Inverted Agahnims Tower", "Inverted Ganons Tower"]

    def testDungeonsExcluded(self):
        excluded_dungeons = [self.multiworld.get_dungeon(dungeon_name, 1) for dungeon_name in self.dungeon_names]
        excluded_regions = [region for dungeon in excluded_dungeons for region in dungeon.regions]
        for region in excluded_regions:
            with self.subTest("region excluded", region=region.name):
                self.assertTrue(region.progress_type == LocationProgressType.EXCLUDED)
            for loc in region.locations:
                if not loc.item:
                    with self.subTest("location excluded", location=loc.name):
                        self.assertTrue(loc.progress_type == LocationProgressType.EXCLUDED)
