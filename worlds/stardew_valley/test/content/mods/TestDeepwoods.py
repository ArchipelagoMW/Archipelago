from ....data.artisan import MachineSource
from ....mods.mod_data import ModNames
from ....strings.artisan_good_names import ArtisanGood
from ....strings.crop_names import Fruit
from ....strings.machine_names import Machine
from ....test.content import SVContentPackTestBase


class TestArtisanEquipment(SVContentPackTestBase):
    mods = (ModNames.deepwoods,)

    def test_mango_wine_exists(self):
        self.assertIn(MachineSource(item=Fruit.mango, machine=Machine.keg), self.content.game_items[ArtisanGood.specific_wine(Fruit.mango)].sources)
        self.assertIn(MachineSource(item=Fruit.mango, machine=Machine.keg), self.content.game_items[ArtisanGood.wine].sources)
