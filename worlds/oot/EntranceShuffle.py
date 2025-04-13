from itertools import chain
import logging

from worlds.generic.Rules import set_rule, add_rule
from BaseClasses import CollectionState

from .Hints import get_hint_area, HintAreaNotFound
from .Regions import TimeOfDay


def set_all_entrances_data(world, player):
    for type, forward_entry, *return_entry in entrance_shuffle_table:
        forward_entrance = world.get_entrance(forward_entry[0], player)
        forward_entrance.data = forward_entry[1]
        forward_entrance.type = type
        forward_entrance.primary = True
        if type == 'Grotto':
            forward_entrance.data['index'] = 0x1000 + forward_entrance.data['grotto_id']
        if return_entry:
            return_entry = return_entry[0]
            return_entrance = world.get_entrance(return_entry[0], player)
            return_entrance.data = return_entry[1]
            return_entrance.type = type
            forward_entrance.bind_two_way(return_entrance)
            if type == 'Grotto':
                return_entrance.data['index'] = 0x7FFF


def assume_entrance_pool(entrance_pool, ootworld, pool_type):
    assumed_pool = []
    for entrance in entrance_pool:
        assumed_forward = entrance.assume_reachable(pool_type)
        if entrance.reverse != None and not ootworld.decouple_entrances:
            assumed_return = entrance.reverse.assume_reachable(pool_type)
            if not (ootworld.mix_entrance_pools != 'off' and (ootworld.shuffle_overworld_entrances or ootworld.shuffle_special_interior_entrances)):
                if (entrance.type in ('Dungeon', 'Grotto', 'Grave') and entrance.reverse.name != 'Spirit Temple Lobby -> Desert Colossus From Spirit Lobby') or \
                   (entrance.type == 'Interior' and ootworld.shuffle_special_interior_entrances):
                    # In most cases, Dungeon, Grotto/Grave and Simple Interior exits shouldn't be assumed able to give access to their parent region
                    set_rule(assumed_return, lambda state, **kwargs: False)
            assumed_forward.bind_two_way(assumed_return)
        assumed_pool.append(assumed_forward)
    return assumed_pool


def build_one_way_targets(world, pool, types_to_include, exclude=(), target_region_names=()):
    one_way_entrances = []
    for pool_type in types_to_include:
        one_way_entrances += world.get_shufflable_entrances(type=pool_type)
    valid_one_way_entrances = list(filter(lambda entrance: entrance.name not in exclude, one_way_entrances))
    if target_region_names:
        return [entrance.get_new_target(pool) for entrance in valid_one_way_entrances
                if entrance.connected_region.name in target_region_names]
    return [entrance.get_new_target(pool) for entrance in valid_one_way_entrances]


#   Abbreviations
#       DMC     Death Mountain Crater
#       DMT     Death Mountain Trail
#       GC      Goron City
#       GF      Gerudo Fortress
#       GS      Gold Skulltula
#       GV      Gerudo Valley
#       HC      Hyrule Castle
#       HF      Hyrule Field
#       KF      Kokiri Forest
#       LH      Lake Hylia
#       LLR     Lon Lon Ranch
#       LW      Lost Woods
#       OGC     Outside Ganon's Castle
#       SFM     Sacred Forest Meadow
#       ToT     Temple of Time
#       ZD      Zora's Domain
#       ZF      Zora's Fountain
#       ZR      Zora's River

entrance_shuffle_table = [
    ('Dungeon',         ('KF Outside Deku Tree -> Deku Tree Lobby',                         { 'index': 0x0000 }),
                        ('Deku Tree Lobby -> KF Outside Deku Tree',                         { 'index': 0x0209, 'blue_warp': 0x0457 })),
    ('Dungeon',         ('Death Mountain -> Dodongos Cavern Beginning',                     { 'index': 0x0004 }),
                        ('Dodongos Cavern Beginning -> Death Mountain',                     { 'index': 0x0242, 'blue_warp': 0x047A })),
    ('Dungeon',         ('Zoras Fountain -> Jabu Jabus Belly Beginning',                    { 'index': 0x0028 }),
                        ('Jabu Jabus Belly Beginning -> Zoras Fountain',                    { 'index': 0x0221, 'blue_warp': 0x010E })),
    ('Dungeon',         ('SFM Forest Temple Entrance Ledge -> Forest Temple Lobby',         { 'index': 0x0169 }),
                        ('Forest Temple Lobby -> SFM Forest Temple Entrance Ledge',         { 'index': 0x0215, 'blue_warp': 0x0608 })),
    ('Dungeon',         ('DMC Fire Temple Entrance -> Fire Temple Lower',                   { 'index': 0x0165 }),
                        ('Fire Temple Lower -> DMC Fire Temple Entrance',                   { 'index': 0x024A, 'blue_warp': 0x0564 })),
    ('Dungeon',         ('Lake Hylia -> Water Temple Lobby',                                { 'index': 0x0010 }),
                        ('Water Temple Lobby -> Lake Hylia',                                { 'index': 0x021D, 'blue_warp': 0x060C })),
    ('Dungeon',         ('Desert Colossus -> Spirit Temple Lobby',                          { 'index': 0x0082 }),
                        ('Spirit Temple Lobby -> Desert Colossus From Spirit Lobby',        { 'index': 0x01E1, 'blue_warp': 0x0610 })),
    ('Dungeon',         ('Graveyard Warp Pad Region -> Shadow Temple Entryway',             { 'index': 0x0037 }),
                        ('Shadow Temple Entryway -> Graveyard Warp Pad Region',             { 'index': 0x0205, 'blue_warp': 0x0580 })),
    ('Dungeon',         ('Kakariko Village -> Bottom of the Well',                          { 'index': 0x0098 }),
                        ('Bottom of the Well -> Kakariko Village',                          { 'index': 0x02A6 })),
    ('Dungeon',         ('ZF Ice Ledge -> Ice Cavern Beginning',                            { 'index': 0x0088 }),
                        ('Ice Cavern Beginning -> ZF Ice Ledge',                            { 'index': 0x03D4 })),
    ('Dungeon',         ('Gerudo Fortress -> Gerudo Training Ground Lobby',                 { 'index': 0x0008 }),
                        ('Gerudo Training Ground Lobby -> Gerudo Fortress',                 { 'index': 0x03A8 })),
    ('DungeonSpecial',  ('Ganons Castle Grounds -> Ganons Castle Lobby',                    { 'index': 0x0467 }),
                        ('Ganons Castle Lobby -> Castle Grounds From Ganons Castle',        { 'index': 0x023D })),

    ('Interior',        ('Kokiri Forest -> KF Midos House',                                 { 'index': 0x0433 }),
                        ('KF Midos House -> Kokiri Forest',                                 { 'index': 0x0443 })),
    ('Interior',        ('Kokiri Forest -> KF Sarias House',                                { 'index': 0x0437 }),
                        ('KF Sarias House -> Kokiri Forest',                                { 'index': 0x0447 })),
    ('Interior',        ('Kokiri Forest -> KF House of Twins',                              { 'index': 0x009C }),
                        ('KF House of Twins -> Kokiri Forest',                              { 'index': 0x033C })),
    ('Interior',        ('Kokiri Forest -> KF Know It All House',                           { 'index': 0x00C9 }),
                        ('KF Know It All House -> Kokiri Forest',                           { 'index': 0x026A })),
    ('Interior',        ('Kokiri Forest -> KF Kokiri Shop',                                 { 'index': 0x00C1 }),
                        ('KF Kokiri Shop -> Kokiri Forest',                                 { 'index': 0x0266 })),
    ('Interior',        ('Lake Hylia -> LH Lab',                                            { 'index': 0x0043 }),
                        ('LH Lab -> Lake Hylia',                                            { 'index': 0x03CC })),
    ('Interior',        ('LH Fishing Island -> LH Fishing Hole',                            { 'index': 0x045F }),
                        ('LH Fishing Hole -> LH Fishing Island',                            { 'index': 0x0309 })),
    ('Interior',        ('GV Fortress Side -> GV Carpenter Tent',                           { 'index': 0x03A0 }),
                        ('GV Carpenter Tent -> GV Fortress Side',                           { 'index': 0x03D0 })),
    ('Interior',        ('Market Entrance -> Market Guard House',                           { 'index': 0x007E }),
                        ('Market Guard House -> Market Entrance',                           { 'index': 0x026E })),
    ('Interior',        ('Market -> Market Mask Shop',                                      { 'index': 0x0530 }),
                        ('Market Mask Shop -> Market',                                      { 'index': 0x01D1, 'addresses': [0xC6DA5E] })),
    ('Interior',        ('Market -> Market Bombchu Bowling',                                { 'index': 0x0507 }),
                        ('Market Bombchu Bowling -> Market',                                { 'index': 0x03BC })),
    ('Interior',        ('Market -> Market Potion Shop',                                    { 'index': 0x0388 }),
                        ('Market Potion Shop -> Market',                                    { 'index': 0x02A2 })),
    ('Interior',        ('Market -> Market Treasure Chest Game',                            { 'index': 0x0063 }),
                        ('Market Treasure Chest Game -> Market',                            { 'index': 0x01D5 })),
    ('Interior',        ('Market Back Alley -> Market Bombchu Shop',                        { 'index': 0x0528 }),
                        ('Market Bombchu Shop -> Market Back Alley',                        { 'index': 0x03C0 })),
    ('Interior',        ('Market Back Alley -> Market Man in Green House',                  { 'index': 0x043B }),
                        ('Market Man in Green House -> Market Back Alley',                  { 'index': 0x0067 })),
    ('Interior',        ('Kakariko Village -> Kak Carpenter Boss House',                    { 'index': 0x02FD }),
                        ('Kak Carpenter Boss House -> Kakariko Village',                    { 'index': 0x0349 })),
    ('Interior',        ('Kakariko Village -> Kak House of Skulltula',                      { 'index': 0x0550 }),
                        ('Kak House of Skulltula -> Kakariko Village',                      { 'index': 0x04EE })),
    ('Interior',        ('Kakariko Village -> Kak Impas House',                             { 'index': 0x039C }),
                        ('Kak Impas House -> Kakariko Village',                             { 'index': 0x0345 })),
    ('Interior',        ('Kak Impas Ledge -> Kak Impas House Back',                         { 'index': 0x05C8 }),
                        ('Kak Impas House Back -> Kak Impas Ledge',                         { 'index': 0x05DC })),
    ('Interior',        ('Kak Backyard -> Kak Odd Medicine Building',                       { 'index': 0x0072 }),
                        ('Kak Odd Medicine Building -> Kak Backyard',                       { 'index': 0x034D })),
    ('Interior',        ('Graveyard -> Graveyard Dampes House',                             { 'index': 0x030D }),
                        ('Graveyard Dampes House -> Graveyard',                             { 'index': 0x0355 })),
    ('Interior',        ('Goron City -> GC Shop',                                           { 'index': 0x037C }),
                        ('GC Shop -> Goron City',                                           { 'index': 0x03FC })),
    ('Interior',        ('Zoras Domain -> ZD Shop',                                         { 'index': 0x0380 }),
                        ('ZD Shop -> Zoras Domain',                                         { 'index': 0x03C4 })),
    ('Interior',        ('Lon Lon Ranch -> LLR Talons House',                               { 'index': 0x004F }),
                        ('LLR Talons House -> Lon Lon Ranch',                               { 'index': 0x0378 })),
    ('Interior',        ('Lon Lon Ranch -> LLR Stables',                                    { 'index': 0x02F9 }),
                        ('LLR Stables -> Lon Lon Ranch',                                    { 'index': 0x042F })),
    ('Interior',        ('Lon Lon Ranch -> LLR Tower',                                      { 'index': 0x05D0 }),
                        ('LLR Tower -> Lon Lon Ranch',                                      { 'index': 0x05D4 })),
    ('Interior',        ('Market -> Market Bazaar',                                         { 'index': 0x052C }),
                        ('Market Bazaar -> Market',                                         { 'index': 0x03B8, 'addresses': [0xBEFD74] })),
    ('Interior',        ('Market -> Market Shooting Gallery',                               { 'index': 0x016D }),
                        ('Market Shooting Gallery -> Market',                               { 'index': 0x01CD, 'addresses': [0xBEFD7C] })),
    ('Interior',        ('Kakariko Village -> Kak Bazaar',                                  { 'index': 0x00B7 }),
                        ('Kak Bazaar -> Kakariko Village',                                  { 'index': 0x0201, 'addresses': [0xBEFD72] })),
    ('Interior',        ('Kakariko Village -> Kak Shooting Gallery',                        { 'index': 0x003B }),
                        ('Kak Shooting Gallery -> Kakariko Village',                        { 'index': 0x0463, 'addresses': [0xBEFD7A] })),
    ('Interior',        ('Desert Colossus -> Colossus Great Fairy Fountain',                { 'index': 0x0588 }),
                        ('Colossus Great Fairy Fountain -> Desert Colossus',                { 'index': 0x057C, 'addresses': [0xBEFD82] })),
    ('Interior',        ('Hyrule Castle Grounds -> HC Great Fairy Fountain',                { 'index': 0x0578 }),
                        ('HC Great Fairy Fountain -> Castle Grounds',                       { 'index': 0x0340, 'addresses': [0xBEFD80] })),
    ('Interior',        ('Ganons Castle Grounds -> OGC Great Fairy Fountain',               { 'index': 0x04C2 }),
                        ('OGC Great Fairy Fountain -> Castle Grounds',                      { 'index': 0x0340, 'addresses': [0xBEFD6C] })),
    ('Interior',        ('DMC Lower Nearby -> DMC Great Fairy Fountain',                    { 'index': 0x04BE }),
                        ('DMC Great Fairy Fountain -> DMC Lower Local',                     { 'index': 0x0482, 'addresses': [0xBEFD6A] })),
    ('Interior',        ('Death Mountain Summit -> DMT Great Fairy Fountain',               { 'index': 0x0315 }),
                        ('DMT Great Fairy Fountain -> Death Mountain Summit',               { 'index': 0x045B, 'addresses': [0xBEFD68] })),
    ('Interior',        ('Zoras Fountain -> ZF Great Fairy Fountain',                       { 'index': 0x0371 }),
                        ('ZF Great Fairy Fountain -> Zoras Fountain',                       { 'index': 0x0394, 'addresses': [0xBEFD7E] })),

    ('SpecialInterior', ('Kokiri Forest -> KF Links House',                                 { 'index': 0x0272 }),
                        ('KF Links House -> Kokiri Forest',                                 { 'index': 0x0211 })),
    ('SpecialInterior', ('ToT Entrance -> Temple of Time',                                  { 'index': 0x0053 }),
                        ('Temple of Time -> ToT Entrance',                                  { 'index': 0x0472 })),
    ('SpecialInterior', ('Kakariko Village -> Kak Windmill',                                { 'index': 0x0453 }),
                        ('Kak Windmill -> Kakariko Village',                                { 'index': 0x0351 })),
    ('SpecialInterior', ('Kakariko Village -> Kak Potion Shop Front',                       { 'index': 0x0384 }),
                        ('Kak Potion Shop Front -> Kakariko Village',                       { 'index': 0x044B })),
    ('SpecialInterior', ('Kak Backyard -> Kak Potion Shop Back',                            { 'index': 0x03EC }),
                        ('Kak Potion Shop Back -> Kak Backyard',                            { 'index': 0x04FF })),

    ('Grotto',          ('Desert Colossus -> Colossus Grotto',                              { 'grotto_id': 0x00, 'entrance': 0x05BC, 'content': 0xFD, 'scene': 0x5C }),
                        ('Colossus Grotto -> Desert Colossus',                              { 'grotto_id': 0x00 })),
    ('Grotto',          ('Lake Hylia -> LH Grotto',                                         { 'grotto_id': 0x01, 'entrance': 0x05A4, 'content': 0xEF, 'scene': 0x57 }),
                        ('LH Grotto -> Lake Hylia',                                         { 'grotto_id': 0x01 })),
    ('Grotto',          ('Zora River -> ZR Storms Grotto',                                  { 'grotto_id': 0x02, 'entrance': 0x05BC, 'content': 0xEB, 'scene': 0x54 }),
                        ('ZR Storms Grotto -> Zora River',                                  { 'grotto_id': 0x02 })),
    ('Grotto',          ('Zora River -> ZR Fairy Grotto',                                   { 'grotto_id': 0x03, 'entrance': 0x036D, 'content': 0xE6, 'scene': 0x54 }),
                        ('ZR Fairy Grotto -> Zora River',                                   { 'grotto_id': 0x03 })),
    ('Grotto',          ('Zora River -> ZR Open Grotto',                                    { 'grotto_id': 0x04, 'entrance': 0x003F, 'content': 0x29, 'scene': 0x54 }),
                        ('ZR Open Grotto -> Zora River',                                    { 'grotto_id': 0x04 })),
    ('Grotto',          ('DMC Lower Nearby -> DMC Hammer Grotto',                           { 'grotto_id': 0x05, 'entrance': 0x05A4, 'content': 0xF9, 'scene': 0x61 }),
                        ('DMC Hammer Grotto -> DMC Lower Local',                            { 'grotto_id': 0x05 })),
    ('Grotto',          ('DMC Upper Nearby -> DMC Upper Grotto',                            { 'grotto_id': 0x06, 'entrance': 0x003F, 'content': 0x7A, 'scene': 0x61 }),
                        ('DMC Upper Grotto -> DMC Upper Local',                             { 'grotto_id': 0x06 })),
    ('Grotto',          ('GC Grotto Platform -> GC Grotto',                                 { 'grotto_id': 0x07, 'entrance': 0x05A4, 'content': 0xFB, 'scene': 0x62 }),
                        ('GC Grotto -> GC Grotto Platform',                                 { 'grotto_id': 0x07 })),
    ('Grotto',          ('Death Mountain -> DMT Storms Grotto',                             { 'grotto_id': 0x08, 'entrance': 0x003F, 'content': 0x57, 'scene': 0x60 }),
                        ('DMT Storms Grotto -> Death Mountain',                             { 'grotto_id': 0x08 })),
    ('Grotto',          ('Death Mountain Summit -> DMT Cow Grotto',                         { 'grotto_id': 0x09, 'entrance': 0x05FC, 'content': 0xF8, 'scene': 0x60 }),
                        ('DMT Cow Grotto -> Death Mountain Summit',                         { 'grotto_id': 0x09 })),
    ('Grotto',          ('Kak Backyard -> Kak Open Grotto',                                 { 'grotto_id': 0x0A, 'entrance': 0x003F, 'content': 0x28, 'scene': 0x52 }),
                        ('Kak Open Grotto -> Kak Backyard',                                 { 'grotto_id': 0x0A })),
    ('Grotto',          ('Kakariko Village -> Kak Redead Grotto',                           { 'grotto_id': 0x0B, 'entrance': 0x05A0, 'content': 0xE7, 'scene': 0x52 }),
                        ('Kak Redead Grotto -> Kakariko Village',                           { 'grotto_id': 0x0B })),
    ('Grotto',          ('Hyrule Castle Grounds -> HC Storms Grotto',                       { 'grotto_id': 0x0C, 'entrance': 0x05B8, 'content': 0xF6, 'scene': 0x5F }),
                        ('HC Storms Grotto -> Castle Grounds',                              { 'grotto_id': 0x0C })),
    ('Grotto',          ('Hyrule Field -> HF Tektite Grotto',                               { 'grotto_id': 0x0D, 'entrance': 0x05C0, 'content': 0xE1, 'scene': 0x51 }),
                        ('HF Tektite Grotto -> Hyrule Field',                               { 'grotto_id': 0x0D })),
    ('Grotto',          ('Hyrule Field -> HF Near Kak Grotto',                              { 'grotto_id': 0x0E, 'entrance': 0x0598, 'content': 0xE5, 'scene': 0x51 }),
                        ('HF Near Kak Grotto -> Hyrule Field',                              { 'grotto_id': 0x0E })),
    ('Grotto',          ('Hyrule Field -> HF Fairy Grotto',                                 { 'grotto_id': 0x0F, 'entrance': 0x036D, 'content': 0xFF, 'scene': 0x51 }),
                        ('HF Fairy Grotto -> Hyrule Field',                                 { 'grotto_id': 0x0F })),
    ('Grotto',          ('Hyrule Field -> HF Near Market Grotto',                           { 'grotto_id': 0x10, 'entrance': 0x003F, 'content': 0x00, 'scene': 0x51 }),
                        ('HF Near Market Grotto -> Hyrule Field',                           { 'grotto_id': 0x10 })),
    ('Grotto',          ('Hyrule Field -> HF Cow Grotto',                                   { 'grotto_id': 0x11, 'entrance': 0x05A8, 'content': 0xE4, 'scene': 0x51 }),
                        ('HF Cow Grotto -> Hyrule Field',                                   { 'grotto_id': 0x11 })),
    ('Grotto',          ('Hyrule Field -> HF Inside Fence Grotto',                          { 'grotto_id': 0x12, 'entrance': 0x059C, 'content': 0xE6, 'scene': 0x51 }),
                        ('HF Inside Fence Grotto -> Hyrule Field',                          { 'grotto_id': 0x12 })),
    ('Grotto',          ('Hyrule Field -> HF Open Grotto',                                  { 'grotto_id': 0x13, 'entrance': 0x003F, 'content': 0x03, 'scene': 0x51 }),
                        ('HF Open Grotto -> Hyrule Field',                                  { 'grotto_id': 0x13 })),
    ('Grotto',          ('Hyrule Field -> HF Southeast Grotto',                             { 'grotto_id': 0x14, 'entrance': 0x003F, 'content': 0x22, 'scene': 0x51 }),
                        ('HF Southeast Grotto -> Hyrule Field',                             { 'grotto_id': 0x14 })),
    ('Grotto',          ('Lon Lon Ranch -> LLR Grotto',                                     { 'grotto_id': 0x15, 'entrance': 0x05A4, 'content': 0xFC, 'scene': 0x63 }),
                        ('LLR Grotto -> Lon Lon Ranch',                                     { 'grotto_id': 0x15 })),
    ('Grotto',          ('SFM Entryway -> SFM Wolfos Grotto',                               { 'grotto_id': 0x16, 'entrance': 0x05B4, 'content': 0xED, 'scene': 0x56 }),
                        ('SFM Wolfos Grotto -> SFM Entryway',                               { 'grotto_id': 0x16 })),
    ('Grotto',          ('Sacred Forest Meadow -> SFM Storms Grotto',                       { 'grotto_id': 0x17, 'entrance': 0x05BC, 'content': 0xEE, 'scene': 0x56 }),
                        ('SFM Storms Grotto -> Sacred Forest Meadow',                       { 'grotto_id': 0x17 })),
    ('Grotto',          ('Sacred Forest Meadow -> SFM Fairy Grotto',                        { 'grotto_id': 0x18, 'entrance': 0x036D, 'content': 0xFF, 'scene': 0x56 }),
                        ('SFM Fairy Grotto -> Sacred Forest Meadow',                        { 'grotto_id': 0x18 })),
    ('Grotto',          ('LW Beyond Mido -> LW Scrubs Grotto',                              { 'grotto_id': 0x19, 'entrance': 0x05B0, 'content': 0xF5, 'scene': 0x5B }),
                        ('LW Scrubs Grotto -> LW Beyond Mido',                              { 'grotto_id': 0x19 })),
    ('Grotto',          ('Lost Woods -> LW Near Shortcuts Grotto',                          { 'grotto_id': 0x1A, 'entrance': 0x003F, 'content': 0x14, 'scene': 0x5B }),
                        ('LW Near Shortcuts Grotto -> Lost Woods',                          { 'grotto_id': 0x1A })),
    ('Grotto',          ('Kokiri Forest -> KF Storms Grotto',                               { 'grotto_id': 0x1B, 'entrance': 0x003F, 'content': 0x2C, 'scene': 0x55 }),
                        ('KF Storms Grotto -> Kokiri Forest',                               { 'grotto_id': 0x1B })),
    ('Grotto',          ('Zoras Domain -> ZD Storms Grotto',                                { 'grotto_id': 0x1C, 'entrance': 0x036D, 'content': 0xFF, 'scene': 0x58 }),
                        ('ZD Storms Grotto -> Zoras Domain',                                { 'grotto_id': 0x1C })),
    ('Grotto',          ('GF Entrances Behind Crates -> GF Storms Grotto',                  { 'grotto_id': 0x1D, 'entrance': 0x036D, 'content': 0xFF, 'scene': 0x5D }),
                        ('GF Storms Grotto -> GF Entrances Behind Crates',                  { 'grotto_id': 0x1D })),
    ('Grotto',          ('GV Fortress Side -> GV Storms Grotto',                            { 'grotto_id': 0x1E, 'entrance': 0x05BC, 'content': 0xF0, 'scene': 0x5A }),
                        ('GV Storms Grotto -> GV Fortress Side',                            { 'grotto_id': 0x1E })),
    ('Grotto',          ('GV Grotto Ledge -> GV Octorok Grotto',                            { 'grotto_id': 0x1F, 'entrance': 0x05AC, 'content': 0xF2, 'scene': 0x5A }),
                        ('GV Octorok Grotto -> GV Grotto Ledge',                            { 'grotto_id': 0x1F })),
    ('Grotto',          ('LW Beyond Mido -> Deku Theater',                                  { 'grotto_id': 0x20, 'entrance': 0x05C4, 'content': 0xF3, 'scene': 0x5B }),
                        ('Deku Theater -> LW Beyond Mido',                                  { 'grotto_id': 0x20 })),

    ('Grave',           ('Graveyard -> Graveyard Shield Grave',                             { 'index': 0x004B }),
                        ('Graveyard Shield Grave -> Graveyard',                             { 'index': 0x035D })),
    ('Grave',           ('Graveyard -> Graveyard Heart Piece Grave',                        { 'index': 0x031C }),
                        ('Graveyard Heart Piece Grave -> Graveyard',                        { 'index': 0x0361 })),
    ('Grave',           ('Graveyard -> Graveyard Royal Familys Tomb',                       { 'index': 0x002D }),
                        ('Graveyard Royal Familys Tomb -> Graveyard',                       { 'index': 0x050B })),
    ('Grave',           ('Graveyard -> Graveyard Dampes Grave',                             { 'index': 0x044F }),
                        ('Graveyard Dampes Grave -> Graveyard',                             { 'index': 0x0359 })),

    ('Overworld',       ('Kokiri Forest -> LW Bridge From Forest',                          { 'index': 0x05E0 }),
                        ('LW Bridge -> Kokiri Forest',                                      { 'index': 0x020D })),
    ('Overworld',       ('Kokiri Forest -> Lost Woods',                                     { 'index': 0x011E }),
                        ('LW Forest Exit -> Kokiri Forest',                                 { 'index': 0x0286 })),
    ('Overworld',       ('Lost Woods -> GC Woods Warp',                                     { 'index': 0x04E2 }),
                        ('GC Woods Warp -> Lost Woods',                                     { 'index': 0x04D6 })),
    ('Overworld',       ('Lost Woods -> Zora River',                                        { 'index': 0x01DD }),
                        ('Zora River -> LW Underwater Entrance',                            { 'index': 0x04DA })),
    ('Overworld',       ('LW Beyond Mido -> SFM Entryway',                                  { 'index': 0x00FC }),
                        ('SFM Entryway -> LW Beyond Mido',                                  { 'index': 0x01A9 })),
    ('Overworld',       ('LW Bridge -> Hyrule Field',                                       { 'index': 0x0185 }),
                        ('Hyrule Field -> LW Bridge',                                       { 'index': 0x04DE })),
    ('Overworld',       ('Hyrule Field -> Lake Hylia',                                      { 'index': 0x0102 }),
                        ('Lake Hylia -> Hyrule Field',                                      { 'index': 0x0189 })),
    ('Overworld',       ('Hyrule Field -> Gerudo Valley',                                   { 'index': 0x0117 }),
                        ('Gerudo Valley -> Hyrule Field',                                   { 'index': 0x018D })),
    ('Overworld',       ('Hyrule Field -> Market Entrance',                                 { 'index': 0x0276 }),
                        ('Market Entrance -> Hyrule Field',                                 { 'index': 0x01FD })),
    ('Overworld',       ('Hyrule Field -> Kakariko Village',                                { 'index': 0x00DB }),
                        ('Kakariko Village -> Hyrule Field',                                { 'index': 0x017D })),
    ('Overworld',       ('Hyrule Field -> ZR Front',                                        { 'index': 0x00EA }),
                        ('ZR Front -> Hyrule Field',                                        { 'index': 0x0181 })),
    ('Overworld',       ('Hyrule Field -> Lon Lon Ranch',                                   { 'index': 0x0157 }),
                        ('Lon Lon Ranch -> Hyrule Field',                                   { 'index': 0x01F9 })),
    ('Overworld',       ('Lake Hylia -> Zoras Domain',                                      { 'index': 0x0328 }),
                        ('Zoras Domain -> Lake Hylia',                                      { 'index': 0x0560 })),
    ('Overworld',       ('GV Fortress Side -> Gerudo Fortress',                             { 'index': 0x0129 }),
                        ('Gerudo Fortress -> GV Fortress Side',                             { 'index': 0x022D })),
    ('Overworld',       ('GF Outside Gate -> Wasteland Near Fortress',                      { 'index': 0x0130 }),
                        ('Wasteland Near Fortress -> GF Outside Gate',                      { 'index': 0x03AC })),
    ('Overworld',       ('Wasteland Near Colossus -> Desert Colossus',                      { 'index': 0x0123 }),
                        ('Desert Colossus -> Wasteland Near Colossus',                      { 'index': 0x0365 })),
    ('Overworld',       ('Market Entrance -> Market',                                       { 'index': 0x00B1 }),
                        ('Market -> Market Entrance',                                       { 'index': 0x0033 })),
    ('Overworld',       ('Market -> Castle Grounds',                                        { 'index': 0x0138 }),
                        ('Castle Grounds -> Market',                                        { 'index': 0x025A })),
    ('Overworld',       ('Market -> ToT Entrance',                                          { 'index': 0x0171 }),
                        ('ToT Entrance -> Market',                                          { 'index': 0x025E })),
    ('Overworld',       ('Kakariko Village -> Graveyard',                                   { 'index': 0x00E4 }),
                        ('Graveyard -> Kakariko Village',                                   { 'index': 0x0195 })),
    ('Overworld',       ('Kak Behind Gate -> Death Mountain',                               { 'index': 0x013D }),
                        ('Death Mountain -> Kak Behind Gate',                               { 'index': 0x0191 })),
    ('Overworld',       ('Death Mountain -> Goron City',                                    { 'index': 0x014D }),
                        ('Goron City -> Death Mountain',                                    { 'index': 0x01B9 })),
    ('Overworld',       ('GC Darunias Chamber -> DMC Lower Local',                          { 'index': 0x0246 }),
                        ('DMC Lower Nearby -> GC Darunias Chamber',                         { 'index': 0x01C1 })),
    ('Overworld',       ('Death Mountain Summit -> DMC Upper Local',                        { 'index': 0x0147 }),
                        ('DMC Upper Nearby -> Death Mountain Summit',                       { 'index': 0x01BD })),
    ('Overworld',       ('ZR Behind Waterfall -> Zoras Domain',                             { 'index': 0x0108 }),
                        ('Zoras Domain -> ZR Behind Waterfall',                             { 'index': 0x019D })),
    ('Overworld',       ('ZD Behind King Zora -> Zoras Fountain',                           { 'index': 0x0225 }),
                        ('Zoras Fountain -> ZD Behind King Zora',                           { 'index': 0x01A1 })),

    ('Overworld',       ('GV Lower Stream -> Lake Hylia',                                   { 'index': 0x0219 })),

    ('OwlDrop',         ('LH Owl Flight -> Hyrule Field',                                   { 'index': 0x027E, 'addresses': [0xAC9F26] })),
    ('OwlDrop',         ('DMT Owl Flight -> Kak Impas Rooftop',                             { 'index': 0x0554, 'addresses': [0xAC9EF2] })),

    ('Spawn',           ('Child Spawn -> KF Links House',                                   { 'index': 0x00BB, 'addresses': [0xB06342] })),
    ('Spawn',           ('Adult Spawn -> Temple of Time',                                   { 'index': 0x05F4, 'addresses': [0xB06332] })),

    ('WarpSong',        ('Minuet of Forest Warp -> Sacred Forest Meadow',                   { 'index': 0x0600, 'addresses': [0xBF023C] })),
    ('WarpSong',        ('Bolero of Fire Warp -> DMC Central Local',                        { 'index': 0x04F6, 'addresses': [0xBF023E] })),
    ('WarpSong',        ('Serenade of Water Warp -> Lake Hylia',                            { 'index': 0x0604, 'addresses': [0xBF0240] })),
    ('WarpSong',        ('Requiem of Spirit Warp -> Desert Colossus',                       { 'index': 0x01F1, 'addresses': [0xBF0242] })),
    ('WarpSong',        ('Nocturne of Shadow Warp -> Graveyard Warp Pad Region',            { 'index': 0x0568, 'addresses': [0xBF0244] })),
    ('WarpSong',        ('Prelude of Light Warp -> Temple of Time',                         { 'index': 0x05F4, 'addresses': [0xBF0246] })),

    ('Extra',           ('ZD Eyeball Frog Timeout -> Zoras Domain',                         { 'index': 0x0153 })),
    ('Extra',           ('ZR Top of Waterfall -> Zora River',                               { 'index': 0x0199 })),
]


def _add_boss_entrances():
    # Compute this at load time to save a lot of duplication
    dungeon_data = {}
    for type, forward, *reverse in entrance_shuffle_table:
        if type != 'Dungeon':
            continue
        if not reverse:
            continue
        name, forward = forward
        reverse = reverse[0][1]
        if 'blue_warp' not in reverse:
            continue
        dungeon_data[name] = {
            'dungeon_index': forward['index'],
            'exit_index': reverse['index'],
            'exit_blue_warp': reverse['blue_warp']
        }

    for type, source, target, dungeon, index, rindex, addresses in [
        (
            'ChildBoss', 'Deku Tree Boss Door', 'Queen Gohma Boss Room',
            'KF Outside Deku Tree -> Deku Tree Lobby',
            0x040f, 0x0252, [ 0xB06292, 0xBC6162, 0xBC60AE ]
        ),
        (
            'ChildBoss', 'Dodongos Cavern Boss Door', 'King Dodongo Boss Room',
            'Death Mountain -> Dodongos Cavern Beginning',
            0x040b, 0x00c5, [ 0xB062B6, 0xBC616E ]
        ),
        (
            'ChildBoss', 'Jabu Jabus Belly Boss Door', 'Barinade Boss Room',
            'Zoras Fountain -> Jabu Jabus Belly Beginning',
            0x0301, 0x0407, [ 0xB062C2, 0xBC60C2 ]
        ),
        (
            'AdultBoss', 'Forest Temple Boss Door', 'Phantom Ganon Boss Room',
            'SFM Forest Temple Entrance Ledge -> Forest Temple Lobby',
            0x000c, 0x024E, [ 0xB062CE, 0xBC6182 ]
        ),
        (
            'AdultBoss', 'Fire Temple Boss Door', 'Volvagia Boss Room',
            'DMC Fire Temple Entrance -> Fire Temple Lower',
            0x0305, 0x0175, [ 0xB062DA, 0xBC60CE ]
        ),
        (
            'AdultBoss', 'Water Temple Boss Door', 'Morpha Boss Room',
            'Lake Hylia -> Water Temple Lobby',
            0x0417, 0x0423, [ 0xB062E6, 0xBC6196 ]
        ),
        (
            'AdultBoss', 'Spirit Temple Boss Door', 'Twinrova Boss Room',
            'Desert Colossus -> Spirit Temple Lobby',
            0x008D, 0x02F5, [ 0xB062F2, 0xBC6122 ]
        ),
        (
            'AdultBoss', 'Shadow Temple Boss Door', 'Bongo Bongo Boss Room',
            'Graveyard Warp Pad Region -> Shadow Temple Entryway',
            0x0413, 0x02B2, [ 0xB062FE, 0xBC61AA ]
        )
    ]:
        d = {'index': index, 'patch_addresses': addresses}
        d.update(dungeon_data[dungeon])
        entrance_shuffle_table.append(
            (type, (f"{source} -> {target}", d), (f"{target} -> {source}", {'index': rindex}))
        )
_add_boss_entrances()


# Basically, the entrances in the list above that go to:
# - DMC Central Local (child access for the bean and skull)
# - Desert Colossus (child access to colossus and spirit)
# - Graveyard Warp Pad Region (access to shadow, plus the gossip stone)
# We will always need to pick one from each list to receive a one-way entrance
# if shuffling warp songs (depending on other settings).
# Table maps: short key -> ([target regions], [allowed types])
priority_entrance_table = {
    'Bolero': (['DMC Central Local'], ['OwlDrop', 'WarpSong']),
    'Nocturne': (['Graveyard Warp Pad Region'], ['OwlDrop', 'Spawn', 'WarpSong']),
    'Requiem': (['Desert Colossus', 'Desert Colossus From Spirit Lobby'], ['OwlDrop', 'Spawn', 'WarpSong']),
}


# These hint texts have more than one entrance, so they are OK for impa's house and potion shop
multi_interior_regions = {
    'Kokiri Forest',
    'Lake Hylia',
    'the Market',
    'Kakariko Village',
    'Lon Lon Ranch',
}

interior_entrance_bias = {
    'ToT Entrance -> Temple of Time': 4,
    'Kakariko Village -> Kak Potion Shop Front': 3,
    'Kak Backyard -> Kak Potion Shop Back': 3,
    'Kakariko Village -> Kak Impas House': 2,
    'Kak Impas Ledge -> Kak Impas House Back': 2,
    'Market Entrance -> Market Guard House': 2,
    'Goron City -> GC Shop': 1,
    'Zoras Domain -> ZD Shop': 1,
}


class EntranceShuffleError(Exception):
    pass


def shuffle_random_entrances(ootworld):
    multiworld = ootworld.multiworld
    player = ootworld.player

    # Gather locations to keep reachable for validation
    all_state = ootworld.get_state_with_complete_itempool()
    all_state.sweep_for_advancements(locations=ootworld.get_locations())
    locations_to_ensure_reachable = {loc for loc in multiworld.get_reachable_locations(all_state, player) if not (loc.type == 'Drop' or (loc.type == 'Event' and 'Subrule' in loc.name))}

    # Set entrance data for all entrances
    set_all_entrances_data(multiworld, player)

    # Determine entrance pools based on settings
    one_way_entrance_pools = {}
    entrance_pools = {}
    one_way_priorities = {}

    if ootworld.owl_drops:
        one_way_entrance_pools['OwlDrop'] = ootworld.get_shufflable_entrances(type='OwlDrop')
    if ootworld.warp_songs:
        one_way_entrance_pools['WarpSong'] = ootworld.get_shufflable_entrances(type='WarpSong')
        # No more exceptions for NL here, causes cascading failures later
        one_way_priorities['Bolero'] = priority_entrance_table['Bolero']
        one_way_priorities['Nocturne'] = priority_entrance_table['Nocturne']
        if not ootworld.shuffle_dungeon_entrances and not ootworld.shuffle_overworld_entrances:
            one_way_priorities['Requiem'] = priority_entrance_table['Requiem']
    if ootworld.spawn_positions:
        one_way_entrance_pools['Spawn'] = ootworld.get_shufflable_entrances(type='Spawn')
        if 'child' not in ootworld.spawn_positions:
            one_way_entrance_pools['Spawn'].remove(ootworld.get_entrance('Child Spawn -> KF Links House'))
        if 'adult' not in ootworld.spawn_positions:
            one_way_entrance_pools['Spawn'].remove(ootworld.get_entrance('Adult Spawn -> Temple of Time'))

    if ootworld.shuffle_bosses == 'full':
        entrance_pools['Boss'] = ootworld.get_shufflable_entrances(type='ChildBoss', only_primary=True)
        entrance_pools['Boss'] += ootworld.get_shufflable_entrances(type='AdultBoss', only_primary=True)
    elif ootworld.shuffle_bosses == 'limited':
        entrance_pools['ChildBoss'] = ootworld.get_shufflable_entrances(type='ChildBoss', only_primary=True)
        entrance_pools['AdultBoss'] = ootworld.get_shufflable_entrances(type='AdultBoss', only_primary=True)

    if ootworld.shuffle_dungeon_entrances:
        entrance_pools['Dungeon'] = ootworld.get_shufflable_entrances(type='Dungeon', only_primary=True)
        if ootworld.open_forest == 'closed':
            entrance_pools['Dungeon'].remove(ootworld.get_entrance('KF Outside Deku Tree -> Deku Tree Lobby'))
        if ootworld.shuffle_special_dungeon_entrances:
            entrance_pools['Dungeon'] += ootworld.get_shufflable_entrances(type='DungeonSpecial', only_primary=True)
        if ootworld.decouple_entrances:
            entrance_pools['DungeonReverse'] = [entrance.reverse for entrance in entrance_pools['Dungeon']]
    if ootworld.shuffle_interior_entrances != 'off':
        entrance_pools['Interior'] = ootworld.get_shufflable_entrances(type='Interior', only_primary=True)
        if ootworld.shuffle_special_interior_entrances:
            entrance_pools['Interior'] += ootworld.get_shufflable_entrances(type='SpecialInterior', only_primary=True)
        if ootworld.decouple_entrances:
            entrance_pools['InteriorReverse'] = [entrance.reverse for entrance in entrance_pools['Interior']]
    if ootworld.shuffle_grotto_entrances:
        entrance_pools['GrottoGrave'] = ootworld.get_shufflable_entrances(type='Grotto', only_primary=True)
        entrance_pools['GrottoGrave'] += ootworld.get_shufflable_entrances(type='Grave', only_primary=True)
        if ootworld.decouple_entrances:
            entrance_pools['GrottoGraveReverse'] = [entrance.reverse for entrance in entrance_pools['GrottoGrave']]
    if ootworld.shuffle_overworld_entrances:
        exclude_overworld_reverse = ootworld.mix_entrance_pools == 'all' and not ootworld.decouple_entrances
        entrance_pools['Overworld'] = ootworld.get_shufflable_entrances(type='Overworld', only_primary=exclude_overworld_reverse)
        if not ootworld.decouple_entrances:
            entrance_pools['Overworld'].remove(ootworld.get_entrance('GV Lower Stream -> Lake Hylia'))

    # Mark shuffled entrances
    for entrance in chain(chain.from_iterable(one_way_entrance_pools.values()), chain.from_iterable(entrance_pools.values())):
        entrance.shuffled = True
        if entrance.reverse:
            entrance.reverse.shuffled = True

    # Combine all entrance pools if mixing
    if ootworld.mix_entrance_pools == 'all':
        entrance_pools = {'Mixed': list(chain.from_iterable(entrance_pools.values()))}
    elif ootworld.mix_entrance_pools == 'indoor':
        if ootworld.shuffle_overworld_entrances:
            ow_pool = entrance_pools['Overworld']
        entrance_pools = {'Mixed': list(filter(lambda entrance: entrance.type != 'Overworld', chain.from_iterable(entrance_pools.values())))}
        if ootworld.shuffle_overworld_entrances:
            entrance_pools['Overworld'] = ow_pool

    # Build target entrance pools
    one_way_target_entrance_pools = {}
    for pool_type, entrance_pool in one_way_entrance_pools.items():
        if pool_type == 'OwlDrop':
            valid_target_types = ('WarpSong', 'OwlDrop', 'Overworld', 'Extra')
            one_way_target_entrance_pools[pool_type] = build_one_way_targets(ootworld, pool_type, valid_target_types, exclude=['Prelude of Light Warp -> Temple of Time'])
            for target in one_way_target_entrance_pools[pool_type]:
                set_rule(target, lambda state: state._oot_reach_as_age(target.parent_region, 'child', player))
        elif pool_type in {'Spawn', 'WarpSong'}: 
            valid_target_types = ('Spawn', 'WarpSong', 'OwlDrop', 'Overworld', 'Interior', 'SpecialInterior', 'Extra')
            one_way_target_entrance_pools[pool_type] = build_one_way_targets(ootworld, pool_type, valid_target_types)
        # Ensure that the last entrance doesn't assume the rest of the targets are reachable
        for target in one_way_target_entrance_pools[pool_type]:
            add_rule(target, (lambda entrances=entrance_pool: (lambda state: any(entrance.connected_region == None for entrance in entrances)))())
    # Disconnect one-way entrances for priority placement
    for entrance in chain.from_iterable(one_way_entrance_pools.values()):
        entrance.disconnect()

    target_entrance_pools = {}
    for pool_type, entrance_pool in entrance_pools.items():
        target_entrance_pools[pool_type] = assume_entrance_pool(entrance_pool, ootworld, pool_type)

    # Build all_state and none_state
    all_state = ootworld.get_state_with_complete_itempool()
    none_state = CollectionState(ootworld.multiworld)

    # Plando entrances
    if ootworld.options.plando_connections:
        rollbacks = []
        all_targets = {**one_way_target_entrance_pools, **target_entrance_pools}
        for conn in ootworld.options.plando_connections:
            try:
                entrance = ootworld.get_entrance(conn.entrance)
                exit = ootworld.get_entrance(conn.exit)
                if entrance is None:
                    raise EntranceShuffleError(f"Could not find entrance to plando: {conn.entrance}")
                if exit is None:
                    raise EntranceShuffleError(f"Could not find entrance to plando: {conn.exit}")
                target_region = exit.name.split(' -> ')[1]
                target_parent = exit.parent_region.name
                pool_type = entrance.type
                matched_targets_to_region = list(filter(lambda target: target.connected_region and target.connected_region.name == target_region,
                                                        all_targets[pool_type]))
                target = next(filter(lambda target: target.replaces.parent_region.name == target_parent, matched_targets_to_region))

                replace_entrance(ootworld, entrance, target, rollbacks, locations_to_ensure_reachable, all_state, none_state)
                if conn.direction == 'both' and entrance.reverse and ootworld.decouple_entrances:
                    replace_entrance(ootworld, entrance.reverse, target.reverse, rollbacks, locations_to_ensure_reachable, all_state, none_state)
            except EntranceShuffleError as e:
                raise RuntimeError(f"Failed to plando OoT entrances. Reason: {e}")
            except StopIteration:
                raise RuntimeError(f"Could not find entrance to plando: {conn.entrance} => {conn.exit}")
            finally:
                for (entrance, target) in rollbacks:
                    confirm_replacement(entrance, target)

    # Check placed one way entrances and trim.
    # The placed entrances are already pointing at their new regions.
    placed_entrances = [entrance for entrance in chain.from_iterable(one_way_entrance_pools.values())
                        if entrance.replaces is not None]
    replaced_entrances = [entrance.replaces for entrance in placed_entrances]
    # Remove replaced entrances so we don't place two in one target.
    for remaining_target in chain.from_iterable(one_way_target_entrance_pools.values()):
        if remaining_target.replaces and remaining_target.replaces in replaced_entrances:
            delete_target_entrance(remaining_target)
    # Remove priority targets if any placed entrances point at their region(s).
    for key, (regions, _) in priority_entrance_table.items():
        if key in one_way_priorities:
            for entrance in placed_entrances:
                if entrance.connected_region and entrance.connected_region.name in regions:
                    del one_way_priorities[key]
                    break

    # Place priority entrances
    shuffle_one_way_priority_entrances(ootworld, one_way_priorities, one_way_entrance_pools, one_way_target_entrance_pools, locations_to_ensure_reachable, all_state, none_state, retry_count=2)

    # Delete priority targets from one-way pools
    replaced_entrances = [entrance.replaces for entrance in chain.from_iterable(one_way_entrance_pools.values())]
    for remaining_target in chain.from_iterable(one_way_target_entrance_pools.values()):
        if remaining_target.replaces in replaced_entrances:
            delete_target_entrance(remaining_target)

    for pool_type, entrance_pool in one_way_entrance_pools.items():
        shuffle_entrance_pool(ootworld, pool_type, entrance_pool, one_way_target_entrance_pools[pool_type], locations_to_ensure_reachable, all_state, none_state, check_all=True, retry_count=5)
        replaced_entrances = [entrance.replaces for entrance in entrance_pool]
        for remaining_target in chain.from_iterable(one_way_target_entrance_pools.values()):
            if remaining_target.replaces in replaced_entrances:
                delete_target_entrance(remaining_target)
        for unused_target in one_way_target_entrance_pools[pool_type]:
            delete_target_entrance(unused_target)

    # Shuffle all entrance pools, in order
    for pool_type, entrance_pool in entrance_pools.items():
        shuffle_entrance_pool(ootworld, pool_type, entrance_pool, target_entrance_pools[pool_type], locations_to_ensure_reachable, all_state, none_state, check_all=True)

    # Multiple checks after shuffling to ensure everything is OK
    # Check that all entrances hook up correctly
    for entrance in ootworld.get_shuffled_entrances():
        if entrance.connected_region == None:
            logging.getLogger('').error(f'{entrance} was shuffled but is not connected to any region')
        if entrance.replaces == None:
            logging.getLogger('').error(f'{entrance} was shuffled but does not replace any entrance')
    if len(ootworld.get_region('Root Exits').exits) > 8:
        for exit in ootworld.get_region('Root Exits').exits:
            logging.getLogger('').error(f'Root Exit: {exit} -> {exit.connected_region}')
        logging.getLogger('').error(f'Root has too many entrances left after shuffling entrances')
    # Game is beatable
    new_all_state = ootworld.get_state_with_complete_itempool()
    if not multiworld.has_beaten_game(new_all_state, player):
        raise EntranceShuffleError('Cannot beat game')
    # Validate world
    validate_world(ootworld, None, locations_to_ensure_reachable, all_state, none_state)


def replace_entrance(ootworld, entrance, target, rollbacks, locations_to_ensure_reachable, all_state, none_state):
    try:
        check_entrances_compatibility(entrance, target, rollbacks)
        change_connections(entrance, target)
        validate_world(ootworld, entrance, locations_to_ensure_reachable, all_state, none_state)
        rollbacks.append((entrance, target))
        return True
    except EntranceShuffleError as e:
        logging.getLogger('').debug(f'Failed to connect {entrance} to {target}, reason: {e}')
        if entrance.connected_region:
            restore_connections(entrance, target)
    return False


def shuffle_one_way_priority_entrances(ootworld, one_way_priorities, one_way_entrance_pools, one_way_target_entrance_pools,
    locations_to_ensure_reachable, all_state, none_state, retry_count=2):

    ootworld.priority_entrances = []

    while retry_count:
        retry_count -= 1
        rollbacks = []

        try:
            for key, (regions, types) in one_way_priorities.items():
                place_one_way_priority_entrance(ootworld, key, regions, types, rollbacks, locations_to_ensure_reachable,
                    all_state, none_state, one_way_entrance_pools, one_way_target_entrance_pools)
            for entrance, target in rollbacks:
                confirm_replacement(entrance, target)
            return
        except EntranceShuffleError as error:
            for entrance, target in rollbacks:
                restore_connections(entrance, target)
            logging.getLogger('').debug(f'Failed to place all priority one-way entrances, retrying {retry_count} more times')

    raise EntranceShuffleError(f'Priority one-way entrance placement attempt count exceeded for world {ootworld.player}')

def place_one_way_priority_entrance(ootworld, priority_name, allowed_regions, allowed_types, rollbacks, locations_to_ensure_reachable,
    all_state, none_state, one_way_entrance_pools, one_way_target_entrance_pools):

    avail_pool = list(chain.from_iterable(one_way_entrance_pools[t] for t in allowed_types if t in one_way_entrance_pools))
    ootworld.random.shuffle(avail_pool)

    for entrance in avail_pool:
        if entrance.replaces:
            continue
        # With mask hints, child needs to be able to access the gossip stone.
        if entrance.parent_region.name == 'Adult Spawn' and (priority_name != 'Nocturne' or ootworld.hints == 'mask'):
            continue
        # With dungeons unshuffled, adult needs to be able to access Shadow Temple.
        if not ootworld.shuffle_dungeon_entrances and priority_name == 'Nocturne':
            if entrance.type != 'WarpSong' and entrance.parent_region.name != 'Adult Spawn':
                continue
        # With overworld unshuffled, child can't spawn at Desert Colossus
        if not ootworld.shuffle_overworld_entrances and priority_name == 'Requiem' and entrance.parent_region.name == 'Child Spawn':
            continue
        for target in one_way_target_entrance_pools[entrance.type]:
            if target.connected_region and target.connected_region.name in allowed_regions:
                if replace_entrance(ootworld, entrance, target, rollbacks, locations_to_ensure_reachable, all_state, none_state):
                    logging.getLogger('').debug(f'Priority placing {entrance} as {target} for {priority_name}')
                    ootworld.priority_entrances.append(entrance)
                    return
    raise EntranceShuffleError(f'Unable to place priority one-way entrance for {priority_name} in world {ootworld.player}')


def shuffle_entrance_pool(ootworld, pool_type, entrance_pool, target_entrances, locations_to_ensure_reachable, all_state, none_state, check_all=False, retry_count=10):
    
    restrictive_entrances, soft_entrances = split_entrances_by_requirements(ootworld, entrance_pool, target_entrances)

    while retry_count:
        retry_count -= 1
        rollbacks = []
        try:
            shuffle_entrances(ootworld, pool_type+'Rest', restrictive_entrances, target_entrances, rollbacks, locations_to_ensure_reachable, all_state, none_state)
            if check_all:
                shuffle_entrances(ootworld, pool_type+'Soft', soft_entrances, target_entrances, rollbacks, locations_to_ensure_reachable, all_state, none_state)
            else:
                shuffle_entrances(ootworld, pool_type+'Soft', soft_entrances, target_entrances, rollbacks, set(), all_state, none_state)

            validate_world(ootworld, None, locations_to_ensure_reachable, all_state, none_state)
            for entrance, target in rollbacks: 
                confirm_replacement(entrance, target)
            return
        except EntranceShuffleError as e:
            for entrance, target in rollbacks:
                restore_connections(entrance, target)
            logging.getLogger('').debug(f'Failed to place all entrances in pool, retrying {retry_count} more times')

    raise EntranceShuffleError(f'Entrance placement attempt count exceeded for world {ootworld.player}')

def shuffle_entrances(ootworld, pool_type, entrances, target_entrances, rollbacks, locations_to_ensure_reachable, all_state, none_state):
    ootworld.random.shuffle(entrances)
    for entrance in entrances:
        if entrance.connected_region != None:
            continue
        ootworld.random.shuffle(target_entrances)
        # Here we deliberately introduce bias by prioritizing certain interiors, i.e. the ones most likely to cause problems.
        # success rate over randomization
        if pool_type in {'InteriorSoft', 'MixedSoft'}:
            target_entrances.sort(reverse=True, key=lambda entrance: interior_entrance_bias.get(entrance.replaces.name, 0))
        for target in target_entrances:
            if target.connected_region == None:
                continue
            if replace_entrance(ootworld, entrance, target, rollbacks, locations_to_ensure_reachable, all_state, none_state):
                break
        if entrance.connected_region == None:
            raise EntranceShuffleError('No more valid entrances')


def split_entrances_by_requirements(ootworld, entrances_to_split, assumed_entrances):
    player = ootworld.player

    # Disconnect all root assumed entrances and save original connections
    original_connected_regions = {}
    entrances_to_disconnect = set(assumed_entrances).union(entrance.reverse for entrance in assumed_entrances if entrance.reverse)
    for entrance in entrances_to_disconnect:
        if entrance.connected_region:
            original_connected_regions[entrance] = entrance.disconnect()

    all_state = ootworld.get_state_with_complete_itempool()

    restrictive_entrances = []
    soft_entrances = []

    for entrance in entrances_to_split:
        all_state.age[player] = 'child'
        if not all_state.can_reach(entrance, 'Entrance', player):
            restrictive_entrances.append(entrance)
            continue
        all_state.age[player] = 'adult'
        if not all_state.can_reach(entrance, 'Entrance', player):
            restrictive_entrances.append(entrance)
            continue
        all_state.age[player] = None
        if not all_state._oot_reach_at_time(entrance.parent_region.name, TimeOfDay.ALL, [], player):
            restrictive_entrances.append(entrance)
            continue
        soft_entrances.append(entrance)

    # Reconnect assumed entrances
    for entrance in entrances_to_disconnect:
        if entrance in original_connected_regions:
            entrance.connect(original_connected_regions[entrance])

    return restrictive_entrances, soft_entrances


# Check to ensure the world is valid. 
# TODO: improve this function
def validate_world(ootworld, entrance_placed, locations_to_ensure_reachable, all_state_orig, none_state_orig):

    multiworld = ootworld.multiworld
    player = ootworld.player

    all_state = all_state_orig.copy()
    none_state = none_state_orig.copy()

    all_state.sweep_for_advancements(locations=ootworld.get_locations())
    none_state.sweep_for_advancements(locations=ootworld.get_locations())

    if ootworld.shuffle_interior_entrances or ootworld.shuffle_overworld_entrances or ootworld.spawn_positions:
        time_travel_state = none_state.copy()
        time_travel_state.collect(ootworld.create_item('Time Travel'), prevent_sweep=True)
        time_travel_state._oot_update_age_reachable_regions(player)

    # Unless entrances are decoupled, we don't want the player to end up through certain entrances as the wrong age
    # This means we need to hard check that none of the relevant entrances are ever reachable as that age
    # This is mostly relevant when shuffling special interiors (such as windmill or kak potion shop)
    # Warp Songs and Overworld Spawns can also end up inside certain indoors so those need to be handled as well
    CHILD_FORBIDDEN = ['OGC Great Fairy Fountain -> Castle Grounds', 'GV Carpenter Tent -> GV Fortress Side']
    ADULT_FORBIDDEN = ['HC Great Fairy Fountain -> Castle Grounds', 'HC Storms Grotto -> Castle Grounds']

    if not ootworld.decouple_entrances:
        for entrance in ootworld.get_shufflable_entrances():
            if entrance.shuffled and entrance.replaces:
                if entrance.replaces.name in CHILD_FORBIDDEN and not entrance_unreachable_as(entrance, 'child', already_checked=[entrance.replaces.reverse]):
                    raise EntranceShuffleError(f'{entrance.replaces.name} replaced by an entrance with potential child access')
                if entrance.replaces.name in ADULT_FORBIDDEN and not entrance_unreachable_as(entrance, 'adult', already_checked=[entrance.replaces.reverse]):
                    raise EntranceShuffleError(f'{entrance.replaces.name} replaced by an entrance with potential adult access')
            else:
                if entrance.name in CHILD_FORBIDDEN and not entrance_unreachable_as(entrance, 'child', already_checked=[entrance.reverse]):
                    raise EntranceShuffleError(f'{entrance.name} potentially accessible as child')
                if entrance.name in ADULT_FORBIDDEN and not entrance_unreachable_as(entrance, 'adult', already_checked=[entrance.reverse]):
                    raise EntranceShuffleError(f'{entrance.name} potentially accessible as adult')

    # Check if all locations are reachable if not NL
    if locations_to_ensure_reachable:
        for loc in locations_to_ensure_reachable:
            if not all_state.can_reach(loc, 'Location', player):
                raise EntranceShuffleError(f'{loc} is unreachable')

    if ootworld.shuffle_interior_entrances and (ootworld.misc_hints or ootworld.hints != 'none') and \
        (entrance_placed == None or entrance_placed.type in ['Interior', 'SpecialInterior']):
        # Ensure Kak Potion Shop entrances are in the same hint area so there is no ambiguity as to which entrance is used for hints
        potion_front = get_entrance_replacing(multiworld.get_region('Kak Potion Shop Front', player), 'Kakariko Village -> Kak Potion Shop Front', player)
        potion_back = get_entrance_replacing(multiworld.get_region('Kak Potion Shop Back', player), 'Kak Backyard -> Kak Potion Shop Back', player)
        if potion_front is not None and potion_back is not None and not same_hint_area(potion_front, potion_back):
            raise EntranceShuffleError('Kak Potion Shop entrances are not in the same hint area')
        elif (potion_front and not potion_back) or (not potion_front and potion_back):
            # Check the hint area and ensure it's one of the ones with more than one entrance
            potion_placed_entrance = potion_front if potion_front else potion_back
            if get_hint_area(potion_placed_entrance) not in multi_interior_regions:
                raise EntranceShuffleError('Kak Potion Shop entrances can never be in the same hint area')

        # When cows are shuffled, ensure the same thing for Impa's House, since the cow is reachable from both sides
        if ootworld.shuffle_cows:
            impas_front = get_entrance_replacing(multiworld.get_region('Kak Impas House', player), 'Kakariko Village -> Kak Impas House', player)
            impas_back = get_entrance_replacing(multiworld.get_region('Kak Impas House Back', player), 'Kak Impas Ledge -> Kak Impas House Back', player)
            if impas_front is not None and impas_back is not None and not same_hint_area(impas_front, impas_back):
                raise EntranceShuffleError('Kak Impas House entrances are not in the same hint area')
            elif (impas_front and not impas_back) or (not impas_front and impas_back):
                impas_placed_entrance = impas_front if impas_front else impas_back
                if get_hint_area(impas_placed_entrance) not in multi_interior_regions:
                    raise EntranceShuffleError('Kak Impas House entrances can never be in the same hint area')

    # Check basic refills, time passing, return to ToT
    if (ootworld.shuffle_special_interior_entrances or ootworld.shuffle_overworld_entrances or ootworld.spawn_positions) and \
        (entrance_placed == None or entrance_placed.type in ['SpecialInterior', 'Overworld', 'Spawn', 'WarpSong', 'OwlDrop']):
        
        valid_starting_regions = {'Kokiri Forest', 'Kakariko Village'}
        if not any(region for region in valid_starting_regions if none_state.can_reach(region, 'Region', player)):
            raise EntranceShuffleError('Invalid starting area')

        if not (any(region for region in time_travel_state.child_reachable_regions[player] if region.time_passes) and
                any(region for region in time_travel_state.adult_reachable_regions[player] if region.time_passes)):
            raise EntranceShuffleError('Time passing is not guaranteed as both ages')

        if ootworld.starting_age == 'child' and (multiworld.get_region('Temple of Time', player) not in time_travel_state.adult_reachable_regions[player]):
            raise EntranceShuffleError('Path to ToT as adult not guaranteed')
        if ootworld.starting_age == 'adult' and (multiworld.get_region('Temple of Time', player) not in time_travel_state.child_reachable_regions[player]):
            raise EntranceShuffleError('Path to ToT as child not guaranteed')

    if (ootworld.shuffle_interior_entrances or ootworld.shuffle_overworld_entrances) and \
        (entrance_placed == None or entrance_placed.type in ['Interior', 'SpecialInterior', 'Overworld', 'Spawn', 'WarpSong', 'OwlDrop']):
        # Ensure big poe shop is always reachable as adult
        if multiworld.get_region('Market Guard House', player) not in time_travel_state.adult_reachable_regions[player]:
            raise EntranceShuffleError('Big Poe Shop access not guaranteed as adult')
        if ootworld.shopsanity == 'off':
            # Ensure that Goron and Zora shops are accessible as adult
            if multiworld.get_region('GC Shop', player) not in all_state.adult_reachable_regions[player]:
                raise EntranceShuffleError('Goron City Shop not accessible as adult')
            if multiworld.get_region('ZD Shop', player) not in all_state.adult_reachable_regions[player]:
                raise EntranceShuffleError('Zora\'s Domain Shop not accessible as adult')
        if ootworld.open_forest == 'closed':
            # Ensure that Kokiri Shop is reachable as child with no items
            if multiworld.get_region('KF Kokiri Shop', player) not in none_state.child_reachable_regions[player]:
                raise EntranceShuffleError('Kokiri Forest Shop not accessible as child in closed forest')



# Recursively check if a given entrance is unreachable as a given age
def entrance_unreachable_as(entrance, age, already_checked=[]):
    already_checked.append(entrance)

    if entrance.type in {'WarpSong', 'Overworld'}:
        return False
    elif entrance.type == 'OwlDrop':
        return age == 'adult'
    elif entrance.name == 'Child Spawn -> KF Links House':
        return age == 'adult'
    elif entrance.name == 'Adult Spawn -> Temple of Time': 
        return age == 'child'

    for parent_entrance in entrance.parent_region.entrances:
        if parent_entrance in already_checked:
            continue
        unreachable = entrance_unreachable_as(parent_entrance, age, already_checked)
        if not unreachable:
            return False
    return True

def same_hint_area(first, second):
    try:
        return get_hint_area(first) == get_hint_area(second)
    except HintAreaNotFound:
        return False

def get_entrance_replacing(region, entrance_name, player):
    original_entrance = region.multiworld.get_entrance(entrance_name, player)
    if not original_entrance.shuffled:
        return original_entrance

    try:
        return next(filter(lambda entrance: entrance.replaces and entrance.replaces.name == entrance_name and \
                                            entrance.parent_region and entrance.parent_region.name != 'Root Exits' and \
                                            entrance.type not in ('OwlDrop', 'Spawn', 'WarpSong') and entrance.player == player, 
                                            region.entrances))
    except StopIteration:
        return None

def change_connections(entrance, target):
    entrance.connect(target.disconnect())
    entrance.replaces = target.replaces
    if entrance.reverse and not entrance.multiworld.worlds[entrance.player].decouple_entrances:
        target.replaces.reverse.connect(entrance.reverse.assumed.disconnect())
        target.replaces.reverse.replaces = entrance.reverse

def restore_connections(entrance, target):
    target.connect(entrance.disconnect())
    entrance.replaces = None
    if entrance.reverse and not entrance.multiworld.worlds[entrance.player].decouple_entrances:
        entrance.reverse.assumed.connect(target.replaces.reverse.disconnect())
        target.replaces.reverse.replaces = None

def check_entrances_compatibility(entrance, target, rollbacks):
    # An entrance shouldn't be connected to its own scene
    if entrance.parent_region.get_scene() and entrance.parent_region.get_scene() == target.connected_region.get_scene():
        raise EntranceShuffleError('Self-scene connections are forbidden')

    # One-way entrances shouldn't lead to the same scene as other one-ways
    if entrance.type in {'OwlDrop', 'Spawn', 'WarpSong'} and \
        any([rollback[0].connected_region.get_scene() == target.connected_region.get_scene() for rollback in rollbacks]):
        raise EntranceShuffleError('Another one-way entrance leads to the same scene')

def confirm_replacement(entrance, target):
    delete_target_entrance(target)
    logging.getLogger('').debug(f'Connected {entrance} to {entrance.connected_region}')
    if entrance.reverse and not entrance.multiworld.worlds[entrance.player].decouple_entrances:
        replaced_reverse = target.replaces.reverse
        delete_target_entrance(entrance.reverse.assumed)
        logging.getLogger('').debug(f'Connected {replaced_reverse} to {replaced_reverse.connected_region}')


def delete_target_entrance(target):
    if target.connected_region != None:
        target.disconnect()
    if target.parent_region != None:
        target.parent_region.exits.remove(target)
        target.parent_region = None
    del target
