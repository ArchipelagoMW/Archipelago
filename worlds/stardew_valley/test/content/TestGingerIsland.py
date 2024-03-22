from . import SVContentPackTestBase
from .. import SVTestBase
from ... import options
from ...content import content_packs
from ...strings.fish_names import Fish
from ...strings.villager_names import NPC


class TestGingerIsland(SVContentPackTestBase):
    vanilla_packs = (content_packs.pelican_town, content_packs.ginger_island)

    def test_leo_is_included(self):
        self.assertIn(NPC.leo, self.content.villagers)

    def test_ginger_island_fishes_are_included(self):
        fish_names = self.content.fishes.keys()

        self.assertIn(Fish.blue_discus, fish_names)
        self.assertIn(Fish.lionfish, fish_names)
        self.assertIn(Fish.stingray, fish_names)

        # 63 from pelican town + 3 ginger island exclusive
        self.assertEqual(63 + 3, len(self.content.fishes))


class TestWithoutGingerIslandE2E(SVTestBase):
    options = {
        options.ExcludeGingerIsland: options.ExcludeGingerIsland.option_true
    }

    def test_leo_is_not_in_the_pool(self):
        for item in self.multiworld.itempool:
            self.assertFalse(("Friendsanity: " + NPC.leo) in item.name)

        for location in self.multiworld.get_locations(self.player):
            self.assertFalse(("Friendsanity: " + NPC.leo) in location.name)
