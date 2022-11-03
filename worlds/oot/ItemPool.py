from collections import namedtuple
from itertools import chain
from .Items import item_table
from .LocationList import location_groups
from decimal import Decimal, ROUND_HALF_UP


# Generates itempools and places fixed items based on settings.

alwaysitems = ([
    'Biggoron Sword',
    'Boomerang',
    'Lens of Truth',
    'Megaton Hammer',
    'Iron Boots',
    'Goron Tunic',
    'Zora Tunic',
    'Hover Boots',
    'Mirror Shield',
    'Stone of Agony',
    'Fire Arrows',
    'Ice Arrows',
    'Light Arrows',
    'Dins Fire',
    'Farores Wind',
    'Nayrus Love',
    'Rupee (1)']
    + ['Progressive Hookshot'] * 2
    + ['Deku Shield']
    + ['Hylian Shield']
    + ['Progressive Strength Upgrade'] * 3
    + ['Progressive Scale'] * 2
    + ['Recovery Heart'] * 6
    + ['Bow'] * 3
    + ['Slingshot'] * 3
    + ['Bomb Bag'] * 3
    + ['Bombs (5)'] * 2
    + ['Bombs (10)']
    + ['Bombs (20)']
    + ['Arrows (5)']
    + ['Arrows (10)'] * 5
    + ['Progressive Wallet'] * 2
    + ['Magic Meter'] * 2
    + ['Double Defense']
    + ['Deku Stick Capacity'] * 2
    + ['Deku Nut Capacity'] * 2
    + ['Piece of Heart (Treasure Chest Game)'])


easy_items = ([
    'Biggoron Sword',
    'Kokiri Sword',
    'Boomerang',
    'Lens of Truth',
    'Megaton Hammer',
    'Iron Boots',
    'Goron Tunic',
    'Zora Tunic',
    'Hover Boots',
    'Mirror Shield',
    'Fire Arrows',
    'Light Arrows',
    'Dins Fire',
    'Progressive Hookshot',
    'Progressive Strength Upgrade',
    'Progressive Scale',
    'Progressive Wallet',
    'Magic Meter',
    'Deku Stick Capacity', 
    'Deku Nut Capacity', 
    'Bow', 
    'Slingshot', 
    'Bomb Bag',
    'Double Defense'] +
    ['Heart Container'] * 16 +
    ['Piece of Heart'] * 3)

normal_items = (
    ['Heart Container'] * 8 +
    ['Piece of Heart'] * 35)


item_difficulty_max = {
    'plentiful': {},
    'balanced': {},
    'scarce': {
        'Bombchus': 3,
        'Bombchus (5)': 1,
        'Bombchus (10)': 2,
        'Bombchus (20)': 0,
        'Magic Meter': 1, 
        'Double Defense': 0, 
        'Deku Stick Capacity': 1, 
        'Deku Nut Capacity': 1, 
        'Bow': 2, 
        'Slingshot': 2, 
        'Bomb Bag': 2,
        'Heart Container': 0,
    },
    'minimal': {
        'Bombchus': 1,
        'Bombchus (5)': 1,
        'Bombchus (10)': 0,
        'Bombchus (20)': 0,
        'Nayrus Love': 0,
        'Magic Meter': 1, 
        'Double Defense': 0, 
        'Deku Stick Capacity': 0, 
        'Deku Nut Capacity': 0, 
        'Bow': 1, 
        'Slingshot': 1, 
        'Bomb Bag': 1,
        'Heart Container': 0,
        'Piece of Heart': 0,
    },
}

DT_vanilla = (
    ['Recovery Heart'] * 2)

DT_MQ = (
    ['Deku Shield'] * 2 +
    ['Rupees (50)'])

DC_vanilla = (
    ['Rupees (20)'])

DC_MQ = (
    ['Hylian Shield'] +
    ['Rupees (5)'])

JB_MQ = (
    ['Deku Nuts (5)'] * 4 +
    ['Recovery Heart'] +
    ['Deku Shield'] +
    ['Deku Stick (1)'])

FoT_vanilla = (
    ['Recovery Heart'] +
    ['Arrows (10)'] +
    ['Arrows (30)'])

FoT_MQ = (
    ['Arrows (5)'])

FiT_vanilla = (
    ['Rupees (200)'])

FiT_MQ = (
    ['Bombs (20)'] +
    ['Hylian Shield'])

SpT_vanilla = (
    ['Deku Shield'] * 2 +
    ['Recovery Heart'] +
    ['Bombs (20)'])

SpT_MQ = (
    ['Rupees (50)'] * 2 +
    ['Arrows (30)'])

ShT_vanilla = (
    ['Arrows (30)'])

ShT_MQ = (
    ['Arrows (5)'] * 2 +
    ['Rupees (20)'])

BW_vanilla = (
    ['Recovery Heart'] +
    ['Bombs (10)'] +
    ['Rupees (200)'] +
    ['Deku Nuts (5)'] +
    ['Deku Nuts (10)'] +
    ['Deku Shield'] +
    ['Hylian Shield'])

GTG_vanilla = (
    ['Arrows (30)'] * 3 +
    ['Rupees (200)'])

GTG_MQ = (
    ['Rupee (Treasure Chest Game)'] * 2 +
    ['Arrows (10)'] +
    ['Rupee (1)'] +
    ['Rupees (50)'])

GC_vanilla = (
    ['Rupees (5)'] * 3 +
    ['Arrows (30)'])

GC_MQ = (
    ['Arrows (10)'] * 2 +
    ['Bombs (5)'] +
    ['Rupees (20)'] +
    ['Recovery Heart'])


normal_bottles = [
    'Bottle',
    'Bottle with Milk',
    'Bottle with Red Potion',
    'Bottle with Green Potion',
    'Bottle with Blue Potion',
    'Bottle with Fairy',
    'Bottle with Fish',
    'Bottle with Bugs',
    'Bottle with Poe',
    'Bottle with Big Poe',
    'Bottle with Blue Fire']

bottle_count = 4


dungeon_rewards = [
    'Kokiri Emerald',
    'Goron Ruby',
    'Zora Sapphire',
    'Forest Medallion',
    'Fire Medallion',
    'Water Medallion',
    'Shadow Medallion',
    'Spirit Medallion',
    'Light Medallion'
]


normal_rupees = (
    ['Rupees (5)'] * 13 +
    ['Rupees (20)'] * 5 +
    ['Rupees (50)'] * 7 +
    ['Rupees (200)'] * 3)

shopsanity_rupees = (
    ['Rupees (5)'] * 2 +
    ['Rupees (20)'] * 10 +
    ['Rupees (50)'] * 10 +
    ['Rupees (200)'] * 5 +
    ['Progressive Wallet'])


vanilla_shop_items = {
    'KF Shop Item 1': 'Buy Deku Shield',
    'KF Shop Item 2': 'Buy Deku Nut (5)',
    'KF Shop Item 3': 'Buy Deku Nut (10)',
    'KF Shop Item 4': 'Buy Deku Stick (1)',
    'KF Shop Item 5': 'Buy Deku Seeds (30)',
    'KF Shop Item 6': 'Buy Arrows (10)',
    'KF Shop Item 7': 'Buy Arrows (30)',
    'KF Shop Item 8': 'Buy Heart',
    'Kak Potion Shop Item 1': 'Buy Deku Nut (5)',
    'Kak Potion Shop Item 2': 'Buy Fish',
    'Kak Potion Shop Item 3': 'Buy Red Potion [30]',
    'Kak Potion Shop Item 4': 'Buy Green Potion',
    'Kak Potion Shop Item 5': 'Buy Blue Fire',
    'Kak Potion Shop Item 6': 'Buy Bottle Bug',
    'Kak Potion Shop Item 7': 'Buy Poe',
    'Kak Potion Shop Item 8': 'Buy Fairy\'s Spirit',
    'Market Bombchu Shop Item 1': 'Buy Bombchu (5)',
    'Market Bombchu Shop Item 2': 'Buy Bombchu (10)',
    'Market Bombchu Shop Item 3': 'Buy Bombchu (10)',
    'Market Bombchu Shop Item 4': 'Buy Bombchu (10)',
    'Market Bombchu Shop Item 5': 'Buy Bombchu (20)',
    'Market Bombchu Shop Item 6': 'Buy Bombchu (20)',
    'Market Bombchu Shop Item 7': 'Buy Bombchu (20)',
    'Market Bombchu Shop Item 8': 'Buy Bombchu (20)',
    'Market Potion Shop Item 1': 'Buy Green Potion',
    'Market Potion Shop Item 2': 'Buy Blue Fire',
    'Market Potion Shop Item 3': 'Buy Red Potion [30]',
    'Market Potion Shop Item 4': 'Buy Fairy\'s Spirit',
    'Market Potion Shop Item 5': 'Buy Deku Nut (5)',
    'Market Potion Shop Item 6': 'Buy Bottle Bug',
    'Market Potion Shop Item 7': 'Buy Poe',
    'Market Potion Shop Item 8': 'Buy Fish',
    'Market Bazaar Item 1': 'Buy Hylian Shield',
    'Market Bazaar Item 2': 'Buy Bombs (5) [35]',
    'Market Bazaar Item 3': 'Buy Deku Nut (5)',
    'Market Bazaar Item 4': 'Buy Heart',
    'Market Bazaar Item 5': 'Buy Arrows (10)',
    'Market Bazaar Item 6': 'Buy Arrows (50)',
    'Market Bazaar Item 7': 'Buy Deku Stick (1)',
    'Market Bazaar Item 8': 'Buy Arrows (30)',
    'Kak Bazaar Item 1': 'Buy Hylian Shield',
    'Kak Bazaar Item 2': 'Buy Bombs (5) [35]',
    'Kak Bazaar Item 3': 'Buy Deku Nut (5)',
    'Kak Bazaar Item 4': 'Buy Heart',
    'Kak Bazaar Item 5': 'Buy Arrows (10)',
    'Kak Bazaar Item 6': 'Buy Arrows (50)',
    'Kak Bazaar Item 7': 'Buy Deku Stick (1)',
    'Kak Bazaar Item 8': 'Buy Arrows (30)',
    'ZD Shop Item 1': 'Buy Zora Tunic',
    'ZD Shop Item 2': 'Buy Arrows (10)',
    'ZD Shop Item 3': 'Buy Heart',
    'ZD Shop Item 4': 'Buy Arrows (30)',
    'ZD Shop Item 5': 'Buy Deku Nut (5)',
    'ZD Shop Item 6': 'Buy Arrows (50)',
    'ZD Shop Item 7': 'Buy Fish',
    'ZD Shop Item 8': 'Buy Red Potion [50]',
    'GC Shop Item 1': 'Buy Bombs (5) [25]',
    'GC Shop Item 2': 'Buy Bombs (10)',
    'GC Shop Item 3': 'Buy Bombs (20)',
    'GC Shop Item 4': 'Buy Bombs (30)',
    'GC Shop Item 5': 'Buy Goron Tunic',
    'GC Shop Item 6': 'Buy Heart',
    'GC Shop Item 7': 'Buy Red Potion [40]',
    'GC Shop Item 8': 'Buy Heart',
}


min_shop_items = (
    ['Buy Deku Shield'] +
    ['Buy Hylian Shield'] +
    ['Buy Goron Tunic'] +
    ['Buy Zora Tunic'] +
    ['Buy Deku Nut (5)'] * 2 + ['Buy Deku Nut (10)'] +
    ['Buy Deku Stick (1)'] * 2 +
    ['Buy Deku Seeds (30)'] +
    ['Buy Arrows (10)'] * 2 + ['Buy Arrows (30)'] + ['Buy Arrows (50)'] +
    ['Buy Bombchu (5)'] + ['Buy Bombchu (10)'] * 2 + ['Buy Bombchu (20)'] +
    ['Buy Bombs (5) [25]'] + ['Buy Bombs (5) [35]'] + ['Buy Bombs (10)'] + ['Buy Bombs (20)'] +
    ['Buy Green Potion'] +
    ['Buy Red Potion [30]'] +
    ['Buy Blue Fire'] +
    ['Buy Fairy\'s Spirit'] +
    ['Buy Bottle Bug'] +
    ['Buy Fish'])


vanilla_deku_scrubs = {
    'ZR Deku Scrub Grotto Rear': 'Buy Red Potion [30]',
    'ZR Deku Scrub Grotto Front': 'Buy Green Potion',
    'SFM Deku Scrub Grotto Rear': 'Buy Red Potion [30]',
    'SFM Deku Scrub Grotto Front': 'Buy Green Potion',
    'LH Deku Scrub Grotto Left': 'Buy Deku Nut (5)',
    'LH Deku Scrub Grotto Right': 'Buy Bombs (5) [35]',
    'LH Deku Scrub Grotto Center': 'Buy Arrows (30)',
    'GV Deku Scrub Grotto Rear': 'Buy Red Potion [30]',
    'GV Deku Scrub Grotto Front': 'Buy Green Potion',
    'LW Deku Scrub Near Deku Theater Right': 'Buy Deku Nut (5)',
    'LW Deku Scrub Near Deku Theater Left': 'Buy Deku Stick (1)',
    'LW Deku Scrub Grotto Rear': 'Buy Arrows (30)',
    'Colossus Deku Scrub Grotto Rear': 'Buy Red Potion [30]',
    'Colossus Deku Scrub Grotto Front': 'Buy Green Potion',
    'DMC Deku Scrub': 'Buy Bombs (5) [35]',
    'DMC Deku Scrub Grotto Left': 'Buy Deku Nut (5)',
    'DMC Deku Scrub Grotto Right': 'Buy Bombs (5) [35]',
    'DMC Deku Scrub Grotto Center': 'Buy Arrows (30)',
    'GC Deku Scrub Grotto Left': 'Buy Deku Nut (5)',
    'GC Deku Scrub Grotto Right': 'Buy Bombs (5) [35]',
    'GC Deku Scrub Grotto Center': 'Buy Arrows (30)',
    'LLR Deku Scrub Grotto Left': 'Buy Deku Nut (5)',
    'LLR Deku Scrub Grotto Right': 'Buy Bombs (5) [35]',
    'LLR Deku Scrub Grotto Center': 'Buy Arrows (30)',
}


deku_scrubs_items = (
    ['Deku Nuts (5)'] * 5 +
    ['Deku Stick (1)'] +
    ['Bombs (5)'] * 5 +
    ['Recovery Heart'] * 4 +
    ['Rupees (5)'] * 4) # ['Green Potion']


songlist = [
    'Zeldas Lullaby',
    'Eponas Song',
    'Suns Song',
    'Sarias Song',
    'Song of Time',
    'Song of Storms',
    'Minuet of Forest',
    'Prelude of Light',
    'Bolero of Fire',
    'Serenade of Water',
    'Nocturne of Shadow',
    'Requiem of Spirit']


skulltula_locations = ([
    'KF GS Know It All House',
    'KF GS Bean Patch',
    'KF GS House of Twins',
    'LW GS Bean Patch Near Bridge',
    'LW GS Bean Patch Near Theater',
    'LW GS Above Theater',
    'SFM GS',
    'HF GS Near Kak Grotto',
    'HF GS Cow Grotto',
    'Market GS Guard House',
    'HC GS Tree',
    'HC GS Storms Grotto',
    'OGC GS',
    'LLR GS Tree',
    'LLR GS Rain Shed',
    'LLR GS House Window',
    'LLR GS Back Wall',
    'Kak GS House Under Construction',
    'Kak GS Skulltula House',
    'Kak GS Guards House',
    'Kak GS Tree',
    'Kak GS Watchtower',
    'Kak GS Above Impas House',
    'Graveyard GS Wall',
    'Graveyard GS Bean Patch',
    'DMT GS Bean Patch',
    'DMT GS Near Kak',
    'DMT GS Falling Rocks Path',
    'DMT GS Above Dodongos Cavern',
    'GC GS Boulder Maze',
    'GC GS Center Platform',
    'DMC GS Crate',
    'DMC GS Bean Patch',
    'ZR GS Ladder',
    'ZR GS Tree',
    'ZR GS Near Raised Grottos',
    'ZR GS Above Bridge',
    'ZD GS Frozen Waterfall',
    'ZF GS Tree',
    'ZF GS Above the Log',
    'ZF GS Hidden Cave',
    'LH GS Bean Patch',
    'LH GS Lab Wall',
    'LH GS Small Island',
    'LH GS Tree',
    'LH GS Lab Crate',
    'GV GS Small Bridge',
    'GV GS Bean Patch',
    'GV GS Behind Tent',
    'GV GS Pillar',
    'GF GS Archery Range',
    'GF GS Top Floor',
    'Wasteland GS',
    'Colossus GS Bean Patch',
    'Colossus GS Tree',
    'Colossus GS Hill'])


tradeitems = (
    'Pocket Egg',
    'Pocket Cucco',
    'Cojiro',
    'Odd Mushroom',
    'Poachers Saw',
    'Broken Sword',
    'Prescription',
    'Eyeball Frog',
    'Eyedrops',
    'Claim Check')

tradeitemoptions = (
    'pocket_egg',
    'pocket_cucco',
    'cojiro',
    'odd_mushroom',
    'poachers_saw',
    'broken_sword',
    'prescription',
    'eyeball_frog',
    'eyedrops',
    'claim_check')


fixedlocations = {
    'Ganon': 'Triforce',
    'Pierre': 'Scarecrow Song',
    'Deliver Rutos Letter': 'Deliver Letter',
    'Master Sword Pedestal': 'Time Travel',
    'Market Bombchu Bowling Bombchus': 'Bombchu Drop',
}

droplocations = {
    'Deku Baba Sticks': 'Deku Stick Drop',
    'Deku Baba Nuts': 'Deku Nut Drop',
    'Stick Pot': 'Deku Stick Drop',
    'Nut Pot': 'Deku Nut Drop',
    'Nut Crate': 'Deku Nut Drop',
    'Blue Fire': 'Blue Fire',
    'Lone Fish': 'Fish',
    'Fish Group': 'Fish',
    'Bug Rock': 'Bugs',
    'Bug Shrub': 'Bugs',
    'Wandering Bugs': 'Bugs',
    'Fairy Pot': 'Fairy',
    'Free Fairies': 'Fairy',
    'Wall Fairy': 'Fairy',
    'Butterfly Fairy': 'Fairy',
    'Gossip Stone Fairy': 'Fairy',
    'Bean Plant Fairy': 'Fairy',
    'Fairy Pond': 'Fairy',
    'Big Poe Kill': 'Big Poe',
}

vanillaBK = {
    'Fire Temple Boss Key Chest': 'Boss Key (Fire Temple)',
    'Shadow Temple Boss Key Chest': 'Boss Key (Shadow Temple)',
    'Spirit Temple Boss Key Chest': 'Boss Key (Spirit Temple)',
    'Water Temple Boss Key Chest': 'Boss Key (Water Temple)',
    'Forest Temple Boss Key Chest': 'Boss Key (Forest Temple)',

    'Fire Temple MQ Boss Key Chest': 'Boss Key (Fire Temple)',
    'Shadow Temple MQ Boss Key Chest': 'Boss Key (Shadow Temple)',
    'Spirit Temple MQ Boss Key Chest': 'Boss Key (Spirit Temple)',
    'Water Temple MQ Boss Key Chest': 'Boss Key (Water Temple)',
    'Forest Temple MQ Boss Key Chest': 'Boss Key (Forest Temple)',    
}

vanillaMC = {
    'Bottom of the Well Compass Chest': 'Compass (Bottom of the Well)',
    'Deku Tree Compass Chest': 'Compass (Deku Tree)',
    'Dodongos Cavern Compass Chest': 'Compass (Dodongos Cavern)',
    'Fire Temple Compass Chest': 'Compass (Fire Temple)',
    'Forest Temple Blue Poe Chest': 'Compass (Forest Temple)',
    'Ice Cavern Compass Chest': 'Compass (Ice Cavern)',
    'Jabu Jabus Belly Compass Chest': 'Compass (Jabu Jabus Belly)',
    'Shadow Temple Compass Chest': 'Compass (Shadow Temple)',
    'Spirit Temple Compass Chest': 'Compass (Spirit Temple)',
    'Water Temple Compass Chest': 'Compass (Water Temple)',

    'Bottom of the Well Map Chest': 'Map (Bottom of the Well)',
    'Deku Tree Map Chest': 'Map (Deku Tree)',
    'Dodongos Cavern Map Chest': 'Map (Dodongos Cavern)',
    'Fire Temple Map Chest': 'Map (Fire Temple)',
    'Forest Temple Map Chest': 'Map (Forest Temple)',
    'Ice Cavern Map Chest': 'Map (Ice Cavern)',
    'Jabu Jabus Belly Map Chest': 'Map (Jabu Jabus Belly)',
    'Shadow Temple Map Chest': 'Map (Shadow Temple)',
    'Spirit Temple Map Chest': 'Map (Spirit Temple)',
    'Water Temple Map Chest': 'Map (Water Temple)',

    'Bottom of the Well MQ Compass Chest': 'Compass (Bottom of the Well)',
    'Deku Tree MQ Compass Chest': 'Compass (Deku Tree)',
    'Dodongos Cavern MQ Compass Chest': 'Compass (Dodongos Cavern)',
    'Fire Temple MQ Compass Chest': 'Compass (Fire Temple)',
    'Forest Temple MQ Compass Chest': 'Compass (Forest Temple)',
    'Ice Cavern MQ Compass Chest': 'Compass (Ice Cavern)',
    'Jabu Jabus Belly MQ Compass Chest': 'Compass (Jabu Jabus Belly)',
    'Shadow Temple MQ Compass Chest': 'Compass (Shadow Temple)',
    'Spirit Temple MQ Compass Chest': 'Compass (Spirit Temple)',
    'Water Temple MQ Compass Chest': 'Compass (Water Temple)',

    'Bottom of the Well MQ Map Chest': 'Map (Bottom of the Well)',
    'Deku Tree MQ Map Chest': 'Map (Deku Tree)',
    'Dodongos Cavern MQ Map Chest': 'Map (Dodongos Cavern)',
    'Fire Temple MQ Map Chest': 'Map (Fire Temple)',
    'Forest Temple MQ Map Chest': 'Map (Forest Temple)',
    'Ice Cavern MQ Map Chest': 'Map (Ice Cavern)',
    'Jabu Jabus Belly MQ Map Chest': 'Map (Jabu Jabus Belly)',
    'Shadow Temple MQ Map Chest': 'Map (Shadow Temple)',
    'Spirit Temple MQ Map Chest': 'Map (Spirit Temple)',
    'Water Temple MQ Map Chest': 'Map (Water Temple)',
}

vanillaSK = {
    'Bottom of the Well Front Left Fake Wall Chest': 'Small Key (Bottom of the Well)',
    'Bottom of the Well Right Bottom Fake Wall Chest': 'Small Key (Bottom of the Well)',
    'Bottom of the Well Freestanding Key': 'Small Key (Bottom of the Well)',
    'Fire Temple Big Lava Room Blocked Door Chest': 'Small Key (Fire Temple)',
    'Fire Temple Big Lava Room Lower Open Door Chest': 'Small Key (Fire Temple)',
    'Fire Temple Boulder Maze Shortcut Chest': 'Small Key (Fire Temple)',
    'Fire Temple Boulder Maze Lower Chest': 'Small Key (Fire Temple)',
    'Fire Temple Boulder Maze Side Room Chest': 'Small Key (Fire Temple)',
    'Fire Temple Boulder Maze Upper Chest': 'Small Key (Fire Temple)',
    'Fire Temple Near Boss Chest': 'Small Key (Fire Temple)',
    'Fire Temple Highest Goron Chest': 'Small Key (Fire Temple)',
    'Forest Temple First Stalfos Chest': 'Small Key (Forest Temple)',
    'Forest Temple First Room Chest': 'Small Key (Forest Temple)',
    'Forest Temple Floormaster Chest': 'Small Key (Forest Temple)',
    'Forest Temple Red Poe Chest': 'Small Key (Forest Temple)',
    'Forest Temple Well Chest': 'Small Key (Forest Temple)',
    'Ganons Castle Light Trial Invisible Enemies Chest': 'Small Key (Ganons Castle)',
    'Ganons Castle Light Trial Lullaby Chest': 'Small Key (Ganons Castle)',
    'Gerudo Training Ground Beamos Chest': 'Small Key (Gerudo Training Ground)',
    'Gerudo Training Ground Eye Statue Chest': 'Small Key (Gerudo Training Ground)',
    'Gerudo Training Ground Hammer Room Switch Chest': 'Small Key (Gerudo Training Ground)',
    'Gerudo Training Ground Heavy Block Third Chest': 'Small Key (Gerudo Training Ground)',
    'Gerudo Training Ground Hidden Ceiling Chest': 'Small Key (Gerudo Training Ground)',
    'Gerudo Training Ground Near Scarecrow Chest': 'Small Key (Gerudo Training Ground)',
    'Gerudo Training Ground Stalfos Chest': 'Small Key (Gerudo Training Ground)',
    'Gerudo Training Ground Underwater Silver Rupee Chest': 'Small Key (Gerudo Training Ground)',
    'Gerudo Training Ground Freestanding Key': 'Small Key (Gerudo Training Ground)',
    'Shadow Temple After Wind Hidden Chest': 'Small Key (Shadow Temple)',
    'Shadow Temple Early Silver Rupee Chest': 'Small Key (Shadow Temple)',
    'Shadow Temple Falling Spikes Switch Chest': 'Small Key (Shadow Temple)',
    'Shadow Temple Invisible Floormaster Chest': 'Small Key (Shadow Temple)',
    'Shadow Temple Freestanding Key': 'Small Key (Shadow Temple)',
    'Spirit Temple Child Early Torches Chest': 'Small Key (Spirit Temple)',
    'Spirit Temple Early Adult Right Chest': 'Small Key (Spirit Temple)',
    'Spirit Temple Near Four Armos Chest': 'Small Key (Spirit Temple)',
    'Spirit Temple Statue Room Hand Chest': 'Small Key (Spirit Temple)',
    'Spirit Temple Sun Block Room Chest': 'Small Key (Spirit Temple)',
    'Water Temple Central Bow Target Chest': 'Small Key (Water Temple)',
    'Water Temple Central Pillar Chest': 'Small Key (Water Temple)',
    'Water Temple Cracked Wall Chest': 'Small Key (Water Temple)',
    'Water Temple Dragon Chest': 'Small Key (Water Temple)',
    'Water Temple River Chest': 'Small Key (Water Temple)',
    'Water Temple Torches Chest': 'Small Key (Water Temple)',

    'Bottom of the Well MQ Dead Hand Freestanding Key': 'Small Key (Bottom of the Well)',
    'Bottom of the Well MQ East Inner Room Freestanding Key': 'Small Key (Bottom of the Well)',
    'Fire Temple MQ Big Lava Room Blocked Door Chest': 'Small Key (Fire Temple)',
    'Fire Temple MQ Near Boss Chest': 'Small Key (Fire Temple)',
    'Fire Temple MQ Lizalfos Maze Side Room Chest': 'Small Key (Fire Temple)',
    'Fire Temple MQ Chest On Fire': 'Small Key (Fire Temple)',
    'Fire Temple MQ Freestanding Key': 'Small Key (Fire Temple)',
    'Forest Temple MQ Wolfos Chest': 'Small Key (Forest Temple)',
    'Forest Temple MQ First Room Chest': 'Small Key (Forest Temple)',
    'Forest Temple MQ Raised Island Courtyard Lower Chest': 'Small Key (Forest Temple)',
    'Forest Temple MQ Raised Island Courtyard Upper Chest': 'Small Key (Forest Temple)',
    'Forest Temple MQ Redead Chest': 'Small Key (Forest Temple)',
    'Forest Temple MQ Well Chest': 'Small Key (Forest Temple)',
    'Ganons Castle MQ Shadow Trial Eye Switch Chest': 'Small Key (Ganons Castle)',
    'Ganons Castle MQ Spirit Trial Sun Back Left Chest': 'Small Key (Ganons Castle)',
    'Ganons Castle MQ Forest Trial Freestanding Key': 'Small Key (Ganons Castle)',
    'Gerudo Training Ground MQ Dinolfos Chest': 'Small Key (Gerudo Training Ground)',
    'Gerudo Training Ground MQ Flame Circle Chest': 'Small Key (Gerudo Training Ground)',
    'Gerudo Training Ground MQ Underwater Silver Rupee Chest': 'Small Key (Gerudo Training Ground)',
    'Shadow Temple MQ Falling Spikes Switch Chest': 'Small Key (Shadow Temple)',
    'Shadow Temple MQ Invisible Blades Invisible Chest': 'Small Key (Shadow Temple)',
    'Shadow Temple MQ Early Gibdos Chest': 'Small Key (Shadow Temple)',
    'Shadow Temple MQ Near Ship Invisible Chest': 'Small Key (Shadow Temple)',
    'Shadow Temple MQ Wind Hint Chest': 'Small Key (Shadow Temple)',
    'Shadow Temple MQ Freestanding Key': 'Small Key (Shadow Temple)',
    'Spirit Temple MQ Child Hammer Switch Chest': 'Small Key (Spirit Temple)',
    'Spirit Temple MQ Child Climb South Chest': 'Small Key (Spirit Temple)',
    'Spirit Temple MQ Map Room Enemy Chest': 'Small Key (Spirit Temple)',
    'Spirit Temple MQ Entrance Back Left Chest': 'Small Key (Spirit Temple)',
    'Spirit Temple MQ Entrance Front Right Chest': 'Small Key (Spirit Temple)',
    'Spirit Temple MQ Mirror Puzzle Invisible Chest': 'Small Key (Spirit Temple)',
    'Spirit Temple MQ Silver Block Hallway Chest': 'Small Key (Spirit Temple)',
    'Water Temple MQ Central Pillar Chest': 'Small Key (Water Temple)',
    'Water Temple MQ Freestanding Key': 'Small Key (Water Temple)',    
}

junk_pool_base = [
    ('Bombs (5)',       8),
    ('Bombs (10)',      2),
    ('Arrows (5)',      8),
    ('Arrows (10)',     2),
    ('Deku Stick (1)',  5),
    ('Deku Nuts (5)',   5),
    ('Deku Seeds (30)', 5),
    ('Rupees (5)',      10),
    ('Rupees (20)',     4),
    ('Rupees (50)',     1),
]

pending_junk_pool = []
junk_pool = []


remove_junk_items = [
    'Bombs (5)',
    'Deku Nuts (5)',
    'Deku Stick (1)',
    'Recovery Heart',
    'Arrows (5)',
    'Arrows (10)',
    'Arrows (30)',
    'Rupees (5)',
    'Rupees (20)',
    'Rupees (50)',
    'Rupees (200)',
    'Deku Nuts (10)',
    'Bombs (10)',
    'Bombs (20)',
    'Deku Seeds (30)',
    'Ice Trap',
]
remove_junk_set = set(remove_junk_items)

exclude_from_major = [ 
    'Deliver Letter',
    'Sell Big Poe',
    'Magic Bean',
    'Zeldas Letter',
    'Bombchus (5)',
    'Bombchus (10)',
    'Bombchus (20)',
    'Odd Potion',
    'Triforce Piece'
]

item_groups = {
    'Junk': remove_junk_items,
    'JunkSong': ('Prelude of Light', 'Serenade of Water'),
    'AdultTrade': tradeitems,
    'Bottle': normal_bottles,
    'Spell': ('Dins Fire', 'Farores Wind', 'Nayrus Love'),
    'Shield': ('Deku Shield', 'Hylian Shield'),
    'Song': songlist,
    'NonWarpSong': songlist[0:6],
    'WarpSong': songlist[6:],
    'HealthUpgrade': ('Heart Container', 'Piece of Heart'),
    'ProgressItem': [name for (name, data) in item_table.items() if data[0] == 'Item' and data[1]],
    'MajorItem': [name for (name, data) in item_table.items() if (data[0] == 'Item' or data[0] == 'Song') and data[1] and name not in exclude_from_major],
    'DungeonReward': dungeon_rewards,

    'ForestFireWater': ('Forest Medallion', 'Fire Medallion', 'Water Medallion'),
    'FireWater': ('Fire Medallion', 'Water Medallion'),
}

random = None


def get_junk_pool(ootworld):
    junk_pool[:] = list(junk_pool_base)
    if ootworld.junk_ice_traps == 'on': 
        junk_pool.append(('Ice Trap', 10))
    elif ootworld.junk_ice_traps in ['mayhem', 'onslaught']:
        junk_pool[:] = [('Ice Trap', 1)]
    return junk_pool


def get_junk_item(count=1, pool=None, plando_pool=None):
    global random
    
    if count < 1:
        raise ValueError("get_junk_item argument 'count' must be greater than 0.")

    return_pool = []
    if pending_junk_pool:
        pending_count = min(len(pending_junk_pool), count)
        return_pool = [pending_junk_pool.pop() for _ in range(pending_count)]
        count -= pending_count

    if pool and plando_pool:
        jw_list = [(junk, weight) for (junk, weight) in junk_pool
                   if junk not in plando_pool or pool.count(junk) < plando_pool[junk].count]
        try:
            junk_items, junk_weights = zip(*jw_list)
        except ValueError:
            raise RuntimeError("Not enough junk is available in the item pool to replace removed items.")
    else:
        junk_items, junk_weights = zip(*junk_pool)
    return_pool.extend(random.choices(junk_items, weights=junk_weights, k=count))

    return return_pool


def replace_max_item(items, item, max):
    count = 0
    for i,val in enumerate(items):
        if val == item:
            if count >= max:
                items[i] = get_junk_item()[0]
            count += 1


def generate_itempool(ootworld):
    world = ootworld.multiworld
    player = ootworld.player
    global random
    random = world.random

    junk_pool = get_junk_pool(ootworld)

    fixed_locations = filter(lambda loc: loc.name in fixedlocations, ootworld.get_locations())
    for location in fixed_locations:
        item = fixedlocations[location.name]
        location.place_locked_item(ootworld.create_item(item))

    drop_locations = filter(lambda loc: loc.type == 'Drop', ootworld.get_locations())
    for drop_location in drop_locations:
        item = droplocations[drop_location.name]
        drop_location.place_locked_item(ootworld.create_item(item))

    # set up item pool
    (pool, placed_items, skip_in_spoiler_locations) = get_pool_core(ootworld)
    ootworld.itempool = [ootworld.create_item(item) for item in pool]
    for (location_name, item) in placed_items.items():
        location = world.get_location(location_name, player)
        location.place_locked_item(ootworld.create_item(item))
        if location_name in skip_in_spoiler_locations:
            location.show_in_spoiler = False



# def try_collect_heart_container(world, pool):
#     if 'Heart Container' in pool:
#         pool.remove('Heart Container')
#         pool.extend(get_junk_item())
#         world.state.collect(ItemFactory('Heart Container'))
#         return True
#     return False


# def try_collect_pieces_of_heart(world, pool):
#     n = pool.count('Piece of Heart') + pool.count('Piece of Heart (Treasure Chest Game)')
#     if n >= 4:
#         for i in range(4):
#             if 'Piece of Heart' in pool:
#                 pool.remove('Piece of Heart')
#                 world.state.collect(ItemFactory('Piece of Heart'))
#             else:
#                 pool.remove('Piece of Heart (Treasure Chest Game)')
#                 world.state.collect(ItemFactory('Piece of Heart (Treasure Chest Game)'))
#             pool.extend(get_junk_item())
#         return True
#     return False


# def collect_pieces_of_heart(world, pool):
#     success = try_collect_pieces_of_heart(world, pool)
#     if not success:
#         try_collect_heart_container(world, pool)


# def collect_heart_container(world, pool):
#     success = try_collect_heart_container(world, pool)
#     if not success:
#         try_collect_pieces_of_heart(world, pool)


def get_pool_core(world):
    global random

    pool = []
    placed_items = {
        'HC Zeldas Letter': 'Zeldas Letter',
    }
    skip_in_spoiler_locations = []

    if world.shuffle_kokiri_sword:
        pool.append('Kokiri Sword')
    else:
        placed_items['KF Kokiri Sword Chest'] = 'Kokiri Sword'

    ruto_bottles = 1
    if world.zora_fountain == 'open':
        ruto_bottles = 0
    elif world.item_pool_value == 'plentiful':
        ruto_bottles += 1

    if world.skip_child_zelda:
        placed_items['HC Malon Egg'] = 'Recovery Heart'
        skip_in_spoiler_locations.append('HC Malon Egg')
    elif world.shuffle_weird_egg:
        pool.append('Weird Egg')
    else:
        placed_items['HC Malon Egg'] = 'Weird Egg'

    if world.shuffle_ocarinas:
        pool.extend(['Ocarina'] * 2)
        if world.item_pool_value == 'plentiful':
            pending_junk_pool.append('Ocarina')
    else:
        placed_items['LW Gift from Saria'] = 'Ocarina'
        placed_items['HF Ocarina of Time Item'] = 'Ocarina'

    if world.shuffle_cows:
        pool.extend(get_junk_item(10 if world.dungeon_mq['Jabu Jabus Belly'] else 9))
    else:
        cow_locations = ['LLR Stables Left Cow', 'LLR Stables Right Cow', 'LLR Tower Left Cow', 'LLR Tower Right Cow', 
            'KF Links House Cow', 'Kak Impas House Cow', 'GV Cow', 'DMT Cow Grotto Cow', 'HF Cow Grotto Cow']
        if world.dungeon_mq['Jabu Jabus Belly']:
            cow_locations.append('Jabu Jabus Belly MQ Cow')
        for loc in cow_locations:
            placed_items[loc] = 'Milk'
            skip_in_spoiler_locations.append(loc)

    if world.shuffle_beans:
        pool.append('Magic Bean Pack')
        if world.item_pool_value == 'plentiful':
            pending_junk_pool.append('Magic Bean Pack')
    else:
        placed_items['ZR Magic Bean Salesman'] = 'Magic Bean'
        skip_in_spoiler_locations.append('ZR Magic Bean Salesman')

    if world.shuffle_medigoron_carpet_salesman:
        pool.append('Giants Knife')
    else:
        placed_items['GC Medigoron'] = 'Giants Knife'
        skip_in_spoiler_locations.append('GC Medigoron')

    if world.dungeon_mq['Deku Tree']:
        skulltula_locations_final = skulltula_locations + [
            'Deku Tree MQ GS Lobby',
            'Deku Tree MQ GS Compass Room',
            'Deku Tree MQ GS Basement Graves Room',
            'Deku Tree MQ GS Basement Back Room']
    else:
        skulltula_locations_final = skulltula_locations + [
            'Deku Tree GS Compass Room',
            'Deku Tree GS Basement Vines',
            'Deku Tree GS Basement Gate',
            'Deku Tree GS Basement Back Room']
    if world.dungeon_mq['Dodongos Cavern']:
        skulltula_locations_final.extend([
            'Dodongos Cavern MQ GS Scrub Room',
            'Dodongos Cavern MQ GS Song of Time Block Room',
            'Dodongos Cavern MQ GS Lizalfos Room',
            'Dodongos Cavern MQ GS Larvae Room',
            'Dodongos Cavern MQ GS Back Area'])
    else:
        skulltula_locations_final.extend([
            'Dodongos Cavern GS Side Room Near Lower Lizalfos',
            'Dodongos Cavern GS Vines Above Stairs',
            'Dodongos Cavern GS Back Room',
            'Dodongos Cavern GS Alcove Above Stairs',
            'Dodongos Cavern GS Scarecrow'])
    if world.dungeon_mq['Jabu Jabus Belly']:
        skulltula_locations_final.extend([
            'Jabu Jabus Belly MQ GS Tailpasaran Room',
            'Jabu Jabus Belly MQ GS Invisible Enemies Room',
            'Jabu Jabus Belly MQ GS Boomerang Chest Room',
            'Jabu Jabus Belly MQ GS Near Boss'])
    else:
        skulltula_locations_final.extend([
            'Jabu Jabus Belly GS Water Switch Room',
            'Jabu Jabus Belly GS Lobby Basement Lower',
            'Jabu Jabus Belly GS Lobby Basement Upper',
            'Jabu Jabus Belly GS Near Boss'])
    if world.dungeon_mq['Forest Temple']:
        skulltula_locations_final.extend([
            'Forest Temple MQ GS First Hallway',
            'Forest Temple MQ GS Block Push Room',
            'Forest Temple MQ GS Raised Island Courtyard',
            'Forest Temple MQ GS Level Island Courtyard',
            'Forest Temple MQ GS Well'])
    else:
        skulltula_locations_final.extend([
            'Forest Temple GS First Room',
            'Forest Temple GS Lobby',
            'Forest Temple GS Raised Island Courtyard',
            'Forest Temple GS Level Island Courtyard',
            'Forest Temple GS Basement'])
    if world.dungeon_mq['Fire Temple']:
        skulltula_locations_final.extend([
            'Fire Temple MQ GS Above Fire Wall Maze',
            'Fire Temple MQ GS Fire Wall Maze Center',
            'Fire Temple MQ GS Big Lava Room Open Door',
            'Fire Temple MQ GS Fire Wall Maze Side Room',
            'Fire Temple MQ GS Skull On Fire'])
    else:
        skulltula_locations_final.extend([
            'Fire Temple GS Song of Time Room',
            'Fire Temple GS Boulder Maze',
            'Fire Temple GS Scarecrow Climb',
            'Fire Temple GS Scarecrow Top',
            'Fire Temple GS Boss Key Loop'])
    if world.dungeon_mq['Water Temple']:
        skulltula_locations_final.extend([
            'Water Temple MQ GS Before Upper Water Switch',
            'Water Temple MQ GS Freestanding Key Area',
            'Water Temple MQ GS Lizalfos Hallway',
            'Water Temple MQ GS River',
            'Water Temple MQ GS Triple Wall Torch'])
    else:
        skulltula_locations_final.extend([
            'Water Temple GS Behind Gate',
            'Water Temple GS River',
            'Water Temple GS Falling Platform Room',
            'Water Temple GS Central Pillar',
            'Water Temple GS Near Boss Key Chest'])
    if world.dungeon_mq['Spirit Temple']:
        skulltula_locations_final.extend([
            'Spirit Temple MQ GS Symphony Room',
            'Spirit Temple MQ GS Leever Room',
            'Spirit Temple MQ GS Nine Thrones Room West',
            'Spirit Temple MQ GS Nine Thrones Room North',
            'Spirit Temple MQ GS Sun Block Room'])
    else:
        skulltula_locations_final.extend([
            'Spirit Temple GS Metal Fence',
            'Spirit Temple GS Sun on Floor Room',
            'Spirit Temple GS Hall After Sun Block Room',
            'Spirit Temple GS Boulder Room',
            'Spirit Temple GS Lobby'])
    if world.dungeon_mq['Shadow Temple']:
        skulltula_locations_final.extend([
            'Shadow Temple MQ GS Falling Spikes Room',
            'Shadow Temple MQ GS Wind Hint Room',
            'Shadow Temple MQ GS After Wind',
            'Shadow Temple MQ GS After Ship',
            'Shadow Temple MQ GS Near Boss'])
    else:
        skulltula_locations_final.extend([
            'Shadow Temple GS Like Like Room',
            'Shadow Temple GS Falling Spikes Room',
            'Shadow Temple GS Single Giant Pot',
            'Shadow Temple GS Near Ship',
            'Shadow Temple GS Triple Giant Pot'])
    if world.dungeon_mq['Bottom of the Well']:
        skulltula_locations_final.extend([
            'Bottom of the Well MQ GS Basement',
            'Bottom of the Well MQ GS Coffin Room',
            'Bottom of the Well MQ GS West Inner Room'])
    else:
        skulltula_locations_final.extend([
            'Bottom of the Well GS West Inner Room',
            'Bottom of the Well GS East Inner Room',
            'Bottom of the Well GS Like Like Cage'])
    if world.dungeon_mq['Ice Cavern']:
        skulltula_locations_final.extend([
            'Ice Cavern MQ GS Scarecrow',
            'Ice Cavern MQ GS Ice Block',
            'Ice Cavern MQ GS Red Ice'])
    else:
        skulltula_locations_final.extend([
            'Ice Cavern GS Spinning Scythe Room',
            'Ice Cavern GS Heart Piece Room',
            'Ice Cavern GS Push Block Room'])
    if world.tokensanity == 'off':
        for location in skulltula_locations_final:
            placed_items[location] = 'Gold Skulltula Token'
            skip_in_spoiler_locations.append(location)
    elif world.tokensanity == 'dungeons':
        for location in skulltula_locations_final:
            if world.get_location(location).scene >= 0x0A:
                placed_items[location] = 'Gold Skulltula Token'
                skip_in_spoiler_locations.append(location)
            else:
                pool.append('Gold Skulltula Token')
    elif world.tokensanity == 'overworld':
        for location in skulltula_locations_final:
            if world.get_location(location).scene < 0x0A:
                placed_items[location] = 'Gold Skulltula Token'
                skip_in_spoiler_locations.append(location)
            else:
                pool.append('Gold Skulltula Token')
    else:
        pool.extend(['Gold Skulltula Token'] * 100)


    if world.bombchus_in_logic:
        pool.extend(['Bombchus'] * 4)
        if world.dungeon_mq['Jabu Jabus Belly']:
            pool.extend(['Bombchus'])
        if world.dungeon_mq['Spirit Temple']:
            pool.extend(['Bombchus'] * 2)
        if not world.dungeon_mq['Bottom of the Well']:
            pool.extend(['Bombchus'])
        if world.dungeon_mq['Gerudo Training Ground']:
            pool.extend(['Bombchus'])
        if world.shuffle_medigoron_carpet_salesman:
            pool.append('Bombchus')

    else:
        pool.extend(['Bombchus (5)'] + ['Bombchus (10)'] * 2)
        if world.dungeon_mq['Jabu Jabus Belly']:
                pool.extend(['Bombchus (10)'])
        if world.dungeon_mq['Spirit Temple']:
                pool.extend(['Bombchus (10)'] * 2)
        if not world.dungeon_mq['Bottom of the Well']:
                pool.extend(['Bombchus (10)'])
        if world.dungeon_mq['Gerudo Training Ground']:
                pool.extend(['Bombchus (10)'])
        if world.dungeon_mq['Ganons Castle']:
            pool.extend(['Bombchus (10)'])
        else:
            pool.extend(['Bombchus (20)'])
        if world.shuffle_medigoron_carpet_salesman:
            pool.append('Bombchus (10)')

    if not world.shuffle_medigoron_carpet_salesman:
        placed_items['Wasteland Bombchu Salesman'] = 'Bombchus (10)'
        skip_in_spoiler_locations.append('Wasteland Bombchu Salesman')

    pool.extend(['Ice Trap'])
    if not world.dungeon_mq['Gerudo Training Ground']:
        pool.extend(['Ice Trap'])
    if not world.dungeon_mq['Ganons Castle']:
        pool.extend(['Ice Trap'] * 4)

    if world.gerudo_fortress == 'open':
        placed_items['Hideout Jail Guard (1 Torch)'] = 'Recovery Heart'
        placed_items['Hideout Jail Guard (2 Torches)'] = 'Recovery Heart'
        placed_items['Hideout Jail Guard (3 Torches)'] = 'Recovery Heart'
        placed_items['Hideout Jail Guard (4 Torches)'] = 'Recovery Heart'
        skip_in_spoiler_locations.extend(['Hideout Jail Guard (1 Torch)', 'Hideout Jail Guard (2 Torches)', 'Hideout Jail Guard (3 Torches)', 'Hideout Jail Guard (4 Torches)'])
    elif world.shuffle_fortresskeys in ['any_dungeon', 'overworld', 'keysanity']:
        if world.gerudo_fortress == 'fast':
            pool.append('Small Key (Thieves Hideout)')
            placed_items['Hideout Jail Guard (2 Torches)'] = 'Recovery Heart'
            placed_items['Hideout Jail Guard (3 Torches)'] = 'Recovery Heart'
            placed_items['Hideout Jail Guard (4 Torches)'] = 'Recovery Heart'
            skip_in_spoiler_locations.extend(['Hideout Jail Guard (2 Torches)', 'Hideout Jail Guard (3 Torches)', 'Hideout Jail Guard (4 Torches)'])
        else:
            pool.extend(['Small Key (Thieves Hideout)'] * 4)
        if world.item_pool_value == 'plentiful':
            pending_junk_pool.append('Small Key (Thieves Hideout)')
    else:
        if world.gerudo_fortress == 'fast':
            placed_items['Hideout Jail Guard (1 Torch)']   = 'Small Key (Thieves Hideout)'
            placed_items['Hideout Jail Guard (2 Torches)'] = 'Recovery Heart'
            placed_items['Hideout Jail Guard (3 Torches)'] = 'Recovery Heart'
            placed_items['Hideout Jail Guard (4 Torches)'] = 'Recovery Heart'
            skip_in_spoiler_locations.extend(['Hideout Jail Guard (2 Torches)', 'Hideout Jail Guard (3 Torches)', 'Hideout Jail Guard (4 Torches)'])
        else:
            placed_items['Hideout Jail Guard (1 Torch)']   = 'Small Key (Thieves Hideout)'
            placed_items['Hideout Jail Guard (2 Torches)'] = 'Small Key (Thieves Hideout)'
            placed_items['Hideout Jail Guard (3 Torches)'] = 'Small Key (Thieves Hideout)'
            placed_items['Hideout Jail Guard (4 Torches)'] = 'Small Key (Thieves Hideout)'

    if world.shuffle_gerudo_card and world.gerudo_fortress != 'open':
        pool.append('Gerudo Membership Card')
    elif world.shuffle_gerudo_card:
        pending_junk_pool.append('Gerudo Membership Card')
        placed_items['Hideout Gerudo Membership Card'] = 'Ice Trap'
        skip_in_spoiler_locations.append('Hideout Gerudo Membership Card')
    else:
        card = world.create_item('Gerudo Membership Card')
        world.multiworld.push_precollected(card)
        placed_items['Hideout Gerudo Membership Card'] = 'Gerudo Membership Card'
        skip_in_spoiler_locations.append('Hideout Gerudo Membership Card')
    if world.shuffle_gerudo_card and world.item_pool_value == 'plentiful':
        pending_junk_pool.append('Gerudo Membership Card')

    if world.item_pool_value == 'plentiful' and world.shuffle_smallkeys in ['any_dungeon', 'overworld', 'keysanity']:
        pending_junk_pool.append('Small Key (Bottom of the Well)')
        pending_junk_pool.append('Small Key (Forest Temple)')
        pending_junk_pool.append('Small Key (Fire Temple)')
        pending_junk_pool.append('Small Key (Water Temple)')
        pending_junk_pool.append('Small Key (Shadow Temple)')
        pending_junk_pool.append('Small Key (Spirit Temple)')
        pending_junk_pool.append('Small Key (Gerudo Training Ground)')
        pending_junk_pool.append('Small Key (Ganons Castle)')

    if world.item_pool_value == 'plentiful' and world.shuffle_bosskeys in ['any_dungeon', 'overworld', 'keysanity']:
        pending_junk_pool.append('Boss Key (Forest Temple)')
        pending_junk_pool.append('Boss Key (Fire Temple)')
        pending_junk_pool.append('Boss Key (Water Temple)')
        pending_junk_pool.append('Boss Key (Shadow Temple)')
        pending_junk_pool.append('Boss Key (Spirit Temple)')

    if world.item_pool_value == 'plentiful' and world.shuffle_ganon_bosskey in ['any_dungeon', 'overworld', 'keysanity']:
        pending_junk_pool.append('Boss Key (Ganons Castle)')

    if world.shopsanity == 'off':
        placed_items.update(vanilla_shop_items)
        if world.bombchus_in_logic:
            placed_items['KF Shop Item 8'] = 'Buy Bombchu (5)'
            placed_items['Market Bazaar Item 4'] = 'Buy Bombchu (5)'
            placed_items['Kak Bazaar Item 4'] = 'Buy Bombchu (5)'
        pool.extend(normal_rupees)
        skip_in_spoiler_locations.extend(vanilla_shop_items.keys())
        if world.bombchus_in_logic:
            skip_in_spoiler_locations.remove('KF Shop Item 8')
            skip_in_spoiler_locations.remove('Market Bazaar Item 4')
            skip_in_spoiler_locations.remove('Kak Bazaar Item 4')

    else:
        remain_shop_items = list(vanilla_shop_items.values())
        pool.extend(min_shop_items)
        for item in min_shop_items:
            remain_shop_items.remove(item)

        shop_slots_count = len(remain_shop_items)
        shop_nonitem_count = len(world.shop_prices)
        shop_item_count = shop_slots_count - shop_nonitem_count

        pool.extend(random.sample(remain_shop_items, shop_item_count))
        if shop_nonitem_count:
            pool.extend(get_junk_item(shop_nonitem_count))
        if world.shopsanity == '0':
            pool.extend(normal_rupees)
        else:
            pool.extend(shopsanity_rupees)

    if world.shuffle_scrubs != 'off':
        if world.dungeon_mq['Deku Tree']:
            pool.append('Deku Shield')
        if world.dungeon_mq['Dodongos Cavern']:
            pool.extend(['Deku Stick (1)', 'Deku Shield', 'Recovery Heart'])
        else:
            pool.extend(['Deku Nuts (5)', 'Deku Stick (1)', 'Deku Shield'])
        if not world.dungeon_mq['Jabu Jabus Belly']:
            pool.append('Deku Nuts (5)')
        if world.dungeon_mq['Ganons Castle']:
            pool.extend(['Bombs (5)', 'Recovery Heart', 'Rupees (5)', 'Deku Nuts (5)'])
        else:
            pool.extend(['Bombs (5)', 'Recovery Heart', 'Rupees (5)'])
        pool.extend(deku_scrubs_items)
        for _ in range(7):
            pool.append('Arrows (30)' if random.randint(0,3) > 0 else 'Deku Seeds (30)')

    else:
        if world.dungeon_mq['Deku Tree']:
            placed_items['Deku Tree MQ Deku Scrub'] = 'Buy Deku Shield'
            skip_in_spoiler_locations.append('Deku Tree MQ Deku Scrub')
        if world.dungeon_mq['Dodongos Cavern']:
            placed_items['Dodongos Cavern MQ Deku Scrub Lobby Rear'] = 'Buy Deku Stick (1)'
            placed_items['Dodongos Cavern MQ Deku Scrub Lobby Front'] = 'Buy Deku Seeds (30)'
            placed_items['Dodongos Cavern MQ Deku Scrub Staircase'] = 'Buy Deku Shield'
            placed_items['Dodongos Cavern MQ Deku Scrub Side Room Near Lower Lizalfos'] = 'Buy Red Potion [30]'
            skip_in_spoiler_locations.extend(['Dodongos Cavern MQ Deku Scrub Lobby Rear', 
                'Dodongos Cavern MQ Deku Scrub Lobby Front', 
                'Dodongos Cavern MQ Deku Scrub Staircase', 
                'Dodongos Cavern MQ Deku Scrub Side Room Near Lower Lizalfos'])
        else:
            placed_items['Dodongos Cavern Deku Scrub Near Bomb Bag Left'] = 'Buy Deku Nut (5)'
            placed_items['Dodongos Cavern Deku Scrub Side Room Near Dodongos'] = 'Buy Deku Stick (1)'
            placed_items['Dodongos Cavern Deku Scrub Near Bomb Bag Right'] = 'Buy Deku Seeds (30)'
            placed_items['Dodongos Cavern Deku Scrub Lobby'] = 'Buy Deku Shield'
            skip_in_spoiler_locations.extend(['Dodongos Cavern Deku Scrub Near Bomb Bag Left',
                'Dodongos Cavern Deku Scrub Side Room Near Dodongos',
                'Dodongos Cavern Deku Scrub Near Bomb Bag Right',
                'Dodongos Cavern Deku Scrub Lobby'])
        if not world.dungeon_mq['Jabu Jabus Belly']:
            placed_items['Jabu Jabus Belly Deku Scrub'] = 'Buy Deku Nut (5)'
            skip_in_spoiler_locations.append('Jabu Jabus Belly Deku Scrub')
        if world.dungeon_mq['Ganons Castle']:
            placed_items['Ganons Castle MQ Deku Scrub Right'] = 'Buy Deku Nut (5)'
            placed_items['Ganons Castle MQ Deku Scrub Center-Left'] = 'Buy Bombs (5) [35]'
            placed_items['Ganons Castle MQ Deku Scrub Center'] = 'Buy Arrows (30)'
            placed_items['Ganons Castle MQ Deku Scrub Center-Right'] = 'Buy Red Potion [30]'
            placed_items['Ganons Castle MQ Deku Scrub Left'] = 'Buy Green Potion'
            skip_in_spoiler_locations.extend(['Ganons Castle MQ Deku Scrub Right',
                'Ganons Castle MQ Deku Scrub Center-Left',
                'Ganons Castle MQ Deku Scrub Center',
                'Ganons Castle MQ Deku Scrub Center-Right',
                'Ganons Castle MQ Deku Scrub Left'])
        else:
            placed_items['Ganons Castle Deku Scrub Center-Left'] = 'Buy Bombs (5) [35]'
            placed_items['Ganons Castle Deku Scrub Center-Right'] = 'Buy Arrows (30)'
            placed_items['Ganons Castle Deku Scrub Right'] = 'Buy Red Potion [30]'
            placed_items['Ganons Castle Deku Scrub Left'] = 'Buy Green Potion'
            skip_in_spoiler_locations.extend(['Ganons Castle Deku Scrub Right',
                'Ganons Castle Deku Scrub Center-Left',
                'Ganons Castle Deku Scrub Center-Right',
                'Ganons Castle Deku Scrub Left'])
        placed_items.update(vanilla_deku_scrubs)
        skip_in_spoiler_locations.extend(vanilla_deku_scrubs.keys())

    pool.extend(alwaysitems)
    
    if world.dungeon_mq['Deku Tree']:
        pool.extend(DT_MQ)
    else:
        pool.extend(DT_vanilla)
    if world.dungeon_mq['Dodongos Cavern']:
        pool.extend(DC_MQ)
    else:
        pool.extend(DC_vanilla)
    if world.dungeon_mq['Jabu Jabus Belly']:
        pool.extend(JB_MQ)
    if world.dungeon_mq['Forest Temple']:
        pool.extend(FoT_MQ)
    else:
        pool.extend(FoT_vanilla)
    if world.dungeon_mq['Fire Temple']:
        pool.extend(FiT_MQ)
    else:
        pool.extend(FiT_vanilla)
    if world.dungeon_mq['Spirit Temple']:
        pool.extend(SpT_MQ)
    else:
        pool.extend(SpT_vanilla)
    if world.dungeon_mq['Shadow Temple']:
        pool.extend(ShT_MQ)
    else:
        pool.extend(ShT_vanilla)
    if not world.dungeon_mq['Bottom of the Well']:
        pool.extend(BW_vanilla)
    if world.dungeon_mq['Gerudo Training Ground']:
        pool.extend(GTG_MQ)
    else:
        pool.extend(GTG_vanilla)
    if world.dungeon_mq['Ganons Castle']:
        pool.extend(GC_MQ)
    else:
        pool.extend(GC_vanilla)

    for i in range(bottle_count):
        if i >= ruto_bottles:
            bottle = random.choice(normal_bottles)
            pool.append(bottle)
        else:
            pool.append('Rutos Letter')

    earliest_trade = tradeitemoptions.index(world.logic_earliest_adult_trade)
    latest_trade = tradeitemoptions.index(world.logic_latest_adult_trade)
    if earliest_trade > latest_trade:
        earliest_trade, latest_trade = latest_trade, earliest_trade
    tradeitem = random.choice(tradeitems[earliest_trade:latest_trade+1])
    world.selected_adult_trade_item = tradeitem
    pool.append(tradeitem)

    pool.extend(songlist)
    if world.shuffle_song_items == 'any' and world.item_pool_value == 'plentiful':
        pending_junk_pool.extend(songlist)

    if world.free_scarecrow:
        item = world.create_item('Scarecrow Song')
        world.multiworld.push_precollected(item)
        world.remove_from_start_inventory.append(item.name)
    
    if world.no_epona_race:
        item = world.create_item('Epona')
        world.multiworld.push_precollected(item)
        world.remove_from_start_inventory.append(item.name)

    if world.shuffle_mapcompass == 'remove' or world.shuffle_mapcompass == 'startwith':
        for item in [item for dungeon in world.dungeons for item in dungeon.dungeon_items]:
            world.multiworld.push_precollected(item)
            world.remove_from_start_inventory.append(item.name)
            pool.extend(get_junk_item())
    if world.shuffle_smallkeys == 'remove':
        for item in [item for dungeon in world.dungeons for item in dungeon.small_keys]:
            world.multiworld.push_precollected(item)
            world.remove_from_start_inventory.append(item.name)
            pool.extend(get_junk_item())
    if world.shuffle_bosskeys == 'remove':
        for item in [item for dungeon in world.dungeons if dungeon.name != 'Ganons Castle' for item in dungeon.boss_key]:
            world.multiworld.push_precollected(item)
            world.remove_from_start_inventory.append(item.name)
            pool.extend(get_junk_item())
    if world.shuffle_ganon_bosskey in ['remove', 'triforce']:
        for item in [item for dungeon in world.dungeons if dungeon.name == 'Ganons Castle' for item in dungeon.boss_key]:
            world.multiworld.push_precollected(item)
            world.remove_from_start_inventory.append(item.name)
            pool.extend(get_junk_item())

    if world.shuffle_mapcompass == 'vanilla':
        for location, item in vanillaMC.items():
            try:
                world.get_location(location)
                placed_items[location] = item
            except KeyError:
                continue
    if world.shuffle_smallkeys == 'vanilla':
        for location, item in vanillaSK.items():
            try:
                world.get_location(location)
                placed_items[location] = item
            except KeyError:
                continue
        # Logic cannot handle vanilla key layout in some dungeons
        # this is because vanilla expects the dungeon major item to be
        # locked behind the keys, which is not always true in rando.
        # We can resolve this by starting with some extra keys
        if world.dungeon_mq['Spirit Temple']:
            # Yes somehow you need 3 keys. This dungeon is bonkers
            items = [world.create_item('Small Key (Spirit Temple)') for i in range(3)]
            for item in items:
                world.multiworld.push_precollected(item)
                world.remove_from_start_inventory.append(item.name)
        #if not world.dungeon_mq['Fire Temple']:
        #    world.state.collect(ItemFactory('Small Key (Fire Temple)'))
    if world.shuffle_bosskeys == 'vanilla':
        for location, item in vanillaBK.items():
            try:
                world.get_location(location)
                placed_items[location] = item
            except KeyError:
                continue


    if not world.keysanity and not world.dungeon_mq['Fire Temple']:
        item = world.create_item('Small Key (Fire Temple)')
        world.multiworld.push_precollected(item)
        world.remove_from_start_inventory.append(item.name)

    if world.triforce_hunt:
        triforce_count = int((Decimal(100 + world.extra_triforce_percentage)/100 * world.triforce_goal).to_integral_value(rounding=ROUND_HALF_UP))
        pending_junk_pool.extend(['Triforce Piece'] * triforce_count)

    if world.shuffle_ganon_bosskey == 'on_lacs':
        placed_items['ToT Light Arrows Cutscene'] = 'Boss Key (Ganons Castle)'
    elif world.shuffle_ganon_bosskey == 'vanilla':
        placed_items['Ganons Tower Boss Key Chest'] = 'Boss Key (Ganons Castle)'

    if world.item_pool_value == 'plentiful':
        pool.extend(easy_items)
    else:
        pool.extend(normal_items)

    if not world.shuffle_kokiri_sword:
        replace_max_item(pool, 'Kokiri Sword', 0)

    if world.junk_ice_traps == 'off': 
        replace_max_item(pool, 'Ice Trap', 0)
    elif world.junk_ice_traps == 'onslaught':
        for item in [item for item, weight in junk_pool_base] + ['Recovery Heart', 'Bombs (20)', 'Arrows (30)']:
            replace_max_item(pool, item, 0)

    for item,max in item_difficulty_max[world.item_pool_value].items():
        replace_max_item(pool, item, max)

    if world.damage_multiplier in ['ohko', 'quadruple'] and world.item_pool_value == 'minimal':
        pending_junk_pool.append('Nayrus Love')

    # world.distribution.alter_pool(world, pool)

    # Make sure our pending_junk_pool is empty. If not, remove some random junk here.
    if pending_junk_pool:

        remove_junk_pool, _ = zip(*junk_pool_base)
        # Omits Rupees (200) and Deku Nuts (10)
        remove_junk_pool = list(remove_junk_pool) + ['Recovery Heart', 'Bombs (20)', 'Arrows (30)', 'Ice Trap']

        junk_candidates = [item for item in pool if item in remove_junk_pool]
        if len(pending_junk_pool) > len(junk_candidates):
            excess = len(pending_junk_pool) - len(junk_candidates)
            if world.triforce_hunt:
                raise RuntimeError(f"Items in the pool for player {world.player} exceed locations. Add {excess} location(s) or remove {excess} triforce piece(s).")
        while pending_junk_pool:
            pending_item = pending_junk_pool.pop()
            if not junk_candidates:
                raise RuntimeError("Not enough junk exists in item pool for %s to be added." % pending_item)
            junk_item = random.choice(junk_candidates)
            junk_candidates.remove(junk_item)
            pool.remove(junk_item)
            pool.append(pending_item)

    return (pool, placed_items, skip_in_spoiler_locations)

def add_dungeon_items(ootworld):
    """Adds maps, compasses, small keys, boss keys, and Ganon boss key into item pool if they are not placed."""
    skip_add_settings = {'remove', 'startwith', 'vanilla', 'on_lacs'}
    for dungeon in ootworld.dungeons:
        if ootworld.shuffle_mapcompass not in skip_add_settings:
            ootworld.itempool.extend(dungeon.dungeon_items)
        if ootworld.shuffle_smallkeys not in skip_add_settings:
            ootworld.itempool.extend(dungeon.small_keys)
        if dungeon.name != 'Ganons Castle' and ootworld.shuffle_bosskeys not in skip_add_settings:
            ootworld.itempool.extend(dungeon.boss_key)
        if dungeon.name == 'Ganons Castle' and ootworld.shuffle_ganon_bosskey not in skip_add_settings:
            ootworld.itempool.extend(dungeon.boss_key)
