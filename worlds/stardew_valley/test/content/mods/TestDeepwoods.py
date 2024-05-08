from worlds.stardew_valley.data.artisan import MachineSource
from worlds.stardew_valley.mods.mod_data import ModNames
from worlds.stardew_valley.strings.artisan_good_names import ArtisanGood
from worlds.stardew_valley.strings.crop_names import Fruit
from worlds.stardew_valley.strings.machine_names import Machine
from worlds.stardew_valley.test.content import SVContentPackTestBase


class TestArtisanEquipment(SVContentPackTestBase):
    mods = (ModNames.deepwoods,)

    def test_mango_wine_exists(self):
        self.assertIn(MachineSource(item=Fruit.mango, machine=Machine.keg), self.content.game_items[ArtisanGood.specific_wine(Fruit.mango)].sources)
        self.assertIn(MachineSource(item=Fruit.mango, machine=Machine.keg), self.content.game_items[ArtisanGood.wine].sources)
