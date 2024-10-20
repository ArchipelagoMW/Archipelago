import os
import json
from collections import defaultdict
from types import SimpleNamespace
from typing import TextIO, Dict

from jinja2 import Environment, PackageLoader, select_autoescape

from GameData import GameData, ElementType, ItemType, ItemFlags

SCRIPT_DIR = os.path.join(os.path.dirname(__file__))

SPECIAL_LOCATIONS = {
    '0x84A',  # "Lash Pebble"
    '0x878',  # "Pound Cube"
    '0x88C',  # "Scoop Gem"
    '0x918',  # "Cyclone Chip"
    '0x94D',  # "Hover Jade"
    '0xA3A',  # "Mars Star"
    '0x8FF',  # "Black Crystal"
    '0x978',  # "Trident"
    '0xAA2',  # "Pretty Stone"
    '0xAA4',  # "Red Cloth"
    '0xAA3',  # "Milk"
    '0xAA1',  # "Li'l Turtle"
    # Don't currently care about large bread; see GS TLA randomizer
    # 0x901,# "Large Bread"
    '0xA20',  # "Sea God's Tear"
    '0x9F9',  # "Magma Ball"
    '0x8D4',  # "Reveal"
    '0x9AE',  # "Parch"
    '0x9BA',  # "Sand"
    '0x9FA',  # "Blaze"
    '0x90B',  # "Eclipse"
    '0x945',  # "Center Prong"
    '0x1',  # "Shaman's Rod"
    '0x2',  # "Mind Read"
    '0x3',  # "Whirlwind"
    '0x4',  # "Growth"
    '0x101',  # "Carry Stone"
    '0x102',  # "Lifting Gem"
    '0x103',  # 'Orb of Force'
    '0x104',  # 'Catch Beads'
    '0x105',  # 'Douse Drop'
    '0x106',  # 'Frost Jewel']
}


# Events and sea
EXTRA_NAMES = [
    {
        'key': 'WesternSea_RustySword',
        'value': 'WesternSea - RustySword'
    },
    {
        'key': 'WesternSea_RustySword_Two',
        'value': 'WesternSea - RustySword - Two'
    },
    {
        'key': 'EasternSea_RustyAxe',
        'value': 'EasternSea - RustyAxe'
    },
    {
        'key': 'EasternSea_RustyMace',
        'value': 'EasternSea - RustyMace'
    },
    {
        'key': 'WesternSea_RustyStaff',
        'value': 'WesternSea - RustyStaff'
    },
    {
        'key': 'Mars_Lighthouse_Doom_Dragon',
        'value': 'Mars Lighthouse - Doom Dragon Fight'
    },
    {
        'key': 'Gabombo_Statue',
        'value': 'Gabombo Statue'
    },
    {
        'key': 'Alhafra_Briggs',
        'value': 'Alhafra Briggs'
    },
    {
        'key': 'Alhafra_Prison_Briggs',
        'value': 'Alhafra Prison Briggs'
    },
    {
        'key': 'Gaia_Rock_Serpent',
        'value': 'Gaia Rock - Serpent Fight'
    },
    {
        'key': 'SeaOfTime_Poseidon',
        'value': 'Sea Of Time - Poseidon fight'
    },
    {
        'key': 'Lemurian_Ship_Aqua_Hydra',
        'value': 'Lemurian Ship - Aqua Hydra fight'
    },
    {
        'key': 'Lemurian_Ship_Engine',
        'value': 'Lemurian Ship - Engine Room'
    },
    {
        'key': 'Shaman_Village_Moapa',
        'value': 'Shaman Village - Moapa fight'
    },
    {
        'key': 'Jupiter_Lighthouse_Aeri_Agatio_and_Karst',
        'value': 'Jupiter_Lighthouse Aeri - Agatio and Karst fight'
    },
    {
        'key': 'Mars_Lighthouse_Flame_Dragons',
        'value': 'Mars Lighthouse - Flame Dragons fight'
    }
]

SPECIAL_PROGRESSIONS: defaultdict[int, str] = defaultdict(lambda: 'filler', {
    # NOTE: using strings here, because importing ItemClassification from BaseClasses will cause a circular import
65:'progression',#    ItemName.Shamans_Rod
458:'progression',#    ItemName.Sea_Gods_Tear
439:'progression',#    ItemName.Right_Prong
448:'progression',#    ItemName.Healing_Fungus
242:'progression',#    ItemName.Black_Crystal
452:'progression',#    ItemName.Pretty_Stone
453:'progression',#    ItemName.Red_Cloth
454:'progression',#    ItemName.Milk
455:'progression',#    ItemName.Lil_Turtle
456:'progression',#    ItemName.Aquarius_Stone
440:'progression',#    ItemName.Left_Prong
451:'progression',#    ItemName.Dancing_Idol
441:'progression',#    ItemName.Center_Prong
460:'progression',#    ItemName.Magma_Ball
326:'progression',#    ItemName.Trident
244:'progression',#    ItemName.Blue_Key
243:'progression',#    ItemName.Red_Key
222:'progression',#    ItemName.Mars_Star
459:'progression',#    ItemName.Ruin_Key
443:     'useful',#     ItemName.Mysterious_Card
444:     'useful',#    ItemName.Trainers_Whip
445:     'useful',#    ItemName.Tomegathericon
# 449:     'filler',#    ItemName.Laughing_Fungus
333:     'useful',#    ItemName.Ixion_Mail
290:     'useful',#    ItemName.Hypnos_Sword
394:     'useful',#    ItemName.Clarity_Circlet
358:     'useful',#    ItemName.Fujin_Shield
279:     'useful',#    ItemName.Storm_Brand
# 231:     'filler',#    ItemName.Bone

425:'useful', # Rusty_Staff_Dracomace
426:'useful', # Rusty_Staff_GlowerStaff
427:'useful', # Rusty_Staff_GoblinsRod
417:'useful', # Rusty_Sword_CorsairsEdge
418:'useful', # Rusty_Sword_RobbersBlade
419:'useful', # Rusty_Sword_PiratesSabre
420:'useful', # Rusty_Sword_SoulBrand
424:'useful', # Rusty_Mace_HagboneMace
423:'useful', # Rusty_Mace_DemonMace
422:'useful', # Rusty_Axe_VikingAxe
421:'useful', # Rusty_Axe_CaptainsAxe

301:'useful', # Themis_Axe
340:'useful', # Full_Metal_Vest
383:'useful', # Nurses_Cap
287:'useful', # Pirates_Sword
414:'useful', # Guardian_Ring
309:'useful', # Blow_Mace
384:'useful', # Thorn_Crown
266:'useful', # Unicorn_Ring
300:'useful', # Disk_Axe
242:'useful', # Bone_Armlet
259:'useful', # Turtle_Boots
291:'useful', # Mist_Sabre
343:'useful', # Festival_Coat
334:'useful', # Phantasmal_Mail
283:'useful', # Cloud_Brand
351:'useful', # Iris_Robe
7:'useful', # Fire_Brand
371:'useful', # Jesters_Armlet
281:'useful', # Lightning_Sword
349:'useful', # Muni_Robe
311:'useful', # Thanatos_Mace
378:'useful', # Viking_Helm
26:'useful', # Masamune
366:'useful', # Spirit_Gloves
344:'useful', # Erinyes_Tunic
319:'useful', # Meditation_Rod
292:'useful', # Phaetons_Blade
388:'useful', # Alastors_Hood
10:'useful', # Sol_Blade
336:'useful', # Valkyrie_Mail

186:'useful', #Psy_Crystal
195:'useful', #Mint
193:'useful', #Apple
190:'useful', #Mist_Potion
194:'useful', #Hard_Nut
193:'useful', #Apple
191:'useful', #Power_Bread
183:'useful', #Potion
192:'useful', #Cookie
429:'useful', #Tear_Stone
196:'useful', #Lucky_Pepper
189:'useful', #Water_of_Life
437:'useful', #Orihalcon
435:'useful', #Mythril_Silver
436:'useful', #Dark_Matter
430:'useful', #Star_Dust
431:'useful', #Sylph_Feather
432:'useful', #Dragon_Skin
434:'useful', #Golem_Core
433:'useful', #Salamander_Tail
})


def main():
    env = Environment(
        loader=PackageLoader("gen"),
        autoescape=select_autoescape()
    )
    data = GameData()
    generate_location_names(env, data)
    generate_item_names(env, data)
    generate_item_data(env, data)
    generate_location_data(env, data)


def generate_location_names(env: Environment, data: GameData):
    template = env.get_template('LocationNames.py.jinja')
    # with open(os.path.join(SCRIPT_DIR, 'data', 'item_locations.json'), 'r') as loc_file:
    #     location_data = json.load(loc_file)
    # with open(os.path.join(SCRIPT_DIR, 'data', 'djinn.json'), 'r') as djinn_file:
    #     djinn_data = json.load(djinn_file, object_hook=lambda d: SimpleNamespace(**d))
    # by_id = dict()
    # for flag, locations in location_data.items():
    #     for loc in locations:
    #         if flag in SPECIAL_LOCATIONS and not loc['isKeyItem']:
    #             continue
    #         loc['flag'] = flag
    #         by_id[loc['id']] = loc
    # {y['id']: y for x in location_data.values() for y in x}
    hidden_items = []
    key_items = []
    summon_tablets = []
    major_items = []
    remainder = []
    earth_djinn = []
    water_djinn = []
    fire_djinn = []
    air_djinn = []
    events = []

    for djinn in data.raw_djinn_data:
        # d = {'key': djinn.name, 'value': djinn.name}
        if djinn.element == ElementType.Earth:
            earth_djinn.append(djinn)
        elif djinn.element == ElementType.Water:
            water_djinn.append(djinn)
        elif djinn.element == ElementType.Fire:
            fire_djinn.append(djinn)
        elif djinn.element == ElementType.Air:
            air_djinn.append(djinn)
    for event in data.events.values():
        events.append(data.location_names[event.flag])
    # names = dict()
    #
    # num_words = {
    #     1: 'One',
    #     2: 'Two',
    #     3: 'Three',
    #     4: 'Four',
    #     5: 'Five',
    #     6: 'Six',
    #     7: 'Seven',
    #     8: 'Eight',
    #     9: 'Nine',
    #     10: 'Ten'
    # }

    # for y in by_id.values():
    #     map_name = y['mapName'].replace(' ', '_').replace("'", '')
    #     item_name = y['vanillaName'].replace(' ', '_').replace("'", '').replace('???', 'Empty')
    #     key = map_name + '_' + item_name
    #     value = map_name + ' - ' + item_name
    #     count = names.get(key, 0)
    #     count += 1
    #     names[key] = count
    #     if count > 1:
    #         word = num_words[count]
    #         key = map_name + '_' + item_name + '_' + word
    #         value = map_name + ' - ' + item_name + ' ' + word
    #     d = {
    #         'key': key,
    #         'value': value
    #     }
    #     if y['isSummon']:
    #         summon_tablets.append(d)
    #     elif y['isKeyItem']:
    #         key_items.append(d)
    #     elif y['isMajorItem']:
    #         major_items.append(d)
    #     elif y['isHidden']:
    #         hidden_items.append(d)
    #     else:
    #         remainder.append(d)
    for loc_datum in data.raw_location_data:
        loc_name = data.location_names[loc_datum.flag]
        # map_name = y['mapName'].replace(' ', '_').replace("'", '')
        # item_name = y['vanillaName'].replace(' ', '_').replace("'", '').replace('???', 'Empty')
        # key = map_name + '_' + item_name
        # value = map_name + ' - ' + item_name
        # count = names.get(key, 0)
        # count += 1
        # names[key] = count
        # if count > 1:
        #     word = num_words[count]
        #     key = map_name + '_' + item_name + '_' + word
        #     value = map_name + ' - ' + item_name + ' ' + word
        # d = {
        #     'key': key,
        #     'value': value
        # }
        if loc_datum.is_summon:
            summon_tablets.append(loc_name)
        elif loc_datum.is_key_item:
            key_items.append(loc_name)
        elif loc_datum.is_major_item:
            major_items.append(loc_name)
        elif loc_datum.is_hidden:
            hidden_items.append(loc_name)
        else:
            remainder.append(loc_name)
    # TODO: need to add these locations somehow
    # remainder += EXTRA_NAMES
    with open(os.path.join(SCRIPT_DIR, 'gen', 'LocationNames.py'), 'w') as outfile:
        write_warning(outfile)
        outfile.write(template.render(hiddenItems=hidden_items, keyItems=key_items,
                                      summonTablets=summon_tablets, majorItems=major_items,
                                      remainder=remainder, earthDjinn=earth_djinn,
                                      waterDjinn=water_djinn, fireDjinn=fire_djinn,
                                      airDjinn=air_djinn, events=events))

def generate_item_names(env: Environment, data: GameData):
    template = env.get_template('ItemNames.py.jinja')

    with (open(os.path.join(SCRIPT_DIR, 'gen', 'ItemNames.py'), 'w') as outfile):
        write_warning(outfile)
        name_dict = {
            item.id: {
                'item':  item,
                'name': data.item_names[item.id]
            } for item in data.raw_item_data
        }
        events = [data.item_names[event.event_id] for event in data.events.values()]
        # TODO: add once Items.py is part of being generated
        # for djinn in data.raw_djinn_data:
        #     name_dict[djinn.id] = {'item': djinn, 'name': ItemName(djinn.id, djinn.name, djinn.name)}
        outfile.write(template.render(
            items=name_dict.values(),
            psyenergies=[data.item_names[x.id] for x in data.raw_psy_data],
            djinn=[data.item_names[x.ap_id] for x in data.raw_djinn_data],
            events=events,
            types=[x for x in ItemType if x < ItemType.Psyenergy]))

def generate_item_data(env: Environment, data: GameData):

    template = env.get_template('ItemData.py.jinja')
    with open(os.path.join(SCRIPT_DIR, 'gen', 'ItemData.py'), 'w') as outfile:
        write_warning(outfile)
        names = data.item_names
        summons = [x for x in data.raw_summon_data]
        psyenergies = [x for x in data.raw_psy_data]
        psyitems = [{'item': x, 'name': names[x.id]} for x in data.raw_item_data if x.item_type == ItemType.PsyenergyItem]
        djinns = [x for x in data.raw_djinn_data]
        # item_counts = defaultdict(lambda: 0)
        # for loc in data.raw_location_data:
        #     item_id = loc.vanilla_contents
        #     item_counts[item_id] += 1
        # print(item_counts)
        # unique_items = [{'item': x, 'name': names[x.id]} for x in data.raw_item_data if x.flags & ItemFlags.Rare]
        # gear = [{'item': x, 'name': names[x.id] } for x in data.raw_item_data if x.item_type.is_gear()]
        remainder = [{'item': x, 'name': names[x.id]} for x in data.raw_item_data if x.id != 0 and x.item_type != ItemType.PsyenergyItem]

        # for item in data.raw_item_data:
        #     if item.flags & ItemFlags.Important:
        #         SPECIAL_PROGRESSIONS.setdefault(item.id, 'progression')
        #     elif item.flags & ItemFlags.Rare:
        #         SPECIAL_PROGRESSIONS.setdefault(item.id, 'useful')

        outfile.write(template.render(
            summons=summons,
            psyenergies=psyenergies,
            psyitems=psyitems,
            djinns=djinns,
            # unique_items=unique_items,
            # gear=gear,
            remainder=remainder,
            progression=SPECIAL_PROGRESSIONS
        ))

def generate_location_data(env: Environment, data: GameData):
    template = env.get_template('LocationData.py.jinja')
    with open(os.path.join(SCRIPT_DIR, 'gen', 'LocationData.py'), 'w') as outfile:
        write_warning(outfile)
        names = data.location_names
        loc_data = data.raw_location_data
        psy_ids = {psy.id for psy in data.raw_psy_data}
        djinn_locs = data.raw_djinn_data
        summons_loc = []
        psy_locs = []
        remainder = []
        for loc in loc_data:
            if loc.is_summon:
                summons_loc.append(loc)
            elif loc.vanilla_contents in psy_ids:
                psy_locs.append(loc)
            else:
                remainder.append(loc)
        loc_type_lookup: defaultdict[int, str] = defaultdict(lambda: 'Item', {
            2722: 'Trade', #Pretty Stone
            2724: 'Trade', #Red Cloth
            2723: 'Trade', #Milk
            2721: 'Trade', #Li'l Turtle
        })
        for loc in remainder:
            if loc.is_hidden:
                loc_type_lookup[loc.id] = 'Hidden'
        outfile.write(template.render(
            summon_locations=summons_loc,
            psyenergy_locations=psy_locs,
            djinn_locations=djinn_locs,
            other_locations=remainder,
            loc_type_lookup=loc_type_lookup
        ))


def write_warning(fp: TextIO):
    fp.write(
        """# This file was generated using jinja2 from a template. If this file needs
# to be changed, either change the template, or the code leveraging the template.
""")

#

if __name__ == '__main__':
    main()
