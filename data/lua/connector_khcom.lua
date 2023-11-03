console.clear()
math.randomseed(os.time())
client_communication_path = os.getenv('LOCALAPPDATA') .. "\\KHCOM\\"

function define_location_ids()
    location_ids = {}
    location_ids["Kingdom Key"]           = 2671001
    location_ids["Three Wishes"]          = 2671002
    location_ids["Crabclaw"]              = 2671003
    location_ids["Pumpkinhead"]           = 2671004
    location_ids["Fairy Harp"]            = 2671005
    location_ids["Wishing Star"]          = 2671006
    location_ids["Spellbinder"]           = 2671007
    location_ids["Metal Chocobo"]         = 2671008
    location_ids["Olympia"]               = 2671009
    location_ids["Lionheart"]             = 2671010
    location_ids["Lady Luck"]             = 2671011
    location_ids["Divine Rose"]           = 2671012
    location_ids["Oathkeeper"]            = 2671013
    location_ids["Oblivion"]              = 2671014
    location_ids["Diamond Dust"]          = 2671015
    location_ids["One Winged Angel"]      = 2671016
    location_ids["Fire"]                  = 2671017
    location_ids["Blizzard"]              = 2671018
    location_ids["Thunder"]               = 2671019
    location_ids["Cure"]                  = 2671020
    location_ids["Gravity"]               = 2671021
    location_ids["Stop"]                  = 2671022
    location_ids["Aero"]                  = 2671023
    location_ids["Simba"]                 = 2671024
    location_ids["Genie"]                 = 2671025
    location_ids["Bambi"]                 = 2671026
    location_ids["Dumbo"]                 = 2671027
    location_ids["Tinker Bell"]           = 2671028
    location_ids["Mushu"]                 = 2671029
    location_ids["Cloud"]                 = 2671030
    location_ids["Potion"]                = 2671031
    location_ids["Hi-Potion"]             = 2671032
    location_ids["Mega-Potion"]           = 2671033
    location_ids["Ether"]                 = 2671034
    location_ids["Mega-Ether"]            = 2671035
    location_ids["Elixir"]                = 2671036
    location_ids["Megalixir"]             = 2671037
    location_ids["Guard Armor"]           = 2671038
    location_ids["Parasite Cage"]         = 2671039
    location_ids["Trickmaster"]           = 2671040
    location_ids["Darkside"]              = 2671041
    location_ids["Card Soldier (Red)"]    = 2671042
    location_ids["Hades"]                 = 2671043
    location_ids["Jafar"]                 = 2671044
    location_ids["Oogie Boogie"]          = 2671045
    location_ids["Ursula"]                = 2671046
    location_ids["Hook"]                  = 2671047
    location_ids["Dragon Maleficent"]     = 2671048
    location_ids["Riku"]                  = 2671049
    location_ids["Axel"]                  = 2671050
    location_ids["Larxene"]               = 2671051
    location_ids["Vexen"]                 = 2671052
    location_ids["Marluxia"]              = 2671053
    location_ids["Shadow"]                = 2672001
    location_ids["Soldier"]               = 2672002
    location_ids["Large Body"]            = 2672003
    location_ids["Red Nocturne"]          = 2672004
    location_ids["Blue Rhapsody"]         = 2672005
    location_ids["Yellow Opera"]          = 2672006
    location_ids["Green Requiem"]         = 2672007
    location_ids["Powerwild"]             = 2672008
    location_ids["Bouncywild"]            = 2672009
    location_ids["Air Soldier"]           = 2672010
    location_ids["Bandit"]                = 2672011
    location_ids["Fat Bandit"]            = 2672012
    location_ids["Barrel Spider"]         = 2672013
    location_ids["Search Ghost"]          = 2672014
    location_ids["Sea Neon"]              = 2672015
    location_ids["Screwdriver"]           = 2672016
    location_ids["Aquatank"]              = 2672017
    location_ids["Wight Knight"]          = 2672018
    location_ids["Gargoyle"]              = 2672019
    location_ids["Pirate"]                = 2672020
    location_ids["Air Pirate"]            = 2672021
    location_ids["Darkball"]              = 2672022
    location_ids["Defender"]              = 2672023
    location_ids["Wyvern"]                = 2672024
    location_ids["Neoshadow"]             = 2672025
    location_ids["White Mushroom"]        = 2672026
    location_ids["Black Fungus"]          = 2672027
    location_ids["Creeper Plant"]         = 2672028
    location_ids["Tornado Step"]          = 2672029
    location_ids["Crescendo"]             = 2672030
    location_ids["Wizard"]                = 2672031
    location_ids["Card Soldier (Black)"]  = 2672036
    location_ids["Key of Beginnings F01"] = 2674001
    location_ids["Key of Beginnings F02"] = 2674002
    location_ids["Key of Beginnings F03"] = 2674003
    location_ids["Key of Beginnings F04"] = 2674004
    location_ids["Key of Beginnings F05"] = 2674005
    location_ids["Key of Beginnings F06"] = 2674006
    location_ids["Key of Beginnings F07"] = 2674007
    location_ids["Key of Beginnings F08"] = 2674008
    location_ids["Key of Beginnings F09"] = 2674009
    location_ids["Key of Beginnings F11"] = 2674011
    location_ids["Key of Beginnings F12"] = 2674012
    location_ids["Key of Beginnings F13"] = 2674013
    location_ids["Key of Guidance F01"]   = 2674101
    location_ids["Key of Guidance F02"]   = 2674102
    location_ids["Key of Guidance F03"]   = 2674103
    location_ids["Key of Guidance F04"]   = 2674104
    location_ids["Key of Guidance F05"]   = 2674105
    location_ids["Key of Guidance F06"]   = 2674106
    location_ids["Key of Guidance F07"]   = 2674107
    location_ids["Key of Guidance F08"]   = 2674108
    location_ids["Key of Guidance F09"]   = 2674109
    location_ids["Key of Guidance F12"]   = 2674112
    location_ids["Key to Truth F01"]      = 2674201
    location_ids["Key to Truth F02"]      = 2674202
    location_ids["Key to Truth F03"]      = 2674203
    location_ids["Key to Truth F04"]      = 2674204
    location_ids["Key to Truth F05"]      = 2674205
    location_ids["Key to Truth F06"]      = 2674206
    location_ids["Key to Truth F07"]      = 2674207
    location_ids["Key to Truth F08"]      = 2674208
    location_ids["Key to Truth F09"]      = 2674209
    return location_ids
end

function define_item_ids()
    item_ids = {}
    item_ids["Bronze Card Pack"]      = 2661001
    item_ids["Silver Card Pack"]      = 2661002
    item_ids["Gold Card Pack"]        = 2661003
    item_ids["Key of Beginnings F02"] = 2663002
    item_ids["Key of Beginnings F03"] = 2663003
    item_ids["Key of Beginnings F04"] = 2663004
    item_ids["Key of Beginnings F05"] = 2663005
    item_ids["Key of Beginnings F06"] = 2663006
    item_ids["Key of Beginnings F07"] = 2663007
    item_ids["Key of Beginnings F08"] = 2663008
    item_ids["Key of Beginnings F09"] = 2663009
    item_ids["Key of Beginnings F10"] = 2663010
    item_ids["Key of Beginnings F11"] = 2663011
    item_ids["Key of Beginnings F12"] = 2663012
    item_ids["Key of Beginnings F13"] = 2663013
    item_ids["Key of Guidance F02"]   = 2663102
    item_ids["Key of Guidance F03"]   = 2663103
    item_ids["Key of Guidance F04"]   = 2663104
    item_ids["Key of Guidance F05"]   = 2663105
    item_ids["Key of Guidance F06"]   = 2663106
    item_ids["Key of Guidance F07"]   = 2663107
    item_ids["Key of Guidance F08"]   = 2663108
    item_ids["Key of Guidance F09"]   = 2663109
    item_ids["Key of Guidance F12"]   = 2663112
    item_ids["Key to Truth F02"]      = 2663202
    item_ids["Key to Truth F03"]      = 2663203
    item_ids["Key to Truth F04"]      = 2663204
    item_ids["Key to Truth F05"]      = 2663205
    item_ids["Key to Truth F06"]      = 2663206
    item_ids["Key to Truth F07"]      = 2663207
    item_ids["Key to Truth F08"]      = 2663208
    item_ids["Key to Truth F09"]      = 2663209
    item_ids["Key to Rewards F01"]    = 2663301
    item_ids["Key to Rewards F02"]    = 2663302
    item_ids["Key to Rewards F03"]    = 2663303
    item_ids["Key to Rewards F04"]    = 2663304
    item_ids["Key to Rewards F05"]    = 2663305
    item_ids["Key to Rewards F06"]    = 2663306
    item_ids["Key to Rewards F07"]    = 2663307
    item_ids["Key to Rewards F08"]    = 2663308
    item_ids["Key to Rewards F09"]    = 2663309
    item_ids["Key to Rewards F11"]    = 2663311
    item_ids["Key to Rewards F12"]    = 2663312
    item_ids["Key to Rewards F13"]    = 2663313
    item_ids["Donald"]                = 2665001
    item_ids["Goofy"]                 = 2665002
    item_ids["Aladdin"]               = 2665003
    item_ids["Ariel"]                 = 2665004
    item_ids["Beast"]                 = 2665005
    item_ids["Peter Pan"]             = 2665006
    item_ids["Jack"]                  = 2665007
    item_ids["Progressive Warp"]      = 2666001
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
    battle_cards["Screwdriver"] = {0x1EF, 0x1F1}
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

location_ids = define_location_ids()
item_ids = define_item_ids()
battle_cards = define_battle_cards()
win_conditions = define_win_conditions()
char_to_hex_map = define_char_to_hex_map()

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
deck_card_pointers_addresses = {0x02039DE0, 0x02039EC0, 0x02039FA0}
world_card_addresses = {0x02039D30, 0x02039D31}
world_card_values = {{0x00,0x02}, {0x08,0x00}, {0x04,0x00}, {0x10,0x00}, {0x01,0x00}, {0x20,0x00}
       ,{0x02,0x00}, {0x40,0x00}, {0x80,0x00}, {0x00,0x04}, {0x00,0x08}, {0x00,0x01}, {0x00,0x10}}
floor_assignment_addresses = {0x02039D36,0x02039D3A,0x02039D3E,0x02039D42,0x02039D46,0x02039D4A,0x02039D4E,0x02039D52,0x02039D56,0x02039D5A,0x02039D5E,0x02039D62,0x02039D66}
floor_progress_addresses = {0x02039D34,0x02039D38,0x02039D3C,0x02039D40,0x02039D44,0x02039D48,0x02039D4C,0x02039D50,0x02039D54,0x02039D58,0x02039D5C,0x02039D60}
floor_doors_addresses = {0x02039D37,0x02039D3B,0x02039D3F,0x02039D43,0x02039D47,0x02039D4B,0x02039D4F,0x02039D53,0x02039D57,0x02039D5B,0x02039D5F,0x02039D63}
floor_assignment_values = {0x0A, 0x04, 0x03, 0x05, 0x01, 0x06, 0x02, 0x07, 0x08, 0x0D, 0x0B, 0x09, 0x0C}

bronze_pack_attack_cards = {"Kingdom Key", "Three Wishes", "Pumpkinhead", "Olympia", "Wishing Star", "Lady Luck"}
bronze_pack_magic_cards = {"Fire", "Blizzard", "Thunder", "Simba", "Genie", "Cloud", "Dumbo"}
bronze_pack_item_cards = {"Potion", "Hi-Potion", "Ether"}

silver_pack_attack_cards = {"Lionheart", "Metal Chocobo", "Spellbinder", "Divine Rose", "Crabclaw"}
silver_pack_magic_cards = {"Cure", "Stop", "Gravity", "Aero", "Bambi", "Mushu", "Tinker Bell"}
silver_pack_item_cards = {"Mega-Potion", "Elixir", "Mega-Ether"}

gold_pack_attack_cards = {"Oathkeeper", "Oblivion", "Diamond Dust", "One-Winged Angel", "Ultima Weapon"}
gold_pack_item_cards = {"Megalixir"}

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
    memory.write_u16_le(deck_cp_cost_address, 0x007B)
    
    memory.write_u16_le(battle_cards_address, 0x1008) --Kingdom Key 8
    set_deck_pointer(1, 0, 0x0000)
    memory.write_u16_le(battle_cards_address + 2, 0x1007) --Kingdom Key 7
    set_deck_pointer(1, 1, 0x0001)
    memory.write_u16_le(battle_cards_address + 4, 0x1006) --Kingdom Key 6
    set_deck_pointer(1, 2, 0x0002)
    memory.write_u16_le(battle_cards_address + 6, 0x1005) --Kingdom Key 5
    set_deck_pointer(1, 3, 0x0003)
    memory.write_u16_le(battle_cards_address + 8, 0x10B9) --Blizzard 5
    set_deck_pointer(1, 4, 0x0004)
    memory.write_u16_le(battle_cards_address + 10, 0x1181) --Potion 5
    set_deck_pointer(1, 5, 0x0005)
    local i = 7
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
    elseif floor_number == 11 then
        return get_stored_gold_cards("Key of Beginnings", floor_number) > 0
    elseif floor_number == 10 then
        return true
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
    if can_complete_floor(12) then
        memory.writebyte(highest_warp_floor_address, (14-1)*2)
        return
    else
        memory.writebyte(highest_warp_floor_address, (12-1)*2)
        return
    end
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
    memory.writebyte(floor_assignment_addresses[13], floor_assignment_values[13])
end

function update_map_cards()
    address = 0x0203A8C0
    while address <= 0x0203A99B do
        memory.writebyte(address, 9)
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

function find_new_keys(old_keys, current_keys, gold_card_type, floor_number)
    local new_keys = {}
    if current_keys > old_keys then
        if floor_number < 10 then
            new_key = gold_card_type .. " F0" .. floor_number
        else
            new_key = gold_card_type .. " F" .. floor_number
        end
        set_current_gold_card_qty(gold_card_type, get_current_gold_card_qty(gold_card_type) - 1, floor_number)
        check_location(new_key)
    end
end

function find_new_battle_cards(old_battle_cards, current_battle_cards)
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
            while i < cnt - old_battle_card_counts[card_value] and (card_value % 0x1000) < 0x01C2 do --don't remove enemy cards
                remove_battle_card(card_value)
                i = i + 1
            end
            check_location(get_battle_card_type(card_value))
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

function check_location(location_name)
    location_id = location_ids[location_name]
    file = io.open(client_communication_path .. "send" .. tostring(location_id), "w")
    io.output(file)
    io.write("")
    io.close(file)
end

function add_gold_card(gold_card_name)
    floor_number = tonumber(string.sub(gold_card_name, -2))
    if string.sub(gold_card_name,1,17) == "Key of Beginnings" then
        set_stored_gold_cards("Key of Beginnings", floor_number, 1)
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
            memory.write_u16_le(battle_cards_address + (2 * offset), v[1]+card_value)
            return
        end
    end
end

function open_card_pack(card_pack)
    if card_pack == "Bronze Card Pack" then
        add_battle_card(bronze_pack_attack_cards[math.random(1, #bronze_pack_attack_cards)])
        add_battle_card(bronze_pack_attack_cards[math.random(1, #bronze_pack_attack_cards)])
        choice = math.random(1,2)
        if choice == 1 then
            add_battle_card(bronze_pack_item_cards[math.random(1, #bronze_pack_item_cards)])
        elseif choice == 2 then
            add_battle_card(bronze_pack_magic_cards[math.random(1, #bronze_pack_magic_cards)])
        end
    end
    if card_pack == "Silver Card Pack" then
        add_battle_card(silver_pack_attack_cards[math.random(1, #silver_pack_attack_cards)])
        add_battle_card(silver_pack_attack_cards[math.random(1, #silver_pack_attack_cards)])
        choice = math.random(1,2)
        if choice == 1 then
            add_battle_card(silver_pack_item_cards[math.random(1, #silver_pack_item_cards)])
        elseif choice == 2 then
            add_battle_card(silver_pack_magic_cards[math.random(1, #silver_pack_magic_cards)])
        end
    end
    if card_pack == "Gold Card Pack" then
        add_battle_card(gold_pack_attack_cards[math.random(1, #gold_pack_attack_cards)])
        add_battle_card(gold_pack_attack_cards[math.random(1, #gold_pack_attack_cards)])
        choice = math.random(1,2)
        if choice == 1 then
            add_battle_card(gold_pack_attack_cards[math.random(1, #gold_pack_attack_cards)])
        elseif choice == 2 then
            add_battle_card(gold_pack_item_cards[math.random(1, #gold_pack_item_cards)])
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
    while i < 13 do
        if get_stored_gold_cards("Key of Beginnings", i) < 1 then
            memory.writebyte(floor_progress_addresses[i], 0x77)
            memory.writebyte(floor_doors_addresses[i], 0x03)
        elseif memory.readbyte(floor_assignment_addresses[i]) == 0x0A and i > 1 then
            memory.writebyte(floor_progress_addresses[i], 0x00)
            memory.writebyte(floor_doors_addresses[i], 0x00)
        end
        i = i + 1
    end
end

function update_post_floor_cutscene_valid()
    i = 1
    while i < 13 do
        if can_complete_floor(i) then
            x = memory.readbyte(floor_progress_addresses[i])
            x = bit.clear(x, 2) --Turns on the post floor cutscene
            x = bit.clear(x, 0) --Turns on the 2nd post floor cutscene
            memory.writebyte(floor_progress_addresses[i],x)
        else
            x = memory.readbyte(floor_progress_addresses[i])
            x = bit.set(x, 2) --Turns off the post floor cutscene
            x = bit.set(x, 0) --Turns off the post floor cutscene
            memory.writebyte(floor_progress_addresses[i],x)
        end
        i = i + 1
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
            last_variables["Last Key of Beginnings"] = get_current_gold_card_qty("Key of Beginnings")
            last_variables["Last Key of Guidance"] = get_current_gold_card_qty("Key of Guidance")
            last_variables["Last Key to Truth"] = get_current_gold_card_qty("Key to Truth")
            last_variables["Last Key to Rewards"] = get_current_gold_card_qty("Key to Rewards")
            last_variables["Last Moogle Points"] = get_moogle_points()
        end
        local current_key_of_beginnings = get_current_gold_card_qty("Key of Beginnings")
        local current_key_of_guidance = get_current_gold_card_qty("Key of Guidance")
        local current_key_to_truth = get_current_gold_card_qty("Key to Truth")
        local current_key_to_rewards = get_current_gold_card_qty("Key to Rewards")
        local new_key_of_beginnings = find_new_keys(last_variables["Last Key of Beginnings"], current_key_of_beginnings, "Key of Beginnings", current_floor)
        find_new_keys(last_variables["Last Key of Guidance"], current_key_of_guidance, "Key of Guidance", current_floor)
        find_new_keys(last_variables["Last Key to Truth"], current_key_to_truth, "Key to Truth", current_floor)
        find_new_keys(last_variables["Last Key to Rewards"], current_key_to_rewards, "Key to Rewards", current_floor)
        local current_battle_cards = get_battle_cards()
        last_deck_pointers = get_deck_pointers()
        find_new_battle_cards(last_variables["Last Battle Cards"], current_battle_cards)
        reassign_deck_pointers(last_deck_pointers)
        set_moogle_points(last_variables["Last Moogle Points"])
    end
    if frame % 300 and current_playtime > 3 then
        last_deck_pointers = get_deck_pointers()
        receive_items()
        reassign_deck_pointers(last_deck_pointers)
        update_current_gold_card_qty(get_floor_number())
        set_key_description_text()
        check_if_victorious()
    end
    last_variables["Last Floor"] = get_floor_number()
    last_variables["Last Key of Beginnings"] = get_current_gold_card_qty("Key of Beginnings")
    last_variables["Last Key of Guidance"] = get_current_gold_card_qty("Key of Guidance")
    last_variables["Last Key to Truth"] = get_current_gold_card_qty("Key to Truth")
    last_variables["Last Key to Rewards"] = get_current_gold_card_qty("Key to Rewards")
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