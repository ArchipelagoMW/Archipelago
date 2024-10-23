import os
import pkgutil

from . import databases
from .rewards import RewardSlot, ItemReward
from .spoilers import SpoilerRow
from .address import *
from .errors import BuildError

CUSTOM_WEAPON_ITEM_ID = 0x46  # Dummy Legend sword
CUSTOM_WEAPON_ITEM_CONST = '#item.fe_CustomWeapon'
CUSTOM_WEAPON_EQUIP_TABLE_INDEX = 0x10
CUSTOM_WEAPON_ELEMENT_TABLE_INDEX = 0x3B

_CAST_TABLE = {
    'White' : 0x0B,
    'Weak' : 0x27,
    'Flood' : 0x43,
    'Blink' : 0x04,
    'Blitz' : 0x44,
    'Nuke' : 0x30,
    'Heal' : 0x12,
    'Wall' : 0x0A,
}

_EQUIP = ['dkcecil', 'kain', 'crydia', 'tellah', 'edward', 'rosa', 'yang', 'palom', 'porom', 'pcecil', 'cid', 'arydia', 'edge', 'fusoya']
_ELEMENTS = ['fire', 'ice', 'lightning', 'dark', 'holy', 'air', 'drain', 'immune', 'poison', 'blind', 'mute', 'piggy', 'mini', 'toad', 'stone', 'swoon', 'calcify1', 'calcify2', 'berserk', 'charm', 'sleep', 'paralyze', 'float', 'curse']
_RACES = ['dragons', 'robots', 'reptiles', 'spirits', 'giants', 'slimes', 'mages', 'undead']

_PLUS_STATS = [3, 5, 10, 15, 5, 10, 15, 5]
_MINUS_STATS = [0, 0, 0, 0, -5, -10, -15, -10]
_PLUS_MINUS_PAIRS = list(zip(_PLUS_STATS, _MINUS_STATS))

_CHARACTER_TO_USERS = {
    'cecil' : ['dkcecil', 'pcecil'],
    'rydia' : ['crydia', 'arydia']
}

def _is_user(cw, character):
    return bool(set(cw.equip + cw.use).intersection(set(_CHARACTER_TO_USERS.get(character, [character]))))

def _calculate_stats_byte(*stats):
    # stats is in the order: STR, AGI, VIT, WIS, WIL
    plus_bonus = 0
    minus_bonus = 0

    def raise_error():
        raise BuildError(f"Cannot represent stats bonus: " + str(stats))

    all_minus = True
    for stat in stats:
        if stat > 0:
            if plus_bonus not in (0, plus_bonus) or stat not in _PLUS_STATS:
                raise_error()
            plus_bonus = stat
            all_minus = False
        elif stat < 0:
            if minus_bonus not in (0, minus_bonus) or stat not in _MINUS_STATS:
                raise_error()
            minus_bonus = stat

    pair = (plus_bonus, minus_bonus)
    if (pair == (0,0)):
        return 0x00

    if all_minus:
        stats_byte = _MINUS_STATS.index(minus_bonus)
    else:
        if pair not in _PLUS_MINUS_PAIRS:
            raise_error()
            
        stats_byte = _PLUS_MINUS_PAIRS.index(pair)

    for i,stat in enumerate(stats):
        bit_index = 7 - i
        if stat > 0:
            stats_byte |= (1 << bit_index)

    return stats_byte



def apply(env):
    custom_weapon = None
    if env.options.ap_data is not None and not env.options.flags.has('objective_mode_classicforge'):
        id = RewardSlot.forge_item + 0x200
        ap_item = env.options.ap_data[str(id)]
        items_dbview = databases.get_items_dbview()
        placement = items_dbview.find_one(lambda i: i.code == ap_item["item_data"]["fe_id"])
        if placement is None:
            env.meta['rewards_assignment'][RewardSlot.forge_item] = ItemReward("#item.Cure1")
        else:
            if env.options.flags.has('hero_challenge'):
                available_weapons = databases.get_custom_weapons_dbview().find_all(
                    lambda cw: not cw.disabled and _is_user(cw, env.meta['starting_character']))
                custom_weapon = env.rnd.choice(available_weapons)
            env.meta['rewards_assignment'][RewardSlot.forge_item] = ItemReward(placement.const)
    elif 'custom_weapon' in env.options.test_settings:
        custom_weapon = databases.get_custom_weapons_dbview().find_one(lambda cw: env.options.test_settings['custom_weapon'].lower() in f"{cw.name}|{cw.spoilername}".lower())
    elif env.options.flags.has('hero_challenge'):
        available_weapons = databases.get_custom_weapons_dbview().find_all(lambda cw: not cw.disabled and _is_user(cw, env.meta['starting_character']))
        custom_weapon = env.rnd.choice(available_weapons)
    elif env.options.flags.has('supersmith'):
        available_weapons = databases.get_custom_weapons_dbview().find_all(lambda cw: not cw.disabled)
        custom_weapon = env.rnd.choice(available_weapons)
    elif env.options.flags.has('altsmith'):
        items_dbview = databases.get_items_dbview()
        if env.options.flags.has('no_adamants'):
            items_dbview.refine(lambda it: it.const != '#item.AdamantArmor')
        items = items_dbview.find_all(lambda it: it.tier in [7, 8])
        smith_reward = env.rnd.choice(items)
        env.meta['rewards_assignment'][RewardSlot.forge_item] = ItemReward(smith_reward.const)
        env.spoilers.add_table("MISC", [SpoilerRow("Smithy item", smith_reward.spoilername, obscurable=True)],
            public=env.options.flags.has_any('-spoil:all', '-spoil:misc'))
    else:
        env.meta['rewards_assignment'][RewardSlot.forge_item] = ItemReward('#item.Excalibur')

    if custom_weapon is None:
        env.add_substitution('custom weapon enabled', '')
        return

    # write item name
    env.add_script(f'text(item name ${CUSTOM_WEAPON_ITEM_ID:02X}) {{{custom_weapon.name}}}')

    # write 8-byte equipment record
    gear_bytes = [0x00] * 8

    if custom_weapon.metallic:
        gear_bytes[0] |= 0x80
    if custom_weapon.throwable:
        gear_bytes[0] |= 0x40
    if custom_weapon.longrange:
        gear_bytes[0] |= 0x20
    
    gear_bytes[1] = custom_weapon.attack
    gear_bytes[2] = custom_weapon.accuracy
    gear_bytes[3] = _CAST_TABLE.get(custom_weapon.cast, 0x00)
    gear_bytes[4] = CUSTOM_WEAPON_ELEMENT_TABLE_INDEX
    
    for i,race in enumerate(_RACES):
        if getattr(custom_weapon, race):
            gear_bytes[5] |= (1 << i)
    
    gear_bytes[6] = CUSTOM_WEAPON_EQUIP_TABLE_INDEX
    if custom_weapon.twohanded:
        gear_bytes[6] |= 0x20
    if custom_weapon.arrow:
        gear_bytes[6] |= 0x40
    if custom_weapon.bow:
        gear_bytes[6] |= 0x80

    gear_bytes[7] = _calculate_stats_byte(custom_weapon.str, custom_weapon.agi, custom_weapon.vit, custom_weapon.wis, custom_weapon.wil)

    env.add_binary(UnheaderedAddress(0x79100 + CUSTOM_WEAPON_ITEM_ID * 0x08), gear_bytes, as_script=True)

    # write spell data
    env.add_binary(UnheaderedAddress(0x79070 + CUSTOM_WEAPON_ITEM_ID), [custom_weapon.spellpower], as_script=True)
    env.add_binary(UnheaderedAddress(0x7D4E0 + CUSTOM_WEAPON_ITEM_ID), [_CAST_TABLE.get(custom_weapon.cast, 0x00)], as_script=True)

    # write animation data
    env.add_binary(UnheaderedAddress(0x79E10 + CUSTOM_WEAPON_ITEM_ID * 0x04), [custom_weapon.anim0, custom_weapon.anim1, custom_weapon.anim2, custom_weapon.anim3], as_script=True)

    # write equip table entry
    equip_value = 0x0000
    for i,job in enumerate(_EQUIP):
        if job in custom_weapon.equip:
            equip_value |= (1 << i)
    env.add_binary(UnheaderedAddress(0x7A550 + CUSTOM_WEAPON_EQUIP_TABLE_INDEX * 0x02), [equip_value & 0xFF, (equip_value >> 8) & 0xFF], as_script=True)

    # write element table entry
    element_value = 0x000000
    for i,elem in enumerate(_ELEMENTS):
        if elem in custom_weapon.elements:
            element_value |= (1 << i)
    env.add_binary(UnheaderedAddress(0x7A590 + CUSTOM_WEAPON_ELEMENT_TABLE_INDEX * 0x03), [element_value & 0xFF, (element_value >> 8) & 0xFF, (element_value >> 16) & 0xFF], as_script=True)

    # set override item description
    infile = pkgutil.get_data(__name__, f"assets/item_info/custom_weapon_{custom_weapon.id:X}_description.bin")
    description_data = infile
    env.meta.setdefault('item_description_overrides', {})[CUSTOM_WEAPON_ITEM_ID] = description_data

    # write proxy item value
    env.add_script(f'patch ($21f0f8 bus) {{ {custom_weapon.proxy} }}')

    # add needed script
    env.add_file(f'scripts/custom_weapon_support.f4c')

    # assign to smith
    env.meta['rewards_assignment'][RewardSlot.forge_item] = ItemReward(CUSTOM_WEAPON_ITEM_CONST)

    # spoiler
    env.spoilers.add_table("MISC", [SpoilerRow("Supersmith weapon", custom_weapon.spoilername, obscurable=True)],
        public=env.options.flags.has_any('-spoil:all', '-spoil:misc'))
