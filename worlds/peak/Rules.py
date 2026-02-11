from typing import TYPE_CHECKING

from BaseClasses import Location, Entrance

if TYPE_CHECKING:
    from . import PeakWorld

CALDERA_LOCATIONS = [
    "Acquire Big Egg", "Acquire Egg", "Acquire Cooked Bird", "Volcanology Badge", "Nomad Badge", "Alpinist Badge",
]

KILN_LOCATIONS = [
    "Acquire Strange Gem", "Peak Badge", "Speed Climber Badge", "Lone Wolf Badge", "Participation Badge",
    "Survivalist Badge", "Naturalist Badge", "Leave No Trace Badge", "Balloon Badge", "Bing Bong Badge",
    "Gourmand Badge", "High Altitude Badge", "Knot Tying Badge", "24 Karat Badge",
]

ROOTS_LOCATIONS = [
    "Acquire Red Shroomberry", "Acquire Blue Shroomberry", "Acquire Yellow Shroomberry",
    "Acquire Green Shroomberry", "Acquire Purple Shroomberry",
    "Acquire Mandrake", "Acquire Bounce Shroom", "Acquire Cloud Fungus", "Mycoacrobatics Badge",
    "Tread Lightly Badge", "Undead Encounter Badge",
    "Web Security Badge", "Advanced Mycology Badge",
]

TROPICS_LOCATIONS = [
    "Acquire Red Clusterberry", "Acquire Yellow Clusterberry", "Acquire Black Clusterberry",
    "Acquire Purple Kingberry", "Acquire Yellow Kingberry", "Acquire Green Kingberry",
    "Acquire Brown Berrynana", "Acquire Blue Berrynana", "Acquire Pink Berrynana",
    "Acquire Yellow Berrynana", "Acquire Yellow Berrynana Peel", "Acquire Pink Berrynana Peel",
    "Acquire Honeycomb", "Acquire Beehive", "Arborist Badge", "Foraging Badge",
    "Acquire Blue Berrynana Peel", "Acquire Magic Bean", "Acquire Tick", "Acquire Brown Berrynana Peel",
]

MESA_LOCATIONS = [
    "Acquire Cactus", "Acquire Aloe Vera", "Acquire Sunscreen", "Acquire Ancient Idol",
    "Acquire Red Prickleberry", "Acquire Gold Prickleberry", "Acquire Scorpion", "Acquire Torch",
    "Megaentomology Badge", "Cool Cucumber Badge", "Astronomy Badge",
    "Daredevil Badge", "Needlepoint Badge", "Acquire Parasol", "Acquire Dynamite", "Forestry Badge",
]

ALPINE_LOCATIONS = [
    "Acquire Orange Winterberry", "Acquire Napberry", "Bundled Up Badge", "Acquire Yellow Winterberry",
    "Animal Serenading Badge", "Acquire Heat Pack", "Trailblazer Badge",
]


def set_rule(spot: Location | Entrance, rule):
    spot.access_rule = rule


def add_rule(spot: Location | Entrance, rule, combine="and"):
    old_rule = spot.access_rule
    if old_rule is Location.access_rule:
        spot.access_rule = rule if combine == "and" else old_rule
    else:
        if combine == "and":
            spot.access_rule = lambda state: rule(state) and old_rule(state)
        else:
            spot.access_rule = lambda state: rule(state) or old_rule(state)


def apply_rules(world: "PeakWorld"):
    """Apply all access rules for Peak locations."""
    player = world.player
    required_ascent = world.options.ascent_count.value
    goal_type = world.options.goal.value
    progressive_stamina_enabled = world.options.progressive_stamina.value

    # Biome access rules
    try:
        set_rule(world.get_location("Roots Access"),
                 lambda state: state.has("Progressive Mountain", player, 1))
        set_rule(world.get_location("Tropics Access"),
                 lambda state: state.has("Progressive Mountain", player, 1))

        set_rule(world.get_location("Mesa Access"),
                 lambda state: state.has("Progressive Mountain", player, 2))
        set_rule(world.get_location("Alpine Access"),
                 lambda state: state.has("Progressive Mountain", player, 2))

        set_rule(world.get_location("Caldera Access"),
                 lambda state: state.has("Progressive Mountain", player, 3))
        set_rule(world.get_location("Kiln Access"),
                 lambda state: state.has("Progressive Mountain", player, 4))
    except KeyError:
        pass

    # Acquire locations - require having received the item from AP first
    acquire_item_rules = {
        "Acquire Rope Spool": "Rope Spool",
        "Acquire Rope Cannon": "Rope Cannon",
        "Acquire Anti-Rope Spool": "Anti-Rope Spool",
        "Acquire Anti-Rope Cannon": "Anti-Rope Cannon",
        "Acquire Chain Launcher": "Chain Launcher",
        "Acquire Piton": "Piton",
        "Acquire Rescue Claw": "Rescue Claw",
        "Acquire Magic Bean": "Magic Bean",
        "Acquire Parasol": "Parasol",
        "Acquire Balloon": "Balloon",
        "Acquire Balloon Bunch": "Balloon Bunch",
        "Acquire Scout Cannon": "Scout Cannon",
        "Acquire Flying Disc": "Flying Disc",
        "Acquire Guidebook": "Guidebook",
        "Acquire Portable Stove": "Portable Stove",
        "Acquire Checkpoint Flag": "Checkpoint Flag",
        "Acquire Lantern": "Lantern",
        "Acquire Flare": "Flare",
        "Acquire Torch": "Torch",
        "Acquire Faerie Lantern": "Faerie Lantern",
        "Acquire Blowgun": "Blowgun",
        "Acquire Cactus": "Cactus",
        "Acquire Compass": "Compass",
        "Acquire Pirate's Compass": "Pirate's Compass",
        "Acquire Binoculars": "Binoculars",
        "Acquire Bandages": "Bandages",
        "Acquire First-Aid Kit": "First-Aid Kit",
        "Acquire Antidote": "Antidote",
        "Acquire Heat Pack": "Heat Pack",
        "Acquire Cure-All": "Cure-All",
        "Acquire Remedy Fungus": "Remedy Fungus",
        "Acquire Medicinal Root": "Medicinal Root",
        "Acquire Aloe Vera": "Aloe Vera",
        "Acquire Sunscreen": "Sunscreen",
        "Acquire Marshmallow": "Marshmallow",
        "Acquire Glizzy": "Glizzy",
        "Acquire Fortified Milk": "Fortified Milk",
        "Acquire Scout Effigy": "Scout Effigy",
        "Acquire Cursed Skull": "Cursed Skull",
        "Acquire Pandora's Lunchbox": "Pandora's Lunchbox",
        "Acquire Ancient Idol": "Ancient Idol",
        "Acquire Strange Gem": "Strange Gem",
        "Acquire Book of Bones": "Book of Bones",
        "Acquire Cloud Fungus": "Cloud Fungus",
        "Acquire Bugle of Friendship": "Bugle of Friendship",
        "Acquire Bugle": "Bugle",
        "Acquire Shelf Shroom": "Shelf Shroom",
        "Acquire Bounce Shroom": "Bounce Shroom",
        "Acquire Button Shroom": "Button Shroom",
        "Acquire Bugle Shroom": "Bugle Shroom",
        "Acquire Cluster Shroom": "Cluster Shroom",
        "Acquire Chubby Shroom": "Chubby Shroom",
        "Acquire Trail Mix": "Trail Mix",
        "Acquire Granola Bar": "Granola Bar",
        "Acquire Scout Cookies": "Scout Cookies",
        "Acquire Airline Food": "Airline Food",
        "Acquire Energy Drink": "Energy Drink",
        "Acquire Sports Drink": "Sports Drink",
        "Acquire Big Lollipop": "Big Lollipop",
        "Acquire Big Egg": "Big Egg",
        "Acquire Egg": "Egg",
        "Acquire Cooked Bird": "Cooked Bird",
        "Acquire Honeycomb": "Honeycomb",
        "Acquire Beehive": "Beehive",
        "Acquire Scorpion": "Scorpion",
        "Acquire Tick": "Tick",
        "Acquire Conch": "Conch",
        "Acquire Dynamite": "Dynamite",
        "Acquire Bing Bong": "Bing Bong",
        "Acquire Mandrake": "Mandrake",
        "Acquire Red Crispberry": "Red Crispberry",
        "Acquire Green Crispberry": "Green Crispberry",
        "Acquire Yellow Crispberry": "Yellow Crispberry",
        "Acquire Coconut": "Coconut",
        "Acquire Coconut Half": "Coconut Half",
        "Acquire Brown Berrynana": "Brown Berrynana",
        "Acquire Blue Berrynana": "Blue Berrynana",
        "Acquire Pink Berrynana": "Pink Berrynana",
        "Acquire Yellow Berrynana": "Yellow Berrynana",
        "Acquire Orange Winterberry": "Orange Winterberry",
        "Acquire Yellow Winterberry": "Yellow Winterberry",
        "Acquire Red Prickleberry": "Red Prickleberry",
        "Acquire Gold Prickleberry": "Gold Prickleberry",
        "Acquire Red Shroomberry": "Red Shroomberry",
        "Acquire Blue Shroomberry": "Blue Shroomberry",
        "Acquire Green Shroomberry": "Green Shroomberry",
        "Acquire Yellow Shroomberry": "Yellow Shroomberry",
        "Acquire Purple Shroomberry": "Purple Shroomberry",
        "Acquire Purple Kingberry": "Purple Kingberry",
        "Acquire Yellow Kingberry": "Yellow Kingberry",
        "Acquire Green Kingberry": "Green Kingberry",
        "Acquire Napberry": "Napberry",
        "Acquire Black Clusterberry": "Black Clusterberry",
        "Acquire Red Clusterberry": "Red Clusterberry",
        "Acquire Yellow Clusterberry": "Yellow Clusterberry",
        "Acquire Scoutmaster's Bugle": "Scoutmaster's Bugle",
        "Acquire Yellow Berrynana Peel": "Yellow Berrynana",
        "Acquire Pink Berrynana Peel": "Pink Berrynana",
        "Acquire Blue Berrynana Peel": "Blue Berrynana",
        "Acquire Brown Berrynana Peel": "Brown Berrynana",
    }

    # Apply acquire item rules - combine with biome requirements where needed
    for location_name, required_item in acquire_item_rules.items():
        try:
            if location_name in MESA_LOCATIONS:
                set_rule(world.get_location(location_name),
                         lambda state, item=required_item:
                         state.has(item, player) and state.has("Mesa Access", player))
            elif location_name in ALPINE_LOCATIONS:
                set_rule(world.get_location(location_name),
                         lambda state, item=required_item:
                         state.has(item, player) and state.has("Alpine Access", player))
            elif location_name in ROOTS_LOCATIONS:
                set_rule(world.get_location(location_name),
                         lambda state, item=required_item:
                         state.has(item, player) and state.has("Roots Access", player))
            elif location_name in TROPICS_LOCATIONS:
                set_rule(world.get_location(location_name),
                         lambda state, item=required_item:
                         state.has(item, player) and state.has("Tropics Access", player))
            elif location_name in CALDERA_LOCATIONS:
                set_rule(world.get_location(location_name),
                         lambda state, item=required_item:
                         state.has(item, player) and state.has("Caldera Access", player))
            elif location_name in KILN_LOCATIONS:
                set_rule(world.get_location(location_name),
                         lambda state, item=required_item:
                         state.has(item, player) and state.has("Kiln Access", player))
            else:
                set_rule(world.get_location(location_name),
                         lambda state, item=required_item: state.has(item, player))
        except KeyError:
            pass

    # All regular badge locations are always accessible
    regular_badges = [
        "Mycology Badge",
        "Endurance Badge", "Toxicology Badge", "Bouldering Badge",
        "Cooking Badge", "Plunderer Badge",
        "Esoterica Badge", "Beachcomber Badge", "Mentorship Badge",
        "Aeronautics Badge",
        "Disaster Response Badge", "Competitive Eating Badge",
        "Cryptogastronomy Badge", "Calcium Intake Badge", "Applied Esoterica Badge",
        "Happy Camper Badge", "First Aid Badge", "Clutch Badge",
        "Emergency Preparedness Badge", "Bookworm Badge", "Resourcefulness Badge",
        "Ultimate Badge",
    ]

    for badge_name in regular_badges:
        try:
            set_rule(world.get_location(badge_name), lambda state: True)
        except KeyError:
            pass

    # Luggage locations are always accessible
    luggage_locations = [
        "Open 1 luggage",
        "Open 5 luggage",
        "Open 10 luggage",
        "Open 15 luggage",
        "Open 20 luggage",
        "Open 25 luggage",
        "Open 30 luggage",
        "Open 35 luggage",
        "Open 40 luggage",
        "Open 45 luggage",
        "Open 50 luggage",
        "Open 55 luggage",
        "Open 60 luggage",
        "Open 65 luggage",
        "Open 70 luggage",
        "Open 75 luggage",
        "Open 80 luggage",
        "Open 85 luggage",
        "Open 90 luggage",
        "Open 95 luggage",
        "Open 100 luggage",
        "Open 2 luggage in a single run",
        "Open 5 luggage in a single run",
        "Open 10 luggage in a single run",
        "Open 15 luggage in a single run",
        "Open 20 luggage in a single run",
    ]

    for luggage_name in luggage_locations:
        try:
            set_rule(world.get_location(luggage_name), lambda state: True)
        except KeyError:
            pass

    # Biome-locked badges (not in acquire_item_rules)
    for mesa_item in MESA_LOCATIONS:
        if mesa_item not in acquire_item_rules:
            try:
                set_rule(world.get_location(mesa_item),
                         lambda state: state.has("Mesa Access", player))
            except KeyError:
                pass

    for alpine_item in ALPINE_LOCATIONS:
        if alpine_item not in acquire_item_rules:
            try:
                set_rule(world.get_location(alpine_item),
                         lambda state: state.has("Alpine Access", player))
            except KeyError:
                pass

    for roots_item in ROOTS_LOCATIONS:
        if roots_item not in acquire_item_rules:
            try:
                set_rule(world.get_location(roots_item),
                         lambda state: state.has("Roots Access", player))
            except KeyError:
                pass

    for tropics_item in TROPICS_LOCATIONS:
        if tropics_item not in acquire_item_rules:
            try:
                set_rule(world.get_location(tropics_item),
                         lambda state: state.has("Tropics Access", player))
            except KeyError:
                pass

    for caldera_item in CALDERA_LOCATIONS:
        if caldera_item not in acquire_item_rules:
            try:
                set_rule(world.get_location(caldera_item),
                         lambda state: state.has("Caldera Access", player))
            except KeyError:
                pass

    for kiln_item in KILN_LOCATIONS:
        if kiln_item not in acquire_item_rules:
            try:
                set_rule(world.get_location(kiln_item),
                         lambda state: state.has("Kiln Access", player))
            except KeyError:
                pass

    # Ascent locations require their corresponding Ascent Completed events
    roman_numerals = ["II", "III", "IV", "V", "VI", "VII", "VIII"]

    max_relevant_ascent = 7
    if goal_type == 0 or goal_type == 3:  # Peak Goal or Peak and Badges Goal
        max_relevant_ascent = required_ascent

    # Event locations for ascent completion
    for ascent_num in range(1, max_relevant_ascent + 1):
        try:
            if ascent_num in [1, 2]:
                set_rule(world.get_location(f"Ascent {ascent_num} Completed"),
                         lambda state, asc=ascent_num:
                         state.has("Kiln Access", player) and
                         state.has("Progressive Ascent", player, asc))
            elif ascent_num in [3, 4, 5]:
                if progressive_stamina_enabled:
                    set_rule(world.get_location(f"Ascent {ascent_num} Completed"),
                             lambda state, asc=ascent_num:
                             state.has("Kiln Access", player) and
                             state.has("Progressive Ascent", player, asc) and
                             state.has("Progressive Stamina Bar", player, 3))
                else:
                    set_rule(world.get_location(f"Ascent {ascent_num} Completed"),
                             lambda state, asc=ascent_num:
                             state.has("Kiln Access", player) and
                             state.has("Progressive Ascent", player, 3))
            elif ascent_num in [6, 7]:
                if progressive_stamina_enabled:
                    set_rule(world.get_location(f"Ascent {ascent_num} Completed"),
                             lambda state, asc=ascent_num:
                             state.has("Kiln Access", player) and
                             state.has("Progressive Ascent", player, asc) and
                             state.has("Progressive Stamina Bar", player, 3) and
                             state.has("Progressive Endurance", player, 4))
                else:
                    set_rule(world.get_location(f"Ascent {ascent_num} Completed"),
                             lambda state, asc=ascent_num:
                             state.has("Kiln Access", player) and
                             state.has("Progressive Ascent", player, asc) and
                             state.has("Progressive Endurance", player, 4))
        except KeyError:
            pass

    # Ascent badge locations require Progressive Ascent
    for ascent_num in range(1, max_relevant_ascent + 1):
        roman_num = roman_numerals[ascent_num - 1]
        ascent_locations = [
            f"Beachcomber {roman_num} Badge (Ascent {ascent_num})",
            f"Trailblazer {roman_num} Badge (Ascent {ascent_num})",
            f"Alpinist {roman_num} Badge (Ascent {ascent_num})",
            f"Volcanology {roman_num} Badge (Ascent {ascent_num})",
            f"Nomad {roman_num} Badge (Ascent {ascent_num})",
            f"Forestry {roman_num} Badge (Ascent {ascent_num})"
        ]

        for ascent_name in ascent_locations:
            try:
                if ascent_num in [1, 2]:
                    set_rule(world.get_location(ascent_name),
                             lambda state, asc=ascent_num:
                             state.has("Kiln Access", player) and
                             state.has("Progressive Ascent", player, asc))
                elif ascent_num in [3, 4, 5]:
                    if progressive_stamina_enabled:
                        set_rule(world.get_location(ascent_name),
                                lambda state, asc=ascent_num:
                                state.has("Kiln Access", player) and
                                state.has("Progressive Ascent", player, asc) and
                                state.has("Progressive Stamina Bar", player, 3))
                    else:
                        set_rule(world.get_location(ascent_name),
                                 lambda state, asc=ascent_num:
                                 state.has("Kiln Access", player) and
                                 state.has("Progressive Ascent", player, 3))
                elif ascent_num in [6, 7]:
                    if progressive_stamina_enabled:
                        set_rule(world.get_location(ascent_name),
                                lambda state, asc=ascent_num:
                                state.has("Kiln Access", player) and
                                state.has("Progressive Ascent", player, asc) and
                                state.has("Progressive Stamina Bar", player, 3) and
                                state.has("Progressive Endurance", player, 4))
                    else:
                        set_rule(world.get_location(f"Ascent {ascent_num} Completed"),
                                 lambda state, asc=ascent_num:
                                 state.has("Kiln Access", player) and
                                 state.has("Progressive Ascent", player, asc) and
                                 state.has("Progressive Endurance", player, 4))
            except KeyError:
                pass

    # Scout sashes require completion of ALL previous ascents
    scout_sashe_requirements = {
        "Rabbit Scout sashe (Ascent 1)": ["Kiln Access"],
        "Raccoon Scout sashe (Ascent 2)": ["Ascent 1 Completed", "Kiln Access"],
        "Mule Scout sashe (Ascent 3)": ["Ascent 1 Completed", "Ascent 2 Completed", "Kiln Access"],
        "Kangaroo Scout sashe (Ascent 4)": ["Ascent 1 Completed", "Ascent 2 Completed", "Ascent 3 Completed",
                                            "Kiln Access"],
        "Owl Scout sashe (Ascent 5)": ["Ascent 1 Completed", "Ascent 2 Completed", "Ascent 3 Completed",
                                       "Ascent 4 Completed", "Kiln Access"],
        "Wolf Scout sashe (Ascent 6)": ["Ascent 1 Completed", "Ascent 2 Completed", "Ascent 3 Completed",
                                        "Ascent 4 Completed", "Ascent 5 Completed", "Kiln Access"],
        "Goat Scout sashe (Ascent 7)": ["Ascent 1 Completed", "Ascent 2 Completed", "Ascent 3 Completed",
                                        "Ascent 4 Completed", "Ascent 5 Completed", "Ascent 6 Completed", "Kiln Access"]
    }

    for scout_name, required_ascents in scout_sashe_requirements.items():
        try:
            if scout_name == "Rabbit Scout sashe (Ascent 1)":
                set_rule(world.get_location(scout_name),
                         lambda state: state.has("Progressive Ascent", player, 1))
            else:
                import re
                match = re.search(r'\(Ascent (\d+)\)', scout_name)
                if match:
                    scout_ascent = int(match.group(1))
                    if scout_ascent in [1, 2]:
                        set_rule(world.get_location(scout_name),
                                 lambda state, reqs=required_ascents, asc=scout_ascent:
                                 all(state.has(ascent, player) for ascent in reqs) and
                                 state.has("Progressive Ascent", player, asc))
                    elif scout_ascent in [3, 4, 5]:
                        if progressive_stamina_enabled:
                            set_rule(world.get_location(scout_name),
                                    lambda state, reqs=required_ascents, asc=scout_ascent:
                                    all(state.has(ascent, player) for ascent in reqs) and
                                    state.has("Progressive Ascent", player, asc) and
                                    state.has("Progressive Stamina Bar", player, 3))
                        else:
                            set_rule(world.get_location(scout_name),
                                     lambda state, reqs=required_ascents, asc=scout_ascent:
                                     all(state.has(ascent, player) for ascent in reqs) and
                                     state.has("Progressive Ascent", player, asc))
                    elif scout_ascent in [6, 7]:
                        if progressive_stamina_enabled:
                            set_rule(world.get_location(scout_name),
                                    lambda state, reqs=required_ascents, asc=scout_ascent:
                                    all(state.has(ascent, player) for ascent in reqs) and
                                    state.has("Progressive Ascent", player, asc) and
                                    state.has("Progressive Stamina Bar", player, 3) and
                                    state.has("Progressive Endurance", player, 4))
                        else:
                            set_rule(world.get_location(scout_name),
                                     lambda state, reqs=required_ascents, asc=scout_ascent:
                                     all(state.has(ascent, player) for ascent in reqs) and
                                     state.has("Progressive Ascent", player, asc) and
                                     state.has("Progressive Endurance", player, 4))
        except KeyError:
            pass
