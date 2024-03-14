import os

from .Dungeon import Dungeon
from .Utils import data_path


dungeon_table = [
    {
        'name': 'Deku Tree',
        'hint': 'the Deku Tree',
        'font_color': 'Green',
        'boss_key':     0, 
        'small_key':    0,
        'small_key_mq': 0,
        'dungeon_item': 1,
    },
    {
        'name': 'Dodongos Cavern',
        'hint': 'Dodongo\'s Cavern',
        'font_color': 'Red',
        'boss_key':     0, 
        'small_key':    0,
        'small_key_mq': 0,
        'dungeon_item': 1,
    },
    {
        'name': 'Jabu Jabus Belly',
        'hint': 'Jabu Jabu\'s Belly',
        'font_color': 'Blue',
        'boss_key':     0, 
        'small_key':    0,
        'small_key_mq': 0,
        'dungeon_item': 1,
    },
    {
        'name': 'Forest Temple',
        'hint': 'the Forest Temple',
        'font_color': 'Green',
        'boss_key':     1, 
        'small_key':    5,
        'small_key_mq': 6,
        'dungeon_item': 1,
    },
    {
        'name': 'Bottom of the Well',
        'hint': 'the Bottom of the Well',
        'font_color': 'Pink',
        'boss_key':     0, 
        'small_key':    3,
        'small_key_mq': 2,
        'dungeon_item': 1,
    },
    {
        'name': 'Fire Temple',
        'hint': 'the Fire Temple',
        'font_color': 'Red',
        'boss_key':     1, 
        'small_key':    8,
        'small_key_mq': 5,
        'dungeon_item': 1,
    },
    {
        'name': 'Ice Cavern',
        'hint': 'the Ice Cavern',
        'font_color': 'Blue',
        'boss_key':     0, 
        'small_key':    0,
        'small_key_mq': 0,
        'dungeon_item': 1,
    },
    {
        'name': 'Water Temple',
        'hint': 'the Water Temple',
        'font_color': 'Blue',
        'boss_key':     1, 
        'small_key':    6,
        'small_key_mq': 2,
        'dungeon_item': 1,
    },
    {
        'name': 'Shadow Temple',
        'hint': 'the Shadow Temple',
        'font_color': 'Pink',
        'boss_key':     1, 
        'small_key':    5,
        'small_key_mq': 6,
        'dungeon_item': 1,
    },
    {
        'name': 'Gerudo Training Ground',
        'hint': 'the Gerudo Training Ground',
        'font_color': 'Yellow',
        'boss_key':     0, 
        'small_key':    9,
        'small_key_mq': 3,
        'dungeon_item': 0,
    },
    {
        'name': 'Spirit Temple',
        'hint': 'the Spirit Temple',
        'font_color': 'Yellow',
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
        font_color = dungeon_info['font_color'] if 'font_color' in dungeon_info else 'White'
        
        if ootworld.logic_rules == 'glitchless' or ootworld.logic_rules == 'no_logic':  # ER + NL
            if not ootworld.dungeon_mq[name]:
                dungeon_json = os.path.join(data_path('World'), name + '.json')
            else:
                dungeon_json = os.path.join(data_path('World'), name + ' MQ.json')
        else:
            if not ootworld.dungeon_mq[name]:
                dungeon_json = os.path.join(data_path('Glitched World'), name + '.json')
            else:
                dungeon_json = os.path.join(data_path('Glitched World'), name + ' MQ.json')

        
        ootworld.load_regions_from_json(dungeon_json)

        # boss_keys = [ootworld.create_item(f'Boss Key ({name})') for i in range(dungeon_info['boss_key'])]
        # if not ootworld.dungeon_mq[dungeon_info['name']]:
        #     small_keys = [ootworld.create_item(f'Small Key ({name})') for i in range(dungeon_info['small_key'])]
        # else:
        #     small_keys = [ootworld.create_item(f'Small Key ({name})') for i in range(dungeon_info['small_key_mq'])]
        # dungeon_items = [ootworld.create_item(f'Map ({name})'), ootworld.create_item(f'Compass ({name})')] * dungeon_info['dungeon_item']
        # if ootworld.shuffle_mapcompass in ['any_dungeon', 'overworld']:
        #     for item in dungeon_items:
        #         item.priority = True

        ootworld.dungeons.append(Dungeon(ootworld, name, hint, font_color))

