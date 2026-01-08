import os, sys
from BaseClasses import ItemClassification, Item
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger("Final Fantasy V Career Day")
arch_item_offset = 352000000



EXDEATH_ITEM_ID = 1200
WORLD2_ACCESS_ITEM_ID = 1201
WORLD3_ACCESS_ITEM_ID = 1202
EXDEATH_W2_ITEM_ID = 1203


# I tried making these integers for better performance
# but AutoWorld.py method get_data_package_data()
# tries to sort this list, and cannot because "Everything" is a group name

# So I changed them back to strings...

ITEM_CODE_UNIQUE = '1'
ITEM_CODE_ABILITIES = '2'
ITEM_CODE_CRYSTALS = '3'
ITEM_CODE_FUNGIBLE = '4'
ITEM_CODE_GIL = '5'
ITEM_CODE_ITEM = '6'
ITEM_CODE_KEY_ITEMS = '7'
ITEM_CODE_MAGIC = '8'
ITEM_CODE_VICTORY = '9'
ITEM_CODE_MIB_REWARD = '10'
ITEM_CODE_MIB_REWARD_PROG = '11'

#Job Codes: Used for grouping together abilities and crystals for additional settings
JOB_CODE_KNIGHT = '12'
JOB_CODE_MONK = '13'
JOB_CODE_THIEF = '14'
JOB_CODE_DRAGOON = '15'
JOB_CODE_NINJA = '16'
JOB_CODE_SAMURAI = '17'
JOB_CODE_BERSERKER = '18'
JOB_CODE_HUNTER = '19'
JOB_CODE_MYSTIC_KNIGHT = '20'
JOB_CODE_WHITE_MAGE = '21'
JOB_CODE_BLACK_MAGE = '22'
JOB_CODE_TIME_MAGE = '23'
JOB_CODE_SUMMONER = '24'
JOB_CODE_BLUE_MAGE = '25'
JOB_CODE_RED_MAGE = '26'
JOB_CODE_TRAINER = '27'
JOB_CODE_CHEMIST = '28'
JOB_CODE_GEOMANCER = '29'
JOB_CODE_BARD = '30'
JOB_CODE_DANCER = '31'
JOB_CODE_MIMIC = '32'
JOB_CODE_FREELANCER = '33'

MAGIC_CODE_TIER_1 = '34'
MAGIC_CODE_TIER_2 = '35'
MAGIC_CODE_TIER_3 = '36'

EVENT_CODE = None

#this is how we'll handle crystal selections now so we can do more with job and ability associations
job_selection_dict = {
    "Knight": '12',
    "Monk": '13',
    "Thief": '14',
    "Dragoon": '15',
    "Ninja": '16',
    "Samurai": '17',
    "Berserker": '18',
    "Hunter": '19',
    "Mystic Knight": '20',
    "White Mage": '21',
    "Black Mage": '22',
    "Time Mage": '23',
    "Summoner": '24',
    "Blue Mage": '25',
    "Red Mage": '26',
    "Trainer": '27',
    "Chemist": '28',
    "Geomancer": '29',
    "Bard": '30',
    "Dancer": '31',
    "Mimic": '32',
    "Freelancer": '33',
}

class ItemData:
    def __init__(self, item_id, classification, groups):
        self.groups = groups
        self.classification = classification
        self.id = None if item_id is None else item_id + arch_item_offset

class FFVCDEventData:
    def __init__(self, event_location, event_item, classification):
        self.event_location = event_location
        self.event_item = event_item
        self.classification = classification
        self.code = EVENT_CODE

def create_item(name: str, classification, item_data_id, player, groups) -> Item:
    return FFVCDItem(name, classification, item_data_id, player, groups)

#not sure this is necessary but wanted to exclude the groups and make absolutely sure everything was set to None for events.
def create_event_item(event: str, classification, EVENT_CODE, player) -> Item:
    return FFVCDEventItem(event, classification.progression, EVENT_CODE, player)

def create_world_events(world):
    for event in [i for i in event_table]:
        event_data = event_table[event]
        new_event_item = create_event_item(event_data.event_item, event_data.classification, event_data.code, world.player)
        new_event_loc = world.multiworld.get_location(event_data.event_location, world.player)
        new_event_loc.address = event_data.code
        new_event_loc.event = True
        new_event_loc.place_locked_item(new_event_item)

def create_world_items(world, trapped_chests_flag = False, chosen_mib_locations = None):
    mib_items_to_place = []
    mib_item_pool = []
    mib_key_item_excludes = []
    
    ##################
    # AP Models Events as items so let's create our events here
    ##################
    create_world_events(world)

    ##################
    # trapped chest items handling
    ##################
    
    if trapped_chests_flag and chosen_mib_locations and world.options.trapped_chests_settings in [0,1]:
        
        mib_item_data = dict({(i, item_table[i]) for i in item_table \
                              if(ITEM_CODE_MIB_REWARD in item_table[i].groups or \
                                (world.options.trapped_chests_settings == 1 and ITEM_CODE_MIB_REWARD_PROG in item_table[i].groups \
                                  and world.options.progression_checks != 0))})
        sorted_list = sorted(mib_item_data.items())
        sorted_dict = {}
        for key, value in sorted_list:
            sorted_dict[key] = value
        mib_item_data = sorted_dict
        for k, v in mib_item_data.items():
            mib_item_pool.append(create_item(k, v.classification, v.id, world.player, v.groups))
            
        mib_items_to_place = world.random.sample(mib_item_pool, k=len(chosen_mib_locations))
        for i in mib_items_to_place:
            if i.classification == ItemClassification.progression:
                mib_key_item_excludes.append(i.name)
    
    ##################    
    # add progression items
    ##################
    placed_items = []
    for key_item_name in [i for i in item_table if ITEM_CODE_KEY_ITEMS in item_table[i].groups]:
        item_data = item_table[key_item_name]
        if item_data.classification == ItemClassification.progression and key_item_name not in mib_key_item_excludes:
            
            new_item = create_item(key_item_name, item_data.classification, item_data.id, \
                                   world.player, item_data.groups)
            placed_items.append(new_item)


    ###############
    # Shuffle job list
    # with how jobs/abilities are being handled now this is a simpler way to do the logic.
    ###############
    available_job_groups = []
    unavailable_job_groups = []
    starting_job_groups = []
    initial_job_list = []
    shuffled_job_list = []


    for job_name in job_selection_dict:
        if job_name in world.options.jobs_included:
            initial_job_list.append(job_selection_dict[job_name])
    world.random.shuffle(initial_job_list)
    while True:
        if (initial_job_list[-1] in [JOB_CODE_KNIGHT,JOB_CODE_MONK,JOB_CODE_THIEF,JOB_CODE_DRAGOON,JOB_CODE_NINJA,
                                   JOB_CODE_SAMURAI,JOB_CODE_BERSERKER,JOB_CODE_HUNTER,JOB_CODE_MYSTIC_KNIGHT,
                                   JOB_CODE_TRAINER,JOB_CODE_CHEMIST,JOB_CODE_GEOMANCER,JOB_CODE_BARD,JOB_CODE_DANCER] \
                                   and initial_job_list[-2] in [JOB_CODE_WHITE_MAGE,JOB_CODE_BLACK_MAGE,JOB_CODE_TIME_MAGE,
                                   JOB_CODE_SUMMONER,JOB_CODE_BLUE_MAGE,JOB_CODE_RED_MAGE]) or \
                                   (initial_job_list[-1] in [JOB_CODE_WHITE_MAGE,JOB_CODE_BLACK_MAGE,JOB_CODE_TIME_MAGE,
                                   JOB_CODE_SUMMONER,JOB_CODE_BLUE_MAGE,JOB_CODE_RED_MAGE] \
                                   and initial_job_list[-2] in [JOB_CODE_KNIGHT,JOB_CODE_MONK,JOB_CODE_THIEF,JOB_CODE_DRAGOON,
                                   JOB_CODE_NINJA,JOB_CODE_SAMURAI,JOB_CODE_BERSERKER,JOB_CODE_HUNTER,JOB_CODE_MYSTIC_KNIGHT,
                                   JOB_CODE_TRAINER,JOB_CODE_CHEMIST,JOB_CODE_GEOMANCER,JOB_CODE_BARD,JOB_CODE_DANCER]):
            early_crystal = initial_job_list[-2]
            break
        else:
            world.random.shuffle(initial_job_list)
            
            
    # This method of assignment guarantees that new memory is allocated for the shuffled list 
    # instead of initial job list and shuffled job list pointing to the same memory
    for job in initial_job_list:
        shuffled_job_list.append(job)
    job_count = len(initial_job_list)

    ###############
    # FOUR JOB ENABLED
    # set 4 starting jobs
    ###############
    if world.options.four_job:
        for i in range(4):
            if job_count < 4:
                raise Exception("4 Job Mode Requires 4 jobs enabled.")
            starting_job_groups.append(shuffled_job_list.pop())

        starting_crystals = [i for i in item_table if ITEM_CODE_CRYSTALS in item_table[i].groups and any(y in starting_job_groups for y in item_table[i].groups)]

    ###############
    # FOUR JOB DISABLED
    # add crystals only if four job not enabled
    ###############
    else:
        first = 0
        # first choose starting crystal
        starting_job_groups.append(shuffled_job_list.pop())
        starting_crystals = [i for i in item_table if ITEM_CODE_CRYSTALS in item_table[i].groups \
                             and any(y in starting_job_groups for y in item_table[i].groups)]
        
        for i in range(world.options.random_job_count - 1): #minus 1 because of starting job
            if i > job_count-2: #minus 2 because starting job and i starting at 0
                break
            available_job_groups.append(shuffled_job_list.pop())
        jobs_to_place = [i for i in item_table if ITEM_CODE_CRYSTALS in item_table[i].groups \
                          and any(y in available_job_groups for y in item_table[i].groups)] 
        for item_name in [i for i in item_table if ITEM_CODE_CRYSTALS in item_table[i].groups]:
            if item_name in jobs_to_place:
                item_data = item_table[item_name]
                new_item = create_item(item_name, item_data.classification, item_data.id, \
                                       world.player, item_data.groups)
                if early_crystal in item_data.groups:
                    world.multiworld.early_items[world.player][item_name] = 1
                placed_items.append(new_item)
        
    ###############
    # ABILITIES SETTINGS
    # if enabled with 4 job mode then place only abilities associated with starting jobs
    ###############
    #set all job groups to available job groups, for abilities there's no reason for distinction between starting and available
    for job in starting_job_groups:
        available_job_groups.append(job)

    # All job abilities
    if world.options.ability_settings == 0 and not world.options.four_job: 
        for item_name in [i for i in item_table if ITEM_CODE_ABILITIES in item_table[i].groups \
                          and any(y in initial_job_list for y in item_table[i].groups)]:
            if item_name not in starting_crystals:
                item_data = item_table[item_name]
                new_item = create_item(item_name, item_data.classification, item_data.id, \
                                    world.player, item_data.groups)
                placed_items.append(new_item)
    #Only for Available Jobs
    elif world.options.ability_settings == 1:
        for item_name in [i for i in item_table if ITEM_CODE_ABILITIES in item_table[i].groups \
                          and any(y in available_job_groups for y in item_table[i].groups)]:
            if item_name not in starting_crystals:
                item_data = item_table[item_name]
                new_item = create_item(item_name, item_data.classification, item_data.id, \
                                    world.player, item_data.groups)
                placed_items.append(new_item)
    #Available Jobs Plus Extra
    elif world.options.ability_settings == 2 and not world.options.four_job:
        #add additonal job groups
        for i in range(world.options.job_group_abilities_number):
            if len(available_job_groups) >= job_count:
                break
            available_job_groups.append(shuffled_job_list.pop())
        
        for item_name in [i for i in item_table if ITEM_CODE_ABILITIES in item_table[i].groups \
                           and any(y in available_job_groups for y in item_table[i].groups)]:
            if item_name not in starting_crystals:
                item_data = item_table[item_name]
                new_item = create_item(item_name, item_data.classification, item_data.id, \
                                    world.player, item_data.groups)
                placed_items.append(new_item)
    #Random by Job
    elif world.options.ability_settings == 3 and not world.options.four_job:
        random_job_groups = world.multiworld.random.sample(initial_job_list,world.options.job_group_abilities_number) 
        for item_name in [i for i in item_table if ITEM_CODE_ABILITIES in item_table[i].groups \
                           and any(y in random_job_groups for y in item_table[i].groups)]:
            if item_name not in starting_crystals:
                item_data = item_table[item_name]
                new_item = create_item(item_name, item_data.classification, item_data.id, \
                                    world.player, item_data.groups)
                placed_items.append(new_item)
    #Random All
    elif world.options.ability_settings == 4 and not world.options.four_job:
        random_any_ability_odds = world.multiworld.random.randint(1,101)
        for item_name in [i for i in item_table if ITEM_CODE_ABILITIES in item_table[i].groups  \
                          and any(y in initial_job_list for y in item_table[i].groups)]:
            random_individual_ability_odds = world.multiworld.random.randint(1,101)
            if item_name not in starting_crystals and random_individual_ability_odds > random_any_ability_odds:
                item_data = item_table[item_name]
                new_item = create_item(item_name, item_data.classification, item_data.id, \
                                    world.player, item_data.groups)
                placed_items.append(new_item)
    #Random only unavailable
    elif world.options.ability_settings == 6 and not world.options.four_job:
        for job in initial_job_list:
            if job not in available_job_groups:
                if (len(available_job_groups) + len(unavailable_job_groups)) >= job_count:
                    break
                elif len(unavailable_job_groups) > world.options.job_group_abilities_number:
                    break
                unavailable_job_groups.append(job)
        for item_name in [i for i in item_table if ITEM_CODE_ABILITIES in item_table[i].groups \
                          and any(y in unavailable_job_groups for y in item_table[i].groups)]:
            if item_name not in starting_crystals:
                item_data = item_table[item_name]
                new_item = create_item(item_name, item_data.classification, item_data.id, \
                                    world.player, item_data.groups)
                placed_items.append(new_item)
    #Don't Place skips this step
    
    ###############
    # PLACE ABILITIES DISABLED
    # do not add abilities only if diabled
    ###############

    ###############
    # PLACE MAGIC
    ###############
    # This will be used to identify all potentially useful magic associated to existing abilities or job crystals in the world.
    if world.options.only_usable_magic:
        placed_job_group_list = []
        for item in placed_items:
            item_groups = getattr(item,'groups')
            for group in [i for i in item_groups if i in initial_job_list]:
                placed_job_group_list.append(group)
        
        for group in [i for i in available_job_groups if i in initial_job_list]:
                placed_job_group_list.append(group)

        placed_job_group_list = list(set(placed_job_group_list))

    magic_exlude_list = []
    if world.options.disable_tier_1_magic and world.options.disable_tier_2_magic and world.options.disable_tier_3_magic:
        raise Exception("Must include at least one tier of magic. Please ajust settings.")

    if world.options.disable_tier_1_magic:
        magic_exlude_list.append(MAGIC_CODE_TIER_1)
    if world.options.disable_tier_2_magic:
        magic_exlude_list.append(MAGIC_CODE_TIER_2)
    if world.options.disable_tier_3_magic:
        magic_exlude_list.append(MAGIC_CODE_TIER_3)

    if world.options.only_usable_magic:
        for item_name in [i for i in item_table\
                                if ITEM_CODE_MAGIC in item_table[i].groups and \
                                    not any(y in magic_exlude_list for y in item_table[i].groups)\
                                        and any(x in placed_job_group_list for x in item_table[i].groups)]:
                
                if item_name not in starting_crystals:
                    
                    item_data = item_table[item_name]
                    new_item = create_item(item_name, item_data.classification, item_data.id, \
                                        world.player, item_data.groups)
                    placed_items.append(new_item)

    else:
        for item_name in [i for i in item_table\
                                if ITEM_CODE_MAGIC in item_table[i].groups and \
                                    not any(y in magic_exlude_list for y in item_table[i].groups)]:
                
                if item_name not in starting_crystals:
                    
                    item_data = item_table[item_name]
                    new_item = create_item(item_name, item_data.classification, item_data.id, \
                                        world.player, item_data.groups)
                    placed_items.append(new_item)   

    for item_name in [i for i in item_table\
                              if ITEM_CODE_GIL in item_table[i].groups]:
            
            if item_name not in starting_crystals:
                
                item_data = item_table[item_name]
                new_item = create_item(item_name, item_data.classification, item_data.id, \
                                       world.player, item_data.groups)
                placed_items.append(new_item)   
    

    
    # then calculate remaining    
    locations_this_world = [i for i in world.multiworld.get_locations(world.player)]
    
    item_count_to_place = len(locations_this_world) - len(mib_items_to_place) - len(placed_items)
    
    # get mib item names, if any
    mib_already_chosen_items = [i.name for i in mib_items_to_place]
    
    filler_list = [i for i in item_table if ITEM_CODE_FUNGIBLE in \
                    item_table[i].groups and i not in mib_already_chosen_items]
    filler_count = len(filler_list)

    # to facilitate more customization we'll make the filler able to dynamically resize using a while loop
    while item_count_to_place > 0: 
        if item_count_to_place > filler_count:
            sample = filler_count
        else:
            sample = item_count_to_place

        for item_name in world.multiworld.random.sample([i for i in item_table if ITEM_CODE_FUNGIBLE in \
                                                        item_table[i].groups and i not in mib_already_chosen_items
                                                        ], sample):
            item_data = item_table[item_name]
            new_item = create_item(item_name, item_data.classification, item_data.id, \
                                                    world.player, item_data.groups)
                
            placed_items.append(new_item)

            if len(placed_items) + len(mib_items_to_place) >= len(locations_this_world) - len(event_table):
                break

        item_count_to_place -= filler_count

    world.random.shuffle(placed_items)
    # add remaining to itempool
    for new_item in placed_items:
        world.multiworld.itempool.append(new_item)
        
    return starting_crystals, placed_items, mib_items_to_place

item_table = {
    "Knight Crystal" : ItemData(100, ItemClassification.useful, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS,JOB_CODE_KNIGHT]),
    "Monk Crystal" : ItemData(101, ItemClassification.useful, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS,JOB_CODE_MONK]),
    "Thief Crystal" : ItemData(102, ItemClassification.useful, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS,JOB_CODE_THIEF]),
    "Dragoon Crystal" : ItemData(103, ItemClassification.useful, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS,JOB_CODE_DRAGOON]),
    "Ninja Crystal" : ItemData(104, ItemClassification.useful, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS,JOB_CODE_NINJA]),
    "Samurai Crystal" : ItemData(105, ItemClassification.useful, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS,JOB_CODE_SAMURAI]),
    "Berserker Crystal" : ItemData(106, ItemClassification.useful, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS,JOB_CODE_BERSERKER]),
    "Hunter Crystal" : ItemData(107, ItemClassification.useful, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS,JOB_CODE_HUNTER]),
    "MysticKnight Crystal" : ItemData(108, ItemClassification.useful, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS,JOB_CODE_MYSTIC_KNIGHT]),
    "WhiteMage Crystal" : ItemData(109, ItemClassification.useful, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS,JOB_CODE_WHITE_MAGE]),
    "BlackMage Crystal" : ItemData(110, ItemClassification.useful, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS,JOB_CODE_BLACK_MAGE]),
    "TimeMage Crystal" : ItemData(111, ItemClassification.useful, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS,JOB_CODE_TIME_MAGE]),
    "Summoner Crystal" : ItemData(112, ItemClassification.useful, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS,JOB_CODE_SUMMONER]),
    "BlueMage Crystal" : ItemData(113, ItemClassification.useful, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS,JOB_CODE_BLUE_MAGE]),
    "RedMage Crystal" : ItemData(114, ItemClassification.useful, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS,JOB_CODE_RED_MAGE]),
    "Trainer Crystal" : ItemData(115, ItemClassification.progression, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS,JOB_CODE_TRAINER]),
    "Chemist Crystal" : ItemData(116, ItemClassification.useful, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS,JOB_CODE_CHEMIST]),
    "Geomancer Crystal" : ItemData(117, ItemClassification.useful, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS,JOB_CODE_GEOMANCER]),
    "Bard Crystal" : ItemData(118, ItemClassification.useful, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS,JOB_CODE_BARD]),
    "Dancer Crystal" : ItemData(119, ItemClassification.useful, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS,JOB_CODE_DANCER]),
    "Mimic Crystal" : ItemData(120, ItemClassification.useful, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS,JOB_CODE_MIMIC]),
    "Freelancer Crystal" : ItemData(121, ItemClassification.useful, [ITEM_CODE_UNIQUE, ITEM_CODE_CRYSTALS,JOB_CODE_FREELANCER]),
    
    #"Fire Sword Magic" : ItemData(200, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_MYSTIC_KNIGHT, MAGIC_CODE_TIER_1]),
    "Ice Sword Magic" : ItemData(201, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_MYSTIC_KNIGHT, MAGIC_CODE_TIER_1]),
    "Bolt Sword Magic" : ItemData(202, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_MYSTIC_KNIGHT, MAGIC_CODE_TIER_1]),
    "Venom Sword Magic" : ItemData(203, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_MYSTIC_KNIGHT, MAGIC_CODE_TIER_1]),
    "Mute Sword Magic" : ItemData(204, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_MYSTIC_KNIGHT, MAGIC_CODE_TIER_1]),
    "Sleep Sword Magic" : ItemData(205, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_MYSTIC_KNIGHT, MAGIC_CODE_TIER_1]),
    "Fire2 Sword Magic" : ItemData(206, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_MYSTIC_KNIGHT, MAGIC_CODE_TIER_2]),
    "Ice2 Sword Magic" : ItemData(207, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_MYSTIC_KNIGHT, MAGIC_CODE_TIER_2]),
    "Bolt2 Sword Magic" : ItemData(208, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_MYSTIC_KNIGHT, MAGIC_CODE_TIER_2]),
    "Drain Sword Magic" : ItemData(209, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_MYSTIC_KNIGHT, MAGIC_CODE_TIER_2]),
    "Break Sword Magic" : ItemData(210, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_MYSTIC_KNIGHT, MAGIC_CODE_TIER_2]),
    "Bio Sword Magic" : ItemData(211, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_MYSTIC_KNIGHT, MAGIC_CODE_TIER_2]),
    "Fire3 Sword Magic" : ItemData(212, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_MYSTIC_KNIGHT, MAGIC_CODE_TIER_3]),
    "Ice3 Sword Magic" : ItemData(213, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_MYSTIC_KNIGHT, MAGIC_CODE_TIER_3]),
    "Bolt3 Sword Magic" : ItemData(214, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_MYSTIC_KNIGHT, MAGIC_CODE_TIER_3]),
    "Holy Sword Magic" : ItemData(215, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_MYSTIC_KNIGHT, MAGIC_CODE_TIER_3]),
    "Flare Sword Magic" : ItemData(216, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_MYSTIC_KNIGHT, MAGIC_CODE_TIER_3]),
    "Psych Sword Magic" : ItemData(217, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_MYSTIC_KNIGHT, MAGIC_CODE_TIER_3]),
    "Cure White Magic" : ItemData(218, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_WHITE_MAGE,JOB_CODE_RED_MAGE, MAGIC_CODE_TIER_1]),
    "Scan White Magic" : ItemData(219, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_WHITE_MAGE,JOB_CODE_RED_MAGE, MAGIC_CODE_TIER_1]),
    "Antdt White Magic" : ItemData(220, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_WHITE_MAGE,JOB_CODE_RED_MAGE, MAGIC_CODE_TIER_1]),
    "Mute White Magic" : ItemData(221, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_WHITE_MAGE,JOB_CODE_RED_MAGE, MAGIC_CODE_TIER_1]),
    "Armor White Magic" : ItemData(222, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_WHITE_MAGE,JOB_CODE_RED_MAGE, MAGIC_CODE_TIER_1]),
    "Size White Magic" : ItemData(223, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_WHITE_MAGE,JOB_CODE_RED_MAGE, MAGIC_CODE_TIER_1]),
    "Cure2 White Magic" : ItemData(224, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_WHITE_MAGE,JOB_CODE_RED_MAGE, MAGIC_CODE_TIER_2]),
    "Life White Magic" : ItemData(225, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_WHITE_MAGE,JOB_CODE_RED_MAGE, MAGIC_CODE_TIER_2]),
    "Charm White Magic" : ItemData(226, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_WHITE_MAGE,JOB_CODE_RED_MAGE, MAGIC_CODE_TIER_2]),
    "Image White Magic" : ItemData(227, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_WHITE_MAGE, MAGIC_CODE_TIER_2]),
    "Shell White Magic" : ItemData(228, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_WHITE_MAGE, MAGIC_CODE_TIER_2]),
    "Heal White Magic" : ItemData(229, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_WHITE_MAGE, MAGIC_CODE_TIER_2]),
    "Cure3 White Magic" : ItemData(230, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_WHITE_MAGE, MAGIC_CODE_TIER_3]),
    "Wall White Magic" : ItemData(231, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_WHITE_MAGE, MAGIC_CODE_TIER_3]),
    "Bersk White Magic" : ItemData(232, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_WHITE_MAGE, MAGIC_CODE_TIER_3]),
    "Life2 White Magic" : ItemData(233, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_WHITE_MAGE, MAGIC_CODE_TIER_3]),
    "Holy White Magic" : ItemData(234, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_WHITE_MAGE, MAGIC_CODE_TIER_3]),
    "Dispel White Magic" : ItemData(235, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_WHITE_MAGE, MAGIC_CODE_TIER_3]),
    "Fire Black Magic" : ItemData(236, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLACK_MAGE,JOB_CODE_RED_MAGE, MAGIC_CODE_TIER_1]),
    "Ice Black Magic" : ItemData(237, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLACK_MAGE,JOB_CODE_RED_MAGE, MAGIC_CODE_TIER_1]),
    "Bolt Black Magic" : ItemData(238, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLACK_MAGE,JOB_CODE_RED_MAGE, MAGIC_CODE_TIER_1]),
    "Venom Black Magic" : ItemData(239, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLACK_MAGE,JOB_CODE_RED_MAGE, MAGIC_CODE_TIER_1]),
    "Sleep Black Magic" : ItemData(240, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLACK_MAGE,JOB_CODE_RED_MAGE, MAGIC_CODE_TIER_1]),
    "Toad Black Magic" : ItemData(241, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLACK_MAGE,JOB_CODE_RED_MAGE, MAGIC_CODE_TIER_1]),
    "Fire2 Black Magic" : ItemData(242, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLACK_MAGE,JOB_CODE_RED_MAGE, MAGIC_CODE_TIER_2]),
    "Ice2 Black Magic" : ItemData(243, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLACK_MAGE,JOB_CODE_RED_MAGE, MAGIC_CODE_TIER_2]),
    "Bolt2 Black Magic" : ItemData(244, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLACK_MAGE,JOB_CODE_RED_MAGE, MAGIC_CODE_TIER_2]),
    "Drain Black Magic" : ItemData(245, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLACK_MAGE, MAGIC_CODE_TIER_2]),
    "Break Black Magic" : ItemData(246, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLACK_MAGE, MAGIC_CODE_TIER_2]),
    "Bio Black Magic" : ItemData(247, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLACK_MAGE, MAGIC_CODE_TIER_2]),
    "Fire3 Black Magic" : ItemData(248, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLACK_MAGE, MAGIC_CODE_TIER_3]),
    "Ice3 Black Magic" : ItemData(249, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLACK_MAGE, MAGIC_CODE_TIER_3]),
    "Bolt3 Black Magic" : ItemData(250, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLACK_MAGE, MAGIC_CODE_TIER_3]),
    "Flare Black Magic" : ItemData(251, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLACK_MAGE, MAGIC_CODE_TIER_3]),
    "Doom Black Magic" : ItemData(252, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLACK_MAGE, MAGIC_CODE_TIER_3]),
    "Psych Black Magic" : ItemData(253, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLACK_MAGE, MAGIC_CODE_TIER_3]),
    #"Drag Time Magic" : ItemData(254, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_TIME_MAGE, MAGIC_CODE_TIER_1]),
    "Slow Time Magic" : ItemData(255, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_TIME_MAGE, MAGIC_CODE_TIER_1]),
    "Regen Time Magic" : ItemData(256, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_TIME_MAGE, MAGIC_CODE_TIER_1]),
    "Void Time Magic" : ItemData(257, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_TIME_MAGE, MAGIC_CODE_TIER_1]),
    "Haste Time Magic" : ItemData(258, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_TIME_MAGE, MAGIC_CODE_TIER_1]),
    "Float Time Magic" : ItemData(259, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_TIME_MAGE, MAGIC_CODE_TIER_1]),
    "Demi Time Magic" : ItemData(260, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_TIME_MAGE, MAGIC_CODE_TIER_2]),
    "Stop Time Magic" : ItemData(261, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_TIME_MAGE, MAGIC_CODE_TIER_2]),
    #"Exit Time Magic" : ItemData(255, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_TIME_MAGE, MAGIC_CODE_TIER_2]), world state is set such that using exit will always trigger leaving the rift
    "Comet Time Magic" : ItemData(263, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_TIME_MAGE, MAGIC_CODE_TIER_2]),
    "Slow2 Time Magic" : ItemData(264, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_TIME_MAGE, MAGIC_CODE_TIER_2]),
    "Reset Time Magic" : ItemData(265, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_TIME_MAGE, MAGIC_CODE_TIER_2]),
    "Qrter Time Magic" : ItemData(266, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_TIME_MAGE, MAGIC_CODE_TIER_3]),
    "Hast2 Time Magic" : ItemData(267, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_TIME_MAGE, MAGIC_CODE_TIER_3]),
    "Old Time Magic" : ItemData(268, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_TIME_MAGE, MAGIC_CODE_TIER_3]),
    "Meteo Time Magic" : ItemData(269, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_TIME_MAGE, MAGIC_CODE_TIER_3]),
    "Quick Time Magic" : ItemData(270, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_TIME_MAGE, MAGIC_CODE_TIER_3]),
    "Xzone Time Magic" : ItemData(271, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_TIME_MAGE, MAGIC_CODE_TIER_3]),
    "Chocob Esper Magic" : ItemData(272, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_SUMMONER, MAGIC_CODE_TIER_1]),
    "Sylph Esper Magic" : ItemData(273, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_SUMMONER, MAGIC_CODE_TIER_1]),
    "Remora Esper Magic" : ItemData(274, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_SUMMONER, MAGIC_CODE_TIER_1]),
    "Shiva Esper Magic" : ItemData(275, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_SUMMONER, MAGIC_CODE_TIER_1]),
    "Ramuh Esper Magic" : ItemData(276, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_SUMMONER, MAGIC_CODE_TIER_1]),
    "Ifrit Esper Magic" : ItemData(277, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_SUMMONER, MAGIC_CODE_TIER_1]),
    "Titan Esper Magic" : ItemData(278, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_SUMMONER, MAGIC_CODE_TIER_2]),
    "Golem Esper Magic" : ItemData(279, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_SUMMONER, MAGIC_CODE_TIER_2]),
    "Shoat Esper Magic" : ItemData(280, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_SUMMONER, MAGIC_CODE_TIER_2]),
    "Crbnkl Esper Magic" : ItemData(281, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_SUMMONER, MAGIC_CODE_TIER_2]),
    "Syldra Esper Magic" : ItemData(282, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_SUMMONER, MAGIC_CODE_TIER_2]),
    "Odin Esper Magic" : ItemData(283, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_SUMMONER, MAGIC_CODE_TIER_2]),
    "Phenix Esper Magic" : ItemData(284, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_SUMMONER, MAGIC_CODE_TIER_3]),
    "Levia Esper Magic" : ItemData(285, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_SUMMONER, MAGIC_CODE_TIER_3]),
    "Bahmut Esper Magic" : ItemData(286, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_SUMMONER, MAGIC_CODE_TIER_3]),
    "Power Song Magic" : ItemData(287, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BARD]),
    "Speed Song Magic" : ItemData(288, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BARD]),
    "Vitality Song Magic" : ItemData(289, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BARD]),
    "Magic Song Magic" : ItemData(290, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BARD]),
    "Hero Song Magic" : ItemData(291, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BARD]),
    "Requiem Song Magic" : ItemData(292, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BARD]),
    "Love Song Magic" : ItemData(293, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BARD]),
    "Charm Song Magic" : ItemData(294, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BARD]),
    "Condemn Blue Magic" : ItemData(295, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLUE_MAGE]),
    "Roulette Blue Magic" : ItemData(296, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLUE_MAGE]),
    "AquaRake Blue Magic" : ItemData(297, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLUE_MAGE]),
    "L5 Doom Blue Magic" : ItemData(298, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLUE_MAGE]),
    "L4 Qrter Blue Magic" : ItemData(299, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLUE_MAGE]),
    "L2 Old Blue Magic" : ItemData(300, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLUE_MAGE]),
    "L3 Flare Blue Magic" : ItemData(301, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLUE_MAGE]),
    "FrogSong Blue Magic" : ItemData(302, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLUE_MAGE]),
    "TinySong Blue Magic" : ItemData(303, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLUE_MAGE]),
    "Flash Blue Magic" : ItemData(304, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLUE_MAGE]),
    "Time Slip Blue Magic" : ItemData(305, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLUE_MAGE]),
    "MoonFlut Blue Magic" : ItemData(306, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLUE_MAGE]),
    "DethClaw Blue Magic" : ItemData(307, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLUE_MAGE]),
    "Aero Blue Magic" : ItemData(308, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLUE_MAGE]),
    "Aero 2 Blue Magic" : ItemData(309, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLUE_MAGE]),
    "Aero 3 Blue Magic" : ItemData(310, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLUE_MAGE]),
    "Emission Blue Magic" : ItemData(311, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLUE_MAGE]),
    "GblinPnch Blue Magic" : ItemData(312, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLUE_MAGE]),
    "DrkShock Blue Magic" : ItemData(313, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLUE_MAGE]),
    "GuardOff Blue Magic" : ItemData(314, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLUE_MAGE]),
    "Fusion Blue Magic" : ItemData(315, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLUE_MAGE]),
    "MindBlst Blue Magic" : ItemData(316, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLUE_MAGE]),
    "Vampire Blue Magic" : ItemData(317, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLUE_MAGE]),
    "Hammer Blue Magic" : ItemData(318, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLUE_MAGE]),
    "BigGuard Blue Magic" : ItemData(319, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLUE_MAGE]),
    "Exploder Blue Magic" : ItemData(320, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLUE_MAGE]),
    "???? Blue Magic" : ItemData(321, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLUE_MAGE]),
    "Blowfish Blue Magic" : ItemData(322, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLUE_MAGE]),
    "WhiteWind Blue Magic" : ItemData(323, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLUE_MAGE]),
    "Missile Blue Magic" : ItemData(324, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_MAGIC,JOB_CODE_BLUE_MAGE]),
        
    "Kick Ability" : ItemData(400, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_MONK]),
    "BuildUp Ability" : ItemData(401, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_MONK]),
    "Mantra Ability" : ItemData(402, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_MONK]),
    "Escape Ability" : ItemData(403, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_THIEF]),
    "Steal Ability" : ItemData(404, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_THIEF]),
    "Mug Ability" : ItemData(405, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_THIEF]),
    "Jump Ability" : ItemData(406, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_DRAGOON]),
    "DrgnSwd Ability" : ItemData(407, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_DRAGOON]),
    "Smoke Ability" : ItemData(408, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_NINJA]),
    "Image Ability" : ItemData(409, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_NINJA]),
    "Throw Ability" : ItemData(410, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_NINJA]),
    "SwdSlap Ability" : ItemData(411, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_SAMURAI]),
    "GilToss Ability" : ItemData(412, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_SAMURAI]),
    "Slash Ability" : ItemData(413, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_SAMURAI]),
    "Animals Ability" : ItemData(414, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_HUNTER]),
    "Aim Ability" : ItemData(415, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_HUNTER]),
    "X-Fight Ability" : ItemData(416, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_HUNTER]),
    "Conjure Ability" : ItemData(417, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_SUMMONER]),
    "Observe Ability" : ItemData(418, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_BLUE_MAGE]),
    "Analyze Ability" : ItemData(419, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_BLUE_MAGE]),
    "Tame Ability" : ItemData(420, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_TRAINER]),
    "Control Ability" : ItemData(421, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_TRAINER]),
    "Catch Ability" : ItemData(422, ItemClassification.progression, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_TRAINER]),
    "Mix Ability" : ItemData(423, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_CHEMIST]),
    "Drink Ability" : ItemData(424, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_CHEMIST]),
    "Pray Ability" : ItemData(425, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_CHEMIST]),
    "Revive Ability" : ItemData(426, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_CHEMIST]),
    "Terrain Ability" : ItemData(427, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_GEOMANCER]),
    "Hide Ability" : ItemData(428, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_BARD]),
    "Sing Ability" : ItemData(429, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_BARD]),
    "Flirt Ability" : ItemData(430, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_DANCER]),
    "Dance Ability" : ItemData(431, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_DANCER]),
    "Mimic Ability" : ItemData(432, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_MIMIC]),
    "MgcSwrd Lv.1 Ability" : ItemData(433, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_MYSTIC_KNIGHT]),
    "MgcSwrd Lv.2 Ability" : ItemData(434, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_MYSTIC_KNIGHT]),
    "MgcSwrd Lv.3 Ability" : ItemData(435, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_MYSTIC_KNIGHT]),
    "MgcSwrd Lv.4 Ability" : ItemData(436, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_MYSTIC_KNIGHT]),
    "MgcSwrd Lv.5 Ability" : ItemData(437, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_MYSTIC_KNIGHT]),
    "MgcSwrd Lv.6 Ability" : ItemData(438, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_MYSTIC_KNIGHT]),
    "White Lv.1 Ability" : ItemData(439, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_WHITE_MAGE]),
    "White Lv.2 Ability" : ItemData(440, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_WHITE_MAGE]),
    "White Lv.3 Ability" : ItemData(441, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_WHITE_MAGE]),
    "White Lv.4 Ability" : ItemData(442, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_WHITE_MAGE]),
    "White Lv.5 Ability" : ItemData(443, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_WHITE_MAGE]),
    "White Lv.6 Ability" : ItemData(444, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_WHITE_MAGE]),
    "Black Lv.1 Ability" : ItemData(445, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_BLACK_MAGE]),
    "Black Lv.2 Ability" : ItemData(446, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_BLACK_MAGE]),
    "Black Lv.3 Ability" : ItemData(447, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_BLACK_MAGE]),
    "Black Lv.4 Ability" : ItemData(448, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_BLACK_MAGE]),
    "Black Lv.5 Ability" : ItemData(449, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_BLACK_MAGE]),
    "Black Lv.6 Ability" : ItemData(450, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_BLACK_MAGE]),
    "Time Lv.1 Ability" : ItemData(451, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_TIME_MAGE]),
    "Time Lv.2 Ability" : ItemData(452, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_TIME_MAGE]),
    "Time Lv.3 Ability" : ItemData(453, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_TIME_MAGE]),
    "Time Lv.4 Ability" : ItemData(454, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_TIME_MAGE]),
    "Time Lv.5 Ability" : ItemData(455, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_TIME_MAGE]),
    "Time Lv.6 Ability" : ItemData(456, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_TIME_MAGE]),
    "Summon Lv.1 Ability" : ItemData(457, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_SUMMONER]),
    "Summon Lv.2 Ability" : ItemData(458, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_SUMMONER]),
    "Summon Lv.3 Ability" : ItemData(459, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_SUMMONER]),
    "Summon Lv.4 Ability" : ItemData(460, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_SUMMONER]),
    "Summon Lv.5 Ability" : ItemData(461, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_SUMMONER]),
    "Red Lv.1 Ability" : ItemData(462, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_RED_MAGE]),
    "Red Lv.2 Ability" : ItemData(463, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_RED_MAGE]),
    "Red Lv.3 Ability" : ItemData(464, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_RED_MAGE]),
    "X-Magic Ability" : ItemData(465, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_RED_MAGE]),
    "Blue Ability" : ItemData(466, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_BLUE_MAGE]),
    "Equip Shield Ability" : ItemData(467, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_KNIGHT]),
    "Equip Armors Ability" : ItemData(468, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_KNIGHT]),
    "Equip Ribbon Ability" : ItemData(469, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_DANCER]),
    "Equip Swords Ability" : ItemData(470, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_KNIGHT]),
    "Equip Spears Ability" : ItemData(471, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_DRAGOON]),
    "Equip Katana Ability" : ItemData(472, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_SAMURAI]),
    "Equip Axes Ability" : ItemData(473, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_BERSERKER]),
    "Equip Bows Ability" : ItemData(474, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_HUNTER]),
    "Equip Whips Ability" : ItemData(475, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_TRAINER]),
    "Equip Harps Ability" : ItemData(476, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_BARD]),
    "Agility Ability" : ItemData(477, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_THIEF]),
    "HP +10% Ability" : ItemData(478, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_MONK]),
    "HP +20% Ability" : ItemData(479, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_MONK]),
    "HP +30% Ability" : ItemData(480, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_MONK]),
    "MP +10% Ability" : ItemData(481, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_WHITE_MAGE]),
    "MP +30% Ability" : ItemData(482, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_BLACK_MAGE]),
    "Brawl Ability" : ItemData(483, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_MONK]),
    "Dbl Grip Ability" : ItemData(484, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_KNIGHT]),
    "2-Wield Ability" : ItemData(485, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_NINJA]),
    "Medicine Ability" : ItemData(486, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_CHEMIST]),
    "Cover Ability" : ItemData(487, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_KNIGHT]),
    "Counter Ability" : ItemData(488, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_MONK]),
    "Evade Ability" : ItemData(489, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_SAMURAI]),
    "Barrier Ability" : ItemData(490, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_MYSTIC_KNIGHT]),
    "Berserk Ability" : ItemData(491, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_BERSERKER]),
    "Caution Ability" : ItemData(492, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_THIEF]),
    "Preemptive Ability" : ItemData(493, ItemClassification.useful, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_NINJA]),
    "DmgFloor Ability" : ItemData(494, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_GEOMANCER]),
    "Equip Rods Ability" : ItemData(495, ItemClassification.filler, [ITEM_CODE_UNIQUE,ITEM_CODE_ABILITIES,JOB_CODE_TIME_MAGE]),
      
    "Knife Item" : ItemData(600, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Dagger Item" : ItemData(601, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Mythril Knife Item" : ItemData(602, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Kunai Item" : ItemData(603, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Mage Masher Item" : ItemData(604, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Guardian Item" : ItemData(605, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Kodachi Item" : ItemData(606, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Orialcon Item" : ItemData(607, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Air Knife Item" : ItemData(608, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Assassin Item" : ItemData(609, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Hardened Dagger Item" : ItemData(610, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Broadsword Item" : ItemData(611, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "RegalCut Item" : ItemData(612, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Mythril Sword Item" : ItemData(613, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Coral Sword Item" : ItemData(614, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Ancient Sword Item" : ItemData(615, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Epee Sword Item" : ItemData(616, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Slumber Sword Item" : ItemData(617, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Defender Sword Item" : ItemData(618, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Excalibur Item" : ItemData(619, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Ragnarok Item" : ItemData(620, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Javelin Item" : ItemData(621, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Spear Item" : ItemData(622, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Mythril Spear Item" : ItemData(623, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Trident Item" : ItemData(624, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Wind Spear Item" : ItemData(625, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Partisan Item" : ItemData(626, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Heavy Spear Item" : ItemData(627, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "DblLance Item" : ItemData(628, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Holy Lance Item" : ItemData(629, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Dragoon Lance Item" : ItemData(630, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Battle Axe Item" : ItemData(631, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Mythril Hammer Item" : ItemData(632, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Ogre Killer Item" : ItemData(633, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "War Hammer Item" : ItemData(634, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Venom Axe Item" : ItemData(635, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Earth Hammer Item" : ItemData(636, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Rune Axe Item" : ItemData(637, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Thor Hammer Item" : ItemData(638, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Katana Item" : ItemData(639, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Air Blade Item" : ItemData(640, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Kotetsu Item" : ItemData(641, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Bizen Item" : ItemData(642, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Forged Item" : ItemData(643, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Murasume Item" : ItemData(644, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Masamune Item" : ItemData(645, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Tempest Item" : ItemData(646, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Rod Item" : ItemData(647, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Fire Rod Item" : ItemData(648, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Ice Rod Item" : ItemData(649, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Thunder Rod Item" : ItemData(650, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Venom Rod Item" : ItemData(651, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Lillith Rod Item" : ItemData(652, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Wizard Rod Item" : ItemData(653, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Staff Item" : ItemData(654, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Mythril Staff Item" : ItemData(655, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Power Staff Item" : ItemData(656, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Healing Staff Item" : ItemData(657, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Staff of Light Item" : ItemData(658, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Sage's Staff Item" : ItemData(659, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Judgement Staff Item" : ItemData(660, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Fire Bow Item" : ItemData(661, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Ice Bow Item" : ItemData(662, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Thunder Bow Item" : ItemData(663, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Darkness Bow Item" : ItemData(664, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Killer Bow Item" : ItemData(665, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Elven Bow Item" : ItemData(666, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Yoichi Bow Item" : ItemData(667, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Artemis Bow Item" : ItemData(668, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Silver Harp Item" : ItemData(669, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Dream Harp Item" : ItemData(670, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Lamia's Harp Item" : ItemData(671, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Apollo's Harp Item" : ItemData(672, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Whip Item" : ItemData(673, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Chain Whip Item" : ItemData(674, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Thunder Whip Item" : ItemData(675, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Flame Whip Item" : ItemData(676, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Dragon's Whisker Item" : ItemData(677, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Giyaman Item" : ItemData(678, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Earth Bell Item" : ItemData(679, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Rune Chime Item" : ItemData(680, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Tinkerbell Item" : ItemData(681, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Drain Sword Item" : ItemData(682, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "RuneEdge Item" : ItemData(683, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Flametongue Item" : ItemData(684, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "IceBrand Item" : ItemData(685, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Full Moon Item" : ItemData(686, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Shuriken Item" : ItemData(687, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Pinwheel Item" : ItemData(688, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Excailbur Item" : ItemData(689, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "BeastKiller Item" : ItemData(690, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Flail Item" : ItemData(691, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Morning Star Item" : ItemData(692, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Wonder Wand Item" : ItemData(693, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Brave Blade Item" : ItemData(694, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Soot Item" : ItemData(695, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Chicken Knife Item" : ItemData(696, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "RisingSun Item" : ItemData(697, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Silver Bow Item" : ItemData(698, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Gale Bow Item" : ItemData(699, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "AntiMagic Bow Item" : ItemData(700, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Avis Killer Item" : ItemData(701, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "DoomCut Item" : ItemData(702, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Giant's Axe Item" : ItemData(703, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "ManEater Item" : ItemData(704, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Thief Knife Item" : ItemData(705, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Dancing Dagger Item" : ItemData(706, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Enhancer Item" : ItemData(707, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Leather Shield Item" : ItemData(708, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Bronze Shield Item" : ItemData(709, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Iron Shield Item" : ItemData(710, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Mythril Shield Item" : ItemData(711, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Golden Shield Item" : ItemData(712, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Aegis Shield Item" : ItemData(713, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Diamond Shield Item" : ItemData(714, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Crystal Shield Item" : ItemData(715, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Leather Cap Item" : ItemData(716, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Bronze Helm Item" : ItemData(717, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Iron Helm Item" : ItemData(718, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Mythril Helm Item" : ItemData(719, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Golden Helm Item" : ItemData(720, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Diamond Helm Item" : ItemData(721, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Crystal Helm Item" : ItemData(722, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Plumed Hat Item" : ItemData(723, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Tricorn Hat Item" : ItemData(724, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Magus Item" : ItemData(725, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Circlet Item" : ItemData(726, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Gold Hairpin Item" : ItemData(727, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Ribbon Item" : ItemData(728, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Bandana Item" : ItemData(729, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "GrnBeret Item" : ItemData(730, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "DarkHood Item" : ItemData(731, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Lamia's Tiara Item" : ItemData(732, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Leather Armor Item" : ItemData(733, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Bronze Armor Item" : ItemData(734, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Iron Armor Item" : ItemData(735, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Mythril Armor Item" : ItemData(736, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Golden Armor Item" : ItemData(737, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Diamond Armor Item" : ItemData(738, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Crystal Armor Item" : ItemData(739, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "CopperPlt Item" : ItemData(740, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Training Suit Item" : ItemData(741, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Silver Plate Item" : ItemData(742, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Stealth Suit Item" : ItemData(743, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "DiamndPlt Item" : ItemData(744, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "DarkSuit Item" : ItemData(745, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Cotton Robe Item" : ItemData(746, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Silk robe Item" : ItemData(747, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Gaia Gear Item" : ItemData(748, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Bard's Surplice Item" : ItemData(749, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Lumina Robe Item" : ItemData(750, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Black Robe Item" : ItemData(751, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "White Robe Item" : ItemData(752, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Mirage Vest Item" : ItemData(753, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Guard Ring Item" : ItemData(754, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Thief's Glove Item" : ItemData(755, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Giant's Gloves Item" : ItemData(756, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Elf Cape Item" : ItemData(757, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Cursed Ring Item" : ItemData(758, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Glasses Item" : ItemData(759, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Running Shoes Item" : ItemData(760, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Mythril Glove Item" : ItemData(761, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Silver Armlet Item" : ItemData(762, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Diamond Armlet Item" : ItemData(763, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Strength Item" : ItemData(764, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Power Wrist Item" : ItemData(765, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Angel Gwn Item" : ItemData(766, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Angel Ring Item" : ItemData(767, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Flame Ring Item" : ItemData(768, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Coral Ring Item" : ItemData(769, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Bone Mail Item" : ItemData(770, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Leather Shoes Item" : ItemData(771, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Kaiser Knuckles Item" : ItemData(772, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Gauntlets Item" : ItemData(773, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Tiger Mask Item" : ItemData(774, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Flame Shield Item" : ItemData(775, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "CornaJar Item" : ItemData(776, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Genji Shield Item" : ItemData(777, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Genji Helm Item" : ItemData(778, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Genji Armor Item" : ItemData(779, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Genji Gloves Item" : ItemData(780, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Wall Ring Item" : ItemData(781, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Hypno Helm Item" : ItemData(782, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Thornlet Item" : ItemData(783, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Ice Shield Item" : ItemData(784, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Cursed Shield Item" : ItemData(785, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Rainbow Dress Item" : ItemData(786, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Red Shoes Item" : ItemData(787, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Potion Item" : ItemData(788, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "HiPotion Item" : ItemData(789, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Ether Item" : ItemData(790, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Elixir Item" : ItemData(791, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Phoenix Down Item" : ItemData(792, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Maiden's Kiss Item" : ItemData(793, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Revivify Item" : ItemData(794, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "TurtleShell Item" : ItemData(795, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Antidote Item" : ItemData(796, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Eyedrop Item" : ItemData(797, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "DragonFang Item" : ItemData(798, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "DarkMatter Item" : ItemData(799, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Soft Item" : ItemData(800, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "LuckMallet Item" : ItemData(801, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Magic Lamp Item" : ItemData(802, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Tent Item" : ItemData(803, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Cabin Item" : ItemData(804, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Giant Drink Item" : ItemData(805, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Power Drink Item" : ItemData(806, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Speed Drink Item" : ItemData(807, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Protect Drink Item" : ItemData(808, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Hero Drink Item" : ItemData(809, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Ramuh Item" : ItemData(810, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Shoat Item" : ItemData(811, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Golem Item" : ItemData(812, ItemClassification.useful, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM, ITEM_CODE_MIB_REWARD]),
    "Flame Scroll Item" : ItemData(813, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Water Scroll Item" : ItemData(814, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    "Thunder Scroll Item" : ItemData(815, ItemClassification.filler, [ITEM_CODE_FUNGIBLE, ITEM_CODE_ITEM]),
    
    "100 Gil" : ItemData(900, ItemClassification.filler, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "300 Gil" : ItemData(901, ItemClassification.filler, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "1000 Gil" : ItemData(902, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "5000 Gil (#1)" : ItemData(903, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "9900 Gil" : ItemData(904, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "8000 Gil (#1)" : ItemData(905, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "4400 Gil" : ItemData(906, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "10000 Gil (#1)" : ItemData(907, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "5000 Gil (#2)" : ItemData(908, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "8000 Gil (#2)" : ItemData(909, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "5000 Gil (#3)" : ItemData(910, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "9000 Gil (#1)" : ItemData(911, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "18000 Gil" : ItemData(912, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "2500 Gil" : ItemData(913, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "4900 Gil" : ItemData(914, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "9500 Gil" : ItemData(915, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "9000 Gil (#2)" : ItemData(916, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "8000 Gil (#3)" : ItemData(917, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "10000 Gil (#2)" : ItemData(918, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "12000 Gil (#1)" : ItemData(919, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "12000 Gil (#2)" : ItemData(920, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "9000 Gil (#3)" : ItemData(921, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "12000 Gil (#3)" : ItemData(922, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "5000 Gil (#4)" : ItemData(923, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "15000 Gil" : ItemData(924, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "20000 Gil" : ItemData(925, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),
    "25000 Gil" : ItemData(926, ItemClassification.useful, [ITEM_CODE_GIL, ITEM_CODE_ITEM]),


    "Walse Tower Key" : ItemData(1000, ItemClassification.progression, [ITEM_CODE_UNIQUE, ITEM_CODE_KEY_ITEMS, ITEM_CODE_MIB_REWARD_PROG]),
    "Steamship Key" : ItemData(1001, ItemClassification.progression, [ITEM_CODE_UNIQUE, ITEM_CODE_KEY_ITEMS, ITEM_CODE_MIB_REWARD_PROG]),
    "Ifrit's Fire" : ItemData(1002, ItemClassification.progression, [ITEM_CODE_UNIQUE, ITEM_CODE_KEY_ITEMS, ITEM_CODE_MIB_REWARD_PROG]),
    "SandwormBait" : ItemData(1003, ItemClassification.progression, [ITEM_CODE_UNIQUE, ITEM_CODE_KEY_ITEMS, ITEM_CODE_MIB_REWARD_PROG]),
    "Big Bridge Key" : ItemData(1004, ItemClassification.progression, [ITEM_CODE_UNIQUE, ITEM_CODE_KEY_ITEMS, ITEM_CODE_MIB_REWARD_PROG]),
    "Hiryuu Call" : ItemData(1005, ItemClassification.progression, [ITEM_CODE_UNIQUE, ITEM_CODE_KEY_ITEMS, ITEM_CODE_MIB_REWARD_PROG]),
    "Submarine Key" : ItemData(1006, ItemClassification.progression, [ITEM_CODE_UNIQUE, ITEM_CODE_KEY_ITEMS, ITEM_CODE_MIB_REWARD_PROG]),
    "Anti Barrier" : ItemData(1007, ItemClassification.progression, [ITEM_CODE_UNIQUE, ITEM_CODE_KEY_ITEMS, ITEM_CODE_MIB_REWARD_PROG]),
    "Bracelet" : ItemData(1008, ItemClassification.progression, [ITEM_CODE_UNIQUE, ITEM_CODE_KEY_ITEMS, ITEM_CODE_MIB_REWARD_PROG]),
    "Pyramid Page" : ItemData(1009, ItemClassification.progression, [ITEM_CODE_UNIQUE, ITEM_CODE_KEY_ITEMS, ITEM_CODE_MIB_REWARD_PROG]),
    "Shrine Page" : ItemData(1010, ItemClassification.progression, [ITEM_CODE_UNIQUE, ITEM_CODE_KEY_ITEMS, ITEM_CODE_MIB_REWARD_PROG]),
    "Trench Page" : ItemData(1011, ItemClassification.progression, [ITEM_CODE_UNIQUE, ITEM_CODE_KEY_ITEMS, ITEM_CODE_MIB_REWARD_PROG]),
    "Falls Page" : ItemData(1012, ItemClassification.progression, [ITEM_CODE_UNIQUE, ITEM_CODE_KEY_ITEMS, ITEM_CODE_MIB_REWARD_PROG]),
    "Mirage Radar" : ItemData(1013, ItemClassification.progression, [ITEM_CODE_UNIQUE, ITEM_CODE_KEY_ITEMS, ITEM_CODE_MIB_REWARD_PROG]),
    "Adamantite" : ItemData(1014, ItemClassification.progression, [ITEM_CODE_UNIQUE, ITEM_CODE_KEY_ITEMS, ITEM_CODE_MIB_REWARD_PROG]),
    "Moogle Suit" : ItemData(1015, ItemClassification.progression, [ITEM_CODE_UNIQUE, ITEM_CODE_KEY_ITEMS, ITEM_CODE_MIB_REWARD_PROG]),
    "Elder Branch" : ItemData(1016, ItemClassification.progression, [ITEM_CODE_UNIQUE, ITEM_CODE_KEY_ITEMS, ITEM_CODE_MIB_REWARD_PROG]),
    "1st Tablet" : ItemData(1017, ItemClassification.progression, [ITEM_CODE_UNIQUE, ITEM_CODE_KEY_ITEMS, ITEM_CODE_MIB_REWARD_PROG]),
    "2nd Tablet" : ItemData(1018, ItemClassification.progression, [ITEM_CODE_UNIQUE, ITEM_CODE_KEY_ITEMS, ITEM_CODE_MIB_REWARD_PROG]),
    "3rd Tablet" : ItemData(1019, ItemClassification.progression, [ITEM_CODE_UNIQUE, ITEM_CODE_KEY_ITEMS, ITEM_CODE_MIB_REWARD_PROG]),
    "4th Tablet" : ItemData(1020, ItemClassification.progression, [ITEM_CODE_UNIQUE, ITEM_CODE_KEY_ITEMS, ITEM_CODE_MIB_REWARD_PROG]),

    #"Victory" : ItemData(1200, ItemClassification.progression, [ITEM_CODE_VICTORY]),
    #"Exdeath in World 2" : ItemData(1203, ItemClassification.progression, [ITEM_CODE_EXDEATH_W2]),

}

event_table = {
    "Victory": FFVCDEventData("ExDeath", "Victory", ItemClassification.progression),
    "ExDeath World 2": FFVCDEventData("ExDeath World 2", "ExDeath World 2", ItemClassification.progression),
    "Piano (Tule)": FFVCDEventData("Piano (Tule)", "Piano (Tule)", ItemClassification.progression),
    "Piano (Carwen)": FFVCDEventData("Piano (Carwen)", "Piano (Carwen)", ItemClassification.progression),
    "Piano (Karnak)": FFVCDEventData("Piano (Karnak)", "Piano (Karnak)", ItemClassification.progression),
    "Piano (Jacole)": FFVCDEventData("Piano (Jacole)", "Piano (Jacole)", ItemClassification.progression),
    "Piano (Crescent)": FFVCDEventData("Piano (Crescent)", "Piano (Crescent)", ItemClassification.progression),
    "Piano (Mua)": FFVCDEventData("Piano (Mua)", "Piano (Mua)", ItemClassification.progression),
    "Piano (Rugor)": FFVCDEventData("Piano (Rugor)", "Piano (Rugor)", ItemClassification.progression),
    "Piano (Mirage)": FFVCDEventData("Piano (Mirage)", "Piano (Mirage)", ItemClassification.progression),}

item_groups = {}
for item, data in item_table.items():
    for group in data.groups:
        item_groups[group] = item_groups.get(group, []) + [item]


class FFVCDItem(Item):
    game = "ffvcd"
    def __init__(self, name, classification, item_data_id, player, groups):
        super().__init__(name, classification, item_data_id, player)
        self.groups = groups

#not sure this is necessary but wanted to exclude the groups and make absolutely sure everything was set to None for events.
class FFVCDEventItem(Item):
    game = "ffvcd"
    def __init__(self, name, classification, item_data_id, player):
        super().__init__(name, classification, item_data_id, player)
        Item.id = None

