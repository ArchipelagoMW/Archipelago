from __future__ import annotations

from typing import TYPE_CHECKING

from . import logic_handling

if TYPE_CHECKING:
    from .world import TVRUHHWorld




def get_location_names_with_ids(location_names: list[str], chosen_list) -> dict[str, int | None]:
    return {location_name: chosen_list[location_name][0] for location_name in location_names}

def create_all_locations(world: TVRUHHWorld) -> None:
    create_regular_locations(world)
    create_events(world)
    # world.location_name_to_id.update(big_bad_list_of_all_locations_with_IDs)




big_bad_list_of_all_locations_with_IDs = {
    "Dream: Love at First Shot": 1000000
}

locations_to_tags = {

}

extra_location_list = {

}

def create_regular_locations(world: TVRUHHWorld) -> None:
    #get regions
    start_dreams = world.get_region("Start")
    quickplay_dreams = world.get_region("Unlocked Quickplay")
    
    #locations in start region
    logic_handling.logic_placer(world,load_location_list(world,dream_list),"dreams")
    logic_handling.logic_placer(world,load_location_list(world,qp_copper),"qp_medal")


def create_extra_locations(world: TVRUHHWorld, amount: int) -> None:
    bonus_locations = world.get_region("Start")
    bonus_locations.add_locations(get_location_names_with_ids(load_extra_locations(amount),extra_location_list))

def load_location_list(world,parentlist: dict,min_id = -1, max_id = -1) -> dict[str, int | None]:
    names = []
    for x in parentlist:
        if not min_id == -1:
            if parentlist[x][0] >= min_id and parentlist[x][0] <= max_id:
                if not world.options.disabled_dreams.__contains__(x.replace("Dream: ","")):
                    names.append(x)
        else:
            if not world.options.disabled_dreams.__contains__(x.replace("Dream: ","")):
                names.append(x)
    names = logic_handling.logic_remover(world, names)
    locations = get_location_names_with_ids(names,parentlist)
    return locations

def load_extra_locations(amount: int) -> dict[str, int | None]:
    a: int = 1
    l = []
    while a <= amount: 
        x = "Bonus Gift " + ((a).__str__())
        l.append(x)
        a += 1
    return l

def create_events(world: TVRUHHWorld) -> None:
    pass

def requestbbl() -> dict[str:int]: 
    # normal locations
    updatebbl(dream_list)
    updatebbl(qp_copper)
    
    # bonus locations
    a: int = 1
    while a <= 1000: 
        x = "Bonus Gift " + ((a).__str__())
        big_bad_list_of_all_locations_with_IDs.update({str(x): int(1450000 + (a-1))})
        extra_location_list.update({str(x): [int(1450000 + (a-1))]})
        a += 1
    
    return big_bad_list_of_all_locations_with_IDs

def updatebbl(whichlist) -> None:
    for x in whichlist:
        big_bad_list_of_all_locations_with_IDs.update({x: whichlist[x][0]})
        locations_to_tags.update({x: whichlist[x][1]})




# First three numbers indicate what type location it is
# Last four numbers is the count
# 100 = dreams (status: currently being worked on)
# 101 = story medals (status: WIP)
# 102 = quickplay copper medals (status: WIP)
# 103 = quickplay bronze medals (status: WIP)
# 104 = quickplay silver medals (status: WIP)
# 105 = quickplay gold medals (status: WIP)
# 106 = quickplay radiant medals (status: WIP)
# 107 = uqp radiant 1 (status: WIP)
# 108 = uqp radiant 2 (status: WIP)
# 109 = uqp radiant 3 (status: WIP)
# 110 = altstory copper medals (status: WIP)
# 111 = altstory bronze medals (status: WIP)
# 112 = altstory silver medals (status: WIP)
# 113 = altstory gold medals (status: WIP)
# 114 = altstory radiant medals (status: WIP)
# 115 = altstory rose medals (status: WIP)
# 116 = altstory crimson medals (status: WIP)
# 117 = towers copper medals (status: WIP)
# 118 = towers bronze medals (status: WIP)
# 119 = towers silver medals (status: WIP)
# 120 = towers gold medals (status: WIP)
# 121 = towers radiant medals (status: WIP)
# 122 = endless stress copper medals (status: WIP)
# 123 = endless stress bronze medals (status: WIP)
# 124 = endless stress silver medals (status: WIP)
# 125 = endless stress gold medals (status: WIP)
# 126 = endless stress radiant medals (status: WIP)
# 127 = endless terror copper medals (status: WIP)
# 128 = endless terror bronze medals (status: WIP)
# 129 = endless terror silver medals (status: WIP)
# 130 = endless terror gold medals (status: WIP)
# 131 = endless terror radiant medals (status: WIP)
# 132 = sublime medals uqp (status: WIP)
# 133 = sublime medals alt story (status: WIP)
# 134 = sublime medals towers (status: WIP)
# 135 = sublime medals endless (status: WIP)
# 136 = qp upgrades (status: WIP)
# 137 = altstory upgrades (status: WIP)
# 138 = endless upgrades (status: WIP)
# 139 = event upgrades (status: WIP)
# 140 = other locations (status: unknown, has any misc. location)

# every list is ordered in sublists that corrospont to the regions
# many regions do not exist in some lists, because they are just tied to a specific gamemode (or something else)
# anything that is not contained in a sublist will have location-based rules in rules.py

dream_list = {
    "Dream: Love at First Shot" : [1000000, []],
    "Dream: Monster Admirer" : [1000001, []],
    "Dream: Monster Hugger" : [1000002, []],
    "Dream: Monster Lover" : [1000003, []],
    "Dream: Nightmarephile" : [1000004, ["grind"]],
    "Dream: Teramonstrophile" : [1000005, ["grind"]],
    "Dream: Weapon of Mass Affection" : [1000006, ["very_grind"]],
    "Dream: Lovepocalypse" : [1000007, ["very_grind"]],
    "Dream: Let Me Love You!" : [1000008, []],
    "Dream: Let Yourself Be Loved!" : [1000009, []],
    "Dream: Violence in the Name of Love!" : [1000010, ["grind"]],
    "Dream: To Shreds, You Say?" : [1000011, ["grind"]],
    "Dream: Love You to Pieces!" : [1000012, ["very_grind"]],
    "Dream: Monster Fear Genophiler" : [1000013, ["very_grind"]],
    #for testing:
    "Dream: Something Something Quick" : [1000069, ["quickplay"]]
}

story_medals = {

}

qp_copper = {
    "QP Copper: Scrambla" : [1020000, []]
}

qp_bronze = {

}

qp_silver = {

}

qp_gold = {

}

qp_radiant = {

}

uqp_rad1 = {

}

uqp_rad2 = {

}

uqp_rad3 = {

}

altstory_copper = {

}

altstory_bronze = {

}

altstory_silver = {

}

altstory_gold = {

}

altstory_radiant = {

}

altstory_rose = {

}

altstory_crimson = {

}

towers_copper = {

}

towers_bronze = {

}

towers_silver = {

}

towers_gold = {

}

towers_radiant = {

}

endl_str_copper = {

}

endl_str_bronze = {

}

endl_str_silver = {

}

endl_str_gold = {

}

endl_str_radiant = {

}

endl_ter_copper = {

}

endl_ter_bronze = {

}

endl_ter_silver = {

}

endl_ter_gold = {

}

endl_ter_radiant = {

}

sublime_uqp = {

}

sublime_altstory = {

}

sublime_tower = {

}

sublime_endless = {

}

qp_upgrades = {

}

altstory_upgr = {

}

endless_upgr = {

}

event_upgrades = {

}

other_locations_list = {
    "Bonus Gift" : [1400000,[]] 
    # unique: 1000 bonus gifts are always loaded in the BBL whereas the needed amount of locations gets added to the regions later. 
    #DO NOT GIVE A LOCATION AN ID OF 1450000 THROUGH 1451000 AS THAT IS WHERE THEY ARE IN TERMS OF ID!!
}