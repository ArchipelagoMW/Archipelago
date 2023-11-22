console.clear()
math.randomseed(os.time())
client_communication_path = os.getenv('LOCALAPPDATA') .. "\\KHCOM\\"

function define_item_ids()
    item_ids = {}
    item_ids["Bronze Card Pack"]                 = 2661001
    item_ids["Silver Card Pack"]                 = 2661002
    item_ids["Gold Card Pack"]                   = 2661003
    
    item_ids["Kingdom Key 1-3"]                  = 2661011
    item_ids["Kingdom Key 4-6"]                  = 2661012
    item_ids["Kingdom Key 7-9"]                  = 2661013
    item_ids["Kingdom Key 0"]                    = 2661014
    item_ids["Three Wishes 1-3"]                 = 2661021
    item_ids["Three Wishes 4-6"]                 = 2661022
    item_ids["Three Wishes 7-9"]                 = 2661023
    item_ids["Three Wishes 0"]                   = 2661024
    item_ids["Crabclaw 1-3"]                     = 2661031
    item_ids["Crabclaw 4-6"]                     = 2661032
    item_ids["Crabclaw 7-9"]                     = 2661033
    item_ids["Crabclaw 0"]                       = 2661034
    item_ids["Pumpkinhead 1-3"]                  = 2661041
    item_ids["Pumpkinhead 4-6"]                  = 2661042
    item_ids["Pumpkinhead 7-9"]                  = 2661043
    item_ids["Pumpkinhead 0"]                    = 2661044
    item_ids["Fairy Harp 1-3"]                   = 2661051
    item_ids["Fairy Harp 4-6"]                   = 2661052
    item_ids["Fairy Harp 7-9"]                   = 2661053
    item_ids["Fairy Harp 0"]                     = 2661054
    item_ids["Wishing Star 1-3"]                 = 2661061
    item_ids["Wishing Star 4-6"]                 = 2661062
    item_ids["Wishing Star 7-9"]                 = 2661063
    item_ids["Wishing Star 0"]                   = 2661064
    item_ids["Spellbinder 1-3"]                  = 2661071
    item_ids["Spellbinder 4-6"]                  = 2661072
    item_ids["Spellbinder 7-9"]                  = 2661073
    item_ids["Spellbinder 0"]                    = 2661074
    item_ids["Metal Chocobo 1-3"]                = 2661081
    item_ids["Metal Chocobo 4-6"]                = 2661082
    item_ids["Metal Chocobo 7-9"]                = 2661083
    item_ids["Metal Chocobo 0"]                  = 2661084
    item_ids["Olympia 1-3"]                      = 2661091
    item_ids["Olympia 4-6"]                      = 2661092
    item_ids["Olympia 7-9"]                      = 2661093
    item_ids["Olympia 0"]                        = 2661094
    item_ids["Lionheart 1-3"]                    = 2661101
    item_ids["Lionheart 4-6"]                    = 2661102
    item_ids["Lionheart 7-9"]                    = 2661103
    item_ids["Lionheart 0"]                      = 2661104
    item_ids["Lady Luck 1-3"]                    = 2661111
    item_ids["Lady Luck 4-6"]                    = 2661112
    item_ids["Lady Luck 7-9"]                    = 2661113
    item_ids["Lady Luck 0"]                      = 2661114
    item_ids["Divine Rose 1-3"]                  = 2661121
    item_ids["Divine Rose 4-6"]                  = 2661122
    item_ids["Divine Rose 7-9"]                  = 2661123
    item_ids["Divine Rose 0"]                    = 2661124
    item_ids["Oathkeeper 1-3"]                   = 2661131
    item_ids["Oathkeeper 4-6"]                   = 2661132
    item_ids["Oathkeeper 7-9"]                   = 2661133
    item_ids["Oathkeeper 0"]                     = 2661134
    item_ids["Oblivion 1-3"]                     = 2661141
    item_ids["Oblivion 4-6"]                     = 2661142
    item_ids["Oblivion 7-9"]                     = 2661143
    item_ids["Oblivion 0"]                       = 2661144
    item_ids["Diamond Dust 1-3"]                 = 2661151
    item_ids["Diamond Dust 4-6"]                 = 2661152
    item_ids["Diamond Dust 7-9"]                 = 2661153
    item_ids["Diamond Dust 0"]                   = 2661154
    item_ids["One Winged Angel 1-3"]             = 2661161
    item_ids["One Winged Angel 4-6"]             = 2661162
    item_ids["One Winged Angel 7-9"]             = 2661163
    item_ids["One Winged Angel 0"]               = 2661164
    item_ids["Ultima Weapon 1-3"]                = 2661171
    item_ids["Ultima Weapon 4-6"]                = 2661172
    item_ids["Ultima Weapon 7-9"]                = 2661173
    item_ids["Ultima Weapon 0"]                  = 2661174
    item_ids["Fire 1-3"]                         = 2661181
    item_ids["Fire 4-6"]                         = 2661182
    item_ids["Fire 7-9"]                         = 2661183
    item_ids["Fire 0"]                           = 2661184
    item_ids["Blizzard 1-3"]                     = 2661191
    item_ids["Blizzard 4-6"]                     = 2661192
    item_ids["Blizzard 7-9"]                     = 2661193
    item_ids["Blizzard 0"]                       = 2661194
    item_ids["Thunder 1-3"]                      = 2661201
    item_ids["Thunder 4-6"]                      = 2661202
    item_ids["Thunder 7-9"]                      = 2661203
    item_ids["Thunder 0"]                        = 2661204
    item_ids["Cure 1-3"]                         = 2661211
    item_ids["Cure 4-6"]                         = 2661212
    item_ids["Cure 7-9"]                         = 2661213
    item_ids["Cure 0"]                           = 2661214
    item_ids["Gravity 1-3"]                      = 2661221
    item_ids["Gravity 4-6"]                      = 2661222
    item_ids["Gravity 7-9"]                      = 2661223
    item_ids["Gravity 0"]                        = 2661224
    item_ids["Stop 1-3"]                         = 2661231
    item_ids["Stop 4-6"]                         = 2661232
    item_ids["Stop 7-9"]                         = 2661233
    item_ids["Stop 0"]                           = 2661234
    item_ids["Aero 1-3"]                         = 2661241
    item_ids["Aero 4-6"]                         = 2661242
    item_ids["Aero 7-9"]                         = 2661243
    item_ids["Aero 0"]                           = 2661244
    item_ids["Simba 1-3"]                        = 2661251
    item_ids["Simba 4-6"]                        = 2661252
    item_ids["Simba 7-9"]                        = 2661253
    item_ids["Simba 0"]                          = 2661254
    item_ids["Genie 1-3"]                        = 2661261
    item_ids["Genie 4-6"]                        = 2661262
    item_ids["Genie 7-9"]                        = 2661263
    item_ids["Genie 0"]                          = 2661264
    item_ids["Bambi 1-3"]                        = 2661271
    item_ids["Bambi 4-6"]                        = 2661272
    item_ids["Bambi 7-9"]                        = 2661273
    item_ids["Bambi 0"]                          = 2661274
    item_ids["Dumbo 1-3"]                        = 2661281
    item_ids["Dumbo 4-6"]                        = 2661282
    item_ids["Dumbo 7-9"]                        = 2661283
    item_ids["Dumbo 0"]                          = 2661284
    item_ids["Tinker Bell 1-3"]                  = 2661291
    item_ids["Tinker Bell 4-6"]                  = 2661292
    item_ids["Tinker Bell 7-9"]                  = 2661293
    item_ids["Tinker Bell 0"]                    = 2661294
    item_ids["Mushu 1-3"]                        = 2661301
    item_ids["Mushu 4-6"]                        = 2661302
    item_ids["Mushu 7-9"]                        = 2661303
    item_ids["Mushu 0"]                          = 2661304
    item_ids["Cloud 1-3"]                        = 2661311
    item_ids["Cloud 4-6"]                        = 2661312
    item_ids["Cloud 7-9"]                        = 2661313
    item_ids["Cloud 0"]                          = 2661314
    item_ids["Potion 1-3"]                       = 2661321
    item_ids["Potion 4-6"]                       = 2661322
    item_ids["Potion 7-9"]                       = 2661323
    item_ids["Potion 0"]                         = 2661324
    item_ids["Hi-Potion 1-3"]                    = 2661331
    item_ids["Hi-Potion 4-6"]                    = 2661332
    item_ids["Hi-Potion 7-9"]                    = 2661333
    item_ids["Hi-Potion 0"]                      = 2661334
    item_ids["Mega-Potion 1-3"]                  = 2661341
    item_ids["Mega-Potion 4-6"]                  = 2661342
    item_ids["Mega-Potion 7-9"]                  = 2661343
    item_ids["Mega-Potion 0"]                    = 2661344
    item_ids["Ether 1-3"]                        = 2661351
    item_ids["Ether 4-6"]                        = 2661352
    item_ids["Ether 7-9"]                        = 2661353
    item_ids["Ether 0"]                          = 2661354
    item_ids["Mega-Ether 1-3"]                   = 2661361
    item_ids["Mega-Ether 4-6"]                   = 2661362
    item_ids["Mega-Ether 7-9"]                   = 2661363
    item_ids["Mega-Ether 0"]                     = 2661364
    item_ids["Elixir 1-3"]                       = 2661371
    item_ids["Elixir 4-6"]                       = 2661372
    item_ids["Elixir 7-9"]                       = 2661373
    item_ids["Elixir 0"]                         = 2661374
    item_ids["Megalixir 1-3"]                    = 2661381
    item_ids["Megalixir 4-6"]                    = 2661382
    item_ids["Megalixir 7-9"]                    = 2661383
    item_ids["Megalixir 0"]                      = 2661384
    
    item_ids["Enemy Card Shadow"]                = 2662001
    item_ids["Enemy Card Soldier"]               = 2662002
    item_ids["Enemy Card Large Body"]            = 2662003
    item_ids["Enemy Card Red Nocturne"]          = 2662004
    item_ids["Enemy Card Blue Rhapsody"]         = 2662005
    item_ids["Enemy Card Yellow Opera"]          = 2662006
    item_ids["Enemy Card Green Requiem"]         = 2662007
    item_ids["Enemy Card Powerwild"]             = 2662008
    item_ids["Enemy Card Bouncywild"]            = 2662009
    item_ids["Enemy Card Air Soldier"]           = 2662010
    item_ids["Enemy Card Bandit"]                = 2662011
    item_ids["Enemy Card Fat Bandit"]            = 2662012
    item_ids["Enemy Card Barrel Spider"]         = 2662013
    item_ids["Enemy Card Search Ghost"]          = 2662014
    item_ids["Enemy Card Sea Neon"]              = 2662015
    item_ids["Enemy Card Screwdiver"]            = 2662016
    item_ids["Enemy Card Aquatank"]              = 2662017
    item_ids["Enemy Card Wight Knight"]          = 2662018
    item_ids["Enemy Card Gargoyle"]              = 2662019
    item_ids["Enemy Card Pirate"]                = 2662020
    item_ids["Enemy Card Air Pirate"]            = 2662021
    item_ids["Enemy Card Darkball"]              = 2662022
    item_ids["Enemy Card Defender"]              = 2662023
    item_ids["Enemy Card Wyvern"]                = 2662024
    item_ids["Enemy Card Neoshadow"]             = 2662025
    item_ids["Enemy Card White Mushroom"]        = 2662026
    item_ids["Enemy Card Black Fungus"]          = 2662027
    item_ids["Enemy Card Creeper Plant"]         = 2662028
    item_ids["Enemy Card Tornado Step"]          = 2662029
    item_ids["Enemy Card Crescendo"]             = 2662030
    item_ids["Enemy Card Guard Armor"]           = 2662031
    item_ids["Enemy Card Parasite Cage"]         = 2662032
    item_ids["Enemy Card Trickmaster"]           = 2662033
    item_ids["Enemy Card Darkside"]              = 2662034
    item_ids["Enemy Card Card Soldier (Red)"]    = 2662035
    item_ids["Enemy Card Card Soldier (Black)"]  = 2662036
    item_ids["Enemy Card Hades"]                 = 2662037
    item_ids["Enemy Card Jafar"]                 = 2662039
    item_ids["Enemy Card Oogie Boogie"]          = 2662040
    item_ids["Enemy Card Ursula"]                = 2662041
    item_ids["Enemy Card Hook"]                  = 2662042
    item_ids["Enemy Card Dragon Maleficent"]     = 2662043
    item_ids["Enemy Card Riku"]                  = 2662044
    item_ids["Enemy Card Larxene"]               = 2662045
    item_ids["Enemy Card Vexen"]                 = 2662046
    item_ids["Enemy Card Marluxia"]              = 2662047
    item_ids["Enemy Card Lexaeus"]               = 2662048
    item_ids["Enemy Card Ansem"]                 = 2662049
    item_ids["Enemy Card Axel"]                  = 2662050
    
    item_ids["Key of Beginnings F02"]            = 2663002
    item_ids["Key of Beginnings F03"]            = 2663003
    item_ids["Key of Beginnings F04"]            = 2663004
    item_ids["Key of Beginnings F05"]            = 2663005
    item_ids["Key of Beginnings F06"]            = 2663006
    item_ids["Key of Beginnings F07"]            = 2663007
    item_ids["Key of Beginnings F08"]            = 2663008
    item_ids["Key of Beginnings F09"]            = 2663009
    item_ids["Key of Beginnings F10"]            = 2663010
    item_ids["Key of Beginnings F11"]            = 2663011
    item_ids["Key of Beginnings F12"]            = 2663012
    item_ids["Key of Beginnings F13"]            = 2663013
    item_ids["Key of Guidance F02"]              = 2663102
    item_ids["Key of Guidance F03"]              = 2663103
    item_ids["Key of Guidance F04"]              = 2663104
    item_ids["Key of Guidance F05"]              = 2663105
    item_ids["Key of Guidance F06"]              = 2663106
    item_ids["Key of Guidance F07"]              = 2663107
    item_ids["Key of Guidance F08"]              = 2663108
    item_ids["Key of Guidance F09"]              = 2663109
    item_ids["Key of Guidance F12"]              = 2663112
    item_ids["Key to Truth F02"]                 = 2663202
    item_ids["Key to Truth F03"]                 = 2663203
    item_ids["Key to Truth F04"]                 = 2663204
    item_ids["Key to Truth F05"]                 = 2663205
    item_ids["Key to Truth F06"]                 = 2663206
    item_ids["Key to Truth F07"]                 = 2663207
    item_ids["Key to Truth F08"]                 = 2663208
    item_ids["Key to Truth F09"]                 = 2663209
    item_ids["Key to Rewards F01"]               = 2663301
    item_ids["Key to Rewards F02"]               = 2663302
    item_ids["Key to Rewards F03"]               = 2663303
    item_ids["Key to Rewards F04"]               = 2663304
    item_ids["Key to Rewards F05"]               = 2663305
    item_ids["Key to Rewards F06"]               = 2663306
    item_ids["Key to Rewards F07"]               = 2663307
    item_ids["Key to Rewards F08"]               = 2663308
    item_ids["Key to Rewards F09"]               = 2663309
    item_ids["Key to Rewards F11"]               = 2663311
    item_ids["Key to Rewards F12"]               = 2663312
    item_ids["Key to Rewards F13"]               = 2663313
    item_ids["Donald"]                           = 2665001
    item_ids["Goofy"]                            = 2665002
    item_ids["Aladdin"]                          = 2665003
    item_ids["Ariel"]                            = 2665004
    item_ids["Beast"]                            = 2665005
    item_ids["Peter Pan"]                        = 2665006
    item_ids["Jack"]                             = 2665007
    return item_ids
end

function define_battle_cards()
    battle_cards = {}
    battle_cards["Kingdom Key"] = {0x000, 0x009}
    battle_cards["Three Wishes"] = {0x00A, 0x013}
    battle_cards["Crabclaw"] = {0x014, 0x01D}
    battle_cards["Pumpkinhead"] = {0x01E, 0x027}
    battle_cards["Fairy Harp"] = {0x028, 0x031}
    battle_cards["Wishing Star"] = {0x032, 0x03B}
    battle_cards["Spellbinder"] = {0x03C, 0x045}
    battle_cards["Metal Chocobo"] = {0x046, 0x04F}
    battle_cards["Olympia"] = {0x050, 0x059}
    battle_cards["Lionheart"] = {0x05A, 0x063}
    battle_cards["Lady Luck"] = {0x064, 0x06D}
    battle_cards["Divine Rose"] = {0x06E, 0x077}
    battle_cards["Oathkeeper"] = {0x078, 0x081}
    battle_cards["Oblivion"] = {0x082, 0x08B}
    battle_cards["Diamond Dust"] = {0x08C, 0x095}
    battle_cards["One Winged Angel"] = {0x096, 0x09F}
    battle_cards["Ultima Weapon"] = {0x0A0, 0x0A9}
    battle_cards["Fire"] = {0x0AA, 0x0B3}
    battle_cards["Blizzard"] = {0x0B4, 0x0BD}
    battle_cards["Thunder"] = {0x0BE, 0x0C7}
    battle_cards["Cure"] = {0x0C8, 0x0D1}
    battle_cards["Gravity"] = {0x0D2, 0x0DB}
    battle_cards["Stop"] = {0x0DC, 0x0E5}
    battle_cards["Aero"] = {0x0E6, 0x0EF}
    battle_cards["Simba"] = {0x104, 0x10D}
    battle_cards["Genie"] = {0x10E, 0x117}
    battle_cards["Bambi"] = {0x118, 0x121}
    battle_cards["Dumbo"] = {0x122, 0x12B}
    battle_cards["Tinker Bell"] = {0x12C, 0x135}
    battle_cards["Mushu"] = {0x136, 0x13F}
    battle_cards["Cloud"] = {0x140, 0x149}
    battle_cards["Potion"] = {0x17C, 0x185}
    battle_cards["Hi-Potion"] = {0x186, 0x18F}
    battle_cards["Mega-Potion"] = {0x190, 0x199}
    battle_cards["Ether"] = {0x19A, 0x1A3}
    battle_cards["Mega-Ether"] = {0x1A4, 0x1AD}
    battle_cards["Elixir"] = {0x1AE, 0x1B7}
    battle_cards["Megalixir"] = {0x1B8, 0x1C1}
    battle_cards["Guard Armor"] = {0x21D, 0x21D}
    battle_cards["Parasite Cage"] = {0x21E, 0x21E}
    battle_cards["Trickmaster"] = {0x21F, 0x21F}
    battle_cards["Darkside"] = {0x220, 0x220}
    battle_cards["Hades"] = {0x227, 0x227}
    battle_cards["Jafar"] = {0x228, 0x228}
    battle_cards["Oogie Boogie"] = {0x229, 0x229}
    battle_cards["Ursula"] = {0x22A, 0x22A}
    battle_cards["Hook"] = {0x22B, 0x22B}
    battle_cards["Dragon Maleficent"] = {0x22C, 0x22C}
    battle_cards["Shadow"] = {0x1C2, 0x1C4}
    battle_cards["Soldier"] = {0x1C5, 0x1C7}
    battle_cards["Large Body"] = {0x1C8, 0x1CA}
    battle_cards["Red Nocturne"] = {0x1CB, 0x1CD}
    battle_cards["Blue Rhapsody"] = {0x1CE, 0x1D0}
    battle_cards["Yellow Opera"] = {0x1D1, 0x1D3}
    battle_cards["Green Requiem"] = {0x1D4, 0x1D6}
    battle_cards["Powerwild"] = {0x1D7, 0x1D9}
    battle_cards["Bouncywild"] = {0x1DA, 0x1DC}
    battle_cards["Air Soldier"] = {0x1DD, 0x1DF}
    battle_cards["Bandit"] = {0x1E0, 0x1E2}
    battle_cards["Fat Bandit"] = {0x1E3, 0x1E5}
    battle_cards["Barrel Spider"] = {0x1E6, 0x1E8}
    battle_cards["Search Ghost"] = {0x1E9, 0x1EB}
    battle_cards["Sea Neon"] = {0x1EC, 0x1EE}
    battle_cards["Screwdiver"] = {0x1EF, 0x1F1}
    battle_cards["Aquatank"] = {0x1F2, 0x1F4}
    battle_cards["Wight Knight"] = {0x1F5, 0x1F7}
    battle_cards["Gargoyle"] = {0x1F8, 0x1FA}
    battle_cards["Pirate"] = {0x1FB, 0x1FD}
    battle_cards["Air Pirate"] = {0x1FE, 0x200}
    battle_cards["Darkball"] = {0x201, 0x203}
    battle_cards["Defender"] = {0x204, 0x206}
    battle_cards["Wyvern"] = {0x207, 0x209}
    battle_cards["Wizard"] = {0x20A, 0x20C}
    battle_cards["Neoshadow"] = {0x20D, 0x20F}
    battle_cards["White Mushroom"] = {0x210, 0x210}
    battle_cards["Black Fungus"] = {0x211, 0x213}
    battle_cards["Creeper Plant"] = {0x214, 0x216}
    battle_cards["Tornado Step"] = {0x217, 0x219}
    battle_cards["Crescendo"] = {0x21A, 0x21C}
    battle_cards["Card Soldier (Red)"] = {0x221, 0x223}
    battle_cards["Card Soldier (Black)"] = {0x224, 0x226}
    battle_cards["Riku"] = {0x22D, 0x22D}
    battle_cards["Axel"] = {0x22E, 0x22E}
    battle_cards["Larxene"] = {0x22F, 0x22F}
    battle_cards["Vexen"] = {0x230, 0x230}
    battle_cards["Marluxia"] = {0x231, 0x231}
    battle_cards["Lexaeus"] = {0x233, 0x233}
    battle_cards["Ansem"] = {0x234, 0x234}
    return battle_cards
end

function define_win_conditions()
    win_conditions = {}
    win_conditions["Donald"] = 0x0F1
    win_conditions["Goofy"] = 0x0FB
    win_conditions["Aladdin"] = 0x14B
    win_conditions["Ariel"] = 0x155
    win_conditions["Jack"] = 0x15F
    win_conditions["Peter Pan"] = 0x169
    win_conditions["Beast"] = 0x173
    return win_conditions
end

function define_char_to_hex_map()
    char_to_hex_map = {}
    char_to_hex_map[" "] = 0x20
    char_to_hex_map["!"] = 0x21
    char_to_hex_map["#"] = 0x23
    char_to_hex_map["%"] = 0x25
    char_to_hex_map["&"] = 0x26
    char_to_hex_map["'"] = 0x27
    char_to_hex_map["("] = 0x28
    char_to_hex_map[")"] = 0x28
    char_to_hex_map["*"] = 0x2A
    char_to_hex_map["+"] = 0x2B
    char_to_hex_map[","] = 0x2C
    char_to_hex_map["-"] = 0x2D
    char_to_hex_map["."] = 0x00
    char_to_hex_map["/"] = 0x2F
    char_to_hex_map["0"] = 0x30
    char_to_hex_map["1"] = 0x31
    char_to_hex_map["2"] = 0x32
    char_to_hex_map["3"] = 0x33
    char_to_hex_map["4"] = 0x34
    char_to_hex_map["5"] = 0x35
    char_to_hex_map["6"] = 0x36
    char_to_hex_map["7"] = 0x37
    char_to_hex_map["8"] = 0x38
    char_to_hex_map["9"] = 0x39
    char_to_hex_map[";"] = 0x3B
    char_to_hex_map["<"] = 0x3C
    char_to_hex_map["="] = 0x3D
    char_to_hex_map[">"] = 0x62
    char_to_hex_map["?"] = 0x3F
    char_to_hex_map["@"] = 0x40
    char_to_hex_map["A"] = 0x41
    char_to_hex_map["B"] = 0x42
    char_to_hex_map["C"] = 0x43
    char_to_hex_map["D"] = 0x44
    char_to_hex_map["E"] = 0x45
    char_to_hex_map["F"] = 0x46
    char_to_hex_map["G"] = 0x47
    char_to_hex_map["H"] = 0x48
    char_to_hex_map["I"] = 0x49
    char_to_hex_map["J"] = 0x4A
    char_to_hex_map["K"] = 0x4B
    char_to_hex_map["L"] = 0x4C
    char_to_hex_map["M"] = 0x4D
    char_to_hex_map["N"] = 0x4E
    char_to_hex_map["O"] = 0x4F
    char_to_hex_map["P"] = 0x50
    char_to_hex_map["Q"] = 0x51
    char_to_hex_map["R"] = 0x52
    char_to_hex_map["S"] = 0x53
    char_to_hex_map["T"] = 0x54
    char_to_hex_map["U"] = 0x55
    char_to_hex_map["V"] = 0x56
    char_to_hex_map["W"] = 0x57
    char_to_hex_map["X"] = 0x58
    char_to_hex_map["Y"] = 0x59
    char_to_hex_map["Z"] = 0x5A
    char_to_hex_map["a"] = 0x61
    char_to_hex_map["b"] = 0x62
    char_to_hex_map["c"] = 0x63
    char_to_hex_map["d"] = 0x64
    char_to_hex_map["e"] = 0x65
    char_to_hex_map["f"] = 0x66
    char_to_hex_map["g"] = 0x67
    char_to_hex_map["h"] = 0x68
    char_to_hex_map["i"] = 0x69
    char_to_hex_map["j"] = 0x6A
    char_to_hex_map["k"] = 0x6B
    char_to_hex_map["l"] = 0x6C
    char_to_hex_map["m"] = 0x6D
    char_to_hex_map["n"] = 0x6E
    char_to_hex_map["o"] = 0x6F
    char_to_hex_map["p"] = 0x70
    char_to_hex_map["q"] = 0x71
    char_to_hex_map["r"] = 0x72
    char_to_hex_map["s"] = 0x73
    char_to_hex_map["t"] = 0x74
    char_to_hex_map["u"] = 0x75
    char_to_hex_map["v"] = 0x76
    char_to_hex_map["w"] = 0x77
    char_to_hex_map["x"] = 0x78
    char_to_hex_map["y"] = 0x79
    char_to_hex_map["z"] = 0x7A
    return char_to_hex_map
end

function define_exceptions()
    exceptions = {
        0x0AF, --Axel Fire 5
        0x189, --Cloud Hi-Potion 3
        0x19D, --Agrabah RoG Ether 3
        0x0C5, --Larxene Thunder 7
        0x0EC, --Riku Aero 6
        0x192, --Riku Mega Potion 2
        0x125, --Monstro RoT Dumbo 3
        0x1A8, --Vexen Mega-Ether 4
    }
    return exceptions
end

function define_journal_bit_location_ids()
    journal_bit_location_ids = {}
    journal_bit_location_ids[0x02039CE4] = {2670107, 2670608, 2670907, 2671208, 2670108, 2670209, 2670306, 2670509}
    journal_bit_location_ids[0x02039CE5] = {2670607, 2670404, 2670706, 2670806, 2670906, 2671013, 2671102, 2671207}
    journal_bit_location_ids[0x02039CE6] = {2671302, 2670007, 2670002, 2670003, 2670004, 2670006, 2670005, 2670109}
    journal_bit_location_ids[0x02039CE7] = {2670406, 2671001, 2670908, nil    , 2670104, 2670105, 2670101, 2670103}
    journal_bit_location_ids[0x02039CE8] = {2670302, 2671203, 2671204, 2671202, 2671206, 2671205, 2670102, nil    }
    journal_bit_location_ids[0x02039CE9] = {2671010, 2671301, 2670203, 2670207, 2670208, 2670204, 2670205, 2670206}
    journal_bit_location_ids[0x02039CEA] = {2670305, 2670304, 2670303, 2670503, 2670504, nil    , 2670508, 2670505}
    journal_bit_location_ids[0x02039CEB] = {2670506, 2670507, 2670603, 2670605, 2670602, 2670604, 2670403, 2670402}
    journal_bit_location_ids[0x02039CEC] = {2670702, 2670705, 2670703, 2670704, nil    , 2670803, 2670804, 2670805}
    journal_bit_location_ids[0x02039CED] = {2670802, 2670905, 2670902, 2670904, 2670903, 2671011, 2671006, 2671005}
    journal_bit_location_ids[0x02039CEE] = {2671008, 2671004, 2671009, 2671007, 2671424, 2671425, 2671416, 2671420}
    journal_bit_location_ids[0x02039CEF] = {2671407, 2671431, 2671415, 2671419, 2671408, 2671402, 2671404, 2671413}
    journal_bit_location_ids[0x02039CF0] = {2671405, 2671423, 2671422, 2671421, 2671403, 2671428, 2671414, 2671418}
    journal_bit_location_ids[0x02039CF1] = {2671401, 2671411, 2671412, 2671430, 2671429, 2671417, 2671427, 2671406}
    journal_bit_location_ids[0x02039CF2] = {2671409, 2671426, 2671410, 2670112, 2670405, 2670210, 2671209, 2670001}
    journal_bit_location_ids[0x02039CF3] = {2670502, 2670701, 2670601, 2670801, 2670401, 2671003, 2670308, 2670301}
    journal_bit_location_ids[0x02039CF4] = {2670111, 2670202, 2670901, 2671201, 2671210, nil    , 2671303, 2671304}
    journal_bit_location_ids[0x02039CF5] = {2670106, 2670009, 2670606, 2670010, 2670501, 2670201, 2670707, 2670110}
    journal_bit_location_ids[0x02039CF6] = {2670511, 2671002, 2670407, 2670807, 2670909, 2670309, 2670008, 2670307}
    journal_bit_location_ids[0x02039CF7] = {2671101, 2670510, 2671012, 2671014, 2671211, nil    , nil    , nil    }
    return journal_bit_location_ids
end

local function has_value (tab, val)
    for index, value in ipairs(tab) do
        if value == val then
            return true
        end
    end

    return false
end

function toBits(num)
    -- returns a table of bits, least significant first.
    local t={} -- will contain the bits
    while num>0 do
        rest=math.fmod(num,2)
        t[#t+1]=rest
        num=(num-rest)/2
    end
    return t
end

item_ids = define_item_ids()
battle_cards = define_battle_cards()
win_conditions = define_win_conditions()
char_to_hex_map = define_char_to_hex_map()
exceptions = define_exceptions()
journal_bit_location_ids = define_journal_bit_location_ids()

pack_size = 3

--Addresses
current_gold_map_cards_addresses = {}
current_gold_map_cards_addresses["Key of Beginnings"] = 0x0203A99D
current_gold_map_cards_addresses["Key of Guidance"] = 0x0203A9A7
current_gold_map_cards_addresses["Key to Truth"] = 0x0203A9B1
current_gold_map_cards_addresses["Key to Rewards"] = 0x0203A9BB
stored_gold_map_cards_addresses = {}
stored_gold_map_cards_addresses["Key of Beginnings"] = {0x0203A99C, 0x0203A99E, 0x0203A99F, 0x0203A9A0, 0x0203A9A1, 0x0203A9A2, 0x0203A9A3, 0x0203A9A4, 0x0203A9A5, 0x0203A99C, 0x0203A99E, 0x0203A99F, 0x0203A9A0}
stored_gold_map_cards_addresses["Key of Guidance"] =   {0x0203A9A6, 0x0203A9A8, 0x0203A9A9, 0x0203A9AA, 0x0203A9AB, 0x0203A9AC, 0x0203A9AD, 0x0203A9AE, 0x0203A9AF, 0x0203A9A6, 0x0203A9A8, 0x0203A9A9, 0x0203A9AA}
stored_gold_map_cards_addresses["Key to Truth"] =      {0x0203A9B0, 0x0203A9B2, 0x0203A9B3, 0x0203A9B4, 0x0203A9B5, 0x0203A9B6, 0x0203A9B7, 0x0203A9B8, 0x0203A9B9, 0x0203A9B0, 0x0203A9B2, 0x0203A9B3, 0x0203A9B4}
stored_gold_map_cards_addresses["Key to Rewards"] =    {0x0203A9BA, 0x0203A9BC, 0x0203A9BD, 0x0203A9BE, 0x0203A9BF, 0x0203A9C0, 0x0203A9C1, 0x0203A9C2, 0x0203A9C3, 0x0203A9BA, 0x0203A9BC, 0x0203A9BD, 0x0203A9BE}
floor_number_address = 0x02039BBE
battle_cards_address = 0x0203A080
time_played_address = 0x02039D8C
check_count_address = 0x02039D22
highest_warp_floor_address = 0x0203C590
moogle_points_address = 0x02039D24
deck_cp_cost_address = 0x02039EBA
deck_card_count_address = 0x02039EBC
deck_card_pointers_addresses = {0x02039DE0, 0x02039EC0, 0x02039FA0}
world_card_addresses = {0x02039D30, 0x02039D31}
world_card_values = {{0x00,0x02}, {0x08,0x00}, {0x04,0x00}, {0x10,0x00}, {0x01,0x00}, {0x20,0x00}
       ,{0x02,0x00}, {0x40,0x00}, {0x80,0x00}, {0x00,0x04}, {0x00,0x08}, {0x00,0x01}, {0x00,0x10}}
floor_assignment_addresses = {0x02039D36,0x02039D3A,0x02039D3E,0x02039D42,0x02039D46,0x02039D4A,0x02039D4E,0x02039D52,0x02039D56,0x02039D5A,0x02039D5E,0x02039D62,0x02039D66}
floor_progress_addresses = {0x02039D34,0x02039D38,0x02039D3C,0x02039D40,0x02039D44,0x02039D48,0x02039D4C,0x02039D50,0x02039D54,0x02039D58,0x02039D5C,0x02039D60, 0x02039D64}
floor_doors_addresses = {0x02039D37,0x02039D3B,0x02039D3F,0x02039D43,0x02039D47,0x02039D4B,0x02039D4F,0x02039D53,0x02039D57,0x02039D5B,0x02039D5F,0x02039D63, 0x02039D67}
floor_assignment_values = {0x0A, 0x04, 0x03, 0x05, 0x01, 0x06, 0x02, 0x07, 0x08, 0x0D, 0x0B, 0x09, 0x0C}


bronze_pack_cards = {"Kingdom Key", "Three Wishes", "Pumpkinhead", "Olympia", "Wishing Star", "Lady Luck", "Fire", "Blizzard", "Thunder", "Simba", "Genie", "Cloud", "Dumbo", "Potion", "Hi-Potion", "Ether"}
silver_pack_cards = {"Lionheart", "Metal Chocobo", "Spellbinder", "Divine Rose", "Crabclaw", "Cure", "Stop", "Gravity", "Aero", "Bambi", "Mushu", "Tinker Bell", "Mega-Potion", "Elixir", "Mega-Ether"}
gold_pack_cards = {"Oathkeeper", "Oblivion", "Diamond Dust", "One Winged Angel", "Ultima Weapon", "Megalixir"}

function save_or_savestate_loaded(past_playtime, current_playtime)
    if current_playtime >= past_playtime then
        if (current_playtime - past_playtime) < 3 then
            return false
        end
    end
    return true
end

function get_floor_number()
    local floor_number = memory.readbyte(floor_number_address) + 1
    return floor_number
end

function get_current_gold_card_qty(gold_card_type)
    local num_of_gold_cards = memory.readbyte(current_gold_map_cards_addresses[gold_card_type])
    return num_of_gold_cards
end

function get_battle_card(offset)
    if memory.read_u16_le(battle_cards_address + (2 * offset)) ~= 0xFFFF then
        return memory.read_u16_le(battle_cards_address + (2 * offset))
    else
        return 0xFFFF
    end
end

function get_battle_cards()
    i = 0
    j = 1
    local battle_cards = {}
    while i < 915 do
        local battle_card = get_battle_card(i)
        if battle_card ~= 0x0FFF then
            battle_cards[j] = battle_card
        end
        j = j + 1
        i = i + 1
    end
    return battle_cards
end

function get_battle_card_type(battle_card_value)
    battle_card_value = battle_card_value % 0x1000
    for k,v in pairs(battle_cards) do
        if battle_card_value >= v[1] and battle_card_value <= v[2] then
            return k
        end
    end
    return "Not Found"
end

function get_playtime()
    local playtime = memory.read_u24_le(time_played_address)
    return playtime
end

function get_stored_gold_cards(key_type, floor_number)
    local num_of_gold_cards = memory.readbyte(stored_gold_map_cards_addresses[key_type][floor_number])
    if floor_number >= 10 then
        if num_of_gold_cards == 2 or num_of_gold_cards == 3 then
            num_of_gold_cards = 1
        else
            num_of_gold_cards = 0
        end
    elseif floor_number <= 4 then
        if num_of_gold_cards == 1 or num_of_gold_cards == 3 then
            num_of_gold_cards = 1
        else
            num_of_gold_cards = 0
        end
    end
    return num_of_gold_cards
end

function get_highest_warp_floor()
    local highest_warp_floor = memory.readbyte(highest_warp_floor_address) / 2 + 1
    return highest_warp_floor
end

function get_deck_pointer(deck_number, offset)
    local deck_pointer = memory.read_u16_le(deck_card_pointers_addresses[deck_number] + 2*offset)
end

function get_deck_pointers()
    local deck_pointers = {}
    i = 1
    while (i <= 3) do
        deck_pointers[i] = {}
        j = 1
        k = 1
        finished = false
        while not finished and k < 100 do
            local deck_pointer = get_deck_pointer(i, j-1)
            if deck_pointer == 0xFFFF then
                finished = true
            else
                deck_pointers[i][j] = deck_pointer
                j = j+1
            end
            k = k + 1
        end
        i = i+1
    end
    return deck_pointers
end

function get_moogle_points()
    return memory.read_u32_le(moogle_points_address)
end

function get_card_base(card_value, premium)
    if premium then
        if card_value > 0x8000 then
            return (card_value % 0x1000) + 0x8000
        end
    end
    return card_value % 0x1000
end

function set_deck_pointer(deck_number, offset, value)
    memory.write_u16_le(deck_card_pointers_addresses[deck_number] + 2*offset, value)
end

function set_starting_deck()
    memory.write_u16_le(deck_cp_cost_address, 43)
    memory.write_u16_le(deck_card_count_address, 0x03)
    
    memory.write_u16_le(battle_cards_address, 0x1008) --Kingdom Key 8
    set_deck_pointer(1, 0, 0x0000)
    memory.write_u16_le(battle_cards_address + 2, 0x1007) --Kingdom Key 7
    set_deck_pointer(1, 1, 0x0001)
    memory.write_u16_le(battle_cards_address + 4, 0x1006) --Kingdom Key 6
    set_deck_pointer(1, 2, 0x0002)
    local i = 4
    while i <= 15 do
        memory.write_u16_le(battle_cards_address + 2*(i-1), 0x0FFF)
        set_deck_pointer(1, i-1, 0xFFFF)
        i = i + 1
    end
end

function set_current_gold_card_qty(gold_card_type, value, floor_number)
    memory.writebyte(current_gold_map_cards_addresses[gold_card_type],value)
    update_current_gold_card_qty(floor_number)
end

function set_stored_gold_cards(gold_card_type, floor_number, x)
    local num_of_gold_cards = memory.readbyte(stored_gold_map_cards_addresses[gold_card_type][floor_number])
    if x > 0 then
        if floor_number >= 10 then
            if num_of_gold_cards == 0 then
                memory.writebyte(stored_gold_map_cards_addresses[gold_card_type][floor_number], 2)
            elseif num_of_gold_cards == 1 then
                memory.writebyte(stored_gold_map_cards_addresses[gold_card_type][floor_number], 3)
            elseif num_of_gold_cards == 2 then
                memory.writebyte(stored_gold_map_cards_addresses[gold_card_type][floor_number], 2)
            elseif num_of_gold_cards == 3 then
                memory.writebyte(stored_gold_map_cards_addresses[gold_card_type][floor_number], 3)
            end
        elseif floor_number <= 4 then
            if num_of_gold_cards == 0 then
                memory.writebyte(stored_gold_map_cards_addresses[gold_card_type][floor_number], 1)
            elseif num_of_gold_cards == 1 then
                memory.writebyte(stored_gold_map_cards_addresses[gold_card_type][floor_number], 1)
            elseif num_of_gold_cards == 2 then
                memory.writebyte(stored_gold_map_cards_addresses[gold_card_type][floor_number], 3)
            elseif num_of_gold_cards == 3 then
                memory.writebyte(stored_gold_map_cards_addresses[gold_card_type][floor_number], 3)
            end
        else
            memory.writebyte(stored_gold_map_cards_addresses[gold_card_type][floor_number], 1)
        end
    elseif x == 0 then
        if floor_number >= 10 then
            if num_of_gold_cards == 0 then
                memory.writebyte(stored_gold_map_cards_addresses[gold_card_type][floor_number], 0)
            elseif num_of_gold_cards == 1 then
                memory.writebyte(stored_gold_map_cards_addresses[gold_card_type][floor_number], 1)
            elseif num_of_gold_cards == 2 then
                memory.writebyte(stored_gold_map_cards_addresses[gold_card_type][floor_number], 0)
            elseif num_of_gold_cards == 3 then
                memory.writebyte(stored_gold_map_cards_addresses[gold_card_type][floor_number], 1)
            end
        elseif floor_number <= 4 then
            if num_of_gold_cards == 0 then
                memory.writebyte(stored_gold_map_cards_addresses[gold_card_type][floor_number], 0)
            elseif num_of_gold_cards == 1 then
                memory.writebyte(stored_gold_map_cards_addresses[gold_card_type][floor_number], 0)
            elseif num_of_gold_cards == 2 then
                memory.writebyte(stored_gold_map_cards_addresses[gold_card_type][floor_number], 2)
            elseif num_of_gold_cards == 3 then
                memory.writebyte(stored_gold_map_cards_addresses[gold_card_type][floor_number], 2)
            end
        else
            memory.writebyte(stored_gold_map_cards_addresses[gold_card_type][floor_number], 0)
        end
    end
end

function set_moogle_points(value)
    memory.write_u32_le(moogle_points_address, value)
end

function can_complete_floor(floor_number)
    if floor_number < 10 then
        return get_stored_gold_cards("Key of Beginnings", floor_number) > 0 and get_stored_gold_cards("Key of Guidance", floor_number) > 0 and get_stored_gold_cards("Key to Truth", floor_number) > 0
    elseif floor_number == 12 then
        return get_stored_gold_cards("Key of Beginnings", floor_number) > 0 and get_stored_gold_cards("Key of Guidance", floor_number) > 0
    elseif floor_number == 11 or floor_number == 10 or floor_number == 13 then
        return get_stored_gold_cards("Key of Beginnings", floor_number) > 0
    else
        return false
    end
end

function update_current_gold_card_qty(current_floor)
    memory.writebyte(current_gold_map_cards_addresses["Key of Beginnings"], get_stored_gold_cards("Key of Beginnings", current_floor))
    if get_stored_gold_cards("Key of Beginnings", current_floor) < 1 then
        memory.writebyte(current_gold_map_cards_addresses["Key of Guidance"], 0x0)
    else
        memory.writebyte(current_gold_map_cards_addresses["Key of Guidance"], get_stored_gold_cards("Key of Guidance", current_floor))
    end
    if get_stored_gold_cards("Key of Beginnings", current_floor) < 1 or get_stored_gold_cards("Key of Guidance", current_floor) < 1 then
        memory.writebyte(current_gold_map_cards_addresses["Key to Truth"], 0x0)
    else
        memory.writebyte(current_gold_map_cards_addresses["Key to Truth"], get_stored_gold_cards("Key to Truth", current_floor))
    end
    memory.writebyte(current_gold_map_cards_addresses["Key to Rewards"], get_stored_gold_cards("Key to Rewards", current_floor))
end

function update_world_cards(current_floor)
    if get_stored_gold_cards("Key of Beginnings", current_floor) > 1 then
        memory.writebyte(world_card_addresses[1], world_card_values[current_floor][1])
        memory.writebyte(world_card_addresses[2], world_card_values[current_floor][2])
    else
        memory.writebyte(world_card_addresses[1], world_card_values[1][1])
        memory.writebyte(world_card_addresses[2], world_card_values[1][2])
    end
end

function update_highest_warp_floor()
    memory.writebyte(highest_warp_floor_address, (14-1)*2)
end

function update_current_floor()
    if get_floor_number() > 0 and get_floor_number() < 14 then
        if get_stored_gold_cards("Key of Beginnings", get_floor_number()) < 1 then
            memory.writebyte(floor_number_address, 0x00)
        end
    end
end

function update_world_assignments()
    i = 1
    while i <= #floor_assignment_values do
        if get_stored_gold_cards("Key of Beginnings", i) < 1 then
            memory.writebyte(floor_assignment_addresses[i], 0x0A)
        else
            memory.writebyte(floor_assignment_addresses[i], floor_assignment_values[i])
        end
        i = i + 1
    end
end

function update_map_cards()
    address = 0x0203A8C0
    while address <= 0x0203A99B do
        if address < 0x0203A992 or address > 0x0203A99B then --skip Moogle Rooms
            memory.writebyte(address, 9)
        else
            memory.writebyte(address, 0)
        end
        address = address + 1
    end
end

function remove_battle_card(card_value)
    local removed = false
   i = 0
   while get_battle_card(i) ~= 0xFFFF and not removed do
       if card_value == get_battle_card(i) then
           memory.write_u16_le(battle_cards_address + (2 * i), 0x0FFF)
           removed = true
       end
       i = i + 1
   end
end

function reassign_deck_pointers(old_deck_pointers)
    for k,v in pairs(old_deck_pointers) do
        for ik,iv in pairs(v) do
            set_deck_pointer(k, ik-1, iv)
        end
    end
end

function remove_new_battle_cards(old_battle_cards, current_battle_cards)
    new_battle_card_types = {}
    old_battle_card_counts = {}
    current_battle_card_counts = {}
    for index,card_value in pairs(old_battle_cards) do
        old_battle_card_counts[get_card_base(card_value, false)] = 0
        current_battle_card_counts[get_card_base(card_value, false)] = 0
    end
    for index,card_value in pairs(current_battle_cards) do
        old_battle_card_counts[get_card_base(card_value, false)] = 0
        current_battle_card_counts[get_card_base(card_value, false)] = 0
    end
    for index,card_value in pairs(old_battle_cards) do
        old_battle_card_counts[get_card_base(card_value, false)] = old_battle_card_counts[get_card_base(card_value, false)] + 1
    end
    for index,card_value in pairs(current_battle_cards) do
        current_battle_card_counts[get_card_base(card_value, false)] = current_battle_card_counts[get_card_base(card_value, false)] + 1
    end
    for card_value, cnt in pairs(current_battle_card_counts) do
        if cnt > old_battle_card_counts[card_value] then
            i = 0
            while i < cnt - old_battle_card_counts[card_value] do
                remove_battle_card(card_value)
                i = i + 1
            end
        end
    end
end

function find_empty_battle_card_offset()
    offset = 0
    while memory.read_u16_le(battle_cards_address + (2 * offset)) ~= 0x0FFF and offset < 915 do
        battle_card = get_battle_card(i)
        offset = offset + 1
    end
    if offset < 915 then
        return offset
    end
    return -1
end

function increment_check_count()
    memory.write_u32_le(moogle_points_address, get_moogle_points() + 1)
end

function write_to_output(file_name, location_name)
    file = io.open("../../worlds/khcom/" .. file_name, "a")
    io.output(file)
    io.write(location_name .. "\n")
    io.close(file)
end

function file_exists(name)
   local f=io.open(name,"r")
   if f~=nil then io.close(f) return true else return false end
end

function add_gold_card(gold_card_name)
    floor_number = tonumber(string.sub(gold_card_name, -2))
    if string.sub(gold_card_name,1,17) == "Key of Beginnings" then
        set_stored_gold_cards("Key of Beginnings", floor_number, 1)
        set_stored_gold_cards("Key of Guidance", floor_number, 1)
        set_stored_gold_cards("Key to Truth", floor_number, 1)
    end
    if string.sub(gold_card_name,1,15) == "Key of Guidance" then
        set_stored_gold_cards("Key of Guidance", floor_number, 1)
    end
    if string.sub(gold_card_name,1,12) == "Key to Truth" then
        set_stored_gold_cards("Key to Truth", floor_number, 1)
    end
    if string.sub(gold_card_name,1,14) == "Key to Rewards" then
        set_stored_gold_cards("Key to Rewards", floor_number, 1)
    end
end

function add_battle_card(battle_card)
    offset = find_empty_battle_card_offset()
    for k,v in pairs(win_conditions) do 
        if k == battle_card then
            memory.write_u16_le(battle_cards_address + (2 * offset), v)
            return
        end
    end
    for k,v in pairs(battle_cards) do 
        if k == battle_card then
            card_value = math.random(0,v[2]-v[1])
            while has_value(exceptions, v[1]+card_value) do
                card_value = math.random(0,v[2]-v[1])
            end
            memory.write_u16_le(battle_cards_address + (2 * offset), v[1]+card_value)
            print("Got Card: " .. battle_card .. " " .. tostring(card_value))
            return
        end
    end
end

function add_battle_card_specific_value(battle_card, value)
    offset = find_empty_battle_card_offset()
    for k,v in pairs(win_conditions) do 
        if k == battle_card then
            memory.write_u16_le(battle_cards_address + (2 * offset), v)
            return
        end
    end
    for k,v in pairs(battle_cards) do 
        if k == battle_card then
            card_value = value
            if not has_value(exceptions, v[1]+card_value) then
                memory.write_u16_le(battle_cards_address + (2 * offset), v[1]+card_value)
                print("Got Card: " .. battle_card .. " " .. tostring(card_value))
            else
                print(battle_card .. " " .. tostring(value) .. " is an exception card, skipping.")
            end
        end
    end
end

function open_card_pack(card_pack)
    print("Opening " .. card_pack)
    if card_pack == "Bronze Card Pack" then
        i = 0
        while i < pack_size do
            add_battle_card(bronze_pack_cards[math.random(1, #bronze_pack_cards)])
            i = i + 1
        end
    end
    if card_pack == "Silver Card Pack" then
        i = 0
        while i < pack_size do
            add_battle_card(silver_pack_cards[math.random(1, #silver_pack_cards)])
            i = i + 1
        end
    end
    if card_pack == "Gold Card Pack" then
        i = 0
        while i < pack_size do
            add_battle_card(gold_pack_cards[math.random(1, #gold_pack_cards)])
            i = i + 1
        end
    end
end

function check_journal()
    for k,v in pairs(journal_bit_location_ids) do
        for ik, iv in pairs(journal_bit_location_ids[k]) do
            if toBits(memory.readbyte(k))[ik] == 1 and iv ~= nil then
                file = io.open(client_communication_path .. "send" .. tostring(iv), "w")
                io.output(file)
                io.write("")
                io.close(file)
            end
        end
    end
end

function receive_items()
    number_of_items_received = 0
    while file_exists(client_communication_path .. "AP_" .. get_moogle_points() + 1 .. ".item") do
        item_found = false
        file = io.open(client_communication_path .. "AP_" .. get_moogle_points() + 1 .. ".item", "r")
        io.input(file)
        received_item_id = tonumber(io.read())
        io.close(file)
        for k,v in pairs(item_ids) do
            if v == received_item_id then
                received_item_name = k
            end
        end
        if string.sub(received_item_name, 1, 3) == "Key" and not item_found then
            add_gold_card(received_item_name)
            item_found = true
        end
        if string.sub(received_item_name, -4) == "Pack" and not item_found then
            open_card_pack(received_item_name)
            item_found = true
        end
        if string.sub(received_item_name, 1, 10) == "Enemy Card" and not item_found then
            add_battle_card(received_item_name:sub(12))
            item_found = true
        end
        if string.sub(received_item_name, -3) == "1-3" and not item_found then
            add_battle_card_specific_value(received_item_name:sub(1, -5), 1)
            add_battle_card_specific_value(received_item_name:sub(1, -5), 2)
            add_battle_card_specific_value(received_item_name:sub(1, -5), 3)
            item_found = true
        end
        if string.sub(received_item_name, -3) == "4-6" and not item_found then
            add_battle_card_specific_value(received_item_name:sub(1, -5), 4)
            add_battle_card_specific_value(received_item_name:sub(1, -5), 5)
            add_battle_card_specific_value(received_item_name:sub(1, -5), 6)
            item_found = true
        end
        if string.sub(received_item_name, -3) == "7-9" and not item_found then
            add_battle_card_specific_value(received_item_name:sub(1, -5), 7)
            add_battle_card_specific_value(received_item_name:sub(1, -5), 8)
            add_battle_card_specific_value(received_item_name:sub(1, -5), 9)
            item_found = true
        end
        if string.sub(received_item_name, -1) == "0" and not item_found then
            add_battle_card_specific_value(received_item_name:sub(1, -3), 0)
            item_found = true
        end
        for k,v in pairs(win_conditions) do
            if not item_found then
                if k == received_item_name then
                    add_battle_card(received_item_name)
                    item_found = true
                end
            end
        end
        for k,v in pairs(battle_cards) do
            if not item_found then
                if k == received_item_name then
                    add_battle_card(received_item_name)
                    item_found = true
                end
            end
        end
        if item_found then
            increment_check_count()
        end
    end
end

function replace_text(address, bytes, new_text)
    local replacement_bytes = {}
    j = 1
    for i = 1, #new_text do
        local c = new_text:sub(i,i)
        replacement_bytes[j] = char_to_hex_map[c]
        replacement_bytes[j+1] = 0x00
        j = j + 2
        i = i + 1
    end
    i = 0
    while i < bytes do
        memory.writebyte(address + i, 0x00)
        i = i + 1
    end
    i = 0
    while i < #replacement_bytes do
        memory.writebyte(address + i, replacement_bytes[i+1])
        i = i + 1
    end
end

function set_key_description_text()
    i=1
    local new_string = ""
    while i <= 13 do
        if get_stored_gold_cards("Key of Beginnings", i)  == 1 then
            new_string = new_string .. tostring(i) .. ","
        end
        i = i + 1
    end
    if new_string ~= "" then
        new_string = new_string:sub(1,-2)
    end
    replace_text(0x09045026, 70, new_string)
    i=1
    new_string = ""
    while i <= 13 do
        if get_stored_gold_cards("Key of Guidance", i)  == 1 then
            new_string = new_string .. tostring(i) .. ","
        end
        i = i + 1
    end
    if new_string ~= "" then
        new_string = new_string:sub(1,-2)
    end
    replace_text(0x0904506E, 70, new_string)
    i=1
    new_string = ""
    while i <= 13 do
        if get_stored_gold_cards("Key to Truth", i)  == 1 then
            new_string = new_string .. tostring(i) .. ","
        end
        i = i + 1
    end
    if new_string ~= "" then
        new_string = new_string:sub(1,-2)
    end
    replace_text(0x090450B6, 70, new_string)
    i=1
    new_string = ""
    while i <= 13 do
        if get_stored_gold_cards("Key to Rewards", i)  == 1 then
            new_string = new_string .. tostring(i) .. ","
        end
        i = i + 1
    end
    if new_string ~= "" then
        new_string = new_string:sub(1,-2)
    end
    replace_text(0x090450FE, 70, new_string)
end

function is_premium(card_value)
    return card_value >= 0x8000
end

function is_used(card_value)
    return (card_value % 0x8000) >= 0x1000
end

function check_if_victorious()
    local i = 0
    local battle_cards = get_battle_cards()
    for k,v in pairs(battle_cards) do
        for ik, iv in pairs(win_conditions) do
            if v == iv then
                i = i + 1
            end
        end
    end
    if i >= 7 then
        send_victory()
    end
end

function update_floor_status()
    i = 2
    while i <= 13 do
        if get_stored_gold_cards("Key of Beginnings", i) < 1 then
            if i == 13 then 
                memory.writebyte(floor_progress_addresses[i], 0x17)
                memory.writebyte(floor_doors_addresses[i], 0x02)
            else
                memory.writebyte(floor_progress_addresses[i], 0x77)
                memory.writebyte(floor_doors_addresses[i], 0x03)
            end
        elseif memory.readbyte(floor_assignment_addresses[i]) == 0x0A and i > 1 then
            memory.writebyte(floor_progress_addresses[i], 0x00)
            memory.writebyte(floor_doors_addresses[i], 0x00)
        end
        i = i + 1
    end
end

function update_post_floor_cutscene_valid()
    i = 2
    while i < 13 do
        if can_complete_floor(i) then
            x = memory.readbyte(floor_progress_addresses[i])
            x = bit.clear(x, 2)
            x = bit.clear(x, 0)
            memory.writebyte(floor_progress_addresses[i],x)
        else
            x = memory.readbyte(floor_progress_addresses[i])
            x = bit.set(x, 2)
            x = bit.set(x, 0)
            memory.writebyte(floor_progress_addresses[i],x)
        end
        i = i + 1
    end
end

function remove_premium_cards()
    local battle_cards = get_battle_cards()
    for k,v in pairs(battle_cards) do
        memory.write_u16_le(battle_cards_address + (2*(k-1)), v%0x8000)
    end
end

function send_victory()
    file = io.open(client_communication_path .. "victory", "w")
    io.output(file)
    io.write("")
    io.close(file)
end

function main_loop(last_variables)
    local frame = emu.framecount()
    local current_playtime = get_playtime()
    if current_playtime == 1 then
        set_starting_deck()
        last_variables["Last Battle Cards"] = get_battle_cards()
        last_variables["Last Moogle Points"] = get_moogle_points()
        set_stored_gold_cards("Key of Beginnings", 1, 1)
        set_stored_gold_cards("Key of Guidance", 1, 1)
        set_stored_gold_cards("Key to Truth", 1, 1)
        update_current_gold_card_qty(1)
    end
    if not save_or_savestate_loaded(last_variables["Last Playtime"], current_playtime) and current_playtime > 3 then
        local current_floor = get_floor_number()
        if current_floor ~= last_variables["Last Floor"] then
            update_world_cards(get_floor_number())
            update_highest_warp_floor()
            last_variables["Last Moogle Points"] = get_moogle_points()
        end
        local current_battle_cards = get_battle_cards()
        last_deck_pointers = get_deck_pointers()
        remove_new_battle_cards(last_variables["Last Battle Cards"], current_battle_cards)
        reassign_deck_pointers(last_deck_pointers)
        set_moogle_points(last_variables["Last Moogle Points"])
    end
    if frame % 180 and current_playtime > 3 then
        check_journal()
        last_deck_pointers = get_deck_pointers()
        receive_items()
        reassign_deck_pointers(last_deck_pointers)
        set_key_description_text()
        check_if_victorious()
        remove_premium_cards()
    end
    update_current_gold_card_qty(get_floor_number())
    last_variables["Last Floor"] = get_floor_number()
    last_variables["Last Battle Cards"] = get_battle_cards()
    last_variables["Last Playtime"] = get_playtime()
    last_variables["Last Highest Warp Floor"] = get_highest_warp_floor()
    last_variables["Last Moogle Points"] = get_moogle_points()
    update_map_cards()
    update_world_cards(get_floor_number())
    update_floor_status()
    update_world_assignments()
    update_post_floor_cutscene_valid()
    return last_variables
end

function main()
    local last_variables = {}
    last_variables["Last Floor"] = get_floor_number()
    last_variables["Last Key of Beginnings"] = get_current_gold_card_qty("Key of Beginnings")
    last_variables["Last Key of Guidance"] = get_current_gold_card_qty("Key of Guidance")
    last_variables["Last Key to Truth"] = get_current_gold_card_qty("Key to Truth")
    last_variables["Last Key to Rewards"] = get_current_gold_card_qty("Key to Rewards")
    last_variables["Last Battle Cards"] = get_battle_cards()
    last_variables["Last Playtime"] = get_playtime()
    last_variables["Last Highest Warp Floor"] = get_highest_warp_floor()
    last_variables["Last Moogle Points"] = get_moogle_points()
    while true do
        local frame = emu.framecount()
        if frame % 20 == 0 then
            local success,err = pcall(main_loop, last_variables)
            if not success then
                print(err)
                client.pause()
                return
            end
        end
        emu.frameadvance()
    end
end

main()