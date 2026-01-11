from typing import Callable, TYPE_CHECKING

from BaseClasses import CollectionState
from .Items import elemental_stones

if TYPE_CHECKING:
    from . import BombTSAWorld

def has_all_elements(state,player): # Debug, checks to see if you have all the element stones
    return (state.has("Fire Stone",player) and state.has("Ice Stone",player) and state.has("Wind Stone",player) and state.has("Earth Stone",player)
                    and state.has("Lightning Stone",player) and state.has("Dark Stone",player) and state.has("Light Stone",player) )

def can_destroy_with_immunity(state, player, immunities):
    #stones = ["Fire Stone","Ice Stone","Wind Stone","Earth Stone","Lightning Stone","Dark Stone","Light Stone"]
    stones = elemental_stones.copy()
    for badstone in immunities:
        stones.pop(stones.index(badstone))
    for havestone in stones:
        if state.has(havestone, player):
            return True
    return False

def can_open_car(state, player):
    return lambda state: state.has("Guardian Glove", player) or (state.has("Earth Stone", player) and state.has("FireUp", player, 2))

def has_all_guardian(state, player): # Debug, checks to see if you have all the guardian armor
    return state.has("Guardian Glove", player) and state.has("Guardian Helmet", player) and state.has("Guardian Boots", player)

def can_build_ice(state, player):
    return state.has("Ice Stone",player) and can_move_bombs(state,player) 

def has_multibomb(state, player): # has a bomb that can place more than 1 of itself
    return state.has("Fire Stone",player) or state.has("Ice Stone",player) or state.has("Wind Stone",player) or state.has("Lightning Stone",player)

def can_destroy(state,player):
    return state.has("Fire Stone",player) or state.has("Electric Stone",player) or state.has("Ice Stone",player) or state.has("Earth Stone", player)

def can_kill_chompers(state, player):
    return can_destroy_with_immunity(state, player, ["Light Stone","Wind Stone"])

def can_bomb_jump(state,player): # Depreciated? 
    return (state.has("Fire Stone",player) or state.has("Electric Stone",player) or state.has("Ice Stone",player) or state.has("Wind Stone", player)) and state.has("BombUp", player, 2)

def can_drain_aquanet_fountain(state, player):
    return (state.has("Guardian Glove", player) and has_multibomb(state, player) and state.has("BombUp", player)) or can_build_ice(state, player),

def can_hit_high_object(state,player):
    return state.has("Guardian Glove", player) or (state.has("Ice Stone",player) and state.has("FireUp", player, 2)) or state.has("Dark Stone", player) or state.has("Light Stone", player)

def starlight_card_hunt(state, player):
    return state.can_reach_location("Starlight Zhael Defeated", player) and state.can_reach_region("Starlight, Wheel of Fortune", player),

def can_hit_fountain(state, player):
    return state.has("Ice Stone", player) and (state.has("Guardian Glove", player) or state.has("FireUp", player, 2))

def can_build_ladder(state,player,bombcnt):
    return state.has("Guardian Glove", player) and state.has("Guardian Helmet", player) and (((state.has("Fire Stone", player) or state.has("Lightning Stone", player)) and state.has("BombUp", player, bombcnt)) or (has_multibomb(state, player) and state.has("BombUp", player, (bombcnt+1))))

def can_move_bombs(state,player): # Can kick or throw
    return state.has("Guardian Glove", player) or state.has("Guardian Boots", player)

def get_region_rules(player):
    return {
        "Menu -> Alcatraz":
            lambda state: can_destroy_with_immunity(state, player, ["Dark Stone","Light Stone"]),
        "Menu -> Aquanet":
            lambda state: state.has("Aquanet Coordinates", player),
        "Menu -> Horizon":
            lambda state: state.has("Horizon Coordinates", player),
        "Menu -> Starlight":
            lambda state: state.has("Starlight Coordinates", player),
        "Menu -> Neverland":
            lambda state: state.has("Neverland Coordinates", player),
        "Menu -> Epikyur":
            lambda state: state.has("Epikyur Coordinates", player),
        "Menu -> Thantos":
            lambda state: state.has("Thantos Coordinates", player),
        #"Aquanet -> Aquanet Elevator":
        #    lambda state: (state.has("Guardian Glove", player) and has_multibomb(state, player) and state.has("BombUp", player)) or can_build_ice(state, player),
        #"Aquanet Elevator -> Aquanet Tower":
        #    lambda state: can_hit_fountain(state, player) and state.has("Fire Stone", player),
        
        #"Horizon -> Horizon Basement":
        #    lambda state: state.has("Blue Gems", player) and can_destroy_with_immunity(state,player,["Wind Stone"]),
        
        #"Starlight -> Starlight Card Hunt":
        #    lambda state: can_destroy_with_immunity(state, player, ["Fire Stone","Earth Stone","Wind Stone","Light Stone"]),
        
        #"Epikyur -> Epikyur Haunted House":
        #    lambda state: can_hit_fountain(state, player) and state.has("Guardian Glove", player) and state.has("Wind Stone", player) and state.has("Earth Stone", player),
        #"Epikyur -> Epikyur Museum":
        #    lambda state: state.has("Earth Stone", player),
        #"Epikyur Haunted House -> Epikyur Coaster":
        #    lambda state: state.has("Earth Stone", player) and state.has("Museum Pass", player),
        
        #"Thantos -> Thantos Trainside":
        #    lambda state: state.has("Train Batteries", player) and can_destroy_with_immunity(state, player, ["Dark Stone"]),

        "Noah -> Noah Core":
            lambda state: has_all_elements(state,player) and has_all_guardian(state, player),
        "Menu -> Shop":
            lambda state: can_destroy_with_immunity(state, player, ["Dark Stone"]),
        "Shop -> Shop Aquanet":
            lambda state: state.can_reach_location("Aquanet Generator", player),
        "Shop -> Shop Horizon":
            lambda state: state.can_reach_location("Horizon Generator", player),
        "Shop -> Shop Starlight":
            lambda state: state.can_reach_location("Starlight Generator", player),
        "Shop -> Shop Neverland":
            lambda state: state.can_reach_location("Neverland Generator", player),
        "Shop -> Shop Epikyur":
            lambda state: state.can_reach_location("Epikyur Generator", player),
        "Shop -> Shop Thantos":
            lambda state: state.can_reach_location("Thantos Generator", player),
 
 
        # Alcatraz
        "Alcatraz, Prison -> Alcatraz, Secret Room 1":
            lambda state: state.can_reach_location("Alcatraz Baelfael Defeated", player),
        "Alcatraz, Sewer Entrance -> Alcatraz, Twisted Sewers":
	        lambda state: can_destroy_with_immunity(state, player, ["Dark Stone"]),
        "Alcatraz, Security Room A -> Alcatraz, Security Room B":
            lambda state: can_destroy_with_immunity(state, player, ["Light Stone"]),
        "Alcatraz, Security Room B -> Alcatraz, Sewage Disposal":
            lambda state: can_destroy_with_immunity(state, player, ["Light Stone"]),
        "Alcatraz, Sewage Disposal -> Alcatraz, Secret Room 2":
            lambda state: state.can_reach_location("Alcatraz Baelfael Defeated", player),
        "Alcatraz, Twisted Sewers -> Alcatraz, Through the Pipe":
            lambda state: state.can_reach_location("Alcatraz Baelfael Defeated", player),
        
        "Alcatraz, Through the Pipe -> Alcatraz, Prison Bridge":
            lambda state: can_destroy_with_immunity(state, player, ["Dark Stone"]),
        "Alcatraz, Pipe Room B -> Alcatraz, Final Defense Unit":
            lambda state: can_destroy_with_immunity(state, player, ["Light Stone"]),
 
        # Aquanet
        "Aquanet, First Room -> Aquanet, Second Room":
            lambda state: can_destroy_with_immunity(state, player, ["Dark Stone"]),
        "Aquanet, Swimming Pool Spa -> Aquanet, Behind the Moat":
            lambda state: can_destroy_with_immunity(state, player, ["Dark Stone"]),
        "Aquanet, Swimming Pool Spa -> Aquanet, Secret Room 1":
            lambda state: can_destroy_with_immunity(state, player, ["Dark Stone"]),
        "Aquanet, Around the Moat -> Aquanet, Secret Room 2":
            lambda state: state.has("Earth Stone", player),
        "Aquanet, Around the Moat -> Aquanet, Secret Room 2":
            lambda state: can_destroy_with_immunity(state, player, ["Dark Stone"]),
        "Aquanet, Elevator Hub -> Aquanet, Hidden Balcony":
            lambda state: can_destroy_with_immunity(state, player, ["Dark Stone"]),
        "Aquanet, Hidden Balcony -> Aquanet, Water Channels":
            lambda state: can_destroy_with_immunity(state, player, ["Ice Stone"]),
        "Aquanet, Water Channels -> Aquanet, Fountain Room":
            lambda state: can_drain_aquanet_fountain(state, player),
        "Aquanet, Elevator Hub -> Aquanet, Behemos' Lair":
            lambda state: can_drain_aquanet_fountain(state, player) and can_destroy_with_immunity(state, player, ["Dark Stone"]),
        "Aquanet, Tower 1F -> Aquanet, Tower 2F":
            lambda state: state.has("Fire Stone", player) and state.has("Ice Stone", player) and state.has("Guardian Glove", player),
        "Aquanet, Tower 2F -> Aquanet, Tower 3F":
            lambda state: can_build_ice(state, player) and can_destroy_with_immunity(state, player, ["Ice Stone"]),
        "Aquanet, Fountain Room -> Aquanet, Secret Room 3":
            lambda state: state.can_reach_location("Aquanet Generator", player),

        # Horizon
        "Horizon, Eastern Tower -> Horizon, First Trial":
            lambda state: can_destroy_with_immunity(state, player, ["Light Stone","Wind Stone"]),
        "Horizon, Leading Road -> Horizon, Resting Point":
            lambda state: state.has("Blue Gems", player) and can_destroy_with_immunity(state,player,["Wind Stone"]),
        "Horizon, Floating Temple -> Horizon, Secret Room 1":
            lambda state: state.has("Wind Stone", player),
        "Horizon, Last Route -> Horizon, Fourth Trial":
            lambda state: can_destroy_with_immunity(state, player, ["Light Stone"]),
        "Horizon, Fourth Trial -> Horizon, Secret Room 2":
            lambda state: state.has("Lightning Stone",player) and state.has("Guardian Helmet", player) and state.has("Guardian Glove", player) and state.has("Wind Stone", player),
        "Horizon, Final Deposit -> Horizon, Gravity Generator Room":
            lambda state: state.has("Red Gem", player),
 
        # Starlight
        "Starlight, Parking Lot -> Starlight, Closed Road":
            lambda state: can_destroy_with_immunity(state, player, ["Dark Stone"]),
        "Starlight, Closed Road -> Starlight, Fountain Square":
            lambda state: can_destroy_with_immunity(state, player, ["Dark Stone"]),
        "Starlight, Closed Road -> Starlight, Hidden Room":
            lambda state: state.can_reach_location("Starlight Zhael Defeated", player),
        "Starlight, Fountain Square -> Starlight, Small Inlet":
            lambda state: can_destroy_with_immunity(state, player, ["Light Stone", "Wind Stone"]),
        "Starlight, Small Inlet -> Starlight, Alleyway":
            lambda state: can_destroy_with_immunity(state, player, ["Dark Stone"]),
        "Starlight, Casino Entrance -> Starlight, Casino Lobby":
            lambda state: can_destroy_with_immunity(state, player, ["Light Stone", "Wind Stone"]),
        "Starlight, Casino Lobby -> Starlight, Slots Room":
            lambda state: can_destroy_with_immunity(state, player, ["Light Stone"]),
        "Starlight, Casino Lobby -> Starlight, Betting Room":
            lambda state: can_destroy_with_immunity(state, player, ["Dark Stone"]),
        "Starlight, Waiting Room -> Starlight, Stage Area":
            lambda state: can_destroy_with_immunity(state, player, ["Dark Stone"]),
        "Starlight, Slots Room -> Starlight, Lookout Point":
            lambda state: state.can_reach_location("Starlight Zhael Defeated", player) and state.can_reach_region("Starlight, Slots Room", player),
        "Starlight, Fountain Square -> Starlight, Gravity Generator Room":
            lambda state: state.has("Royal Straight", player),
 

        # Neverland
        "Neverland, Entry Point -> Neverland, Through the Line of Fire":
            lambda state: can_kill_chompers(state, player),
        "Neverland, Intersection -> Neverland, Secret Room 1":
            lambda state: state.has("Dark Stone", player) and ((state.has("Ice Stone", player) and can_move_bombs(state,player) )or state.has("Wind Stone", player)),
        "Neverland, Intersection -> Neverland, Conveyor Belts":
            lambda state: can_kill_chompers(state, player),
        "Neverland, Intersection -> Neverland, Potholes":
            lambda state: can_kill_chompers(state, player),
        "Neverland, Potholes -> Neverland, Second Passageway":
            lambda state: can_destroy_with_immunity(state, player, ["Light Stone","Wind Stone"]) and state.can_reach_region("Neverland, Conveyor Belts", player),
        "Neverland, Carrier Works -> Neverland, Switch Room":
            lambda state: (state.has("Skates", player) or can_move_bombs(state, player)) and can_kill_chompers(state, player),
        "Neverland, Switch Room -> Neverland, Secret Room 2":
            lambda state: state.has("Ice Stone", player) and can_move_bombs(state, player) and state.can_reach_location("Neverland Molok Defeated", player),
        "Neverland, Furnace -> Neverland, Safe Point":
            lambda state: can_destroy_with_immunity(state, player, ["Dark Stone"]),
        "Neverland, Bridge Room -> Neverland, Third Passageway":
            lambda state: state.can_reach_region("Neverland, Cage Room", player),
 
        # Epikyur
        "Epikyur, Center Fountain -> Epikyur, Tattered Bridge":
            lambda state: state.has("Ice Stone",player) and (state.has("Guardian Glove", player) or state.has("FireUp", player, 3)),
        "Epikyur, Tattered Bridge -> Epikyur, Haunted House Yard":
            lambda state: state.has("Earth Stone", player),
        "Epikyur, Haunted House Yard -> Epikyur, Haunted House Lobby":
            lambda state: state.has("Guardian Glove", player),
        "Epikyur, Haunted House Lobby -> Epikyur, Haunted House Spike Traps":
            lambda state: state.has("Wind Stone", player),
        "Epikyur, Haunted House Storeroom -> Epikyur, Haunted House Coaster Start":
            lambda state: state.has("Museum Pass", player),
        "Epikyur, Haunted House Coaster Start -> Epikyur, Coaster Finish":
            lambda state: state.has("Coaster Battery", player),
        "Epikyur, Center Fountain -> Epikyur, Castle of Time First Room":
            lambda state: state.can_reach_location("Epikyur Zoniha Defeated", player),
        "Epikyur, Center Fountain -> Epikyur, Misaligned Bridge":
            lambda state: state.has("Earth Stone", player),
        "Epikyur, Castle of Time Second Room -> Epikyur, Gravity Generator Room":
            lambda state: state.has("Fire Stone", player) and state.has("Ice Stone", player) and state.has("Wind Stone", player) and state.has("Lightning Stone", player) and state.has("Earth Stone", player),
 
        # Thantos
        "Thantos, Hangout -> Thantos, Secret Room 1":
            lambda state: state.has("Earth Stone", player),
        "Thantos, Back Alley -> Thantos, Gravity Generator Room":
            lambda state: state.has("Dark Stone", player),
        "Thantos, Streets -> Thantos, Wrecked Lot":
            lambda state: state.has("Earth Stone", player) or state.has("Guardian Glove", player),
        "Thantos, Wrecked Lot -> Thantos, Battle for the Battery":
            lambda state: can_destroy_with_immunity(state, player, ["Dark Stone"]),
        "Thantos, Battle for the Battery -> Thantos, Compactor":
            lambda state: state.has("Light Stone", player),
        #"Thantos, Wrecked Lot -> Thantos, Battery Ambush":
        "Thantos, Subway Entrance -> Thantos, Aboard the Subway":
            lambda state: state.has("Train Batteries", player),
        "Thantos, Supposed Dead End -> Thantos, The Crevice":
            lambda state: can_destroy_with_immunity(state, player, ["Dark Stone"]),
        "Thantos, The Crevice -> Thantos, Voltage Storage Unit":
            lambda state: state.has("Wind Stone", player),
        "Thantos, Voltage Storage Unit -> Thantos, Secret Room 3":
            lambda state: state.has("Earth Stone", player),
        "Thantos, Hidden Territory -> Thantos, Top of the Tower":
            lambda state: state.has("Lightning Stone",player) and state.has("Guardian Boots", player) and state.can_reach_region("Thantos, Voltage Storage Unit", player),




 
 }      



#"Rule":
#            lambda state: state.has("Item", player, 3),

def get_location_rules(player):
    return {
       
        #"Guardian Armor Body":
        #    lambda state: state.has("Guardian Helmet",player) and state.has("Guardian Glove",player) and state.has("FireUp", player, 3) and state.has("Ice Stone", player),

        # Alcatraz
        "Alcatraz Part Red":
            lambda state: state.can_reach_region("Alcatraz, Prison Bridge", player),
        "Alcatraz Part Yellow":
            lambda state: state.has("Guardian Glove", player),
        "Alcatraz Generator":
            lambda state: can_hit_high_object(state,player),

        # Aquanet
        "Aquanet Part Blue":
            lambda state: can_build_ladder(state,player, 3),
        "Aquanet Guardian Armor":
            lambda state: state.has("Earth Stone", player),
        "Aquanet Remote Fountain Room":
            lambda state: state.has("Guardian Glove", player),
        "Aquanet Remote To the Tower":
            lambda state: state.has("Guardian Glove", player),
         # Glove
        #"Aquanet Behemos Defeated":
        #    lambda state: state.has("Guardian Glove", player) and state.has("Bomb"),
        #"Aquanet Remote To the Tower":
        #    lambda state: 
         # Ice bomb + Fire Bomb
        "Aquanet Part Yellow":
            lambda state: state.has("Wind Stone", player) and state.has("Guardian Glove", player),
        "Aquanet Generator":
            lambda state: state.has("Ice Stone", player) and can_destroy_with_immunity(state, player, ["Ice Stone","Dark Stone"]),


        # Horizon
        "Horizon Right Blue Jewel":
            lambda state: can_destroy_with_immunity(state,player,["Wind Stone"]) or can_move_bombs(state,player),
        "Horizon Part Blue":
            lambda state: can_destroy_with_immunity(state,player,["Dark Stone"]),
        "Horizon Remote Second Trial":
            lambda state: can_destroy_with_immunity(state,player,["Dark Stone"]),
        "Horizon Part Red":
            lambda state: can_build_ladder(state,player, 1),

         # Two Blue Gems
        "Horizon Remote Final Deposit":
            lambda state: state.has("Guardian Glove", player),
         # Wind Bomb
        "Horizon Right Green Jewel":
            lambda state: state.has("Wind Stone", player),
        
        "Horizon Guardian Armor":
            lambda state: state.has("Lightning Stone", player) and state.has("Wind Stone", player) and state.has("Guardian Glove", player),
        "Horizon Part Yellow":
            lambda state: state.has("Wind Stone", player),
         # Two Green Gem
        "Horizon Left Green Jewel":
            lambda state: state.has("Wind Stone", player),
        "Horizon Right Green Jewel":
            lambda state: state.has("Guardian Helmet", player) and state.has("Wind Stone", player),
        "Horizon Middle Green Jewel":
            lambda state: state.has("Wind Stone", player) and state.has("Green Gems", player),
        
        "Horizon Red Jewel":
            lambda state: state.has("Wind Stone", player) and state.has("Green Gems", player),
         # Red Gem
        "Horizon Generator":
            lambda state: state.has("Wind Stone", player) and can_move_bombs(state, player),

        # Starlight
        "Starlight Part Red":
            lambda state: can_build_ladder(state, player, 3),
        "Starlight Part Blue":
            lambda state: can_move_bombs(state, player) and state.can_reach_region("Starlight, Slots Room", player),
        "Starlight Remote Casino Lobby":
            lambda state: can_build_ladder(state, player, 2),
        "Starlight Remote Waiting Room":
            lambda state: state.has("Wind Stone", player),
        "Starlight Generator":
            lambda state: state.has("Lightning Stone", player) and can_build_ice(state, player) and can_move_bombs(state, player),
        "Starlight Zhael Defeated":
            lambda state: can_destroy_with_immunity(state, player, ["Dark Stone"]),
        "Starlight Part Yellow":
            lambda state: state.can_reach_location("Starlight Zhael Defeated", player),
        "Starlight King Of Clubs":
            lambda state: starlight_card_hunt(state, player),
        "Starlight Knight Of Diamonds":
            lambda state: starlight_card_hunt(state, player),
        "Starlight Ace Of Spaces":
            lambda state: starlight_card_hunt(state, player),
        "Starlight Queen Of Hearts":
            lambda state: starlight_card_hunt(state, player),

        # Neverland
        "Neverland Part Red":
            lambda state: state.has("Wind Stone", player) or can_build_ladder(state, player, 2),
        "Neverland Remote Bonus Room":
            lambda state: state.has("Wind Stone", player) or can_build_ladder(state, player, 3),
        "Neverland Part Blue":
            lambda state: can_build_ladder(state, player, 3),
        "Neverland Molok Defeated":
            lambda state: can_destroy_with_immunity(state, player, ["Dark Stone"]),
        #"Neverland Guardian Armor":
        #    lambda state: state.has("Dark Stone", player) and ((state.has("Ice Stone", player) and can_move_bombs(state,player) )or state.has("Wind Stone", player)),
        "Neverland Generator":
            lambda state: state.has("Earth Stone", player) and can_build_ice(state, player) and state.has("Guardian Boots", player) and state.has("Wind Stone", player),
        
        # Epikyur
        "Epikyur Haunted House Pass":
            lambda state: state.has("Guardian Glove", player),
        "Epikyur Coaster Battery":
            lambda state: state.has("Haunted House Pass", player),
        "Epikyur Zoniha Defeated":
            lambda state: can_destroy_with_immunity(state, player, ["Dark Stone"]),
        "Epikyur Glove Center Fountain":
            lambda state: can_build_ice(state, player),
        "Epikyur Part Green":
            lambda state: state.has("Wind Stone", player),
        "Epikyur Part Yellow":
            lambda state: can_build_ladder(state, player, 2),
        "Epikyur Museum Pass":
            lambda state: state.has("Lightning Stone", player),
        "Epikyur Generator":
            lambda state: state.has("Lightning Stone", player) and state.has("Wind Stone", player) and state.has("BombUp", player, 2) and state.has("Guardian Boots", player) and (state.has("Guardian Glove", player) or state.has("Light Stone", player)),
            
        # Thantos
        "Thantos Part Yellow": 
            lambda state: state.has("Earth Stone", player),
        "Thantos Generator":
            lambda state: can_build_ice(state, player) and state.has("Dark Stone", player) and state.has("Wind Stone", player) and state.has("Earth Stone", player),
        "Thantos Lower Train Battery":
            lambda state: can_open_car(state, player),
        "Thantos Upper Train Battery":
            lambda state: can_open_car(state, player) and (state.has("Lightning Stone", player) or state.has("Earth Stone", player)) ,
        "Thantos Part Red":
            lambda state: can_open_car(state, player) and state.has("Light Stone", player),
        "Thantos Part Blue":
            lambda state: can_destroy_with_immunity(state, player, ["Dark Stone"]),
        "Thantos Remote Crevice":
            lambda state: state.has("Wind Stone", player),
        "Thantos Part Green":
            lambda state: state.has("Wind Stone", player) and state.has("Earth Stone", player),
        "Thantos Bulzeeb Defeated":
            lambda state: can_destroy_with_immunity(state, player, ["Dark Stone"]),

        # Noah'
        "Noah Card Key 1":
            lambda state: state.has("Guardian Boots", player),
        "Noah Card Key 2":
            lambda state: state.has("Lightning Stone", player) and state.has("Earth Stone", player),
        "Noah Card Key 3":
            lambda state: state.has("Lightning Stone", player) and state.has("Earth Stone", player),

        # Pommy Transforms
        "Pommy Beast Transformation":
            lambda state: state.has("Pommy Animal Gene", player),
        "Pommy Dinosaur Transformation":
            lambda state: state.has("Pommy Beast Gene", player),
        "Pommy Shadow Transformation":
            lambda state: state.has("Pommy Beast Gene", player) or state.has("Pommy Penguin Gene", player),
        "Pommy Dragon Transformation":
            lambda state: state.has("Pommy Penguin Gene", player),
        "Pommy Bird Transformation":
            lambda state: state.has("Pommy Penguin Gene", player),
        "Pommy Chicken Transformation":
            lambda state: state.has("Pommy Penguin Gene", player),
        
        "Pommy Claw Transformation":
            lambda state: state.has("Pommy Knuckle Gene", player),
        "Pommy Hammer Transformation":
            lambda state: state.has("Pommy Knuckle Gene", player),
        "Pommy Pixie Transformation":
            lambda state: state.has("Pommy Claw Gene", player) or state.has("Pommy Hammer Gene", player),
        "Pommy Cat Transformation":
            lambda state: state.has("Pommy Claw Gene", player),
        "Pommy Devil Transformation":
            lambda state: state.has("Pommy Claw Gene", player),
        "Pommy Knight Transformation":
            lambda state: state.has("Pommy Hammer Gene", player),
        "Pommy Mage Transformation":
            lambda state: state.has("Pommy Hammer Gene", player),
    }
