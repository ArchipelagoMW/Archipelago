LUAGUI_NAME = "recomAP"
LUAGUI_AUTH = "Gicu"
LUAGUI_DESC = "RE: Chain of Memories AP Integration"

if os.getenv('LOCALAPPDATA') ~= nil then
    client_communication_path = os.getenv('LOCALAPPDATA') .. "\\KHRECOM\\"
else
    client_communication_path = os.getenv('HOME') .. "/KHRECOM/"
    ok, err, code = os.rename(client_communication_path, client_communication_path)
    if not ok and code ~= 13 then
        os.execute("mkdir " .. path)
    end
end

function decimalToHex(num)
    if num == 0 then
        return '0'
    end
    local neg = false
    if num < 0 then
        neg = true
        num = num * -1
    end
    local hexstr = "0123456789ABCDEF"
    local result = ""
    while num > 0 do
        local n = math.fmod(num, 16)
        result = string.sub(hexstr, n + 1, n + 1) .. result
        num = math.floor(num / 16)
    end
    if neg then
        result = '-' .. result
    end
    return result
end

function file_exists(name)
   local f=io.open(name,"r")
   if f~=nil then io.close(f) return true else return false end
end

function define_journal_byte_location_ids()
    journal_byte_location_ids = {nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil     --Story
                                ,nil    , nil    , nil    , nil    , nil    , nil                                                                                                        --Empty
                                ,nil    , nil    , nil    , nil    , nil    , nil    , nil                                                                                               --Characters I
                                ,nil    , nil    , nil    , nil    , nil    , nil                                                                                                        --Characters II
                                ,nil    , nil    , nil    , nil    , nil                                                                                                                 --Others
                                ,nil    , nil    , nil    , nil                                                                                                                          --Traverse Town
                                ,nil    , nil    , nil    , nil    , nil    , nil                                                                                                        --Wonderland
                                ,nil    , nil    , nil    , nil                                                                                                                          --Olympus Coliseum
                                ,nil    , nil    , nil    , nil    , nil    , nil                                                                                                        --Agrabah
                                ,nil    , nil    , nil    , nil    , nil    , nil    , nil                                                                                               --Halloween Town
                                ,nil    , nil                                                                                                                                            --Monstro
                                ,nil    , nil    , nil    , nil                                                                                                                          --Atlantica
                                ,nil    , nil    , nil    , nil                                                                                                                          --Neverland
                                ,nil    , nil    , nil    , nil                                                                                                                          --Hollow Bastion
                                ,nil    , nil    , nil    , nil    , nil    , nil    , nil                                                                                               --100 Acre Wood
                                ,nil    , nil    , nil                                                                                                                                   --Destiny Island
                                ,2691424, 2691425, 2691416, 2691420, 2691407, 2691431, 2691415, 2691419, 2691408, 2691402, 2691404, 2691413, 2691405, 2691423, 2691422, 2691421, 2691403 --Heartless 1
                                ,2691428, 2691414, 2691418, 2691401, 2691411, 2691412, 2691430, 2691429, 2691417, 2691427, 2691406, 2691409 ,2671426, 2691410, nil    , nil    , nil     --Heartless 2
                                ,nil                                                                                                                                                     --Heartless 3
                                ,nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil     --Offset E3 - F3
                                ,nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil     --Offset F4 - 104
                                ,nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil     --Offset 105 - 115
                                ,nil    , nil    , nil    , nil    , nil                                                                                                                 --Offset 116 - 11A
                                ,2690001, 2690502, 2690701, 2690601, 2690801, 2690401, 2691004, 2690308, 2690301, 2690107, 2690202, 2690901, 2691201, 2691202, nil    , 2691303, 2691304 --Keyblades 1
                                ,nil    , nil    , nil    , nil    , nil    , nil                                                                                                        --Keyblades 2
                                ,2690101, 2690003, 2690602, 2690004, 2690501, 2690201, 2690702                                                                                           --Magic Cards
                                ,2690103, 2690508, 2691001, 2690406, 2690806, 2690906, 2690307                                                                                           --Summon Cards
                                ,2690002, 2690304, 2691101, 2690505, 2691003, 2691002, 2691208                                                                                           --Item Cards
                                ,nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil                                                                                      --Friend Cards
                                ,nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil     --Enemy Cards 1
                                ,nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , 2690106, 2690306, 2690207, 2690507 --Enemy Cards 2
                                ,2690706, 2690606, 2690404, 2690805, 2690905, 2691207, 2691204, 2690204, nil    , nil    , nil    , nil    , 2691103, nil    , nil    , nil    , 2691303 --Enemy Cards 3
                                ,nil    , nil    , 2691301, 2691203, nil                                                                                                                 --Enemy Cards 4
                                }
    return journal_byte_location_ids
end

function define_room_byte_location_ids()
    room_byte_location_ids = {2690102, 2690104, 2690105
                             ,2690203, 2690205, 2690207
                             ,2690302, 2690303, 2690305
                             ,2690402, 2690403, 2690405
                             ,2690503, 2690504, 2690506
                             ,2690603, 2690604, 2690605
                             ,2690703, 2690704, 2690705
                             ,2690802, 2690803, 2690804
                             ,2690902, 2690903, 2690904
                             ,nil    , nil    , nil    
                             ,2691102, nil    , nil    
                             ,2691205, 2691206, nil    
                             ,2691302, nil    , 123    
                             }
    return room_byte_location_ids
end

function define_card_order()
    card_order = {"Kingdom Key"
                ,"Three Wishes"
                ,"Crabclaw"
                ,"Pumpkinhead"
                ,"Fairy Harp"
                ,"Wishing Star"
                ,"Spellbinder"
                ,"Metal Chocobo"
                ,"Olympia"
                ,"Lionheart"
                ,"Lady Luck"
                ,"Divine Rose"
                ,"Oathkeeper"
                ,"Oblivion"
                ,"Ultima Weapon"
                ,"Diamond Dust"
                ,"One-Winged Angel"
                ,"Soul Eater"
                ,"Star Seeker"
                ,"Total Eclipse"
                ,"Midnight Roar"
                ,"Maverick Flare"
                ,"Two Become One"
                ,"Bond of Flame"
                ,"Premium Kingdom Key"
                ,"Premium Three Wishes"
                ,"Premium Crabclaw"
                ,"Premium Pumpkinhead"
                ,"Premium Fairy Harp"
                ,"Premium Wishing Star"
                ,"Premium Spellbinder"
                ,"Premium Metal Chocobo"
                ,"Premium Olympia"
                ,"Premium Lionheart"
                ,"Premium Lady Luck"
                ,"Premium Divine Rose"
                ,"Premium Oathkeeper"
                ,"Premium Oblivion"
                ,"Premium Ultima Weapon"
                ,"Premium Diamond Dust"
                ,"Premium One-Winged Angel"
                ,"Premium Soul Eater"
                ,"Premium Star Seeker"
                ,"Premium Total Eclipse"
                ,"Premium Midnight Roar"
                ,"Premium Maverick Flare"
                ,"Premium Two Become One"
                ,"Premium Bond of Flame"
                ,"Fire"
                ,"Blizzard"
                ,"Thunder"
                ,"Cure"
                ,"Gravity"
                ,"Stop"
                ,"Aero"
                ,nil
                ,nil
                ,"Simba"
                ,"Genie"
                ,"Bambi"
                ,"Dumbo"
                ,"Tinker Bell"
                ,"Mushu"
                ,"Cloud"
                ,"Premium Fire"
                ,"Premium Blizzard"
                ,"Premium Thunder"
                ,"Premium Cure"
                ,"Premium Gravity"
                ,"Premium Stop"
                ,"Premium Aero"
                ,nil
                ,nil
                ,"Premium Simba"
                ,"Premium Genie"
                ,"Premium Bambi"
                ,"Premium Dumbo"
                ,"Premium Tinker Bell"
                ,"Premium Mushu"
                ,"Premium Cloud"
                ,"Potion"
                ,"Hi-Potion"
                ,"Mega-Potion"
                ,"Ether"
                ,"Mega-Ether"
                ,"Elixir"
                ,"Megalixir"
                ,"Tranquil Darkness"
                ,"Teeming Darkness"
                ,"Feeble Darkness"
                ,"Almighty Darkness"
                ,"Sleeping Darkness"
                ,"Looming Darkness"
                ,"Premium Room"
                ,"White Room"
                ,"Black Room"
                ,"Bottomless Darkness"
                ,"Roulette Room"
                ,"Martial Awakening"
                ,"Sorcerous Awakening"
                ,"Alchemic Awakening"
                ,"Meeting Ground"
                ,"Stagnant Space"
                ,"Strong Initiative"
                ,"Lasting Daze"
                ,"Calm Bounty"
                ,"Guarded Trove"
                ,"False Bounty"
                ,"Moment's Reprieve"
                ,"Mingling Worlds"
                ,"Moogle Room"
                ,"Random Joker"}
    return card_order
end

function define_enemy_card_order()
    enemy_card_order = {
        "Shadow"
        ,"Soldier"
        ,"Large Body"
        ,"Red Nocturne"
        ,"Blue Rhapsody"
        ,"Yellow Opera"
        ,"Green Requiem"
        ,"Powerwild"
        ,"Bouncywild"
        ,"Air Soldier"
        ,"Bandit"
        ,"Fat Bandit"
        ,"Barrel Spider"
        ,"Search Ghost"
        ,"Sea Neon"
        ,"Screwdiver"
        ,"Aquatank"
        ,"Wight Knight"
        ,"Gargoyle"
        ,"Pirate"
        ,"Air Pirate"
        ,"Darkball"
        ,"Defender"
        ,"Wyvern"
        ,"Wizard"
        ,"Neoshadow"
        ,"White Mushroom"
        ,"Black Fungus"
        ,"Creeper Plant"
        ,"Tornado Step"
        ,"Crescendo"
        ,"Guard Armor"
        ,"Parasite Cage"
        ,"Trickmaster"
        ,"Darkside"
        ,"Card Soldier"
        ,"Hades"
        ,"Jafar-Genie"
        ,"Oogie-Boogie"
        ,"Ursula"
        ,"Hook"
        ,"Dragon Maleficent"
        ,"Riku Replica"
        ,"Axel"
        ,"Larxene"
        ,"Vexen"
        ,"Marluxia"
        ,"Lexaeus"
        ,"Ansem"
        ,"Zexion"
        ,"Xemnas"
        ,"Xigbar"
        ,"Xaldin"
        ,"Saix"
        ,"Demyx"
        ,"Luxord"
        ,"Roxas"
        ,"Gold Card"
        ,"Platinum Card"
        }
    return enemy_card_order
end

function define_item_ids()
    item_ids = {}
    item_ids["Bronze Card Pack"]                 = 2681001
    item_ids["Silver Card Pack"]                 = 2681002
    item_ids["Gold Card Pack"]                   = 2681003
    item_ids["Kingdom Key 1-3"]                  = 2681011
    item_ids["Kingdom Key 4-6"]                  = 2681012
    item_ids["Kingdom Key 7-9"]                  = 2681013
    item_ids["Kingdom Key 0"]                    = 2681014
    item_ids["Three Wishes 1-3"]                 = 2681021
    item_ids["Three Wishes 4-6"]                 = 2681022
    item_ids["Three Wishes 7-9"]                 = 2681023
    item_ids["Three Wishes 0"]                   = 2681024
    item_ids["Crabclaw 1-3"]                     = 2681031
    item_ids["Crabclaw 4-6"]                     = 2681032
    item_ids["Crabclaw 7-9"]                     = 2681033
    item_ids["Crabclaw 0"]                       = 2681034
    item_ids["Pumpkinhead 1-3"]                  = 2681041
    item_ids["Pumpkinhead 4-6"]                  = 2681042
    item_ids["Pumpkinhead 7-9"]                  = 2681043
    item_ids["Pumpkinhead 0"]                    = 2681044
    item_ids["Fairy Harp 1-3"]                   = 2681051
    item_ids["Fairy Harp 4-6"]                   = 2681052
    item_ids["Fairy Harp 7-9"]                   = 2681053
    item_ids["Fairy Harp 0"]                     = 2681054
    item_ids["Wishing Star 1-3"]                 = 2681061
    item_ids["Wishing Star 4-6"]                 = 2681062
    item_ids["Wishing Star 7-9"]                 = 2681063
    item_ids["Wishing Star 0"]                   = 2681064
    item_ids["Spellbinder 1-3"]                  = 2681071
    item_ids["Spellbinder 4-6"]                  = 2681072
    item_ids["Spellbinder 7-9"]                  = 2681073
    item_ids["Spellbinder 0"]                    = 2681074
    item_ids["Metal Chocobo 1-3"]                = 2681081
    item_ids["Metal Chocobo 4-6"]                = 2681082
    item_ids["Metal Chocobo 7-9"]                = 2681083
    item_ids["Metal Chocobo 0"]                  = 2681084
    item_ids["Olympia 1-3"]                      = 2681091
    item_ids["Olympia 4-6"]                      = 2681092
    item_ids["Olympia 7-9"]                      = 2681093
    item_ids["Olympia 0"]                        = 2681094
    item_ids["Lionheart 1-3"]                    = 2681101
    item_ids["Lionheart 4-6"]                    = 2681102
    item_ids["Lionheart 7-9"]                    = 2681103
    item_ids["Lionheart 0"]                      = 2681104
    item_ids["Lady Luck 1-3"]                    = 2681111
    item_ids["Lady Luck 4-6"]                    = 2681112
    item_ids["Lady Luck 7-9"]                    = 2681113
    item_ids["Lady Luck 0"]                      = 2681114
    item_ids["Divine Rose 1-3"]                  = 2681121
    item_ids["Divine Rose 4-6"]                  = 2681122
    item_ids["Divine Rose 7-9"]                  = 2681123
    item_ids["Divine Rose 0"]                    = 2681124
    item_ids["Oathkeeper 1-3"]                   = 2681131
    item_ids["Oathkeeper 4-6"]                   = 2681132
    item_ids["Oathkeeper 7-9"]                   = 2681133
    item_ids["Oathkeeper 0"]                     = 2681134
    item_ids["Oblivion 1-3"]                     = 2681141
    item_ids["Oblivion 4-6"]                     = 2681142
    item_ids["Oblivion 7-9"]                     = 2681143
    item_ids["Oblivion 0"]                       = 2681144
    item_ids["Diamond Dust 1-3"]                 = 2681151
    item_ids["Diamond Dust 4-6"]                 = 2681152
    item_ids["Diamond Dust 7-9"]                 = 2681153
    item_ids["Diamond Dust 0"]                   = 2681154
    item_ids["One Winged Angel 1-3"]             = 2681161
    item_ids["One Winged Angel 4-6"]             = 2681162
    item_ids["One Winged Angel 7-9"]             = 2681163
    item_ids["One Winged Angel 0"]               = 2681164
    item_ids["Ultima Weapon 1-3"]                = 2681171
    item_ids["Ultima Weapon 4-6"]                = 2681172
    item_ids["Ultima Weapon 7-9"]                = 2681173
    item_ids["Ultima Weapon 0"]                  = 2681174
    item_ids["Fire 1-3"]                         = 2681181
    item_ids["Fire 4-6"]                         = 2681182
    item_ids["Fire 7-9"]                         = 2681183
    item_ids["Fire 0"]                           = 2681184
    item_ids["Blizzard 1-3"]                     = 2681191
    item_ids["Blizzard 4-6"]                     = 2681192
    item_ids["Blizzard 7-9"]                     = 2681193
    item_ids["Blizzard 0"]                       = 2681194
    item_ids["Thunder 1-3"]                      = 2681201
    item_ids["Thunder 4-6"]                      = 2681202
    item_ids["Thunder 7-9"]                      = 2681203
    item_ids["Thunder 0"]                        = 2681204
    item_ids["Cure 1-3"]                         = 2681211
    item_ids["Cure 4-6"]                         = 2681212
    item_ids["Cure 7-9"]                         = 2681213
    item_ids["Cure 0"]                           = 2681214
    item_ids["Gravity 1-3"]                      = 2681221
    item_ids["Gravity 4-6"]                      = 2681222
    item_ids["Gravity 7-9"]                      = 2681223
    item_ids["Gravity 0"]                        = 2681224
    item_ids["Stop 1-3"]                         = 2681231
    item_ids["Stop 4-6"]                         = 2681232
    item_ids["Stop 7-9"]                         = 2681233
    item_ids["Stop 0"]                           = 2681234
    item_ids["Aero 1-3"]                         = 2681241
    item_ids["Aero 4-6"]                         = 2681242
    item_ids["Aero 7-9"]                         = 2681243
    item_ids["Aero 0"]                           = 2681244
    item_ids["Simba 1-3"]                        = 2681251
    item_ids["Simba 4-6"]                        = 2681252
    item_ids["Simba 7-9"]                        = 2681253
    item_ids["Simba 0"]                          = 2681254
    item_ids["Genie 1-3"]                        = 2681261
    item_ids["Genie 4-6"]                        = 2681262
    item_ids["Genie 7-9"]                        = 2681263
    item_ids["Genie 0"]                          = 2681264
    item_ids["Bambi 1-3"]                        = 2681271
    item_ids["Bambi 4-6"]                        = 2681272
    item_ids["Bambi 7-9"]                        = 2681273
    item_ids["Bambi 0"]                          = 2681274
    item_ids["Dumbo 1-3"]                        = 2681281
    item_ids["Dumbo 4-6"]                        = 2681282
    item_ids["Dumbo 7-9"]                        = 2681283
    item_ids["Dumbo 0"]                          = 2681284
    item_ids["Tinker Bell 1-3"]                  = 2681291
    item_ids["Tinker Bell 4-6"]                  = 2681292
    item_ids["Tinker Bell 7-9"]                  = 2681293
    item_ids["Tinker Bell 0"]                    = 2681294
    item_ids["Mushu 1-3"]                        = 2681301
    item_ids["Mushu 4-6"]                        = 2681302
    item_ids["Mushu 7-9"]                        = 2681303
    item_ids["Mushu 0"]                          = 2681304
    item_ids["Cloud 1-3"]                        = 2681311
    item_ids["Cloud 4-6"]                        = 2681312
    item_ids["Cloud 7-9"]                        = 2681313
    item_ids["Cloud 0"]                          = 2681314
    item_ids["Potion 1-3"]                       = 2681321
    item_ids["Potion 4-6"]                       = 2681322
    item_ids["Potion 7-9"]                       = 2681323
    item_ids["Potion 0"]                         = 2681324
    item_ids["Hi-Potion 1-3"]                    = 2681331
    item_ids["Hi-Potion 4-6"]                    = 2681332
    item_ids["Hi-Potion 7-9"]                    = 2681333
    item_ids["Hi-Potion 0"]                      = 2681334
    item_ids["Mega-Potion 1-3"]                  = 2681341
    item_ids["Mega-Potion 4-6"]                  = 2681342
    item_ids["Mega-Potion 7-9"]                  = 2681343
    item_ids["Mega-Potion 0"]                    = 2681344
    item_ids["Ether 1-3"]                        = 2681351
    item_ids["Ether 4-6"]                        = 2681352
    item_ids["Ether 7-9"]                        = 2681353
    item_ids["Ether 0"]                          = 2681354
    item_ids["Mega-Ether 1-3"]                   = 2681361
    item_ids["Mega-Ether 4-6"]                   = 2681362
    item_ids["Mega-Ether 7-9"]                   = 2681363
    item_ids["Mega-Ether 0"]                     = 2681364
    item_ids["Elixir 1-3"]                       = 2681371
    item_ids["Elixir 4-6"]                       = 2681372
    item_ids["Elixir 7-9"]                       = 2681373
    item_ids["Elixir 0"]                         = 2681374
    item_ids["Megalixir 1-3"]                    = 2681381
    item_ids["Megalixir 4-6"]                    = 2681382
    item_ids["Megalixir 7-9"]                    = 2681383
    item_ids["Megalixir 0"]                      = 2681384
    item_ids["Enemy Card Shadow"]                = 2682001
    item_ids["Enemy Card Soldier"]               = 2682002
    item_ids["Enemy Card Large Body"]            = 2682003
    item_ids["Enemy Card Red Nocturne"]          = 2682004
    item_ids["Enemy Card Blue Rhapsody"]         = 2682005
    item_ids["Enemy Card Yellow Opera"]          = 2682006
    item_ids["Enemy Card Green Requiem"]         = 2682007
    item_ids["Enemy Card Powerwild"]             = 2682008
    item_ids["Enemy Card Bouncywild"]            = 2682009
    item_ids["Enemy Card Air Soldier"]           = 2682010
    item_ids["Enemy Card Bandit"]                = 2682011
    item_ids["Enemy Card Fat Bandit"]            = 2682012
    item_ids["Enemy Card Barrel Spider"]         = 2682013
    item_ids["Enemy Card Search Ghost"]          = 2682014
    item_ids["Enemy Card Sea Neon"]              = 2682015
    item_ids["Enemy Card Screwdiver"]            = 2682016
    item_ids["Enemy Card Aquatank"]              = 2682017
    item_ids["Enemy Card Wight Knight"]          = 2682018
    item_ids["Enemy Card Gargoyle"]              = 2682019
    item_ids["Enemy Card Pirate"]                = 2682020
    item_ids["Enemy Card Air Pirate"]            = 2682021
    item_ids["Enemy Card Darkball"]              = 2682022
    item_ids["Enemy Card Defender"]              = 2682023
    item_ids["Enemy Card Wyvern"]                = 2682024
    item_ids["Enemy Card Neoshadow"]             = 2682025
    item_ids["Enemy Card White Mushroom"]        = 2682026
    item_ids["Enemy Card Black Fungus"]          = 2682027
    item_ids["Enemy Card Creeper Plant"]         = 2682028
    item_ids["Enemy Card Tornado Step"]          = 2682029
    item_ids["Enemy Card Crescendo"]             = 2682030
    item_ids["Enemy Card Guard Armor"]           = 2682031
    item_ids["Enemy Card Parasite Cage"]         = 2682032
    item_ids["Enemy Card Trickmaster"]           = 2682033
    item_ids["Enemy Card Darkside"]              = 2682034
    item_ids["Enemy Card Card Soldier (Red)"]    = 2682035
    item_ids["Enemy Card Card Soldier (Black)"]  = 2682036
    item_ids["Enemy Card Hades"]                 = 2682037
    item_ids["Enemy Card Jafar"]                 = 2682039
    item_ids["Enemy Card Oogie Boogie"]          = 2682040
    item_ids["Enemy Card Ursula"]                = 2682041
    item_ids["Enemy Card Hook"]                  = 2682042
    item_ids["Enemy Card Dragon Maleficent"]     = 2682043
    item_ids["Enemy Card Riku"]                  = 2682044
    item_ids["Enemy Card Larxene"]               = 2682045
    item_ids["Enemy Card Vexen"]                 = 2682046
    item_ids["Enemy Card Marluxia"]              = 2682047
    item_ids["Enemy Card Lexaeus"]               = 2682048
    item_ids["Enemy Card Ansem"]                 = 2682049
    item_ids["Enemy Card Axel"]                  = 2682050
    item_ids["Wonderland"]                       = 2683002
    item_ids["Olympus Coliseum"]                 = 2683003
    item_ids["Monstro"]                          = 2683004
    item_ids["Agrabah"]                          = 2683005
    item_ids["Halloween Town"]                   = 2683006
    item_ids["Atlantica"]                        = 2683007
    item_ids["Neverland"]                        = 2683008
    item_ids["Hollow Bastion"]                   = 2683009
    item_ids["100 Acre Wood"]                    = 2683010
    item_ids["Twilight Town"]                    = 2683011
    item_ids["Destiny Islands"]                  = 2683012
    item_ids["Castle Oblivion"]                  = 2683013
    item_ids["Key to Rewards F01"]               = 2683301
    item_ids["Key to Rewards F02"]               = 2683302
    item_ids["Key to Rewards F03"]               = 2683303
    item_ids["Key to Rewards F04"]               = 2683304
    item_ids["Key to Rewards F05"]               = 2683305
    item_ids["Key to Rewards F06"]               = 2683306
    item_ids["Key to Rewards F07"]               = 2683307
    item_ids["Key to Rewards F08"]               = 2683308
    item_ids["Key to Rewards F09"]               = 2683309
    item_ids["Key to Rewards F11"]               = 2683311
    item_ids["Key to Rewards F12"]               = 2683312
    item_ids["Key to Rewards F13"]               = 2683313
    item_ids["Donald"]                           = 2685001
    item_ids["Goofy"]                            = 2685002
    item_ids["Aladdin"]                          = 2685003
    item_ids["Ariel"]                            = 2685004
    item_ids["Beast"]                            = 2685005
    item_ids["Peter Pan"]                        = 2685006
    item_ids["Jack"]                             = 2685007
    return item_ids
end

journal_byte_location_ids = define_journal_byte_location_ids()
room_byte_location_ids = define_room_byte_location_ids()
card_order = define_card_order()
enemy_card_order = define_enemy_card_order()
item_ids = define_item_ids()

frame_count = 1


function get_journal_array()
    journal_byte_pointer_offset = 0x394DA8
    journal_byte_value_offset = 0x64
    journal_byte_pointer = GetPointer(journal_byte_pointer_offset, journal_byte_value_offset)
    return ReadArray(journal_byte_pointer, #journal_byte_location_ids, true)
end

function get_checked_journal_location_ids(journal_array)
    checked_journal_location_ids = {}
    for k,v in pairs(journal_array) do
        if v > 0 then
            checked_journal_location_ids[#checked_journal_location_ids+1]=journal_byte_location_ids[k]
        end
    end
    return checked_journal_location_ids
end

function get_room_array()
    room_byte_pointer_offset = 0x394D38
    room_byte_value_offset = 0x18
    room_byte_pointer = GetPointer(room_byte_pointer_offset, room_byte_value_offset)
    return ReadArray(room_byte_pointer, #room_byte_location_ids, true)
end

function get_checked_room_location_ids(room_array)
    checked_room_location_ids = {}
    for k,v in pairs(room_array) do
        if v > 0 then
            checked_room_location_ids[#checked_room_location_ids+1]=room_byte_location_ids[k]
        end
    end
    return checked_room_location_ids
end

function get_current_floor()
    return ReadByte(0x3939E4)
end

function get_time_played()
    time_played_pointer_offset = 0x393280
    time_played_offset_1 = 0x8
    time_played_offset_2 = 0x300
    time_played_pointer_1 = GetPointer(time_played_pointer_offset, time_played_offset_1)
    time_played_pointer_2 = GetPointer(time_played_pointer_1, time_played_offset_2, true)
    time_played = ReadInt(time_played_pointer_2, true)
    return time_played
end

function get_empty_card_array()
    card_array = {}
    i = 1
    while i <= #card_order * 10 do
        card_array[i] = 0
        i = i + 1
    end
    return card_array
end

function get_empty_enemy_card_array()
    enemy_cards_array = {}
    i = 1
    while i <= #enemy_card_order do
        enemy_cards_array[i] = 0
        i = i + 1
    end
    return enemy_cards_array
end

function get_empty_world_assignment_array()
    world_assignment_array = {1,1,1,1,1,1,1,1,1,1,1,1,1}
    return world_assignment_array
end

function get_empty_friends_array()
    friends_array = {0,0,0,0,0,0,0}
    return friends_array
end

function get_empty_gold_map_cards_array()
    gold_map_cards_array = {0,0,0,0}
    return gold_map_cards_array
end

function get_empty_cutscene_array()
    return {0x01, 0x00, 0x02, 0x00, 0x03, 0x00, 0x04, 0x00, 0x05, 0x00, 0x06, 0x00, 0x07, 0x00, 0x08, 0x00, 0x09, 0x00, 0x0A, 0x00, 0x0B, 0x00, 0x0C, 0x00, 0x0D, 0x00, 0x0E, 0x00, 0x0F, 
            0x00, 0x10, 0x00, 0x11, 0x00, 0x12, 0x00, 0x13, 0x00, 0x14, 0x00, 0x15, 0x00, 0x16, 0x00, 0x17, 0x00, 0x18, 0x00}
end

function set_gold_map_cards(gold_map_cards_array)
    gold_map_cards_pointer_offset = 0x392990
    gold_map_cards_value_offset = 0x2
    gold_map_cards_pointer = GetPointer(gold_map_cards_pointer_offset, gold_map_cards_value_offset)
    WriteArray(gold_map_cards_pointer, gold_map_cards_array, true)
end

function set_cards(card_array)
    cards_pointer_offset = 0x394D98
    card_value_offset = -0xD74
    cards_pointer = GetPointer(cards_pointer_offset, card_value_offset)
    WriteArray(cards_pointer, card_array, true)
end

function set_enemy_cards(enemy_card_array)
    enemy_cards_pointer_offset = 0x394D98
    enemy_cards_value_offset = -0x914
    enemy_cards_pointer = GetPointer(enemy_cards_pointer_offset, enemy_cards_value_offset)
    WriteArray(enemy_cards_pointer, enemy_card_array, true)
end

function set_friends(friends_array)
    friend_byte_pointer_offset = 0x394DA8
    friend_byte_value_offset = 0x147
    friend_byte_pointer = GetPointer(friend_byte_pointer_offset, friend_byte_value_offset)
    WriteArray(friend_byte_pointer, friends_array, true)
end

function set_world_assignment(world_assignment_array)
    world_assignment_pointer_offset = 0x394D38
    world_assignment_value_offset = 0x48
    world_assignment_pointer = GetPointer(world_assignment_pointer_offset, world_assignment_value_offset)
    WriteArray(world_assignment_pointer, world_assignment_array, true)
end

function set_initial_map_cards(card_array)
    map_card_names = {"Tranquil Darkness"
                ,"Teeming Darkness"
                ,"Feeble Darkness"
                ,"Almighty Darkness"
                ,"Sleeping Darkness"
                ,"Looming Darkness"
                ,"Premium Room"
                ,"White Room"
                ,"Black Room"
                ,"Bottomless Darkness"
                ,"Roulette Room"
                ,"Martial Awakening"
                ,"Sorcerous Awakening"
                ,"Alchemic Awakening"
                ,"Meeting Ground"
                ,"Stagnant Space"
                ,"Strong Initiative"
                ,"Lasting Daze"
                ,"Calm Bounty"
                ,"Guarded Trove"
                ,"False Bounty"
                ,"Moment's Reprieve"
                ,"Mingling Worlds"
                ,"Random Joker"}
    for k,v in pairs(map_card_names) do
        i = 0
        while i < 10 do
            card_array = add_card(card_array, v, i)
            i = i + 1
        end
    end
    return card_array
end

function set_initial_battle_cards(card_array)
    card_array = add_card(card_array, "Kingdom Key", 8)
    card_array = add_card(card_array, "Kingdom Key", 7)
    card_array = add_card(card_array, "Kingdom Key", 6)
    return card_array
end

function send_checks(friends_array)
    location_ids = get_checked_journal_location_ids(get_journal_array())
    for k,v in pairs(location_ids) do
        if not file_exists(client_communication_path .. "send" .. tostring(v)) then
            file = io.open(client_communication_path .. "send" .. tostring(v), "w")
            io.output(file)
            io.write("")
            io.close(file)
        end
    end
    location_ids = get_checked_room_location_ids(get_room_array())
    for k,v in pairs(location_ids) do
        if not file_exists(client_communication_path .. "send" .. tostring(v)) then
            file = io.open(client_communication_path .. "send" .. tostring(v), "w")
            io.output(file)
            io.write("")
            io.close(file)
        end
    end
    friends = 0
    for k,v in pairs(friends_array) do
        friends = friends + v
    end
    if friends == 7 then
        if not file_exists(client_communication_path .. "victory") then
            file = io.open(client_communication_path .. "victory", "w")
            io.output(file)
            io.write("")
            io.close(file)
        end
    end
end

function set_cutscene_array(cutscene_array)
    cutscene_array_pointer_offset = 0x394D70
    cutscene_array_value_offset = 0x272
    cutscene_array_pointer = GetPointer(cutscene_array_pointer_offset, cutscene_array_value_offset)
    WriteArray(cutscene_array_pointer, cutscene_array, true)
end

function receive_items()
    card_array = get_empty_card_array()
    enemy_card_array = get_empty_enemy_card_array()
    world_assignment_array = get_empty_world_assignment_array()
    gold_map_cards_array = get_empty_gold_map_cards_array()
    friends_array = get_empty_friends_array()
    current_floor = get_current_floor()
    progressive_bosses = 0
    local i = 1
    card_array = set_initial_battle_cards(card_array)
    card_array = set_initial_map_cards(card_array)
    while file_exists(client_communication_path .. "AP_" .. tostring(i) .. ".item") do
        file = io.open(client_communication_path .. "AP_" .. tostring(i) .. ".item", "r")
        io.input(file)
        received_item_id = tonumber(io.read())
        io.close(file)
        for k,v in pairs(item_ids) do
            if received_item_id == v then
                received_item_name = k
                if string.sub(received_item_name, 1, 10) == "Enemy Card" and not item_found then
                    enemy_card_array = add_enemy_card(enemy_card_array, received_item_name:sub(12))
                elseif string.sub(received_item_name, -3) == "1-3" and not item_found then
                    card_array = add_card(card_array, received_item_name:sub(1, -5), 1)
                    card_array = add_card(card_array, received_item_name:sub(1, -5), 2)
                    card_array = add_card(card_array, received_item_name:sub(1, -5), 3)
                elseif string.sub(received_item_name, -3) == "4-6" and not item_found then
                    card_array = add_card(card_array, received_item_name:sub(1, -5), 4)
                    card_array = add_card(card_array, received_item_name:sub(1, -5), 5)
                    card_array = add_card(card_array, received_item_name:sub(1, -5), 6)
                elseif string.sub(received_item_name, -3) == "7-9" and not item_found then
                    card_array = add_card(card_array, received_item_name:sub(1, -5), 7)
                    card_array = add_card(card_array, received_item_name:sub(1, -5), 8)
                    card_array = add_card(card_array, received_item_name:sub(1, -5), 9)
                elseif string.sub(received_item_name, -1) == "0" and not item_found then
                    card_array = add_card(card_array, received_item_name:sub(1, -3), 0)
                elseif received_item_name == "Wonderland" then
                    world_assignment_array[2] = 0x4
                elseif received_item_name == "Olympus Coliseum" then
                    world_assignment_array[3] = 0x3
                elseif received_item_name == "Monstro" then
                    world_assignment_array[4] = 0x5
                elseif received_item_name == "Agrabah" then
                    world_assignment_array[5] = 0x2
                elseif received_item_name == "Halloween Town" then
                    world_assignment_array[6] = 0x6
                elseif received_item_name == "Atlantica" then
                    world_assignment_array[7] = 0x7
                elseif received_item_name == "Neverland" then
                    world_assignment_array[8] = 0x8
                elseif received_item_name == "Hollow Bastion" then
                    world_assignment_array[9] = 0x9
                elseif received_item_name == "100 Acre Wood" then
                    world_assignment_array[10] = 0xA
                elseif received_item_name == "Twilight Town" then
                    world_assignment_array[11] = 0xB
                elseif received_item_name == "Destiny Islands" then
                    world_assignment_array[12] = 0xC
                elseif received_item_name == "Castle Oblivion" then
                    world_assignment_array[13] = 0xD
                elseif received_item_name == "Donald" then
                    friends_array[1] = 1
                elseif received_item_name == "Goofy" then
                    friends_array[2] = 1
                elseif received_item_name == "Aladdin" then
                    friends_array[3] = 1
                elseif received_item_name == "Ariel" then
                    friends_array[4] = 1
                elseif received_item_name == "Jack" then
                    friends_array[5] = 1
                elseif received_item_name == "Peter Pan" then
                    friends_array[6] = 1
                elseif received_item_name == "Beast" then
                    friends_array[7] = 1
                elseif string.sub(received_item_name, 1, 14)  == "Key to Rewards" and current_floor == tonumber(string.sub(received_item_name, -2)) then
                    gold_map_cards_array[4] = 1
                end
            end
        end
        i = i + 1
    end
    if current_floor > 1 and world_assignment_array[current_floor] ~= 1 or current_floor == 1 then
        gold_map_cards_array[1] = 1
        gold_map_cards_array[2] = 1
        gold_map_cards_array[3] = 1
    end
    set_cards(card_array)
    set_enemy_cards(enemy_card_array)
    set_world_assignment(world_assignment_array)
    set_friends(friends_array)
    set_gold_map_cards(gold_map_cards_array)
    set_cutscene_array(calculate_cutscene_array())
    return friends_array
end

function add_card(card_array, card_name, card_value)
    for k,v in pairs(card_order) do
        if v == card_name then
            card_array[((k-1)*10)+(card_value+1)] = 1
        end
    end
    return card_array
end

function add_enemy_card(enemy_card_array, card_name)
    for k,v in pairs(enemy_card_order) do
        if v == card_name then
            enemy_card_array[k] = 1
        end
    end
    return enemy_card_array
end

function calculate_cutscene_array()
    journal_byte_pointer_offset = 0x394DA8
    journal_byte_value_offset_axel    = 0x132
    journal_byte_value_offset_larxene = 0x134
    journal_byte_value_offset_riku    = 0x138
    journal_byte_value_offset_vexen   = 0x144
    
    
    journal_byte_pointer = GetPointer(journal_byte_pointer_offset, 0x0)
    axel_byte    = ReadByte(journal_byte_pointer+journal_byte_value_offset_axel   ,true)
    larxene_byte = ReadByte(journal_byte_pointer+journal_byte_value_offset_larxene,true)
    riku_byte    = ReadByte(journal_byte_pointer+journal_byte_value_offset_riku   ,true)
    
    if larxene_byte == 1 and riku_byte == 1 and axel_byte == 1 then
        return {0x01, 0x00, 0x02, 0x00, 0x03, 0x00, 0x04, 0x00, 0x05, 0x00, 0x06, 0x00, 0x07, 0x00, 0x08, 0x00, 0x09, 0x00, 0x0A, 0x00, 0x0B, 0x00, 0x0C, 0x00, 0x0D, 0x00, 0x0E, 0x00, 0x0F, 
                0x00, 0x10, 0x00, 0x11, 0x00, 0x12, 0x00, 0x13, 0x00, 0x14, 0x00, 0x15, 0x00, 0x16, 0x00, 0x17, 0x00, 0xE8, 0x07}
    elseif larxene_byte == 1 and axel_byte == 1 then
        return {0x01, 0x00, 0x02, 0x00, 0x03, 0x00, 0x04, 0x00, 0x05, 0x00, 0x06, 0x00, 0x07, 0x00, 0x08, 0x00, 0x09, 0x00, 0x0A, 0x00, 0x0B, 0x00, 0x0C, 0x00, 0x0D, 0x00, 0xDE, 0x07, 0x0F, 
                0x00, 0x10, 0x00, 0x11, 0x00, 0x12, 0x00, 0x13, 0x00, 0x14, 0x00, 0x15, 0x00, 0x16, 0x00, 0x17, 0x00, 0x18, 0x00}
    elseif axel_byte == 1 then
        return {0x01, 0x00, 0x02, 0x00, 0x03, 0x00, 0x04, 0x00, 0x05, 0x00, 0x06, 0x00, 0x07, 0x00, 0x08, 0x00, 0x09, 0x00, 0x0A, 0x00, 0x0B, 0x00, 0xDC, 0x07, 0x0D, 0x00, 0x0E, 0x00, 0x0F, 
                0x00, 0x10, 0x00, 0x11, 0x00, 0x12, 0x00, 0x13, 0x00, 0x14, 0x00, 0x15, 0x00, 0x16, 0x00, 0x17, 0x00, 0x18, 0x00}
    else
        return {0x01, 0x00, 0xD2, 0x07, 0x03, 0x00, 0x04, 0x00, 0x05, 0x00, 0x06, 0x00, 0x07, 0x00, 0x08, 0x00, 0x09, 0x00, 0x0A, 0x00, 0x0B, 0x00, 0x0C, 0x00, 0x0D, 0x00, 0x0E, 0x00, 0x0F, 
                0x00, 0x10, 0x00, 0x11, 0x00, 0x12, 0x00, 0x13, 0x00, 0x14, 0x00, 0x15, 0x00, 0x16, 0x00, 0x17, 0x00, 0x18, 0x00}
    end
    
end

function has_key_of_rewards()
    floor_num = get_current_floor()
    if floor_num < 10 then
        item_id = item_ids["Key to Rewards F0" .. tostring(floor_num)]
    else
        item_id = item_ids["Key to Rewards F" .. tostring(floor_num)]
    end
    i = 0
    while file_exists(client_communication_path .. "AP_" .. tostring(i) .. ".item") do
        file = io.open(client_communication_path .. "AP_" .. tostring(i) .. ".item", "r")
        io.input(file)
        received_item_id = tonumber(io.read())
        io.close(file)
        if received_item_id == item_id then
            return true
        end
    end
    return false
end

function _OnInit()
    ConsolePrint("KHRECOM AP Running...")
end

function _OnFrame()
    if frame_count % 120 == 0 then
        friends_array = receive_items()
        send_checks(friends_array)
    end
    frame_count = frame_count + 1
end