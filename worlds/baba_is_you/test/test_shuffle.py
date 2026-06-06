from .bases import BabaIsYouTestBase

from ..levels import LEVEL_DATA

from BaseClasses import CollectionState

class TestShuffleLogic(BabaIsYouTestBase):
    options = {
        "goal": 0,
        "level_shuffle": 2,
        "area_access": 2,
        "start_with_default_words": True,
        #"accessibility": "minimal",
    }

    # Check if we can complete Map 0-7 with only the default words
    def test_map_clearable(self) -> None:
        with self.subTest("Test that Map 0-7 are beatable with only the default words"):
            for i in range(8):
                regionName = self.world.level_shuffle_dict.get(f"Map-{i}")
                data = LEVEL_DATA.get(regionName)
                levelName = data.get("name")
                location = self.world.get_location(levelName + ": Win")
                if not location.can_reach(self.multiworld.state):
                    self.fail(f"Map-{i}, shuffled to {regionName}, is not beatable")
    
    def test_win_events(self) -> None:
        with self.subTest("All win events have the right amount and are obtainable"):
            state = self.multiworld.get_all_state()
            for name in LEVEL_DATA:
                data = LEVEL_DATA[name]
                if data.get("completeCount") is not None:
                    itemName = name + " Win"
                    wins = len(self.multiworld.find_item_locations(itemName, self.player))
                    neededWins = data.get("completeCount")
                    self.assertEqual(wins, neededWins, f"There are {wins} {itemName}s when there should be {neededWins}")
                    # unused: list all win types at the parent (should be only "[Parent] Win")
                    """if wins != neededWins:
                        childList = []
                        for name2 in LEVEL_DATA:
                            data2 = LEVEL_DATA[name2]
                            if data2.get("parent") == name:
                                name3 = self.world.level_shuffle_dict.get(name2)
                                location = self.world.get_location(LEVEL_DATA[name3]["name"] + ": Win Event")
                                childList.append(str(location.item))
                        self.fail(f"In {name}: "+str(childList))"""
                    self.assertEqual(state.count(itemName, self.player), neededWins, "There should be enough obtainable win events")