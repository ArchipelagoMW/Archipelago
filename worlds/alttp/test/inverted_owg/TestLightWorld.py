from .TestInvertedOWG import TestInvertedOWG


class TestLightWorld(TestInvertedOWG):

    def testLightWorld(self):
        self.run_location_tests([
            ["Master Sword Pedestal", False, []],
            ["Master Sword Pedestal", False, [], ['Green Pendant']],
            ["Master Sword Pedestal", False, [], ['Red Pendant']],
            ["Master Sword Pedestal", False, [], ['Blue Pendant']],
            ["Master Sword Pedestal", True, ['Green Pendant', 'Red Pendant', 'Blue Pendant', 'Moon Pearl', 'Pegasus Boots']],
            ["Master Sword Pedestal", True, ['Green Pendant', 'Red Pendant', 'Blue Pendant', 'Magic Mirror', 'Pegasus Boots']],

            ["Link's Uncle", False, []],
            ["Link's Uncle", False, [], ['Moon Pearl']],
            ["Link's Uncle", True, ['Moon Pearl', 'Pegasus Boots']],

            ["Secret Passage", False, []],
            ["Secret Passage", False, [], ['Moon Pearl']],
            ["Secret Passage", True, ['Moon Pearl', 'Pegasus Boots']],

            ["King's Tomb", False, []],
            ["King's Tomb", False, [], ['Pegasus Boots']],
            ["King's Tomb", False, [], ['Moon Pearl']],
            ["King's Tomb", False, ['Magic Mirror']],
            ["King's Tomb", True, ['Pegasus Boots', 'Moon Pearl']],

            ["Floodgate Chest", False, []],
            ["Floodgate Chest", False, [], ['Moon Pearl', 'Magic Mirror']],
            ["Floodgate Chest", True, ['Moon Pearl', 'Pegasus Boots']],
            ["Floodgate Chest", True, ['Magic Mirror', 'Pegasus Boots']],

            ["Kakariko Tavern", False, []],
            ["Kakariko Tavern", False, [], ['Moon Pearl', 'Magic Mirror']],
            ["Kakariko Tavern", True, ['Moon Pearl', 'Pegasus Boots']],
            ["Kakariko Tavern", True, ['Magic Mirror', 'Pegasus Boots']],
            ["Kakariko Tavern", True, ['Beat Agahnim 1', 'Moon Pearl']],
            ["Kakariko Tavern", True, ['Beat Agahnim 1', 'Magic Mirror']],

            ["Chicken House", False, []],
            ["Chicken House", False, [], ['Moon Pearl']],
            ["Chicken House", True, ['Moon Pearl', 'Pegasus Boots']],

            ["Aginah's Cave", False, []],
            ["Aginah's Cave", False, [], ['Moon Pearl']],
            ["Aginah's Cave", True, ['Moon Pearl', 'Pegasus Boots']],

            ["Sahasrahla's Hut - Left", False, []],
            ["Sahasrahla's Hut - Left", False, [], ['Moon Pearl', 'Magic Mirror']],
            ["Sahasrahla's Hut - Left", False, [], ['Moon Pearl', 'Pegasus Boots']],
            ["Sahasrahla's Hut - Left", True, ['Moon Pearl', 'Pegasus Boots']],
            ["Sahasrahla's Hut - Left", True, ['Magic Mirror', 'Pegasus Boots']],
            ##todo: Damage boost superbunny not in logic
            #["Sahasrahla's Hut - Left", True, ['Beat Agahnim 1', 'Pegasus Boots']],
            ["Sahasrahla's Hut - Left", True, ['Moon Pearl', 'Beat Agahnim 1']],

            ["Sahasrahla's Hut - Middle", False, []],
            ["Sahasrahla's Hut - Middle", False, [], ['Moon Pearl', 'Magic Mirror']],
            ["Sahasrahla's Hut - Middle", False, [], ['Moon Pearl', 'Pegasus Boots']],
            ["Sahasrahla's Hut - Middle", True, ['Moon Pearl', 'Pegasus Boots']],
            ["Sahasrahla's Hut - Middle", True, ['Magic Mirror', 'Pegasus Boots']],
            #["Sahasrahla's Hut - Middle", True, ['Beat Agahnim 1', 'Pegasus Boots']],
            ["Sahasrahla's Hut - Middle", True, ['Moon Pearl', 'Beat Agahnim 1']],

            ["Sahasrahla's Hut - Right", False, []],
            ["Sahasrahla's Hut - Right", False, [], ['Moon Pearl', 'Magic Mirror']],
            ["Sahasrahla's Hut - Right", False, [], ['Moon Pearl', 'Pegasus Boots']],
            ["Sahasrahla's Hut - Right", True, ['Moon Pearl', 'Pegasus Boots']],
            ["Sahasrahla's Hut - Right", True, ['Magic Mirror', 'Pegasus Boots']],
            #["Sahasrahla's Hut - Right", True, ['Beat Agahnim 1', 'Pegasus Boots']],
            ["Sahasrahla's Hut - Right", True, ['Moon Pearl', 'Beat Agahnim 1']],

            ["Kakariko Well - Top", False, []],
            ["Kakariko Well - Top", False, [], ['Moon Pearl']],
            ["Kakariko Well - Top", True, ['Moon Pearl', 'Pegasus Boots']],

            ["Kakariko Well - Left", False, []],
            ["Kakariko Well - Left", True, ['Moon Pearl', 'Pegasus Boots']],
            ["Kakariko Well - Left", True, ['Magic Mirror', 'Pegasus Boots']],
            ["Kakariko Well - Left", True, ['Progressive Glove', 'Progressive Glove', 'Pegasus Boots']],
            ["Kakariko Well - Left", True, ['Beat Agahnim 1']],

            ["Kakariko Well - Middle", False, []],
            ["Kakariko Well - Middle", True, ['Moon Pearl', 'Pegasus Boots']],
            ["Kakariko Well - Middle", True, ['Magic Mirror', 'Pegasus Boots']],
            ["Kakariko Well - Middle", True, ['Progressive Glove', 'Progressive Glove', 'Pegasus Boots']],
            ["Kakariko Well - Middle", True, ['Beat Agahnim 1']],

            ["Kakariko Well - Right", False, []],
            ["Kakariko Well - Right", True, ['Moon Pearl', 'Pegasus Boots']],
            ["Kakariko Well - Right", True, ['Magic Mirror', 'Pegasus Boots']],
            ["Kakariko Well - Right", True, ['Progressive Glove', 'Progressive Glove', 'Pegasus Boots']],
            ["Kakariko Well - Right", True, ['Beat Agahnim 1']],

            ["Kakariko Well - Bottom", False, []],
            ["Kakariko Well - Bottom", True, ['Moon Pearl', 'Pegasus Boots']],
            ["Kakariko Well - Bottom", True, ['Magic Mirror', 'Pegasus Boots']],
            ["Kakariko Well - Bottom", True, ['Progressive Glove', 'Progressive Glove', 'Pegasus Boots']],
            ["Kakariko Well - Bottom", True, ['Beat Agahnim 1']],

            ["Blind's Hideout - Top", False, []],
            ["Blind's Hideout - Top", False, [], ['Moon Pearl']],
            ["Blind's Hideout - Top", True, ['Moon Pearl', 'Pegasus Boots']],

            ["Blind's Hideout - Left", False, []],
            ["Blind's Hideout - Left", False, [], ['Moon Pearl', 'Magic Mirror']],
            ["Blind's Hideout - Left", True, ['Moon Pearl', 'Pegasus Boots']],
            ["Blind's Hideout - Left", True, ['Magic Mirror', 'Pegasus Boots']],
            ["Blind's Hideout - Left", True, ['Magic Mirror', 'Beat Agahnim 1']],

            ["Blind's Hideout - Right", False, []],
            ["Blind's Hideout - Right", False, [], ['Moon Pearl', 'Magic Mirror']],
            ["Blind's Hideout - Right", True, ['Moon Pearl', 'Pegasus Boots']],
            ["Blind's Hideout - Right", True, ['Magic Mirror', 'Pegasus Boots']],
            ["Blind's Hideout - Right", True, ['Magic Mirror', 'Beat Agahnim 1']],

            ["Blind's Hideout - Far Left", False, []],
            ["Blind's Hideout - Far Left", False, [], ['Moon Pearl', 'Magic Mirror']],
            ["Blind's Hideout - Far Left", True, ['Moon Pearl', 'Pegasus Boots']],
            ["Blind's Hideout - Far Left", True, ['Magic Mirror', 'Pegasus Boots']],
            ["Blind's Hideout - Far Left", True, ['Magic Mirror', 'Beat Agahnim 1']],

            ["Blind's Hideout - Far Right", False, []],
            ["Blind's Hideout - Far Right", False, [], ['Moon Pearl', 'Magic Mirror']],
            ["Blind's Hideout - Far Right", True, ['Moon Pearl', 'Pegasus Boots']],
            ["Blind's Hideout - Far Right", True, ['Magic Mirror', 'Pegasus Boots']],
            ["Blind's Hideout - Far Right", True, ['Magic Mirror', 'Beat Agahnim 1']],

            ["Bonk Rock Cave", False, []],
            ["Bonk Rock Cave", False, [], ['Pegasus Boots']],
            ["Bonk Rock Cave", False, [], ['Moon Pearl']],
            ["Bonk Rock Cave", True, ['Moon Pearl', 'Pegasus Boots']],

            ["Mini Moldorm Cave - Far Left", False, []],
            ["Mini Moldorm Cave - Far Left", False, [], ['Moon Pearl']],
            ["Mini Moldorm Cave - Far Left", True, ['Moon Pearl', 'Pegasus Boots']],

            ["Mini Moldorm Cave - Left", False, []],
            ["Mini Moldorm Cave - Left", False, [], ['Moon Pearl']],
            ["Mini Moldorm Cave - Left", True, ['Moon Pearl', 'Pegasus Boots']],

            ["Mini Moldorm Cave - Right", False, []],
            ["Mini Moldorm Cave - Right", False, [], ['Moon Pearl']],
            ["Mini Moldorm Cave - Right", True, ['Moon Pearl', 'Pegasus Boots']],

            ["Mini Moldorm Cave - Far Right", False, []],
            ["Mini Moldorm Cave - Far Right", False, [], ['Moon Pearl']],
            ["Mini Moldorm Cave - Far Right", True, ['Moon Pearl', 'Pegasus Boots']],

            ["Mini Moldorm Cave - Generous Guy", False, []],
            ["Mini Moldorm Cave - Generous Guy", False, [], ['Moon Pearl']],
            ["Mini Moldorm Cave - Generous Guy", True, ['Moon Pearl', 'Pegasus Boots']],

            ["Ice Rod Cave", False, []],
            ["Ice Rod Cave", False, [], ['Moon Pearl']],
            ["Ice Rod Cave", True, ['Moon Pearl', 'Pegasus Boots']],
            #I don't think so
            #["Ice Rod Cave", True, ['Magic Mirror', 'Pegasus Boots', 'BigRedBomb']],
            #["Ice Rod Cave", True, ['Magic Mirror', 'Beat Agahnim 1', 'BigRedBomb']],

            ["Bottle Merchant", False, []],
            ["Bottle Merchant", True, ['Pegasus Boots', 'Magic Mirror']],
            ["Bottle Merchant", True, ['Moon Pearl', 'Pegasus Boots']],
            ["Bottle Merchant", True, ['Progressive Glove', 'Progressive Glove', 'Pegasus Boots']],
            ["Bottle Merchant", True, ['Magic Mirror', 'Pegasus Boots']],

            ["Sahasrahla", False, []],
            ["Sahasrahla", False, [], ['Green Pendant']],
            ["Sahasrahla", True, ['Green Pendant', 'Magic Mirror', 'Pegasus Boots']],
            ["Sahasrahla", True, ['Green Pendant', 'Moon Pearl', 'Pegasus Boots']],
            ["Sahasrahla", True, ['Green Pendant', 'Magic Mirror', 'Pegasus Boots']],
            ["Sahasrahla", True, ['Green Pendant', 'Progressive Glove', 'Progressive Glove', 'Pegasus Boots']],

            ["Magic Bat", False, []],
            ["Magic Bat", False, [], ['Magic Powder']],
            ["Magic Bat", False, [], ['Moon Pearl']],
            ["Magic Bat", True, ['Magic Powder', 'Pegasus Boots', 'Moon Pearl']],

            ["Sick Kid", False, []],
            ["Sick Kid", False, [], ['AnyBottle']],
            ["Sick Kid", False, ['Bottle (Bee)']],
            ["Sick Kid", False, ['Bottle (Fairy)']],
            ["Sick Kid", False, ['Bottle (Red Potion)']],
            ["Sick Kid", False, ['Bottle (Green Potion)']],
            ["Sick Kid", False, ['Bottle (Blue Potion)']],
            ["Sick Kid", False, ['Bottle']],
            ["Sick Kid", False, ['Bottle (Good Bee)']],
            ["Sick Kid", True, ['Bottle (Bee)', 'Magic Mirror', 'Pegasus Boots']],
            ["Sick Kid", True, ['Bottle (Bee)', 'Moon Pearl', 'Pegasus Boots']],
            ["Sick Kid", True, ['Bottle (Fairy)', 'Magic Mirror', 'Pegasus Boots']],
            ["Sick Kid", True, ['Bottle (Fairy)', 'Moon Pearl', 'Pegasus Boots']],
            ["Sick Kid", True, ['Bottle (Red Potion)', 'Magic Mirror', 'Pegasus Boots']],
            ["Sick Kid", True, ['Bottle (Red Potion)', 'Moon Pearl', 'Pegasus Boots']],
            ["Sick Kid", True, ['Bottle (Green Potion)', 'Magic Mirror', 'Pegasus Boots']],
            ["Sick Kid", True, ['Bottle (Green Potion)', 'Moon Pearl', 'Pegasus Boots']],
            ["Sick Kid", True, ['Bottle (Blue Potion)', 'Magic Mirror', 'Pegasus Boots']],
            ["Sick Kid", True, ['Bottle (Blue Potion)', 'Moon Pearl', 'Pegasus Boots']],
            ["Sick Kid", True, ['Bottle (Good Bee)', 'Magic Mirror', 'Pegasus Boots']],
            ["Sick Kid", True, ['Bottle (Good Bee)', 'Moon Pearl', 'Pegasus Boots']],
            ["Sick Kid", True, ['Bottle', 'Magic Mirror', 'Pegasus Boots']],
            ["Sick Kid", True, ['Bottle', 'Moon Pearl', 'Pegasus Boots']],
            ["Sick Kid", True, ['Bottle', 'Progressive Glove', 'Progressive Glove', 'Pegasus Boots']],

            ["Hobo", False, []],
            ["Hobo", False, [], ['Moon Pearl']],
            ["Hobo", True, ['Moon Pearl', 'Pegasus Boots']],
            ["Hobo", True, ['Moon Pearl', 'Beat Agahnim 1']],

            ["Bombos Tablet", False, []],
            ["Bombos Tablet", False, ['Progressive Sword'], ['Progressive Sword']],
            ["Bombos Tablet", False, [], ['Book of Mudora']],
            ["Bombos Tablet", True, ['Moon Pearl', 'Book of Mudora', 'Pegasus Boots', 'Progressive Sword', 'Progressive Sword']],
            ["Bombos Tablet", True, ['Magic Mirror', 'Book of Mudora', 'Pegasus Boots', 'Progressive Sword', 'Progressive Sword']],
            ["Bombos Tablet", True, ['Progressive Glove', 'Progressive Glove', 'Book of Mudora', 'Pegasus Boots', 'Progressive Sword', 'Progressive Sword']],

            ["King Zora", False, []],
            ["King Zora", False, [], ['Moon Pearl']],
            ["King Zora", True, ['Moon Pearl', 'Pegasus Boots']],

            ["Lost Woods Hideout", False, []],
            ["Lost Woods Hideout", False, [], ['Moon Pearl']],
            ["Lost Woods Hideout", True, ['Moon Pearl', 'Pegasus Boots']],

            ["Lumberjack Tree", False, []],
            ["Lumberjack Tree", False, [], ['Beat Agahnim 1']],
            ["Lumberjack Tree", False, [], ['Pegasus Boots']],
            ["Lumberjack Tree", False, [], ['Moon Pearl']],
            ["Lumberjack Tree", True, ['Pegasus Boots', 'Moon Pearl', 'Beat Agahnim 1']],

            ["Cave 45", False, []],
            ["Cave 45", False, [], ['Moon Pearl', 'Magic Mirror']],
            ["Cave 45", True, ['Moon Pearl', 'Pegasus Boots']],
            ["Cave 45", True, ['Magic Mirror', 'Pegasus Boots']],
            ["Cave 45", True, ['Magic Mirror', 'Beat Agahnim 1']],

            ["Graveyard Cave", False, []],
            ["Graveyard Cave", False, [], ['Moon Pearl']],
            ["Graveyard Cave", True, ['Moon Pearl', 'Pegasus Boots']],

            ["Checkerboard Cave", False, []],
            ["Checkerboard Cave", False, [], ['Progressive Glove']],
            ["Checkerboard Cave", False, [], ['Moon Pearl']],
            ["Checkerboard Cave", True, ['Progressive Glove', 'Pegasus Boots', 'Moon Pearl']],

            ["Library", False, []],
            ["Library", False, [], ['Pegasus Boots']],
            ["Library", False, [], ['Moon Pearl', 'Magic Mirror']],
            ["Library", True, ['Pegasus Boots', 'Moon Pearl']],
            ["Library", True, ['Pegasus Boots', 'Magic Mirror']],

            ["Mushroom", False, []],
            ["Mushroom", False, [], ['Moon Pearl']],
            ["Mushroom", True, ['Moon Pearl', 'Pegasus Boots']],

            ["Potion Shop", False, []],
            ["Potion Shop", False, [], ['Mushroom']],
            ["Potion Shop", False, [], ['Moon Pearl']],
            ["Potion Shop", True, ['Mushroom', 'Moon Pearl', 'Pegasus Boots']],

            ["Maze Race", False, []],
            ["Maze Race", False, [], ['Moon Pearl']],
            ["Maze Race", True, ['Moon Pearl', 'Pegasus Boots']],

            ["Desert Ledge", False, []],
            ["Desert Ledge", True, ['Book of Mudora', 'Magic Mirror', 'Pegasus Boots']],
            ["Desert Ledge", True, ['Book of Mudora', 'Progressive Glove', 'Progressive Glove', 'Pegasus Boots']],
            ["Desert Ledge", True, ['Book of Mudora', 'Beat Agahnim 1']],
            ["Desert Ledge", True, ['Moon Pearl', 'Pegasus Boots']],

            ["Lake Hylia Island", False, []],
            ["Lake Hylia Island", False, [], ['Moon Pearl']],
            ["Lake Hylia Island", True, ['Moon Pearl', 'Pegasus Boots']],

            ["Sunken Treasure", False, []],
            ["Sunken Treasure", False, [], ['Moon Pearl', 'Magic Mirror']],
            ["Sunken Treasure", True, ['Moon Pearl', 'Pegasus Boots']],
            ["Sunken Treasure", True, ['Magic Mirror', 'Pegasus Boots']],
            ["Sunken Treasure", True, ['Magic Mirror', 'Beat Agahnim 1']],

            ["Zora's Ledge", False, []],
            ["Zora's Ledge", False, [], ['Moon Pearl']],
            ["Zora's Ledge", True, ['Moon Pearl', 'Pegasus Boots']],

            ["Flute Spot", False, []],
            ["Flute Spot", False, [], ['Shovel']],
            ["Flute Spot", False, [], ['Moon Pearl']],
            ["Flute Spot", True, ['Shovel', 'Moon Pearl', 'Pegasus Boots']],

            ["Waterfall Fairy - Left", False, []],
            ["Waterfall Fairy - Left", False, [], ['Moon Pearl']],
            ["Waterfall Fairy - Left", True, ['Moon Pearl', 'Pegasus Boots']],
            ["Waterfall Fairy - Left", True, ['Moon Pearl', 'Beat Agahnim 1']],
            ["Waterfall Fairy - Left", True, ['Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Waterfall Fairy - Left", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

            ["Waterfall Fairy - Right", False, []],
            ["Waterfall Fairy - Right", False, [], ['Moon Pearl']],
            ["Waterfall Fairy - Right", True, ['Moon Pearl', 'Pegasus Boots']],
            ["Waterfall Fairy - Right", True, ['Moon Pearl', 'Beat Agahnim 1']],
            ["Waterfall Fairy - Right", True, ['Moon Pearl', 'Progressive Glove', 'Hammer']],
            ["Waterfall Fairy - Right", True, ['Moon Pearl', 'Progressive Glove', 'Progressive Glove']],

            # Bomb Merchant is not a separate check, and is only used as part of the Pyramid Fairy rules
            # ["Bomb Merchant", False, []],
            # ["Bomb Merchant", False, [], ['Crystal 5']],
            # ["Bomb Merchant", False, [], ['Crystal 6']],
            # ["Bomb Merchant", True, ['Crystal 5', 'Crystal 6', 'Moon Pearl', 'Pegasus Boots']],
            # ["Bomb Merchant", True, ['Crystal 5', 'Crystal 6', 'Magic Mirror', 'Pegasus Boots']],
            # ["Bomb Merchant", True, ['Crystal 5', 'Crystal 6', 'Beat Agahnim 1']],

            ["Ganon", False, []],
        ])