from typing import List, Tuple, Optional, Callable, NamedTuple, Union, Dict
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
        LocationData('Breaker Room', 'Breaker Room Clear Chest', 8543,
                     rule=lambda state: state.has("Breaker Key", player)),

        # Ghost Affected Clear Chests. Rules applied to region entrances
        LocationData('Wardrobe', 'Wardrobe Shelf Key', 8544),
        LocationData('Hidden Room', 'Hidden Room Clear Chest', 8545),
        LocationData('Mirror Room', 'Mirror Room Clear Chest', 8546),
        LocationData('Kitchen', 'Kitchen Clear Chest', 8547),
        LocationData('1F Bathroom', '1F Bathroom Shelf Key', 8548),
        LocationData('Courtyard', 'Courtyard Clear Chest', 8549),
        LocationData('Tea Room', 'Tea Room Clear Chest', 8550),
        LocationData('2F Washroom', '2F Washroom Clear Chest', 8551),
        LocationData('Projection Room', 'Projection Room Clear Chest', 8552),
        LocationData('Safari Room', 'Safari Room Clear Chest', 8553),
        LocationData('Cellar', 'Cellar Clear Chest', 8554),
        LocationData('Roof', 'Roof Clear Chest', 8555),
        LocationData('Sealed Room', 'Sealed Room Clear Chest', 8556),
        LocationData('Armory', 'Armory Clear Chest', 8557),
        LocationData('Pipe Room', 'Pipe Room Clear Chest', 8558,
                     rule=lambda state: state.has("Ice Element Medal", player)),

        # Game Event Locations
        LocationData('Balcony', 'Diamond Door', None, "Blackout", lambda state: state.has("Diamond Key", player)),
        LocationData('Storage Room', 'Storage Room Cage', None, "Boo Release"),
        # LocationData('Nursery', 'Chauncey',  None),
        # LocationData('Graveyard', 'Bogmire',  None),
        LocationData("Balcony", "Bolossus Boo 1", None, "Boo"),
        LocationData("Balcony", "Bolossus Boo 2", None, "Boo"),
        LocationData("Balcony", "Bolossus Boo 3", None, "Boo"),
        LocationData("Balcony", "Bolossus Boo 4", None, "Boo"),
        LocationData("Balcony", "Bolossus Boo 5", None, "Boo"),
        LocationData("Balcony", "Bolossus Boo 6", None, "Boo"),
        LocationData("Balcony", "Bolossus Boo 7", None, "Boo"),
        LocationData("Balcony", "Bolossus Boo 8", None, "Boo"),
        LocationData("Balcony", "Bolossus Boo 9", None, "Boo"),
        LocationData("Balcony", "Bolossus Boo 10", None, "Boo"),
        LocationData("Balcony", "Bolossus Boo 11", None, "Boo"),
        LocationData("Balcony", "Bolossus Boo 12", None, "Boo"),
        LocationData("Balcony", "Bolossus Boo 13", None, "Boo"),
        LocationData("Balcony", "Bolossus Boo 14", None, "Boo"),
        LocationData("Balcony", "Bolossus Boo 15", None, "Boo"),
        LocationData('Secret Altar', name="King Boo", code=None, locked_item="Mario's Painting", )
    ]

    # Adds all waterable plants as locations
    if not multiworld or is_option_enabled(multiworld, player, "Plantsanity"):
        location_table += (
            LocationData('Wardrobe Balcony', 'Wardrobe Balcony Plant 1', 8559,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Wardrobe Balcony', 'Wardrobe Balcony Plant 2', 8560,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Wardrobe Balcony', 'Wardrobe Balcony Plant 3', 8561,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Wardrobe Balcony', 'Wardrobe Balcony Plant 4', 8562,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Master Bedroom', 'Master Bedroom Plant', 8563,
                         rule=lambda state: state.has("Water Element Medal", player)),
            #   LocationData('Boneyard', 'Huge Flower', 8564,
            #               rule=lambda state: state.has("Water Element Medal", player) and state.has()),  need to determine how to make unskippable
            LocationData('Courtyard', 'Courtyard Fountain Plant 1', 8565,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Courtyard', 'Courtyard Fountain Plant 2', 8566,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Courtyard', 'Courtyard Fountain Plant 3', 8567,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Courtyard', 'Courtyard Fountain Plant 4', 8568,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Balcony', 'Balcony Plant 1', 8569,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Balcony', 'Balcony Plant 2', 8570,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Balcony', 'Balcony Plant 3', 8571,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Balcony', 'Balcony Plant 4', 8572,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Balcony', 'Balcony Plant 5', 8573,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Balcony', 'Balcony Plant 6', 8574,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Balcony', 'Balcony Plant 7', 8575,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Balcony', 'Balcony Plant 8', 8576,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Balcony', 'Balcony Plant 9', 8577,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Balcony', 'Balcony Plant 10', 8578,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Balcony', 'Balcony Plant 11', 8579,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Balcony', 'Balcony Plant 12', 8580,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Balcony', 'Balcony Plant 13', 8581,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Balcony', 'Balcony Plant 14', 8582,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Balcony', 'Balcony Plant 15', 8583,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Balcony', 'Balcony Plant 16', 8584,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Sitting Room', 'Sitting Room Plant', 8585,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Guest Room', 'Guest Room Plant', 8586,
                         rule=lambda state: state.has("Water Element Medal", player))
        )

    # Adds the myriad shackable objects as locations
    if not multiworld or is_option_enabled(multiworld, player, "Interactables"):
        location_table += (
            LocationData('Left Side forest Caves', 'Lake Serene: Cantoran', 8587),
        )
    # Adds Toads as locations
    if not multiworld or is_option_enabled(multiworld, player, "Toadsanity"):
        location_table += (
            LocationData('Foyer', 'Foyer Toad', 8650),
            LocationData('Wardrobe', 'Wardrobe Balcony Toad', 8651),
            LocationData('1F Washroom', '1F Washroom Toad', 8652),
            LocationData('Courtyard', 'Courtyard Toad', 8653)
        )

    # Adds Portrait Ghosts as locations
    if not multiworld or is_option_enabled(multiworld, player, "PortraitGhosts"):
        location_table += (
            LocationData('Study', 'Neville, the Bookish Father', 8654),
            LocationData('Master Bedroom', 'Lydia, the Mirror-Gazing Mother', 8655),
            LocationData('Nursery', 'Chauncey, the Spoiled Baby', 8656),
            LocationData('Twins\' Room', 'Henry and Orville, the Twin Brothers', 8657,
                         rule=lambda state: state.has_group("Medal", player)),
            LocationData('Ballroom', 'The Floating Whirlindas, the Dancing Couple', 8658),
            LocationData('Butler\'s Room', 'Shivers, the Wandering Butler', 8659,
                         rule=lambda state: state.has("Fire Element Medal", player)),
            LocationData('Fortune-Teller\'s Room', 'Madame Clairvoya, the Freaky Fortune-Teller', 8660,
                         rule=lambda state: state.has_group("Mario Item", player, multiworld.MarioItems[player])),
            LocationData('Conservatory', ' Melody Pianissima, the Beautiful Pianist', 8661),
            LocationData('Dining Room', 'Mr. Luggs, the Glutton', 8662,
                         rule=lambda state: state.has("Fire Element Medal", player)),
            LocationData('Boneyard', 'Spooky, the Guard Dog', 8663,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Graveyard', 'Bogmire, the Cemetary Shadow', 8664),
            LocationData('Rec Room', 'Biff Atlas, the Bodybuilder', 8665),
            LocationData('Billiards Room', 'Slim Bankshot, the Lonely Poolshark', 8666),
            LocationData('2F Bathroom', 'Miss Petunia, the Bathing Beauty', 8667,
                         rule=lambda state: state.has("Ice Element Medal", player)),
            LocationData('Nana\'s Room', 'Nana, the Scarf-Knitting Granny', 8668),
            LocationData('Guest Room', 'Sue Pea, the Dozing Girl', 8669,
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Wardrobe', 'Uncle Grimmly, Hermit of the Darkness', 8670,
                         rule=lambda state: state.has("Blackout", player)),
            LocationData('Balcony', 'Boolossus, the Jumbo Ghost', 8670,
                         rule=lambda state: state.has("Ice Element Medal", player)),
            LocationData('Ceramics Studio', 'Jarvis, the Jar Collector', 8671,
                         rule=lambda state: state.has("Ice Element Medal", player)),
            LocationData('Clockwork Room', 'Clockwork Soldiers, the Toy Platoon', 8672),
            LocationData('Artist\'s Studio', 'Vincent van Gore, the Starving Artist', 8673),
            LocationData('Cold Storage', 'Sir Weston, the Chilly Climber', 8674,
                         rule=lambda state: state.has("Fire Element Medal", player))
        )

    # Adds Blue Ghosts and Gold Mice as locations
    if not multiworld or is_option_enabled(multiworld, player, "SpeedySpirits"):
        location_table += (
            LocationData('Lower lake desolation', 'Lake Desolation: Memory - Coyote Jump (Time Messenger)', 8675),
            LocationData('Library', 'Library: Memory - Waterway (A Message)', 8676),
            LocationData('Library top', 'Library: Memory - Library Gap (Lachiemi Sun)', 8677),
            LocationData('Library top', 'Library: Memory - Mr. Hat Portrait (Moonlit Night)', 8678),
            LocationData('Varndagroth tower left', 'Varndagroth Towers (Left): Memory - Elevator (Nomads)', 8679,
                         lambda state: state.has('Elevator Keycard', player)),
            LocationData('Varndagroth tower right (lower)', 'Varndagroth Towers: Memory - Siren Elevator (Childhood)',
                         8680, lambda state: state._timespinner_has_keycard_B(multiworld, player)),
            LocationData('Varndagroth tower right (lower)', 'Varndagroth Towers (Right): Memory - Bottom (Faron)',
                         8731),
            LocationData('Military Fortress', 'Military Fortress: Memory - Bomber Climb (A Solution)', 8681,
                         lambda state: state.has('Timespinner Wheel',
                                                 player) and state._timespinner_has_doublejump_of_npc(multiworld,
                                                                                                      player)),
            LocationData('The lab', 'Lab: Memory - Genza\'s Secret Stash 1 (An Old Friend)', 8682,
                         lambda state: state._timespinner_can_break_walls(multiworld, player)),
            LocationData('The lab', 'Lab: Memory - Genza\'s Secret Stash 2 (Twilight Dinner)', 8683,
                         lambda state: state._timespinner_can_break_walls(multiworld, player)),
            LocationData('Emperors tower', 'Emperor\'s Tower: Memory - Way Up There (Final Circle)', 8684,
                         lambda state: state._timespinner_has_doublejump_of_npc(multiworld, player)),
            LocationData('Forest', 'Forest: Journal - Rats (Lachiem Expedition)', 8685),
            LocationData('Forest', 'Forest: Journal - Bat Jump Ledge (Peace Treaty)', 8686,
                         lambda state: state._timespinner_has_doublejump_of_npc(multiworld,
                                                                                player) or state._timespinner_has_forwarddash_doublejump(
                             multiworld, player) or state._timespinner_has_fastjump_on_npc(multiworld, player)),
            LocationData('Castle Ramparts', 'Castle Ramparts: Journal - Floating in Moat (Prime Edicts)', 8687),
            LocationData('Castle Ramparts', 'Castle Ramparts: Journal - Archer + Knight (Declaration of Independence)',
                         8688),
            LocationData('Castle Keep', 'Castle Keep: Journal - Under the Twins (Letter of Reference)', 8689),
            LocationData('Castle Keep', 'Castle Keep: Journal - Castle Loop Giantess (Political Advice)', 8690),
            LocationData('Royal towers (lower)', 'Royal Towers: Journal - Aelana\'s Room (Diplomatic Missive)', 8691,
                         lambda state: state._timespinner_has_pink(multiworld, player)),
            LocationData('Royal towers (upper)',
                         'Royal Towers: Journal - Top Struggle Juggle Base (War of the Sisters)',
                         8692),
            LocationData('Royal towers (upper)', 'Royal Towers: Journal - Aelana Boss (Stained Letter)', 8693),
            LocationData('Royal towers', 'Royal Towers: Journal - Near Bottom Struggle Juggle (Mission Findings)',
                         8694, lambda state: state._timespinner_has_doublejump_of_npc(multiworld, player)),
            LocationData('Caves of Banishment (Maw)', 'Caves of Banishment (Maw): Journal - Lower Left Caves (Naivety)',
                         8695)
        )

    # 1337199 - 1337236 Reserved for future use

    # Turns Boos into check locations and adds Boos as items
    if not multiworld or is_option_enabled(multiworld, player, "Boosanity"):
        location_table += (
            LocationData('Parlor', 'Parlor Boo', 8696, rule=lambda state: state.has("Boo Radar", player)),
            LocationData('Anteroom', 'Anteroom Boo', 8697, rule=lambda state: state.has("Boo Radar", player)),
            LocationData('Wardrobe', 'Wardrobe Boo', 8698, rule=lambda state: state.has("Boo Radar", player)),
            LocationData('Study', 'Study Boo', 8699, rule=lambda state: state.has("Boo Radar", player)),
            LocationData('Master Bedroom', 'Master Bedroom Boo', 8700,
                         rule=lambda state: state.has("Boo Radar", player)),
            LocationData('Nursery', 'Nursery Boo', 8701, rule=lambda state: state.has("Boo Radar", player)),
            LocationData('Twins\' Room', 'Twins\' Room Boo', 8702,
                         rule=lambda state: state.has_group("Medal", player) and state.has("Boo Radar", player)),
            LocationData('Laundry Room', 'Laundry Room Boo', 8703, rule=lambda state: state.has("Boo Radar", player)),
            LocationData('Butler\'s Room', 'Butler\'s Room Boo', 8704,
                         rule=lambda state: state.has("Fire Element Medal", player) and state.has("Boo Release", player)
                                            and state.has("Boo Radar", player)),
            LocationData('Hidden Room', 'Hidden Room Boo', 8705, rule=lambda state: state.has("Boo Radar", player)),
            LocationData('Fortune-Teller\'s Room', 'Fortune-Teller\'s Room Boo', 8706,
                         rule=lambda state: state.has_group("Mario Item", player, multiworld.MarioItems[player])
                         and state.has("Boo Radar", player)),
            LocationData('Mirror Room', 'Mirror Room Boo', 8707, rule=lambda state: state.has("Boo Radar", player)),
            LocationData('Ballroom', 'Ballroom Boo', 8708, rule=lambda state: state.has("Boo Radar", player)),
            LocationData('Storage Room', 'Storage Room Boo', 8709, rule=lambda state: state.has("Boo Radar", player)),
            LocationData('Dining Room', 'Dining Room Boo', 8710,
                         rule=lambda state: state.has("Fire Element Medal", player) and state.has("Boo Radar", player)),
            LocationData('Kitchen', 'Kitchen Boo', 8711, rule=lambda state: state.has("Boo Radar", player)),
            LocationData('Conservatory', 'Conservatory Boo', 8712, rule=lambda state: state.has("Boo Radar", player)),
            LocationData('Rec Room', 'Rec Room Boo', 8713, rule=lambda state: state.has("Boo Radar", player)),
            LocationData('Billiards Room', 'Billiards Room Boo', 8714, rule=lambda state: state.has("Boo Radar", player)),
            LocationData('Projection Room', 'Projection Room Boo', 8715,
                         rule=lambda state: state.has("Boo Radar", player)),
            LocationData('Tea Room', 'Tea Room Boo', 8716, rule=lambda state: state.has("Boo Radar", player)),
            LocationData('Nana\'s Room', 'Nana\'s Room Boo', 8717, rule=lambda state: state.has("Boo Radar", player)),
            LocationData('Sitting Room', 'Sitting Room Boo', 8718,
                         rule=lambda state: state.has("Fire Element Medal", player)
                                            and state.has("Water Element Medal", player)
                                            and state.has("Boo Radar", player)
                         ),
            LocationData('Guest Room', 'Guest Room Boo', 8719,
                         rule=lambda state: state.has("Water Element Medal", player) and state.has("Boo Radar", player)),
            LocationData('Safari Room', 'Safari Room Boo', 8720, rule=lambda state: state.has("Boo Radar", player)),
            LocationData('Artist\'s Studio', 'Artist\'s Studio Boo', 8721,
                         rule=lambda state: state.has("Boo Radar", player)),
            LocationData('Armory', 'Armory Boo', 8722, rule=lambda state: state.has("Boo Radar", player)),
            LocationData('Ceramics Studio', 'Ceramics Studio Boo', 8723,
                         rule=lambda state: state.has("Ice Element Medal", player)
                                            and state.has("Boo Radar", player)),
            LocationData('Telephone Room', 'Telephone Room Boo', 8724, rule=lambda state: state.has("Boo Radar", player)),
            LocationData('Clockwork Room', 'Clockwork Room Boo', 8725, rule=lambda state: state.has("Boo Radar", player)),
            LocationData('Astral Hall', 'Astral Hall Boo', 8726,
                         rule=lambda state: state.has("Fire Element Medal", player)
                                            and state.has("Boo Radar", player)),
            LocationData('Breaker Room', 'Breaker Room Boo', 8727,
                         rule=lambda state: state.has("Blackout", player) and state.has("Boo Radar", player)),
            LocationData('Cellar', 'Cellar Boo', 8728, rule=lambda state: state.has("Boo Radar", player)),
            LocationData('Pipe Room', 'Pipe Room Boo', 8729, rule=lambda state: state.has("Boo Radar", player)),
            LocationData('Cold Storage', 'Cold Storage Boo', 8730,
                         rule=lambda state: state.has("Fire Element Medal", player)
                                            and state.has("Boo Radar", player))

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
            LocationData('Twins\' Room', 'Twins\' Room Boo', None, "Boo",
                         rule=lambda state: state.has_group("Medal", player)),
            LocationData('Laundry Room', 'Laundry Room Boo', None, "Boo"),
            LocationData('Butler\'s Room', 'Butler\'s Room Boo', None, "Boo",
                         rule=lambda state: state.has("Fire Element Medal", player) and state.has("Boo Release",
                                                                                                  player)),
            LocationData('Hidden Room', 'Hidden Room Boo', None, "Boo"),
            LocationData('Fortune-Teller\'s Room', 'Fortune-Teller\'s Room Boo', None, "Boo",
                         rule=lambda state: state.has_group("Mario Item", player, multiworld.MarioItems[player])),
            LocationData('Mirror Room', 'Mirror Room Boo', None, "Boo"),
            LocationData('Ballroom', 'Ballroom Boo', None, "Boo"),
            LocationData('Storage Room', 'Storage Room Boo', None, "Boo"),
            LocationData('Dining Room', 'Dining Room Boo', None, "Boo",
                         rule=lambda state: state.has("Fire Element Medal", player)),
            LocationData('Kitchen', 'Kitchen Boo', None, "Boo"),
            LocationData('Conservatory', 'Conservatory Boo', None, "Boo"),
            LocationData('Rec Room', 'Rec Room Boo', None, "Boo"),
            LocationData('Billiards Room', 'Billiards Room Boo', None, "Boo"),
            LocationData('Projection Room', 'Projection Room Boo', None, "Boo"),
            LocationData('Tea Room', 'Tea Room Boo', None, "Boo"),
            LocationData('Nana\'s Room', 'Nana\'s Room Boo', None, "Boo"),
            LocationData('Sitting Room', 'Sitting Room Boo', None, "Boo",
                         rule=lambda state: state.has("Fire Element Medal", player) and state.has("Water Element Medal",
                                                                                                  player)),
            LocationData('Guest Room', 'Guest Room Boo', None, "Boo",
                         rule=lambda state: state.has("Water Element Medal", player)),
            LocationData('Safari Room', 'Safari Room Boo', None, "Boo"),
            LocationData('Artist\'s Studio', 'Artist\'s Studio Boo', None, "Boo"),
            LocationData('Armory', 'Armory Boo', None, "Boo"),
            LocationData('Ceramics Studio', 'Ceramics Studio Boo', None, "Boo",
                         rule=lambda state: state.has("Ice Element Medal", player)),
            LocationData('Telephone Room', 'Telephone Room Boo', None, "Boo"),
            LocationData('Clockwork Room', 'Clockwork Room Boo', None, "Boo"),
            LocationData('Astral Hall', 'Astral Hall Boo', None, "Boo",
                         rule=lambda state: state.has("Fire Element Medal", player)),
            LocationData('Breaker Room', 'Breaker Room Boo', None, "Boo",
                         rule=lambda state: state.has("Blackout", player)),
            LocationData('Cellar', 'Cellar Boo', None, "Boo"),
            LocationData('Pipe Room', 'Pipe Room Boo', None, "Boo"),
            LocationData('Cold Storage', 'Cold Storage Boo', None, "Boo",
                         lambda state: state.has("Fire Element Medal", player))
        )
    return tuple(location_table)


def is_option_enabled(world: MultiWorld, player: int, name: str) -> bool:
    return get_option_value(world, player, name) > 0


def get_option_value(world: MultiWorld, player: int, name: str) -> Union[int, Dict, List]:
    option = getattr(world, name, None)
    if option == None:
        return 0

    return option[player].value
