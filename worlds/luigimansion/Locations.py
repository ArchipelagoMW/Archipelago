from typing import List, Tuple, Optional, Callable, NamedTuple
from BaseClasses import MultiWorld, Location

EventId: Optional[int] = None


# need to understand how Location subclasses are used to ensure passing of correct information

class LMLocation(Location):
    game: str = "Luigi's Mansion"


class LocationData(NamedTuple):
    parent_region: str
    name: str
    code: Optional[int]
    locked_item: Optional[str] = None
    rule: Callable = lambda state: True


def get_locations(multiworld: Optional[MultiWorld], player: Optional[int]) -> Tuple[LocationData, ...]:
    location_table: List[LocationData] = [
        LocationData("Wardrobe", 'Wardrobe Clear Chest', 8500,
                     rule=lambda state: state.has("Blackout", player)),
        LocationData('Study', 'Study Clear Chest', 8501),
        LocationData('Master Bedroom', 'Master Bedroom Clear Chest', 8502),
        LocationData('Nursery', 'Nursery Clear Chest', 8503),
        LocationData('1F Washroom', '1F Washroom Toilet', 8504),
        LocationData('Fortune-Teller\'s Room', 'Fortune Teller Clear Chest', 8505,
                     rule=lambda state: state.has_group("Mario Item", player, multiworld.MarioItems[player])),
        LocationData('Fortune-Teller\'s Room', 'Fortune Teller Candles Key', 8506,
                     rule=lambda state: state.has("Fire Element Medal", player)),
        LocationData('Laundry Room', 'Laundry Washing Machine', 8507),
        LocationData('Butler\'s Room', 'Butler Clear Chest', 8508,
                     rule=lambda state: state.has("Fire Element Medal", player) and state.has("Boo Release",
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
                     rule=lambda state: state.has("Fire Element Medal", player)),
        LocationData('Rec Room', 'Rec Room Treadmill Key', 8518),
        LocationData('Rec Room', 'Rec Room Clear Chest', 8519),
        LocationData('Courtyard', 'Courtyard Birdhouse', 8520),
        LocationData('2F Bathroom', '2F Bathroom Clear Chest', 8521),
        LocationData('Nana\'s Room', 'Nana\'s Room Clear Chest', 8522),
        LocationData('Observatory', 'Observatory Power Star', 8523),
        LocationData('Twins\' Room', 'Twins\' Room Clear Chest', 8524,
                     rule=lambda state: state.has_group("Medal", player)),
        LocationData('Billiards Room', 'Billiards Room Clear Chest', 8525),
        LocationData('Balcony', 'Balcony Room Clear Chest', 8526,
                     rule=lambda state: state.has("Ice Element Medal", player)),
        LocationData('Ceramics Studio', 'Ceramics Studio Clear Chest', 8527,
                     rule=lambda state: state.has("Ice Element Medal", player)),
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
                     rule=lambda state: state.has("Water Element Medal", player)),
        LocationData('Parlor', 'Parlor Clear Chest', 8546),
        LocationData('Cold Storage', 'Cold Storage Clear Chest', 8542,
                     rule=lambda state: state.has("Fire Element Medal", player)),

        # Ghost Affected Clear Chests. Rules applied to region entrances
        LocationData('Study', 'Study Clear Chest', 8501),

        # Game Event Locations
        LocationData('Balcony', 'Boolossus', None, "Blackout", lambda state: state.has("Ice Element Medal", player)),
        LocationData('Storage Room', 'Storage Room Cage', None, "Boo Release"),
        # LocationData('Nursery', 'Chauncey',  None),
        # LocationData('Graveyard', 'Bogmire',  None),
        # LocationData('Secret Altar', 'King Boo', None, "Mario") How does make Mario a victory?
    ]

    # Adds all waterable plants as locations
    if multiworld.Plants[player] == True:
        location_table += (
            LocationData('Wardrobe Balcony', 'Wardrobe Balcony Plant 1', 1337156,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Wardrobe Balcony', 'Wardrobe Balcony Plant 2', 1337156,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Wardrobe Balcony', 'Wardrobe Balcony Plant 3', 1337156,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Wardrobe Balcony', 'Wardrobe Balcony Plant 4', 1337156,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Master Bedroom', 'Master Bedroom Plant', 1337156,
                         rule=lambda state: state.has("Water Element Medal", player)),
            #   LocationData('Boneyard', 'Huge Flower', 1337156,
            #               rule=lambda state: state.has("Water Element Medal", player) and state.has()),  need to determine how to make unskippable
            LocationData('Courtyard', 'Courtyard Fountain Plant 1', 1337156,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Courtyard', 'Courtyard Fountain Plant 2', 1337156,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Courtyard', 'Courtyard Fountain Plant 3', 1337156,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Courtyard', 'Courtyard Fountain Plant 4', 1337156,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Balcony', 'Balcony Plant 1', 1337156,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Balcony', 'Balcony Plant 2', 1337156,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Balcony', 'Balcony Plant 3', 1337156,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Balcony', 'Balcony Plant 4', 1337156,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Balcony', 'Balcony Plant 5', 1337156,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Balcony', 'Balcony Plant 6', 1337156,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Balcony', 'Balcony Plant 7', 1337156,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Balcony', 'Balcony Plant 8', 1337156,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Balcony', 'Balcony Plant 9', 1337156,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Balcony', 'Balcony Plant 10', 1337156,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Balcony', 'Balcony Plant 11', 1337156,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Balcony', 'Balcony Plant 12', 1337156,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Balcony', 'Balcony Plant 13', 1337156,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Balcony', 'Balcony Plant 14', 1337156,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Balcony', 'Balcony Plant 15', 1337156,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Balcony', 'Balcony Plant 16', 1337156,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Sitting Room', 'Sitting Room Plant', 1337156,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Guest Room', 'Guest Room Plant', 1337156,
                         rule=lambda state: state.has("Water Element Medal", player))
        )

    # Adds the myriad shackable objects as locations
    if multiworld.Interactables[player] == True:
        location_table += (
            LocationData('Left Side forest Caves', 'Lake Serene: Cantoran', 1337176),
        )
    # Adds Toads as locations
    if multiworld.Toadsanity[player] == True:
        location_table += (
            LocationData('Foyer', 'Foyer Toad', 1337176),
            LocationData('Wardrobe', 'Wardrobe Balcony Toad', 1337176),
            LocationData('1F Washroom', '1F Washroom Toad', 1337176),
            LocationData('Courtyard', 'Courtyard Toad', 1337176)
        )

    # Adds Portrait Ghosts as locations
    if multiworld.PortraitGhosts[player] == True:
        location_table += (
            LocationData('Study', 'Neville, the Bookish Father', 1337176),
            LocationData('Master Bedroom', 'Lydia, the Mirror-Gazing Mother', 1337176),
            LocationData('Nursery', 'Chauncey, the Spoiled Baby', 1337176),
            LocationData('Twins\' Room', 'Henry and Orville, the Twin Brothers', 1337176,
                         rule=lambda state: state.has_group("Medal", player)),
            LocationData('Ballroom', 'The Floating Whirlindas, the Dancing Couple', 1337176),
            LocationData('Butler\'s Room', 'Shivers, the Wandering Butler', 1337176,
                         rule=lambda state: state.has("Fire Element Medal", player)),
            LocationData('Fortune-Teller\'s Room', 'Madame Clairvoya, the Freaky Fortune-Teller', 1337176,
                         rule=lambda state: state.has_group("Mario Item", player, multiworld.MarioItems[player])),
            LocationData('Conservatory', ' Melody Pianissima, the Beautiful Pianist', 1337176),
            LocationData('Dining Room', 'Mr. Luggs, the Glutton', 1337176,
                         rule=lambda state: state.has("Fire Element Medal", player)),
            LocationData('Boneyard', 'Spooky, the Guard Dog', 1337176,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Graveyard', 'Bogmire, the Cemetary Shadow', 1337176),
            LocationData('Rec Room', 'Biff Atlas, the Bodybuilder', 1337176),
            LocationData('Billiards Room', 'Slim Bankshot, the Lonely Poolshark', 1337176),
            LocationData('2F Bathroom', 'Miss Petunia, the Bathing Beauty', 1337176,
                         rule=lambda state: state.has("Ice Element Medal", player)),
            LocationData('Nana\'s Room', 'Nana, the Scarf-Knitting Granny', 1337176),
            LocationData('Guest Room', 'Sue Pea, the Dozing Girl', 1337176,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Wardrobe', 'Uncle Grimmly, Hermit of the Darkness', 1337176,
                         rule=lambda state: state.has("Blackout", player)),
            LocationData('Balcony', 'Boolossus, the Jumbo Ghost', 1337176,
                         rule=lambda state: state.has("Ice Element Medal", player)),
            LocationData('Ceramics Studio', 'Jarvis, the Jar Collector', 1337176,
                         rule=lambda state: state.has("Ice Element Medal", player)),
            LocationData('Clockwork Room', 'Clockwork Soldiers, the Toy Platoon', 1337176),
            LocationData('Artist\'s Studio', 'Vincent van Gore, the Starving Artist', 1337176),
            LocationData('Cold Storage', 'Sir Weston, the Chilly Climber', 1337176,
                         rule=lambda state: state.has("Fire Element Medal", player))
        )

    # Adds Blue Ghosts and Gold Mice as locations
    if multiworld.SpeedySpirits[player] == True:
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
                                                 player) and state._timespinner_has_doublejump_of_npc(multiworld,
                                                                                                      player)),
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
            LocationData('Royal towers (upper)',
                         'Royal Towers: Journal - Top Struggle Juggle Base (War of the Sisters)',
                         1337195),
            LocationData('Royal towers (upper)', 'Royal Towers: Journal - Aelana Boss (Stained Letter)', 1337196),
            LocationData('Royal towers', 'Royal Towers: Journal - Near Bottom Struggle Juggle (Mission Findings)',
                         1337197, lambda state: state._timespinner_has_doublejump_of_npc(multiworld, player)),
            LocationData('Caves of Banishment (Maw)', 'Caves of Banishment (Maw): Journal - Lower Left Caves (Naivety)',
                         1337198)
        )

    # 1337199 - 1337236 Reserved for future use

    # Turns Boos into check locations and adds Boos as items
    if multiworld.Boosanity[player] == True:
        location_table += (
            LocationData('Parlor', 'Parlor Boo', 1337237),
            LocationData('Anteroom', 'Anteroom Boo', 1337238),
            LocationData('Wardrobe', 'Wardrobe Boo', 1337239),
            LocationData('Study', 'Study Boo', 1337240),
            LocationData('Master Bedroom', 'Master Bedroom Boo', 1337241),
            LocationData('Nursery', 'Nursery Boo', 1337242),
            LocationData('Twins\' Room', 'Twins\' Room Boo', 1337245),
            LocationData('Laundry Room', 'Laundry Room Boo', 1337243),
            LocationData('Butler\'s Room', 'Butler\'s Room Boo', 1337244),
            LocationData('Hidden Room', 'Hidden Room Boo', 1337245),
            LocationData('Fortune-Teller\'s Room', 'Fortune-Teller\'s Room Boo', 1337245),
            LocationData('Mirror Room', 'Mirror Room Boo', 1337245),
            LocationData('Ballroom', 'Ballroom Boo', 1337245),
            LocationData('Storage Room', 'Storage Room Boo', 1337245),
            LocationData('Dining Room', 'Dining Room Boo', 1337245),
            LocationData('Kitchen', 'Kitchen Boo', 1337245),
            LocationData('Conservatory', 'Conservatory Boo', 1337245),
            LocationData('Rec Room', 'Rec Room Boo', 1337245),
            LocationData('Billiards Room', 'Billiards Room Boo', 1337245),
            LocationData('Projection Room', 'Projection Room Boo', 1337245),
            LocationData('Tea Room', 'Tea Room Boo', 1337245),
            LocationData('Nana\'s Room', 'Nana\'s Room Boo', 1337245),
            LocationData('Sitting Room', 'Sitting Room Boo', 1337245),
            LocationData('Guest Room', 'Guest Room Boo', 1337245),
            LocationData('Safari Room', 'Safari Room Boo', 1337245),
            LocationData('Artist\'s Studio', 'Artist\'s Studio Boo', 1337245),
            LocationData('Armory', 'Armory Boo', 1337245),
            LocationData('Ceramics Studio', 'Ceramics Studio Boo', 1337245),
            LocationData('Telephone Room', 'Telephone Room Boo', 1337245),
            LocationData('Clockwork Room', 'Clockwork Room Boo', 1337245),
            LocationData('Astral Hall', 'Astral Hall Boo', 1337245),
            LocationData('Breaker Room', 'Breaker Room Boo', 1337245),
            LocationData('Cellar', 'Cellar Boo', 1337245),
            LocationData('Pipe Room', 'Pipe Room Boo', 1337245),
            LocationData('Cold Storage', 'Cold Storage Boo', 1337245)

        )
    else:
        # event location data for boos. Create as locked during location creation
        location_table += (
            LocationData('Parlor', 'Parlor Boo', None, "Boo"),
            LocationData('Anteroom', 'Anteroom Boo', None, "Boo"),
            LocationData('Wardrobe', 'Wardrobe Boo', None, "Boo"),
            LocationData('Study', 'Study Boo', None, "Boo"),
            LocationData('Master Bedroom', 'Master Bedroom Boo', None, "Boo"),
            LocationData('Nursery', 'Nursery Boo', None, "Boo"),
            LocationData('Twins\' Room', 'Twins\' Room Boo', None, "Boo"),
            LocationData('Laundry Room', 'Laundry Room Boo', None, "Boo"),
            LocationData('Butler\'s Room', 'Butler\'s Room Boo', None, "Boo"),
            LocationData('Hidden Room', 'Hidden Room Boo', None, "Boo"),
            LocationData('Fortune-Teller\'s Room', 'Fortune-Teller\'s Room Boo', None, "Boo"),
            LocationData('Mirror Room', 'Mirror Room Boo', None, "Boo"),
            LocationData('Ballroom', 'Ballroom Boo', None, "Boo"),
            LocationData('Storage Room', 'Storage Room Boo', None, "Boo"),
            LocationData('Dining Room', 'Dining Room Boo', None, "Boo"),
            LocationData('Kitchen', 'Kitchen Boo', None, "Boo"),
            LocationData('Conservatory', 'Conservatory Boo', None, "Boo"),
            LocationData('Rec Room', 'Rec Room Boo', None, "Boo"),
            LocationData('Billiards Room', 'Billiards Room Boo', None, "Boo"),
            LocationData('Projection Room', 'Projection Room Boo', None, "Boo"),
            LocationData('Tea Room', 'Tea Room Boo', None, "Boo"),
            LocationData('Nana\'s Room', 'Nana\'s Room Boo', None, "Boo"),
            LocationData('Sitting Room', 'Sitting Room Boo', None, "Boo"),
            LocationData('Guest Room', 'Guest Room Boo', None, "Boo"),
            LocationData('Safari Room', 'Safari Room Boo', None, "Boo"),
            LocationData('Artist\'s Studio', 'Artist\'s Studio Boo', None, "Boo"),
            LocationData('Armory', 'Armory Boo', None, "Boo"),
            LocationData('Ceramics Studio', 'Ceramics Studio Boo', None, "Boo"),
            LocationData('Telephone Room', 'Telephone Room Boo', None, "Boo"),
            LocationData('Clockwork Room', 'Clockwork Room Boo', None, "Boo"),
            LocationData('Astral Hall', 'Astral Hall Boo', None, "Boo"),
            LocationData('Breaker Room', 'Breaker Room Boo', None, "Boo"),
            LocationData('Cellar', 'Cellar Boo', None, "Boo"),
            LocationData('Pipe Room', 'Pipe Room Boo', None, "Boo"),
            LocationData('Cold Storage', 'Cold Storage Boo', None, "Boo")
        )
    return tuple(location_table)
