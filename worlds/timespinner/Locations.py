from typing import List, Tuple, Optional, Callable, NamedTuple
from BaseClasses import MultiWorld
from .Options import is_option_enabled

EventId: Optional[int] = None


class LocationData(NamedTuple):
    region: str
    name: str
    code: Optional[int]
    rule: Callable = lambda state: True


def get_locations(world: Optional[MultiWorld], player: Optional[int]) -> Tuple[LocationData, ...]:
    # 1337000 - 1337155 Generic locations
    # 1337171 - 1337175 New Pickup checks
    # 1337246 - 1337249 Ancient Pyramid
    location_table: List[LocationData] = [
        # Present item locations
        LocationData('Tutorial', 'Yo Momma 1',  1337000),
        LocationData('Tutorial', 'Yo Momma 2',  1337001),
        LocationData('Lake desolation', 'Starter chest 2',  1337002),
        LocationData('Lake desolation', 'Starter chest 3',  1337003),
        LocationData('Lake desolation', 'Starter chest 1',  1337004),
        LocationData('Lake desolation', 'Timespinner Wheel room',  1337005),
        LocationData('Lake desolation', 'Forget me not chest',  1337006, lambda state: state._timespinner_has_fire(world, player) and state.can_reach('Upper Lake Serene', 'Region', player)),
        LocationData('Lake desolation', 'Chicken chest', 1337007, lambda state: state._timespinner_has_timestop(world, player)),
        LocationData('Lower lake desolation', 'Not so secret room',  1337008, lambda state: state._timespinner_can_break_walls(world, player)),
        LocationData('Lower lake desolation', 'Tank chest',  1337009, lambda state: state._timespinner_has_timestop(world, player)),
        LocationData('Upper lake desolation', 'Upper desolation Oxygen recovery room',  1337010),
        LocationData('Upper lake desolation', 'Upper desolation secret',  1337011, lambda state: state._timespinner_can_break_walls(world, player)),
        LocationData('Upper lake desolation', 'Upper desolation double jump cave platform',  1337012, lambda state: state._timespinner_has_doublejump(world, player)),
        LocationData('Upper lake desolation', 'Upper desolation double jump cave floor',  1337013),
        LocationData('Upper lake desolation', 'Upper desolation sparrow chest',  1337014),
        LocationData('Upper lake desolation', 'Crash site pedestal',  1337015),
        LocationData('Upper lake desolation', 'Crash site chest 1',  1337016, lambda state: state.has_all({'Killed Maw'}, player)),
        LocationData('Upper lake desolation', 'Crash site chest 2',  1337017, lambda state: state.has_all({'Killed Maw'}, player)),
        LocationData('Eastern lake desolation', 'Kitty Boss',  1337018),
        LocationData('Library', 'Library Basement',  1337019),
        LocationData('Library', 'Library warp gate',  1337020),
        LocationData('Library', 'Librarian',  1337021),
        LocationData('Library', 'Reading nook chest',  1337022),
        LocationData('Library', 'Storage room chest 1',  1337023, lambda state: state._timespinner_has_keycard_D(world, player)),
        LocationData('Library', 'Storage room chest 2',  1337024, lambda state: state._timespinner_has_keycard_D(world, player)),
        LocationData('Library', 'Storage room chest 3',  1337025, lambda state: state._timespinner_has_keycard_D(world, player)),
        LocationData('Library top', 'Backer room chest 5',  1337026),
        LocationData('Library top', 'Backer room chest 4',  1337027),
        LocationData('Library top', 'Backer room chest 3',  1337028),
        LocationData('Library top', 'Backer room chest 2',  1337029),
        LocationData('Library top', 'Backer room chest 1',  1337030),
        LocationData('Varndagroth tower left', 'Elevator Key not required',  1337031),
        LocationData('Varndagroth tower left', 'Ye olde Timespinner',  1337032),
        LocationData('Varndagroth tower left', 'Varndagroth left bottom floor',  1337033, lambda state: state._timespinner_has_keycard_C(world, player)),
        LocationData('Varndagroth tower left', 'Left air vents secret',  1337034, lambda state: state._timespinner_can_break_walls(world, player)),
        LocationData('Varndagroth tower left', 'Left elevator chest',  1337035, lambda state: state.has('Elevator Keycard', player)),
        LocationData('Varndagroth tower right (upper)', 'Varndagroth bridge',  1337036),
        LocationData('Varndagroth tower right (elevator)', 'Right Varndagroth elevator chest',  1337037),
        LocationData('Varndagroth tower right (upper)', 'Elevator card chest',  1337038, lambda state: state.has('Elevator Keycard', player) or state._timespinner_has_doublejump(world, player)),
        LocationData('Varndagroth tower right (upper)', 'Air vents right',  1337039, lambda state: state.has('Elevator Keycard', player) or state._timespinner_has_doublejump(world, player)),
        LocationData('Varndagroth tower right (upper)', 'Air Vents left',  1337040, lambda state: state.has('Elevator Keycard', player) or state._timespinner_has_doublejump(world, player)),
        LocationData('Varndagroth tower right (lower)', 'Varndagroth right bottom floor',  1337041),
        LocationData('Varndagroth tower right (elevator)', 'Varndagroth',  1337042, lambda state: state._timespinner_has_keycard_C(world, player)),
        LocationData('Varndagroth tower right (elevator)', 'Varndagroth Spider hell',  1337043, lambda state: state._timespinner_has_keycard_A(world, player)),
        LocationData('Skeleton Shaft', 'Skeleton',  1337044),
        LocationData('Sealed Caves (Xarion)', 'Sealed cave shroom jump room',  1337045, lambda state: state._timespinner_has_timestop(world, player)),
        LocationData('Sealed Caves (Xarion)', 'Sealed cave double shroom room',  1337046),
        LocationData('Sealed Caves (Xarion)', 'Sealed cave Mini jackpot room',  1337047, lambda state: state._timespinner_has_forwarddash_doublejump(world, player)),
        LocationData('Sealed Caves (Xarion)', 'Below sealed cave mini jackpot room',  1337048),
        LocationData('Sealed Caves (Xarion)', 'Sealed cave secret room',  1337049, lambda state: state._timespinner_can_break_walls(world, player)),
        LocationData('Sealed Caves (Xarion)', 'Sealed cave bottom left',  1337050),
        LocationData('Sealed Caves (Xarion)', 'Last chance before Xarion',  1337051, lambda state: state._timespinner_has_doublejump(world, player)),
        LocationData('Sealed Caves (Xarion)', 'Xarion',  1337052),
        LocationData('Sealed Caves (Sirens)', 'Upper sealed cave water hook',  1337053, lambda state: state.has('Water Mask', player)),
        LocationData('Sealed Caves (Sirens)', 'Upper sealed cave siren room right',  1337054, lambda state: state.has('Water Mask', player)),
        LocationData('Sealed Caves (Sirens)', 'Upper sealed cave siren room left',  1337055, lambda state: state.has('Water Mask', player)),
        LocationData('Sealed Caves (Sirens)', 'Upper sealed cave after sirens chest 1',  1337056),
        LocationData('Sealed Caves (Sirens)', 'Upper sealed cave after sirens chest 2',  1337057),
        LocationData('Military Fortress', 'Military bomber chest',  1337058, lambda state: state.has('Timespinner Wheel', player) and state._timespinner_has_doublejump_of_npc(world, player)),
        LocationData('Military Fortress', 'Close combat room',  1337059),
        LocationData('Military Fortress (hangar)', 'Military soldiers bridge',  1337060),
        LocationData('Military Fortress (hangar)', 'Military giantess room',  1337061),
        LocationData('Military Fortress (hangar)', 'Military giantess bridge',  1337062),
        LocationData('Military Fortress (hangar)', 'Military B door chest 2',  1337063, lambda state: state._timespinner_has_doublejump(world, player) and state._timespinner_has_keycard_B(world, player)),
        LocationData('Military Fortress (hangar)', 'Military B door chest 1',  1337064, lambda state: state._timespinner_has_doublejump(world, player) and state._timespinner_has_keycard_B(world, player)),
        LocationData('Military Fortress (hangar)', 'Military pedestal',  1337065, lambda state: state._timespinner_has_doublejump_of_npc(world, player) or state._timespinner_has_forwarddash_doublejump(world, player)),
        LocationData('The lab', 'Coffee break',  1337066),
        LocationData('The lab', 'Lower trash right',  1337067, lambda state: state._timespinner_has_doublejump(world, player)),
        LocationData('The lab', 'Lower trash left',  1337068, lambda state: state._timespinner_has_upwarddash(world, player)),
        LocationData('The lab', 'Below lab entrance',  1337069, lambda state: state._timespinner_has_doublejump(world, player)),
        LocationData('The lab (power off)', 'Trash jump room',  1337070),
        LocationData('The lab (power off)', 'Dynamo Works',  1337071),
        LocationData('The lab (upper)', 'Blob mom',  1337072),
        LocationData('The lab (power off)', 'Experiment #13',  1337073),
        LocationData('The lab (upper)', 'Download and chest room',  1337074),
        LocationData('The lab (upper)', 'Lab secret',  1337075, lambda state: state._timespinner_can_break_walls(world, player)),
        LocationData('The lab (power off)', 'Lab Spider hell',  1337076, lambda state: state._timespinner_has_keycard_A(world, player)),
        LocationData('Emperors tower', 'Dad\'s bottom',  1337077),
        LocationData('Emperors tower', 'Dad\'s courtyard floor secret',  1337078, lambda state: state._timespinner_has_upwarddash(world, player) and state._timespinner_can_break_walls(world, player)),
        LocationData('Emperors tower', 'Dad\'s courtyard chest',  1337079, lambda state: state._timespinner_has_upwarddash(world, player)),
        LocationData('Emperors tower', 'Galactic sage room',  1337080),
        LocationData('Emperors tower', 'Bottom of Dad\'s right tower',  1337081),
        LocationData('Emperors tower', 'Wayyyy up there',  1337082, lambda state: state._timespinner_has_doublejump_of_npc(world, player)),
        LocationData('Emperors tower', 'Dad\'s left tower balcony',  1337083),
        LocationData('Emperors tower', 'Dad\'s Chambers chest',  1337084),
        LocationData('Emperors tower', 'Dad\'s Chambers pedestal',  1337085),

        # Past item locations
        LocationData('Refugee Camp', 'Neliste\'s Bra',  1337086),
        LocationData('Refugee Camp', 'Refugee camp storage chest 3',  1337087),
        LocationData('Refugee Camp', 'Refugee camp storage chest 2',  1337088),
        LocationData('Refugee Camp', 'Refugee camp storage chest 1',  1337089),
        LocationData('Forest', 'Refugee camp roof',  1337090),
        LocationData('Forest', 'Forest bat jump ledge',  1337091, lambda state: state._timespinner_has_doublejump_of_npc(world, player) or state._timespinner_has_forwarddash_doublejump(world, player) or state._timespinner_has_fastjump_on_npc(world, player)),
        LocationData('Forest', 'Forest green platform secret',  1337092, lambda state: state._timespinner_can_break_walls(world, player)),
        LocationData('Forest', 'Forest rats guarded chest',  1337093),
        LocationData('Forest', 'Waterfall chest 1',  1337094, lambda state: state.has('Water Mask', player)),
        LocationData('Forest', 'Waterfall chest 2',  1337095, lambda state: state.has('Water Mask', player)),
        LocationData('Forest', 'Forest batcave',  1337096),
        LocationData('Forest', 'In the moat',  1337097),
        LocationData('Left Side forest Caves', 'Before Serene single bat cave',  1337098),
        LocationData('Upper Lake Serene', 'Upper Serene rat nest',  1337099),
        LocationData('Upper Lake Serene', 'Upper Serene double jump cave platform',  1337100, lambda state: state._timespinner_has_doublejump(world, player)),
        LocationData('Upper Lake Serene', 'Upper Serene double jump cave floor',  1337101),
        LocationData('Upper Lake Serene', 'Upper Serene cave secret',  1337102, lambda state: state._timespinner_can_break_walls(world, player)),
        LocationData('Upper Lake Serene', 'Before Big Bird', 1337175),
        LocationData('Upper Lake Serene', 'Serene behind the vines',  1337103),
        LocationData('Upper Lake Serene', 'Pyramid keys room',  1337104),
        LocationData('Upper Lake Serene', 'Chicken ledge', 1337174),
        LocationData('Lower Lake Serene', 'Deep dive',  1337105),
        LocationData('Lower Lake Serene', 'Under the eels',  1337106),
        LocationData('Lower Lake Serene', 'Water spikes room',  1337107),
        LocationData('Lower Lake Serene', 'Underwater secret',  1337108, lambda state: state._timespinner_can_break_walls(world, player)),
        LocationData('Lower Lake Serene', 'T chest',  1337109),
        LocationData('Lower Lake Serene', 'Past the eels',  1337110),
        LocationData('Lower Lake Serene', 'Underwater pedestal',  1337111),
        LocationData('Caves of Banishment (upper)', 'Banishment shroom jump room',  1337112, lambda state: state._timespinner_has_doublejump(world, player)),
        LocationData('Caves of Banishment (upper)', 'Banishment secret room',  1337113),
        LocationData('Caves of Banishment (upper)', 'Banishment bottom left',  1337114),
        LocationData('Caves of Banishment (upper)', 'Banishment single shroom room',  1337115),
        LocationData('Caves of Banishment (upper)', 'Banishment jackpot room chest 1',  1337116, lambda state: state._timespinner_has_forwarddash_doublejump(world, player)),
        LocationData('Caves of Banishment (upper)', 'Banishment jackpot room chest 2',  1337117, lambda state: state._timespinner_has_forwarddash_doublejump(world, player)),
        LocationData('Caves of Banishment (upper)', 'Banishment jackpot room chest 3',  1337118, lambda state: state._timespinner_has_forwarddash_doublejump(world, player)),
        LocationData('Caves of Banishment (upper)', 'Banishment jackpot room chest 4',  1337119, lambda state: state._timespinner_has_forwarddash_doublejump(world, player)),
        LocationData('Caves of Banishment (upper)', 'Banishment pedestal',  1337120),
        LocationData('Caves of Banishment (Maw)', 'Last chance before Maw',  1337121, lambda state: state._timespinner_has_doublejump(world, player)),
        LocationData('Caves of Banishment (Maw)', 'Plasma Crystal', 1337173, lambda state: state.has_any({'Gas Mask', 'Talaria Attachment'}, player)),
        LocationData('Caves of Banishment (Maw)', 'Killed Maw',  EventId, lambda state: state.has('Gas Mask', player)),
        LocationData('Caves of Banishment (Maw)', 'Mineshaft',  1337122, lambda state: state.has('Gas Mask', player)),
        LocationData('Caves of Banishment (Sirens)', 'Wyvern room',  1337123),
        LocationData('Caves of Banishment (Sirens)', 'Upper banishment above sirens',  1337124),
        LocationData('Caves of Banishment (Sirens)', 'Under banishment sirens left',  1337125, lambda state: state.has('Water Mask', player)),
        LocationData('Caves of Banishment (Sirens)', 'Under banishment sirens right',  1337126, lambda state: state.has('Water Mask', player)),
        LocationData('Caves of Banishment (Sirens)', 'Underwater banishment sirens right ground', 1337172, lambda state: state.has('Water Mask', player)),
        LocationData('Caves of Banishment (Sirens)', 'Banishment water hook',  1337127, lambda state: state.has('Water Mask', player)),
        LocationData('Castle Ramparts', 'Castle bomber chest',  1337128, lambda state: state._timespinner_has_multiple_small_jumps_of_npc(world, player)),
        LocationData('Castle Ramparts', 'Ramparts Freeze the engineer',  1337129, lambda state: state.has('Talaria Attachment', player) or state._timespinner_has_timestop(world, player)),
        LocationData('Castle Ramparts', 'Ramparts Giantess guarded room',  1337130),
        LocationData('Castle Ramparts', 'Ramparts Knight and archer guarded room',  1337131),
        LocationData('Castle Ramparts', 'Ramparts pedestal',  1337132),
        LocationData('Castle Keep', 'Castle basement secret pedestal',  1337133, lambda state: state._timespinner_can_break_walls(world, player)),
        LocationData('Castle Keep', 'Clean the castle basement',  1337134),
        LocationData('Royal towers (lower)', 'Yas queen room',  1337135, lambda state: state._timespinner_has_pink(world, player)),
        LocationData('Castle Keep', 'Castle basement giantess',  1337136),
        LocationData('Castle Keep', 'Omelette chest',  1337137),
        LocationData('Castle Keep', 'Just an egg',  1337138),
        LocationData('Castle Keep', 'Under the twins',  1337139),
        LocationData('Castle Keep', 'Killed Twins',  EventId, lambda state: state._timespinner_has_timestop(world, player)),
        LocationData('Castle Keep', 'Advisor jump', 1337171, lambda state: state._timespinner_has_timestop(world, player)),
        LocationData('Castle Keep', 'Twins',  1337140, lambda state: state._timespinner_has_timestop(world, player)),
        LocationData('Castle Keep', 'Royal guard tiny room',  1337141, lambda state: state._timespinner_has_doublejump(world, player) or state._timespinner_has_fastjump_on_npc(world,player)),
        LocationData('Royal towers (lower)', 'Royal tower floor secret',  1337142, lambda state: state._timespinner_has_doublejump(world, player) and state._timespinner_can_break_walls(world, player)),
        LocationData('Royal towers', 'Royal towers pre-climb gap',  1337143),
        LocationData('Royal towers', 'Royal towers long balcony',  1337144),
        LocationData('Royal towers (upper)', 'Next to bottom royal tower struggle juggle',  1337145),
        LocationData('Royal towers (upper)', 'Bottom royal tower struggle juggle',  1337146, lambda state: state._timespinner_has_doublejump_of_npc(world, player)),
        LocationData('Royal towers (upper)', 'Top royal tower struggle juggle',  1337147, lambda state: state._timespinner_has_doublejump_of_npc(world, player)),
        LocationData('Royal towers (upper)', 'No struggle required',  1337148, lambda state: state._timespinner_has_doublejump_of_npc(world, player)),
        LocationData('Royal towers', 'Right tower freebie',  1337149),
        LocationData('Royal towers (upper)', 'Royal towers left small balcony',  1337150),
        LocationData('Royal towers (upper)', 'Royal tower left royal guard',  1337151),
        LocationData('Royal towers (upper)', 'Before Aelana',  1337152),
        LocationData('Royal towers (upper)', 'Killed Aelana',  EventId),
        LocationData('Royal towers (upper)', 'Aelana\'s attic',  1337153, lambda state: state._timespinner_has_upwarddash(world, player)),
        LocationData('Royal towers (upper)', 'Aelana\'s chest',  1337154),
        LocationData('Royal towers (upper)', 'Aelana\'s pedestal',  1337155),

        # Ancient pyramid locations
        LocationData('Ancient Pyramid (left)', 'Why not it\'s right there',  1337246),
        LocationData('Ancient Pyramid (left)', 'Conviction guarded room',  1337247),
        LocationData('Ancient Pyramid (left)', 'Pit secret room',  1337248, lambda state: state._timespinner_can_break_walls(world, player)),
        LocationData('Ancient Pyramid (left)', 'Regret chest',  1337249, lambda state: state._timespinner_can_break_walls(world, player)),
        LocationData('Ancient Pyramid (right)', 'Nightmare Door chest',  1337236),
        LocationData('Ancient Pyramid (right)', 'Killed Nightmare',  EventId)
    ]

    # 1337156 - 1337170 Downloads
    if not world or is_option_enabled(world, player, "DownloadableItems"):
        location_table += ( 
            LocationData('Library', 'Library terminal 2 (Lachiem)',  1337156, lambda state: state.has('Tablet', player)),
            LocationData('Library', 'Library terminal 1 (Windaria)',  1337157, lambda state: state.has('Tablet', player)),
            # 1337158 Is lost in time
            LocationData('Library', 'Library terminal 3 (Emporer Nuvius)',  1337159, lambda state: state.has('Tablet', player)),
            LocationData('Library', 'V terminal 1 (War of the Sisters)',  1337160, lambda state: state.has_all({'Tablet', 'Library Keycard V'}, player)),
            LocationData('Library', 'V terminal 2 (Lake Desolation Map)',  1337161, lambda state: state.has_all({'Tablet', 'Library Keycard V'}, player)),
            LocationData('Library', 'V terminal 3 (Vilete)',  1337162, lambda state: state.has_all({'Tablet', 'Library Keycard V'}, player)),
            LocationData('Library top', 'Backer room terminal (Vandagray Metropolis Map)',  1337163, lambda state: state.has('Tablet', player)),
            LocationData('Varndagroth tower right (elevator)', 'Medbay terminal (Bleakness Research)',  1337164, lambda state: state.has('Tablet', player) and state._timespinner_has_keycard_B(world, player)),
            LocationData('The lab (upper)', 'Chest and download terminal (Experiment #13)',  1337165, lambda state: state.has('Tablet', player)),
            LocationData('The lab (power off)', 'Lab terminal middle (Amadeus Laboratory Map)',  1337166, lambda state: state.has('Tablet', player)),
            LocationData('The lab (power off)', 'Sentry platform terminal (Origins)',  1337167, lambda state: state.has('Tablet', player)),
            LocationData('The lab', 'Experiment 13 terminal (W.R.E.C Farewell)',  1337168, lambda state: state.has('Tablet', player)),
            LocationData('The lab', 'Lab terminal left (Biotechnology)',  1337169, lambda state: state.has('Tablet', player)),
            LocationData('The lab (power off)', 'Lab terminal right (Experiment #11)',  1337170, lambda state: state.has('Tablet', player))
        )

    # 1337176 - 1337176 Cantoran
    if not world or is_option_enabled(world, player, "Cantoran"):
        location_table += (
            LocationData('Left Side forest Caves', 'Cantoran',  1337176),
        )

    # 1337177 - 1337198 Lore Checks
    if not world or is_option_enabled(world, player, "LoreChecks"):
        location_table += (
            LocationData('Lower lake desolation', 'Memory - Coyote Jump (Time Messenger)',  1337177),
            LocationData('Library', 'Memory - Waterway (A Message)',  1337178),
            LocationData('Library top', 'Memory - Library Gap (Lachiemi Sun)',  1337179),
            LocationData('Library top', 'Memory - Mr. Hat Portrait (Moonlit Night)',  1337180),
            LocationData('Varndagroth tower left', 'Memory - Left Elevator (Nomads)',  1337181, lambda state: state.has('Elevator Keycard', player)),
            LocationData('Varndagroth tower right (lower)', 'Memory - Siren Elevator (Childhood)',  1337182, lambda state: state._timespinner_has_keycard_B(world, player)),
            LocationData('Varndagroth tower right (lower)', 'Memory - Varndagroth Right Bottom (Faron)',  1337183),
            LocationData('Military Fortress', 'Memory - Bomber Climb (A Solution)',  1337184, lambda state: state.has('Timespinner Wheel', player) and state._timespinner_has_doublejump_of_npc(world, player)),
            LocationData('The lab', 'Memory - Genza\'s Secret Stash 1 (An Old Friend)',  1337185, lambda state: state._timespinner_can_break_walls(world, player)),
            LocationData('The lab', 'Memory - Genza\'s Secret Stash 2 (Twilight Dinner)',  1337186, lambda state: state._timespinner_can_break_walls(world, player)),
            LocationData('Emperors tower', 'Memory - Way Up There (Final Circle)',  1337187, lambda state: state._timespinner_has_doublejump_of_npc(world, player)),
            LocationData('Forest', 'Journal - Forest Rats (Lachiem Expedition)',  1337188),
            LocationData('Forest', 'Journal - Forest Bat Jump Ledge (Peace Treaty)',  1337189, lambda state: state._timespinner_has_doublejump_of_npc(world, player) or state._timespinner_has_forwarddash_doublejump(world, player) or state._timespinner_has_fastjump_on_npc(world, player)),
            LocationData('Castle Ramparts', 'Journal - Floating in Moat (Prime Edicts)',  1337190),
            LocationData('Castle Ramparts', 'Journal - Archer + Knight (Declaration of Independence)',  1337191),
            LocationData('Castle Keep', 'Journal - Under the Twins (Letter of Reference)',  1337192),
            LocationData('Castle Keep', 'Journal - Castle Loop Giantess (Political Advice)',  1337193),
            LocationData('Royal towers (lower)', 'Journal - Aelana\'s Room (Diplomatic Missive)',  1337194, lambda state: state._timespinner_has_pink(world, player)),
            LocationData('Royal towers (upper)', 'Journal - Top Struggle Juggle Base (War of the Sisters)',  1337195),
            LocationData('Royal towers (upper)', 'Journal - Aelana Boss (Stained Letter)',  1337196),
            LocationData('Royal towers', 'Journal - Near Bottom Struggle Juggle (Mission Findings)',  1337197, lambda state: state._timespinner_has_doublejump_of_npc(world, player)),
            LocationData('Caves of Banishment (Maw)', 'Journal - Lower Left Maw Caves (Naivety)',  1337198)
        )

    # 1337199 - 1337236 Reserved for future use

    # 1337237 - 1337245 GyreArchives
    if not world or is_option_enabled(world, player, "GyreArchives"):
        location_table += (
            LocationData('Ravenlord\'s Lair', 'Ravenlord post fight (pedestal)',  1337237),
            LocationData('Ifrit\'s Lair', 'Ifrit post fight (pedestal)',  1337238),
            LocationData('Temporal Gyre', 'Gyre chest 1',  1337239),
            LocationData('Temporal Gyre', 'Gyre chest 2',  1337240),
            LocationData('Temporal Gyre', 'Gyre chest 3',  1337241),
            LocationData('Ravenlord\'s Lair', 'Ravenlord pre fight',  1337242),
            LocationData('Ravenlord\'s Lair', 'Ravenlord post fight (chest)',  1337243),
            LocationData('Ifrit\'s Lair', 'Ifrit pre fight',  1337244),
            LocationData('Ifrit\'s Lair', 'Ifrit post fight (chest)', 1337245),
        )
 
    return tuple(location_table)
        

starter_progression_locations: Tuple[str, ...] = (
    'Starter chest 2',
    'Starter chest 3',
    'Starter chest 1',
    'Timespinner Wheel room'
)
