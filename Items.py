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
            advancement, key, crystal, code, altar_hint, altar_credit, sickkid_credit, zora_credit, witch_credit, fluteboy_credit = item_table[item]
            if item == 'Bottle':
                # randomly fill bottle
                code = [0x16, 0x2B, 0x2C, 0x2D, 0x3C, 0x3D, 0x48][random.randint(0, 6)]
            ret.append(Item(item, advancement, key, crystal, code, altar_hint, altar_credit, sickkid_credit, zora_credit, witch_credit, fluteboy_credit))
        else:
            logging.getLogger('').warning('Unknown Items: %s' % item)
    
    if singleton:
        return ret[0]
    else:
        return ret


# Format: Name: (Advancement, Key, Crystal, ItemCode, Altar Hint Text, Altar Credit Text, Sick Kid Credit Text, Zora Credit Text, Witch Credit Text, Flute Boy Credit Text)
item_table = {'Bow': (True, False, False, 0x0B, 'You have\nchosen the\narcher class.', None, None, None, None, None),
              'Book of Mudora': (True, False, False, 0x1D, 'This is a\nparadox?!', None, None, None, None, None),
              'Hammer': (True, False, False, 0x09, 'stop\nhammer time!', None, None, None, None, None),
              'Hookshot': (True, False, False, 0x0A, 'BOING!!!\nBOING!!!\nBOING!!!', None, None, None, None, None),
              'Magic Mirror': (True, False, False, 0x1A, 'Isn\'t your\nreflection so\npretty?', None, None, None, None, None),
              'Ocarina': (True, False, False, 0x14, 'Save the duck\nand fly to\nfreedom!', None, None, None, None, None),
              'Pegasus Boots': (True, False, False, 0x4B, 'Gotta go fast!', None, None, None, None, None),
              'Power Glove': (True, False, False, 0x1B, 'Now you can\nlift weak\nstuff!', None, None, None, None, None),
              'Cape': (True, False, False, 0x19, 'Wear this to\nbecome\ninvisible!', None, None, None, None, None),
              'Mushroom': (True, False, False, 0x29, 'I\'m a fun guy!\n\nI\'m a funghi!', None, None, None, None, None),
              'Shovel': (True, False, False, 0x13, 'Can\n   You\n      Dig it?', None, None, None, None, None),
              'Lamp': (True, False, False, 0x12, 'Baby, baby,\nbaby.\nLight my way!', None, None, None, None, None),
              'Magic Powder': (True, False, False, 0x0D, 'you can turn\nanti-faeries\ninto fairies', None, None, None, None, None),
              'Moon Pearl': (True, False, False, 0x1F, '  Bunny Link\n      be\n     gone!', None, None, None, None, None),
              'Cane of Somaria': (True, False, False, 0x15, 'I make blocks\nto hold down\nswitches!', None, None, None, None, None),
              'Fire Rod': (True, False, False, 0x07, 'I\'m the hot\nrod. I make\nthings burn!', None, None, None, None, None),
              'Flippers': (True, False, False, 0x1E, 'fancy a swim?', None, None, None, None, None),
              'Ice Rod': (True, False, False, 0x08, 'I\'m the cold\nrod. I make\nthings freeze!', None, None, None, None, None),
              'Titans Mitts': (True, False, False, 0x1C, 'Now you can\nlift heavy\nstuff!', None, None, None, None, None),
              'Ether': (True, False, False, 0x10, 'Zero Kelvin!\nAbsolute zero!\nFear the cold!', None, None, None, None, None),
              'Bombos': (True, False, False, 0x0F, 'Burn, baby,\nburn! Fear my\nring of fire!', None, None, None, None, None),
              'Quake': (True, False, False, 0x11, 'Maxing out the\nRichter scale\nis what I do!', None, None, None, None, None),
              'Bottle': (True, False, False, 0xFF, 'Now you can\nstore potions\nand stuff!', None, None, None, None, None),  # specific content written on creation
              'Master Sword': (True, False, False, 0x50, 'I thought this\nwas meant to\nbe randomized?', None, None, None, None, None),
              'Tempered Sword': (True, False, False, 0x02, 'I stole the\nblacksmith\'s\njob!', None, None, None, None, None),
              'Fighter Sword': (True, False, False, 0x49, 'A pathetic\nsword rests\nhere!', None, None, None, None, None),
              'GoldenSword': (True, False, False, 0x03, 'The butter\nsword rests\nhere!', None, None, None, None, None),
              'Progressive Sword': (True, False, False, 0x5E, 'a better copy\nof your sword\nfor your time', None, None, None, None, None),
              'Progressive Glove': (True, False, False, 0x61, 'a way to lift\nheavier things', None, None, None, None, None),
              'Silver Arrows': (True, False, False, 0x58, 'Do you fancy\nsilver tipped\narrows?', None, None, None, None, None),
              'Green Pendant': (True, False, True, [0x04, 0x38, 0x60, 0x00, 0x69, 0x01], None, None, None, None, None, None),
              'Red Pendant': (True, False, True, [0x02, 0x34, 0x60, 0x00, 0x69, 0x02], None, None, None, None, None, None),
              'Blue Pendant': (True, False, True, [0x01, 0x32, 0x60, 0x00, 0x69, 0x03], None, None, None, None, None, None),
              'Triforce': (True, False, False, 0x6A, '\n   YOU WIN!', None, None, None, None, None),
              'Crystal 1': (True, False, True, [0x02, 0x34, 0x64, 0x40, 0x7F, 0x06], None, None, None, None, None, None),
              'Crystal 2': (True, False, True, [0x10, 0x34, 0x64, 0x40, 0x79, 0x06], None, None, None, None, None, None),
              'Crystal 3': (True, False, True, [0x40, 0x34, 0x64, 0x40, 0x6C, 0x06], None, None, None, None, None, None),
              'Crystal 4': (True, False, True, [0x20, 0x34, 0x64, 0x40, 0x6D, 0x06], None, None, None, None, None, None),
              'Crystal 5': (True, False, True, [0x04, 0x34, 0x64, 0x40, 0x6E, 0x06], None, None, None, None, None, None),
              'Crystal 6': (True, False, True, [0x01, 0x34, 0x64, 0x40, 0x6F, 0x06], None, None, None, None, None, None),
              'Crystal 7': (True, False, True, [0x08, 0x34, 0x64, 0x40, 0x7C, 0x06], None, None, None, None, None, None),
              'Single Arrow': (False, False, False, 0x43, 'a lonely arrow\nsits here.', None, None, None, None, None),
              'Arrows (10)': (False, False, False, 0x44, 'This will give\nyou ten shots\nwith your bow!', None, None, None, None, None),
              'Arrow Upgrade (+10)': (False, False, False, 0x54, 'increase arrow\nstorage, low\nlow price', None, None, None, None, None),
              'Arrow Upgrade (+5)': (False, False, False, 0x53, 'increase arrow\nstorage, low\nlow price', None, None, None, None, None),
              'Single Bomb': (False, False, False, 0x27, 'I make things\ngo BOOM! But\njust once.', None, None, None, None, None),
              'Bombs (3)': (False, False, False, 0x28, 'I make things\ngo triple\nBOOM!!!', None, None, None, None, None),
              'Bomb Upgrade (+10)': (False, False, False, 0x52, 'increase bomb\nstorage, low\nlow price', None, None, None, None, None),
              'Bomb Upgrade (+5)': (False, False, False, 0x51, 'increase bomb\nstorage, low\nlow price', None, None, None, None, None),
              'Blue Mail': (False, False, False, 0x22, 'Now you\'re a\nblue elf!', None, None, None, None, None),
              'Red Mail': (False, False, False, 0x23, 'Now you\'re a\nred elf!', None, None, None, None, None),
              'Progressive Armor': (False, False, False, 0x60, 'time for a\nchange of\nclothes?', None, None, None, None, None),
              'Blue Boomerang': (False, False, False, 0x0C, 'No matter what\nyou do, blue\nreturns to you', None, None, None, None, None),
              'Red Boomerang': (False, False, False, 0x2A, 'No matter what\nyou do, red\nreturns to you', None, None, None, None, None),
              'Blue Shield': (False, False, False, 0x04, 'Now you can\ndefend against\npebbles!', None, None, None, None, None),
              'Red Shield': (False, False, False, 0x05, 'Now you can\ndefend against\nfireballs!', None, None, None, None, None),
              'Mirror Shield': (False, False, False, 0x06, 'Now you can\ndefend against\nlasers!', None, None, None, None, None),
              'Progressive Shield': (False, False, False, 0x5F, 'have a better\nblocker in\nfront of you', None, None, None, None, None),
              'Bug Catching Net': (False, False, False, 0x21, 'Let\'s catch\nsome bees and\nfaeries!', None, None, None, None, None),
              'Cane of Byrna': (False, False, False, 0x18, 'Use this to\nbecome\ninvincible!', None, None, None, None, None),
              'Boss Heart Container': (False, False, False, 0x3E, 'Maximum health\nincreased!\nYeah!', None, None, None, None, None),
              'Sanctuary Heart Container': (False, False, False, 0x3F, 'Maximum health\nincreased!\nYeah!', None, None, None, None, None),
              'Piece of Heart': (False, False, False, 0x17, 'Just a little\npiece of love!', None, None, None, None, None),
              'Rupee (1)': (False, False, False, 0x34, 'Just pocket\nchange. Move\nright along.', None, None, None, None, None),
              'Rupees (5)': (False, False, False, 0x35, 'Just pocket\nchange. Move\nright along.', None, None, None, None, None),
              'Rupees (20)': (False, False, False, 0x36, 'Just couch\ncash. Move\nright along.', None, None, None, None, None),
              'Rupees (50)': (False, False, False, 0x41, 'Just couch\ncash. Move\nright along.', None, None, None, None, None),
              'Rupees (100)': (False, False, False, 0x40, 'A rupee stash!\nHell yeah!', None, None, None, None, None),
              'Rupees (300)': (False, False, False, 0x46, 'A rupee hoard!\nHell yeah!', None, None, None, None, None),
              'Magic Upgrade (1/2)': (True, False, False, 0x4E, 'Your magic\npower has been\ndoubled!', None, None, None, None, None),  # can be required to beat mothula in an open seed in very very rare circumstance
              'Magic Upgrade (1/4)': (True, False, False, 0x4F, 'Your magic\npower has been\nquadrupled!', None, None, None, None, None),  # can be required to beat mothula in an open seed in very very rare circumstance
              # ToDo Use dungeons specific items once they work correctly
              'Small Key (Eastern Palace)': (False, True, False, 0x24, None, None, None, None, None, None),
              'Big Key (Eastern Palace)': (False, True, False, 0x32, None, None, None, None, None, None),
              'Compass (Eastern Palace)': (False, False, False, 0x25, None, None, None, None, None, None),
              'Map (Eastern Palace)': (False, False, False, 0x33, None, None, None, None, None, None),
              'Small Key (Desert Palace)': (False, True, False, 0x24, None, None, None, None, None, None),
              'Big Key (Desert Palace)': (False, True, False, 0x32, None, None, None, None, None, None),
              'Compass (Desert Palace)': (False, False, False, 0x25, None, None, None, None, None, None),
              'Map (Desert Palace)': (False, False, False, 0x33, None, None, None, None, None, None),
              'Small Key (Tower of Hera)': (False, True, False, 0x24, None, None, None, None, None, None),
              'Big Key (Tower of Hera)': (False, True, False, 0x32, None, None, None, None, None, None),
              'Compass (Tower of Hera)': (False, False, False, 0x25, None, None, None, None, None, None),
              'Map (Tower of Hera)': (False, False, False, 0x33, None, None, None, None, None, None),
              'Small Key (Escape)': (False, True, False, 0x24, None, None, None, None, None, None),
              'Big Key (Escape)': (False, True, False, 0x32, None, None, None, None, None, None),
              'Map (Escape)': (False, False, False, 0x33, None, None, None, None, None, None),
              'Small Key (Agahnims Tower)': (False, True, False, 0x24, None, None, None, None, None, None),
              'Small Key (Palace of Darkness)': (False, True, False, 0x24, None, None, None, None, None, None),
              'Big Key (Palace of Darkness)': (False, True, False, 0x32, None, None, None, None, None, None),
              'Compass (Palace of Darkness)': (False, False, False, 0x25, None, None, None, None, None, None),
              'Map (Palace of Darkness)': (False, False, False, 0x33, None, None, None, None, None, None),
              'Small Key (Thieves Town)': (False, True, False, 0x24, None, None, None, None, None, None),
              'Big Key (Thieves Town)': (False, True, False, 0x32, None, None, None, None, None, None),
              'Compass (Thieves Town)': (False, False, False, 0x25, None, None, None, None, None, None),
              'Map (Thieves Town)': (False, False, False, 0x33, None, None, None, None, None, None),
              'Small Key (Skull Woods)': (False, True, False, 0x24, None, None, None, None, None, None),
              'Big Key (Skull Woods)': (False, True, False, 0x32, None, None, None, None, None, None),
              'Compass (Skull Woods)': (False, False, False, 0x25, None, None, None, None, None, None),
              'Map (Skull Woods)': (False, False, False, 0x33, None, None, None, None, None, None),
              'Small Key (Swamp Palace)': (False, True, False, 0x24, None, None, None, None, None, None),
              'Big Key (Swamp Palace)': (False, True, False, 0x32, None, None, None, None, None, None),
              'Compass (Swamp Palace)': (False, False, False, 0x25, None, None, None, None, None, None),
              'Map (Swamp Palace)': (False, False, False, 0x33, None, None, None, None, None, None),
              'Small Key (Ice Palace)': (False, True, False, 0x24, None, None, None, None, None, None),
              'Big Key (Ice Palace)': (False, True, False, 0x32, None, None, None, None, None, None),
              'Compass (Ice Palace)': (False, False, False, 0x25, None, None, None, None, None, None),
              'Map (Ice Palace)': (False, False, False, 0x33, None, None, None, None, None, None),
              'Small Key (Misery Mire)': (False, True, False, 0x24, None, None, None, None, None, None),
              'Big Key (Misery Mire)': (False, True, False, 0x32, None, None, None, None, None, None),
              'Compass (Misery Mire)': (False, False, False, 0x25, None, None, None, None, None, None),
              'Map (Misery Mire)': (False, False, False, 0x33, None, None, None, None, None, None),
              'Small Key (Turtle Rock)': (False, True, False, 0x24, None, None, None, None, None, None),
              'Big Key (Turtle Rock)': (False, True, False, 0x32, None, None, None, None, None, None),
              'Compass (Turtle Rock)': (False, False, False, 0x25, None, None, None, None, None, None),
              'Map (Turtle Rock)': (False, False, False, 0x33, None, None, None, None, None, None),
              'Small Key (Ganons Tower)': (False, True, False, 0x24, None, None, None, None, None, None),
              'Big Key (Ganons Tower)': (False, True, False, 0x32, None, None, None, None, None, None),
              'Compass (Ganons Tower)': (False, False, False, 0x25, None, None, None, None, None, None),
              'Map (Ganons Tower)': (False, False, False, 0x33, None, None, None, None, None, None)}
