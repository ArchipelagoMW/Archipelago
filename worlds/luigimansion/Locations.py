from typing import List, Tuple, Optional, Callable, NamedTuple
from BaseClasses import MultiWorld, Location
from .Regions import is_option_enabled

EventId: Optional[int] = None


# need to understand how Location subclasses are used to ensure passing of correct information

class LMLocation(Location):
    game: str = "Luigi's Mansion"


class LocationData(NamedTuple):
    parent_region: str
    name: str
    code: Optional[int]
    rule: Callable = lambda state: True

ghost_affected_locations = [
    LocationData('Study', 'Study Clear Chest', 8501),
]

def get_locations(multiworld: Optional[MultiWorld], player: Optional[int]) -> Tuple[LocationData, ...]:
    # 1337000 - 1337155 Generic locations
    # 1337171 - 1337175 New Pickup checks
    # 1337246 - 1337249 Ancient Pyramid
    location_table: List[LocationData] = [
        # Present item locations
        LocationData("Wardrobe", 'Wardrobe Clear Chest', 8500,
                     lambda state: state.has("Boolossus", player)),
        LocationData('Study', 'Study Clear Chest', 8501),
        LocationData('Master Bedroom', 'Master Bedroom Clear Chest', 8502),
        LocationData('Nursery', 'Nursery Clear Chest', 8503),
        LocationData('1F Washroom', '1F Washroom Toilet', 8504),
        LocationData('Fortune-Teller\'s Room', 'Fortune Teller Clear Chest', 8505,
                     lambda state: state.has_group("Mario Item", player, multiworld.MarioItems[player])),
        LocationData('Fortune-Teller\'s Room', 'Fortune Teller Candles Key', 8506,
                     lambda state: state.has("Fire Element Medal", player)),
        LocationData('Laundry Room', 'Laundry Washing Machine', 8507),
        LocationData('Butler\'s Room', 'Butler Clear Chest', 8508,
                     lambda state: state.has("Fire Element Medal", player) and state.has("Boo Release",
                                                                                         player)),
        LocationData('Hidden Room', 'Hidden Room Large Chest L', 8509),
        LocationData('Hidden Room', 'Hidden Room Large Chest C', 8510),
        LocationData('Hidden Room', 'Hidden Room Large Chest R', 8511),
        LocationData('Hidden Room', 'Hidden Room Small Chest L Floor', 8512),
        LocationData('Hidden Room', 'Hidden Room Small Chest R Floor', 8513),
        LocationData('Hidden Room', 'Hidden Room Small Chest L Shelf', 8514),
        LocationData('Hidden Room', 'Hidden Room Small Chest R Shelf', 8515),
        LocationData('Conservatory', 'Conservatory Clear Chest', 8516),
        LocationData('Dining Room', 'Dining Room Clear Chest', 8517,
                     lambda state: state.has("Fire Element Medal", player)),
        LocationData('Rec Room', 'Rec Room Treadmill Key', 8518),
        LocationData('Rec Room', 'Rec Room Clear Chest', 8519),
        LocationData('Courtyard', 'Courtyard Birdhouse', 8520),
        LocationData('2F Bathroom', '2F Bathroom Clear Chest', 8521,
                     lambda state: state.has("Ice Element Medal", player)),
        LocationData('Nana\'s Room', 'Nana\'s Room Clear Chest', 8522),
        LocationData('Observatory', 'Observatory Power Star', 8523),
        LocationData('Twins\' Room', 'Twins\' Room Clear Chest', 8524,
                     lambda state: state.has_group("Medal", player)),
        LocationData('Billiards Room', 'Billiards Room Clear Chest', 8525),
        LocationData('Balcony', 'Balcony Room Clear Chest', 8526,
                     lambda state: state.has("Ice Element Medal", player)),
        LocationData('Ceramics Studio', 'Ceramics Studio Clear Chest', 8527,
                     lambda state: state.has("Ice Element Medal", player)),
        LocationData('Sealed Room', 'Sealed Room NW Shelf Chest', 8528),
        LocationData('Sealed Room', 'Sealed Room NE Shelf Chest', 8529),
        LocationData('Sealed Room', 'Sealed Room SW Shelf Chest', 8530),
        LocationData('Sealed Room', 'Sealed Room SE Shelf Chest', 8531),
        LocationData('Sealed Room', 'Sealed Room Table Chest', 8532),
        LocationData('Sealed Room', 'Sealed Room Lower Big Chest', 8533),
        LocationData('Sealed Room', 'Sealed Room Upper L Big Chest', 8534),
        LocationData('Sealed Room', 'Sealed Room Upper C Big Chest', 8535),
        LocationData('Sealed Room', 'Sealed Room Upper R Big Chest', 8536),
        LocationData('Armory', 'Armory 1st Gray Chest', 8537),
        LocationData('Armory', 'Armory 2nd Gray Chest', 8538),
        LocationData('Armory', 'Armory 3rd Gray Chest', 8539),
        LocationData('Armory', 'Armory 4th Gray Chest', 8540),
        LocationData('Armory', 'Armory 5th Gray Chest', 8541),
        LocationData('Telephone Room', 'Telephone Room Wood Chest C Chest', 8542),
        LocationData('Telephone Room', 'Telephone Room Wood Chest R1 Chest', 8543),
        LocationData('Telephone Room', 'Telephone Room Wood Chest R2 Chest', 8544),
        LocationData('Guest Room', 'Guest Room Clear Chest', 8545,
                     lambda state: state.has("Water Element Medal", player)),
        LocationData('Parlor', 'Parlor Clear Chest', 8546),
        LocationData('Cold Storage', 'Cold Storage Clear Chest', 8542,
                     lambda state: state.has("Fire Element Medal", player)),

        # Ghost Affected Clear Chests
        LocationData('Study', 'Study Clear Chest', 8501),

        # Game Event Locations
        LocationData('Balcony', 'Boolossus', None,
                     lambda state: state.has("Ice Element Medal", player)),
        LocationData('Storage Room', 'Storage Room Cage', None),
        # LocationData('Nursery', 'Chauncey',  None),
        # LocationData('Graveyard', 'Bogmire',  None),
    ]

    # Adds all waterable plants as locations
    if not multiworld or is_option_enabled(multiworld, player, "Plants"):
        location_table += (
            LocationData('Library', 'Library: Terminal 2 (Lachiem)', 1337156, lambda state: state.has('Tablet', player)),
            LocationData('Library', 'Library: Terminal 1 (Windaria)', 1337157, lambda state: state.has('Tablet', player)),
            # 1337158 Is lost in time
            LocationData('Library', 'Library: Terminal 3 (Emporer Nuvius)', 1337159,
                       lambda state: state.has('Tablet', player)),
            LocationData('Library', 'Library: V terminal 1 (War of the Sisters)', 1337160,
                       lambda state: state.has_all({'Tablet', 'Library Keycard V'}, player)),
            LocationData('Library', 'Library: V terminal 2 (Lake Desolation Map)', 1337161,
                       lambda state: state.has_all({'Tablet', 'Library Keycard V'}, player)),
            LocationData('Library', 'Library: V terminal 3 (Vilete)', 1337162,
                       lambda state: state.has_all({'Tablet', 'Library Keycard V'}, player)),
            LocationData('Library top', 'Library: Backer room terminal (Vandagray Metropolis Map)', 1337163,
                       lambda state: state.has('Tablet', player)),
            LocationData('Varndagroth tower right (elevator)',
                       'Varndagroth Towers (Right): Medbay terminal (Bleakness Research)', 1337164,
                       lambda state: state.has('Tablet', player) and state._timespinner_has_keycard_B(multiworld, player)),
            LocationData('The lab (upper)', 'Lab: Download and chest room terminal (Experiment #13)', 1337165,
                       lambda state: state.has('Tablet', player)),
            LocationData('The lab (power off)', 'Lab: Middle terminal (Amadeus Laboratory Map)', 1337166,
                       lambda state: state.has('Tablet', player)),
            LocationData('The lab (power off)', 'Lab: Sentry platform terminal (Origins)', 1337167,
                       lambda state: state.has('Tablet', player)),
            LocationData('The lab', 'Lab: Experiment 13 terminal (W.R.E.C Farewell)', 1337168,
                       lambda state: state.has('Tablet', player)),
            LocationData('The lab', 'Lab: Left terminal (Biotechnology)', 1337169,
                       lambda state: state.has('Tablet', player)),
            LocationData('The lab (power off)', 'Lab: Right terminal (Experiment #11)', 1337170,
                       lambda state: state.has('Tablet', player))
        )

    # Adds the myriad shackable objects as locations
    if multiworld.Interactables == True:
        location_table += (
            LocationData('Left Side forest Caves', 'Lake Serene: Cantoran', 1337176),
        )
    # Adds Toads as locations
    if not multiworld or is_option_enabled(multiworld, player, "Toadsanity"):
        location_table += (
            LocationData('Left Side forest Caves', 'Lake Serene: Cantoran', 1337176),
        )

    # Adds Portrait Ghosts as locations
    if not multiworld or is_option_enabled(multiworld, player, "Portrait Ghosts"):
        location_table += (
            LocationData('Left Side forest Caves', 'Lake Serene: Cantoran', 1337176),
        )

    # Adds Blue Ghosts and Gold Mice as locations
    if not multiworld or is_option_enabled(multiworld, player, "Money Ghosts"):
        location_table += (
            LocationData('Lower lake desolation', 'Lake Desolation: Memory - Coyote Jump (Time Messenger)', 1337177),
            LocationData('Library', 'Library: Memory - Waterway (A Message)', 1337178),
            LocationData('Library top', 'Library: Memory - Library Gap (Lachiemi Sun)', 1337179),
            LocationData('Library top', 'Library: Memory - Mr. Hat Portrait (Moonlit Night)', 1337180),
            LocationData('Varndagroth tower left', 'Varndagroth Towers (Left): Memory - Elevator (Nomads)', 1337181,
                       lambda state: state.has('Elevator Keycard', player)),
            LocationData('Varndagroth tower right (lower)', 'Varndagroth Towers: Memory - Siren Elevator (Childhood)',
                       1337182, lambda state: state._timespinner_has_keycard_B(multiworld, player)),
            LocationData('Varndagroth tower right (lower)', 'Varndagroth Towers (Right): Memory - Bottom (Faron)',
                       1337183),
            LocationData('Military Fortress', 'Military Fortress: Memory - Bomber Climb (A Solution)', 1337184,
                       lambda state: state.has('Timespinner Wheel',
                                               player) and state._timespinner_has_doublejump_of_npc(multiworld, player)),
            LocationData('The lab', 'Lab: Memory - Genza\'s Secret Stash 1 (An Old Friend)', 1337185,
                       lambda state: state._timespinner_can_break_walls(multiworld, player)),
            LocationData('The lab', 'Lab: Memory - Genza\'s Secret Stash 2 (Twilight Dinner)', 1337186,
                       lambda state: state._timespinner_can_break_walls(multiworld, player)),
            LocationData('Emperors tower', 'Emperor\'s Tower: Memory - Way Up There (Final Circle)', 1337187,
                       lambda state: state._timespinner_has_doublejump_of_npc(multiworld, player)),
            LocationData('Forest', 'Forest: Journal - Rats (Lachiem Expedition)', 1337188),
            LocationData('Forest', 'Forest: Journal - Bat Jump Ledge (Peace Treaty)', 1337189,
                       lambda state: state._timespinner_has_doublejump_of_npc(multiworld,
                                                                              player) or state._timespinner_has_forwarddash_doublejump(
                           multiworld, player) or state._timespinner_has_fastjump_on_npc(multiworld, player)),
            LocationData('Castle Ramparts', 'Castle Ramparts: Journal - Floating in Moat (Prime Edicts)', 1337190),
            LocationData('Castle Ramparts', 'Castle Ramparts: Journal - Archer + Knight (Declaration of Independence)',
                       1337191),
            LocationData('Castle Keep', 'Castle Keep: Journal - Under the Twins (Letter of Reference)', 1337192),
            LocationData('Castle Keep', 'Castle Keep: Journal - Castle Loop Giantess (Political Advice)', 1337193),
            LocationData('Royal towers (lower)', 'Royal Towers: Journal - Aelana\'s Room (Diplomatic Missive)', 1337194,
                       lambda state: state._timespinner_has_pink(multiworld, player)),
            LocationData('Royal towers (upper)', 'Royal Towers: Journal - Top Struggle Juggle Base (War of the Sisters)',
                       1337195),
            LocationData('Royal towers (upper)', 'Royal Towers: Journal - Aelana Boss (Stained Letter)', 1337196),
            LocationData('Royal towers', 'Royal Towers: Journal - Near Bottom Struggle Juggle (Mission Findings)',
                       1337197, lambda state: state._timespinner_has_doublejump_of_npc(multiworld, player)),
            LocationData('Caves of Banishment (Maw)', 'Caves of Banishment (Maw): Journal - Lower Left Caves (Naivety)',
                       1337198)
        )

    # 1337199 - 1337236 Reserved for future use

    # Turns Boos into check locations and adds Boos as items
    if not multiworld or is_option_enabled(multiworld, player, "Boosanity"):
        location_table += (
            LocationData('Ravenlord\'s Lair', 'Ravenlord: Post fight (pedestal)', 1337237),
            LocationData('Ifrit\'s Lair', 'Ifrit: Post fight (pedestal)', 1337238),
            LocationData('Temporal Gyre', 'Temporal Gyre: Chest 1', 1337239),
            LocationData('Temporal Gyre', 'Temporal Gyre: Chest 2', 1337240),
            LocationData('Temporal Gyre', 'Temporal Gyre: Chest 3', 1337241),
            LocationData('Ravenlord\'s Lair', 'Ravenlord: Pre fight', 1337242),
            LocationData('Ravenlord\'s Lair', 'Ravenlord: Post fight (chest)', 1337243),
            LocationData('Ifrit\'s Lair', 'Ifrit: Pre fight', 1337244),
            LocationData('Ifrit\'s Lair', 'Ifrit: Post fight (chest)', 1337245),
        )

    # Room Clear Chests Affected by Random Ghost types
    if multiworld.Enemizer == False:
         location_table += (
             LocationData('Left Side forest Caves', 'Lake Serene: Cantoran',  1337176),
         )
    else:

    return tuple(location_table)


