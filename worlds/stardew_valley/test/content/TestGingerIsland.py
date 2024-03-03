from . import SVContentPackTestBase
from .. import SVTestBase
from ... import options
from ...content import content_packs
from ...strings.villager_names import NPC


class TestWithoutGingerIsland(SVContentPackTestBase):
    vanilla_packs = (content_packs.pelican_town,)

    def test_leo_is_not_included(self):
        self.assertNotIn(NPC.leo, self.content.villagers)


class TestGingerIsland(SVContentPackTestBase):
    vanilla_packs = (content_packs.pelican_town, content_packs.ginger_island)

    def test_leo_is_included(self):
        self.assertIn(NPC.leo, self.content.villagers)


class TestWithoutGingerIslandE2E(SVTestBase):
    options = {
        options.ExcludeGingerIsland: options.ExcludeGingerIsland.option_true
    }

    def test_leo_is_not_in_the_pool(self):
        for item in self.multiworld.itempool:
            self.assertFalse(("Friendsanity: " + NPC.leo) in item.name)

        for location in self.multiworld.get_locations(self.player):
            self.assertFalse(("Friendsanity: " + NPC.leo) in location.name)
