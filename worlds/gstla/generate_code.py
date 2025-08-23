from __future__ import annotations

import os
from collections import defaultdict
from typing import TextIO, Dict, Set

from jinja2 import Environment, PackageLoader, select_autoescape

from GameData import GameData, ElementType, ItemType, ItemFlags

SCRIPT_DIR = os.path.join(os.path.dirname(__file__))


CLASSIFICATION_OVERRIDES: defaultdict[int, str] = defaultdict(lambda: 'filler', {
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
222:'progression',#    ItemName.Mythril_Bag_Mars
459:'progression',#    ItemName.Ruin_Key
# 229:'progression_skip_balancing', # ItemName.Lucky_Medal
443:     'useful',#     ItemName.Mysterious_Card
444:     'useful',#    ItemName.Trainers_Whip
445:     'useful',#    ItemName.Tomegathericon
# 449:     'filler',#    ItemName.Laughing_Fungus
# 333:     'useful',#    ItemName.Ixion_Mail
# 290:     'useful',#    ItemName.Hypnos_Sword
# 394:     'useful',#    ItemName.Clarity_Circlet
# 358:     'useful',#    ItemName.Fujin_Shield
# 279:     'useful',#    ItemName.Storm_Brand
# 231:     'filler',#    ItemName.Bone

# 425:'useful', # Rusty_Staff_Dracomace
# 426:'useful', # Rusty_Staff_GlowerStaff
# 427:'useful', # Rusty_Staff_GoblinsRod
# 417:'useful', # Rusty_Sword_CorsairsEdge
# 418:'useful', # Rusty_Sword_RobbersBlade
# 419:'useful', # Rusty_Sword_PiratesSabre
# 420:'useful', # Rusty_Sword_SoulBrand
# 424:'useful', # Rusty_Mace_HagboneMace
# 423:'useful', # Rusty_Mace_DemonMace
# 422:'useful', # Rusty_Axe_VikingAxe
# 421:'useful', # Rusty_Axe_CaptainsAxe

# 301:'useful', # Themis_Axe
# 340:'useful', # Full_Metal_Vest
# 383:'useful', # Nurses_Cap
# 287:'useful', # Pirates_Sword
# 414:'useful', # Guardian_Ring
# 309:'useful', # Blow_Mace
# 384:'useful', # Thorn_Crown
# 266:'useful', # Unicorn_Ring
# 300:'useful', # Disk_Axe
# 370:'useful', # Bone_Armlet
# 259:'useful', # Turtle_Boots
# 291:'useful', # Mist_Sabre
# 343:'useful', # Festival_Coat
# 334:'useful', # Phantasmal_Mail
# 283:'useful', # Cloud_Brand
# 351:'useful', # Iris_Robe
# 7:'useful', # Fire_Brand
# 371:'useful', # Jesters_Armlet
# 281:'useful', # Lightning_Sword
# 349:'useful', # Muni_Robe
# 311:'useful', # Thanatos_Mace
# 378:'useful', # Viking_Helm
# 26:'useful', # Masamune
# 366:'useful', # Spirit_Gloves
# 344:'useful', # Erinyes_Tunic
# 319:'useful', # Meditation_Rod
# 292:'useful', # Phaetons_Blade
# 388:'useful', # Alastors_Hood
# 10:'useful', # Sol_Blade
# 336:'useful', # Valkyrie_Mail

183:'useful', #Potion
186:'useful', #Psy_Crystal
190:'useful', #Mist_Potion
# 191:'useful', #Power_Bread
# 192:'useful', #Cookie
# 193:'useful', #Apple
# 194:'useful', #Hard_Nut
# 195:'useful', #Mint
# 196:'useful', #Lucky_Pepper
429:'useful', #Tear_Stone
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


USEFUL_ITEM_GROUPS: Dict[str, Set[int]] = {
    "useful_consumables": {
        183, # Potion
        186, # Psy Crystal
        189, # Water of Life
        190, # Mist Potion
    },
    "forge_materials": {
        x for x in range(429, 438) # Tear Stone through Orihalcon
    },
    "class_change_items": {
        x for x in range(443, 446) # Mysterious Card, Trainer's Whip, Tomagathericon
    }
}

OTHER_ITEM_GROUPS: Dict[str, Set[int]] = {
    "rusty_items": {
        x for x in range(417, 428) # Rusty Sword - Robber's Blade through Goblin's Rod
    },
    "stat_boosters": {
        x for x in range(191, 197)  # Power Bread through Lucky Pepper
    },
}


# Items that should not be part of the item data at all
EXCLUDED_ITEMS = {
    184, # Hermes' Water
    185, # Empty Bottle
    220, # Venus Star
    221, # Mercury Star
    223, # Mythril Bag (Jupiter)
    224, # Mythril Bag (Empty)
    225, # Small Jewel
    230, # Dragon's Eye
    232, # Anchor Charm
    234, # Cell Key
    235, # Boat Ticket
    237, # Mystic Draught
    245, # Mythril Bag (Mars & Jupiter)
    246, # Jupiter Star
    247, # Mars Star, 222, Mythril Bag (Mars) is actually used in the game
    450, # Signal Whistle
    457, # Large Bread
}

def main():
    env = Environment(
        loader=PackageLoader("gen"),
        autoescape=select_autoescape()
    )
    env.filters['bitwise_and'] = lambda x, y: x & y > 0
    data = GameData()
    generate_location_names(env, data)
    generate_item_names(env, data)
    generate_item_data(env, data)
    generate_location_data(env, data)


def generate_location_names(env: Environment, data: GameData):
    template = env.get_template('LocationNames.py.jinja')
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
    name_list = []

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
        name_list.append({'name': djinn.name, 'id': djinn.ap_id})
    for event in data.events.values():
        events.append(data.location_names[event.event_id])
        name_list.append({'name': data.location_names[event.event_id].py_name, 'id': event.event_id})
    for loc_datum in data.raw_location_data:
        loc_name = data.location_names[loc_datum.id]
        name_list.append({'name': loc_name.py_name, 'id': loc_datum.addr[0]})
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

    with open(os.path.join(SCRIPT_DIR, 'gen', 'InternalLocationNames.py'), 'w') as outfile:
        write_warning(outfile)
        outfile.write(template.render(hiddenItems=hidden_items, keyItems=key_items,
                                      summonTablets=summon_tablets, majorItems=major_items,
                                      remainder=remainder, earthDjinn=earth_djinn,
                                      waterDjinn=water_djinn, fireDjinn=fire_djinn,
                                      airDjinn=air_djinn, events=events,
                                      name_list=name_list))

def generate_item_names(env: Environment, data: GameData):
    template = env.get_template('ItemNames.py.jinja')

    with open(os.path.join(SCRIPT_DIR, 'gen', 'InternalItemNames.py'), 'w') as outfile:
        write_warning(outfile)
        name_dict = {
            item.id: {
                'item':  item,
                'name': data.item_names[item.id]
            } for item in data.raw_item_data if item.id not in EXCLUDED_ITEMS
        }
        name_list = [{'name': data.item_names[x.id].py_name, 'id': x.id}
                     for x in data.raw_item_data if x.id not in EXCLUDED_ITEMS]
        summons = [x for x in data.raw_summon_data]
        name_list += [{'name': x.name, 'id': x.id} for x in summons]
        events = [data.item_names[event.event_id] for event in data.events.values()]
        name_list += [{'name': data.item_names[x.id].py_name, 'id': x.id} for x in events]
        name_list += [{'name': d.name, 'id': d.ap_id} for d in data.raw_djinn_data]
        name_list += [{'name': data.item_names[p.id].py_name, 'id': p.id} for p in data.raw_psy_data]
        name_list += [{'name': c.name, 'id': c.id} for c in data.raw_character_data]
        outfile.write(template.render(
            name_list=name_list,
            summons=summons,
            items=name_dict.values(),
            psyenergies=[data.item_names[x.id] for x in data.raw_psy_data],
            djinn=[data.item_names[x.ap_id] for x in data.raw_djinn_data],
            events=events,
            characters=[data.item_names[c.id] for c in data.raw_character_data],
            types=[x for x in ItemType if x < ItemType.Psyenergy or x == ItemType.Mimic]))

def generate_item_data(env: Environment, data: GameData):

    template = env.get_template('ItemData.py.jinja')
    with open(os.path.join(SCRIPT_DIR, 'gen', 'InternalItemData.py'), 'w') as outfile:
        write_warning(outfile)
        names = data.item_names

        summons = [x for x in data.raw_summon_data]
        psyenergies = [x for x in data.raw_psy_data]
        characters = [c for c in data.raw_character_data]
        djinns = [x for x in data.raw_djinn_data]
        psyitems = []
        mimics = []
        other_prog = []
        other_useful = dict()
        other_items = dict()
        shop_only = []
        forge_only = []
        lucky_only = []
        non_vanilla = []
        vanilla_coins = []
        misc = []
        remainder = []
        vanilla_item_ids = { x.vanilla_contents for x in data.raw_location_data if x.vanilla_name != 'Mimic'}
        vanilla_item_ids.add(228) # Game Ticket
        misc_ids = {
            0, # Empty
            231, # Bone
            449, # Laughing Fungus
        }
        shop_only_ids = set()
        forge_only_ids = set()
        lucky_only_ids = set()
        for id in data.vanilla_shop_contents:
            if id not in vanilla_item_ids:
                shop_only_ids.add(id)
            vanilla_item_ids.add(id)
        for id in data.forgeable_ids:
            if id not in vanilla_item_ids:
                forge_only_ids.add(id)
            vanilla_item_ids.add(id)
        for id in data.lucky_medal_ids:
            if id not in vanilla_item_ids:
                lucky_only_ids.add(id)
            vanilla_item_ids.add(id)
        for id in data.lucky_wheels_ids:
            if id not in vanilla_item_ids:
                lucky_only_ids.add(id)
            vanilla_item_ids.add(id)
        classifications = dict(CLASSIFICATION_OVERRIDES)
        for item in data.raw_item_data:
            datum = {'item': item, 'name': names[item.id]}
            if item.id not in classifications:
                if item.item_type in {ItemType.Shirt, ItemType.Boots, ItemType.Ring}:
                    classifications[item.id] = 'useful'
                elif item.item_type in {ItemType.Armor, ItemType.Weapon, ItemType.Helm, ItemType.Shield} and item.flags & ItemFlags.Rare > 0:
                    classifications[item.id] = 'useful'
                else:
                    classifications[item.id] = 'filler'
            if item.id in EXCLUDED_ITEMS:
                continue
            elif item.is_mimic:
                mimics.append(datum)
            elif item.item_type == ItemType.PsyenergyItem:
                psyitems.append(datum)
            elif CLASSIFICATION_OVERRIDES[item.id] == 'progression':
                other_prog.append(datum)
            elif any(item.id in keys for keys in OTHER_ITEM_GROUPS.values()):
                other_items[item.id] = datum
            elif CLASSIFICATION_OVERRIDES[item.id] == 'useful':
                other_useful[item.id] = datum
            elif item.id in shop_only_ids:
                shop_only.append(datum)
            elif item.id in forge_only_ids:
                forge_only.append(datum)
            elif item.id in lucky_only_ids:
                lucky_only.append(datum)
            elif item.id > 0x8000:
                vanilla_coins.append(datum)
            elif item.id not in vanilla_item_ids:
                non_vanilla.append(datum)
            elif item.id in misc_ids:
                misc.append(datum)
            elif classifications[item.id] == 'useful':
                other_useful[item.id] = datum
            else:
                remainder.append(datum)
        useful_remainder_ids = set()
        for usefuls in USEFUL_ITEM_GROUPS.values():
            useful_remainder_ids |= usefuls
        useful_remainder_ids = {x['item'].id for x in other_useful.values()} - useful_remainder_ids
        outfile.write(template.render(
            summons=summons,
            psyenergies=psyenergies,
            psyitems=psyitems,
            djinns=djinns,
            characters=characters,
            mimics=mimics,
            other_prog=other_prog,
            misc=misc,
            other_useful=other_useful,
            useful_groups=USEFUL_ITEM_GROUPS,
            useful_remainder=useful_remainder_ids,
            other_items=other_items,
            other_groups=OTHER_ITEM_GROUPS,
            non_vanilla=non_vanilla,
            shop_only=shop_only,
            forge_only=forge_only,
            lucky_only=lucky_only,
            vanilla_coins=vanilla_coins,
            vanilla_item_ids=sorted(vanilla_item_ids),
            # unique_items=unique_items,
            # gear=gear,
            remainder=remainder,
            progression=classifications,
            events=data.events.values()
        ))

def generate_location_data(env: Environment, data: GameData):
    template = env.get_template('LocationData.py.jinja')
    with open(os.path.join(SCRIPT_DIR, 'gen', 'InternalLocationData.py'), 'w') as outfile:
        write_warning(outfile)
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
            3328: 'Character', # Contigo Isaac
            3329: 'Character', # Contigo Garet
            3330: 'Character', # Contigo Ivan
            3331: 'Character', # Contigo Mia
            3333: 'Character', # Idejima Jenna
            3334: 'Character', # Idejima Sheba
            3335: 'Character', # Kibombo Piers
        })
        for loc in remainder:
            if loc.is_hidden:
                loc_type_lookup[loc.id] = 'Hidden'
        outfile.write(template.render(
            summon_locations=summons_loc,
            psyenergy_locations=psy_locs,
            djinn_locations=djinn_locs,
            other_locations=remainder,
            events=data.events.values(),
            loc_type_lookup=loc_type_lookup,
        ))


def write_warning(fp: TextIO):
    fp.write(
        """# This file was generated using jinja2 from a template. If this file needs
# to be changed, either change the template, or the code leveraging the template.
""")

#

if __name__ == '__main__':
    main()
