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
                     lambda state: state.has("Mario Item", player, multiworld.MarioItems[player])),
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

        # Game Event Locations
        LocationData('Balcony', 'Boolossus', None,
                     lambda state: state.has("Ice Element Medal", player)),
        LocationData('Storage Room', 'Storage Room Cage', None),
        # LocationData('Nursery', 'Chauncey',  None),
        # LocationData('Graveyard', 'Bogmire',  None),

        # Past item locations
        LMLocation('Refugee Camp', 'Refugee Camp: Neliste\'s Bra', 1337086),
        LMLocation('Refugee Camp', 'Refugee Camp: Storage chest 3', 1337087),
        LMLocation('Refugee Camp', 'Refugee Camp: Storage chest 2', 1337088),
        LMLocation('Refugee Camp', 'Refugee Camp: Storage chest 1', 1337089),
        LMLocation('Forest', 'Forest: Refugee camp roof', 1337090),
        LMLocation('Forest', 'Forest: Bat jump ledge', 1337091,
                   lambda state: state._timespinner_has_doublejump_of_npc(world,
                                                                          player) or state._timespinner_has_forwarddash_doublejump(
                       world, player) or state._timespinner_has_fastjump_on_npc(world, player)),
        LMLocation('Forest', 'Forest: Green platform secret', 1337092,
                   lambda state: state._timespinner_can_break_walls(world, player)),
        LMLocation('Forest', 'Forest: Rats guarded chest', 1337093),
        LMLocation('Forest', 'Forest: Waterfall chest 1', 1337094, lambda state: state.has('Water Mask', player)),
        LMLocation('Forest', 'Forest: Waterfall chest 2', 1337095, lambda state: state.has('Water Mask', player)),
        LMLocation('Forest', 'Forest: Batcave', 1337096),
        LMLocation('Forest', 'Castle Ramparts: In the moat', 1337097),
        LMLocation('Left Side forest Caves', 'Forest: Before Serene single bat cave', 1337098),
        LMLocation('Upper Lake Serene', 'Lake Serene (Upper): Rat nest', 1337099),
        LMLocation('Upper Lake Serene', 'Lake Serene (Upper): Double jump cave platform', 1337100,
                   lambda state: state._timespinner_has_doublejump(world, player)),
        LMLocation('Upper Lake Serene', 'Lake Serene (Upper): Double jump cave floor', 1337101),
        LMLocation('Upper Lake Serene', 'Lake Serene (Upper): Cave secret', 1337102,
                   lambda state: state._timespinner_can_break_walls(world, player)),
        LMLocation('Upper Lake Serene', 'Lake Serene: Before Big Bird', 1337175),
        LMLocation('Upper Lake Serene', 'Lake Serene: Behind the vines', 1337103),
        LMLocation('Upper Lake Serene', 'Lake Serene: Pyramid keys room', 1337104),
        LMLocation('Upper Lake Serene', 'Lake Serene (Upper): Chicken ledge', 1337174),
        LMLocation('Lower Lake Serene', 'Lake Serene (Lower): Deep dive', 1337105),
        LMLocation('Lower Lake Serene', 'Lake Serene (Lower): Under the eels', 1337106),
        LMLocation('Lower Lake Serene', 'Lake Serene (Lower): Water spikes room', 1337107),
        LMLocation('Lower Lake Serene', 'Lake Serene (Lower): Underwater secret', 1337108,
                   lambda state: state._timespinner_can_break_walls(world, player)),
        LMLocation('Lower Lake Serene', 'Lake Serene (Lower): T chest', 1337109),
        LMLocation('Lower Lake Serene', 'Lake Serene (Lower): Past the eels', 1337110),
        LMLocation('Lower Lake Serene', 'Lake Serene (Lower): Underwater pedestal', 1337111),
        LMLocation('Caves of Banishment (upper)', 'Caves of Banishment (Maw): Shroom jump room', 1337112,
                   lambda state: state._timespinner_has_doublejump(world, player)),
        LMLocation('Caves of Banishment (upper)', 'Caves of Banishment (Maw): Secret room', 1337113),
        LMLocation('Caves of Banishment (upper)', 'Caves of Banishment (Maw): Bottom left room', 1337114),
        LMLocation('Caves of Banishment (upper)', 'Caves of Banishment (Maw): Single shroom room', 1337115),
        LMLocation('Caves of Banishment (upper)', 'Caves of Banishment (Maw): Jackpot room chest 1', 1337116,
                   lambda state: state._timespinner_has_forwarddash_doublejump(world, player)),
        LMLocation('Caves of Banishment (upper)', 'Caves of Banishment (Maw): Jackpot room chest 2', 1337117,
                   lambda state: state._timespinner_has_forwarddash_doublejump(world, player)),
        LMLocation('Caves of Banishment (upper)', 'Caves of Banishment (Maw): Jackpot room chest 3', 1337118,
                   lambda state: state._timespinner_has_forwarddash_doublejump(world, player)),
        LMLocation('Caves of Banishment (upper)', 'Caves of Banishment (Maw): Jackpot room chest 4', 1337119,
                   lambda state: state._timespinner_has_forwarddash_doublejump(world, player)),
        LMLocation('Caves of Banishment (upper)', 'Caves of Banishment (Maw): Pedestal', 1337120),
        LMLocation('Caves of Banishment (Maw)', 'Caves of Banishment (Maw): Last chance before Maw', 1337121,
                   lambda state: state._timespinner_has_doublejump(world, player)),
        LMLocation('Caves of Banishment (Maw)', 'Caves of Banishment (Maw): Plasma Crystal', 1337173,
                   lambda state: state.has_any({'Gas Mask', 'Talaria Attachment'}, player)),
        LMLocation('Caves of Banishment (Maw)', 'Killed Maw', EventId, lambda state: state.has('Gas Mask', player)),
        LMLocation('Caves of Banishment (Maw)', 'Caves of Banishment (Maw): Mineshaft', 1337122,
                   lambda state: state.has('Gas Mask', player)),
        LMLocation('Caves of Banishment (Sirens)', 'Caves of Banishment (Sirens): Wyvern room', 1337123),
        LMLocation('Caves of Banishment (Sirens)', 'Caves of Banishment (Sirens): Siren room above water chest',
                   1337124),
        LMLocation('Caves of Banishment (Sirens)', 'Caves of Banishment (Sirens): Siren room underwater left chest',
                   1337125, lambda state: state.has('Water Mask', player)),
        LMLocation('Caves of Banishment (Sirens)', 'Caves of Banishment (Sirens): Siren room underwater right chest',
                   1337126, lambda state: state.has('Water Mask', player)),
        LMLocation('Caves of Banishment (Sirens)', 'Caves of Banishment (Sirens): Siren room underwater right ground',
                   1337172, lambda state: state.has('Water Mask', player)),
        LMLocation('Caves of Banishment (Sirens)', 'Caves of Banishment (Sirens): Water hook', 1337127,
                   lambda state: state.has('Water Mask', player)),
        LMLocation('Castle Ramparts', 'Castle Ramparts: Bomber chest', 1337128,
                   lambda state: state._timespinner_has_multiple_small_jumps_of_npc(world, player)),
        LMLocation('Castle Ramparts', 'Castle Ramparts: Freeze the engineer', 1337129,
                   lambda state: state.has('Talaria Attachment', player) or state._timespinner_has_timestop(world,
                                                                                                            player)),
        LMLocation('Castle Ramparts', 'Castle Ramparts: Giantess guarded room', 1337130),
        LMLocation('Castle Ramparts', 'Castle Ramparts: Knight and archer guarded room', 1337131),
        LMLocation('Castle Ramparts', 'Castle Ramparts: Pedestal', 1337132),
        LMLocation('Castle Keep', 'Castle Keep: Basement secret pedestal', 1337133,
                   lambda state: state._timespinner_can_break_walls(world, player)),
        LMLocation('Castle Keep', 'Castle Keep: Clean the castle basement', 1337134),
        LMLocation('Royal towers (lower)', 'Castle Keep: Yas queen room', 1337135,
                   lambda state: state._timespinner_has_pink(world, player)),
        LMLocation('Castle Keep', 'Castle Keep: Giantess guarded chest', 1337136),
        LMLocation('Castle Keep', 'Castle Keep: Omelette chest', 1337137),
        LMLocation('Castle Keep', 'Castle Keep: Just an egg', 1337138),
        LMLocation('Castle Keep', 'Castle Keep: Under the twins', 1337139),
        LMLocation('Castle Keep', 'Killed Twins', EventId,
                   lambda state: state._timespinner_has_timestop(world, player)),
        LMLocation('Castle Keep', 'Castle Keep: Advisor jump', 1337171,
                   lambda state: state._timespinner_has_timestop(world, player)),
        LMLocation('Castle Keep', 'Castle Keep: Twins', 1337140,
                   lambda state: state._timespinner_has_timestop(world, player)),
        LMLocation('Castle Keep', 'Castle Keep: Royal guard tiny room', 1337141,
                   lambda state: state._timespinner_has_doublejump(world,
                                                                   player) or state._timespinner_has_fastjump_on_npc(
                       world, player)),
        LMLocation('Royal towers (lower)', 'Royal Towers: Floor secret', 1337142,
                   lambda state: state._timespinner_has_doublejump(world,
                                                                   player) and state._timespinner_can_break_walls(world,
                                                                                                                  player)),
        LMLocation('Royal towers', 'Royal Towers: Pre-climb gap', 1337143),
        LMLocation('Royal towers', 'Royal Towers: Long balcony', 1337144),
        LMLocation('Royal towers (upper)', 'Royal Towers: Past bottom struggle juggle', 1337145),
        LMLocation('Royal towers (upper)', 'Royal Towers: Bottom struggle juggle', 1337146,
                   lambda state: state._timespinner_has_doublejump_of_npc(world, player)),
        LMLocation('Royal towers (upper)', 'Royal Towers: Top struggle juggle', 1337147,
                   lambda state: state._timespinner_has_doublejump_of_npc(world, player)),
        LMLocation('Royal towers (upper)', 'Royal Towers: No struggle required', 1337148,
                   lambda state: state._timespinner_has_doublejump_of_npc(world, player)),
        LMLocation('Royal towers', 'Royal Towers: Right tower freebie', 1337149),
        LMLocation('Royal towers (upper)', 'Royal Towers: Left tower small balcony', 1337150),
        LMLocation('Royal towers (upper)', 'Royal Towers: Left tower royal guard', 1337151),
        LMLocation('Royal towers (upper)', 'Royal Towers: Before Aelana', 1337152),
        LMLocation('Royal towers (upper)', 'Killed Aelana', EventId),
        LMLocation('Royal towers (upper)', 'Royal Towers: Aelana\'s attic', 1337153,
                   lambda state: state._timespinner_has_upwarddash(world, player)),
        LMLocation('Royal towers (upper)', 'Royal Towers: Aelana\'s chest', 1337154),
        LMLocation('Royal towers (upper)', 'Royal Towers: Aelana\'s pedestal', 1337155),

        # Ancient pyramid locations
        LMLocation('Ancient Pyramid (entrance)', 'Ancient Pyramid: Why not it\'s right there', 1337246),
        LMLocation('Ancient Pyramid (left)', 'Ancient Pyramid: Conviction guarded room', 1337247),
        LMLocation('Ancient Pyramid (left)', 'Ancient Pyramid: Pit secret room', 1337248,
                   lambda state: state._timespinner_can_break_walls(world, player)),
        LMLocation('Ancient Pyramid (left)', 'Ancient Pyramid: Regret chest', 1337249,
                   lambda state: state._timespinner_can_break_walls(world, player)),
        LMLocation('Ancient Pyramid (right)', 'Ancient Pyramid: Nightmare Door chest', 1337236),
        LMLocation('Ancient Pyramid (right)', 'Killed Nightmare', EventId, lambda state: state.has_all(
            {'Timespinner Wheel', 'Timespinner Spindle', 'Timespinner Gear 1', 'Timespinner Gear 2',
             'Timespinner Gear 3'}, player))
    ]

    # Adds all waterable plants as locations
    if not world or is_option_enabled(world, player, "Plants"):
        location_table += (
            LMLocation('Library', 'Library: Terminal 2 (Lachiem)', 1337156, lambda state: state.has('Tablet', player)),
            LMLocation('Library', 'Library: Terminal 1 (Windaria)', 1337157, lambda state: state.has('Tablet', player)),
            # 1337158 Is lost in time
            LMLocation('Library', 'Library: Terminal 3 (Emporer Nuvius)', 1337159,
                       lambda state: state.has('Tablet', player)),
            LMLocation('Library', 'Library: V terminal 1 (War of the Sisters)', 1337160,
                       lambda state: state.has_all({'Tablet', 'Library Keycard V'}, player)),
            LMLocation('Library', 'Library: V terminal 2 (Lake Desolation Map)', 1337161,
                       lambda state: state.has_all({'Tablet', 'Library Keycard V'}, player)),
            LMLocation('Library', 'Library: V terminal 3 (Vilete)', 1337162,
                       lambda state: state.has_all({'Tablet', 'Library Keycard V'}, player)),
            LMLocation('Library top', 'Library: Backer room terminal (Vandagray Metropolis Map)', 1337163,
                       lambda state: state.has('Tablet', player)),
            LMLocation('Varndagroth tower right (elevator)',
                       'Varndagroth Towers (Right): Medbay terminal (Bleakness Research)', 1337164,
                       lambda state: state.has('Tablet', player) and state._timespinner_has_keycard_B(world, player)),
            LMLocation('The lab (upper)', 'Lab: Download and chest room terminal (Experiment #13)', 1337165,
                       lambda state: state.has('Tablet', player)),
            LMLocation('The lab (power off)', 'Lab: Middle terminal (Amadeus Laboratory Map)', 1337166,
                       lambda state: state.has('Tablet', player)),
            LMLocation('The lab (power off)', 'Lab: Sentry platform terminal (Origins)', 1337167,
                       lambda state: state.has('Tablet', player)),
            LMLocation('The lab', 'Lab: Experiment 13 terminal (W.R.E.C Farewell)', 1337168,
                       lambda state: state.has('Tablet', player)),
            LMLocation('The lab', 'Lab: Left terminal (Biotechnology)', 1337169,
                       lambda state: state.has('Tablet', player)),
            LMLocation('The lab (power off)', 'Lab: Right terminal (Experiment #11)', 1337170,
                       lambda state: state.has('Tablet', player))
        )

    # Adds the myriad shackable objects as locations
    if not world or is_option_enabled(world, player, "Interactables"):
        location_table += (
            LMLocation('Left Side forest Caves', 'Lake Serene: Cantoran', 1337176),
        )
    # Adds Toads as locations
    if not world or is_option_enabled(world, player, "Toadsanity"):
        location_table += (
            LMLocation('Left Side forest Caves', 'Lake Serene: Cantoran', 1337176),
        )

    # Adds Portrait Ghosts as locations
    if not world or is_option_enabled(world, player, "Portrait Ghosts"):
        location_table += (
            LMLocation('Left Side forest Caves', 'Lake Serene: Cantoran', 1337176),
        )

    # Adds Blue Ghosts and Gold Mice as locations
    if not world or is_option_enabled(world, player, "Money Ghosts"):
        location_table += (
            LMLocation('Lower lake desolation', 'Lake Desolation: Memory - Coyote Jump (Time Messenger)', 1337177),
            LMLocation('Library', 'Library: Memory - Waterway (A Message)', 1337178),
            LMLocation('Library top', 'Library: Memory - Library Gap (Lachiemi Sun)', 1337179),
            LMLocation('Library top', 'Library: Memory - Mr. Hat Portrait (Moonlit Night)', 1337180),
            LMLocation('Varndagroth tower left', 'Varndagroth Towers (Left): Memory - Elevator (Nomads)', 1337181,
                       lambda state: state.has('Elevator Keycard', player)),
            LMLocation('Varndagroth tower right (lower)', 'Varndagroth Towers: Memory - Siren Elevator (Childhood)',
                       1337182, lambda state: state._timespinner_has_keycard_B(world, player)),
            LMLocation('Varndagroth tower right (lower)', 'Varndagroth Towers (Right): Memory - Bottom (Faron)',
                       1337183),
            LMLocation('Military Fortress', 'Military Fortress: Memory - Bomber Climb (A Solution)', 1337184,
                       lambda state: state.has('Timespinner Wheel',
                                               player) and state._timespinner_has_doublejump_of_npc(world, player)),
            LMLocation('The lab', 'Lab: Memory - Genza\'s Secret Stash 1 (An Old Friend)', 1337185,
                       lambda state: state._timespinner_can_break_walls(world, player)),
            LMLocation('The lab', 'Lab: Memory - Genza\'s Secret Stash 2 (Twilight Dinner)', 1337186,
                       lambda state: state._timespinner_can_break_walls(world, player)),
            LMLocation('Emperors tower', 'Emperor\'s Tower: Memory - Way Up There (Final Circle)', 1337187,
                       lambda state: state._timespinner_has_doublejump_of_npc(world, player)),
            LMLocation('Forest', 'Forest: Journal - Rats (Lachiem Expedition)', 1337188),
            LMLocation('Forest', 'Forest: Journal - Bat Jump Ledge (Peace Treaty)', 1337189,
                       lambda state: state._timespinner_has_doublejump_of_npc(world,
                                                                              player) or state._timespinner_has_forwarddash_doublejump(
                           world, player) or state._timespinner_has_fastjump_on_npc(world, player)),
            LMLocation('Castle Ramparts', 'Castle Ramparts: Journal - Floating in Moat (Prime Edicts)', 1337190),
            LMLocation('Castle Ramparts', 'Castle Ramparts: Journal - Archer + Knight (Declaration of Independence)',
                       1337191),
            LMLocation('Castle Keep', 'Castle Keep: Journal - Under the Twins (Letter of Reference)', 1337192),
            LMLocation('Castle Keep', 'Castle Keep: Journal - Castle Loop Giantess (Political Advice)', 1337193),
            LMLocation('Royal towers (lower)', 'Royal Towers: Journal - Aelana\'s Room (Diplomatic Missive)', 1337194,
                       lambda state: state._timespinner_has_pink(world, player)),
            LMLocation('Royal towers (upper)', 'Royal Towers: Journal - Top Struggle Juggle Base (War of the Sisters)',
                       1337195),
            LMLocation('Royal towers (upper)', 'Royal Towers: Journal - Aelana Boss (Stained Letter)', 1337196),
            LMLocation('Royal towers', 'Royal Towers: Journal - Near Bottom Struggle Juggle (Mission Findings)',
                       1337197, lambda state: state._timespinner_has_doublejump_of_npc(world, player)),
            LMLocation('Caves of Banishment (Maw)', 'Caves of Banishment (Maw): Journal - Lower Left Caves (Naivety)',
                       1337198)
        )

    # 1337199 - 1337236 Reserved for future use

    # Turns Boos into check locations and adds Boos as items
    if not world or is_option_enabled(world, player, "Boosanity"):
        location_table += (
            LMLocation('Ravenlord\'s Lair', 'Ravenlord: Post fight (pedestal)', 1337237),
            LMLocation('Ifrit\'s Lair', 'Ifrit: Post fight (pedestal)', 1337238),
            LMLocation('Temporal Gyre', 'Temporal Gyre: Chest 1', 1337239),
            LMLocation('Temporal Gyre', 'Temporal Gyre: Chest 2', 1337240),
            LMLocation('Temporal Gyre', 'Temporal Gyre: Chest 3', 1337241),
            LMLocation('Ravenlord\'s Lair', 'Ravenlord: Pre fight', 1337242),
            LMLocation('Ravenlord\'s Lair', 'Ravenlord: Post fight (chest)', 1337243),
            LMLocation('Ifrit\'s Lair', 'Ifrit: Pre fight', 1337244),
            LMLocation('Ifrit\'s Lair', 'Ifrit: Post fight (chest)', 1337245),
        )

    # Room Clear Chests Affected by Random Ghost types
    # if not world or is_option_enabled(world, player, "Enemizer"):
    #     location_table += (
    #         LMLocation('Left Side forest Caves', 'Lake Serene: Cantoran',  1337176),
    #     )

    return tuple(location_table)


starter_progression_locations: Tuple[str, ...] = (
    'Lake Desolation: Starter chest 2',
    'Lake Desolation: Starter chest 3',
    'Lake Desolation: Starter chest 1',
    'Lake Desolation (Lower): Timespinner Wheel room'
)
