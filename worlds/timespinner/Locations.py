from typing import List, Optional, Callable, NamedTuple
from BaseClasses import CollectionState
from BaseRules import AllReq, AnyReq, Req, complex_reqs_to_rule
from .Options import TimespinnerOptions
from .PreCalculatedWeights import PreCalculatedWeights
from .LogicExtensions import TimespinnerLogic

EventId: Optional[int] = None


class LocationData(NamedTuple):
    region: str
    name: str
    code: Optional[int]
    rule: Optional[Callable[[CollectionState], bool]] = None


def get_location_datas(player: Optional[int], options: Optional[TimespinnerOptions],
                  precalculated_weights: Optional[PreCalculatedWeights]) -> List[LocationData]:
    flooded: Optional[PreCalculatedWeights] = precalculated_weights
    logic = TimespinnerLogic(player, options, precalculated_weights)

    # 1337000 - 1337155 Generic locations
    # 1337171 - 1337175 New Pickup checks
    # 1337246 - 1337249 Ancient Pyramid
    location_table: List[LocationData] = [
        # Present item locations
        LocationData('Tutorial', 'Tutorial: Yo Momma 1',  1337000),
        LocationData('Tutorial', 'Tutorial: Yo Momma 2',  1337001),
        LocationData('Lake desolation', 'Lake Desolation: Starter chest 2',  1337002),
        LocationData('Lake desolation', 'Lake Desolation: Starter chest 3',  1337003),
        LocationData('Lake desolation', 'Lake Desolation: Starter chest 1',  1337004),
        LocationData('Lake desolation', 'Lake Desolation (Lower): Timespinner Wheel room',  1337005),
        LocationData('Lake desolation', 'Lake Desolation: Forget me not chest',  1337006, lambda state: logic.has_fire(state) and state.can_reach('Upper Lake Serene', 'Region', player)),
        LocationData('Lake desolation', 'Lake Desolation (Lower): Chicken chest', 1337007, logic.has_timestop),
        LocationData('Lower lake desolation', 'Lake Desolation (Lower): Not so secret room',  1337008, logic.can_break_walls),
        LocationData('Lower lake desolation', 'Lake Desolation (Upper): Tank chest',  1337009, logic.has_timestop),
        LocationData('Upper lake desolation', 'Lake Desolation (Upper): Oxygen recovery room',  1337010),
        LocationData('Upper lake desolation', 'Lake Desolation (Upper): Secret room',  1337011, logic.can_break_walls),
        LocationData('Upper lake desolation', 'Lake Desolation (Upper): Double jump cave platform',  1337012, logic.has_doublejump),
        LocationData('Upper lake desolation', 'Lake Desolation (Upper): Double jump cave floor',  1337013),
        LocationData('Upper lake desolation', 'Lake Desolation (Upper): Sparrow chest',  1337014),
        LocationData('Upper lake desolation', 'Lake Desolation (Upper): Crash site pedestal',  1337015),
        LocationData('Upper lake desolation', 'Lake Desolation (Upper): Crash site chest 1',  1337016, complex_reqs_to_rule(player, Req('Killed Maw'))),
        LocationData('Upper lake desolation', 'Lake Desolation (Upper): Crash site chest 2',  1337017, complex_reqs_to_rule(player, Req('Killed Maw'))),
        LocationData('Eastern lake desolation', 'Lake Desolation: Kitty Boss',  1337018),
        LocationData('Library', 'Library: Basement',  1337019),
        LocationData('Library', 'Library: Warp gate',  1337020),
        LocationData('Library', 'Library: Librarian',  1337021),
        LocationData('Library', 'Library: Reading nook chest',  1337022),
        LocationData('Library', 'Library: Storage room chest 1',  1337023, logic.has_keycard_D),
        LocationData('Library', 'Library: Storage room chest 2',  1337024, logic.has_keycard_D),
        LocationData('Library', 'Library: Storage room chest 3',  1337025, logic.has_keycard_D),
        LocationData('Library top', 'Library: Backer room chest 5',  1337026),
        LocationData('Library top', 'Library: Backer room chest 4',  1337027),
        LocationData('Library top', 'Library: Backer room chest 3',  1337028),
        LocationData('Library top', 'Library: Backer room chest 2',  1337029),
        LocationData('Library top', 'Library: Backer room chest 1',  1337030),
        LocationData('Varndagroth tower left', 'Varndagroth Towers (Left): Elevator Key not required',  1337031),
        LocationData('Varndagroth tower left', 'Varndagroth Towers (Left): Ye olde Timespinner',  1337032),
        LocationData('Varndagroth tower left', 'Varndagroth Towers (Left): Bottom floor',  1337033, logic.has_keycard_C),
        LocationData('Varndagroth tower left', 'Varndagroth Towers (Left): Air vents secret',  1337034, logic.can_break_walls),
        LocationData('Varndagroth tower left', 'Varndagroth Towers (Left): Elevator chest',  1337035, complex_reqs_to_rule(player, Req('Elevator Keycard'))),
        LocationData('Varndagroth tower right (upper)', 'Varndagroth Towers: Bridge',  1337036),
        LocationData('Varndagroth tower right (elevator)', 'Varndagroth Towers (Right): Elevator chest',  1337037),
        LocationData('Varndagroth tower right (upper)', 'Varndagroth Towers (Right): Elevator card chest',  1337038, complex_reqs_to_rule(player, AnyReq([Req('Elevator Keycard'), logic.doublejump_req]))),
        LocationData('Varndagroth tower right (upper)', 'Varndagroth Towers (Right): Air vents right chest',  1337039, complex_reqs_to_rule(player, AnyReq([Req('Elevator Keycard'), logic.doublejump_req]))),
        LocationData('Varndagroth tower right (upper)', 'Varndagroth Towers (Right): Air vents left chest',  1337040, complex_reqs_to_rule(player, AnyReq([Req('Elevator Keycard'), logic.doublejump_req]))),
        LocationData('Varndagroth tower right (lower)', 'Varndagroth Towers (Right): Bottom floor',  1337041),
        LocationData('Varndagroth tower right (elevator)', 'Varndagroth Towers (Right): Varndagroth',  1337042, logic.has_keycard_C),
        LocationData('Varndagroth tower right (elevator)', 'Varndagroth Towers (Right): Spider Hell',  1337043, logic.has_keycard_A),
        LocationData('Skeleton Shaft', 'Sealed Caves (Xarion): Skeleton',  1337044),
        LocationData('Sealed Caves (Xarion)', 'Sealed Caves (Xarion): Shroom jump room',  1337045, logic.has_timestop),
        LocationData('Sealed Caves (Xarion)', 'Sealed Caves (Xarion): Double shroom room',  1337046),
        LocationData('Sealed Caves (Xarion)', 'Sealed Caves (Xarion): Mini jackpot room',  1337047, logic.has_forwarddash_doublejump),
        LocationData('Sealed Caves (Xarion)', 'Sealed Caves (Xarion): Below mini jackpot room',  1337048),
        LocationData('Sealed Caves (Xarion)', 'Sealed Caves (Xarion): Secret room',  1337049, logic.can_break_walls),
        LocationData('Sealed Caves (Xarion)', 'Sealed Caves (Xarion): Bottom left room',  1337050),
        LocationData('Sealed Caves (Xarion)', 'Sealed Caves (Xarion): Last chance before Xarion',  1337051, logic.has_doublejump),
        LocationData('Sealed Caves (Xarion)', 'Sealed Caves (Xarion): Xarion',  1337052, complex_reqs_to_rule(player, Req('Water Mask')) if flooded and flooded.flood_xarion else None),
        LocationData('Sealed Caves (Sirens)', 'Sealed Caves (Sirens): Water hook',  1337053, complex_reqs_to_rule(player, Req('Water Mask'))),
        LocationData('Sealed Caves (Sirens)', 'Sealed Caves (Sirens): Siren room underwater right',  1337054, complex_reqs_to_rule(player, Req('Water Mask'))),
        LocationData('Sealed Caves (Sirens)', 'Sealed Caves (Sirens): Siren room underwater left',  1337055, complex_reqs_to_rule(player, Req('Water Mask'))),
        LocationData('Sealed Caves (Sirens)', 'Sealed Caves (Sirens): Cave after sirens chest 1',  1337056),
        LocationData('Sealed Caves (Sirens)', 'Sealed Caves (Sirens): Cave after sirens chest 2',  1337057),
        LocationData('Military Fortress', 'Military Fortress: Bomber chest',  1337058, complex_reqs_to_rule(player, AllReq([Req('Timespinner Wheel'), logic.doublejump_req]))),
        LocationData('Military Fortress', 'Military Fortress: Close combat room',  1337059),
        LocationData('Military Fortress (hangar)', 'Military Fortress: Soldiers bridge',  1337060),
        LocationData('Military Fortress (hangar)', 'Military Fortress: Giantess room',  1337061),
        LocationData('Military Fortress (hangar)', 'Military Fortress: Giantess bridge',  1337062),
        LocationData('Military Fortress (hangar)', 'Military Fortress: B door chest 2',  1337063, complex_reqs_to_rule(player, AllReq([logic.keycard_B_req, Req('Water Mask') if flooded and flooded.flood_lab else logic.doublejump_req]))),
        LocationData('Military Fortress (hangar)', 'Military Fortress: B door chest 1',  1337064, complex_reqs_to_rule(player, AllReq([logic.keycard_B_req, Req('Water Mask') if flooded and flooded.flood_lab else logic.doublejump_req]))),
        LocationData('Military Fortress (hangar)', 'Military Fortress: Pedestal',  1337065, complex_reqs_to_rule(player, Req('Water Mask')) if flooded and flooded.flood_lab else complex_reqs_to_rule(player, AnyReq([logic.doublejump_of_npc_req, logic.forwarddash_doublejump_req]))),
        LocationData('The lab', 'Lab: Coffee break',  1337066),
        LocationData('The lab', 'Lab: Lower trash right',  1337067, logic.has_doublejump),
        LocationData('The lab', 'Lab: Lower trash left',  1337068, logic.has_upwarddash),
        LocationData('The lab', 'Lab: Below lab entrance',  1337069, logic.has_doublejump),
        LocationData('The lab (power off)', 'Lab: Trash jump room',  1337070),
        LocationData('The lab (power off)', 'Lab: Dynamo Works',  1337071),
        LocationData('The lab (upper)', 'Lab: Genza (Blob Mom)',  1337072),
        LocationData('The lab (power off)', 'Lab: Experiment #13',  1337073),
        LocationData('The lab (upper)', 'Lab: Download and chest room chest',  1337074),
        LocationData('The lab (upper)', 'Lab: Lab secret',  1337075, logic.can_break_walls),
        LocationData('The lab (power off)', 'Lab: Spider Hell',  1337076, logic.has_keycard_A),
        LocationData('Emperors tower', 'Emperor\'s Tower: Courtyard bottom chest',  1337077),
        LocationData('Emperors tower', 'Emperor\'s Tower: Courtyard floor secret',  1337078, complex_reqs_to_rule(player, AllReq([logic.upwarddash_req, logic.break_walls_req]))),
        LocationData('Emperors tower', 'Emperor\'s Tower: Courtyard upper chest',  1337079, logic.has_upwarddash),
        LocationData('Emperors tower', 'Emperor\'s Tower: Galactic sage room',  1337080),
        LocationData('Emperors tower', 'Emperor\'s Tower: Bottom right tower',  1337081),
        LocationData('Emperors tower', 'Emperor\'s Tower: Wayyyy up there',  1337082, logic.has_doublejump_of_npc),
        LocationData('Emperors tower', 'Emperor\'s Tower: Left tower balcony',  1337083),
        LocationData('Emperors tower', 'Emperor\'s Tower: Emperor\'s Chambers chest',  1337084),
        LocationData('Emperors tower', 'Emperor\'s Tower: Emperor\'s Chambers pedestal',  1337085),
        LocationData('Emperors tower', 'Killed Emperor', EventId),

        # Past item locations
        LocationData('Refugee Camp', 'Refugee Camp: Neliste\'s Bra',  1337086),
        LocationData('Refugee Camp', 'Refugee Camp: Storage chest 3',  1337087),
        LocationData('Refugee Camp', 'Refugee Camp: Storage chest 2',  1337088),
        LocationData('Refugee Camp', 'Refugee Camp: Storage chest 1',  1337089),
        LocationData('Forest', 'Forest: Refugee camp roof',  1337090),
        LocationData('Forest', 'Forest: Bat jump ledge',  1337091, complex_reqs_to_rule(player, AnyReq([logic.doublejump_of_npc_req, logic.forwarddash_doublejump_req, logic.fastjump_on_npc_req]))),
        LocationData('Forest', 'Forest: Green platform secret',  1337092, logic.can_break_walls),
        LocationData('Forest', 'Forest: Rats guarded chest',  1337093),
        LocationData('Forest', 'Forest: Waterfall chest 1',  1337094, complex_reqs_to_rule(player, Req('Water Mask'))),
        LocationData('Forest', 'Forest: Waterfall chest 2',  1337095, complex_reqs_to_rule(player, Req('Water Mask'))),
        LocationData('Forest', 'Forest: Batcave',  1337096),
        LocationData('Forest', 'Castle Ramparts: In the moat',  1337097, complex_reqs_to_rule(player, Req('Water Mask')) if flooded and flooded.flood_moat else None),
        LocationData('Left Side forest Caves', 'Forest: Before Serene single bat cave',  1337098),
        LocationData('Upper Lake Serene', 'Lake Serene (Upper): Rat nest',  1337099),
        LocationData('Upper Lake Serene', 'Lake Serene (Upper): Double jump cave platform',  1337100, logic.has_doublejump),
        LocationData('Upper Lake Serene', 'Lake Serene (Upper): Double jump cave floor',  1337101),
        LocationData('Upper Lake Serene', 'Lake Serene (Upper): Cave secret',  1337102, logic.can_break_walls),
        LocationData('Upper Lake Serene', 'Lake Serene: Before Big Bird', 1337175),
        LocationData('Upper Lake Serene', 'Lake Serene: Behind the vines',  1337103),
        LocationData('Upper Lake Serene', 'Lake Serene: Pyramid keys room',  1337104),
        LocationData('Upper Lake Serene', 'Lake Serene (Upper): Chicken ledge', 1337174),
        LocationData('Lower Lake Serene', 'Lake Serene (Lower): Deep dive',  1337105),
        LocationData('Left Side forest Caves', 'Lake Serene (Lower): Under the eels',  1337106, complex_reqs_to_rule(player, Req('Water Mask'))),
        LocationData('Lower Lake Serene', 'Lake Serene (Lower): Water spikes room',  1337107),
        LocationData('Lower Lake Serene', 'Lake Serene (Lower): Underwater secret',  1337108, logic.can_break_walls),
        LocationData('Lower Lake Serene', 'Lake Serene (Lower): T chest',  1337109, logic.has_doublejump_of_npc if flooded and not flooded.flood_lake_serene else None),
        LocationData('Left Side forest Caves', 'Lake Serene (Lower): Past the eels',  1337110, complex_reqs_to_rule(player, Req('Water Mask'))),
        LocationData('Lower Lake Serene', 'Lake Serene (Lower): Underwater pedestal',  1337111, logic.has_doublejump if flooded and not flooded.flood_lake_serene else None),
        LocationData('Caves of Banishment (upper)', 'Caves of Banishment (Maw): Shroom jump room',  1337112, logic.has_doublejump if flooded and not flooded.flood_maw else None),
        LocationData('Caves of Banishment (upper)', 'Caves of Banishment (Maw): Secret room',  1337113, complex_reqs_to_rule(player, AllReq([logic.break_walls_req, Req('Water Mask') if flooded and flooded.flood_maw else None]))),
        LocationData('Caves of Banishment (upper)', 'Caves of Banishment (Maw): Bottom left room',  1337114, complex_reqs_to_rule(player, Req('Water Mask')) if flooded and flooded.flood_maw else None),
        LocationData('Caves of Banishment (upper)', 'Caves of Banishment (Maw): Single shroom room',  1337115),
        LocationData('Caves of Banishment (upper)', 'Caves of Banishment (Maw): Jackpot room chest 1',  1337116, logic.has_forwarddash_doublejump if flooded and not flooded.flood_maw else None),
        LocationData('Caves of Banishment (upper)', 'Caves of Banishment (Maw): Jackpot room chest 2',  1337117, logic.has_forwarddash_doublejump if flooded and not flooded.flood_maw else None),
        LocationData('Caves of Banishment (upper)', 'Caves of Banishment (Maw): Jackpot room chest 3',  1337118, logic.has_forwarddash_doublejump if flooded and not flooded.flood_maw else None),
        LocationData('Caves of Banishment (upper)', 'Caves of Banishment (Maw): Jackpot room chest 4',  1337119, logic.has_forwarddash_doublejump if flooded and not flooded.flood_maw else None),
        LocationData('Caves of Banishment (upper)', 'Caves of Banishment (Maw): Pedestal',  1337120, complex_reqs_to_rule(player, Req('Water Mask')) if flooded and flooded.flood_maw else None),
        LocationData('Caves of Banishment (Maw)', 'Caves of Banishment (Maw): Last chance before Maw',  1337121, complex_reqs_to_rule(player, Req('Water Mask')) if flooded and flooded.flood_maw else logic.has_doublejump),
        LocationData('Caves of Banishment (Maw)', 'Caves of Banishment (Maw): Plasma Crystal', 1337173, complex_reqs_to_rule(player, AllReq([AnyReq([Req('Gas Mask'), Req('Talaria Attachment')]),
                                                                                                                                             Req('Water Mask') if flooded and flooded.flood_maw else None]))),
        LocationData('Caves of Banishment (Maw)', 'Killed Maw',  EventId, complex_reqs_to_rule(player, AllReq([Req('Gas Mask'), Req('Water Mask') if flooded and flooded.flood_maw else None]))),
        LocationData('Caves of Banishment (Maw)', 'Caves of Banishment (Maw): Mineshaft',  1337122, complex_reqs_to_rule(player, AllReq([AnyReq([Req('Gas Mask'), Req('Talaria Attachment')]),
                                                                                                                                         Req('Water Mask') if flooded and flooded.flood_maw else None]))),
        LocationData('Caves of Banishment (Sirens)', 'Caves of Banishment (Sirens): Wyvern room',  1337123),
        LocationData('Caves of Banishment (Sirens)', 'Caves of Banishment (Sirens): Siren room above water chest',  1337124),
        LocationData('Caves of Banishment (Sirens)', 'Caves of Banishment (Sirens): Siren room underwater left chest',  1337125, complex_reqs_to_rule(player, Req('Water Mask'))),
        LocationData('Caves of Banishment (Sirens)', 'Caves of Banishment (Sirens): Siren room underwater right chest',  1337126, complex_reqs_to_rule(player, Req('Water Mask'))),
        LocationData('Caves of Banishment (Sirens)', 'Caves of Banishment (Sirens): Siren room underwater right ground', 1337172, complex_reqs_to_rule(player, Req('Water Mask'))),
        LocationData('Caves of Banishment (Sirens)', 'Caves of Banishment (Sirens): Water hook',  1337127, complex_reqs_to_rule(player, Req('Water Mask'))),
        LocationData('Castle Ramparts', 'Castle Ramparts: Bomber chest',  1337128, logic.has_multiple_small_jumps_of_npc),
        LocationData('Castle Ramparts', 'Castle Ramparts: Freeze the engineer',  1337129, complex_reqs_to_rule(player, AnyReq([Req('Talaria Attachment'), logic.timestop_req]))),
        LocationData('Castle Ramparts', 'Castle Ramparts: Giantess guarded room',  1337130),
        LocationData('Castle Ramparts', 'Castle Ramparts: Knight and archer guarded room',  1337131),
        LocationData('Castle Ramparts', 'Castle Ramparts: Pedestal',  1337132),
        LocationData('Castle Basement', 'Castle Basement: Secret pedestal',  1337133, logic.can_break_walls),
        LocationData('Castle Basement', 'Castle Basement: Clean the castle basement',  1337134),
        LocationData('Royal towers (lower)', 'Castle Keep: Yas queen room',  1337135, logic.has_pink),
        LocationData('Castle Basement', 'Castle Basement: Giantess guarded chest',  1337136),
        LocationData('Castle Basement', 'Castle Basement: Omelette chest',  1337137),
        LocationData('Castle Basement', 'Castle Basement: Just an egg',  1337138),
        LocationData('Castle Keep', 'Castle Keep: Under the twins',  1337139),
        LocationData('Castle Keep', 'Killed Twins',  EventId, logic.has_timestop),
        LocationData('Castle Keep', 'Castle Keep: Advisor jump', 1337171, logic.has_timestop),
        LocationData('Castle Keep', 'Castle Keep: Twins',  1337140, logic.has_timestop),
        LocationData('Castle Keep', 'Castle Keep: Royal guard tiny room',  1337141, complex_reqs_to_rule(player, AnyReq([logic.doublejump_req, logic.fastjump_on_npc_req]))),
        LocationData('Royal towers (lower)', 'Royal Towers: Floor secret',  1337142, complex_reqs_to_rule(player, AllReq([logic.doublejump_req, logic.break_walls_req]))),
        LocationData('Royal towers', 'Royal Towers: Pre-climb gap',  1337143),
        LocationData('Royal towers', 'Royal Towers: Long balcony',  1337144, complex_reqs_to_rule(player, Req('Water Mask')) if flooded and flooded.flood_courtyard else None),
        LocationData('Royal towers', 'Royal Towers: Past bottom struggle juggle',  1337145, logic.has_doublejump_of_npc if flooded and not flooded.flood_courtyard else None),
        LocationData('Royal towers', 'Royal Towers: Bottom struggle juggle',  1337146, logic.has_doublejump_of_npc),
        LocationData('Royal towers (upper)', 'Royal Towers: Top struggle juggle',  1337147, logic.has_doublejump_of_npc),
        LocationData('Royal towers (upper)', 'Royal Towers: No struggle required',  1337148),
        LocationData('Royal towers', 'Royal Towers: Right tower freebie',  1337149),
        LocationData('Royal towers (upper)', 'Royal Towers: Left tower small balcony',  1337150),
        LocationData('Royal towers (upper)', 'Royal Towers: Left tower royal guard',  1337151),
        LocationData('Royal towers (upper)', 'Royal Towers: Before Aelana',  1337152),
        LocationData('Royal towers (upper)', 'Killed Aelana',  EventId),
        LocationData('Royal towers (upper)', 'Royal Towers: Aelana\'s attic',  1337153, logic.has_upwarddash),
        LocationData('Royal towers (upper)', 'Royal Towers: Aelana\'s chest',  1337154),
        LocationData('Royal towers (upper)', 'Royal Towers: Aelana\'s pedestal',  1337155),

        # Ancient pyramid locations
        LocationData('Ancient Pyramid (entrance)', 'Ancient Pyramid: Why not it\'s right there',  1337246),
        LocationData('Ancient Pyramid (left)', 'Ancient Pyramid: Conviction guarded room',  1337247),
        LocationData('Ancient Pyramid (left)', 'Ancient Pyramid: Pit secret room',  1337248, complex_reqs_to_rule(player, AllReq([logic.break_walls_req, Req('Water Mask') if flooded and flooded.flood_pyramid_shaft else None]))),
        LocationData('Ancient Pyramid (left)', 'Ancient Pyramid: Regret chest',  1337249, complex_reqs_to_rule(player, AllReq([logic.break_walls_req, Req('Water Mask') if flooded and flooded.flood_pyramid_shaft else logic.doublejump_req]))),
        LocationData('Ancient Pyramid (right)', 'Ancient Pyramid: Nightmare Door chest',  1337236, complex_reqs_to_rule(player, Req('Water Mask')) if flooded and flooded.flood_pyramid_back else None),
        LocationData('Ancient Pyramid (right)', 'Killed Nightmare', EventId, complex_reqs_to_rule(player, AllReq([logic.all_timespinner_pieces_req, Req('Water Mask') if flooded and flooded.flood_pyramid_back else None])))
    ]

    # 1337156 - 1337170 Downloads
    if not options or options.downloadable_items:
        has_tablet = complex_reqs_to_rule(player, Req('Tablet'))
        has_tablet_v = complex_reqs_to_rule(player, AllReq([Req('Tablet'), Req('Library Keycard V')]))
        has_tablet_b = complex_reqs_to_rule(player, AllReq([Req('Tablet'), logic.keycard_B_req]))
        location_table += ( 
            LocationData('Library', 'Library: Terminal 2 (Lachiem)',  1337156, has_tablet),
            LocationData('Library', 'Library: Terminal 1 (Windaria)',  1337157, has_tablet),
            # 1337158 Is lost in time
            LocationData('Library', 'Library: Terminal 3 (Emperor Nuvius)',  1337159, has_tablet),
            LocationData('Library', 'Library: V terminal 1 (War of the Sisters)',  1337160, has_tablet_v),
            LocationData('Library', 'Library: V terminal 2 (Lake Desolation Map)',  1337161, has_tablet_v),
            LocationData('Library', 'Library: V terminal 3 (Vilete)',  1337162, has_tablet_v),
            LocationData('Library top', 'Library: Backer room terminal (Vandagray Metropolis Map)',  1337163, has_tablet),
            LocationData('Varndagroth tower right (elevator)', 'Varndagroth Towers (Right): Medbay terminal (Bleakness Research)',  1337164, has_tablet_b),
            LocationData('The lab (upper)', 'Lab: Download and chest room terminal (Experiment #13)',  1337165, has_tablet),
            LocationData('The lab (power off)', 'Lab: Middle terminal (Amadeus Laboratory Map)',  1337166, has_tablet),
            LocationData('The lab (power off)', 'Lab: Sentry platform terminal (Origins)',  1337167, has_tablet),
            LocationData('The lab', 'Lab: Experiment 13 terminal (W.R.E.C Farewell)',  1337168, has_tablet),
            LocationData('The lab', 'Lab: Left terminal (Biotechnology)',  1337169, has_tablet),
            LocationData('The lab (power off)', 'Lab: Right terminal (Experiment #11)',  1337170, has_tablet)
        )

    # 1337176 - 1337176 Cantoran
    if not options or options.cantoran:
        location_table += (
            LocationData('Left Side forest Caves', 'Lake Serene: Cantoran',  1337176),
        )

    # 1337177 - 1337198 Lore Checks
    if not options or options.lore_checks:
        location_table += (
            LocationData('Lower lake desolation', 'Lake Desolation: Memory - Coyote Jump (Time Messenger)',  1337177),
            LocationData('Library', 'Library: Memory - Waterway (A Message)',  1337178),
            LocationData('Library top', 'Library: Memory - Library Gap (Lachiemi Sun)',  1337179),
            LocationData('Library top', 'Library: Memory - Mr. Hat Portrait (Moonlit Night)',  1337180),
            LocationData('Varndagroth tower left', 'Varndagroth Towers (Left): Memory - Elevator (Nomads)',  1337181, complex_reqs_to_rule(player, Req('Elevator Keycard'))),
            LocationData('Varndagroth tower right (lower)', 'Varndagroth Towers: Memory - Siren Elevator (Childhood)',  1337182, logic.has_keycard_B),
            LocationData('Varndagroth tower right (lower)', 'Varndagroth Towers (Right): Memory - Bottom (Faron)',  1337183),
            LocationData('Military Fortress', 'Military Fortress: Memory - Bomber Climb (A Solution)',  1337184, complex_reqs_to_rule(player, AllReq([Req('Timespinner Wheel'), logic.doublejump_of_npc_req]))),
            LocationData('The lab', 'Lab: Memory - Genza\'s Secret Stash 1 (An Old Friend)',  1337185, logic.can_break_walls),
            LocationData('The lab', 'Lab: Memory - Genza\'s Secret Stash 2 (Twilight Dinner)',  1337186, logic.can_break_walls),
            LocationData('Emperors tower', 'Emperor\'s Tower: Memory - Way Up There (Final Circle)',  1337187, logic.has_doublejump_of_npc),
            LocationData('Forest', 'Forest: Journal - Rats (Lachiem Expedition)',  1337188),
            LocationData('Forest', 'Forest: Journal - Bat Jump Ledge (Peace Treaty)',  1337189, complex_reqs_to_rule(player, AnyReq([logic.doublejump_of_npc_req, logic.forwarddash_doublejump_req, logic.fastjump_on_npc_req]))),
            LocationData('Forest', 'Forest: Journal - Floating in Moat (Prime Edicts)',  1337190, complex_reqs_to_rule(player, Req('Water Mask')) if flooded and flooded.flood_moat else None),
            LocationData('Castle Ramparts', 'Castle Ramparts: Journal - Archer + Knight (Declaration of Independence)',  1337191),
            LocationData('Castle Keep', 'Castle Keep: Journal - Under the Twins (Letter of Reference)',  1337192),
            LocationData('Castle Basement', 'Castle Basement: Journal - Castle Loop Giantess (Political Advice)',  1337193),
            LocationData('Royal towers (lower)', 'Royal Towers: Journal - Aelana\'s Room (Diplomatic Missive)',  1337194, logic.has_pink),
            LocationData('Royal towers (upper)', 'Royal Towers: Journal - Top Struggle Juggle Base (War of the Sisters)',  1337195),
            LocationData('Royal towers (upper)', 'Royal Towers: Journal - Aelana Boss (Stained Letter)',  1337196),
            LocationData('Royal towers', 'Royal Towers: Journal - Near Bottom Struggle Juggle (Mission Findings)',  1337197, logic.has_doublejump_of_npc if flooded and not flooded.flood_courtyard else None),
            LocationData('Caves of Banishment (Maw)', 'Caves of Banishment (Maw): Journal - Lower Left Caves (Naivety)',  1337198, complex_reqs_to_rule(player, Req('Water Mask')) if flooded and flooded.flood_maw else None)
        )

    # 1337199 - 1337236 Reserved for future use

    # 1337237 - 1337245 GyreArchives
    if not options or options.gyre_archives:
        location_table += (
            LocationData('Ravenlord\'s Lair', 'Ravenlord: Post fight (pedestal)',  1337237),
            LocationData('Ifrit\'s Lair', 'Ifrit: Post fight (pedestal)',  1337238),
            LocationData('Temporal Gyre', 'Temporal Gyre: Chest 1',  1337239),
            LocationData('Temporal Gyre', 'Temporal Gyre: Chest 2',  1337240),
            LocationData('Temporal Gyre', 'Temporal Gyre: Chest 3',  1337241),
            LocationData('Ravenlord\'s Lair', 'Ravenlord: Pre fight',  1337242),
            LocationData('Ravenlord\'s Lair', 'Ravenlord: Post fight (chest)',  1337243),
            LocationData('Ifrit\'s Lair', 'Ifrit: Pre fight',  1337244),
            LocationData('Ifrit\'s Lair', 'Ifrit: Post fight (chest)', 1337245),
        )
 
    return location_table
