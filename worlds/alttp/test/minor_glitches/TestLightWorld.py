from .TestMinor import TestMinor


class TestLightWorld(TestMinor):
    
    def testLightWorld(self):
        self.run_location_tests([
            ["Master Sword Pedestal", False, []],
            ["Master Sword Pedestal", False, [], ['Green Pendant']],
            ["Master Sword Pedestal", False, [], ['Red Pendant']],
            ["Master Sword Pedestal", False, [], ['Blue Pendant']],
            ["Master Sword Pedestal", True, ['Green Pendant', 'Red Pendant', 'Blue Pendant']],

            ["Link's Uncle", True, []],

            ["Secret Passage", True, []],

            ["King's Tomb", False, []],
            ["King's Tomb", False, [], ['Pegasus Boots']],
            ["King's Tomb", True, ['Pegasus Boots', 'Progressive Glove', 'Progressive Glove']],
            ["King's Tomb", True, ['Pegasus Boots', 'Progressive Glove', 'Hammer', 'Moon Pearl', 'Magic Mirror']],
            ["King's Tomb", True, ['Pegasus Boots', 'Beat Agahnim 1', 'Progressive Glove', 'Hookshot', 'Moon Pearl', 'Magic Mirror']],
            ["King's Tomb", True, ['Pegasus Boots', 'Beat Agahnim 1', 'Hammer', 'Hookshot', 'Moon Pearl', 'Magic Mirror']],
            ["King's Tomb", True, ['Pegasus Boots', 'Beat Agahnim 1', 'Flippers', 'Hookshot', 'Moon Pearl', 'Magic Mirror']],

            ["Floodgate Chest", True, []],

            ["Link's House", True, []],

            ["Kakariko Tavern", True, []],

            ["Chicken House", True, []],

            ["Aginah's Cave", True, []],

            ["Sahasrahla's Hut - Left", True, []],

            ["Sahasrahla's Hut - Middle", True, []],

            ["Sahasrahla's Hut - Right", True, []],

            ["Kakariko Well - Top", True, []],

            ["Kakariko Well - Left", True, []],

            ["Kakariko Well - Middle", True, []],

            ["Kakariko Well - Right", True, []],

            ["Kakariko Well - Bottom", True, []],

            ["Blind's Hideout - Top", True, []],

            ["Blind's Hideout - Left", True, []],

            ["Blind's Hideout - Right", True, []],

            ["Blind's Hideout - Far Left", True, []],

            ["Blind's Hideout - Far Right", True, []],

            ["Bonk Rock Cave", False, []],
            ["Bonk Rock Cave", False, [], ['Pegasus Boots']],
            ["Bonk Rock Cave", True, ['Pegasus Boots']],

            ["Mini Moldorm Cave - Far Left", True, []],

            ["Mini Moldorm Cave - Left", True, []],

            ["Mini Moldorm Cave - Right", True, []],

            ["Mini Moldorm Cave - Far Right", True, []],

            ["Ice Rod Cave", True, []],

            ["Bottle Merchant", True, []],

            ["Sahasrahla", False, []],
            ["Sahasrahla", False, [], ['Green Pendant']],
            ["Sahasrahla", True, ['Green Pendant']],

            ["Magic Bat", False, []],
            ["Magic Bat", False, [], ['Magic Powder']],
            ["Magic Bat", False, [], ['Hammer', 'Magic Mirror']],
            ["Magic Bat", False, [], ['Hammer', 'Moon Pearl']],
            ["Magic Bat", False, ['Progressive Glove'], ['Hammer', 'Progressive Glove']],
            ["Magic Bat", True, ['Magic Powder', 'Hammer']],
            ["Magic Bat", True, ['Magic Powder', 'Progressive Glove', 'Progressive Glove', 'Moon Pearl', 'Magic Mirror']],

            ["Sick Kid", False, []],
            ["Sick Kid", False, [], ['AnyBottle']],
            ["Sick Kid", True, ['Bottle (Bee)']],
            ["Sick Kid", True, ['Bottle (Fairy)']],
            ["Sick Kid", True, ['Bottle (Red Potion)']],
            ["Sick Kid", True, ['Bottle (Green Potion)']],
            ["Sick Kid", True, ['Bottle (Blue Potion)']],
            ["Sick Kid", True, ['Bottle']],
            ["Sick Kid", True, ['Bottle (Good Bee)']],

            ["Hobo", True, []],

            ["Bombos Tablet", False, []],
            ["Bombos Tablet", False, [], ['Magic Mirror']],
            ["Bombos Tablet", False, ['Progressive Sword'], ['Progressive Sword']],
            ["Bombos Tablet", False, [], ['Book of Mudora']],
            ["Bombos Tablet", False, [], ['Moon Pearl']],
            ["Bombos Tablet", True, ['Moon Pearl', 'Magic Mirror', 'Book of Mudora', 'Progressive Sword', 'Progressive Sword', 'Progressive Glove', 'Progressive Glove']],
            ["Bombos Tablet", True, ['Moon Pearl', 'Magic Mirror', 'Book of Mudora', 'Progressive Sword', 'Progressive Sword', 'Progressive Glove', 'Hammer']],
            ["Bombos Tablet", True, ['Moon Pearl', 'Magic Mirror', 'Book of Mudora', 'Progressive Sword', 'Progressive Sword', 'Beat Agahnim 1', 'Hammer']],
            ["Bombos Tablet", True, ['Moon Pearl', 'Magic Mirror', 'Book of Mudora', 'Progressive Sword', 'Progressive Sword', 'Beat Agahnim 1', 'Progressive Glove', 'Hookshot']],
            ["Bombos Tablet", True, ['Moon Pearl', 'Magic Mirror', 'Book of Mudora', 'Progressive Sword', 'Progressive Sword', 'Beat Agahnim 1', 'Flippers', 'Hookshot']],

            ["King Zora", True, []],

            ["Lost Woods Hideout", True, []],

            ["Lumberjack Tree", False, []],
            ["Lumberjack Tree", False, [], ['Pegasus Boots']],
            ["Lumberjack Tree", False, [], ['Beat Agahnim 1']],
            ["Lumberjack Tree", True, ['Pegasus Boots', 'Beat Agahnim 1']],

            ["Cave 45", False, []],
            ["Cave 45", False, [], ['Magic Mirror']],
            ["Cave 45", False, [], ['Moon Pearl']],
            ["Cave 45", True, ['Moon Pearl', 'Magic Mirror', 'Progressive Glove', 'Progressive Glove']],
            ["Cave 45", True, ['Moon Pearl', 'Magic Mirror', 'Progressive Glove', 'Hammer']],
            ["Cave 45", True, ['Moon Pearl', 'Magic Mirror', 'Beat Agahnim 1', 'Hammer']],
            ["Cave 45", True, ['Moon Pearl', 'Magic Mirror', 'Beat Agahnim 1', 'Progressive Glove', 'Hookshot']],
            ["Cave 45", True, ['Moon Pearl', 'Magic Mirror', 'Beat Agahnim 1', 'Flippers', 'Hookshot']],

            ["Graveyard Cave", False, []],
            ["Graveyard Cave", False, [], ['Magic Mirror']],
            ["Graveyard Cave", False, [], ['Moon Pearl']],
            ["Graveyard Cave", True, ['Moon Pearl', 'Magic Mirror', 'Progressive Glove', 'Progressive Glove']],
            ["Graveyard Cave", True, ['Moon Pearl', 'Magic Mirror', 'Progressive Glove', 'Hammer']],
            ["Graveyard Cave", True, ['Moon Pearl', 'Magic Mirror', 'Beat Agahnim 1', 'Hammer', 'Hookshot']],
            ["Graveyard Cave", True, ['Moon Pearl', 'Magic Mirror', 'Beat Agahnim 1', 'Progressive Glove', 'Hookshot']],
            ["Graveyard Cave", True, ['Moon Pearl', 'Magic Mirror', 'Beat Agahnim 1', 'Flippers', 'Hookshot']],

            ["Checkerboard Cave", False, []],
            ["Checkerboard Cave", False, [], ['Progressive Glove']],
            ["Checkerboard Cave", False, [], ['Flute']],
            ["Checkerboard Cave", False, [], ['Magic Mirror']],
            ["Checkerboard Cave", True, ['Flute', 'Magic Mirror', 'Progressive Glove', 'Progressive Glove']],

            ["Mini Moldorm Cave - Generous Guy", True, []],

            ["Library", False, []],
            ["Library", False, [], ['Pegasus Boots']],
            ["Library", True, ['Pegasus Boots']],

            ["Mushroom", True, []],

            ["Potion Shop", False, []],
            ["Potion Shop", False, [], ['Mushroom']],
            ["Potion Shop", True, ['Mushroom']],

            ["Maze Race", True, []],

            ["Desert Ledge", False, []],
            ["Desert Ledge", False, [], ['Book of Mudora', 'Flute']],
            ["Desert Ledge", False, [], ['Book of Mudora', 'Magic Mirror']],
            ["Desert Ledge", False, ['Progressive Glove'], ['Book of Mudora', 'Progressive Glove']],
            ["Desert Ledge", True, ['Book of Mudora']],
            ["Desert Ledge", True, ['Flute', 'Magic Mirror', 'Progressive Glove', 'Progressive Glove']],

            ["Lake Hylia Island", False, []],
            ["Lake Hylia Island", False, [], ['Magic Mirror']],
            ["Lake Hylia Island", False, [], ['Moon Pearl']],
            ["Lake Hylia Island", False, [], ['Flippers']],
            ["Lake Hylia Island", True, ['Flippers', 'Moon Pearl', 'Magic Mirror', 'Progressive Glove', 'Progressive Glove']],
            ["Lake Hylia Island", True, ['Flippers', 'Moon Pearl', 'Magic Mirror', 'Progressive Glove', 'Hammer']],
            ["Lake Hylia Island", True, ['Flippers', 'Moon Pearl', 'Magic Mirror', 'Beat Agahnim 1']],

            ["Sunken Treasure", True, []],

            ["Zora's Ledge", False, []],
            ["Zora's Ledge", False, [], ['Flippers']],
            ["Zora's Ledge", True, ['Flippers']],

            ["Flute Spot", False, []],
            ["Flute Spot", False, [], ['Shovel']],
            ["Flute Spot", True, ['Shovel']],

            ["Waterfall Fairy - Left", False, []],
            ["Waterfall Fairy - Left", False, [], ['Flippers']],
            ["Waterfall Fairy - Left", True, ['Flippers']],

            ["Waterfall Fairy - Right", False, []],
            ["Waterfall Fairy - Right", False, [], ['Flippers']],
            ["Waterfall Fairy - Right", True, ['Flippers']],
        ])