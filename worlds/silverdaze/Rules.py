from BaseClasses import CollectionState
from typing import TYPE_CHECKING
from worlds.generic.Rules import add_rule, forbid_item
from .Names.LocationName import LocationName
from .Locations import all_locations, hidden
from . import StateLogic

if TYPE_CHECKING:
    from . import SDWorld

#Return the number of party members the player has received... somehow.
def get_party_total(world: "SDWorld") -> int:
    return 1
  
#Return if the Red Key item has been given to the player.  
def owns_red_key(state: CollectionState, player: int) -> bool:
    return state.has("Red Key", player)

#Return if the Yellow Key item has been given to the player.
def owns_yellow_key(state: CollectionState, player: int) -> bool:
    return state.has("Yellow Key", player)   
###Sawyer: After this point we would start adding the other keys.

#For Zone Checks we'll try to Lambda from the StateLogic file which will have all the rules to enter a zone. This way we don't have to repeat stuff.
#Return if the player is allowed access to Red Zone 1
def red(state: CollectionState, player: int) -> bool:
    lambda state: StateLogic.red(state, world.player)

#Return if the player is allowed access to Red Zone 2 (Behind Yellow Door)
def red2(state: CollectionState, player: int) -> bool:
    lambda state: StateLogic.red2(state, world.player)
###Sawyer: After this point we would start adding the other zones.

###Sawyer: Here we would place the ReCollections

#And now we start assinging things to rules!
def set_rules(world: "SDWorld", player: int):
    grey_zone = {
        "PinnJoin",
        if party(state, player) > 1 [
        #Need at least one party member to get these.
            "Ultima",
            "StarterHealToken1",
            "StarterHealToken2",
            "GeoJoin",
            "Cotton2Chest1",
            "Cotton3Chest1",
            "YellowKey",
            "PinnMP3",
            "GeoMP3",
            "GeoWeapon1",
            
        ],
        if state.has(("Yellow Key",player)) [
        #Need the yellow key to get these.
            "Hub2Chest1",
        ],
        if red2(state, player) and state.has(("Red Key",player)) [
        #Need access to Red2 and own the Red Key
            "Hub2Chest2"
        ],
    }
    red_zone = {
        if red(state, player)[
        #Need access to Red1
            "Red3Chest",     
            "QuoDefender1",
            "QuoDefender2",
            "QuoDefender3",
            
        ],
        if red(state,player) and state.has(("Red Key",player)) [
        #Need access to Red1 and own the Red Key
            "Red1Chest",
            "Red3_BackdoorChest"
        ],
        if red2(state, player)[
        #Need access to Red2
            "Red4Chest1",
            "Red4Chest2",
            "Red4Chest3",
            "RedTower2Chest",
            "RedTower4Chest",
            "Nyx",
            "Kani",
            "RedChasm1Chest",
            "RedChasm2Chest1",
            "RedChasmReunionChest",
            "Kingoose1",
            "Kingoose2",
            "Kingoose3",
            "Nyx1",
            "Nyx2",
            "Nyx3",
            "KaniMP3",
            "KaniWeapon1",
            "KaniWeapon2",
            "KaniWeapon3",   
        ],
        if red2(state,player) and state.has(("Red Key",player)) [
        #Need access to Red1 and own the Red Key
            "RedChasm2Chest2",
        ],
    }

    
# Win condition.
#For the demo, the win condition is 3 party members. In the final game there'll be an actual state for game completion (defeating the final boss).
world.multiworld.completion_condition[player] = lambda state: state.get_party_total(player) > 2