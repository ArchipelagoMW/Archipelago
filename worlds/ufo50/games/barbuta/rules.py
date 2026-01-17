from typing import TYPE_CHECKING, Dict
from BaseClasses import Region, CollectionState
from worlds.generic.Rules import set_rule

if TYPE_CHECKING:
    from ... import UFO50World


pin = "Barbuta - Pin"
umbrella = "Barbuta - Umbrella"
necklace = "Barbuta - Necklace"
candy = "Barbuta - Candy"
key = "Barbuta - Key"
blood_sword = "Barbuta - Blood Sword"
broken_wall = "Barbuta - A Broken Wall"
wand = "Barbuta - Wand"
bat_orb = "Barbuta - Bat Orb"
egg = "Barbuta - Egg"


# count the value of the money items
def has_money(amount: int, state: CollectionState, player: int) -> bool:
    current_money = state.count("Barbuta - $100", player) * 100
    if current_money >= amount:
        return True
    current_money += state.count("Barbuta - $50", player) * 50
    if current_money >= amount:
        return True
    return False


def create_rules(world: "UFO50World", regions: Dict[str, Region]) -> None:
    player = world.player

    def has_wand(state: CollectionState) -> bool:
        return state.has(wand, player) and state.can_reach(regions["Wand Trade Room"])

    regions["Menu"].connect(regions["Starting Area"])

    regions["Starting Area"].connect(regions["Key Room"])
    regions["Starting Area"].connect(regions["Platforms above R4C4"],
                                     rule=lambda state: state.has(necklace, player))
    regions["Starting Area"].connect(regions["Blood Sword Room"])
    # pin via G2, umbrella via H3
    regions["Starting Area"].connect(regions["R7C3 and Nearby"],
                                     rule=lambda state: state.has_any((pin, umbrella), player))
    regions["Starting Area"].connect(regions["R6C7 and Nearby"],
                                     rule=lambda state: state.has(pin, player))
    regions["Starting Area"].connect(regions["Mimic Room"],
                                     rule=lambda state: has_wand(state))
    regions["Starting Area"].connect(regions["R3C7 above Ladders"],
                                     rule=lambda state: state.has(candy, player))

    regions["Platforms above R4C4"].connect(regions["Bat Altar"])  # drop down off the left side
    regions["Platforms above R4C4"].connect(regions["Above Entrance"])  # drop down off right side, need to break blocks
    regions["Platforms above R4C4"].connect(regions["Boss Area"],
                                            rule=lambda state: state.has(key, player))

    regions["Above Entrance"].connect(regions["Wand Trade Room"])  # walk through the fake wall after using the door

    regions["R7C7 and Nearby"].connect(regions["Wand Trade Room"],
                                       rule=lambda state: state.has(pin, player))

    regions["Wand Trade Room"].connect(regions["R7C7 and Nearby"],
                                       rule=lambda state: state.has(pin, player))

    regions["R3C7 above Ladders"].connect(regions["Boss Area"],
                                          rule=lambda state: state.has(broken_wall, player))

    regions["Mimic Room"].connect(regions["Boss Area"])

    set_rule(world.get_location("Barbuta - Chest - R7C2"),
             rule=lambda state: state.has(pin, player))
    set_rule(world.get_location("Barbuta - Egg Shop - R2C6"),
             rule=lambda state: has_money(100, state, player))
    set_rule(world.get_location("Barbuta - Upper Shop Candy - R3C1"),
             rule=lambda state: has_money(100, state, player))
    set_rule(world.get_location("Barbuta - Upper Shop Umbrella - R3C1"),
             rule=lambda state: has_money(50, state, player))
    set_rule(world.get_location("Barbuta - Lower Shop Umbrella - R6C2"),
             rule=lambda state: has_money(100, state, player))
    set_rule(world.get_location("Barbuta - Lower Shop Trash - R6C2"),
             rule=lambda state: has_money(50, state, player))
    set_rule(world.get_location("Barbuta - Lower Shop Pin - R6C2"),
             rule=lambda state: has_money(200, state, player))
    set_rule(world.get_location("Barbuta - Little Guy Breaks a Wall - R4C7"),
             rule=lambda state: has_money(500, state, player))

    # garden is sphere 1
    set_rule(world.get_location("Barbuta - Gold"),
             rule=lambda state: state.has_any((blood_sword, bat_orb), player) or has_wand(state))
    if "Barbuta" in world.options.cherry_allowed_games:
        set_rule(world.get_location("Barbuta - Cherry"),
                 rule=lambda state: state.has(bat_orb, player)
                 and state.has(egg, player, 2)
                 and (state.has(blood_sword, player) or has_wand(state)))
