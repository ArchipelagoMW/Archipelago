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
            advancement, priority, key, crystal, code, altar_hint, altar_credit, sickkid_credit, zora_credit, witch_credit, fluteboy_credit = item_table[item]
            if item == 'Bottle':
                # randomly fill bottle
                code = [0x16, 0x2B, 0x2C, 0x2D, 0x3C, 0x3D, 0x48][random.randint(0, 6)]
            ret.append(Item(item, advancement, priority, key, crystal, code, altar_hint, altar_credit, sickkid_credit, zora_credit, witch_credit, fluteboy_credit))
        else:
            logging.getLogger('').warning('Unknown Item: %s' % item)
            return None
    
    if singleton:
        return ret[0]
    else:
        return ret


# Format: Name: (Advancement, Priority, Key, Crystal, ItemCode, Altar Hint Text, Altar Credit Text, Sick Kid Credit Text, Zora Credit Text, Witch Credit Text, Flute Boy Credit Text)
item_table = {'Bow': (True, False, False, False, 0x0B, 'You have\nchosen the\narcher class.', 'and the D', 'Ex-Adventurer', None, None, None),
              'Book of Mudora': (True, False, False, False, 0x1D, 'This is a\nparadox?!', 'and the Paradox', 'Lazy Reader', None, None, None),
              'Hammer': (True, False, False, False, 0x09, 'stop\nhammer time!', 'and the blunt weapon', None, None, None, None),
              'Hookshot': (True, False, False, False, 0x0A, 'BOING!!!\nBOING!!!\nBOING!!!', 'and the finglonger', None, None, None, None),
              'Magic Mirror': (True, False, False, False, 0x1A, 'Isn\'t your\nreflection so\npretty?', 'and the narcissism', None, None, None, None),
              'Ocarina': (True, False, False, False, 0x14, 'Save the duck\nand fly to\nfreedom!', 'and the sequel bait', None, None, None, None),
              'Pegasus Boots': (True, False, False, False, 0x4B, 'Gotta go fast!', 'and the cowboy boots', None, None, None, None),
              'Power Glove': (True, False, False, False, 0x1B, 'Now you can\nlift weak\nstuff!', 'and the input device', None, None, None, None),
              'Cape': (True, False, False, False, 0x19, 'Wear this to\nbecome\ninvisible!', 'and the invisicloak', None, None, None, None),
              'Mushroom': (True, False, False, False, 0x29, 'I\'m a fun guy!\n\nI\'m a funghi!', 'and the drugs', None, None, None, None),
              'Shovel': (True, False, False, False, 0x13, 'Can\n   You\n      Dig it?', 'and the fetch quest', None, None, None, None),
              'Lamp': (True, False, False, False, 0x12, 'Baby, baby,\nbaby.\nLight my way!', 'and the light source', None, None, None, None),
              'Magic Powder': (True, False, False, False, 0x0D, 'you can turn\nanti-faeries\ninto fairies', 'and the sprinkles', None, None, None, None),
              'Moon Pearl': (True, False, False, False, 0x1F, '  Bunny Link\n      be\n     gone!', 'and the debunnifier', None, None, None, None),
              'Cane of Somaria': (True, False, False, False, 0x15, 'I make blocks\nto hold down\nswitches!', 'and the red blocks', None, None, None, None),
              'Fire Rod': (True, False, False, False, 0x07, 'I\'m the hot\nrod. I make\nthings burn!', 'and the flamethrower', None, None, None, None),
              'Flippers': (True, False, False, False, 0x1E, 'fancy a swim?', 'and the toewebs', None, None, None, None),
              'Ice Rod': (True, False, False, False, 0x08, 'I\'m the cold\nrod. I make\nthings freeze!', 'and the ice machine', None, None, None, None),
              'Titans Mitts': (True, False, False, False, 0x1C, 'Now you can\nlift heavy\nstuff!', 'and Midas\' touch', None, None, None, None),
              'Ether': (True, False, False, False, 0x10, 'This magic\ncoin freezes\neverything!', 'and the fancy key', None, None, None, None),
              'Bombos': (True, False, False, False, 0x0F, 'Burn, baby,\nburn! Fear my\nring of fire!', 'and the airstrike', None, None, None, None),
              'Quake': (True, False, False, False, 0x11, 'Maxing out the\nRichter scale\nis what I do!', 'and the fancy key', None, None, None, None),
              'Bottle': (True, False, False, False, 0xFF, 'Now you can\nstore potions\nand stuff!', 'and the bee storage', None, None, None, None),  # specific content written on creation
              'Master Sword': (True, False, False, False, 0x50, 'I beat barries and pigs alike', 'and excalibur', None, None, None, None),
              'Tempered Sword': (True, False, False, False, 0x02, 'I stole the\nblacksmith\'s\njob!', 'and the forged bread', None, None, None, None),
              'Fighter Sword': (True, False, False, False, 0x49, 'A pathetic\nsword rests\nhere!', 'and the butter knife', None, None, None, None),
              'Golden Sword': (True, False, False, False, 0x03, 'The butter\nsword rests\nhere!', 'and the butter stick', None, None, None, None),
              'Progressive Sword': (True, False, False, False, 0x5E, 'a better copy\nof your sword\nfor your time', 'and the poke upgrade', None, None, None, None),
              'Progressive Glove': (True, False, False, False, 0x61, 'a way to lift\nheavier things', 'and the lift upgrade', None, None, None, None),
              'Silver Arrows': (True, False, False, False, 0x58, 'Do you fancy\nsilver tipped\narrows?', 'and the pig remover', None, None, None, None),
              'Green Pendant': (True, False, False, True, [0x04, 0x38, 0x62, 0x00, 0x69, 0x01], None, None, None, None, None, None),
              'Red Pendant': (True, False, False, True, [0x02, 0x34, 0x60, 0x00, 0x69, 0x02], None, None, None, None, None, None),
              'Blue Pendant': (True, False, False, True, [0x01, 0x32, 0x60, 0x00, 0x69, 0x03], None, None, None, None, None, None),
              'Triforce': (True, False, False, False, 0x6A, '\n   YOU WIN!', 'and the triforce', None, None, None, None),
              'Power Star': (True, False, False, False, 0x6B, 'a small victory', 'and the power star', None, None, None, None),
              'Triforce Piece': (True, False, False, False, 0x6C, 'a small victory', 'and the thirdforce', None, None, None, None),
              'Crystal 1': (True, False, False, True, [0x02, 0x34, 0x64, 0x40, 0x7F, 0x06], None, None, None, None, None, None),
              'Crystal 2': (True, False, False, True, [0x10, 0x34, 0x64, 0x40, 0x79, 0x06], None, None, None, None, None, None),
              'Crystal 3': (True, False, False, True, [0x40, 0x34, 0x64, 0x40, 0x6C, 0x06], None, None, None, None, None, None),
              'Crystal 4': (True, False, False, True, [0x20, 0x34, 0x64, 0x40, 0x6D, 0x06], None, None, None, None, None, None),
              'Crystal 5': (True, False, False, True, [0x04, 0x34, 0x64, 0x40, 0x6E, 0x06], None, None, None, None, None, None),
              'Crystal 6': (True, False, False, True, [0x01, 0x34, 0x64, 0x40, 0x6F, 0x06], None, None, None, None, None, None),
              'Crystal 7': (True, False, False, True, [0x08, 0x34, 0x64, 0x40, 0x7C, 0x06], None, None, None, None, None, None),
              'Single Arrow': (False, False, False, False, 0x43, 'a lonely arrow\nsits here.', 'and the arrow', None, None, None, None),
              'Arrows (10)': (False, False, False, False, 0x44, 'This will give\nyou ten shots\nwith your bow!', 'and the arrow pack', None, None, None, None),
              'Arrow Upgrade (+10)': (False, False, False, False, 0x54, 'increase arrow\nstorage, low\nlow price', 'and the quiver', None, None, None, None),
              'Arrow Upgrade (+5)': (False, False, False, False, 0x53, 'increase arrow\nstorage, low\nlow price', 'and the quiver', None, None, None, None),
              'Single Bomb': (False, False, False, False, 0x27, 'I make things\ngo BOOM! But\njust once.', 'and the explosive', None, None, None, None),
              'Bombs (3)': (False, False, False, False, 0x28, 'I make things\ngo triple\nBOOM!!!', 'and the boombox', None, None, None, None),
              'Bomb Upgrade (+10)': (False, False, False, False, 0x52, 'increase bomb\nstorage, low\nlow price', 'and the bomb bag', None, None, None, None),
              'Bomb Upgrade (+5)': (False, False, False, False, 0x51, 'increase bomb\nstorage, low\nlow price', 'and the bomb bag', None, None, None, None),
              'Blue Mail': (False, True, False, False, 0x22, 'Now you\'re a\nblue elf!', 'and the banana hat', None, None, None, None),
              'Red Mail': (False, True, False, False, 0x23, 'Now you\'re a\nred elf!', 'and the eggplant hat', None, None, None, None),
              'Progressive Armor': (False, True, False, False, 0x60, 'time for a\nchange of\nclothes?', 'and the hurt upgrade', None, None, None, None),
              'Blue Boomerang': (False, True, False, False, 0x0C, 'No matter what\nyou do, blue\nreturns to you', 'and the bluemarang', None, None, None, None),
              'Red Boomerang': (False, True, False, False, 0x2A, 'No matter what\nyou do, red\nreturns to you', 'and the badmarang', None, None, None, None),
              'Blue Shield': (False, True, False, False, 0x04, 'Now you can\ndefend against\npebbles!', 'and the stone blocker', None, None, None, None),
              'Red Shield': (False, True, False, False, 0x05, 'Now you can\ndefend against\nfireballs!', 'and the shot blocker', None, None, None, None),
              'Mirror Shield': (False, True, False, False, 0x06, 'Now you can\ndefend against\nlasers!', 'and the laser blocker', None, None, None, None),
              'Progressive Shield': (False, True, False, False, 0x5F, 'have a better\nblocker in\nfront of you', 'and the new shield', None, None, None, None),
              'Bug Catching Net': (False, True, False, False, 0x21, 'Let\'s catch\nsome bees and\nfaeries!', 'and the bee catcher', None, None, None, None),
              'Cane of Byrna': (False, True, False, False, 0x18, 'Use this to\nbecome\ninvincible!', 'and the bad cane', None, None, None, None),
              'Boss Heart Container': (False, False, False, False, 0x3E, 'Maximum health\nincreased!\nYeah!', 'and the love', None, None, None, None),
              'Sanctuary Heart Container': (False, False, False, False, 0x3F, 'Maximum health\nincreased!\nYeah!', 'and the love', None, None, None, None),
              'Piece of Heart': (False, False, False, False, 0x17, 'Just a little\npiece of love!', 'and the love', None, None, None, None),
              'Rupee (1)': (False, False, False, False, 0x34, 'Just pocket\nchange. Move\nright along.', 'and the cash stash', None, None, None, None),
              'Rupees (5)': (False, False, False, False, 0x35, 'Just pocket\nchange. Move\nright along.', 'and the cash stash', None, None, None, None),
              'Rupees (20)': (False, False, False, False, 0x36, 'Just couch\ncash. Move\nright along.', 'and the cash stash', None, None, None, None),
              'Rupees (50)': (False, False, False, False, 0x41, 'Just couch\ncash. Move\nright along.', 'and the cash stash', None, None, None, None),
              'Rupees (100)': (False, False, False, False, 0x40, 'A rupee stash!\nHell yeah!', 'and the cash stash', None, None, None, None),
              'Rupees (300)': (False, False, False, False, 0x46, 'A rupee hoard!\nHell yeah!', 'and the cash stash', None, None, None, None),
              'Rupoor': (False, False, False, False, 0x59, 'a debt collector', None, None, None, None, None),
              'Red Clock': (False, True, False, False, 0x5B, 'a waste of time', 'and the rolex', None, None, None, None),
              'Blue Clock': (False, True, False, False, 0x5C, 'a bit of time', 'and the rolex', None, None, None, None),
              'Green Clock': (False, True, False, False, 0x5D, 'a lot of time', 'and the rolex', None, None, None, None),
              'Single RNG': (False, True, False, False, 0x62, 'something you don\'t yet have', None, None, None, None, None),
              'Multi RNG': (False, True, False, False, 0x63, 'something you may already have', None, None, None, None, None),
              'Magic Upgrade (1/2)': (True, False, False, False, 0x4E, 'Your magic\npower has been\ndoubled!', 'and the spell power', None, None, None, None),  # can be required to beat mothula in an open seed in very very rare circumstance
              'Magic Upgrade (1/4)': (True, False, False, False, 0x4F, 'Your magic\npower has been\nquadrupled!', 'and the spell power', None, None, None, None),  # can be required to beat mothula in an open seed in very very rare circumstance
              # ToDo Use dungeons specific items once they work correctly
              'Small Key (Eastern Palace)': (False, False, True, False, 0x24, None, None, None, None, None, None),
              'Big Key (Eastern Palace)': (False, False, True, False, 0x32, None, None, None, None, None, None),
              'Compass (Eastern Palace)': (False, True, False, False, 0x25, None, None, None, None, None, None),
              'Map (Eastern Palace)': (False, True, False, False, 0x33, None, None, None, None, None, None),
              'Small Key (Desert Palace)': (False, False, True, False, 0x24, None, None, None, None, None, None),
              'Big Key (Desert Palace)': (False, False, True, False, 0x32, None, None, None, None, None, None),
              'Compass (Desert Palace)': (False, True, False, False, 0x25, None, None, None, None, None, None),
              'Map (Desert Palace)': (False, True, False, False, 0x33, None, None, None, None, None, None),
              'Small Key (Tower of Hera)': (False, False, True, False, 0x24, None, None, None, None, None, None),
              'Big Key (Tower of Hera)': (False, False, True, False, 0x32, None, None, None, None, None, None),
              'Compass (Tower of Hera)': (False, True, False, False, 0x25, None, None, None, None, None, None),
              'Map (Tower of Hera)': (False, True, False, False, 0x33, None, None, None, None, None, None),
              'Small Key (Escape)': (False, False, True, False, 0x24, None, None, None, None, None, None),
              'Big Key (Escape)': (False, False, True, False, 0x32, None, None, None, None, None, None),
              'Map (Escape)': (False, True, False, False, 0x33, None, None, None, None, None, None),
              'Small Key (Agahnims Tower)': (False, False, True, False, 0x24, None, None, None, None, None, None),
              'Small Key (Palace of Darkness)': (False, False, True, False, 0x24, None, None, None, None, None, None),
              'Big Key (Palace of Darkness)': (False, False, True, False, 0x32, None, None, None, None, None, None),
              'Compass (Palace of Darkness)': (False, True, False, False, 0x25, None, None, None, None, None, None),
              'Map (Palace of Darkness)': (False, True, False, False, 0x33, None, None, None, None, None, None),
              'Small Key (Thieves Town)': (False, False, True, False, 0x24, None, None, None, None, None, None),
              'Big Key (Thieves Town)': (False, False, True, False, 0x32, None, None, None, None, None, None),
              'Compass (Thieves Town)': (False, True, False, False, 0x25, None, None, None, None, None, None),
              'Map (Thieves Town)': (False, True, False, False, 0x33, None, None, None, None, None, None),
              'Small Key (Skull Woods)': (False, False, True, False, 0x24, None, None, None, None, None, None),
              'Big Key (Skull Woods)': (False, False, True, False, 0x32, None, None, None, None, None, None),
              'Compass (Skull Woods)': (False, True, False, False, 0x25, None, None, None, None, None, None),
              'Map (Skull Woods)': (False, True, False, False, 0x33, None, None, None, None, None, None),
              'Small Key (Swamp Palace)': (False, False, True, False, 0x24, None, None, None, None, None, None),
              'Big Key (Swamp Palace)': (False, False, True, False, 0x32, None, None, None, None, None, None),
              'Compass (Swamp Palace)': (False, True, False, False, 0x25, None, None, None, None, None, None),
              'Map (Swamp Palace)': (False, True, False, False, 0x33, None, None, None, None, None, None),
              'Small Key (Ice Palace)': (False, False, True, False, 0x24, None, None, None, None, None, None),
              'Big Key (Ice Palace)': (False, False, True, False, 0x32, None, None, None, None, None, None),
              'Compass (Ice Palace)': (False, True, False, False, 0x25, None, None, None, None, None, None),
              'Map (Ice Palace)': (False, True, False, False, 0x33, None, None, None, None, None, None),
              'Small Key (Misery Mire)': (False, False, True, False, 0x24, None, None, None, None, None, None),
              'Big Key (Misery Mire)': (False, False, True, False, 0x32, None, None, None, None, None, None),
              'Compass (Misery Mire)': (False, True, False, False, 0x25, None, None, None, None, None, None),
              'Map (Misery Mire)': (False, True, False, False, 0x33, None, None, None, None, None, None),
              'Small Key (Turtle Rock)': (False, False, True, False, 0x24, None, None, None, None, None, None),
              'Big Key (Turtle Rock)': (False, False, True, False, 0x32, None, None, None, None, None, None),
              'Compass (Turtle Rock)': (False, True, False, False, 0x25, None, None, None, None, None, None),
              'Map (Turtle Rock)': (False, True, False, False, 0x33, None, None, None, None, None, None),
              'Small Key (Ganons Tower)': (False, False, True, False, 0x24, None, None, None, None, None, None),
              'Big Key (Ganons Tower)': (False, False, True, False, 0x32, None, None, None, None, None, None),
              'Compass (Ganons Tower)': (False, True, False, False, 0x25, None, None, None, None, None, None),
              'Map (Ganons Tower)': (False, True, False, False, 0x33, None, None, None, None, None, None),
              'Nothing': (False, False, False, False, 0x5A, 'Some Hot Air', 'and the Nothing', None, None, None, None),
              'Beat Agahnim 1': (True, False, False, False, None, None, None, None, None, None, None),
              'Beat Agahnim 2': (True, False, False, False, None, None, None, None, None, None, None)}
