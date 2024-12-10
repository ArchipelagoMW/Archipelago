from . import SVContentPackTestBase
from .. import SVTestBase
from ... import options
from ...content import content_packs
from ...data.artisan import MachineSource
from ...strings.artisan_good_names import ArtisanGood
from ...strings.crop_names import Fruit, Vegetable
from ...strings.fish_names import Fish
from ...strings.machine_names import Machine
from ...strings.villager_names import NPC


class TestGingerIsland(SVContentPackTestBase):
    vanilla_packs = SVContentPackTestBase.vanilla_packs + (content_packs.ginger_island_content_pack,)

    def test_leo_is_included(self):
        self.assertIn(NPC.leo, self.content.villagers)

    def test_ginger_island_fishes_are_included(self):
        fish_names = self.content.fishes.keys()

        self.assertIn(Fish.blue_discus, fish_names)
        self.assertIn(Fish.lionfish, fish_names)
        self.assertIn(Fish.stingray, fish_names)

        # 63 from pelican town + 3 ginger island exclusive
        self.assertEqual(63 + 3, len(self.content.fishes))

    def test_ginger_island_fruits_can_be_made_into_wines(self):
        self.assertIn(MachineSource(item=Fruit.banana, machine=Machine.keg), self.content.game_items[ArtisanGood.specific_wine(Fruit.banana)].sources)
        self.assertIn(MachineSource(item=Fruit.banana, machine=Machine.keg), self.content.game_items[ArtisanGood.wine].sources)

        self.assertIn(MachineSource(item=Fruit.mango, machine=Machine.keg), self.content.game_items[ArtisanGood.specific_wine(Fruit.mango)].sources)
        self.assertIn(MachineSource(item=Fruit.mango, machine=Machine.keg), self.content.game_items[ArtisanGood.wine].sources)

        self.assertIn(MachineSource(item=Fruit.pineapple, machine=Machine.keg), self.content.game_items[ArtisanGood.specific_wine(Fruit.pineapple)].sources)
        self.assertIn(MachineSource(item=Fruit.pineapple, machine=Machine.keg), self.content.game_items[ArtisanGood.wine].sources)

    def test_ginger_island_vegetables_can_be_made_into_wines(self):
        taro_root_juice_sources = self.content.game_items[ArtisanGood.specific_juice(Vegetable.taro_root)].sources
        self.assertIn(MachineSource(item=Vegetable.taro_root, machine=Machine.keg), taro_root_juice_sources)
        self.assertIn(MachineSource(item=Vegetable.taro_root, machine=Machine.keg), self.content.game_items[ArtisanGood.juice].sources)


class TestWithoutGingerIslandE2E(SVTestBase):
    options = {
        options.ExcludeGingerIsland: options.ExcludeGingerIsland.option_true
    }

    def test_leo_is_not_in_the_pool(self):
        for item in self.multiworld.itempool:
            self.assertFalse(("Friendsanity: " + NPC.leo) in item.name)

        for location in self.multiworld.get_locations(self.player):
            self.assertFalse(("Friendsanity: " + NPC.leo) in location.name)
