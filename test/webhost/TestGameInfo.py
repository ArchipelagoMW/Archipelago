import unittest
import Utils
import os
from worlds.AutoWorld import AutoWorldRegister


class TestTutorial(unittest.TestCase):
    def testHasGameInfo(self):
        import WebHost
        WebHost.create_ordered_tutorials_file()
        for game_name, world_type in AutoWorldRegister.world_types.items():
            if not world_type.hidden:
                target_path = Utils.local_path("WebHostLib", "static", "generated", "docs", game_name)
                for game_info_lang in world_type.web.game_info_languages:
                    with self.subTest(game_name):
                        try:
                            self.assertTrue(os.path.isfile(Utils.local_path(target_path,
                                                                            f'{game_info_lang}_{game_name}.md')))
                        except AssertionError:
                            self.fail(f'{game_name} missing game info file for "{game_info_lang}" language entry.')
