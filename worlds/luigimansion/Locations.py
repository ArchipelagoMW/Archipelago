from typing import List, Tuple, Optional, Callable, NamedTuple
from BaseClasses import MultiWorld, Location
from .Options import is_option_enabled

EventId: Optional[int] = None

# need to understand how Location sublasses are used to ensure passing of correct information

class LMLocation(Location):
    game: str = "Luigi\'s Mansion"


def get_locations(world: Optional[MultiWorld], player: Optional[int]) -> Tuple[LMLocation, ...]:
    # 1337000 - 1337155 Generic locations
    # 1337171 - 1337175 New Pickup checks
    # 1337246 - 1337249 Ancient Pyramid
    location_table: List[LMLocation] = [
        # Present item locations
        LMLocation(parent_region='Tutorial', name='Tutorial: Yo Momma 1',  address=1337000),
        LMLocation('Tutorial', 'Tutorial: Yo Momma 2',  1337001),
        LMLocation('Lake desolation', 'Lake Desolation: Starter chest 2',  1337002),
        LMLocation('Lake desolation', 'Lake Desolation: Starter chest 3',  1337003),
        LMLocation('Lake desolation', 'Lake Desolation: Starter chest 1',  1337004),
        LMLocation('Lake desolation', 'Lake Desolation (Lower): Timespinner Wheel room',  1337005),
        LMLocation('Lake desolation', 'Lake Desolation: Forget me not chest',  1337006, lambda state: state._timespinner_has_fire(world, player) and state.can_reach('Upper Lake Serene', 'Region', player)),
        LMLocation('Lake desolation', 'Lake Desolation (Lower): Chicken chest', 1337007, lambda state: state._timespinner_has_timestop(world, player)),
        LMLocation('Lower lake desolation', 'Lake Desolation (Lower): Not so secret room',  1337008, lambda state: state._timespinner_can_break_walls(world, player)),
        LMLocation('Lower lake desolation', 'Lake Desolation (Upper): Tank chest',  1337009, lambda state: state._timespinner_has_timestop(world, player)),
        LMLocation('Upper lake desolation', 'Lake Desolation (Upper): Oxygen recovery room',  1337010),
        LMLocation('Upper lake desolation', 'Lake Desolation (Upper): Secret room',  1337011, lambda state: state._timespinner_can_break_walls(world, player)),
        LMLocation('Upper lake desolation', 'Lake Desolation (Upper): Double jump cave platform',  1337012, lambda state: state._timespinner_has_doublejump(world, player)),
        LMLocation('Upper lake desolation', 'Lake Desolation (Upper): Double jump cave floor',  1337013),
        LMLocation('Upper lake desolation', 'Lake Desolation (Upper): Sparrow chest',  1337014),
        LMLocation('Upper lake desolation', 'Lake Desolation (Upper): Crash site pedestal',  1337015),
        LMLocation('Upper lake desolation', 'Lake Desolation (Upper): Crash site chest 1',  1337016, lambda state: state.has_all({'Killed Maw'}, player)),
        LMLocation('Upper lake desolation', 'Lake Desolation (Upper): Crash site chest 2',  1337017, lambda state: state.has_all({'Killed Maw'}, player)),
        LMLocation('Eastern lake desolation', 'Lake Desolation: Kitty Boss',  1337018),
        LMLocation('Library', 'Library: Basement',  1337019),
        LMLocation('Library', 'Library: Warp gate',  1337020),
        LMLocation('Library', 'Library: Librarian',  1337021),
        LMLocation('Library', 'Library: Reading nook chest',  1337022),
        LMLocation('Library', 'Library: Storage room chest 1',  1337023, lambda state: state._timespinner_has_keycard_D(world, player)),
        LMLocation('Library', 'Library: Storage room chest 2',  1337024, lambda state: state._timespinner_has_keycard_D(world, player)),
        LMLocation('Library', 'Library: Storage room chest 3',  1337025, lambda state: state._timespinner_has_keycard_D(world, player)),
        LMLocation('Library top', 'Library: Backer room chest 5',  1337026),
        LMLocation('Library top', 'Library: Backer room chest 4',  1337027),
        LMLocation('Library top', 'Library: Backer room chest 3',  1337028),
        LMLocation('Library top', 'Library: Backer room chest 2',  1337029),
        LMLocation('Library top', 'Library: Backer room chest 1',  1337030),
        LMLocation('Varndagroth tower left', 'Varndagroth Towers (Left): Elevator Key not required',  1337031),
        LMLocation('Varndagroth tower left', 'Varndagroth Towers (Left): Ye olde Timespinner',  1337032),
        LMLocation('Varndagroth tower left', 'Varndagroth Towers (Left): Bottom floor',  1337033, lambda state: state._timespinner_has_keycard_C(world, player)),
        LMLocation('Varndagroth tower left', 'Varndagroth Towers (Left): Air vents secret',  1337034, lambda state: state._timespinner_can_break_walls(world, player)),
        LMLocation('Varndagroth tower left', 'Varndagroth Towers (Left): Elevator chest',  1337035, lambda state: state.has('Elevator Keycard', player)),
        LMLocation('Varndagroth tower right (upper)', 'Varndagroth Towers: Bridge',  1337036),
        LMLocation('Varndagroth tower right (elevator)', 'Varndagroth Towers (Right): Elevator chest',  1337037),
        LMLocation('Varndagroth tower right (upper)', 'Varndagroth Towers (Right): Elevator card chest',  1337038, lambda state: state.has('Elevator Keycard', player) or state._timespinner_has_doublejump(world, player)),
        LMLocation('Varndagroth tower right (upper)', 'Varndagroth Towers (Right): Air vents right chest',  1337039, lambda state: state.has('Elevator Keycard', player) or state._timespinner_has_doublejump(world, player)),
        LMLocation('Varndagroth tower right (upper)', 'Varndagroth Towers (Right): Air vents left chest',  1337040, lambda state: state.has('Elevator Keycard', player) or state._timespinner_has_doublejump(world, player)),
        LMLocation('Varndagroth tower right (lower)', 'Varndagroth Towers (Right): Bottom floor',  1337041),
        LMLocation('Varndagroth tower right (elevator)', 'Varndagroth Towers (Right): Varndagroth',  1337042, lambda state: state._timespinner_has_keycard_C(world, player)),
        LMLocation('Varndagroth tower right (elevator)', 'Varndagroth Towers (Right): Spider Hell',  1337043, lambda state: state._timespinner_has_keycard_A(world, player)),
        LMLocation('Skeleton Shaft', 'Sealed Caves (Xarion): Skeleton',  1337044),
        LMLocation('Sealed Caves (Xarion)', 'Sealed Caves (Xarion): Shroom jump room',  1337045, lambda state: state._timespinner_has_timestop(world, player)),
        LMLocation('Sealed Caves (Xarion)', 'Sealed Caves (Xarion): Double shroom room',  1337046),
        LMLocation('Sealed Caves (Xarion)', 'Sealed Caves (Xarion): Mini jackpot room',  1337047, lambda state: state._timespinner_has_forwarddash_doublejump(world, player)),
        LMLocation('Sealed Caves (Xarion)', 'Sealed Caves (Xarion): Below mini jackpot room',  1337048),
        LMLocation('Sealed Caves (Xarion)', 'Sealed Caves (Xarion): Secret room',  1337049, lambda state: state._timespinner_can_break_walls(world, player)),
        LMLocation('Sealed Caves (Xarion)', 'Sealed Caves (Xarion): Bottom left room',  1337050),
        LMLocation('Sealed Caves (Xarion)', 'Sealed Caves (Xarion): Last chance before Xarion',  1337051, lambda state: state._timespinner_has_doublejump(world, player)),
        LMLocation('Sealed Caves (Xarion)', 'Sealed Caves (Xarion): Xarion',  1337052),
        LMLocation('Sealed Caves (Sirens)', 'Sealed Caves (Sirens): Water hook',  1337053, lambda state: state.has('Water Mask', player)),
        LMLocation('Sealed Caves (Sirens)', 'Sealed Caves (Sirens): Siren room underwater right',  1337054, lambda state: state.has('Water Mask', player)),
        LMLocation('Sealed Caves (Sirens)', 'Sealed Caves (Sirens): Siren room underwater left',  1337055, lambda state: state.has('Water Mask', player)),
        LMLocation('Sealed Caves (Sirens)', 'Sealed Caves (Sirens): Cave after sirens chest 1',  1337056),
        LMLocation('Sealed Caves (Sirens)', 'Sealed Caves (Sirens): Cave after sirens chest 2',  1337057),
        LMLocation('Military Fortress', 'Military Fortress: Bomber chest',  1337058, lambda state: state.has('Timespinner Wheel', player) and state._timespinner_has_doublejump_of_npc(world, player)),
        LMLocation('Military Fortress', 'Military Fortress: Close combat room',  1337059),
        LMLocation('Military Fortress (hangar)', 'Military Fortress: Soldiers bridge',  1337060),
        LMLocation('Military Fortress (hangar)', 'Military Fortress: Giantess room',  1337061),
        LMLocation('Military Fortress (hangar)', 'Military Fortress: Giantess bridge',  1337062),
        LMLocation('Military Fortress (hangar)', 'Military Fortress: B door chest 2',  1337063, lambda state: state._timespinner_has_doublejump(world, player) and state._timespinner_has_keycard_B(world, player)),
        LMLocation('Military Fortress (hangar)', 'Military Fortress: B door chest 1',  1337064, lambda state: state._timespinner_has_doublejump(world, player) and state._timespinner_has_keycard_B(world, player)),
        LMLocation('Military Fortress (hangar)', 'Military Fortress: Pedestal',  1337065, lambda state: state._timespinner_has_doublejump_of_npc(world, player) or state._timespinner_has_forwarddash_doublejump(world, player)),
        LMLocation('The lab', 'Lab: Coffee break',  1337066),
        LMLocation('The lab', 'Lab: Lower trash right',  1337067, lambda state: state._timespinner_has_doublejump(world, player)),
        LMLocation('The lab', 'Lab: Lower trash left',  1337068, lambda state: state._timespinner_has_upwarddash(world, player)),
        LMLocation('The lab', 'Lab: Below lab entrance',  1337069, lambda state: state._timespinner_has_doublejump(world, player)),
        LMLocation('The lab (power off)', 'Lab: Trash jump room',  1337070),
        LMLocation('The lab (power off)', 'Lab: Dynamo Works',  1337071),
        LMLocation('The lab (upper)', 'Lab: Genza (Blob Mom)',  1337072),
        LMLocation('The lab (power off)', 'Lab: Experiment #13',  1337073),
        LMLocation('The lab (upper)', 'Lab: Download and chest room chest',  1337074),
        LMLocation('The lab (upper)', 'Lab: Lab secret',  1337075, lambda state: state._timespinner_can_break_walls(world, player)),
        LMLocation('The lab (power off)', 'Lab: Spider Hell',  1337076, lambda state: state._timespinner_has_keycard_A(world, player)),
        LMLocation('Emperors tower', 'Emperor\'s Tower: Courtyard bottom chest',  1337077),
        LMLocation('Emperors tower', 'Emperor\'s Tower: Courtyard floor secret',  1337078, lambda state: state._timespinner_has_upwarddash(world, player) and state._timespinner_can_break_walls(world, player)),
        LMLocation('Emperors tower', 'Emperor\'s Tower: Courtyard upper chest',  1337079, lambda state: state._timespinner_has_upwarddash(world, player)),
        LMLocation('Emperors tower', 'Emperor\'s Tower: Galactic sage room',  1337080),
        LMLocation('Emperors tower', 'Emperor\'s Tower: Bottom right tower',  1337081),
        LMLocation('Emperors tower', 'Emperor\'s Tower: Wayyyy up there',  1337082, lambda state: state._timespinner_has_doublejump_of_npc(world, player)),
        LMLocation('Emperors tower', 'Emperor\'s Tower: Left tower balcony',  1337083),
        LMLocation('Emperors tower', 'Emperor\'s Tower: Emperor\'s Chambers chest',  1337084),
        LMLocation('Emperors tower', 'Emperor\'s Tower: Emperor\'s Chambers pedestal',  1337085),

        # Past item locations
        LMLocation('Refugee Camp', 'Refugee Camp: Neliste\'s Bra',  1337086),
        LMLocation('Refugee Camp', 'Refugee Camp: Storage chest 3',  1337087),
        LMLocation('Refugee Camp', 'Refugee Camp: Storage chest 2',  1337088),
        LMLocation('Refugee Camp', 'Refugee Camp: Storage chest 1',  1337089),
        LMLocation('Forest', 'Forest: Refugee camp roof',  1337090),
        LMLocation('Forest', 'Forest: Bat jump ledge',  1337091, lambda state: state._timespinner_has_doublejump_of_npc(world, player) or state._timespinner_has_forwarddash_doublejump(world, player) or state._timespinner_has_fastjump_on_npc(world, player)),
        LMLocation('Forest', 'Forest: Green platform secret',  1337092, lambda state: state._timespinner_can_break_walls(world, player)),
        LMLocation('Forest', 'Forest: Rats guarded chest',  1337093),
        LMLocation('Forest', 'Forest: Waterfall chest 1',  1337094, lambda state: state.has('Water Mask', player)),
        LMLocation('Forest', 'Forest: Waterfall chest 2',  1337095, lambda state: state.has('Water Mask', player)),
        LMLocation('Forest', 'Forest: Batcave',  1337096),
        LMLocation('Forest', 'Castle Ramparts: In the moat',  1337097),
        LMLocation('Left Side forest Caves', 'Forest: Before Serene single bat cave',  1337098),
        LMLocation('Upper Lake Serene', 'Lake Serene (Upper): Rat nest',  1337099),
        LMLocation('Upper Lake Serene', 'Lake Serene (Upper): Double jump cave platform',  1337100, lambda state: state._timespinner_has_doublejump(world, player)),
        LMLocation('Upper Lake Serene', 'Lake Serene (Upper): Double jump cave floor',  1337101),
        LMLocation('Upper Lake Serene', 'Lake Serene (Upper): Cave secret',  1337102, lambda state: state._timespinner_can_break_walls(world, player)),
        LMLocation('Upper Lake Serene', 'Lake Serene: Before Big Bird', 1337175),
        LMLocation('Upper Lake Serene', 'Lake Serene: Behind the vines',  1337103),
        LMLocation('Upper Lake Serene', 'Lake Serene: Pyramid keys room',  1337104),
        LMLocation('Upper Lake Serene', 'Lake Serene (Upper): Chicken ledge', 1337174),
        LMLocation('Lower Lake Serene', 'Lake Serene (Lower): Deep dive',  1337105),
        LMLocation('Lower Lake Serene', 'Lake Serene (Lower): Under the eels',  1337106),
        LMLocation('Lower Lake Serene', 'Lake Serene (Lower): Water spikes room',  1337107),
        LMLocation('Lower Lake Serene', 'Lake Serene (Lower): Underwater secret',  1337108, lambda state: state._timespinner_can_break_walls(world, player)),
        LMLocation('Lower Lake Serene', 'Lake Serene (Lower): T chest',  1337109),
        LMLocation('Lower Lake Serene', 'Lake Serene (Lower): Past the eels',  1337110),
        LMLocation('Lower Lake Serene', 'Lake Serene (Lower): Underwater pedestal',  1337111),
        LMLocation('Caves of Banishment (upper)', 'Caves of Banishment (Maw): Shroom jump room',  1337112, lambda state: state._timespinner_has_doublejump(world, player)),
        LMLocation('Caves of Banishment (upper)', 'Caves of Banishment (Maw): Secret room',  1337113),
        LMLocation('Caves of Banishment (upper)', 'Caves of Banishment (Maw): Bottom left room',  1337114),
        LMLocation('Caves of Banishment (upper)', 'Caves of Banishment (Maw): Single shroom room',  1337115),
        LMLocation('Caves of Banishment (upper)', 'Caves of Banishment (Maw): Jackpot room chest 1',  1337116, lambda state: state._timespinner_has_forwarddash_doublejump(world, player)),
        LMLocation('Caves of Banishment (upper)', 'Caves of Banishment (Maw): Jackpot room chest 2',  1337117, lambda state: state._timespinner_has_forwarddash_doublejump(world, player)),
        LMLocation('Caves of Banishment (upper)', 'Caves of Banishment (Maw): Jackpot room chest 3',  1337118, lambda state: state._timespinner_has_forwarddash_doublejump(world, player)),
        LMLocation('Caves of Banishment (upper)', 'Caves of Banishment (Maw): Jackpot room chest 4',  1337119, lambda state: state._timespinner_has_forwarddash_doublejump(world, player)),
        LMLocation('Caves of Banishment (upper)', 'Caves of Banishment (Maw): Pedestal',  1337120),
        LMLocation('Caves of Banishment (Maw)', 'Caves of Banishment (Maw): Last chance before Maw',  1337121, lambda state: state._timespinner_has_doublejump(world, player)),
        LMLocation('Caves of Banishment (Maw)', 'Caves of Banishment (Maw): Plasma Crystal', 1337173, lambda state: state.has_any({'Gas Mask', 'Talaria Attachment'}, player)),
        LMLocation('Caves of Banishment (Maw)', 'Killed Maw',  EventId, lambda state: state.has('Gas Mask', player)),
        LMLocation('Caves of Banishment (Maw)', 'Caves of Banishment (Maw): Mineshaft',  1337122, lambda state: state.has('Gas Mask', player)),
        LMLocation('Caves of Banishment (Sirens)', 'Caves of Banishment (Sirens): Wyvern room',  1337123),
        LMLocation('Caves of Banishment (Sirens)', 'Caves of Banishment (Sirens): Siren room above water chest',  1337124),
        LMLocation('Caves of Banishment (Sirens)', 'Caves of Banishment (Sirens): Siren room underwater left chest',  1337125, lambda state: state.has('Water Mask', player)),
        LMLocation('Caves of Banishment (Sirens)', 'Caves of Banishment (Sirens): Siren room underwater right chest',  1337126, lambda state: state.has('Water Mask', player)),
        LMLocation('Caves of Banishment (Sirens)', 'Caves of Banishment (Sirens): Siren room underwater right ground', 1337172, lambda state: state.has('Water Mask', player)),
        LMLocation('Caves of Banishment (Sirens)', 'Caves of Banishment (Sirens): Water hook',  1337127, lambda state: state.has('Water Mask', player)),
        LMLocation('Castle Ramparts', 'Castle Ramparts: Bomber chest',  1337128, lambda state: state._timespinner_has_multiple_small_jumps_of_npc(world, player)),
        LMLocation('Castle Ramparts', 'Castle Ramparts: Freeze the engineer',  1337129, lambda state: state.has('Talaria Attachment', player) or state._timespinner_has_timestop(world, player)),
        LMLocation('Castle Ramparts', 'Castle Ramparts: Giantess guarded room',  1337130),
        LMLocation('Castle Ramparts', 'Castle Ramparts: Knight and archer guarded room',  1337131),
        LMLocation('Castle Ramparts', 'Castle Ramparts: Pedestal',  1337132),
        LMLocation('Castle Keep', 'Castle Keep: Basement secret pedestal',  1337133, lambda state: state._timespinner_can_break_walls(world, player)),
        LMLocation('Castle Keep', 'Castle Keep: Clean the castle basement',  1337134),
        LMLocation('Royal towers (lower)', 'Castle Keep: Yas queen room',  1337135, lambda state: state._timespinner_has_pink(world, player)),
        LMLocation('Castle Keep', 'Castle Keep: Giantess guarded chest',  1337136),
        LMLocation('Castle Keep', 'Castle Keep: Omelette chest',  1337137),
        LMLocation('Castle Keep', 'Castle Keep: Just an egg',  1337138),
        LMLocation('Castle Keep', 'Castle Keep: Under the twins',  1337139),
        LMLocation('Castle Keep', 'Killed Twins',  EventId, lambda state: state._timespinner_has_timestop(world, player)),
        LMLocation('Castle Keep', 'Castle Keep: Advisor jump', 1337171, lambda state: state._timespinner_has_timestop(world, player)),
        LMLocation('Castle Keep', 'Castle Keep: Twins',  1337140, lambda state: state._timespinner_has_timestop(world, player)),
        LMLocation('Castle Keep', 'Castle Keep: Royal guard tiny room',  1337141, lambda state: state._timespinner_has_doublejump(world, player) or state._timespinner_has_fastjump_on_npc(world,player)),
        LMLocation('Royal towers (lower)', 'Royal Towers: Floor secret',  1337142, lambda state: state._timespinner_has_doublejump(world, player) and state._timespinner_can_break_walls(world, player)),
        LMLocation('Royal towers', 'Royal Towers: Pre-climb gap',  1337143),
        LMLocation('Royal towers', 'Royal Towers: Long balcony',  1337144),
        LMLocation('Royal towers (upper)', 'Royal Towers: Past bottom struggle juggle',  1337145),
        LMLocation('Royal towers (upper)', 'Royal Towers: Bottom struggle juggle',  1337146, lambda state: state._timespinner_has_doublejump_of_npc(world, player)),
        LMLocation('Royal towers (upper)', 'Royal Towers: Top struggle juggle',  1337147, lambda state: state._timespinner_has_doublejump_of_npc(world, player)),
        LMLocation('Royal towers (upper)', 'Royal Towers: No struggle required',  1337148, lambda state: state._timespinner_has_doublejump_of_npc(world, player)),
        LMLocation('Royal towers', 'Royal Towers: Right tower freebie',  1337149),
        LMLocation('Royal towers (upper)', 'Royal Towers: Left tower small balcony',  1337150),
        LMLocation('Royal towers (upper)', 'Royal Towers: Left tower royal guard',  1337151),
        LMLocation('Royal towers (upper)', 'Royal Towers: Before Aelana',  1337152),
        LMLocation('Royal towers (upper)', 'Killed Aelana',  EventId),
        LMLocation('Royal towers (upper)', 'Royal Towers: Aelana\'s attic',  1337153, lambda state: state._timespinner_has_upwarddash(world, player)),
        LMLocation('Royal towers (upper)', 'Royal Towers: Aelana\'s chest',  1337154),
        LMLocation('Royal towers (upper)', 'Royal Towers: Aelana\'s pedestal',  1337155),

        # Ancient pyramid locations
        LMLocation('Ancient Pyramid (entrance)', 'Ancient Pyramid: Why not it\'s right there',  1337246),
        LMLocation('Ancient Pyramid (left)', 'Ancient Pyramid: Conviction guarded room',  1337247),
        LMLocation('Ancient Pyramid (left)', 'Ancient Pyramid: Pit secret room',  1337248, lambda state: state._timespinner_can_break_walls(world, player)),
        LMLocation('Ancient Pyramid (left)', 'Ancient Pyramid: Regret chest',  1337249, lambda state: state._timespinner_can_break_walls(world, player)),
        LMLocation('Ancient Pyramid (right)', 'Ancient Pyramid: Nightmare Door chest',  1337236),
        LMLocation('Ancient Pyramid (right)', 'Killed Nightmare', EventId, lambda state: state.has_all({'Timespinner Wheel', 'Timespinner Spindle', 'Timespinner Gear 1', 'Timespinner Gear 2', 'Timespinner Gear 3'}, player))
    ]

    # 1337156 - 1337170 Downloads
    if not world or is_option_enabled(world, player, "Plants"):
        location_table += ( 
            LMLocation('Library', 'Library: Terminal 2 (Lachiem)',  1337156, lambda state: state.has('Tablet', player)),
            LMLocation('Library', 'Library: Terminal 1 (Windaria)',  1337157, lambda state: state.has('Tablet', player)),
            # 1337158 Is lost in time
            LMLocation('Library', 'Library: Terminal 3 (Emporer Nuvius)',  1337159, lambda state: state.has('Tablet', player)),
            LMLocation('Library', 'Library: V terminal 1 (War of the Sisters)',  1337160, lambda state: state.has_all({'Tablet', 'Library Keycard V'}, player)),
            LMLocation('Library', 'Library: V terminal 2 (Lake Desolation Map)',  1337161, lambda state: state.has_all({'Tablet', 'Library Keycard V'}, player)),
            LMLocation('Library', 'Library: V terminal 3 (Vilete)',  1337162, lambda state: state.has_all({'Tablet', 'Library Keycard V'}, player)),
            LMLocation('Library top', 'Library: Backer room terminal (Vandagray Metropolis Map)',  1337163, lambda state: state.has('Tablet', player)),
            LMLocation('Varndagroth tower right (elevator)', 'Varndagroth Towers (Right): Medbay terminal (Bleakness Research)',  1337164, lambda state: state.has('Tablet', player) and state._timespinner_has_keycard_B(world, player)),
            LMLocation('The lab (upper)', 'Lab: Download and chest room terminal (Experiment #13)',  1337165, lambda state: state.has('Tablet', player)),
            LMLocation('The lab (power off)', 'Lab: Middle terminal (Amadeus Laboratory Map)',  1337166, lambda state: state.has('Tablet', player)),
            LMLocation('The lab (power off)', 'Lab: Sentry platform terminal (Origins)',  1337167, lambda state: state.has('Tablet', player)),
            LMLocation('The lab', 'Lab: Experiment 13 terminal (W.R.E.C Farewell)',  1337168, lambda state: state.has('Tablet', player)),
            LMLocation('The lab', 'Lab: Left terminal (Biotechnology)',  1337169, lambda state: state.has('Tablet', player)),
            LMLocation('The lab (power off)', 'Lab: Right terminal (Experiment #11)',  1337170, lambda state: state.has('Tablet', player))
        )

    # 1337176 - 1337176 Cantoran
    if not world or is_option_enabled(world, player, "Furniture"):
        location_table += (
            LMLocation('Left Side forest Caves', 'Lake Serene: Cantoran',  1337176),
        )

    # 1337177 - 1337198 Lore Checks
    if not world or is_option_enabled(world, player, "Light Fixtures"):
        location_table += (
            LMLocation('Lower lake desolation', 'Lake Desolation: Memory - Coyote Jump (Time Messenger)',  1337177),
            LMLocation('Library', 'Library: Memory - Waterway (A Message)',  1337178),
            LMLocation('Library top', 'Library: Memory - Library Gap (Lachiemi Sun)',  1337179),
            LMLocation('Library top', 'Library: Memory - Mr. Hat Portrait (Moonlit Night)',  1337180),
            LMLocation('Varndagroth tower left', 'Varndagroth Towers (Left): Memory - Elevator (Nomads)',  1337181, lambda state: state.has('Elevator Keycard', player)),
            LMLocation('Varndagroth tower right (lower)', 'Varndagroth Towers: Memory - Siren Elevator (Childhood)',  1337182, lambda state: state._timespinner_has_keycard_B(world, player)),
            LMLocation('Varndagroth tower right (lower)', 'Varndagroth Towers (Right): Memory - Bottom (Faron)',  1337183),
            LMLocation('Military Fortress', 'Military Fortress: Memory - Bomber Climb (A Solution)',  1337184, lambda state: state.has('Timespinner Wheel', player) and state._timespinner_has_doublejump_of_npc(world, player)),
            LMLocation('The lab', 'Lab: Memory - Genza\'s Secret Stash 1 (An Old Friend)',  1337185, lambda state: state._timespinner_can_break_walls(world, player)),
            LMLocation('The lab', 'Lab: Memory - Genza\'s Secret Stash 2 (Twilight Dinner)',  1337186, lambda state: state._timespinner_can_break_walls(world, player)),
            LMLocation('Emperors tower', 'Emperor\'s Tower: Memory - Way Up There (Final Circle)',  1337187, lambda state: state._timespinner_has_doublejump_of_npc(world, player)),
            LMLocation('Forest', 'Forest: Journal - Rats (Lachiem Expedition)',  1337188),
            LMLocation('Forest', 'Forest: Journal - Bat Jump Ledge (Peace Treaty)',  1337189, lambda state: state._timespinner_has_doublejump_of_npc(world, player) or state._timespinner_has_forwarddash_doublejump(world, player) or state._timespinner_has_fastjump_on_npc(world, player)),
            LMLocation('Castle Ramparts', 'Castle Ramparts: Journal - Floating in Moat (Prime Edicts)',  1337190),
            LMLocation('Castle Ramparts', 'Castle Ramparts: Journal - Archer + Knight (Declaration of Independence)',  1337191),
            LMLocation('Castle Keep', 'Castle Keep: Journal - Under the Twins (Letter of Reference)',  1337192),
            LMLocation('Castle Keep', 'Castle Keep: Journal - Castle Loop Giantess (Political Advice)',  1337193),
            LMLocation('Royal towers (lower)', 'Royal Towers: Journal - Aelana\'s Room (Diplomatic Missive)',  1337194, lambda state: state._timespinner_has_pink(world, player)),
            LMLocation('Royal towers (upper)', 'Royal Towers: Journal - Top Struggle Juggle Base (War of the Sisters)',  1337195),
            LMLocation('Royal towers (upper)', 'Royal Towers: Journal - Aelana Boss (Stained Letter)',  1337196),
            LMLocation('Royal towers', 'Royal Towers: Journal - Near Bottom Struggle Juggle (Mission Findings)',  1337197, lambda state: state._timespinner_has_doublejump_of_npc(world, player)),
            LMLocation('Caves of Banishment (Maw)', 'Caves of Banishment (Maw): Journal - Lower Left Caves (Naivety)',  1337198)
        )

    # 1337199 - 1337236 Reserved for future use

    # 1337237 - 1337245 GyreArchives
    if not world or is_option_enabled(world, player, "GyreArchives"):
        location_table += (
            LMLocation('Ravenlord\'s Lair', 'Ravenlord: Post fight (pedestal)',  1337237),
            LMLocation('Ifrit\'s Lair', 'Ifrit: Post fight (pedestal)',  1337238),
            LMLocation('Temporal Gyre', 'Temporal Gyre: Chest 1',  1337239),
            LMLocation('Temporal Gyre', 'Temporal Gyre: Chest 2',  1337240),
            LMLocation('Temporal Gyre', 'Temporal Gyre: Chest 3',  1337241),
            LMLocation('Ravenlord\'s Lair', 'Ravenlord: Pre fight',  1337242),
            LMLocation('Ravenlord\'s Lair', 'Ravenlord: Post fight (chest)',  1337243),
            LMLocation('Ifrit\'s Lair', 'Ifrit: Pre fight',  1337244),
            LMLocation('Ifrit\'s Lair', 'Ifrit: Post fight (chest)', 1337245),
        )
 
    return tuple(location_table)
        

starter_progression_locations: Tuple[str, ...] = (
    'Lake Desolation: Starter chest 2',
    'Lake Desolation: Starter chest 3',
    'Lake Desolation: Starter chest 1',
    'Lake Desolation (Lower): Timespinner Wheel room'
)
