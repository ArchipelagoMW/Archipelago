import typing
import time

from BaseClasses import Location


hades_base_location_id = 5093427000

#This is basically location + score checks. Keeping this as a variable to have easier time keeping
max_number_room_checks = 1700+hades_base_location_id

#Making global tables that can be used for unit testing.

global location_table_tartarus 
location_table_tartarus = {
    "Beat Meg": None,
}

global location_table_asphodel
location_table_asphodel = {
    "Beat Lernie": None,
}

global location_table_elyseum
location_table_elyseum = {
    "Beat Bros": None,
}

global location_table_styx
location_table_styx = {
    "Beat Hades": None,
}

global location_table_styx_late
location_table_styx_late = {
}

location_keepsakes ={
    "CerberusKeepsake": max_number_room_checks+1,
    "AchillesKeepsake": max_number_room_checks+2,
    "NyxKeepsake": max_number_room_checks+3,
    "ThanatosKeepsake": max_number_room_checks+4,
    "CharonKeepsake": max_number_room_checks+5,
    "HypnosKeepsake": max_number_room_checks+6,
    "MegaeraKeepsake": max_number_room_checks+7,
    "OrpheusKeepsake": max_number_room_checks+8,
    "DusaKeepsake": max_number_room_checks+9,
    "SkellyKeepsake": max_number_room_checks+10,
    "ZeusKeepsake": max_number_room_checks+11,
    "PoseidonKeepsake": max_number_room_checks+12,
    "AthenaKeepsake": max_number_room_checks+13,
    "AphroditeKeepsake": max_number_room_checks+14,
    "AresKeepsake": max_number_room_checks+15,
    "ArtemisKeepsake": max_number_room_checks+16,
    "DionysusKeepsake": max_number_room_checks+17,
    "HermesKeepsake": max_number_room_checks+18,
    "DemeterKeepsake": max_number_room_checks+19,
    "ChaosKeepsake": max_number_room_checks+20,
    "SisyphusKeepsake": max_number_room_checks+21,
    "EurydiceKeepsake": max_number_room_checks+22,
    "PatroclusKeepsake": max_number_room_checks+23,
}

location_weapons ={
    "SwordWeaponUnlockLocation": max_number_room_checks+25,
    "BowWeaponUnlockLocation": max_number_room_checks+26,
    "SpearWeaponUnlockLocation": max_number_room_checks+27,
    "ShieldWeaponUnlockLocation": max_number_room_checks+28,
    "FistWeaponUnlockLocation": max_number_room_checks+29,
    "GunWeaponUnlockLocation": max_number_room_checks+30,
}


location_store_gemstones ={
    "FountainUpgrade1Location": max_number_room_checks+31,
    "FountainUpgrade2Location": max_number_room_checks+32,
    "FountainTartarusLocation": max_number_room_checks+33,
    "FountainAsphodelLocation": max_number_room_checks+34,
    "FountainElysiumLocation": max_number_room_checks+35,
    "UrnsOfWealth1Location": max_number_room_checks+36,
    "UrnsOfWealth2Location": max_number_room_checks+37,
    "UrnsOfWealth3Location": max_number_room_checks+38,
    "InfernalTrove1Location": max_number_room_checks+39,
    "InfernalTrove2Location": max_number_room_checks+40,
    "InfernalTrove3Location": max_number_room_checks+41,
    "KeepsakeCollectionLocation": max_number_room_checks+42,
}

location_store_diamonds ={
    "DeluxeContractorDeskLocation": max_number_room_checks+44,
    "VanquishersKeepLocation": max_number_room_checks+45,
    "FishingRodLocation": max_number_room_checks+46,
    "CourtMusicianSentenceLocation": max_number_room_checks+47,
    "CourtMusicianStandLocation": max_number_room_checks+48,
    "PitchBlackDarknessLocation": max_number_room_checks+49,
    "FatedKeysLocation": max_number_room_checks+50,
    "BrilliantGemstonesLocation": max_number_room_checks+51,
    "VintageNectarLocation": max_number_room_checks+52,
    "DarkerThirstLocation": max_number_room_checks+53, 
}

location_table_fates = {
    "IsThereNoEscape?": max_number_room_checks+54,
    "DistantRelatives": max_number_room_checks+55,
    "ChthonicColleagues": max_number_room_checks+56,
    "TheReluctantMusician": max_number_room_checks+57,
    "GoddessOfWisdom": max_number_room_checks+58,
    "GodOfTheHeavens": max_number_room_checks+59,
    "GodOfTheSea": max_number_room_checks+60,
    "GoddessOfLove": max_number_room_checks+61,
    "GodOfWar": max_number_room_checks+62,
    "GoddessOfTheHunt": max_number_room_checks+63,
    "GodOfWine": max_number_room_checks+64,
    "GodOfSwiftness": max_number_room_checks+65,
    "GoddessOfSeasons": max_number_room_checks+66,
    "PowerWithoutEqual": max_number_room_checks+67,
    "DivinePairings": max_number_room_checks+68,
    "PrimordialBoons": max_number_room_checks+69,
    "PrimordialBanes": max_number_room_checks+70,
    "InfernalArms": max_number_room_checks+71,
    "TheStygianBlade": max_number_room_checks+72,
    "TheHeartSeekingBow": max_number_room_checks+73,
    "TheShieldOfChaos": max_number_room_checks+74,
    "TheEternalSpear": max_number_room_checks+75,
    "TheTwinFists": max_number_room_checks+76,
    "TheAdamantRail": max_number_room_checks+77,
    "MasterOfArms": max_number_room_checks+78,
    "AViolentPast": max_number_room_checks+79,
    "HarshConditions": max_number_room_checks+80,
    "SlashedBenefits": max_number_room_checks+81,
    "WantonRansacking": max_number_room_checks+82,
    "ASimpleJob": max_number_room_checks+83,
    "ChthonicKnowledge": max_number_room_checks+84,
    "CustomerLoyalty": max_number_room_checks+85,
    "DarkReflections": max_number_room_checks+86,
    "CloseAtHeart": max_number_room_checks+87,
    "DenizensOfTheDeep": max_number_room_checks+88,
    "TheUselessTrinket": max_number_room_checks+89,
}


location_table_fates_events = {
    "IsThereNoEscape?Event": None,
    "DistantRelativesEvent": None,
    "ChthonicColleaguesEvent": None,
    "TheReluctantMusicianEvent": None,
    "GoddessOfWisdomEvent": None,
    "GodOfTheHeavensEvent": None,
    "GodOfTheSeaEvent": None,
    "GoddessOfLoveEvent": None,
    "GodOfWarEvent": None,
    "GoddessOfTheHuntEvent": None,
    "GodOfWineEvent": None,
    "GodOfSwiftnessEvent": None,
    "GoddessOfSeasonsEvent": None,
    "PowerWithoutEqualEvent": None,
    "DivinePairingsEvent": None,
    "PrimordialBoonsEvent": None,
    "PrimordialBanesEvent": None,
    "InfernalArmsEvent": None,
    "TheStygianBladeEvent": None,
    "TheHeartSeekingBowEvent": None,
    "TheShieldOfChaosEvent": None,
    "TheEternalSpearEvent": None,
    "TheTwinFistsEvent": None,
    "TheAdamantRailEvent": None,
    "MasterOfArmsEvent": None,
    "AViolentPastEvent": None,
    "HarshConditionsEvent": None,
    "SlashedBenefitsEvent": None,
    "WantonRansackingEvent": None,
    "ASimpleJobEvent": None,
    "ChthonicKnowledgeEvent": None,
    "CustomerLoyaltyEvent": None,
    "DarkReflectionsEvent": None,
    "CloseAtHeartEvent": None,
    "DenizensOfTheDeepEvent": None,
    "TheUselessTrinketEvent": None,
}

#----------------------

location_weapons_subfixes = [
    "SwordWeapon",
    "SpearWeapon",
    "ShieldWeapon",
    "BowWeapon",
    "FistWeapon",
    "GunWeapon",
]

#---------------------

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

    global location_table_elyseum
    location_table_elyseum = {
        "Beat Bros": None,
    }

    global location_table_styx
    location_table_styx = {
        "Beat Hades": None,
    }
    
    global location_table_styx_late
    location_table_styx_late = {
    }
    

#Change parameters so they include the settings of the player
#Chose between old and new system. And for the new system we want to be able
#to choose how many "locations" we have.
def setup_location_table_with_settings(options):
    clear_tables()
    total_table = {}
 
    total_table.update(location_table_fates_events)
    
    if (options.keepsakesanity.value == 1):
        total_table.update(location_keepsakes)
     
    if (options.weaponsanity.value == 1):
        for weaponLocation, weaponData in location_weapons.items():
            if (not should_ignore_weapon_location(weaponLocation, options)):
                total_table.update({weaponLocation : weaponData})
                
    if (options.storesanity.value==1):
        total_table.update(location_store_gemstones)
        total_table.update(location_store_diamonds)

    if (options.location_system.value==1):
        result = give_default_location_table()
        total_table.update(result)
    elif (options.location_system.value==2):
        levels = options.score_rewards_amount.value
        total_table.update(give_score_location_table(levels))
    elif (options.location_system.value==3):
        total_table.update(give_weapon_based_locations())
    
    if (options.fatesanity==1):
        total_table.update(location_table_fates)
    
    return total_table
            
#-----------------------------------------------

def should_ignore_weapon_location(weaponLocation, options):
    if (options.initial_weapon.value == 0 and weaponLocation == "SwordWeaponUnlockLocation"):
        return True
    if (options.initial_weapon.value == 1 and weaponLocation == "BowWeaponUnlockLocation"):
        return True
    if (options.initial_weapon.value == 2 and weaponLocation == "SpearWeaponUnlockLocation"):
        return True
    if (options.initial_weapon.value == 3 and weaponLocation == "ShieldWeaponUnlockLocation"):
        return True
    if (options.initial_weapon.value == 4 and weaponLocation == "FistWeaponUnlockLocation"):
        return True
    if (options.initial_weapon.value == 5 and weaponLocation == "GunWeaponUnlockLocation"):
        return True
    return False


#-----------------------------------------------

def give_default_location_table():
    #Repopulate tartarus table; rooms from 1 to 13.
    global location_table_tartarus 
    for i in range(13):
        stringInt=i+1;
        if (stringInt<10):
            stringInt = "0"+str(stringInt);
        location_table_tartarus["ClearRoom"+str(stringInt)] = hades_base_location_id+i
        
    #Repopulate asphodel table, rooms from 14 to 23
    global location_table_asphodel
    for i in range(13,23):
        location_table_asphodel["ClearRoom"+str(i+1)]=hades_base_location_id+i
    
    #Repopulate elyseum table, rooms from 24 to 35
    global location_table_elyseum
    for i in range(23,35):
        location_table_elyseum["ClearRoom"+str(i+1)]=hades_base_location_id+i
    
    #Repopulate styx table, rooms from 35 to 72. Split into early and late
    global location_table_styx 
    for i in range(35,60):
        location_table_styx["ClearRoom"+str(i+1)]=hades_base_location_id+i
        
    global location_table_styx_late
    for i in range(60,72):
        location_table_styx_late["ClearRoom"+str(i+1)]=hades_base_location_id+i
    
    location_table = {
        **location_table_tartarus, 
        **location_table_asphodel,
        **location_table_elyseum,
        **location_table_styx,
        **location_table_styx_late,
    }
    return location_table

def give_score_location_table(locations):
    fraction_location = int(locations/8)
    locations_first_region = locations-7*fraction_location

    global location_table_tartarus 
    ##Recall to add a offset for the location to avoid sharing ids if two players play with different settings
    for i in range(locations_first_region):
        stringInt=str(i+1);
        while (len(stringInt)<4):
            stringInt = "0"+str(stringInt);
        location_table_tartarus["ClearScore"+str(stringInt)]=hades_base_location_id+i+72 

    global location_table_asphodel
    for i in range(locations_first_region, locations_first_region+2*fraction_location):
        stringInt=str(i+1);
        while (len(stringInt)<4):
            stringInt = "0"+str(stringInt);
        location_table_asphodel["ClearScore"+stringInt]=hades_base_location_id+i+72 
        
    global location_table_elyseum
    for i in range(locations_first_region+2*fraction_location, locations_first_region+4*fraction_location):
        stringInt=str(i+1);
        while (len(stringInt)<4):
            stringInt = "0"+str(stringInt);
        location_table_elyseum["ClearScore"+stringInt]=hades_base_location_id+i+72 
    
    global location_table_styx
    for i in range(locations_first_region+4*fraction_location, locations_first_region+6*fraction_location):
        stringInt=str(i+1);
        while (len(stringInt)<4):
            stringInt = "0"+str(stringInt);
        location_table_styx["ClearScore"+stringInt]=hades_base_location_id+i+72 
        
    global location_table_styx_late
    for i in range(locations_first_region+6*fraction_location, locations):
        stringInt=str(i+1);
        while (len(stringInt)<4):
            stringInt = "0"+str(stringInt);
        location_table_styx_late["ClearScore"+stringInt]=hades_base_location_id+i+72 

    location_table = {
        **location_table_tartarus, 
        **location_table_asphodel,
        **location_table_elyseum,
        **location_table_styx,
        **location_table_styx_late,
    }
    
    return location_table
    

def give_weapon_based_locations():
    subfixCounter = 0
    weapon_locations = {}
    
    for weaponSubfix in location_weapons_subfixes:
    
        for i in range(13):
            stringInt=i+1;
            if (stringInt<10):
                stringInt = "0"+str(stringInt);
            weapon_locations["ClearRoom"+str(stringInt)+weaponSubfix] = hades_base_location_id+1073+i+subfixCounter*73
        weapon_locations["Beat Meg"+weaponSubfix] = None

        for i in range(13,23):
            weapon_locations["ClearRoom"+str(i+1)+weaponSubfix]=hades_base_location_id+1073+i+subfixCounter*73
    
        weapon_locations["Beat Lernie"+weaponSubfix] = None

        for i in range(23,35):
            weapon_locations["ClearRoom"+str(i+1)+weaponSubfix]=hades_base_location_id+1073+i+subfixCounter*73
        weapon_locations["Beat Bros"+weaponSubfix] = None    

        for i in range(35,60):
            weapon_locations["ClearRoom"+str(i+1)+weaponSubfix]=hades_base_location_id+1073+i+subfixCounter*73
        
        weapon_locations["Beat Hades"+weaponSubfix] = None

        for i in range(60,72):
            weapon_locations["ClearRoom"+str(i+1)+weaponSubfix]=hades_base_location_id+1073+i+subfixCounter*73
            
        subfixCounter += 1
    
    return weapon_locations

#-----------------------------------------------



group_fates = {"fates" : location_table_fates.keys()}
group_keepsakes = {"keepsakes" : location_keepsakes.keys()}
group_weapons = {"weapons" : location_weapons.keys()}
group_contractor_gemstones = {"contractor_gems" : location_store_gemstones.keys()}
group_contractor_diamonds = {"contractor_diamonds" : location_store_diamonds.keys()}

location_name_groups = {
    **group_fates,
    **group_keepsakes,
    **group_weapons,
    **group_contractor_gemstones,
    **group_contractor_diamonds,
}


#-----------------------------------------------

class HadesLocation(Location):
    game: str = "Hades"

    def __init__(self, player: int, name: str, address=None, parent=None):
        super(HadesLocation, self).__init__(player, name, address, parent)
        if address is None:
            self.event = True
            self.locked = True