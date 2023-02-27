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
        for dungeon in excluded_dungeons:
            with self.subTest("dungeon excluded", dungeon=dungeon.name):
                self.assertTrue(dungeon.progress_type == LocationProgressType.EXCLUDED)

        excluded_regions = [region for dungeon in excluded_dungeons for region in dungeon.regions]
        for region in excluded_regions:
            with self.subTest("region excluded", region=region.name):
                self.assertTrue(region.progress_type == LocationProgressType.EXCLUDED)
            region.set_progress_type()
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
        for dungeon in excluded_dungeons:
            with self.subTest("dungeon excluded", dungeon=dungeon.name):
                self.assertTrue(dungeon.progress_type == LocationProgressType.EXCLUDED)

        excluded_regions = [region for dungeon in excluded_dungeons for region in dungeon.regions]
        for region in excluded_regions:
            with self.subTest("region excluded", region=region.name):
                self.assertTrue(region.progress_type == LocationProgressType.EXCLUDED)
            region.set_progress_type()
            for loc in region.locations:
                if not loc.item:
                    with self.subTest("location excluded", location=loc.name):
                        self.assertTrue(loc.progress_type == LocationProgressType.EXCLUDED)