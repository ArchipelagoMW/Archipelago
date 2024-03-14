import typing

from BaseClasses import Item, ItemClassification


def oot_data_to_ap_id(data, event): 
    if event or data[2] is None or data[0] == 'Shop': 
        return None
    offset = 66000
    if data[0] in ['Item', 'BossKey', 'Compass', 'Map', 'SmallKey', 'Token', 'GanonBossKey', 'HideoutSmallKey', 'Song']:
        return offset + data[2]
    else: 
        raise Exception(f'Unexpected OOT item type found: {data[0]}')


def ap_id_to_oot_data(ap_id): 
    offset = 66000
    val = ap_id - offset
    try: 
        return list(filter(lambda d: d[1][0] == 'Item' and d[1][2] == val, item_table.items()))[0]
    except IndexError: 
        raise Exception(f'Could not find desired item ID: {ap_id}')


def oot_is_item_of_type(item, item_type):
    if isinstance(item, OOTItem):
        return item.type == item_type
    if isinstance(item, str):
        return item in item_table and item_table[item][0] == item_type
    return False


class OOTItem(Item):
    game: str = "Ocarina of Time"
    type: str

    def __init__(self, name, player, data, event, force_not_advancement):
        (type, advancement, index, special) = data
        # "advancement" is True, False or None; some items are not advancement based on settings
        if force_not_advancement:
            classification = ItemClassification.useful
        elif name == "Ice Trap":
            classification = ItemClassification.trap
        elif name in {'Gold Skulltula Token', 'Triforce Piece'}:
            classification = ItemClassification.progression_skip_balancing
        elif advancement:
            classification = ItemClassification.progression
        else:
            classification = ItemClassification.filler
        super(OOTItem, self).__init__(name, classification, oot_data_to_ap_id(data, event), player)
        self.type = type
        self.index = index
        self.special = special or {}
        self.price = special.get('price', None) if special else None
        self.internal = False

    @property
    def dungeonitem(self) -> bool:
        return self.type in ['SmallKey', 'HideoutSmallKey', 'BossKey', 'GanonBossKey', 'Map', 'Compass']


# Progressive: True  -> Advancement
#              False -> Priority
#              None  -> Normal
#    Item:                                            (type, Progressive, GetItemID, special),
item_table = {
    'Bombs (5)':                                       ('Item',     None,  0x01, {'junk': 8}),
    'Deku Nuts (5)':                                   ('Item',     None,  0x02, {'junk': 5}),
    'Bombchus (10)':                                   ('Item',     True,  0x03, None),
    'Boomerang':                                       ('Item',     True,  0x06, None),
    'Deku Stick (1)':                                  ('Item',     None,  0x07, {'junk': 5}),
    'Lens of Truth':                                   ('Item',     True,  0x0A, None),
    'Megaton Hammer':                                  ('Item',     True,  0x0D, None),
    'Cojiro':                                          ('Item',     True,  0x0E, {'trade': True}),
    'Bottle':                                          ('Item',     True,  0x0F, {'bottle': float('Inf')}),
    'Bottle with Milk':                                ('Item',     True,  0x14, {'bottle': float('Inf')}),
    'Rutos Letter':                                    ('Item',     True,  0x15, None),
    'Deliver Letter':                                  ('Item',     True,  None, {'bottle': float('Inf')}),
    'Sell Big Poe':                                    ('Item',     True,  None, {'bottle': float('Inf')}),
    'Magic Bean':                                      ('Item',     True,  0x16, {'progressive': 10}),
    'Skull Mask':                                      ('Item',     True,  0x17, {'trade': True}),
    'Spooky Mask':                                     ('Item',     None,  0x18, {'trade': True}),
    'Keaton Mask':                                     ('Item',     None,  0x1A, {'trade': True}),
    'Bunny Hood':                                      ('Item',     None,  0x1B, {'trade': True}),
    'Mask of Truth':                                   ('Item',     True,  0x1C, {'trade': True}),
    'Pocket Egg':                                      ('Item',     True,  0x1D, {'trade': True}),
    'Pocket Cucco':                                    ('Item',     True,  0x1E, {'trade': True}),
    'Odd Mushroom':                                    ('Item',     True,  0x1F, {'trade': True}),
    'Odd Potion':                                      ('Item',     True,  0x20, {'trade': True}),
    'Poachers Saw':                                    ('Item',     True,  0x21, {'trade': True}),
    'Broken Sword':                                    ('Item',     True,  0x22, {'trade': True}),
    'Prescription':                                    ('Item',     True,  0x23, {'trade': True}),
    'Eyeball Frog':                                    ('Item',     True,  0x24, {'trade': True}),
    'Eyedrops':                                        ('Item',     True,  0x25, {'trade': True}),
    'Claim Check':                                     ('Item',     True,  0x26, {'trade': True}),
    'Kokiri Sword':                                    ('Item',     True,  0x27, None),
    'Giants Knife':                                    ('Item',     True,  0x28, None),
    'Deku Shield':                                     ('Item',     None,  0x29, None),
    'Hylian Shield':                                   ('Item',     None,  0x2A, None),
    'Mirror Shield':                                   ('Item',     True,  0x2B, None),
    'Goron Tunic':                                     ('Item',     True,  0x2C, None),
    'Zora Tunic':                                      ('Item',     True,  0x2D, None),
    'Iron Boots':                                      ('Item',     True,  0x2E, None),
    'Hover Boots':                                     ('Item',     True,  0x2F, None),
    'Stone of Agony':                                  ('Item',     True,  0x39, None),
    'Gerudo Membership Card':                          ('Item',     True,  0x3A, None),
    'Heart Container':                                 ('Item',     True,  0x3D, {'alias': ('Piece of Heart', 4), 'progressive': float('Inf')}),
    'Piece of Heart':                                  ('Item',     True,  0x3E, {'progressive': float('Inf')}),
    'Boss Key':                                        ('BossKey',  True,  0x3F, None),
    'Compass':                                         ('Compass',  None,  0x40, None),
    'Map':                                             ('Map',      None,  0x41, None),
    'Small Key':                                       ('SmallKey', True,  0x42, {'progressive': float('Inf')}),
    'Weird Egg':                                       ('Item',     True,  0x47, {'trade': True}),
    'Recovery Heart':                                  ('Item',     None,  0x48, {'junk': 0}),
    'Arrows (5)':                                      ('Item',     None,  0x49, {'junk': 8}),
    'Arrows (10)':                                     ('Item',     None,  0x4A, {'junk': 2}),
    'Arrows (30)':                                     ('Item',     None,  0x4B, {'junk': 0}),
    'Rupee (1)':                                       ('Item',     None,  0x4C, {'junk': -1}),
    'Rupees (5)':                                      ('Item',     None,  0x4D, {'junk': 10}),
    'Rupees (20)':                                     ('Item',     None,  0x4E, {'junk': 4}),
    'Milk':                                            ('Item',     None,  0x50, None),
    'Goron Mask':                                      ('Item',     None,  0x51, None),
    'Zora Mask':                                       ('Item',     None,  0x52, None),
    'Gerudo Mask':                                     ('Item',     None,  0x53, None),
    'Rupees (50)':                                     ('Item',     None,  0x55, {'junk': 1}),
    'Rupees (200)':                                    ('Item',     None,  0x56, {'junk': 0}),
    'Biggoron Sword':                                  ('Item',     True,  0x57, None),
    'Fire Arrows':                                     ('Item',     True,  0x58, None),
    'Ice Arrows':                                      ('Item',     True,  0x59, None),
    'Light Arrows':                                    ('Item',     True,  0x5A, None),
    'Gold Skulltula Token':                            ('Token',    True,  0x5B, {'progressive': float('Inf')}),
    'Dins Fire':                                       ('Item',     True,  0x5C, None),
    'Nayrus Love':                                     ('Item',     True,  0x5E, None),
    'Farores Wind':                                    ('Item',     True,  0x5D, None),
    'Deku Nuts (10)':                                  ('Item',     None,  0x64, {'junk': 0}),
    'Bombs (10)':                                      ('Item',     None,  0x66, {'junk': 2}),
    'Bombs (20)':                                      ('Item',     None,  0x67, {'junk': 0}),
    'Deku Seeds (30)':                                 ('Item',     None,  0x69, {'junk': 5}),
    'Bombchus (5)':                                    ('Item',     True,  0x6A, None),
    'Bombchus (20)':                                   ('Item',     True,  0x6B, None),
    'Rupee (Treasure Chest Game)':                     ('Item',     None,  0x72, None),
    'Piece of Heart (Treasure Chest Game)':            ('Item',     True,  0x76, {'alias': ('Piece of Heart', 1), 'progressive': float('Inf')}),
    'Ice Trap':                                        ('Item',     None,  0x7C, {'junk': 0}),
    'Progressive Hookshot':                            ('Item',     True,  0x80, {'progressive': 2}),
    'Progressive Strength Upgrade':                    ('Item',     True,  0x81, {'progressive': 3}),
    'Bomb Bag':                                        ('Item',     True,  0x82, None),
    'Bow':                                             ('Item',     True,  0x83, None),
    'Slingshot':                                       ('Item',     True,  0x84, None),
    'Progressive Wallet':                              ('Item',     True,  0x85, {'progressive': 3}),
    'Progressive Scale':                               ('Item',     True,  0x86, {'progressive': 2}),
    'Deku Nut Capacity':                               ('Item',     None,  0x87, None),
    'Deku Stick Capacity':                             ('Item',     None,  0x88, None),
    'Bombchus':                                        ('Item',     True,  0x89, None),
    'Magic Meter':                                     ('Item',     True,  0x8A, None),
    'Ocarina':                                         ('Item',     True,  0x8B, None),
    'Bottle with Red Potion':                          ('Item',     True,  0x8C, {'bottle': True, 'shop_object': 0x0F}),
    'Bottle with Green Potion':                        ('Item',     True,  0x8D, {'bottle': True, 'shop_object': 0x0F}),
    'Bottle with Blue Potion':                         ('Item',     True,  0x8E, {'bottle': True, 'shop_object': 0x0F}),
    'Bottle with Fairy':                               ('Item',     True,  0x8F, {'bottle': True, 'shop_object': 0x0F}),
    'Bottle with Fish':                                ('Item',     True,  0x90, {'bottle': True, 'shop_object': 0x0F}),
    'Bottle with Blue Fire':                           ('Item',     True,  0x91, {'bottle': True, 'shop_object': 0x0F}),
    'Bottle with Bugs':                                ('Item',     True,  0x92, {'bottle': True, 'shop_object': 0x0F}),
    'Bottle with Big Poe':                             ('Item',     True,  0x93, {'shop_object': 0x0F}),
    'Bottle with Poe':                                 ('Item',     True,  0x94, {'bottle': True, 'shop_object': 0x0F}),
    'Boss Key (Forest Temple)':                        ('BossKey',  True,  0x95, None),
    'Boss Key (Fire Temple)':                          ('BossKey',  True,  0x96, None),
    'Boss Key (Water Temple)':                         ('BossKey',  True,  0x97, None),
    'Boss Key (Spirit Temple)':                        ('BossKey',  True,  0x98, None),
    'Boss Key (Shadow Temple)':                        ('BossKey',  True,  0x99, None),
    'Boss Key (Ganons Castle)':                   ('GanonBossKey',  True,  0x9A, None),
    'Compass (Deku Tree)':                             ('Compass', False,  0x9B, None),
    'Compass (Dodongos Cavern)':                       ('Compass', False,  0x9C, None),
    'Compass (Jabu Jabus Belly)':                      ('Compass', False,  0x9D, None),
    'Compass (Forest Temple)':                         ('Compass', False,  0x9E, None),
    'Compass (Fire Temple)':                           ('Compass', False,  0x9F, None),
    'Compass (Water Temple)':                          ('Compass', False,  0xA0, None),
    'Compass (Spirit Temple)':                         ('Compass', False,  0xA1, None),
    'Compass (Shadow Temple)':                         ('Compass', False,  0xA2, None),
    'Compass (Bottom of the Well)':                    ('Compass', False,  0xA3, None),
    'Compass (Ice Cavern)':                            ('Compass', False,  0xA4, None),
    'Map (Deku Tree)':                                 ('Map',     False,  0xA5, None),
    'Map (Dodongos Cavern)':                           ('Map',     False,  0xA6, None),
    'Map (Jabu Jabus Belly)':                          ('Map',     False,  0xA7, None),
    'Map (Forest Temple)':                             ('Map',     False,  0xA8, None),
    'Map (Fire Temple)':                               ('Map',     False,  0xA9, None),
    'Map (Water Temple)':                              ('Map',     False,  0xAA, None),
    'Map (Spirit Temple)':                             ('Map',     False,  0xAB, None),
    'Map (Shadow Temple)':                             ('Map',     False,  0xAC, None),
    'Map (Bottom of the Well)':                        ('Map',     False,  0xAD, None),
    'Map (Ice Cavern)':                                ('Map',     False,  0xAE, None),
    'Small Key (Forest Temple)':                       ('SmallKey', True,  0xAF, {'progressive': float('Inf')}),
    'Small Key (Fire Temple)':                         ('SmallKey', True,  0xB0, {'progressive': float('Inf')}),
    'Small Key (Water Temple)':                        ('SmallKey', True,  0xB1, {'progressive': float('Inf')}),
    'Small Key (Spirit Temple)':                       ('SmallKey', True,  0xB2, {'progressive': float('Inf')}),
    'Small Key (Shadow Temple)':                       ('SmallKey', True,  0xB3, {'progressive': float('Inf')}),
    'Small Key (Bottom of the Well)':                  ('SmallKey', True,  0xB4, {'progressive': float('Inf')}),
    'Small Key (Gerudo Training Ground)':              ('SmallKey', True,  0xB5, {'progressive': float('Inf')}),
    'Small Key (Thieves Hideout)':              ('HideoutSmallKey', True,  0xB6, {'progressive': float('Inf')}),
    'Small Key (Ganons Castle)':                       ('SmallKey', True,  0xB7, {'progressive': float('Inf')}),
    'Double Defense':                                  ('Item',     None,  0xB8, None),
    'Buy Magic Bean':                                  ('Item',     True,  0x16, {'alias': ('Magic Bean', 10), 'progressive': 10}),
    'Magic Bean Pack':                                 ('Item',     True,  0xC9, {'alias': ('Magic Bean', 10), 'progressive': 10}),
    'Triforce Piece':                                  ('Item',     True,  0xCA, {'progressive': float('Inf')}),
    'Zeldas Letter':                                   ('Item',     True,  0x0B, {'trade': True}),
    'Time Travel':                                     ('Event',    True,  None, None),
    'Scarecrow Song':                                  ('Event',    True,  None, None),
    'Triforce':                                        ('Event',    True,  None, None),

    # Event items otherwise generated by generic event logic
    # can be defined here to enforce their appearance in playthroughs.
    'Water Temple Clear':               ('Event',    True,  None, None),
    'Forest Trial Clear':               ('Event',    True,  None, None),
    'Fire Trial Clear':                 ('Event',    True,  None, None),
    'Water Trial Clear':                ('Event',    True,  None, None),
    'Shadow Trial Clear':               ('Event',    True,  None, None),
    'Spirit Trial Clear':               ('Event',    True,  None, None),
    'Light Trial Clear':                ('Event',    True,  None, None),

    'Deku Stick Drop':                  ('Drop',     True,  None, None),
    'Deku Nut Drop':                    ('Drop',     True,  None, None),
    'Blue Fire':                        ('Drop',     True,  None, None),
    'Fairy':                            ('Drop',     True,  None, None),
    'Fish':                             ('Drop',     True,  None, None),
    'Bugs':                             ('Drop',     True,  None, None),
    'Big Poe':                          ('Drop',     True,  None, None),
    'Bombchu Drop':                     ('Drop',     True,  None, None),
    'Deku Shield Drop':                 ('Drop',     True,  None, None),

    # Consumable refills defined mostly to placate 'starting with' options
    'Arrows':                           ('Refill',   None,  None, None),
    'Bombs':                            ('Refill',   None,  None, None),
    'Deku Seeds':                       ('Refill',   None,  None, None),
    'Deku Sticks':                      ('Refill',   None,  None, None),
    'Deku Nuts':                        ('Refill',   None,  None, None),
    'Rupees':                           ('Refill',   None,  None, None),

    'Minuet of Forest':                 ('Song',     True,  0xBB,
                                            {
                                                'text_id': 0x73,
                                                'song_id': 0x02,
                                                'item_id': 0x5A,
                                            }),
    'Bolero of Fire':                   ('Song',     True,  0xBC,
                                            {
                                                'text_id': 0x74,
                                                'song_id': 0x03,
                                                'item_id': 0x5B,
                                            }),
    'Serenade of Water':                ('Song',     True,  0xBD,
                                            {
                                                'text_id': 0x75,
                                                'song_id': 0x04,
                                                'item_id': 0x5C,
                                            }),
    'Requiem of Spirit':                ('Song',     True,  0xBE,
                                            {
                                                'text_id': 0x76,
                                                'song_id': 0x05,
                                                'item_id': 0x5D,
                                            }),
    'Nocturne of Shadow':               ('Song',     True,  0xBF,
                                            {
                                                'text_id': 0x77,
                                                'song_id': 0x06,
                                                'item_id': 0x5E,
                                            }),
    'Prelude of Light':                 ('Song',     True,  0xC0,
                                            {
                                                'text_id': 0x78,
                                                'song_id': 0x07,
                                                'item_id': 0x5F,
                                            }),
    'Zeldas Lullaby':                   ('Song',     True,  0xC1,
                                            {
                                                'text_id': 0xD4,
                                                'song_id': 0x0A,
                                                'item_id': 0x60,
                                            }),
    'Eponas Song':                      ('Song',     True,  0xC2,
                                            {
                                                'text_id': 0xD2,
                                                'song_id': 0x09,
                                                'item_id': 0x61,
                                            }),
    'Sarias Song':                      ('Song',     True,  0xC3,
                                            {
                                                'text_id': 0xD1,
                                                'song_id': 0x08,
                                                'item_id': 0x62,
                                            }),
    'Suns Song':                        ('Song',     True,  0xC4,
                                            {
                                                'text_id': 0xD3,
                                                'song_id': 0x0B,
                                                'item_id': 0x63,
                                            }),
    'Song of Time':                     ('Song',     True,  0xC5,
                                            {
                                                'text_id': 0xD5,
                                                'song_id': 0x0C,
                                                'item_id': 0x64,
                                            }),
    'Song of Storms':                   ('Song',     True,  0xC6,
                                            {
                                                'text_id': 0xD6,
                                                'song_id': 0x0D,
                                                'item_id': 0x65,
                                            }),

    'Small Key Ring (Forest Temple)':                  ('SmallKey', True,  0xCB, {'alias': ('Small Key (Forest Temple)', 10), 'progressive': float('Inf')}),
    'Small Key Ring (Fire Temple)':                    ('SmallKey', True,  0xCC, {'alias': ('Small Key (Fire Temple)', 10), 'progressive': float('Inf')}),
    'Small Key Ring (Water Temple)':                   ('SmallKey', True,  0xCD, {'alias': ('Small Key (Water Temple)', 10), 'progressive': float('Inf')}),
    'Small Key Ring (Spirit Temple)':                  ('SmallKey', True,  0xCE, {'alias': ('Small Key (Spirit Temple)', 10), 'progressive': float('Inf')}),
    'Small Key Ring (Shadow Temple)':                  ('SmallKey', True,  0xCF, {'alias': ('Small Key (Shadow Temple)', 10), 'progressive': float('Inf')}),
    'Small Key Ring (Bottom of the Well)':             ('SmallKey', True,  0xD0, {'alias': ('Small Key (Bottom of the Well)', 10), 'progressive': float('Inf')}),
    'Small Key Ring (Gerudo Training Ground)':         ('SmallKey', True,  0xD1, {'alias': ('Small Key (Gerudo Training Ground)', 10), 'progressive': float('Inf')}),
    'Small Key Ring (Thieves Hideout)':         ('HideoutSmallKey', True,  0xD2, {'alias': ('Small Key (Thieves Hideout)', 10), 'progressive': float('Inf')}),
    'Small Key Ring (Ganons Castle)':                  ('SmallKey', True,  0xD3, {'alias': ('Small Key (Ganons Castle)', 10), 'progressive': float('Inf')}),

    'Buy Deku Nut (5)':                 ('Shop',     True,  0x00, {'object': 0x00BB, 'price': 15}),
    'Buy Arrows (30)':                  ('Shop',     False, 0x01, {'object': 0x00D8, 'price': 60}),
    'Buy Arrows (50)':                  ('Shop',     False, 0x02, {'object': 0x00D8, 'price': 90}),
    'Buy Bombs (5) for 25 Rupees':      ('Shop',     False, 0x03, {'object': 0x00CE, 'price': 25}),
    'Buy Deku Nut (10)':                ('Shop',     True,  0x04, {'object': 0x00BB, 'price': 30}),
    'Buy Deku Stick (1)':               ('Shop',     True,  0x05, {'object': 0x00C7, 'price': 10}),
    'Buy Bombs (10)':                   ('Shop',     False, 0x06, {'object': 0x00CE, 'price': 50}),
    'Buy Fish':                         ('Shop',     True,  0x07, {'object': 0x00F4, 'price': 200}),
    'Buy Red Potion for 30 Rupees':     ('Shop',     False, 0x08, {'object': 0x00EB, 'price': 30}),
    'Buy Green Potion':                 ('Shop',     False, 0x09, {'object': 0x00EB, 'price': 30}),
    'Buy Blue Potion':                  ('Shop',     False, 0x0A, {'object': 0x00EB, 'price': 100}),
    'Buy Hylian Shield':                ('Shop',     True,  0x0C, {'object': 0x00DC, 'price': 80}),
    'Buy Deku Shield':                  ('Shop',     True,  0x0D, {'object': 0x00CB, 'price': 40}),
    'Buy Goron Tunic':                  ('Shop',     True,  0x0E, {'object': 0x00F2, 'price': 200}),
    'Buy Zora Tunic':                   ('Shop',     True,  0x0F, {'object': 0x00F2, 'price': 300}),
    'Buy Heart':                        ('Shop',     False, 0x10, {'object': 0x00B7, 'price': 10}),
    'Buy Bombchu (10)':                 ('Shop',     True,  0x15, {'object': 0x00D9, 'price': 99}),
    'Buy Bombchu (20)':                 ('Shop',     True,  0x16, {'object': 0x00D9, 'price': 180}),
    'Buy Bombchu (5)':                  ('Shop',     True,  0x18, {'object': 0x00D9, 'price': 60}),
    'Buy Deku Seeds (30)':              ('Shop',     False, 0x1D, {'object': 0x0119, 'price': 30}),
    'Sold Out':                         ('Shop',     False, 0x26, {'object': 0x0148}),
    'Buy Blue Fire':                    ('Shop',     True,  0x27, {'object': 0x0173, 'price': 300}),
    'Buy Bottle Bug':                   ('Shop',     True,  0x28, {'object': 0x0174, 'price': 50}),
    'Buy Poe':                          ('Shop',     False, 0x2A, {'object': 0x0176, 'price': 30}),
    'Buy Fairy\'s Spirit':              ('Shop',     True,  0x2B, {'object': 0x0177, 'price': 50}),
    'Buy Arrows (10)':                  ('Shop',     False, 0x2C, {'object': 0x00D8, 'price': 20}),
    'Buy Bombs (20)':                   ('Shop',     False, 0x2D, {'object': 0x00CE, 'price': 80}),
    'Buy Bombs (30)':                   ('Shop',     False, 0x2E, {'object': 0x00CE, 'price': 120}),
    'Buy Bombs (5) for 35 Rupees':      ('Shop',     False, 0x2F, {'object': 0x00CE, 'price': 35}),
    'Buy Red Potion for 40 Rupees':     ('Shop',     False, 0x30, {'object': 0x00EB, 'price': 40}),
    'Buy Red Potion for 50 Rupees':     ('Shop',     False, 0x31, {'object': 0x00EB, 'price': 50}),

    'Kokiri Emerald':                   ('DungeonReward',    True,  None,
                                            {
                                                'stone':      True,
                                                'addr2_data': 0x80,
                                                'bit_mask':   0x00040000,
                                                'item_id':    0x6C,
                                                'actor_type': 0x13,
                                                'object_id':  0x00AD,
                                            }),
    'Goron Ruby':                       ('DungeonReward',    True,  None,
                                            {
                                                'stone':      True,
                                                'addr2_data': 0x81,
                                                'bit_mask':   0x00080000,
                                                'item_id':    0x6D,
                                                'actor_type': 0x14,
                                                'object_id':  0x00AD,
                                            }),
    'Zora Sapphire':                    ('DungeonReward',    True,  None,
                                            {
                                                'stone':      True,
                                                'addr2_data': 0x82,
                                                'bit_mask':   0x00100000,
                                                'item_id':    0x6E,
                                                'actor_type': 0x15,
                                                'object_id':  0x00AD,
                                            }),
    'Forest Medallion':                 ('DungeonReward',    True,  None,
                                            {
                                                'medallion':  True,
                                                'addr2_data': 0x3E,
                                                'bit_mask':   0x00000001,
                                                'item_id':    0x66,
                                                'actor_type': 0x0B,
                                                'object_id':  0x00BA,
                                            }),
    'Fire Medallion':                   ('DungeonReward',    True,  None,
                                            {
                                                'medallion':  True,
                                                'addr2_data': 0x3C,
                                                'bit_mask':   0x00000002,
                                                'item_id':    0x67,
                                                'actor_type': 0x09,
                                                'object_id':  0x00BA,
                                            }),
    'Water Medallion':                  ('DungeonReward',    True,  None,
                                            {
                                                'medallion':  True,
                                                'addr2_data': 0x3D,
                                                'bit_mask':   0x00000004,
                                                'item_id':    0x68,
                                                'actor_type': 0x0A,
                                                'object_id':  0x00BA,
                                            }),
    'Spirit Medallion':                 ('DungeonReward',    True,  None,
                                            {
                                                'medallion':  True,
                                                'addr2_data': 0x3F,
                                                'bit_mask':   0x00000008,
                                                'item_id':    0x69,
                                                'actor_type': 0x0C,
                                                'object_id':  0x00BA,
                                            }),
    'Shadow Medallion':                 ('DungeonReward',    True,  None,
                                            {
                                                'medallion':  True,
                                                'addr2_data': 0x41,
                                                'bit_mask':   0x00000010,
                                                'item_id':    0x6A,
                                                'actor_type': 0x0D,
                                                'object_id':  0x00BA,
                                            }),
    'Light Medallion':                  ('DungeonReward',    True,  None,
                                            {
                                                'medallion':  True,
                                                'addr2_data': 0x40,
                                                'bit_mask':   0x00000020,
                                                'item_id':    0x6B,
                                                'actor_type': 0x0E,
                                                'object_id':  0x00BA,
                                            }),
}
