'''
This rando unit handles the logic that assigns the locations
of keyitems, bosses, and monster-in-a-box locations, accounting 
for randomizer flags and interactions between them. The actual 
effects of these assignments are dealt with in keyitem_rando 
and boss_rando.
'''
import unicodedata

from .rewards import EmptyReward, KeyItemReward, ItemReward, AxtorReward, RewardSlot, RewardsAssignment, REWARD_SLOT_SPOILER_NAMES
from . import databases
from . import dep_checker
from . import priority_assigner
from . import util
from .spoilers import SpoilerRow

from .address import *


import math
import re
import string

DEBUG = 0
MAX_RANDOMIZATION_ATTEMPTS = 100

COMMON_BRANCHES = [
    ['#item.Magma?', 'underground'],
    ['#item.DarkCrystal?', 'moon'],
    ]

HOOK_UNDERGROUND_BRANCH = ['#item.fe_Hook?', 'kingqueen_slot', 'rubicant_slot', 'underground']

ESSENTIAL_KEY_ITEMS = {
    KeyItemReward('#item.Package')         : RewardSlot.starting_item, #'package_slot',
    KeyItemReward('#item.SandRuby')        : RewardSlot.antlion_item, #'sandruby_slot', 
    KeyItemReward('#item.Baron')           : RewardSlot.baron_inn_item, #'baron_key_slot',
    KeyItemReward('#item.TwinHarp')        : RewardSlot.toroia_hospital_item, #'twinharp_slot', 
    KeyItemReward('#item.EarthCrystal')    : RewardSlot.magnes_item, #'earth_crystal_slot',
    KeyItemReward('#item.Magma')           : RewardSlot.zot_item, #'magma_key_slot', 
    KeyItemReward('#item.Tower')           : RewardSlot.babil_boss_item, #'tower_key_slot', 
    KeyItemReward('#item.fe_Hook')         : RewardSlot.cannon_item, #'hook_slot',
    KeyItemReward('#item.Luca')            : RewardSlot.luca_item, #'luca_key_slot', 
    KeyItemReward('#item.DarkCrystal')     : RewardSlot.sealed_cave_item, #'dark_crystal_slot',
    KeyItemReward('#item.Rat')             : RewardSlot.feymarch_item, #'rat_tail_slot', 
    KeyItemReward('#item.Pan')             : RewardSlot.found_yang_item, #'pan_slot', 
    KeyItemReward('#item.Crystal')         : RewardSlot.fallen_golbez_item, #'zeromus_crystal_slot', 
    KeyItemReward('#item.Legend')          : RewardSlot.ordeals_item, #'legend_sword_slot', 
    KeyItemReward('#item.Adamant')         : RewardSlot.rat_trade_item, #'adamant_slot',
    }

NONESSENTIAL_KEY_ITEMS = {
    KeyItemReward('#item.Spoon')           : RewardSlot.pan_trade_item, #'spoon_slot',
    KeyItemReward('#item.Pink')            : None,
    }

SUMMON_QUEST_ITEMS = {
    ItemReward('#item.Sylph')              : RewardSlot.sylph_item, #'sylph_item_slot',
    ItemReward('#item.Asura')              : RewardSlot.feymarch_queen_item, #'asura_item_slot',
    ItemReward('#item.Levia')              : RewardSlot.feymarch_king_item, #'levia_item_slot',
    ItemReward('#item.Odin')               : RewardSlot.baron_throne_item, #'odin_item_slot',
    ItemReward('#item.Baham')              : RewardSlot.bahamut_item, #'baham_item_slot',
    }

MOON_BOSS_ITEMS = {
    ItemReward('#item.Murasame')           : RewardSlot.lunar_boss_1_item, #'murasame_slot',
    ItemReward('#item.CrystalSword')       : RewardSlot.lunar_boss_2_item, #'crystal_sword_slot',
    ItemReward('#item.WhiteSpear')         : RewardSlot.lunar_boss_3_item, #'white_spear_slot',
    ItemReward('#item.Ribbon_1')           : RewardSlot.lunar_boss_4_item_1, #'ribbon1_slot',
    ItemReward('#item.Ribbon_2')           : RewardSlot.lunar_boss_4_item_2, #'ribbon2_slot',
    ItemReward('#item.Masamune')           : RewardSlot.lunar_boss_5_item, #'masamune_slot',
    }

VANILLA_ITEMS = dict()
VANILLA_ITEMS.update(ESSENTIAL_KEY_ITEMS)
VANILLA_ITEMS.update(NONESSENTIAL_KEY_ITEMS)
VANILLA_ITEMS.update(SUMMON_QUEST_ITEMS)
VANILLA_ITEMS.update(MOON_BOSS_ITEMS)

ITEM_SLOTS = {
    RewardSlot.starting_item          : [],
    RewardSlot.antlion_item           : ['antlion_slot'],
    RewardSlot.fabul_item             : ['fabulgauntlet_slot'],
    RewardSlot.ordeals_item           : ['milon_slot', 'milonz_slot', 'mirrorcecil_slot'],
    RewardSlot.baron_inn_item         : ['guard_slot', 'karate_slot'],
    RewardSlot.baron_castle_item      : ['#item.Baron?', 'baigan_slot', 'kainazzo_slot'],
    RewardSlot.toroia_hospital_item   : [],
    RewardSlot.magnes_item            : ['#item.TwinHarp?', 'darkelf_slot'],
    RewardSlot.zot_item               : ['#item.EarthCrystal?', 'magus_slot', 'valvalis_slot'],
    RewardSlot.babil_boss_item        : ['underground?', 'lugae_slot'],
    RewardSlot.cannon_item            : ['underground?', '#item.Tower?', 'darkimp_slot'],
    RewardSlot.luca_item              : ['underground?', 'calbrena_slot', 'golbez_slot'],
    RewardSlot.sealed_cave_item       : ['underground?', '#item.Luca?', 'evilwall_slot'],
    RewardSlot.found_yang_item        : ['underground?'],
    RewardSlot.pan_trade_item         : ['underground?', '#item.Pan?'],
    RewardSlot.feymarch_item          : ['underground?'],
    RewardSlot.rat_trade_item         : ['#item.fe_Hook?', '#item.Rat?'],
    RewardSlot.rydias_mom_item        : ['dmist?'],
    }

SUMMON_QUEST_SLOTS = {
    RewardSlot.sylph_item             : ['underground?', '#item.Pan?'],
    RewardSlot.feymarch_queen_item    : ['underground?', 'asura_slot'],
    RewardSlot.feymarch_king_item     : ['underground?', 'leviatan_slot'],
    RewardSlot.baron_throne_item      : ['#item.Baron?', 'baigan_slot', 'odin_slot'],
    RewardSlot.bahamut_item           : ['moon?', 'bahamut_slot'],
    }

MOON_BOSS_SLOTS = {
    RewardSlot.lunar_boss_1_item      : ['moon?', 'paledim_slot'],
    RewardSlot.lunar_boss_2_item      : ['moon?', 'wyvern_slot'],
    RewardSlot.lunar_boss_3_item      : ['moon?', 'plague_slot'],
    RewardSlot.lunar_boss_4_item_1    : ['moon?', 'dlunar_slot'],
    RewardSlot.lunar_boss_4_item_2    : ['moon?', 'dlunar_slot'],
    RewardSlot.lunar_boss_5_item      : ['moon?', 'ogopogo_slot'],
    }

CHEST_ITEM_SLOTS = {
    RewardSlot.zot_chest              : [],
    RewardSlot.eblan_chest_1          : [],
    RewardSlot.eblan_chest_2          : [],
    RewardSlot.eblan_chest_3          : [],
    RewardSlot.lower_babil_chest_1    : ['underground?'],
    RewardSlot.lower_babil_chest_2    : ['underground?'],
    RewardSlot.lower_babil_chest_3    : ['underground?'],
    RewardSlot.lower_babil_chest_4    : ['underground?'],
    RewardSlot.cave_eblan_chest       : ['#item.fe_Hook?'],
    RewardSlot.upper_babil_chest      : ['#item.fe_Hook?'],
    RewardSlot.cave_of_summons_chest  : ['underground?'],
    RewardSlot.sylph_cave_chest_1     : ['underground?'],
    RewardSlot.sylph_cave_chest_2     : ['underground?'],
    RewardSlot.sylph_cave_chest_3     : ['underground?'],
    RewardSlot.sylph_cave_chest_4     : ['underground?'],
    RewardSlot.sylph_cave_chest_5     : ['underground?'],
    RewardSlot.sylph_cave_chest_6     : ['underground?'],
    RewardSlot.sylph_cave_chest_7     : ['underground?'],
    RewardSlot.giant_chest            : ['moon?'],
    RewardSlot.lunar_path_chest       : ['moon?'],
    RewardSlot.lunar_core_chest_1     : ['moon?'],
    RewardSlot.lunar_core_chest_2     : ['moon?'],
    RewardSlot.lunar_core_chest_3     : ['moon?'],
    RewardSlot.lunar_core_chest_4     : ['moon?'],
    RewardSlot.lunar_core_chest_5     : ['moon?'],
    RewardSlot.lunar_core_chest_6     : ['moon?'],
    RewardSlot.lunar_core_chest_7     : ['moon?'],
    RewardSlot.lunar_core_chest_8     : ['moon?'],
    RewardSlot.lunar_core_chest_9     : ['moon?'],
    }

CHEST_ITEM_SLOT_GROUPS = [
        [
            RewardSlot.eblan_chest_1,
            RewardSlot.eblan_chest_2,
            RewardSlot.eblan_chest_3,
        ],
        [
            RewardSlot.zot_chest,
        ],
        [
            RewardSlot.lower_babil_chest_1,
            RewardSlot.lower_babil_chest_2,
            RewardSlot.lower_babil_chest_3,
            RewardSlot.lower_babil_chest_4,
        ],
        [
            RewardSlot.cave_eblan_chest,
        ],
        [
            RewardSlot.upper_babil_chest,
        ],
        [
            RewardSlot.cave_of_summons_chest,
        ],
        [
            RewardSlot.sylph_cave_chest_1,
            RewardSlot.sylph_cave_chest_2,
            RewardSlot.sylph_cave_chest_3,
            RewardSlot.sylph_cave_chest_4,
            RewardSlot.sylph_cave_chest_5,
            RewardSlot.sylph_cave_chest_6,
            RewardSlot.sylph_cave_chest_7,
        ],
        [
            RewardSlot.giant_chest,
        ],
        [
            RewardSlot.lunar_path_chest,
        ],
        [
            RewardSlot.lunar_core_chest_1,
            RewardSlot.lunar_core_chest_2,
            RewardSlot.lunar_core_chest_3,
            RewardSlot.lunar_core_chest_4,
            RewardSlot.lunar_core_chest_5,
            RewardSlot.lunar_core_chest_6,
            RewardSlot.lunar_core_chest_7,
            RewardSlot.lunar_core_chest_8,
            RewardSlot.lunar_core_chest_9,
        ],
    ]

CHEST_NUMBERS = {
    RewardSlot.eblan_chest_1         : ['#EblanWestTower1F', 1],
    RewardSlot.eblan_chest_2         : ['#EblanEastTower2F', 3],
    RewardSlot.eblan_chest_3         : ['#EblanBasement', 2],
    RewardSlot.zot_chest             : ['#Zot2F', 0],
    RewardSlot.lower_babil_chest_1   : ['#BabilIcebrandRoom', 0],
    RewardSlot.lower_babil_chest_2   : ['#BabilBlizzardRoom', 0],
    RewardSlot.lower_babil_chest_3   : ['#BabilIceShieldRoom', 0],
    RewardSlot.lower_babil_chest_4   : ['#BabilIceMailRoom', 0],
    RewardSlot.cave_eblan_chest      : ['#CaveEblanSaveRoom', 0],
    RewardSlot.upper_babil_chest     : ['#BabilB2', 0],
    RewardSlot.cave_of_summons_chest : ['#CaveOfSummons3F', 0],
    RewardSlot.sylph_cave_chest_1    : ['#SylvanCave2F', 9],
    RewardSlot.sylph_cave_chest_2    : ['#SylvanCaveTreasury', 0],
    RewardSlot.sylph_cave_chest_3    : ['#SylvanCaveTreasury', 1],
    RewardSlot.sylph_cave_chest_4    : ['#SylvanCaveTreasury', 2],
    RewardSlot.sylph_cave_chest_5    : ['#SylvanCaveTreasury', 3],
    RewardSlot.sylph_cave_chest_6    : ['#SylvanCaveTreasury', 4],
    RewardSlot.sylph_cave_chest_7    : ['#SylvanCaveTreasury', 5],
    RewardSlot.giant_chest           : ['#GiantPassage', 0],
    RewardSlot.lunar_path_chest      : ['#LunarPassage1', 0],
    RewardSlot.lunar_core_chest_1    : ['#LunarSubterran1F', 0],
    RewardSlot.lunar_core_chest_2    : ['#LunarSubterran2F', 1],
    RewardSlot.lunar_core_chest_3    : ['#LunarSubterran4F', 1],
    RewardSlot.lunar_core_chest_4    : ['#LunarSubterran5F', 0],
    RewardSlot.lunar_core_chest_5    : ['#LunarSubterran5F', 1],
    RewardSlot.lunar_core_chest_6    : ['#LunarSubterran5F', 2],
    RewardSlot.lunar_core_chest_7    : ['#LunarSubterran5F', 3],
    RewardSlot.lunar_core_chest_8    : ['#LunarSubterran5F', 4],
    RewardSlot.lunar_core_chest_9    : ['#LunarSubterranTunnelMinerva', 0],
    }

BOSS_SLOTS = {
    'dmist_slot'            : [],
    'officer_slot'          : ['#item.Package?'],
    'octomamm_slot'         : [],
    'antlion_slot'          : [],
    'mombomb_slot'          : [],
    'fabulgauntlet_slot'    : [],
    'milon_slot'            : [],
    'milonz_slot'           : ['milon_slot'],
    'mirrorcecil_slot'      : ['milon_slot', 'milonz_slot'],
    'karate_slot'           : ['guard_slot'],
    'guard_slot'            : [],
    'baigan_slot'           : ['#item.Baron?'],
    'kainazzo_slot'         : ['#item.Baron?', 'baigan_slot'],
    'darkelf_slot'          : ['#item.TwinHarp?'],
    'magus_slot'            : [],
    'valvalis_slot'         : ['#item.EarthCrystal?', 'magus_slot'],
    'calbrena_slot'         : ['underground?'],
    'golbez_slot'           : ['underground?', 'calbrena_slot'],
    'lugae_slot'            : ['underground?'],
    'darkimp_slot'          : ['underground?', '#item.Tower?'],
    'kingqueen_slot'        : ['#item.fe_Hook?'],
    'rubicant_slot'         : ['#item.fe_Hook?', 'kingqueen_slot'],
    'evilwall_slot'         : ['underground?', '#item.Luca?'],
    'asura_slot'            : ['underground?'],
    'leviatan_slot'         : ['underground?'],
    'odin_slot'             : ['#item.Baron?', 'baigan_slot'],
    'bahamut_slot'          : ['moon?'],
    'elements_slot'         : ['moon?'],
    'cpu_slot'              : ['moon?', 'elements_slot'],
    'paledim_slot'          : ['moon?'],
    'wyvern_slot'           : ['moon?'],
    'plague_slot'           : ['moon?'],
    'dlunar_slot'           : ['moon?'],
    'ogopogo_slot'          : ['moon?'], 
    }

BOSSES = [
    'dmist',
    'officer',
    'octomamm',
    'antlion',
    'waterhag',
    'mombomb',
    'fabulgauntlet',
    'milon',
    'milonz',
    'mirrorcecil',
    'guard',
    'karate',
    'baigan',
    'kainazzo',
    'darkelf',
    'magus',
    'valvalis',
    'calbrena',
    'golbez',
    'lugae',
    'darkimp',
    'kingqueen',
    'rubicant',
    'evilwall',
    'asura',
    'leviatan',
    'odin',
    'bahamut',
    'elements',
    'cpu',
    'paledim',
    'wyvern',
    'plague',
    'dlunar',
    'ogopogo',
    ]

QUEST_REWARD_CURVES = {
    'Ungated_Quest' : [
        RewardSlot.starting_item,
        RewardSlot.antlion_item,
        RewardSlot.fabul_item,
        RewardSlot.ordeals_item,
        RewardSlot.baron_inn_item,
        RewardSlot.toroia_hospital_item,
        RewardSlot.rydias_mom_item,
    ],

    'Gated_Quest' : [
        RewardSlot.baron_castle_item,
        RewardSlot.magnes_item,
        RewardSlot.zot_item,
        RewardSlot.babil_boss_item,
        RewardSlot.cannon_item,
        RewardSlot.luca_item,
        RewardSlot.sealed_cave_item,
        RewardSlot.found_yang_item,
        RewardSlot.pan_trade_item,
        RewardSlot.feymarch_item,
        RewardSlot.rat_trade_item,
        RewardSlot.sylph_item,
        RewardSlot.feymarch_queen_item,
        RewardSlot.feymarch_king_item,
        RewardSlot.baron_throne_item,
    ],

    'Moon_Quest' : [
        RewardSlot.bahamut_item,
        RewardSlot.lunar_boss_1_item,
        RewardSlot.lunar_boss_2_item,
        RewardSlot.lunar_boss_3_item,
        RewardSlot.lunar_boss_4_item_1,
        RewardSlot.lunar_boss_4_item_2,
        RewardSlot.lunar_boss_5_item,
    ]
}

def apply(env):
    treasure_dbview = databases.get_treasure_dbview()
    treasure_dbview.refine(lambda t: not t.exclude)

    items_dbview = databases.get_items_dbview()
    if env.options.flags.has('treasure_no_j_items'):
        items_dbview.refine(lambda it: not it.j)
    if env.options.flags.has('no_adamants'):
        items_dbview.refine(lambda it: it.const != '#item.AdamantArmor')
    if env.options.flags.has('no_cursed_rings'):
        items_dbview.refine(lambda it: it.const != '#item.Cursed')

    unsafe = False
    if env.options.flags.has('key_items_unsafe'):
        unsafe = True

    keyitem_assigner = priority_assigner.PriorityAssigner()

    # slot tiers:
    #  0 - slots allowed to contain progression items, other than MIABs
    #  1 - MIABs allowed to contain progression items
    #  2 - slots without progression items but with good stuff
    #  3 - remaining slots

    # item tiers:
    #  0 - items that cannot be in MIABs under any circumstances
    #  1 - progression items
    #  2 - non-progression key items
    #  3 - good non-progression items
    #  4 - less good non-progression items

    keyitem_assigner.item_tier(0).set_max_slot_bucket(0)
    keyitem_assigner.item_tier(1).set_max_slot_bucket(1)
    keyitem_assigner.item_tier(2).set_max_slot_bucket(2)
    keyitem_assigner.item_tier(3).set_max_slot_bucket(2)

    keyitem_assigner.slot_tier(0).extend(ITEM_SLOTS)
    #if env.options.flags.has('no_free_key_item'):
    #    keyitem_assigner.slot_tier(0).remove(RewardSlot.toroia_hospital_item)
    #else:
    #    keyitem_assigner.slot_tier(0).remove(RewardSlot.rydias_mom_item)

    keyitem_assigner.item_tier(1).extend(ESSENTIAL_KEY_ITEMS)
    keyitem_assigner.item_tier(2).extend(NONESSENTIAL_KEY_ITEMS)

    if env.meta.get('has_objectives', False) and env.meta.get('zeromus_required', True):
        keyitem_assigner.item_tier(1).remove(KeyItemReward('#item.Crystal'))
        if env.options.flags.has('objective_mode_classicforge'):
            keyitem_assigner.item_tier(3).append(ItemReward('#item.Excalibur'))

    for item in env.meta.get('objective_required_key_items', []):
        reward = KeyItemReward(item)
        for item_tier in range(2, 5):
            if reward in keyitem_assigner.item_tier(item_tier):
                keyitem_assigner.item_tier(item_tier).remove(reward)
                keyitem_assigner.item_tier(1).append(reward)
                break

    keyitem_capable_fight_slots = []
    keyitem_incapable_fight_slots = []

    if env.options.flags.has('key_items_in_summon_quests'):
        keyitem_capable_fight_slots.extend(SUMMON_QUEST_SLOTS)
    else:
        keyitem_incapable_fight_slots.extend(SUMMON_QUEST_SLOTS)

    if env.options.flags.has('key_items_in_moon_bosses'):
        keyitem_capable_fight_slots.extend(MOON_BOSS_SLOTS)
    else:
        keyitem_incapable_fight_slots.extend(MOON_BOSS_SLOTS)

    env.rnd.shuffle(keyitem_capable_fight_slots)
    num_privileged_fight_slots = int(math.ceil(len(keyitem_capable_fight_slots) / 2))

    # limit the number of fight slots that may contain key items according to probability curve
    r = env.rnd.random()
    while r < 0.5:
        num_privileged_fight_slots += 1
        r *= 2.0

    keyitem_assigner.slot_tier(0).extend(keyitem_capable_fight_slots[:num_privileged_fight_slots])
    keyitem_assigner.slot_tier(2).extend(keyitem_capable_fight_slots[num_privileged_fight_slots:])

    keyitem_assigner.slot_tier(3).extend(keyitem_incapable_fight_slots)

    if env.options.flags.has('key_items_in_miabs'):
        # limit the number of MIABs that may contain key items according to probability curve
        max_good_per_area = 2
        r = env.rnd.random()
        while r < 0.5:
            max_good_per_area += 1
            r *= 2.0

        good_miabs = []
        bad_miabs = []
        for group in CHEST_ITEM_SLOT_GROUPS:
            if 'lunar_core_chest' in group[0].name and not (env.options.flags.has('key_items_in_moon_bosses') or unsafe):
                bad_miabs.extend(group)
            elif len(group) > max_good_per_area:
                group = list(group)
                env.rnd.shuffle(group)
                good_miabs.extend(group[:max_good_per_area])
                bad_miabs.extend(group[max_good_per_area:])
            else:
                good_miabs.extend(group)

        env.rnd.shuffle(good_miabs)
        bad_miabs.extend(good_miabs[:3])
        good_miabs = good_miabs[3:]

        keyitem_assigner.slot_tier(1).extend(good_miabs)
        keyitem_assigner.slot_tier(3).extend(bad_miabs)
    else:
        pass
        #keyitem_assigner.slot_tier(3).extend(CHEST_ITEM_SLOTS)
    

    if env.options.flags.has('pass_in_key_items'):
        keyitem_assigner.item_tier(1).append(ItemReward('#item.Pass'))

    ## Deprecated no_magma code, preserving in case of future implementation.
    # if env.options.flags.has('key_items_no_magma'):
    #     keyitem_assigner.item_tier(1).remove(KeyItemReward('#item.Magma'))
    #     layout = '"Package  SandRuby   [lightsword]Legend"      [[ 01 ]]\n        "[key]Baron   [harp]TwinHarp  [crystal]Earth" [[ 01 ]]\n        "         [key]Tower     Hook"            [[ 01 ]]\n        "[key]Luca    [crystal]Darkness  [tail]Rat"   [[ 01 ]]\n        "Adamant  Pan        [knife]Spoon"            [[ 01 ]]\n        "[tail]Pink    [crystal]Crystal"              [[ 00 ]]'
    #     env.add_substitution('tracker layout', layout)

    assignable_boss_slots = BOSS_SLOTS.copy()
    bosses = list(BOSSES)

    if env.options.flags.has('key_items_force_magma'):
        prevent_hook_seed = True
    elif not env.options.flags.has_any('key_items_in_summon_quests', 'key_items_in_moon_bosses', 'key_items_in_miabs') and not env.options.flags.has('key_items_force_hook'):
        prevent_hook_seed = (env.rnd.random() < 0.5)
    else:
        prevent_hook_seed = False

    # perform assignment
    attempts = 0
    found_valid_assignment = False
    while not found_valid_assignment and attempts < MAX_RANDOMIZATION_ATTEMPTS:
        boss_assignment = {}
        rewards_assignment = RewardsAssignment()

        # assign key items
        if env.options.ap_data is not None:
            for slot in RewardSlot:
                # 0x5A and 0x5D aren't applicable to AP games.
                # Rewards go up to 0x60, but the last two aren't used yet.
                skip_list = [0x5A, 0x5D, 0x5F, 0x60]
                # These three are treasure chests, so we use the treasure chest ID.
                if slot == RewardSlot.feymarch_item:
                    id = 0x13D
                elif slot == RewardSlot.lunar_boss_4_item_1:
                    id = 0x19F
                elif slot == RewardSlot.lunar_boss_4_item_2:
                    id = 0x1A0
                elif slot < 0x20 or slot in skip_list:
                    continue  # not doing characters here
                elif slot >= 0x3C and slot <= 0x58:
                    id = treasure_dbview.find_one(
                        lambda t: t.map == CHEST_NUMBERS[slot][0] and
                                  t.index == CHEST_NUMBERS[slot][1]).flag
                else:
                    id = slot + 0x200 # Reward location IDs are ingame index plus 0x200.
                if int(id) == 0x25B and env.options.flags.has('objective_mode_classicforge'):
                    # We skip Kokkol if we're on Forge the Crystal.
                    continue
                # We attempt to find the FF4 item in the slot...
                try:
                    ap_item = env.options.ap_data[str(id)]
                    placement = items_dbview.find_one(lambda i: i.code == ap_item["item_data"]["fe_id"])
                # ...and if there is none, it's a remote item, so we place a Cure1 as a placeholder
                # and let the scripting know to use the AP version of the event scripting for that slot.
                except KeyError:
                    placement = None
                if placement is None:
                    reward = ItemReward("#item.Cure1")
                    env.add_toggle(f"ap_{slot.name}")
                else:
                    reward = ItemReward(placement.const)
                script_text = env.meta["text_pointers"].pop()
                pointer = script_text[20:24]
                pointer = pointer[1:] if pointer[3] != ")" else pointer[1:3]
                env.add_script(f"consts(ap_reward_slot) {{${pointer} {slot.name}}} ")
                if ap_item["item_data"]["name"] == "Archipelago Item":
                    safe_item_name = unicodedata.normalize("NFKD", ap_item["item_name"])
                    safe_item_name = re.sub(r"[^a-zA-Z0-9`\'.\-_!?%/:,\s]", "-", safe_item_name)
                    safe_player_name = unicodedata.normalize("NFKD", ap_item["player_name"])
                    safe_player_name = re.sub(r"[^a-zA-Z0-9`\'.\-_!?%/:,\s]", "-", safe_player_name)
                    env.add_script(f'{script_text} {{Found {safe_player_name}\'s \n{safe_item_name}. }}')
                else:
                    env.add_script(f'{script_text} {{Found your own\n{placement.name}. }}')
                rewards_assignment[slot] = reward
        elif env.options.flags.has('key_items_vanilla'):
            # vanilla assignment
            rewards_assignment[RewardSlot.fabul_item] = ItemReward('#item.BlackSword')
            rewards_assignment[RewardSlot.baron_castle_item] = (ItemReward('#item.Pass') if env.options.flags.has('pass_in_key_items') else EmptyReward())

            used_keyitems = set()
            for item in ESSENTIAL_KEY_ITEMS:
                if item.item == "#item.Crystal" and env.meta.get('has_objectives', False) and env.meta.get('zeromus_required', True):
                    continue
                    
                slot = ESSENTIAL_KEY_ITEMS[item]
                if slot:
                    if env.options.flags.has('no_free_key_item') and slot == RewardSlot.toroia_hospital_item:
                        slot = RewardSlot.rydias_mom_item
                    rewards_assignment[slot] = item
                    used_keyitems.add(item.item)
            for item in NONESSENTIAL_KEY_ITEMS:
                slot = NONESSENTIAL_KEY_ITEMS[item]
                if slot:
                    rewards_assignment[slot] = item
                    used_keyitems.add(item.item)

            if not set(env.meta.get('objective_required_key_items', [])).issubset(used_keyitems):
                raise Exception("Objective required key item is not present in vanilla key item assignment.")

            remaining_slots = []
            for slot_tier in range(4):
                for slot in keyitem_assigner.slot_tier(slot_tier):
                    if slot not in rewards_assignment:
                        remaining_slots.append(slot)
        else:
            keyitem_assignment, remaining_slots, remaining_items = keyitem_assigner.assign(env.rnd)
            rewards_assignment.update(keyitem_assignment)

        # assign bosses
        if not env.options.flags.has('bosses_vanilla'):
            env.rnd.shuffle(bosses)
            while bosses[len(bosses) - 1] in env.meta["objective_required_bosses"]:
                env.rnd.shuffle(bosses)
            for i,k in enumerate(assignable_boss_slots):
                boss_assignment[k] = bosses[i]

            if 'boss' in env.options.test_settings:
                for force_slot in env.options.test_settings['boss']:
                    force_boss = env.options.test_settings['boss'][force_slot]
                    replaced_boss = boss_assignment[force_slot]
                    if force_boss != replaced_boss:
                        for k in boss_assignment:
                            if boss_assignment[k] == force_boss:
                                boss_assignment[k] = replaced_boss
                                break
                        boss_assignment[force_slot] = force_boss

        else:
            # vanilla assignment
            used_bosses = set()
            for k in assignable_boss_slots:
                boss = k.replace('_slot', '')
                boss_assignment[k] = boss
                used_bosses.add(boss)

            if not set(env.meta['objective_required_bosses']).issubset(used_bosses):
                raise Exception("Objective required boss is not present in vanilla boss assignment.")
        if DEBUG:
            print('assignment {}:'.format(attempts))
            for k in rewards_assignment:
                print('  {} <- {}'.format(str(k), rewards_assignment[k]))
            for k in boss_assignment:
                print('  {} <- {}'.format(k, boss_assignment[k]))
            print(f'remaining slots: {",".join([str(s) for s in remaining_slots])}')

        # build dependency checker
        checker = dep_checker.DepChecker()
        def add_branch_with_substitutions(*steps):
            b = []
            for step in steps:
                if step in rewards_assignment:
                    if rewards_assignment[step] != EmptyReward():
                        b.append(rewards_assignment[step].item)
                elif step in boss_assignment:
                    b.append(boss_assignment[step])
                else:
                    b.append(step)
            checker.add_branch(*b)

        for branch in COMMON_BRANCHES:
            add_branch_with_substitutions(*branch)

        if not prevent_hook_seed:
            add_branch_with_substitutions(*HOOK_UNDERGROUND_BRANCH)

        for slot in rewards_assignment:
            if rewards_assignment[slot] == EmptyReward():
                continue

            if slot in ITEM_SLOTS:
                src_branch = ITEM_SLOTS[slot]
            elif slot in SUMMON_QUEST_SLOTS:
                src_branch = SUMMON_QUEST_SLOTS[slot]
            elif slot in MOON_BOSS_SLOTS:
                src_branch = MOON_BOSS_SLOTS[slot]
            elif slot in CHEST_ITEM_SLOTS:
                src_branch = CHEST_ITEM_SLOTS[slot]

            add_branch_with_substitutions(*src_branch, rewards_assignment[slot].item)

        for slot in boss_assignment:        
            add_branch_with_substitutions(*assignable_boss_slots[slot], boss_assignment[slot])

        checker.resolve()

        # make sure key items are all obtainable
        if DEBUG:
            print('testing reachability')
        tests = []
        tests.append('dmist')

        underground_path_disallowed = []
        if not env.options.flags.has('bosses_vanilla') and not env.options.flags.has('bosses_unsafe'):
            # must be able to access underground without encountering, golbez, wyvern, valvalis or odin replacement
            # (or Dark Cecil in NFL2)
            mean_bosses = ['golbez', 'wyvern', 'valvalis', boss_assignment['odin_slot']]

            if env.options.flags.has('no_free_bosses') and 'mirrorcecil' not in mean_bosses:
                mean_bosses.append('mirrorcecil')
                
            # obscure special case: if a mean boss is in Yang's slot, and
            #  DMist is in guard slot, and DMist gates underworld, then
            #  that's bad
            if env.options.flags.has('no_free_key_item') and boss_assignment['guard_slot'] == 'dmist' and boss_assignment['karate_slot'] in mean_bosses:
                mean_bosses.append('dmist')

            underground_path_disallowed.extend(mean_bosses)

        # must be able to encounter all bosses required of forced objective flags
        tests.extend(env.meta.get('objective_required_bosses', []))

        found_valid_assignment = True
        break # We skip validation, because AP handles that for us.

        attempts += 1

    if not found_valid_assignment:
        raise Exception("Failed to find valid assignment after too many attempts; aborting")

    if DEBUG:
        result, path = checker.check('#item.Magma', without=['#item.fe_Hook'])
        print(f"Hook seed? : {not result}")


    # assign remaining treasures now since they don't have dependency concerns
    if env.options.flags.has('treasure_shuffle') or env.options.flags.has('treasure_vanilla'):
        # Tvanilla acts like Tshuffle, except that only the K categories specified partake
        # in the shuffle, and unspecifed K categories get vanilla assignment

        is_vanilla = env.options.flags.has('treasure_vanilla')
        pool = []
        if is_vanilla and not env.options.flags.has('key_items_in_summon_quests'):
            for item in SUMMON_QUEST_ITEMS:
                slot = SUMMON_QUEST_ITEMS[item]
                if slot not in rewards_assignment:
                    rewards_assignment[slot] = item
        else:
            pool.extend(SUMMON_QUEST_ITEMS)

        if is_vanilla and not env.options.flags.has('key_items_in_moon_bosses'):
            for item in MOON_BOSS_ITEMS:
                slot = MOON_BOSS_ITEMS[item]
                if slot not in rewards_assignment:
                    rewards_assignment[slot] = item
        else:
            pool.extend(MOON_BOSS_ITEMS)

        if is_vanilla and not env.options.flags.has('key_items_in_miabs'):
            for slot in CHEST_NUMBERS:
                if slot not in rewards_assignment:
                    treasure = treasure_dbview.find_one(lambda t : [t.map, t.index] == CHEST_NUMBERS[slot])
                    rewards_assignment[slot] = ItemReward(treasure.jcontents if (treasure.jcontents and not env.options.flags.has('treasure_no_j_items')) else treasure.contents)
        else:
            for slot in CHEST_NUMBERS:
                treasure = treasure_dbview.find_one(lambda t : [t.map, t.index] == CHEST_NUMBERS[slot])
                pool.append(ItemReward(treasure.jcontents if (treasure.jcontents and not env.options.flags.has('treasure_no_j_items')) else treasure.contents))

        env.rnd.shuffle(pool)
        for slot_tier in range(4):
            for slot in keyitem_assigner.slot_tier(slot_tier):
                if slot not in rewards_assignment:
                    try:          
                        rewards_assignment[slot] = pool.pop()
                    except:
                        # Pnone + win:crystal causes an issue under Tvanilla | Tshuffle. This is a workaround to that.
                        rewards_assignment[slot] = (ItemReward('#item.Cure1') if not is_vanilla else EmptyReward())
    else:
        # revised Rivers rando
        curves_dbview = databases.get_curves_dbview()

        unassigned_quest_slots = [slot for slot in (list(ITEM_SLOTS) + list(SUMMON_QUEST_SLOTS) + list(MOON_BOSS_SLOTS)) if slot not in rewards_assignment]

        if env.options.flags.has('treasure_standard') or env.options.flags.has('treasure_wild'):
            src_pool = items_dbview.find_all(lambda it: it.tier in [6, 7, 8])
            pool = list(src_pool)
            while len(pool) < len(unassigned_quest_slots):
                pool.append(env.rnd.choice(src_pool))
            env.rnd.shuffle(pool)
            for slot in unassigned_quest_slots:
                rewards_assignment[slot] = ItemReward(pool.pop().const)
        else:
            for curve_name in QUEST_REWARD_CURVES:
                quest_curve = curves_dbview.find_one(lambda c: c.area == curve_name)
                unassigned_quest_slots_for_curve = [s for s in unassigned_quest_slots if s in QUEST_REWARD_CURVES[curve_name]]
                weights = {i : getattr(quest_curve, f"tier{i}") for i in range(1,9)}
                if env.options.flags.has('treasure_wild_weighted'):
                    weights = util.get_boosted_weights(weights)
                quest_distribution = util.Distribution(weights)
                tier_counts = quest_distribution.choose_many(env.rnd, len(unassigned_quest_slots_for_curve))
                pool = []
                for tier in tier_counts:
                    if tier_counts[tier] <= 0:
                        continue

                    tier_src_pool = items_dbview.find_all(lambda it: it.tier == tier)
                    tier_pool = list(tier_src_pool)
                    if len(tier_pool) > tier_counts[tier]:
                        tier_pool = env.rnd.sample(tier_pool, tier_counts[tier])
                    else:
                        while len(tier_pool) < tier_counts[tier]:
                            tier_pool.append(env.rnd.choice(tier_src_pool))
                    pool.extend(tier_pool)

                env.rnd.shuffle(pool)
                for slot in unassigned_quest_slots_for_curve:
                    rewards_assignment[slot] = ItemReward(pool.pop().const)
            
            for slot in unassigned_quest_slots:
                if slot not in rewards_assignment:
                    raise Exception(f"No reward assigned for slot {slot}")

        unassigned_chest_slots = [slot for slot in CHEST_ITEM_SLOTS if slot not in rewards_assignment]
        if env.options.flags.has('treasure_standard') or env.options.flags.has('treasure_wild'):
            src_pool = items_dbview.find_all(lambda it: it.tier >= 5)
            pool = list(src_pool)
            while len(pool) < len(unassigned_chest_slots):
                pool.append(env.rnd.choice(src_pool))

            env.rnd.shuffle(pool)
            for slot in unassigned_chest_slots:
                rewards_assignment[slot] = ItemReward(pool.pop().const)
        else:
            unassigned_chest_slots_by_area = {}
            for slot in unassigned_chest_slots:
                t = treasure_dbview.find_one(lambda t: [t.map, t.index] == CHEST_NUMBERS[slot])
                unassigned_chest_slots_by_area.setdefault(t.area, []).append(slot)

            miab_distributions = {}
            for c in curves_dbview.find_all(lambda c: c.area.startswith("MIAB_")):
                weights = {i : getattr(c, f"tier{i}") for i in range(1,9)}
                if env.options.flags.has('treasure_wild_weighted'):
                    weights = util.get_boosted_weights(weights)

                miab_distributions[c.area[len("MIAB_"):]] = util.Distribution(weights)

            tier_counts_by_area = {}
            total_tier_counts = {}
            for area in unassigned_chest_slots_by_area:
                raw_counts = miab_distributions[area].choose_many(env.rnd, len(unassigned_chest_slots_by_area[area]))
                tier_counts_by_area[area] = {}
                for tier in raw_counts:
                    tier_counts_by_area[area].setdefault(tier, 0)
                    tier_counts_by_area[area][tier] += raw_counts[tier]
                    total_tier_counts.setdefault(tier, 0)
                    total_tier_counts[tier] += raw_counts[tier]

            pools = {}
            for tier in total_tier_counts:
                src_pool = items_dbview.find_all(lambda it: it.tier == tier)
                if len(src_pool) > total_tier_counts[tier]:
                    pools[tier] = env.rnd.sample(src_pool, total_tier_counts[tier])
                else:
                    pools[tier] = list(src_pool)
                    while len(pools[tier]) < total_tier_counts[tier]:
                        pools[tier].append(env.rnd.choice(src_pool))
                env.rnd.shuffle(pools[tier])

            for area in unassigned_chest_slots_by_area:
                area_pool = []
                for tier in tier_counts_by_area[area]:
                    for i in range(tier_counts_by_area[area][tier]):
                        area_pool.append(pools[tier].pop())
                env.rnd.shuffle(area_pool)
                for slot in unassigned_chest_slots_by_area[area]:
                    rewards_assignment[slot] = ItemReward(area_pool.pop().const)

    # randomize fight treasure locations (keyitem rando needs to know this for ending)
    env.meta['miab_locations'] = {}
    if env.options.flags.has('vanilla_miabs'):
        for slot in CHEST_NUMBERS:
            env.meta['miab_locations'][slot] = CHEST_NUMBERS[slot]
    else:
        areas = {}
        for slot in CHEST_NUMBERS:
            treasure = treasure_dbview.find_one(lambda t: [t.map, t.index] == CHEST_NUMBERS[slot])
            areas.setdefault(treasure.area, []).append(slot)
        for area in areas:
            new_chests = env.rnd.sample(treasure_dbview.find_all(lambda t: t.area == area), len(areas[area]))
            for i,slot in enumerate(areas[area]):
                id = new_chests[i].flag
                ap_item = env.options.ap_data[str(id)]
                placement = items_dbview.find_one(lambda i: i.code == ap_item["item_data"]["fe_id"])
                if placement is None:
                    rewards_assignment[slot] = ItemReward("#item.Cure1")
                else:
                    rewards_assignment[slot] = ItemReward(placement.const)
                env.meta['miab_locations'][slot] = [new_chests[i].map, new_chests[i].index]

    # hacky cleanup step for _1 and _2 suffixes, and build key item metadata for random objectives
    env.meta['available_key_items'] = set()
    for slot in rewards_assignment:
        reward = rewards_assignment[slot]
        if reward:
            try:
                item = reward.item
            except AttributeError:
                continue

            if type(item) is str and (item.endswith('_1') or item.endswith('_2')):
                rewards_assignment[slot] = ItemReward(item[:-2])

            if reward.is_key:
                env.meta['available_key_items'].add(reward.item)

    # assign fixed reward slots
    #  (note: smith reward is assigned in custom_weapon_rando)
    if env.meta.get('has_objectives', False) and env.meta.get('zeromus_required', True):
        rewards_assignment[RewardSlot.fixed_crystal] = KeyItemReward('#item.Crystal')

    #if env.options.flags.has('no_adamants'):
    #    items = items_dbview.find_all(lambda it: it.tier in [7, 8])
    #    pink_tail_item = env.rnd.choice(items)
    #    rewards_assignment[RewardSlot.pink_trade_item] = ItemReward(pink_tail_item.const)
    #else:
    #    rewards_assignment[RewardSlot.pink_trade_item] = ItemReward(pink_tail_item.const)
        #rewards_assignment[RewardSlot.pink_trade_item] = ItemReward('#item.AdamantArmor')

    # for now, assign flat character positions
    rewards_assignment[RewardSlot.starting_character] = AxtorReward('#actor.DKCecil')
    rewards_assignment[RewardSlot.starting_partner_character] = AxtorReward('#actor.Kain1')
    rewards_assignment[RewardSlot.mist_character] = AxtorReward('#actor.CRydia')
    rewards_assignment[RewardSlot.watery_pass_character] = AxtorReward('#actor.Tellah1')
    rewards_assignment[RewardSlot.damcyan_character] = AxtorReward('#actor.Edward')
    rewards_assignment[RewardSlot.kaipo_character] = AxtorReward('#actor.Rosa1')
    rewards_assignment[RewardSlot.hobs_character] = AxtorReward('#actor.Yang1')
    rewards_assignment[RewardSlot.mysidia_character_1] = AxtorReward('#actor.Palom')
    rewards_assignment[RewardSlot.mysidia_character_2] = AxtorReward('#actor.Porom')
    rewards_assignment[RewardSlot.ordeals_character] = AxtorReward('#actor.Tellah2')
    rewards_assignment[RewardSlot.baron_inn_character] = AxtorReward('#actor.Yang2')
    rewards_assignment[RewardSlot.baron_castle_character] = AxtorReward('#actor.Cid')
    rewards_assignment[RewardSlot.zot_character_1] = AxtorReward('#actor.Kain2')
    rewards_assignment[RewardSlot.zot_character_2] = AxtorReward('#actor.Rosa2')
    rewards_assignment[RewardSlot.dwarf_castle_character] = AxtorReward('#actor.ARydia')
    rewards_assignment[RewardSlot.cave_eblan_character] = AxtorReward('#actor.Edge')
    rewards_assignment[RewardSlot.lunar_palace_character] = AxtorReward('#actor.Fusoya')
    rewards_assignment[RewardSlot.giant_character] = AxtorReward('#actor.Kain3')

    combined_assignments = {k : rewards_assignment[k] for k in rewards_assignment}
    combined_assignments.update(boss_assignment)
    env.update_assignments(combined_assignments)

    if DEBUG:
        print('FINAL ASSIGNMENT:')
        max_slot_length = max([len(str(s)) for s in combined_assignments])
        format_str = '  {{:{}}} <- {{}}'.format(max_slot_length)
        for k in combined_assignments:
            print(format_str.format(str(k), combined_assignments[k]))
        print('ATTEMPTS: {}'.format(attempts))

        print('BREAKDOWN of gating key items:')
        breakdown_items = list(ESSENTIAL_KEY_ITEMS)
        if env.options.flags.has('pass_in_key_items'):
            breakdown_items.append('#item.Pass')
        breakdown = {'normal':0, 'summon':0, 'moonboss':0, 'chests':0};
        for item in ESSENTIAL_KEY_ITEMS:
            for k in rewards_assignment:
                if rewards_assignment[k] == item:
                    if k in ITEM_SLOTS:
                        breakdown['normal'] += 1
                    elif k in SUMMON_QUEST_SLOTS:
                        breakdown['summon'] += 1
                    elif k in MOON_BOSS_SLOTS:
                        breakdown['moonboss'] += 1
                    elif k in CHEST_ITEM_SLOTS:
                        breakdown['chests'] += 1
        for k in breakdown:
            print(f'{k} : {breakdown[k]}')

    # need a table indicating which slots could contain key items for hinting
    # purposes, might as well do that here
    if env.options.hide_flags:
        potential_key_item_slots = list(ITEM_SLOTS) + list(SUMMON_QUEST_SLOTS) + list(MOON_BOSS_SLOTS) + list(CHEST_ITEM_SLOTS)
    elif env.options.flags.has('key_items_vanilla'):
        potential_key_item_slots = [s for s in range(RewardSlot.MAX_COUNT) if s in rewards_assignment and isinstance(rewards_assignment[s], ItemReward) and rewards_assignment[s].is_key]
    else:
        potential_key_item_slots = list(ITEM_SLOTS)
        if env.options.flags.has('key_items_in_summon_quests'):
            potential_key_item_slots.extend(SUMMON_QUEST_SLOTS)
        if env.options.flags.has('key_items_in_moon_bosses'):
            potential_key_item_slots.extend(MOON_BOSS_SLOTS)
        if env.options.flags.has('key_items_in_miabs'):
            potential_key_item_slots.extend(CHEST_ITEM_SLOTS)

    env.add_binary(BusAddress(0x21dc00), [1 if s in potential_key_item_slots else 0 for s in range(RewardSlot.MAX_COUNT)], as_script=True)
    env.add_substitution('randomizer key item count', '{:02X}'.format(17))

    # setup objectives reference table, and create boss metadata for random objectives purposes
    boss_objective_consts = []
    env.meta['available_bosses'] = set()
    for slot in BOSS_SLOTS:
        boss_objective_consts.append(f'#objective.boss_{boss_assignment[slot]}')
        env.meta['available_bosses'].add(boss_assignment[slot])
    env.add_script('patch($21f840 bus) {\n' + '\n'.join(boss_objective_consts) + '\n}')

    # remove golbez item delivery if not needed
    if (RewardSlot.fallen_golbez_item not in rewards_assignment):
        env.add_substitution('golbez awards item', '')

    # generate spoiler logs
    item_spoiler_names = {it.const: it.spoilername for it in databases.get_items_dbview()}

    key_item_spoilers = []
    for key_item_reward in list(ESSENTIAL_KEY_ITEMS) + list(NONESSENTIAL_KEY_ITEMS) + [ItemReward("#item.Pass")]:
        slot = rewards_assignment.find_slot(key_item_reward)
        if slot is None:
            slot = RewardSlot.none
        key_item_spoilers.append( SpoilerRow(item_spoiler_names[key_item_reward.item], REWARD_SLOT_SPOILER_NAMES[slot], obscurable=True) )
    env.spoilers.add_table("KEY ITEM LOCATIONS (and Pass if Pkey)", key_item_spoilers, public=env.options.flags.has_any('-spoil:all', '-spoil:keyitems'))

    quest_spoilers = []
    for slot in list(ITEM_SLOTS) + list(SUMMON_QUEST_SLOTS) + list(MOON_BOSS_SLOTS) + [RewardSlot.pink_trade_item]:
        if slot in rewards_assignment:
            reward = rewards_assignment[slot]
            if type(reward) is EmptyReward:
                reward_text = "(nothing)"
            else:
                reward_text = item_spoiler_names[reward.item]
            quest_spoilers.append( SpoilerRow(REWARD_SLOT_SPOILER_NAMES[slot], reward_text, obscurable=True) )
    env.spoilers.add_table("QUEST REWARDS", quest_spoilers, public=env.options.flags.has_any('-spoil:all', '-spoil:rewards'))

    # leave rewards assignment in meta for later use (TODO: later make it a first class member of env)
    env.meta['rewards_assignment'] = rewards_assignment
