from typing import Dict, List

# groups for ladders at the same elevation, for use in determing whether you can ls to entrances in diff rulesets
overworld_ladder_groups: Dict[str, List[str]] = {
    # lowest elevation, in-line with swamp lower, rotating lights, atoll lower, west garden lower
    "Group 1": ["Ladders in Overworld Town", "Ladder to Ruined Atoll", "Ladder to Swamp"],
    # in-line with furnace from beach, swamp upper entrance
    "Group 2": ["Ladders near Weathervane", "Ladders in Overworld Town", "Ladder to Swamp"],
    # in-line with west garden upper, ruined passage
    "Group 3": ["Ladders near Weathervane", "Ladders to West Bell"],
    # in-line with old house door, chest above ruined passage
    "Group 4": ["Ladders near Weathervane", "Ladder to Quarry", "Ladders to West Bell", "Ladders in Overworld Town"],
    # skip top of top ladder next to weathervane level, does not provide logical access to anything
    # in-line with quarry
    "Group 5": ["Ladders near Dark Tomb", "Ladder to Quarry", "Ladders to West Bell", "Ladders in Overworld Town",
                "Ladders in Well"],
    # in-line with patrol cave, east forest, fortress, and stairs towards special shop
    "Group 6": ["Ladders near Overworld Checkpoint", "Ladders near Patrol Cave"],
    # skip top of belltower and middle of dark tomb ladders, does not grant access to anything
    # in-line with temple rafters entrance, can get you to patrol cave ladders via knocking out of ls
    "Group 7": ["Ladders near Patrol Cave", "Ladder near Temple Rafters"],
    # in-line with the chest above dark tomb, gets you up the mountain stairs
    "Group 8": ["Ladders near Patrol Cave", "Ladder near Temple Rafters", "Ladders near Dark Tomb"],
}


# ladders accessible within different regions of overworld, only those that are relevant
# other scenes will just have them hardcoded since this type of structure is not necessary there
region_ladders: Dict[str, List[str]] = {
    "Overworld": ["Ladders near Weathervane", "Ladders near Overworld Checkpoint", "Ladders near Dark Tomb",
                  "Ladders in Overworld Town", "Ladder to Swamp", "Ladders in Well"],
    "Overworld Beach": ["Ladder to Ruined Atoll"],
    "Overworld at Patrol Cave": ["Ladders near Patrol Cave"],
    "Overworld Quarry Entry": ["Ladder to Quarry"],
    "Overworld Belltower": ["Ladders to West Bell"],
}