from BaseClasses import Location


hades_base_location_id = 5093427000

# This is basically location + score checks. Keeping this as a variable to have easier time keeping
max_number_room_checks = 1700 + hades_base_location_id

# Making global tables that can be used for unit testing.

global location_table_tartarus 
location_table_tartarus = {
    "Beat Meg": None,
}

global location_table_asphodel
location_table_asphodel = {
    "Beat Lernie": None,
}

global location_table_elysium
location_table_elysium = {
    "Beat Bros": None,
}

global location_table_styx
location_table_styx = {
    "Beat Hades": None,
}

global location_table_styx_late
location_table_styx_late = {
}

location_keepsakes = {
    "Cerberus Keepsake": max_number_room_checks + 1,
    "Achilles Keepsake": max_number_room_checks + 2,
    "Nyx Keepsake": max_number_room_checks + 3,
    "Thanatos Keepsake": max_number_room_checks + 4,
    "Charon Keepsake": max_number_room_checks + 5,
    "Hypnos Keepsake": max_number_room_checks + 6,
    "Megaera Keepsake": max_number_room_checks + 7,
    "Orpheus Keepsake": max_number_room_checks + 8,
    "Dusa Keepsake": max_number_room_checks + 9,
    "Skelly Keepsake": max_number_room_checks + 10,
    "Zeus Keepsake": max_number_room_checks + 11,
    "Poseidon Keepsake": max_number_room_checks + 12,
    "Athena Keepsake": max_number_room_checks + 13,
    "Aphrodite Keepsake": max_number_room_checks + 14,
    "Ares Keepsake": max_number_room_checks + 15,
    "Artemis Keepsake": max_number_room_checks + 16,
    "Dionysus Keepsake": max_number_room_checks + 17,
    "Hermes Keepsake": max_number_room_checks + 18,
    "Demeter Keepsake": max_number_room_checks + 19,
    "Chaos Keepsake": max_number_room_checks + 20,
    "Sisyphus Keepsake": max_number_room_checks + 21,
    "Eurydice Keepsake": max_number_room_checks + 22,
    "Patroclus Keepsake": max_number_room_checks + 23,
}

location_weapons = {
    "Sword Weapon Unlock Location": max_number_room_checks + 25,
    "Bow Weapon Unlock Location": max_number_room_checks + 26,
    "Spear Weapon Unlock Location": max_number_room_checks + 27,
    "Shield Weapon Unlock Location": max_number_room_checks + 28,
    "Fist Weapon Unlock Location": max_number_room_checks + 29,
    "Gun Weapon Unlock Location": max_number_room_checks + 30,
}


location_store_gemstones = {
    "Fountain Upgrade1 Location": max_number_room_checks + 31,
    "Fountain Upgrade2 Location": max_number_room_checks + 32,
    "Fountain Tartarus Location": max_number_room_checks + 33,
    "Fountain Asphodel Location": max_number_room_checks + 34,
    "Fountain Elysium Location": max_number_room_checks + 35,
    "Urns Of Wealth1 Location": max_number_room_checks + 36,
    "Urns Of Wealth2 Location": max_number_room_checks + 37,
    "Urns Of Wealth3 Location": max_number_room_checks + 38,
    "Infernal Trove1 Location": max_number_room_checks + 39,
    "Infernal Trove2 Location": max_number_room_checks + 40,
    "Infernal Trove3 Location": max_number_room_checks + 41,
    "Keepsake Collection Location": max_number_room_checks + 42,
}

location_store_diamonds = {
    "Deluxe Contractor Desk Location": max_number_room_checks + 44,
    "Vanquishers Keep Location": max_number_room_checks + 45,
    "Fishing Rod Location": max_number_room_checks + 46,
    "Court Musician Sentence Location": max_number_room_checks + 47,
    "Court Musician Stand Location": max_number_room_checks + 48,
    "Pitch Black Darkness Location": max_number_room_checks + 49,
    "Fated Keys Location": max_number_room_checks + 50,
    "Brilliant Gemstones Location": max_number_room_checks + 51,
    "Vintage Nectar Location": max_number_room_checks + 52,
    "Darker Thirst Location": max_number_room_checks + 53,
}

location_table_fates = {
    "Is There No Escape?": max_number_room_checks + 54,
    "Distant Relatives": max_number_room_checks + 55,
    "Chthonic Colleagues": max_number_room_checks + 56,
    "The Reluctant Musician": max_number_room_checks + 57,
    "Goddess Of Wisdom": max_number_room_checks + 58,
    "God Of The Heavens": max_number_room_checks + 59,
    "God Of The Sea": max_number_room_checks + 60,
    "Goddess Of Love": max_number_room_checks + 61,
    "God Of War": max_number_room_checks + 62,
    "Goddess Of The Hunt": max_number_room_checks + 63,
    "God Of Wine": max_number_room_checks + 64,
    "God Of Swiftness": max_number_room_checks + 65,
    "Goddess Of Seasons": max_number_room_checks + 66,
    "Power Without Equal": max_number_room_checks + 67,
    "Divine Pairings": max_number_room_checks + 68,
    "Primordial Boons": max_number_room_checks + 69,
    "Primordial Banes": max_number_room_checks + 70,
    "Infernal Arms": max_number_room_checks + 71,
    "The Stygian Blade": max_number_room_checks + 72,
    "The Heart Seeking Bow": max_number_room_checks + 73,
    "The Shield Of Chaos": max_number_room_checks + 74,
    "The Eternal Spear": max_number_room_checks + 75,
    "The Twin Fists": max_number_room_checks + 76,
    "The Adamant Rail": max_number_room_checks + 77,
    "Master Of Arms": max_number_room_checks + 78,
    "A Violent Past": max_number_room_checks + 79,
    "Harsh Conditions": max_number_room_checks + 80,
    "Slashed Benefits": max_number_room_checks + 81,
    "Wanton Ransacking": max_number_room_checks + 82,
    "A Simple Job": max_number_room_checks + 83,
    "Chthonic Knowledge": max_number_room_checks + 84,
    "Customer Loyalty": max_number_room_checks + 85,
    "Dark Reflections": max_number_room_checks + 86,
    "Close At Heart": max_number_room_checks + 87,
    "Denizens Of The Deep": max_number_room_checks + 88,
    "The Useless Trinket": max_number_room_checks + 89,
}


location_table_fates_events = {
    "Is There No Escape? Event": None,
    "Distant Relatives Event": None,
    "Chthonic Colleagues Event": None,
    "The Reluctant Musician Event": None,
    "Goddess Of Wisdom Event": None,
    "God Of The Heavens Event": None,
    "God Of The Sea Event": None,
    "Goddess Of Love Event": None,
    "God Of War Event": None,
    "Goddess Of The Hunt Event": None,
    "God Of Wine Event": None,
    "God Of Swiftness Event": None,
    "Goddess Of Seasons Event": None,
    "Power Without Equal Event": None,
    "Divine Pairings Event": None,
    "Primordial Boons Event": None,
    "Primordial Banes Event": None,
    "Infernal Arms Event": None,
    "The Stygian Blade Event": None,
    "The Heart Seeking Bow Event": None,
    "The Shield Of Chaos Event": None,
    "The Eternal Spear Event": None,
    "The Twin Fists Event": None,
    "The Adamant Rail Event": None,
    "Master Of Arms Event": None,
    "A Violent Past Event": None,
    "Harsh Conditions Event": None,
    "Slashed Benefits Event": None,
    "Wanton Ransacking Event": None,
    "A Simple Job Event": None,
    "Chthonic Knowledge Event": None,
    "Customer Loyalty Event": None,
    "Dark Reflections Event": None,
    "Close At Heart Event": None,
    "Denizens Of The Deep Event": None,
    "The Useless Trinket Event": None,
}

# ----------------------

location_weapons_subfixes = [
    "Sword Weapon",
    "Spear Weapon",
    "Shield Weapon",
    "Bow Weapon",
    "Fist Weapon",
    "Gun Weapon",
]

# ---------------------


def give_all_locations_table():
    table_rooms = give_default_location_table()
    table_score = give_score_location_table(1000)
    table_weaponlocation = give_weapon_based_locations()    

    return {
        **table_rooms,
        **table_score,
        **table_weaponlocation,
        **location_keepsakes,
        **location_weapons,
        **location_store_gemstones,
        **location_store_diamonds,
        **location_table_fates,
        **location_table_fates_events,
    }


def clear_tables():
    global location_table_tartarus 
    location_table_tartarus = {
        "Beat Meg": None,
    }

    global location_table_asphodel
    location_table_asphodel = {
        "Beat Lernie": None,
    }

    global location_table_elysium
    location_table_elysium = {
        "Beat Bros": None,
    }

    global location_table_styx
    location_table_styx = {
        "Beat Hades": None,
    }
    
    global location_table_styx_late
    location_table_styx_late = {
    }
    

# Change parameters so they include the settings of the player
# Chose between old and new system. And for the new system we want to be able
# to choose how many "locations" we have.
def setup_location_table_with_settings(options):
    clear_tables()
    total_table = {}
 
    total_table.update(location_table_fates_events)
    
    if options.keepsakesanity.value == 1:
        total_table.update(location_keepsakes)
     
    if options.weaponsanity.value == 1:
        for weaponLocation, weaponData in location_weapons.items():
            if not should_ignore_weapon_location(weaponLocation, options):
                total_table.update({weaponLocation: weaponData})
                
    if options.storesanity.value == 1:
        total_table.update(location_store_gemstones)
        total_table.update(location_store_diamonds)

    if options.location_system.value == 1:
        result = give_default_location_table()
        total_table.update(result)
    elif options.location_system.value == 2:
        levels = options.score_rewards_amount.value
        total_table.update(give_score_location_table(levels))
    elif options.location_system.value == 3:
        total_table.update(give_weapon_based_locations())
    
    if options.fatesanity == 1:
        total_table.update(location_table_fates)
    
    return total_table
            
# -----------------------------------------------


def should_ignore_weapon_location(weaponLocation, options):
    if options.initial_weapon.value == 0 and weaponLocation == "Sword Weapon Unlock Location":
        return True
    if options.initial_weapon.value == 1 and weaponLocation == "Bow Weapon Unlock Location":
        return True
    if options.initial_weapon.value == 2 and weaponLocation == "Spear Weapon Unlock Location":
        return True
    if options.initial_weapon.value == 3 and weaponLocation == "Shield Weapon Unlock Location":
        return True
    if options.initial_weapon.value == 4 and weaponLocation == "Fist Weapon Unlock Location":
        return True
    if options.initial_weapon.value == 5 and weaponLocation == "Gun Weapon Unlock Location":
        return True
    return False


# -----------------------------------------------

def give_default_location_table():
    #Repopulate tartarus table; rooms from 1 to 13.
    global location_table_tartarus
    for i in range(13):
        stringInt = i + 1
        if stringInt < 10:
            stringInt = "0"+str(stringInt);
        location_table_tartarus["Clear Room "+str(stringInt)] = hades_base_location_id + i
        
    # Repopulate asphodel table, rooms from 14 to 23
    global location_table_asphodel
    for i in range(13, 23):
        location_table_asphodel["Clear Room "+str(i + 1)] = hades_base_location_id + i
    
    # Repopulate elysium table, rooms from 24 to 35
    global location_table_elysium
    for i in range(23, 35):
        location_table_elysium["Clear Room "+str(i + 1)] = hades_base_location_id + i
    
    # Repopulate styx table, rooms from 35 to 72. Split into early and late
    global location_table_styx 
    for i in range(35, 60):
        location_table_styx["Clear Room "+str(i + 1)] = hades_base_location_id + i
        
    global location_table_styx_late
    for i in range(60, 72):
        location_table_styx_late["Clear Room "+str(i + 1)] = hades_base_location_id + i
    
    location_table = {
        **location_table_tartarus, 
        **location_table_asphodel,
        **location_table_elysium,
        **location_table_styx,
        **location_table_styx_late,
    }
    return location_table


def give_score_location_table(locations):
    fraction_location = int(locations/8)
    locations_first_region = locations - 7 * fraction_location

    global location_table_tartarus 
    # Recall to add a offset for the location to avoid sharing ids if two players play with different settings
    for i in range(locations_first_region):
        stringInt = str(i + 1)
        while len(stringInt) < 4:
            stringInt = "0" + str(stringInt)
        location_table_tartarus["Clear Score "+str(stringInt)] = hades_base_location_id + i + 72

    global location_table_asphodel
    for i in range(locations_first_region, locations_first_region + 2 * fraction_location):
        stringInt = str(i + 1)
        while len(stringInt) < 4:
            stringInt = "0" + str(stringInt)
        location_table_asphodel["Clear Score "+stringInt] = hades_base_location_id + i + 72
        
    global location_table_elysium
    for i in range(locations_first_region+2*fraction_location, locations_first_region + 4 * fraction_location):
        stringInt = str(i + 1)
        while len(stringInt) < 4:
            stringInt = "0" + str(stringInt)
        location_table_elysium["Clear Score "+stringInt] = hades_base_location_id + i + 72
    
    global location_table_styx
    for i in range(locations_first_region+4*fraction_location, locations_first_region + 6 * fraction_location):
        stringInt = str(i + 1)
        while len(stringInt) < 4:
            stringInt = "0" + str(stringInt)
        location_table_styx["Clear Score "+stringInt] = hades_base_location_id + i + 72
        
    global location_table_styx_late
    for i in range(locations_first_region+6*fraction_location, locations):
        stringInt = str(i + 1)
        while len(stringInt) < 4:
            stringInt = "0" + str(stringInt)
        location_table_styx_late["Clear Score "+stringInt] = hades_base_location_id + i + 72

    location_table = {
        **location_table_tartarus, 
        **location_table_asphodel,
        **location_table_elysium,
        **location_table_styx,
        **location_table_styx_late,
    }
    
    return location_table
    

def give_weapon_based_locations():
    subfixCounter = 0
    weapon_locations = {}
    
    for weaponSubfix in location_weapons_subfixes:
    
        for i in range(13):
            stringInt = i + 1
            if stringInt < 10:
                stringInt = "0" + str(stringInt)
            weapon_locations["Clear Room " + str(stringInt) + " " + weaponSubfix] = hades_base_location_id + 1073 + i \
                + 73 * subfixCounter
        weapon_locations["Beat Meg "+weaponSubfix] = None

        for i in range(13, 23):
            weapon_locations["Clear Room " + str(i + 1) + " " + weaponSubfix] = hades_base_location_id + 1073 + i \
                + 73 * subfixCounter
    
        weapon_locations["Beat Lernie "+weaponSubfix] = None

        for i in range(23, 35):
            weapon_locations["Clear Room " + str(i + 1) + " " + weaponSubfix] = hades_base_location_id + 1073 + i \
                + 73 * subfixCounter
        weapon_locations["Beat Bros "+weaponSubfix] = None    

        for i in range(35, 60):
            weapon_locations["Clear Room " + str(i + 1) + " " + weaponSubfix] = hades_base_location_id + 1073 + i \
                + 73 * subfixCounter
        
        weapon_locations["Beat Hades " + weaponSubfix] = None

        for i in range(60, 72):
            weapon_locations["Clear Room " + str(i + 1) + " " + weaponSubfix] = hades_base_location_id + 1073 + i \
                + 73 * subfixCounter
            
        subfixCounter += 1
    
    return weapon_locations

# -----------------------------------------------


group_fates = {"fates": location_table_fates.keys()}
group_keepsakes = {"keepsakes": location_keepsakes.keys()}
group_weapons = {"weapons": location_weapons.keys()}
group_contractor_gemstones = {"contractor_gems": location_store_gemstones.keys()}
group_contractor_diamonds = {"contractor_diamonds": location_store_diamonds.keys()}

location_name_groups = {
    **group_fates,
    **group_keepsakes,
    **group_weapons,
    **group_contractor_gemstones,
    **group_contractor_diamonds,
}


# -----------------------------------------------

class HadesLocation(Location):
    game: str = "Hades"

    def __init__(self, player: int, name: str, address=None, parent=None):
        super(HadesLocation, self).__init__(player, name, address, parent)
        if address is None:
            self.event = True
            self.locked = True