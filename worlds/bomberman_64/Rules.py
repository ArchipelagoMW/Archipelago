from typing import Callable, TYPE_CHECKING

from BaseClasses import CollectionState

if TYPE_CHECKING:
    from . import Bomb64World

def can_lower_bridge(state, player):
    return state.has("Power Glove", player) or state.has("Power Bombs", player)


def can_move_bombs(state,player):
    return state.has("Power Glove", player) or state.has("Bomb Kick", player)

def can_hit_floating(state,player):
    return state.has("Power Glove", player) and (state.has("Remote Bombs", player) or (state.has("Power Bombs", player) and state.has("Fireup", player, 2)))

def can_build_bridge(state,player):
    return state.has("Power Glove", player) and state.has("Remote Bombs", player) and state.has("Bombup",player)

def can_fight_mainboss(state,player):
    return state.has("Remote Bombs", player) and state.has("Power Glove", player)

def get_region_rules(player, cards):
    return {
        "Menu -> Black Fortress":
            lambda state: state.has("Black Key", player, 1),
        "Black Fortress -> Vs Altair":
            lambda state: state.has("Black Key", player, 3) and state.has("Gold Card", player, cards) and state.has("Bomb Kick", player),
        
        "Green Garden -> Friend or Foe":
            lambda state: state.has("Green Key", player),
        "Green Garden -> To Have or Have Not":
            lambda state: state.has("Green Key", player, 2) and state.has("Power Glove", player),
        "Green Garden -> Winged Guardian":
            lambda state: state.has("Green Key", player, 3) and can_fight_mainboss(state,player),
        
        "Blue Resort -> Switches and Bridges":
            lambda state: can_lower_bridge(state, player),
            #lambda state: state.has("Power Glove", player) or state.has("Power Bombs", player),
        "Blue Resort -> Vs Artemis":
            lambda state: state.has("Blue Key", player),
        "Blue Resort -> Pump It Up":
            lambda state: state.has("Blue Key", player, 2),
        "Blue Resort -> Sewer Savage":
            lambda state: state.has("Blue Key", player, 3) and can_fight_mainboss(state,player) ,
        
        "Red Mountain -> Vs Orion":
            lambda state: state.has("Red Key", player),
        "Red Mountain -> On the Right Track":
            lambda state: state.has("Red Key", player, 2),
        "Red Mountain -> Hot Avenger":
            lambda state: state.has("Red Key", player, 3) and can_fight_mainboss(state,player),
        
        "White Glacier -> Vs Regulus":
            lambda state: state.has("White Key", player),
        "White Glacier -> Shiny Slippery Icy Floor":
            lambda state: state.has("White Key", player, 2),
        "White Glacier -> Cold Killer":
            lambda state: state.has("White Key", player, 3) and can_fight_mainboss(state,player),
        
        "Black Fortress -> Go For Broke":
            lambda state: state.has("Black Key", player, 1),
        "Black Fortress -> High Tech Harvester":
            lambda state: state.has("Black Key", player, 2) and can_fight_mainboss(state,player) and state.has("Bomb Kick", player),
        "Black Fortress -> Trap Tower":
            lambda state: state.has("Black Key", player, 3),
        #"Black Fortress -> Vs Altair":
        #    lambda state: state.has("Black Key", player, 3) and state.has("Power Glove", player) and state.has("Bomb Kick", player),
    
        "Untouchable Treasure -> Untouchable Treasure Clear":
            lambda state: state.has("Bomb Kick", player) or (state.has("Power Bombs",player ) and state.has("Power Glove",player)),
        "To Have or Have Not -> To Have or Have Not Clear":
            lambda state: state.has("Green Key", player, 2) and state.has("Bomb Kick", player) and can_lower_bridge(state, player),
        #"Switches and Bridges -> Switches and Bridges Clear":
        #    lambda state: can_lower_bridge(state, player),
        "Pump It Up -> Pump It Up Clear":
            lambda state: state.has("Power Bombs", player),
        "Hot On The Trail -> Hot On The Trail Clear":
            lambda state: state.has("Power Glove", player),
        "Blizzard Peaks -> Blizzard Peaks Clear":
            lambda state: state.has("Power Glove", player) or state.has("Power Bombs", player),
        
        "Go For Broke -> Go For Broke Clear":
            lambda state: can_move_bombs(state, player) and state.has("Power Bombs", player),
        "Black Fortress -> Rainbow Palace":
            lambda state: state.has("Gold Card", player, cards >> 2),
        "Rainbow Palace -> Beyond the Clouds":
            lambda state: state.has("Gold Card", player, cards >> 2),
        "Beyond the Clouds -> Beyond the Clouds Clear":
            lambda state: can_build_bridge(state,player) and state.has("Bomb Kick", player) and state.has("Bombup", player, 4),
        "Rainbow Palace -> Vs Spellmaker":
            lambda state: state.has("Gold Card", player, cards >> 1) and state.has("Power Glove", player),
        "Rainbow Palace -> Doom Castle":
            lambda state: state.has("Gold Card", player, (cards >> 1) + (cards >> 2)),
        "Doom Castle -> Doom Castle Clear":
            lambda state: can_build_bridge(state, player) and state.has("Bomb Kick", player) and state.has("Bombup", player, 4),
    }      

#def get_palace_region_rules(player, cards):
#    return {#
#
#    }

def get_location_rules(player):
    return {
        "Untouchable Treasure Card 2":
            lambda state: state.has("Power Bombs", player),
        "Untouchable Treasure Card 3":
            lambda state: state.has("Power Bombs", player) and state.has("Remote Bombs", player),
        "Untouchable Treasure Card 1": # Power Glove needed for bombup too
            lambda state: (state.has("Bombup", player) and state.has("Remote Bombs", player) and state.has("Power Glove", player)) or state.has("Power Bombs", player),

        "To Have or Have Not Card 1":
            lambda state: can_hit_floating(state, player),
        "To Have or Have Not Card 3":
            lambda state: state.has("Bomb Kick", player),

        "Switches and Bridges Card 1":
            lambda state: state.has("Power Glove", player),
        "Switches and Bridges Card 2":
            lambda state: can_hit_floating(state,player),
        #"Switches and Bridges Card 3":
        #    lambda state: state.has("Power Glove", player) or state.has("Power Bombs", player),
            #lambda state: can_lower_bridge(state, player),

        "Pump It Up Card 1":
            lambda state: can_lower_bridge(state, player),
        "Pump It Up Card 3":
            lambda state: can_lower_bridge(state, player),

        "Hot On The Trail Card 2":
            lambda state: state.has("Power Glove", player),

        "Beyond the Clouds Card 1":
            lambda state: can_build_bridge(state, player),
        "Beyond the Clouds Card 2":
            lambda state: can_build_bridge(state, player),
        "Beyond the Clouds Card 3":
            lambda state: can_move_bombs(state, player) and state.has("Remote Bombs", player),
        


        # Kill count logic
        "Untouchable Treasure Card Kills":
            lambda state: can_move_bombs(state,player),
        "To Have or Have Not Card Kills":
            lambda state: can_move_bombs(state,player),
        "Switches and Bridges Card Kills":
            lambda state: can_move_bombs(state,player), #and state.has("Power Glove", player) or state.has("Power Bombs", player), #can_lower_bridge(state,player),
        "Pump It Up Card Kills":
            lambda state: can_move_bombs(state,player) and can_lower_bridge(state,player),
        "Hot On The Trail Card Kills":
            lambda state: can_move_bombs(state,player),
        "On the Right Track Card Kills":
            lambda state: can_move_bombs(state,player),
        "Blizzard Peaks Card Kills":
            lambda state: can_move_bombs(state,player),
        "Shiny Slippery Icy Floor Card Kills":
            lambda state: can_move_bombs(state,player),
        "Go For Broke Card Kills":
            lambda state: can_move_bombs(state,player),
        "Trap Tower Card Kills":
            lambda state: can_move_bombs(state,player),
        "Beyond the Clouds Card Kills":
            lambda state: can_move_bombs(state,player),
        "Doom Castle Card Kills":
            lambda state: can_move_bombs(state,player),

        # Bomber Boss Logic
        "Friend or Foe Card 4":
            lambda state: state.has("Power Glove", player),
        "Friend or Foe Card 5":
            lambda state: state.has("Power Glove", player),
        "Vs Artemis Card 3":
            lambda state: state.has("Power Glove", player),
        "Vs Artemis Card 4":
            lambda state: state.has("Power Glove", player),
        "Vs Artemis Card 5":
            lambda state: state.has("Power Glove", player),
        "Vs Orion Card 4":
            lambda state: state.has("Power Glove", player),
        "Vs Orion Card 5":
            lambda state: state.has("Power Glove", player),
        "Vs Regulus Card 2":
            lambda state: can_move_bombs(state, player),
        "Vs Regulus Card 3":
            lambda state: state.has("Power Glove", player),
        "Vs Regulus Card 4":
            lambda state: state.has("Power Glove", player) and state.has("Bomb Kick", player),
        "Vs Regulus Card 5":
            lambda state: state.has("Power Glove", player) and state.has("Bomb Kick", player),

        # Power Bomb and Remote bomb
        "Untouchable Treasure Power Bomb":
            lambda state: can_build_bridge(state,player) and state.has("Bombup", player, 5),
        "To Have or Have Not Power Bomb":
            lambda state: can_lower_bridge(state, player),
        "To Have or Have Not Remote Bomb Tower":
            lambda state: can_lower_bridge(state, player),
        "To Have or Have Not Remote Bomb Ledge":
            lambda state: state.has("Power Glove", player) and state.has("Bomb Kick", player),
        #"Switches and Bridges Power Bomb":
        #    lambda state: can_lower_bridge(state, player),
        #"Switches and Bridges Remote Bomb":
        #    lambda state: can_lower_bridge(state, player),
        "Trap Tower Power Bomb Secret Platform":
            lambda state: can_build_bridge(state,player),
        "Trap Tower Power Bomb Entrance":
            lambda state: can_build_bridge(state,player),
        "Beyond the Clouds Remote Bomb Main Room":
            lambda state: can_build_bridge(state,player) and state.has("Bombup", player, 2),
        "Doom Castle Power Bomb":
            lambda state: can_move_bombs(state,player),

        # Custom Balls
        "Untouchable Treasure Custom Red":
            lambda state: can_build_bridge(state, player) and state.has("Bombup", player, 5),
        "Doom Castle Custom Red":
            lambda state: can_build_bridge(state, player),
        "To Have or Have Not Custom Yellow":
            lambda state: can_lower_bridge(state, player),
        "To Have or Have Not Custom Blue":
            lambda state: can_build_bridge(state, player) and state.has("Bomb Kick",player) and state.has("Bombup", player, 2),
        "Pump It Up Custom Blue":
            lambda state: can_lower_bridge(state, player),
        "Beyond the Clouds Custom Blue":
            lambda state: can_build_bridge(state, player) and state.has("Bomb Kick",player) and state.has("Bombup", player, 2),
        "Pump It Up Custom Yellow":
            lambda state: can_lower_bridge(state, player),
        "Hot On The Trail Custom Red":
            lambda state: state.has("Power Bombs", player),
        "On the Right Track Custom Yellow":
            lambda state: state.has("Power Bombs", player),
        "Trap Tower Custom Blue":
            lambda state: can_build_bridge(state, player),
        "Trap Tower Custom Yellow":
            lambda state: can_build_bridge(state, player),
        "Trap Tower Custom Red":
            lambda state: can_build_bridge(state, player),
        "Beyond the Clouds Custom Blue":
            lambda state: can_build_bridge(state, player) and state.has("Bombup", player, 3),
    }

def get_normalmode_rules(player):
    return {
        "Hot On The Trail Card 3":
            lambda state: state.has("Power Bombs", player),
        "On the Right Track Card 2": #Power Glove?
            lambda state: state.has("Remote Bombs", player) and state.has("Power Glove", player),
        "Pump It Up Power Bomb":
            lambda state: can_lower_bridge(state, player),
        # Custom Balls
        "Untouchable Treasure Custom Green":
            lambda state: state.has("Power Bombs", player),
        "Switches and Bridges Custom Red":
            lambda state: can_build_bridge(state, player),
        "Hot On The Trail Custom Green":
            lambda state: state.has("Power Glove", player),
        "Blizzard Peaks Custom Blue":
            lambda state: can_lower_bridge(state, player),
        "Blizzard Peaks Custom Red":
            lambda state: can_build_bridge(state, player),
        "Doom Castle Custom Yellow":
            lambda state: can_build_bridge(state, player),
    }

def get_hardmode_rules(player):
    return {
        "Hot On The Trail Card 3":
            lambda state: state.has("Power Bombs", player) and (state.has("Power Glove", player) or state.has("Remote Bombs",player)),
        "To Have or Have Not Card 2":
            lambda state: state.has("Bomb Kick", player),
        "Blizzard Peaks Card 1":
            lambda state: state.has("Power Glove", player) or state.has("Power Bombs", player),
        "Blizzard Peaks Card 3":
            lambda state: can_build_bridge(state,player) and state.has("Bombup", player, 2),
        "Doom Castle Card 3":
            lambda state: can_build_bridge(state, player),

        # remote and Power exceptions
        "Untouchable Treasure Remote Bomb":
            lambda state: can_move_bombs(state,player) or (state.has("Remote Bombs", player) and state.has("Bombup",player, 1)),
        "Doom Castle Remote Bomb":
            lambda state: state.has("Power Glove", player),
        # Custom Balls
        "Untouchable Treasure Custom Green":
            lambda state: can_build_bridge(state,player) and state.has("Bombup", player, 5),
        "Switches and Bridges Custom Red":
            lambda state: can_hit_floating(state,player),
        "Hot On The Trail Custom Green":
            lambda state: state.has("Power Bombs", player),
        "On the Right Track Custom Blue":
            lambda state: can_hit_floating(state,player),
    }