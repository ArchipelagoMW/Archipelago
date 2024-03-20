from worlds.ahit.Regions import act_chapters
from worlds.ahit.Rules import act_connections
from . import HatInTimeTestBase


class TestActs(HatInTimeTestBase):
    def run_default_tests(self) -> bool:
        return False
      
    def testAllStateCanReachEverything(self):
        pass

    options = {
        "ActRandomizer": 2,
        "EnableDLC1": 1,
        "EnableDLC2": 1,
        "ShuffleActContracts": 0,
    }

    def test_act_shuffle(self):
        for i in range(1000):
            self.world_setup()
            self.collect_all_but([""])

            for name in act_chapters.keys():
                region = self.multiworld.get_region(name, 1)
                for entrance in region.entrances:
                    if entrance.name in act_connections.keys():
                        continue

                    self.assertTrue(self.can_reach_entrance(entrance.name),
                                    f"Can't reach {name} from {entrance}\n"
                                    f"{entrance.parent_region.entrances[0]} -> {entrance.parent_region} "
                                    f"-> {entrance} -> {name}"
                                    f" (expected method of access)")
