from .TestInvertedMinor import TestInvertedMinor


class TestInvertedLightWorld(TestInvertedMinor):
    def setUp(self):
        super().setUp()

    def testLostWoods(self):
        self.run_location_tests([
            ["Master Sword Pedestal", False, []],
            ["Master Sword Pedestal", False, [], ['Green Pendant']],
            ["Master Sword Pedestal", False, [], ['Red Pendant']],
            ["Master Sword Pedestal", False, [], ['Blue Pendant']],
            ["Master Sword Pedestal", True, ['Green Pendant', 'Red Pendant', 'Blue Pendant', 'Beat Agahnim 1']],
            ["Master Sword Pedestal", True, ['Green Pendant', 'Red Pendant', 'Blue Pendant', 'Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Master Sword Pedestal", True, ['Green Pendant', 'Red Pendant', 'Blue Pendant', 'Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

            ["Mushroom", False, []],
            ["Mushroom", False, [], ['Moon Pearl']],
            ["Mushroom", True, ['Moon Pearl', 'Beat Agahnim 1']],
            ["Mushroom", True, ['Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Mushroom", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

            ["Lost Woods Hideout", False, []],
            ["Lost Woods Hideout", False, [], ['Moon Pearl']],
            ["Lost Woods Hideout", True, ['Moon Pearl', 'Beat Agahnim 1']],
            ["Lost Woods Hideout", True, ['Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Lost Woods Hideout", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

            ["Lumberjack Tree", False, []],
            ["Lumberjack Tree", False, [], ['Pegasus Boots']],
            ["Lumberjack Tree", False, [], ['Beat Agahnim 1']],
            ["Lumberjack Tree", False, [], ['Moon Pearl']],
            ["Lumberjack Tree", True, ['Pegasus Boots', 'Beat Agahnim 1', 'Moon Pearl']],
        ])

    def testKakariko(self):
        self.run_location_tests([
            ["Kakariko Tavern", False, []],
            ["Kakariko Tavern", True, ['Moon Pearl', 'Beat Agahnim 1']],
            ["Kakariko Tavern", True, ['Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Kakariko Tavern", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

            ["Chicken House", False, []],
            ["Chicken House", False, [], ['Moon Pearl']],
            ["Chicken House", False, ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)','Bomb Upgrade (50)']],
            ["Chicken House", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Beat Agahnim 1']],
            ["Chicken House", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Chicken House", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

            # top can't be bombed as super bunny and needs Moon Pearl
            ["Kakariko Well - Top", False, []],
            ["Kakariko Well - Top", False, [], ['Moon Pearl']],
            ["Kakariko Well - Top", False, ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)','Bomb Upgrade (50)']],
            ["Kakariko Well - Top", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Beat Agahnim 1']],
            ["Kakariko Well - Top", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Kakariko Well - Top", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

            ["Kakariko Well - Left", False, []],
            ["Kakariko Well - Left", True, ['Beat Agahnim 1']],
            ["Kakariko Well - Left", True, ['Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Kakariko Well - Left", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

            ["Kakariko Well - Middle", False, []],
            ["Kakariko Well - Middle", True, ['Beat Agahnim 1']],
            ["Kakariko Well - Middle", True, ['Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Kakariko Well - Middle", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

            ["Kakariko Well - Right", False, []],
            ["Kakariko Well - Right", True, ['Beat Agahnim 1']],
            ["Kakariko Well - Right", True, ['Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Kakariko Well - Right", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

            ["Kakariko Well - Bottom", False, []],
            ["Kakariko Well - Bottom", True, ['Beat Agahnim 1']],
            ["Kakariko Well - Bottom", True, ['Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Kakariko Well - Bottom", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

            ["Blind's Hideout - Top", False, []],
            ["Blind's Hideout - Top", False, [], ['Moon Pearl', 'Magic Mirror']],
            ["Blind's Hideout - Top", False, ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)','Bomb Upgrade (50)']],
            ["Blind's Hideout - Top", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Beat Agahnim 1']],
            ["Blind's Hideout - Top", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Blind's Hideout - Top", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

            ["Blind's Hideout - Left", False, []],
            ["Blind's Hideout - Left", False, [], ['Moon Pearl', 'Magic Mirror']],
            ["Blind's Hideout - Left", True, ['Moon Pearl', 'Beat Agahnim 1']],
            ["Blind's Hideout - Left", True, ['Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Blind's Hideout - Left", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

            ["Blind's Hideout - Right", False, []],
            ["Blind's Hideout - Right", False, [], ['Moon Pearl', 'Magic Mirror']],
            ["Blind's Hideout - Right", True, ['Moon Pearl', 'Beat Agahnim 1']],
            ["Blind's Hideout - Right", True, ['Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Blind's Hideout - Right", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

            ["Blind's Hideout - Far Left", False, []],
            ["Blind's Hideout - Far Left", False, [], ['Moon Pearl', 'Magic Mirror']],
            ["Blind's Hideout - Far Left", True, ['Moon Pearl', 'Beat Agahnim 1']],
            ["Blind's Hideout - Far Left", True, ['Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Blind's Hideout - Far Left", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

            ["Blind's Hideout - Far Right", False, []],
            ["Blind's Hideout - Far Right", False, [], ['Moon Pearl', 'Magic Mirror']],
            ["Blind's Hideout - Far Right", True, ['Moon Pearl', 'Beat Agahnim 1']],
            ["Blind's Hideout - Far Right", True, ['Magic Mirror', 'Beat Agahnim 1']],
            ["Blind's Hideout - Far Right", True, ['Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Blind's Hideout - Far Right", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

            ["Bottle Merchant", False, []],
            ["Bottle Merchant", True, ['Beat Agahnim 1']],
            ["Bottle Merchant", True, ['Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Bottle Merchant", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

            ["Sick Kid", False, []],
            ["Sick Kid", False, [], ['AnyBottle']],
            ["Sick Kid", False, ['Bottle (Bee)']],
            ["Sick Kid", False, ['Bottle (Fairy)']],
            ["Sick Kid", False, ['Bottle (Red Potion)']],
            ["Sick Kid", False, ['Bottle (Green Potion)']],
            ["Sick Kid", False, ['Bottle (Blue Potion)']],
            ["Sick Kid", False, ['Bottle']],
            ["Sick Kid", False, ['Bottle (Good Bee)']],
            ["Sick Kid", True, ['Bottle (Bee)', 'Beat Agahnim 1']],
            ["Sick Kid", True, ['Bottle (Bee)', 'Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Sick Kid", True, ['Bottle (Bee)', 'Moon Pearl', 'Progressive Glove', 'Progressive Glove']],
            ["Sick Kid", True, ['Bottle (Fairy)', 'Beat Agahnim 1']],
            ["Sick Kid", True, ['Bottle (Fairy)', 'Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Sick Kid", True, ['Bottle (Fairy)', 'Moon Pearl', 'Progressive Glove', 'Progressive Glove']],
            ["Sick Kid", True, ['Bottle (Red Potion)', 'Beat Agahnim 1']],
            ["Sick Kid", True, ['Bottle (Red Potion)', 'Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Sick Kid", True, ['Bottle (Red Potion)', 'Moon Pearl', 'Progressive Glove', 'Progressive Glove']],
            ["Sick Kid", True, ['Bottle (Green Potion)', 'Beat Agahnim 1']],
            ["Sick Kid", True, ['Bottle (Green Potion)', 'Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Sick Kid", True, ['Bottle (Green Potion)', 'Moon Pearl', 'Progressive Glove', 'Progressive Glove']],
            ["Sick Kid", True, ['Bottle (Blue Potion)', 'Beat Agahnim 1']],
            ["Sick Kid", True, ['Bottle (Blue Potion)', 'Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Sick Kid", True, ['Bottle (Blue Potion)', 'Moon Pearl', 'Progressive Glove', 'Progressive Glove']],
            ["Sick Kid", True, ['Bottle', 'Beat Agahnim 1']],
            ["Sick Kid", True, ['Bottle', 'Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Sick Kid", True, ['Bottle', 'Moon Pearl', 'Progressive Glove', 'Progressive Glove']],
            ["Sick Kid", True, ['Bottle (Good Bee)', 'Beat Agahnim 1']],
            ["Sick Kid", True, ['Bottle (Good Bee)', 'Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Sick Kid", True, ['Bottle (Good Bee)', 'Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

            ["Magic Bat", False, []],
            ["Magic Bat", False, [], ['Magic Powder']],
            ["Magic Bat", False, [], ['Hammer']],
            ["Magic Bat", False, [], ['Moon Pearl']],
            ["Magic Bat", False, ['Magic Powder', 'Hammer', 'Moon Pearl']],
            ["Magic Bat", True, ['Magic Powder', 'Hammer', 'Moon Pearl', 'Beat Agahnim 1']],
            ["Magic Bat", True, ['Magic Powder', 'Hammer', 'Moon Pearl', 'Progressive Glove']],

            ["Library", False, []],
            ["Library", False, [], ['Pegasus Boots']],
            ["Library", True, ['Pegasus Boots', 'Moon Pearl', 'Beat Agahnim 1']],
            ["Library", True, ['Pegasus Boots', 'Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Library", True, ['Pegasus Boots', 'Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

            ["Maze Race", False, []],
            ["Maze Race", False, [], ['Moon Pearl']],
            ["Maze Race", False, ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)','Bomb Upgrade (50)', 'Pegasus Boots']],
            ["Maze Race", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Beat Agahnim 1']],
            ["Maze Race", True, ['Pegasus Boots', 'Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Maze Race", True, ['Pegasus Boots', 'Moon Pearl', 'Progressive Glove', 'Progressive Glove']],
        ])

    def testSouthLightWorld(self):
        self.run_location_tests([
            ["Desert Ledge", False, []],
            ["Desert Ledge", False, [], ['Book of Mudora']],
            ["Desert Ledge", True, ['Book of Mudora', 'Beat Agahnim 1']],
            ["Desert Ledge", True, ['Book of Mudora', 'Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Desert Ledge", True, ['Book of Mudora', 'Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

            ["Checkerboard Cave", False, []],
            ["Checkerboard Cave", False, [], ['Progressive Glove']],
            ["Checkerboard Cave", False, [], ['Moon Pearl']],
            ["Checkerboard Cave", True, ['Progressive Glove', 'Beat Agahnim 1', 'Moon Pearl']],
            ["Checkerboard Cave", True, ['Progressive Glove', 'Hammer', 'Moon Pearl']],
            ["Checkerboard Cave", True, ['Progressive Glove', 'Progressive Glove', 'Moon Pearl']],

            ["Aginah's Cave", False, []],
            ["Aginah's Cave", False, [], ['Moon Pearl']],
            ["Aginah's Cave", False, [], ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)']],
            ["Aginah's Cave", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Beat Agahnim 1']],
            ["Aginah's Cave", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Aginah's Cave", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

            ["Bombos Tablet", False, []],
            ["Bombos Tablet", False, ['Progressive Sword'], ['Progressive Sword']],
            ["Bombos Tablet", False, [], ['Book of Mudora']],
            # Flute to Mire, take portal
            ["Bombos Tablet", True, ['Flute', 'Book of Mudora', 'Progressive Glove', 'Progressive Glove', 'Progressive Sword', 'Progressive Sword']],
            ["Bombos Tablet", True, ['Beat Agahnim 1', 'Book of Mudora', 'Progressive Sword', 'Progressive Sword']],
            ["Bombos Tablet", True, ['Moon Pearl', 'Book of Mudora', 'Progressive Glove', 'Progressive Glove', 'Progressive Sword', 'Progressive Sword']],
            ["Bombos Tablet", True, ['Moon Pearl', 'Book of Mudora', 'Progressive Glove', 'Hammer', 'Progressive Sword', 'Progressive Sword']],
            ["Bombos Tablet", True, ['Book of Mudora', 'Beat Agahnim 1', 'Progressive Sword', 'Progressive Sword']],

            ["Floodgate Chest", False, []],
            ["Floodgate Chest", False, [], ['Moon Pearl', 'Magic Mirror']],
            ["Floodgate Chest", True, ['Magic Mirror', 'Beat Agahnim 1']],
            ["Floodgate Chest", True, ['Moon Pearl', 'Beat Agahnim 1']],
            ["Floodgate Chest", True, ['Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Floodgate Chest", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

            ["Sunken Treasure", False, []],
            ["Sunken Treasure", False, [], ['Moon Pearl', 'Magic Mirror']],
            ["Sunken Treasure", True, ['Magic Mirror', 'Beat Agahnim 1']],
            ["Sunken Treasure", True, ['Moon Pearl', 'Beat Agahnim 1']],
            ["Sunken Treasure", True, ['Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Sunken Treasure", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

            ["Mini Moldorm Cave - Far Left", False, []],
            ["Mini Moldorm Cave - Far Left", False, [], ['Moon Pearl']],
            ["Mini Moldorm Cave - Far Left", False, [], ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)']],
            ["Mini Moldorm Cave - Far Left", True, ['Bomb Upgrade (+5)', 'Progressive Sword', 'Moon Pearl', 'Beat Agahnim 1']],
            ["Mini Moldorm Cave - Far Left", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Mini Moldorm Cave - Far Left", True, ['Bomb Upgrade (+5)', 'Progressive Sword', 'Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

            ["Mini Moldorm Cave - Left", False, []],
            ["Mini Moldorm Cave - Left", False, [], ['Moon Pearl']],
            ["Mini Moldorm Cave - Left", False, [], ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)']],
            ["Mini Moldorm Cave - Left", True, ['Bomb Upgrade (+5)', 'Progressive Sword', 'Moon Pearl', 'Beat Agahnim 1']],
            ["Mini Moldorm Cave - Left", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Mini Moldorm Cave - Left", True, ['Bomb Upgrade (+5)', 'Progressive Sword', 'Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

            ["Mini Moldorm Cave - Generous Guy", False, []],
            ["Mini Moldorm Cave - Generous Guy", False, [], ['Moon Pearl']],
            ["Mini Moldorm Cave - Generous Guy", False, [], ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)']],
            ["Mini Moldorm Cave - Generous Guy", True, ['Bomb Upgrade (+5)', 'Progressive Sword', 'Moon Pearl', 'Beat Agahnim 1']],
            ["Mini Moldorm Cave - Generous Guy", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Mini Moldorm Cave - Generous Guy", True, ['Bomb Upgrade (+5)', 'Progressive Sword', 'Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

            ["Mini Moldorm Cave - Right", False, []],
            ["Mini Moldorm Cave - Right", False, [], ['Moon Pearl']],
            ["Mini Moldorm Cave - Right", False, [], ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)']],
            ["Mini Moldorm Cave - Right", True, ['Bomb Upgrade (+5)', 'Progressive Sword', 'Moon Pearl', 'Beat Agahnim 1']],
            ["Mini Moldorm Cave - Right", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Mini Moldorm Cave - Right", True, ['Bomb Upgrade (+5)', 'Progressive Sword', 'Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

            ["Mini Moldorm Cave - Far Right", False, []],
            ["Mini Moldorm Cave - Far Right", False, [], ['Moon Pearl']],
            ["Mini Moldorm Cave - Far Right", False, [], ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)']],
            ["Mini Moldorm Cave - Far Right", True, ['Bomb Upgrade (+5)', 'Progressive Sword', 'Moon Pearl', 'Beat Agahnim 1']],
            ["Mini Moldorm Cave - Far Right", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Mini Moldorm Cave - Far Right", True, ['Bomb Upgrade (+5)', 'Progressive Sword', 'Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

            ["Ice Rod Cave", False, []],
            ["Ice Rod Cave", False, [], ['Moon Pearl']],
            ["Ice Rod Cave", False, [], ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)']],
            ["Ice Rod Cave", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Beat Agahnim 1']],
            ["Ice Rod Cave", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Ice Rod Cave", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Progressive Glove', 'Progressive Glove']],
        ])

    def testZoraArea(self):
        self.run_location_tests([
            ["King Zora", False, []],
            ["King Zora", False, [], ['Moon Pearl']],
            ["King Zora", True, ['Moon Pearl', 'Beat Agahnim 1']],
            ["King Zora", True, ['Progressive Glove', 'Moon Pearl', 'Hammer']],
            ["King Zora", True, ['Progressive Glove', 'Progressive Glove', 'Moon Pearl']],

            ["Zora's Ledge", False, []],
            ["Zora's Ledge", False, [], ['Flippers']],
            ["Zora's Ledge", False, [], ['Moon Pearl']],
            ["Zora's Ledge", True, ['Flippers', 'Moon Pearl', 'Beat Agahnim 1']],
            ["Zora's Ledge", True, ['Flippers', 'Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Zora's Ledge", True, ['Flippers', 'Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

            ["Waterfall Fairy - Left", False, []],
            ["Waterfall Fairy - Left", False, [], ['Flippers']],
            ["Waterfall Fairy - Left", False, [], ['Moon Pearl']],
            ["Waterfall Fairy - Left", True, ['Flippers', 'Moon Pearl', 'Beat Agahnim 1']],
            ["Waterfall Fairy - Left", True, ['Flippers', 'Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Waterfall Fairy - Left", True, ['Flippers', 'Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

            ["Waterfall Fairy - Right", False, []],
            ["Waterfall Fairy - Right", False, [], ['Flippers']],
            ["Waterfall Fairy - Right", False, [], ['Moon Pearl']],
            ["Waterfall Fairy - Right", True, ['Flippers', 'Moon Pearl', 'Beat Agahnim 1']],
            ["Waterfall Fairy - Right", True, ['Flippers', 'Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Waterfall Fairy - Right", True, ['Flippers', 'Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

        ])
    
    def testLightWorld(self):
        self.run_location_tests([
            ["Link's Uncle", False, []],
            ["Link's Uncle", False, [], ['Moon Pearl']],
            ["Link's Uncle", True, ['Moon Pearl', 'Beat Agahnim 1']],
            ["Link's Uncle", True, ['Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Link's Uncle", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

            ["Secret Passage", False, []],
            ["Secret Passage", False, [], ['Moon Pearl']],
            ["Secret Passage", True, ['Moon Pearl', 'Beat Agahnim 1']],
            ["Secret Passage", True, ['Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Secret Passage", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

            ["King's Tomb", False, []],
            ["King's Tomb", False, [], ['Pegasus Boots']],
            ["King's Tomb", False, ['Progressive Glove'], ['Progressive Glove']],
            ["King's Tomb", False, [], ['Moon Pearl']],
            ["King's Tomb", True, ['Pegasus Boots', 'Progressive Glove', 'Progressive Glove', 'Moon Pearl']],

            ["Sahasrahla's Hut - Left", False, []],
            ["Sahasrahla's Hut - Left", False, [], ['Moon Pearl', 'Magic Mirror']],
            ["Sahasrahla's Hut - Left", False, [], ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)', 'Pegasus Boots']],
            ["Sahasrahla's Hut - Left", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Beat Agahnim 1']],
            ["Sahasrahla's Hut - Left", True, ['Pegasus Boots', 'Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Sahasrahla's Hut - Left", True, ['Pegasus Boots', 'Moon Pearl', 'Progressive Glove', 'Progressive Glove']],
            # super bunny bonk
            ["Sahasrahla's Hut - Left", True, ['Magic Mirror', 'Beat Agahnim 1', 'Pegasus Boots']],

            ["Sahasrahla's Hut - Middle", False, []],
            ["Sahasrahla's Hut - Middle", False, [], ['Moon Pearl', 'Magic Mirror']],
            ["Sahasrahla's Hut - Middle", False, [], ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)', 'Pegasus Boots']],
            ["Sahasrahla's Hut - Middle", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Beat Agahnim 1']],
            ["Sahasrahla's Hut - Middle", True, ['Pegasus Boots', 'Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Sahasrahla's Hut - Middle", True, ['Pegasus Boots', 'Moon Pearl', 'Progressive Glove', 'Progressive Glove']],
            # super bunny bonk
            ["Sahasrahla's Hut - Middle", True, ['Magic Mirror', 'Beat Agahnim 1', 'Pegasus Boots']],

            ["Sahasrahla's Hut - Right", False, []],
            ["Sahasrahla's Hut - Right", False, [], ['Moon Pearl', 'Magic Mirror']],
            ["Sahasrahla's Hut - Right", False, [], ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)', 'Pegasus Boots']],
            ["Sahasrahla's Hut - Right", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Beat Agahnim 1']],
            ["Sahasrahla's Hut - Right", True, ['Pegasus Boots', 'Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Sahasrahla's Hut - Right", True, ['Pegasus Boots', 'Moon Pearl', 'Progressive Glove', 'Progressive Glove']],
            # super bunny bonk
            ["Sahasrahla's Hut - Right", True, ['Magic Mirror', 'Beat Agahnim 1', 'Pegasus Boots']],

            ["Sahasrahla", False, []],
            ["Sahasrahla", False, [], ['Green Pendant']],
            ["Sahasrahla", True, ['Green Pendant', 'Beat Agahnim 1']],
            ["Sahasrahla", True, ['Green Pendant', 'Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Sahasrahla", True, ['Green Pendant', 'Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

            ["Bonk Rock Cave", False, []],
            ["Bonk Rock Cave", False, [], ['Pegasus Boots']],
            ["Bonk Rock Cave", False, [], ['Moon Pearl']],
            ["Bonk Rock Cave", True, ['Pegasus Boots', 'Moon Pearl', 'Beat Agahnim 1']],
            ["Bonk Rock Cave", True, ['Pegasus Boots', 'Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Bonk Rock Cave", True, ['Pegasus Boots', 'Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

            ["Hobo", False, []],
            ["Hobo", False, [], ['Moon Pearl']],
            ["Hobo", True, ['Moon Pearl', 'Beat Agahnim 1']],
            ["Hobo", True, ['Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Hobo", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

            ["Cave 45", False, []],
            ["Cave 45", False, [], ['Moon Pearl', 'Magic Mirror']],
            ["Cave 45", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove']],
            ["Cave 45", True, ['Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Cave 45", True, ['Moon Pearl', 'Beat Agahnim 1']],
            ["Cave 45", True, ['Magic Mirror', 'Beat Agahnim 1']],

            ["Graveyard Cave", False, []],
            ["Graveyard Cave", False, [], ['Moon Pearl']],
            ["Graveyard Cave", False, [], ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)']],
            ["Graveyard Cave", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Progressive Glove', 'Progressive Glove']],
            ["Graveyard Cave", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Graveyard Cave", True, ['Bomb Upgrade (+5)', 'Moon Pearl', 'Beat Agahnim 1']],

            ["Potion Shop", False, []],
            ["Potion Shop", False, [], ['Mushroom']],
            ["Potion Shop", False, [], ['Moon Pearl']],
            ["Potion Shop", True, ['Mushroom', 'Moon Pearl', 'Beat Agahnim 1']],
            ["Potion Shop", True, ['Mushroom', 'Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Potion Shop", True, ['Mushroom', 'Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

            ["Lake Hylia Island", False, []],
            ["Lake Hylia Island", False, [], ['Moon Pearl']],
            ["Lake Hylia Island", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove']],
            ["Lake Hylia Island", True, ['Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Lake Hylia Island", True, ['Moon Pearl', 'Beat Agahnim 1']],

            ["Flute Spot", False, []],
            ["Flute Spot", False, [], ['Shovel']],
            ["Flute Spot", False, [], ['Moon Pearl']],
            ["Flute Spot", True, ['Shovel', 'Moon Pearl', 'Beat Agahnim 1']],
            ["Flute Spot", True, ['Shovel', 'Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Flute Spot", True, ['Shovel', 'Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

            ["Ganon", False, []],
            ["Ganon", False, [], ['Moon Pearl']],
            ["Ganon", False, [], ['Beat Agahnim 2']],
        ])