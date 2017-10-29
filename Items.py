from BaseClasses import Item
import random
import logging


def ItemFactory(items):
    ret = []
    singleton = False
    if isinstance(items, str):
        items = [items]
        singleton = True
    for item in items:
        if item in item_table:
            advancement, priority, type, code, pedestal_hint, pedestal_credit, sickkid_credit, zora_credit, witch_credit, fluteboy_credit = item_table[item]
            if item == 'Bottle':
                # randomly fill bottle
                code = [0x16, 0x2B, 0x2C, 0x2D, 0x3C, 0x3D, 0x48][random.randint(0, 6)]
            ret.append(Item(item, advancement, priority, type, code, pedestal_hint, pedestal_credit, sickkid_credit, zora_credit, witch_credit, fluteboy_credit))
        else:
            logging.getLogger('').warning('Unknown Item: %s' % item)
            return None
    
    if singleton:
        return ret[0]
    else:
        return ret


# Format: Name: (Advancement, Priority, Type, ItemCode, Pedestal Hint Text, Pedestal Credit Text, Sick Kid Credit Text, Zora Credit Text, Witch Credit Text, Flute Boy Credit Text)
item_table = {'Bow': (True, False, None, 0x0B, 'You have\nchosen the\narcher class.', 'and the D', 'Ex-Adventurer', None, None, None),
              'Book of Mudora': (True, False, None, 0x1D, 'This is a\nparadox?!', 'and the Paradox', 'Lazy Reader', None, None, None),
              'Hammer': (True, False, None, 0x09, 'stop\nhammer time!', 'and the blunt weapon', None, None, None, None),
              'Hookshot': (True, False, None, 0x0A, 'BOING!!!\nBOING!!!\nBOING!!!', 'and the finglonger', None, None, None, None),
              'Magic Mirror': (True, False, None, 0x1A, 'Isn\'t your\nreflection so\npretty?', 'and the narcissism', None, None, None, None),
              'Ocarina': (True, False, None, 0x14, 'Save the duck\nand fly to\nfreedom!', 'and the sequel bait', None, None, None, None),
              'Pegasus Boots': (True, False, None, 0x4B, 'Gotta go fast!', 'and the cowboy boots', None, None, None, None),
              'Power Glove': (True, False, None, 0x1B, 'Now you can\nlift weak\nstuff!', 'and the input device', None, None, None, None),
              'Cape': (True, False, None, 0x19, 'Wear this to\nbecome\ninvisible!', 'and the invisicloak', None, None, None, None),
              'Mushroom': (True, False, None, 0x29, 'I\'m a fun guy!\n\nI\'m a funghi!', 'and the drugs', None, None, None, None),
              'Shovel': (True, False, None, 0x13, 'Can\n   You\n      Dig it?', 'and the fetch quest', None, None, None, None),
              'Lamp': (True, False, None, 0x12, 'Baby, baby,\nbaby.\nLight my way!', 'and the light source', None, None, None, None),
              'Magic Powder': (True, False, None, 0x0D, 'you can turn\nanti-faeries\ninto fairies', 'and the sprinkles', None, None, None, None),
              'Moon Pearl': (True, False, None, 0x1F, '  Bunny Link\n      be\n     gone!', 'and the debunnifier', None, None, None, None),
              'Cane of Somaria': (True, False, None, 0x15, 'I make blocks\nto hold down\nswitches!', 'and the red blocks', None, None, None, None),
              'Fire Rod': (True, False, None, 0x07, 'I\'m the hot\nrod. I make\nthings burn!', 'and the flamethrower', None, None, None, None),
              'Flippers': (True, False, None, 0x1E, 'fancy a swim?', 'and the toewebs', None, None, None, None),
              'Ice Rod': (True, False, None, 0x08, 'I\'m the cold\nrod. I make\nthings freeze!', 'and the ice machine', None, None, None, None),
              'Titans Mitts': (True, False, None, 0x1C, 'Now you can\nlift heavy\nstuff!', 'and Midas\' touch', None, None, None, None),
              'Ether': (True, False, None, 0x10, 'This magic\ncoin freezes\neverything!', 'and the fancy key', None, None, None, None),
              'Bombos': (True, False, None, 0x0F, 'Burn, baby,\nburn! Fear my\nring of fire!', 'and the airstrike', None, None, None, None),
              'Quake': (True, False, None, 0x11, 'Maxing out the\nRichter scale\nis what I do!', 'and the fancy key', None, None, None, None),
              'Bottle': (True, False, None, 0xFF, 'Now you can\nstore potions\nand stuff!', 'and the bee storage', None, None, None, None),  # specific content written on creation
              'Master Sword': (True, False, None, 0x50, 'I beat barries and pigs alike', 'and excalibur', None, None, None, None),
              'Tempered Sword': (True, False, None, 0x02, 'I stole the\nblacksmith\'s\njob!', 'and the forged bread', None, None, None, None),
              'Fighter Sword': (True, False, None, 0x49, 'A pathetic\nsword rests\nhere!', 'and the butter knife', None, None, None, None),
              'Golden Sword': (True, False, None, 0x03, 'The butter\nsword rests\nhere!', 'and the butter stick', None, None, None, None),
              'Progressive Sword': (True, False, None, 0x5E, 'a better copy\nof your sword\nfor your time', 'and the poke upgrade', None, None, None, None),
              'Progressive Glove': (True, False, None, 0x61, 'a way to lift\nheavier things', 'and the lift upgrade', None, None, None, None),
              'Silver Arrows': (True, False, None, 0x58, 'Do you fancy\nsilver tipped\narrows?', 'and the pig remover', None, None, None, None),
              'Green Pendant': (True, False, 'Crystal', [0x04, 0x38, 0x62, 0x00, 0x69, 0x01], None, None, None, None, None, None),
              'Red Pendant': (True, False, 'Crystal', [0x02, 0x34, 0x60, 0x00, 0x69, 0x02], None, None, None, None, None, None),
              'Blue Pendant': (True, False, 'Crystal', [0x01, 0x32, 0x60, 0x00, 0x69, 0x03], None, None, None, None, None, None),
              'Triforce': (True, False, None, 0x6A, '\n   YOU WIN!', 'and the triforce', None, None, None, None),
              'Power Star': (True, False, None, 0x6B, 'a small victory', 'and the power star', None, None, None, None),
              'Triforce Piece': (True, False, None, 0x6C, 'a small victory', 'and the thirdforce', None, None, None, None),
              'Crystal 1': (True, False, 'Crystal', [0x02, 0x34, 0x64, 0x40, 0x7F, 0x06], None, None, None, None, None, None),
              'Crystal 2': (True, False, 'Crystal', [0x10, 0x34, 0x64, 0x40, 0x79, 0x06], None, None, None, None, None, None),
              'Crystal 3': (True, False, 'Crystal', [0x40, 0x34, 0x64, 0x40, 0x6C, 0x06], None, None, None, None, None, None),
              'Crystal 4': (True, False, 'Crystal', [0x20, 0x34, 0x64, 0x40, 0x6D, 0x06], None, None, None, None, None, None),
              'Crystal 5': (True, False, 'Crystal', [0x04, 0x32, 0x64, 0x40, 0x6E, 0x06], None, None, None, None, None, None),
              'Crystal 6': (True, False, 'Crystal', [0x01, 0x32, 0x64, 0x40, 0x6F, 0x06], None, None, None, None, None, None),
              'Crystal 7': (True, False, 'Crystal', [0x08, 0x34, 0x64, 0x40, 0x7C, 0x06], None, None, None, None, None, None),
              'Single Arrow': (False, False, None, 0x43, 'a lonely arrow\nsits here.', 'and the arrow', None, None, None, None),
              'Arrows (10)': (False, False, None, 0x44, 'This will give\nyou ten shots\nwith your bow!', 'and the arrow pack', None, None, None, None),
              'Arrow Upgrade (+10)': (False, False, None, 0x54, 'increase arrow\nstorage, low\nlow price', 'and the quiver', None, None, None, None),
              'Arrow Upgrade (+5)': (False, False, None, 0x53, 'increase arrow\nstorage, low\nlow price', 'and the quiver', None, None, None, None),
              'Single Bomb': (False, False, None, 0x27, 'I make things\ngo BOOM! But\njust once.', 'and the explosive', None, None, None, None),
              'Bombs (3)': (False, False, None, 0x28, 'I make things\ngo triple\nBOOM!!!', 'and the boombox', None, None, None, None),
              'Bomb Upgrade (+10)': (False, False, None, 0x52, 'increase bomb\nstorage, low\nlow price', 'and the bomb bag', None, None, None, None),
              'Bomb Upgrade (+5)': (False, False, None, 0x51, 'increase bomb\nstorage, low\nlow price', 'and the bomb bag', None, None, None, None),
              'Blue Mail': (False, True, None, 0x22, 'Now you\'re a\nblue elf!', 'and the banana hat', None, None, None, None),
              'Red Mail': (False, True, None, 0x23, 'Now you\'re a\nred elf!', 'and the eggplant hat', None, None, None, None),
              'Progressive Armor': (False, True, None, 0x60, 'time for a\nchange of\nclothes?', 'and the hurt upgrade', None, None, None, None),
              'Blue Boomerang': (False, True, None, 0x0C, 'No matter what\nyou do, blue\nreturns to you', 'and the bluemarang', None, None, None, None),
              'Red Boomerang': (False, True, None, 0x2A, 'No matter what\nyou do, red\nreturns to you', 'and the badmarang', None, None, None, None),
              'Blue Shield': (False, True, None, 0x04, 'Now you can\ndefend against\npebbles!', 'and the stone blocker', None, None, None, None),
              'Red Shield': (False, True, None, 0x05, 'Now you can\ndefend against\nfireballs!', 'and the shot blocker', None, None, None, None),
              'Mirror Shield': (True, False, None, 0x06, 'Now you can\ndefend against\nlasers!', 'and the laser blocker', None, None, None, None),
              'Progressive Shield': (True, False, None, 0x5F, 'have a better\nblocker in\nfront of you', 'and the new shield', None, None, None, None),
              'Bug Catching Net': (True, False, None, 0x21, 'Let\'s catch\nsome bees and\nfaeries!', 'and the bee catcher', None, None, None, None),
              'Cane of Byrna': (True, False, None, 0x18, 'Use this to\nbecome\ninvincible!', 'and the bad cane', None, None, None, None),
              'Boss Heart Container': (False, False, None, 0x3E, 'Maximum health\nincreased!\nYeah!', 'and the love', None, None, None, None),
              'Sanctuary Heart Container': (False, False, None, 0x3F, 'Maximum health\nincreased!\nYeah!', 'and the love', None, None, None, None),
              'Piece of Heart': (False, False, None, 0x17, 'Just a little\npiece of love!', 'and the love', None, None, None, None),
              'Rupee (1)': (False, False, None, 0x34, 'Just pocket\nchange. Move\nright along.', 'and the cash stash', None, None, None, None),
              'Rupees (5)': (False, False, None, 0x35, 'Just pocket\nchange. Move\nright along.', 'and the cash stash', None, None, None, None),
              'Rupees (20)': (False, False, None, 0x36, 'Just couch\ncash. Move\nright along.', 'and the cash stash', None, None, None, None),
              'Rupees (50)': (False, False, None, 0x41, 'Just couch\ncash. Move\nright along.', 'and the cash stash', None, None, None, None),
              'Rupees (100)': (False, False, None, 0x40, 'A rupee stash!\nHell yeah!', 'and the cash stash', None, None, None, None),
              'Rupees (300)': (False, False, None, 0x46, 'A rupee hoard!\nHell yeah!', 'and the cash stash', None, None, None, None),
              'Rupoor': (False, False, None, 0x59, 'a debt collector', None, None, None, None, None),
              'Red Clock': (False, True, None, 0x5B, 'a waste of time', 'and the rolex', None, None, None, None),
              'Blue Clock': (False, True, None, 0x5C, 'a bit of time', 'and the rolex', None, None, None, None),
              'Green Clock': (False, True, None, 0x5D, 'a lot of time', 'and the rolex', None, None, None, None),
              'Single RNG': (False, True, None, 0x62, 'something you don\'t yet have', None, None, None, None, None),
              'Multi RNG': (False, True, None, 0x63, 'something you may already have', None, None, None, None, None),
              'Magic Upgrade (1/2)': (True, False, None, 0x4E, 'Your magic\npower has been\ndoubled!', 'and the spell power', None, None, None, None),  # can be required to beat mothula in an open seed in very very rare circumstance
              'Magic Upgrade (1/4)': (True, False, None, 0x4F, 'Your magic\npower has been\nquadrupled!', 'and the spell power', None, None, None, None),  # can be required to beat mothula in an open seed in very very rare circumstance
              'Small Key (Eastern Palace)': (False, False, 'SmallKey', 0xA2, 'Okay, this\nkey doesn\'t\nreally exist', None, None, None, None, None),
              'Big Key (Eastern Palace)': (False, False, 'BigKey', 0x9D, 'The big key\nof the east', None, None, None, None, None),
              'Compass (Eastern Palace)': (False, True, 'Compass', 0x8D, None, None, None, None, None, None),
              'Map (Eastern Palace)': (False, True, 'Map', 0x7D, None, None, None, None, None, None),
              'Small Key (Desert Palace)': (False, False, 'SmallKey', 0xA3, 'Sand spills\nout of this\nsmall key', None, None, None, None, None),
              'Big Key (Desert Palace)': (False, False, 'BigKey', 0x9C, 'Sand spills\nout of this\nbig key', None, None, None, None, None),
              'Compass (Desert Palace)': (False, True, 'Compass', 0x8C, None, None, None, None, None, None),
              'Map (Desert Palace)': (False, True, 'Map', 0x7C, None, None, None, None, None, None),
              'Small Key (Tower of Hera)': (False, False, 'SmallKey', 0xAA, 'The key\nto moldorms\nbasement', None, None, None, None, None),
              'Big Key (Tower of Hera)': (False, False, 'BigKey', 0x95, 'The big key\nto moldorms\nheart', None, None, None, None, None),
              'Compass (Tower of Hera)': (False, True, 'Compass', 0x85, None, None, None, None, None, None),
              'Map (Tower of Hera)': (False, True, 'Map', 0x75, None, None, None, None, None, None),
              'Small Key (Escape)': (False, False, 'SmallKey', 0xA0, 'The key to\nthe castle', None, None, None, None, None),
              'Big Key (Escape)': (False, False, 'BigKey', 0x9F, 'You should\nhave got this\nfrom a guard', None, None, None, None, None),
              'Map (Escape)': (False, True, 'Map', 0x7F, None, None, None, None, None, None),
              'Small Key (Agahnims Tower)': (False, False, 'SmallKey', 0xA4, 'Agahanim\nhalfway\nunlocked', None, None, None, None, None),
              'Small Key (Palace of Darkness)': (False, False, 'SmallKey', 0xA6, 'A small key\nthat steals\nlight', None, None, None, None, None),
              'Big Key (Palace of Darkness)': (False, False, 'BigKey', 0x99, 'Hammeryump\nwith this\nbig key', None, None, None, None, None),
              'Compass (Palace of Darkness)': (False, True, 'Compass', 0x89, None, None, None, None, None, None),
              'Map (Palace of Darkness)': (False, True, 'Map', 0x79, None, None, None, None, None, None),
              'Small Key (Thieves Town)': (False, False, 'SmallKey', 0xAB, 'The small key\nof rouges', None, None, None, None, None),
              'Big Key (Thieves Town)': (False, False, 'BigKey', 0x94, 'The Big Key\nof rouges', None, None, None, None, None),
              'Compass (Thieves Town)': (False, True, 'Compass', 0x84, None, None, None, None, None, None),
              'Map (Thieves Town)': (False, True, 'Map', 0x74, None, None, None, None, None, None),
              'Small Key (Skull Woods)': (False, False, 'SmallKey', 0xA8, 'The small key\nof the dark\nforest', None, None, None, None, None),
              'Big Key (Skull Woods)': (False, False, 'BigKey', 0x97, 'The big key\nof the dark\nforest', None, None, None, None, None),
              'Compass (Skull Woods)': (False, True, 'Compass', 0x87, None, None, None, None, None, None),
              'Map (Skull Woods)': (False, True, 'Map', 0x77, None, None, None, None, None, None),
              'Small Key (Swamp Palace)': (False, False, 'SmallKey', 0xA5, 'Access to\nthe swamp\nis granted', None, None, None, None, None),
              'Big Key (Swamp Palace)': (False, False, 'BigKey', 0x9A, 'The Big key\nto the swamp', None, None, None, None, None),
              'Compass (Swamp Palace)': (False, True, 'Compass', 0x8A, None, None, None, None, None, None),
              'Map (Swamp Palace)': (False, True, 'Map', 0x7A, None, None, None, None, None, None),
              'Small Key (Ice Palace)': (False, False, 'SmallKey', 0xA9, 'A frozen\nsmall key\nrests here', None, None, None, None, None),
              'Big Key (Ice Palace)': (False, False, 'BigKey', 0x96, 'A frozen\nbig key\nrests here', None, None, None, None, None),
              'Compass (Ice Palace)': (False, True, 'Compass', 0x86, None, None, None, None, None, None),
              'Map (Ice Palace)': (False, True, 'Map', 0x76, None, None, None, None, None, None),
              'Small Key (Misery Mire)': (False, False, 'SmallKey', 0xA7, 'The small key\nto Vitreous', None, None, None, None, None),
              'Big Key (Misery Mire)': (False, False, 'BigKey', 0x98, 'The big key\nto Vitreous', None, None, None, None, None),
              'Compass (Misery Mire)': (False, True, 'Compass', 0x88, None, None, None, None, None, None),
              'Map (Misery Mire)': (False, True, 'Map', 0x78, None, None, None, None, None, None),
              'Small Key (Turtle Rock)': (False, False, 'SmallKey', 0xAC, 'The small key\nof terrorpins', None, None, None, None, None),
              'Big Key (Turtle Rock)': (False, False, 'BigKey', 0x93, 'The big key\nof terrorpins', None, None, None, None, None),
              'Compass (Turtle Rock)': (False, True, 'Compass', 0x83, None, None, None, None, None, None),
              'Map (Turtle Rock)': (False, True, 'Map', 0x73, None, None, None, None, None, None),
              'Small Key (Ganons Tower)': (False, False, 'SmallKey', 0xAD, 'The small key\nof evils bane', None, None, None, None, None),
              'Big Key (Ganons Tower)': (False, False, 'BigKey', 0x92, 'The Big Key\nof evils bane', 'la key of evils bane', None, None, None, None),
              'Compass (Ganons Tower)': (False, True, 'Compass', 0x82, None, None, None, None, None, None),
              'Map (Ganons Tower)': (False, True, 'Map', 0x72, None, None, None, None, None, None),
              'Nothing': (False, False, None, 0x5A, 'Some Hot Air', 'and the Nothing', None, None, None, None),
              'Beat Agahnim 1': (True, False, 'Event', None, None, None, None, None, None, None),
              'Beat Agahnim 2': (True, False, 'Event', None, None, None, None, None, None, None)}
