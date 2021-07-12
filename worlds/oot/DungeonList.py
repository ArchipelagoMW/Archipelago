import os

from .Dungeon import Dungeon
from .Items import ItemFactory
from .Utils import data_path


dungeon_table = [
    {
        'name': 'Deku Tree',
        'boss_key':     0, 
        'small_key':    0,
        'small_key_mq': 0,
        'dungeon_item': 1,
    },
    {
        'name': 'Dodongos Cavern',
        'hint': 'Dodongo\'s Cavern',
        'boss_key':     0, 
        'small_key':    0,
        'small_key_mq': 0,
        'dungeon_item': 1,
    },
    {
        'name': 'Jabu Jabus Belly',
        'hint': 'Jabu Jabu\'s Belly',
        'boss_key':     0, 
        'small_key':    0,
        'small_key_mq': 0,
        'dungeon_item': 1,
    },
    {
        'name': 'Forest Temple',
        'boss_key':     1, 
        'small_key':    5,
        'small_key_mq': 6,
        'dungeon_item': 1,
    },
    {
        'name': 'Bottom of the Well',
        'boss_key':     0, 
        'small_key':    3,
        'small_key_mq': 2,
        'dungeon_item': 1,
    },
    {
        'name': 'Fire Temple',
        'boss_key':     1, 
        'small_key':    8,
        'small_key_mq': 5,
        'dungeon_item': 1,
    },
    {
        'name': 'Ice Cavern',
        'boss_key':     0, 
        'small_key':    0,
        'small_key_mq': 0,
        'dungeon_item': 1,
    },
    {
        'name': 'Water Temple',
        'boss_key':     1, 
        'small_key':    6,
        'small_key_mq': 2,
        'dungeon_item': 1,
    },
    {
        'name': 'Shadow Temple',
        'boss_key':     1, 
        'small_key':    5,
        'small_key_mq': 6,
        'dungeon_item': 1,
    },
    {
        'name': 'Gerudo Training Grounds',
        'boss_key':     0, 
        'small_key':    9,
        'small_key_mq': 3,
        'dungeon_item': 0,
    },
    {
        'name': 'Spirit Temple',
        'boss_key':     1, 
        'small_key':    5,
        'small_key_mq': 7,
        'dungeon_item': 1,
    },
    {
        'name': 'Ganons Castle',
        'hint': 'Ganon\'s Castle',
        'boss_key':     1, 
        'small_key':    2,
        'small_key_mq': 3,
        'dungeon_item': 0,
    },
]


def create_dungeons(ootworld):
    ootworld.dungeons = []
    for dungeon_info in dungeon_table:
        name = dungeon_info['name']
        hint = dungeon_info['hint'] if 'hint' in dungeon_info else name
        
        if ootworld.logic_rules == 'glitched':
            if not ootworld.dungeon_mq[name]:
                dungeon_json = os.path.join(data_path('Glitched World'), name + '.json')
            else:
                dungeon_json = os.path.join(data_path('Glitched World'), name + ' MQ.json')
        else:
            if not ootworld.dungeon_mq[name]:
                dungeon_json = os.path.join(data_path('World'), name + '.json')
            else:
                dungeon_json = os.path.join(data_path('World'), name + ' MQ.json')

        
        ootworld.load_regions_from_json(dungeon_json)

        boss_keys = ItemFactory(['Boss Key (%s)' % name] * dungeon_info['boss_key'], ootworld.player)
        if not ootworld.dungeon_mq[dungeon_info['name']]:
            small_keys = ItemFactory(['Small Key (%s)' % name] * dungeon_info['small_key'], ootworld.player)
        else:
            small_keys = ItemFactory(['Small Key (%s)' % name] * dungeon_info['small_key_mq'], ootworld.player)
        # small_keys = ItemFactory(['Small Key (%s)' % name] * dungeon_info['small_key'], ootworld.player)
        dungeon_items = ItemFactory(['Map (%s)' % name, 
                                     'Compass (%s)' % name] * dungeon_info['dungeon_item'], ootworld.player)
        if ootworld.shuffle_mapcompass in ['any_dungeon', 'overworld']:
            for item in dungeon_items:
                item.priority = True

        ootworld.dungeons.append(Dungeon(ootworld, name, hint, boss_keys, small_keys, dungeon_items))

