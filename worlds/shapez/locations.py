from BaseClasses import Location, LocationProgressType, Region

location_description = {  # TODO
    "Level 1": "TODO",
    "Level 1 Additional": "TODO",
    "Level 20 Additional": "TODO",
    "Routing Upgrade Tier II": "TODO",
    "Extracting Upgrade Tier II": "TODO",
    "Shape Processing Upgrade Tier II": "TODO",
    "Color Processing Upgrade Tier II": "TODO",
    "Painter": "TODO",
    "Cutter": "TODO",
    "Rotater": "TODO",
    "Wait, they stack?": "TODO",
    "Wires": "TODO",
    "Storage": "TODO",
    "Freedom": "TODO",
    "The logo!": "TODO",
    "To the moon": "TODO",
    "It's piling up": "TODO",
    "I'll use it later": "TODO",
    "Efficiency 1": "TODO",
    "Preparing to launch": "TODO",
    "SpaceY": "TODO",
    "Stack overflow": "TODO",
    "It's a mess": "TODO",
    "Faster": "TODO",
    "Even faster": "TODO",
    "Get rid of them": "TODO",
    "It's been a long time": "TODO",
    "Addicted": "TODO",
    "Can't stop": "TODO",
    "Is this the end?": "TODO",
    "Getting into it": "TODO",
    "Now it's easy": "TODO",
    "Computer Guy": "TODO",
    "Speedrun Master": "TODO",
    "Speedrun Novice": "TODO",
    "Not an idle game": "TODO",
    "Efficiency 2": "TODO",
    "Branding specialist 1": "TODO",
    "Branding specialist 2": "TODO",
    "King of Inefficiency": "TODO",
    "It's so slow": "TODO",
    "MAM (Make Anything Machine)": "TODO",
    "Perfectionist": "TODO",
    "The next dimension": "TODO",
    "Oops": "TODO",
    "Copy-Pasta": "TODO",
    "I've seen that before ...": "TODO",
    "Memories from the past": "TODO",
    "I need trains": "TODO",
    "A bit early?": "TODO",
    "GPS": "TODO"
}

translate: list[tuple[int, str]] = [
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I")
]


def roman(num: int) -> str:
    rom: str = ""
    for key, val in translate:
        while num >= key:
            rom += val
            num -= key
    return rom


all_locations: list[str] = (["Level 1 Additional", "Level 20 Additional"]
                            + [f"Level {x}" for x in range(1, 1001)]
                            + [f"Routing Upgrade Tier {roman(x)}" for x in range(2, 1001)]
                            + [f"Extracting Upgrade Tier {roman(x)}" for x in range(2, 1001)]
                            + [f"Shape Processing Upgrade Tier {roman(x)}" for x in range(2, 1001)]
                            + [f"Color Processing Upgrade Tier {roman(x)}" for x in range(2, 1001)]
                            + ["Painter", "Cutter", "Rotater", "Wait, they stack?", "Wires", "Storage",
                               "Freedom", "The logo!", "To the moon", "It's piling up", "I'll use it later",
                               "Efficiency 1", "Preparing to launch", "SpaceY", "Stack overflow", "It's a mess",
                               "Faster", "Even faster", "Get rid of them", "It's been a long time", "Addicted",
                               "Can't stop", "Is this the end?", "Getting into it", "Now it's easy", "Computer Guy",
                               "Speedrun Master", "Speedrun Novice", "Not an idle game", "Efficiency 2",
                               "Branding specialist 1", "Branding specialist 2", "King of Inefficiency", "It's so slow",
                               "MAM (Make Anything Machine)", "Perfectionist", "The next dimension", "Oops",
                               "Copy-Pasta", "I've seen that before ...", "Memories from the past", "I need trains",
                               "A bit early?", "GPS", ])

# included_locations: dict[str, tuple[str, LocationProgressType]]
# """Name: (region name, LocationProgressType)"""


def addlevels(maxlevel: int, logictype: int) -> dict[str, tuple[str, LocationProgressType]]:
    """Returns a dictionary with all level locations based on given options (maxlevel INCLUDED).
    If shape requirements are not randomized, give logic type 0."""

    # Level 1 is always directly accessible
    locations: dict[str, tuple[str, LocationProgressType]] = {"Level 1": ("Main", LocationProgressType.PRIORITY),
                                                              "Level 1 Additional": (
                                                              "Main", LocationProgressType.PRIORITY)}

    if logictype == 0 or logictype == 1:
        locations["Level 20 Additional"] = ("Levels with 5 Buildings", LocationProgressType.DEFAULT)
        locations["Level 2"] = ("Levels with 1 Building", LocationProgressType.DEFAULT)
        locations["Level 3"] = ("Levels with 1 Building", LocationProgressType.DEFAULT)
        locations["Level 4"] = ("Levels with 1 Building", LocationProgressType.DEFAULT)
        locations["Level 5"] = ("Levels with 2 Buildings", LocationProgressType.DEFAULT)
        locations["Level 6"] = ("Levels with 2 Buildings", LocationProgressType.DEFAULT)
        locations["Level 7"] = ("Levels with 3 Buildings", LocationProgressType.DEFAULT)
        locations["Level 8"] = ("Levels with 3 Buildings", LocationProgressType.DEFAULT)
        locations["Level 9"] = ("Levels with 4 Buildings", LocationProgressType.DEFAULT)
        locations["Level 10"] = ("Levels with 4 Buildings", LocationProgressType.DEFAULT)
        for x in range(11, maxlevel+1):
            locations[f"Level {x}"] = ("Levels with 5 Buildings", LocationProgressType.DEFAULT)
    elif logictype == 2 or logictype == 3:
        phaselength = maxlevel//6
        l20phase = 20//phaselength
        if l20phase == 0:
            locations["Level 20 Additional"] = ("Main", LocationProgressType.DEFAULT)
        elif l20phase == 1:
            locations["Level 20 Additional"] = ("Levels with 1 Building", LocationProgressType.DEFAULT)
        else:
            locations["Level 20 Additional"] = (f"Levels with {min(l20phase, 5)} Buildings", LocationProgressType.DEFAULT)
        for x in range(2, phaselength):
            locations[f"Level {x}"] = ("Main", LocationProgressType.DEFAULT)
        for x in range(phaselength, phaselength*2):
            locations[f"Level {x}"] = ("Levels with 1 Building", LocationProgressType.DEFAULT)
        for x in range(phaselength*2, phaselength*3):
            locations[f"Level {x}"] = ("Levels with 2 Buildings", LocationProgressType.DEFAULT)
        for x in range(phaselength*3, phaselength*4):
            locations[f"Level {x}"] = ("Levels with 3 Buildings", LocationProgressType.DEFAULT)
        for x in range(phaselength*4, phaselength*5):
            locations[f"Level {x}"] = ("Levels with 4 Buildings", LocationProgressType.DEFAULT)
        for x in range(phaselength*5, maxlevel+1):
            locations[f"Level {x}"] = ("Levels with 5 Buildings", LocationProgressType.DEFAULT)
    else:  # logictype == 4
        locations["Level 20 Additional"] = ("Levels with 5 Buildings", LocationProgressType.DEFAULT)
        for x in range(2, maxlevel+1):
            locations[f"Level {x}"] = ("Levels with 5 Buildings", LocationProgressType.DEFAULT)

    return locations


def addupgrades(finaltier: int, logictype: int) -> dict[str, tuple[str, LocationProgressType]]:
    """Returns a dictionary with all upgrade locations based on given options (finaltier INCLUDED).
    If shape requirements are not randomized, give logic type 0."""

    locations: dict[str, tuple[str, LocationProgressType]] = {}
    categories = ["Routing", "Extracting", "Shape Processing", "Color Processing"]

    for cat in categories:
        locations[f"{cat} Upgrade Tier II"] = ("Upgrades Tier II", LocationProgressType.PRIORITY)

    if logictype == 0:
        locations["Routing Upgrade Tier III"] = ("Upgrades with 2 Buildings", LocationProgressType.PRIORITY)
        locations["Extracting Upgrade Tier III"] = ("Upgrades with 2 Buildings", LocationProgressType.PRIORITY)
        locations["Shape Processing Upgrade Tier III"] = ("Upgrades with 1 Building", LocationProgressType.PRIORITY)
        locations["Color Processing Upgrade Tier III"] = ("Upgrades with 3 Buildings", LocationProgressType.PRIORITY)
        for x in range(4, finaltier+1):
            for cat in categories:
                locations[f"{cat} Upgrade Tier {roman(x)}"] = ("Upgrades with 5 Buildings", LocationProgressType.DEFAULT)
    elif logictype == 1:
        for cat in categories:
            locations[f"{cat} Upgrade Tier III"] = ("Upgrades with 1 Building", LocationProgressType.PRIORITY)
        for x in range(4, 7):
            for cat in categories:
                locations[f"{cat} Upgrade Tier {roman(x)}"] = (f"Upgrades with {x-2} Buildings", LocationProgressType.DEFAULT)
        for x in range(7, finaltier+1):
            for cat in categories:
                locations[f"{cat} Upgrade Tier {roman(x)}"] = ("Upgrades with 5 Buildings", LocationProgressType.DEFAULT)
    else: # logictype == 2
        for cat in categories:
            locations[f"{cat} Upgrade Tier III"] = ("Upgrades with 5 Buildings", LocationProgressType.PRIORITY)
        for x in range(4, finaltier+1):
            for cat in categories:
                locations[f"{cat} Upgrade Tier {roman(x)}"] = ("Upgrades with 5 Buildings", LocationProgressType.DEFAULT)

    return locations


def addachievements(include: bool, excludesoftlock: bool, excludelong: bool, excludeprogressive: bool,
                    maxlevel: int, levellogictype: int, finaltier: int, upgradelogictype: int,
                    goal: int) -> dict[str, tuple[str, LocationProgressType]]:
    """Returns a dictionary with all achievement locations based on given options."""

    locations: dict[str, tuple[str, LocationProgressType]] = {}
    phaselength = maxlevel//6
    l12phase = 12//phaselength
    l14phase = 14//phaselength
    l20phase = 20//phaselength
    l26phase = 26//phaselength
    l27phase = 27//phaselength
    l50phase = 50//phaselength
    l100phase = 100//phaselength

    if not include:
        return locations

    locations["Painter"] = ("Painted Shape Achievements", LocationProgressType.DEFAULT)
    locations["Cutter"] = ("Cut Shape Achievements", LocationProgressType.DEFAULT)
    locations["Rotater"] = ("Rotated Shape Achievements", LocationProgressType.DEFAULT)
    locations["Wait, they stack?"] = ("Stacked Shape Achievements", LocationProgressType.DEFAULT)
    if levellogictype in [0, 1, 4]:
        locations["Wires"] = ("Levels with 5 Buildings", LocationProgressType.DEFAULT)
    else:
        if l20phase == 0:
            locations["Wires"] = ("Main", LocationProgressType.DEFAULT)
        elif l20phase == 1:
            locations["Wires"] = ("Levels with 1 Building", LocationProgressType.DEFAULT)
        else:
            locations["Wires"] = (f"Levels with {min(l20phase, 5)} Buildings", LocationProgressType.DEFAULT)
    locations["Storage"] = ("Stored Shape Achievements", LocationProgressType.DEFAULT)
    if goal: # not goal == 0
        if levellogictype in [0, 1, 4]:
            locations["Freedom"] = ("Levels with 5 Buildings", LocationProgressType.DEFAULT)
        else:
            if l26phase == 0:
                locations["Freedom"] = ("Main", LocationProgressType.DEFAULT)
            elif l26phase == 1:
                locations["Freedom"] = ("Levels with 1 Building", LocationProgressType.DEFAULT)
            else:
                locations["Freedom"] = (f"Levels with {min(l26phase, 5)} Buildings", LocationProgressType.DEFAULT)
    locations["The logo!"] = ("All Buildings Shapes", LocationProgressType.DEFAULT)
    locations["To the moon"] = ("All Buildings Shapes", LocationProgressType.DEFAULT)
    locations["It's piling up"] = ("All Buildings Shapes", LocationProgressType.DEFAULT)
    locations["I'll use it later"] = ("All Buildings Shapes", LocationProgressType.DEFAULT)
    locations["Efficiency 1"] = ("All Buildings Shapes", LocationProgressType.DEFAULT)
    locations["Preparing to launch"] = ("All Buildings Shapes", LocationProgressType.DEFAULT)
    locations["SpaceY"] = ("All Buildings Shapes", LocationProgressType.DEFAULT)
    locations["Stack overflow"] = ("Stacked Shape Achievements", LocationProgressType.DEFAULT)
    locations["It's a mess"] = ("Main", LocationProgressType.DEFAULT)
    if upgradelogictype == 1:
        locations["Faster"] = ("Upgrades with 3 Buildings", LocationProgressType.DEFAULT)
        if finaltier > 8:
            locations["Even faster"] = ("Upgrades with 5 Buildings", LocationProgressType.DEFAULT)
    else:
        locations["Faster"] = ("Upgrades with 5 Buildings", LocationProgressType.DEFAULT)
        if finaltier > 8:
            locations["Even faster"] = ("Upgrades with 5 Buildings", LocationProgressType.DEFAULT)
    locations["Get rid of them"] = ("Trashed Shape Achievements", LocationProgressType.DEFAULT)
    if goal > 1 or maxlevel > 50:
        if levellogictype in [0, 1, 4]:
            locations["Can't stop"] = ("Levels with 5 Buildings", LocationProgressType.DEFAULT)
        else:
            if l50phase == 0:
                locations["Can't stop"] = ("Main", LocationProgressType.DEFAULT)
            elif l50phase == 1:
                locations["Can't stop"] = ("Levels with 1 Building", LocationProgressType.DEFAULT)
            else:
                locations["Can't stop"] = (f"Levels with {min(l50phase, 5)} Buildings", LocationProgressType.DEFAULT)
    if goal > 1 or maxlevel > 100:
        if levellogictype in [0, 1, 4]:
            locations["Is this the end?"] = ("Levels with 5 Buildings", LocationProgressType.DEFAULT)
        else:
            if l100phase == 0:
                locations["Is this the end?"] = ("Main", LocationProgressType.DEFAULT)
            elif l100phase == 1:
                locations["Is this the end?"] = ("Levels with 1 Building", LocationProgressType.DEFAULT)
            else:
                locations["Is this the end?"] = (f"Levels with {min(l100phase, 5)} Buildings", LocationProgressType.DEFAULT)
    locations["Getting into it"] = ("Main", LocationProgressType.DEFAULT)
    locations["Now it's easy"] = ("All Buildings Shapes", LocationProgressType.DEFAULT)
    locations["Computer Guy"] = ("Wiring Achievements", LocationProgressType.DEFAULT)
    locations["Efficiency 2"] = ("All Buildings Shapes", LocationProgressType.DEFAULT)
    locations["Branding specialist 1"] = ("All Buildings Shapes", LocationProgressType.DEFAULT)
    locations["Branding specialist 2"] = ("All Buildings Shapes", LocationProgressType.DEFAULT)
    if goal: # not goal == 0
        if levellogictype in [0, 1, 4]:
            locations["MAM (Make Anything Machine)"] = ("Levels with 5 Buildings", LocationProgressType.DEFAULT)
        else:
            if l27phase == 0:
                locations["MAM (Make Anything Machine)"] = ("Main", LocationProgressType.DEFAULT)
            elif l27phase == 1:
                locations["MAM (Make Anything Machine)"] = ("Levels with 1 Building", LocationProgressType.DEFAULT)
            else:
                locations["MAM (Make Anything Machine)"] = (f"Levels with {min(l27phase, 5)} Buildings", LocationProgressType.DEFAULT)
    locations["Perfectionist"] = ("Main", LocationProgressType.DEFAULT)
    locations["The next dimension"] = ("Wiring Achievements", LocationProgressType.DEFAULT)
    locations["Oops"] = ("Main", LocationProgressType.DEFAULT)
    locations["Copy-Pasta"] = ("All Buildings Shapes", LocationProgressType.DEFAULT)
    locations["I've seen that before ..."] = ("All Buildings Shapes", LocationProgressType.DEFAULT)
    locations["Memories from the past"] = ("All Buildings Shapes", LocationProgressType.DEFAULT)
    locations["I need trains"] = ("Main", LocationProgressType.DEFAULT)
    locations["GPS"] = ("Main", LocationProgressType.DEFAULT)

    if excludeprogressive:
        unreasonable_type = LocationProgressType.EXCLUDED
    else:
        unreasonable_type = LocationProgressType.DEFAULT

    if not excludesoftlock:
        if levellogictype in [0, 1, 4]:
            locations["Speedrun Master"] = ("Levels with 5 Buildings", unreasonable_type)
            locations["Speedrun Novice"] = ("Levels with 5 Buildings", unreasonable_type)
            locations["Not an idle game"] = ("Levels with 5 Buildings", unreasonable_type)
            locations["It's so slow"] = ("Levels with 5 Buildings", unreasonable_type)
            locations["King of Inefficiency"] = ("Levels with 5 Buildings", unreasonable_type)
        else:
            if l12phase == 0:
                locations["Speedrun Master"] = ("Main", unreasonable_type)
                locations["Speedrun Novice"] = ("Main", unreasonable_type)
                locations["Not an idle game"] = ("Main", unreasonable_type)
                locations["It's so slow"] = ("Main", unreasonable_type)
            elif l12phase == 1:
                locations["Speedrun Master"] = ("Levels with 1 Building", unreasonable_type)
                locations["Speedrun Novice"] = ("Levels with 1 Building", unreasonable_type)
                locations["Not an idle game"] = ("Levels with 1 Building", unreasonable_type)
                locations["It's so slow"] = ("Levels with 1 Building", unreasonable_type)
            else:
                locations["Speedrun Master"] = (f"Levels with {min(l12phase, 5)} Buildings", unreasonable_type)
                locations["Speedrun Novice"] = (f"Levels with {min(l12phase, 5)} Buildings", unreasonable_type)
                locations["Not an idle game"] = (f"Levels with {min(l12phase, 5)} Buildings", unreasonable_type)
                locations["It's so slow"] = (f"Levels with {min(l12phase, 5)} Buildings", unreasonable_type)
            if l14phase == 0:
                locations["King of Inefficiency"] = ("Main", unreasonable_type)
            elif l14phase == 1:
                locations["King of Inefficiency"] = ("Levels with 1 Building", unreasonable_type)
            else:
                locations["King of Inefficiency"] = (f"Levels with {min(l14phase, 5)} Buildings", unreasonable_type)
        locations["A bit early?"] = ("All Buildings Shapes", unreasonable_type)

    if not excludelong:
        locations["It's been a long time"] = ("Main", unreasonable_type)
        locations["Addicted"] = ("Main", unreasonable_type)

    return locations


class ShapezLocation(Location):
    game = "Shapez"

    def __init__(self, player: int, name: str, address: int, region: Region, progress_type: LocationProgressType):
        super(ShapezLocation, self).__init__(player, name, address, region)
        self.progress_type = progress_type
