from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import items

if TYPE_CHECKING:
    from .world import TVRUHHWorld




class TVRUHHLocation(Location):
    game = "TVRUHH"

def get_location_names_with_ids(location_names: list[str], chosen_list) -> dict[str, int | None]:
    return {location_name: chosen_list[location_name] for location_name in location_names}

def create_all_locations(world: TVRUHHWorld) -> None:
    create_regular_locations(world)
    create_events(world)



big_bad_list_of_all_locations_with_IDs = {

}



def create_regular_locations(world: TVRUHHWorld) -> None:
    #get regions
    start_dreams = world.get_region("Start")
    quickplay_dreams = world.get_region("Unlocked Quickplay")
    
    #locations in start region
    start_dreams.add_locations(load_all_lists(world,"starting_dreams"),TVRUHHLocation)
    quickplay_dreams.add_locations(load_all_lists(world,"quickplay_start"),TVRUHHLocation)


def load_all_lists(world: TVRUHHWorld, chosenlist: str = "") -> dict[str, int | None]:
    x = {}
    print("TVRUHH: Loading list",chosenlist)
    if chosenlist == "":
        x.update(load_remaining_locations(dream_list,world))
        if world.options.grindy_dreams:
            x.update(load_remaining_locations(grindy_dream_list,world))
        if world.options.extremely_grindy_dreams:
            x.update(load_remaining_locations(extremely_grindy_dream_list,world))
        if world.options.tedious_dreams:
            x.update(load_remaining_locations(tedious_dream_list,world))
        if world.options.extremely_tedious_dreams:
            x.update(load_remaining_locations(extremely_tedious_dream_list,world))
    else:
        x.update(load_location_list(dream_list,chosenlist,world))
        if world.options.grindy_dreams:
            x.update(load_location_list(grindy_dream_list,chosenlist,world))
        if world.options.extremely_grindy_dreams:
            x.update(load_location_list(extremely_grindy_dream_list,chosenlist,world))
        if world.options.tedious_dreams:
            x.update(load_location_list(tedious_dream_list,chosenlist,world))
        if world.options.extremely_tedious_dreams:
            x.update(load_location_list(extremely_tedious_dream_list,chosenlist,world))
    
    return x




def load_location_list(parentlist: dict,childlist: str,world,min_id = -1, max_id = -1) -> dict[str, int | None]:
    names = []
    for x in parentlist[childlist]:
        if not min_id == -1:
            if parentlist[childlist][x] >= min_id and parentlist[childlist][x] <= max_id:
                if world.options.disabled_dreams.__contains__(x.replace("Dream: ","")):
                    print("TVRUHH:", x, "was disabled, is not added as location.")
                else:
                    print("TVRUHH:", x, "not disabled, adding as location...")
                    names.append(x)
                    big_bad_list_of_all_locations_with_IDs.update({x: parentlist[childlist][x]})
        else:
            if world.options.disabled_dreams.__contains__(x.replace("Dream: ","")):
                print("TVRUHH:", x, "was disabled, is not added as location.")
            else:
                print("TVRUHH:", x, "not disabled, adding as location...")
                names.append(x)
                big_bad_list_of_all_locations_with_IDs.update({x: parentlist[childlist][x]})
    locations = get_location_names_with_ids(names,parentlist[childlist])
    print(names)
    print(big_bad_list_of_all_locations_with_IDs)
    return locations

def load_remaining_locations(whichlist: dict,world: TVRUHHWorld,min_id = -1, max_id = -1) -> dict[str, int | None]:
    names = []
    for x in whichlist:
        if not whichlist[x] is dict:
            if not min_id == -1:
                if whichlist[x] >= min_id and whichlist[x] <= max_id:
                    if not world.options.disabled_dreams.__contains__(x.replace("Dream: ","")):
                        print("TVRUHH:", x, "not disabled, adding as location...")
                        names.append(x)
                        big_bad_list_of_all_locations_with_IDs.update({x: whichlist[x]})
            else:
                if not world.options.disabled_dreams.__contains__(x.replace("Dream: ","")):
                    print("TVRUHH:", x, "not disabled, adding as location...")
                    names.append(x)
                    big_bad_list_of_all_locations_with_IDs.update({x: whichlist[x]})
    locations = get_location_names_with_ids(names,whichlist)
    return locations

def create_events(world: TVRUHHWorld) -> None:
    pass





# First three numbers indicate what type location it is
# Last four numbers is the count
# 100 = dreams (status: currently being worked on)
# 101 = grindy dreams (status: currently being worked on)
# 102 = extremely grindy dreams (status: currently being worked on)
# 103 = tedious dreams (status: currently being worked on)
# 104 = extremely tedious dreams (status: currently being worked on)
# 105 = story medals (status: WIP)
# 106 = quickplay copper medals (status: WIP)
# 107 = quickplay bronze medals (status: WIP)
# 108 = quickplay silver medals (status: WIP)
# 109 = quickplay gold medals (status: WIP)
# 110 = quickplay radiant medals (status: WIP)
# 111 = uqp radiant 1 (status: WIP)
# 112 = uqp radiant 2 (status: WIP)
# 113 = uqp radiant 3 (status: WIP)
# 114 = altstory copper medals (status: WIP)
# 115 = altstory bronze medals (status: WIP)
# 116 = altstory silver medals (status: WIP)
# 117 = altstory gold medals (status: WIP)
# 118 = altstory radiant medals (status: WIP)
# 119 = altstory rose medals (status: WIP)
# 120 = altstory crimson medals (status: WIP)
# 121 = towers copper medals (status: WIP)
# 122 = towers bronze medals (status: WIP)
# 123 = towers silver medals (status: WIP)
# 124 = towers gold medals (status: WIP)
# 125 = towers radiant medals (status: WIP)
# 126 = endless stress copper medals (status: WIP)
# 127 = endless stress bronze medals (status: WIP)
# 128 = endless stress silver medals (status: WIP)
# 129 = endless stress gold medals (status: WIP)
# 130 = endless stress radiant medals (status: WIP)
# 131 = endless terror copper medals (status: WIP)
# 132 = endless terror bronze medals (status: WIP)
# 133 = endless terror silver medals (status: WIP)
# 134 = endless terror gold medals (status: WIP)
# 135 = endless terror radiant medals (status: WIP)
# 136 = sublime medals uqp (status: WIP)
# 137 = sublime medals alt story (status: WIP)
# 138 = sublime medals towers (status: WIP)
# 139 = sublime medals endless (status: WIP)
# 140 = qp upgrades (status: WIP)
# 141 = altstory upgrades (status: WIP)
# 142 = endless upgrades (status: WIP)
# 143 = event upgrades (status: WIP)

# every list is ordered in sublists that corrospont to the regions
# many regions do not exist in some lists, because they are just tied to a specific gamemode (or something else)
# anything that is not contained in a sublist will have location-based rules in rules.py

dream_list = {
    "starting_dreams": {
        # Lovely Dreams
        "Dream: Love at First Shot": 1000000,
        "Dream: Monster Admirer": 1000001,
        "Dream: Monster Hugger": 1000002,
        "Dream: Let Me Love You!": 1000003,
        "Dream: Ten Thousand Shots in the Air": 1000004,
        "Dream: Clearing Out the Fear": 1000005,
        "Dream: Shambled Paradox": 1000006,
        "Dream: Her Adamant Will": 1000007,
        "Dream: Mutual Exclusion": 1000008,
        "Dream: Defense Mechanism": 1000009,
        "Dream: My Heart Is See Through": 1000010,
        "Dream: The Void Rains Down Upon You": 1000011,
        "Dream: Fever Dream": 1000012,
        # Lovely Feats
        "Dream: Gathering Hearts": 1000013,
        "Dream: Making Friends": 1000014,
        "Dream: Full Combo!": 1000015,
        "Dream: Affection Sevenfold": 1000016,
        "Dream: Expert Level Affection": 1000017,
        "Dream: Good Score": 1000018,
        "Dream: Great Score": 1000019,
        "Dream: BFF": 1000020,
        "Dream: Panic Attack!": 1000021,
        "Dream: No Need to Panic": 1000022,
        "Dream: Tsundere": 1000023,
        # Tetrid Totals
        "Dream: Tetrahedron of Shame": 1000024,
        "Dream: Tetrahedron of Frustration": 1000025,
        "Dream: Tetrahedron of Denial": 1000026,
        "Dream: Tetrahedron of Anxienty": 1000027,
        "Dream: Tetrahedron of Insecurity": 1000028,
        "Dream: Tetrahedron of Loneliness": 1000029,
        "Dream: Tetrehedron of Power": 1000030,
        "Dream: Collection of Triangles": 1000031,
        "Dream: 200 Tetrahedrons!": 1000032,
        "Dream: 400 Tetrahedrons!": 1000033,
        "Dream: 600 Tetrahedrons!": 1000034,
        # Collection Ambitions
        "Dream: Shiny Monster Cards": 1000035,
        "Dream: Glowing Starter Pack": 1000036,
        "Dream: Lovely Deck of Monsters": 1000037,
        "Dream: Rare Monster Cards": 1000038,
        "Dream: A Handful of Shiny Gifts": 1000039,
        "Dream: A Pile of Sparkling Gifts": 1000040,
        "Dream: A Rare Holographic Card!": 1000041,
        "Dream: Sparkling Bonus Pack": 1000042,
        "Dream: Shimmering Quick Gifts": 1000043,
        # Heart Trails
        "Dream: Her Heart: Karma Collector": 1000044,
        "Dream: Her Heart: Light Gifts": 1000045
    },
    "post_50_monsters": {
        
    },
    "quickplay_start": {
        
    }

}

grindy_dream_list = {
    "starting_dreams": {
        
    },
    "quickplay_start": {
        
    }
}

extremely_grindy_dream_list = {
    "starting_dreams": {

    },
    "quickplay_start": {
        
    }
}

tedious_dream_list = {
    "starting_dreams": {

    },
    "quickplay_start": {
        
    }
}

extremely_tedious_dream_list = {
    "starting_dreams": {
        
    },
    "quickplay_start": {
        
    }
}