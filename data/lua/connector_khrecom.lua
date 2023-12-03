LUAGUI_NAME = "recomAP"
LUAGUI_AUTH = "Gicu"
LUAGUI_DESC = "RE: Chain of Memories AP Integration"

if os.getenv('LOCALAPPDATA') ~= nil then
    client_communication_path = os.getenv('LOCALAPPDATA') .. "\\KHCOM\\"
else
    client_communication_path = os.getenv('HOME') .. "/KHCOM/"
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
    journal_byte_location_ids = {2670107, 2670608, 2670907, 2671208, 2670108, 2670209, 2670306, 2670509, 2670607, 2670404, 2670706, 2670806, 2670906, 2671013, 2671102, 2671207, 2671302 --Story
                                ,nil    , nil    , nil    , nil    , nil    , nil                                                                                                        --Empty
                                ,2670007, 2670002, 2670003, 2670004, nil    , 2670006, 2670005                                                                                           --Characters I
                                ,2671206, 2671205, 2671010, 2670102, 2671301, nil                                                                                                        --Characters II
                                ,2670109, 2670406, 2671001, 2670908, nil                                                                                                                 --Others
                                ,2670104, 2670105, 2670101, 2670103                                                                                                                      --Traverse Town
                                ,2670203, 2670207, 2670208, 2670204, 2670205, 2670206                                                                                                    --Wonderland
                                ,2670305, 2670304, 2670303, 2670302                                                                                                                      --Olympus Coliseum
                                ,2670503, 2670504, 2670508, 2670505, 2670506, 2670507                                                                                                    --Agrabah
                                ,nil    , nil    , nil    , 2670603, 2670605, 2670602, 2670604                                                                                           --Halloween Town
                                ,2670403, 2670402                                                                                                                                        --Monstro
                                ,2670702, 2670705, 2670703, 2670704                                                                                                                      --Atlantica
                                ,2670803, 2670804, 2670805, 2670802                                                                                                                      --Neverland
                                ,2670905, 2670902, 2670904, 2670903                                                                                                                      --Hollow Bastion
                                ,2671011, 2671006, 2671005, 2671008, 2671004, 2671009, 2671007                                                                                           --100 Acre Wood
                                ,2671203, 2671204, 2671202                                                                                                                               --Destiny Island
                                ,2671424, 2671425, 2671416, 2671420, 2671407, 2671431, 2671415, 2671419, 2671408, 2671402, 2671404, 2671413, 2671405, 2671423, 2671422, 2671421, 2671403 --Heartless 1
                                ,2671428, 2671414, 2671418, 2671401, 2671411, 2671412, 2671430, 2671429, 2671417, 2671427, 2671406, 2671409 ,2671426, 2671410, 2670112, 2670405, 2670210 --Heartless 2
                                ,2671209                                                                                                                                                 --Heartless 2
                                ,nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil     --Offset E3 - F3
                                ,nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil     --Offset F4 - 104
                                ,nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil    , nil     --Offset 105 - 115
                                ,nil    , nil    , nil    , nil    , nil                                                                                                                 --Offset 116 - 11A
                                ,2670001, 2670502, 2670701, 2670601, 2670801, 2670401, 2671003, 2670308, 2670301, 2670111, 2670202, 2670901, 2671201, nil    , nil    , 2671303, 2671304 --Keyblades 1
                                ,nil    , nil    , nil    , nil    , nil    , nil                                                                                                        --Keyblades 2
                                ,2670106, 2670009, 2670606, 2670010, 2670501, 2670201, 2670707                                                                                           --Magic Cards
                                ,2670110, 2670511, 2671002, 2670407, 2670807, 2670909, 2670309                                                                                           --Summon Cards
                                ,2670008, 2670307, 2671101, 2670510, 2671012, 2671014, 2671211}                                                                                          --Item Cards
    return journal_byte_location_ids
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

function define_location_lookup()
    location_lookup = {}
        location_lookup["Starting Checks (Attack Cards Kingdom Key)"] =                        2670001
        location_lookup["Starting Checks (Characters I Donald)"] =                             2670002
        location_lookup["Starting Checks (Characters I Goofy)"] =                              2670003
        location_lookup["Starting Checks (Characters I Jiminy Cricket)"] =                     2670004
        location_lookup["Starting Checks (Characters I Kairi)"] =                              2670005
        location_lookup["Starting Checks (Characters I Riku)"] =                               2670006
        location_lookup["Starting Checks (Characters I Sora)"] =                               2670007
        location_lookup["Starting Checks (Item Cards Potion)"] =                               2670008
        location_lookup["Starting Checks (Magic Cards Blizzard)"] =                            2670009
        location_lookup["Starting Checks (Magic Cards Cure)"] =                                2670010
        location_lookup["F01 Traverse Town Post Floor (Characters I Aerith)"] =                2670101
        location_lookup["F01 Traverse Town Post Floor (Characters I Axel)"] =                  2670102
        location_lookup["F01 Traverse Town Post Floor (Characters I Cid)"] =                   2670103
        location_lookup["F01 Traverse Town Post Floor (Characters I Leon)"] =                  2670104
        location_lookup["F01 Traverse Town Post Floor (Characters I Yuffie)"] =                2670105
        location_lookup["F01 Traverse Town Post Floor (Magic Cards Fire)"] =                   2670106
        location_lookup["F01 Traverse Town Post Floor (Story Sora's Tale I)"] =                2670107
        location_lookup["F01 Traverse Town Post Floor (Story Traverse Town)"] =                2670108
        location_lookup["F01 Traverse Town Room of Beginnings (Characters I Simba)"] =         2670109
        location_lookup["F01 Traverse Town Room of Beginnings (Magic Cards Simba)"] =          2670110
        location_lookup["F01 Traverse Town Room of Rewards (Attack Cards Lionheart)"] =        2670111
        location_lookup["F01 Traverse Town Room of Truth (The Heartless Guard Armor)"] =       2670112
        location_lookup["F02 Wonderland Bounty (Magic Cards Stop)"] =                          2670201
        location_lookup["F02 Wonderland Field (Attack Cards Lady Luck)"] =                     2670202
        location_lookup["F02 Wonderland Post Floor (Characters II Alice)"] =                   2670203
        location_lookup["F02 Wonderland Post Floor (Characters II Card of Hearts)"] =          2670204
        location_lookup["F02 Wonderland Post Floor (Characters II Card of Spades)"] =          2670205
        location_lookup["F02 Wonderland Post Floor (Characters II The Cheshire Cat)"] =        2670206
        location_lookup["F02 Wonderland Post Floor (Characters II The Queen of Hearts)"] =     2670207
        location_lookup["F02 Wonderland Post Floor (Characters II The White Rabbit)"] =        2670208
        location_lookup["F02 Wonderland Post Floor (Story Wonderland)"] =                      2670209
        location_lookup["F02 Wonderland Room of Truth (The Heartless Trickmaster)"] =          2670210
        location_lookup["F03 Olympus Coliseum Field (Attack Cards Olympia)"] =                 2670301
        location_lookup["F03 Olympus Coliseum Post Floor (Characters I Cloud)"] =              2670302
        location_lookup["F03 Olympus Coliseum Post Floor (Characters II Hades)"] =             2670303
        location_lookup["F03 Olympus Coliseum Post Floor (Characters II Philoctetes)"] =       2670304
        location_lookup["F03 Olympus Coliseum Post Floor (Characters II Hercules)"] =          2670305
        location_lookup["F03 Olympus Coliseum Post Floor (Story Olympus Coliseum)"] =          2670306
        location_lookup["F03 Olympus Coliseum Room of Guidance (Item Cards Hi-Potion)"] =      2670307
        location_lookup["F03 Olympus Coliseum Room of Rewards (Attack Card Metal Chocobo)"] =  2670308
        location_lookup["F03 Olympus Coliseum Room of Truth (Magic Cards Cloud)"] =            2670309
        location_lookup["F04 Monstro Field (Wishing Star)"] =                                  2670401
        location_lookup["F04 Monstro Post Floor (Characters II Geppetto)"] =                   2670402
        location_lookup["F04 Monstro Post Floor (Characters II Pinocchio)"] =                  2670403
        location_lookup["F04 Monstro Post Floor (Story Monstro)"] =                            2670404
        location_lookup["F04 Monstro Room of Guidance (The Heartless Parasite Cage)"] =        2670405
        location_lookup["F04 Monstro Room of Truth (Characters I Dumbo)"] =                    2670406
        location_lookup["F04 Monstro Room of Truth (Magic Cards Dumbo)"] =                     2670407
        location_lookup["F05 Agrabah Bounty (Magic Cards Gravity)"] =                          2670501
        location_lookup["F05 Agrabah Field (Attack Cards Three Wishes)"] =                     2670502
        location_lookup["F05 Agrabah Post Floor (Characters II Aladdin)"] =                    2670503
        location_lookup["F05 Agrabah Post Floor (Characters II Genie)"] =                      2670504
        location_lookup["F05 Agrabah Post Floor (Characters II Iago)"] =                       2670505
        location_lookup["F05 Agrabah Post Floor (Characters II Jafar)"] =                      2670506
        location_lookup["F05 Agrabah Post Floor (Characters II Jafar-Genie)"] =                2670507
        location_lookup["F05 Agrabah Post Floor (Characters II Jasmine)"] =                    2670508
        location_lookup["F05 Agrabah Post Floor (Story Agrabah)"] =                            2670509
        location_lookup["F05 Agrabah Room of Guidance (Item Cards Ether)"] =                   2670510
        location_lookup["F05 Agrabah Room of Truth (Magic Cards Genie)"] =                     2670511
        location_lookup["F06 Halloween Town Field (Attack Cards Pumpkinhead)"] =               2670601
        location_lookup["F06 Halloween Town Post Floor (Characters II Dr. Finkelstein)"] =     2670602
        location_lookup["F06 Halloween Town Post Floor (Characters II Jack)"] =                2670603
        location_lookup["F06 Halloween Town Post Floor (Characters II Oogie Boogie)"] =        2670604
        location_lookup["F06 Halloween Town Post Floor (Characters II Sally)"] =               2670605
        location_lookup["F06 Halloween Town Post Floor (Magic Cards Thunder)"] =               2670606
        location_lookup["F06 Halloween Town Post Floor (Story Halloween Town)"] =              2670607
        location_lookup["F06 Halloween Town Post Floor (Story Sora's Tale II)"] =              2670608
        location_lookup["F07 Atlantica Field (Crabclaw)"] =                                    2670701
        location_lookup["F07 Atlantica Post Floor (Characters II Ariel)"] =                    2670702
        location_lookup["F07 Atlantica Post Floor (Characters II Flounder)"] =                 2670703
        location_lookup["F07 Atlantica Post Floor (Characters II Ursula)"] =                   2670704
        location_lookup["F07 Atlantica Post Floor (Characters II Sebastion)"] =                2670705
        location_lookup["F07 Atlantica Post Floor (Story Atlantica)"] =                        2670706
        location_lookup["F07 Atlantica Post Floor (Magic Cards Aero)"] =                       2670707
        location_lookup["F08 Neverland Field (Attack Cards Fairy Harp)"] =                     2670801
        location_lookup["F08 Neverland Post Floor (Characters II Hook)"] =                     2670802
        location_lookup["F08 Neverland Post Floor (Characters II Peter Pan)"] =                2670803
        location_lookup["F08 Neverland Post Floor (Characters II Tinker Bell)"] =              2670804
        location_lookup["F08 Neverland Post Floor (Characters II Wendy)"] =                    2670805
        location_lookup["F08 Neverland Post Floor (Story Neverland)"] =                        2670806
        location_lookup["F08 Neverland Room of Truth (Magic Cards Tinker Bell)"] =             2670807
        location_lookup["F09 Hollow Bastion Field (Attack Cards Divine Rose)"] =               2670901
        location_lookup["F09 Hollow Bastion Post Floor (Characters II Belle)"] =               2670902
        location_lookup["F09 Hollow Bastion Post Floor (Characters II Dragon Maleficent)"] =   2670903
        location_lookup["F09 Hollow Bastion Post Floor (Characters II Maleficent)"] =          2670904
        location_lookup["F09 Hollow Bastion Post Floor (Characters II The Beast)"] =           2670905
        location_lookup["F09 Hollow Bastion Post Floor (Story Hollow Bastion)"] =              2670906
        location_lookup["F09 Hollow Bastion Post Floor (Story Sora's Tale III)"] =             2670907
        location_lookup["F09 Hollow Bastion Room of Rewards (Characters I Mushu)"] =           2670908
        location_lookup["F09 Hollow Bastion Room of Rewards (Magic Cards Mushu)"] =            2670909
        location_lookup["F10 100 Acre Wood Complete (Characters I Bambi)"] =                   2671001
        location_lookup["F10 100 Acre Wood Complete (Magic Cards Bambi)"] =                    2671002
        location_lookup["F10 100 Acre Wood Field Scene Owl (Attack Cards Spellbinder)"] =      2671003
        location_lookup["F10 100 Acre Wood Field Scene Eeyore (Characters II Eeyore)"] =       2671004
        location_lookup["F10 100 Acre Wood Field Scene Owl (Characters II Owl)"] =             2671005
        location_lookup["F10 100 Acre Wood Field Scene Piglet (Characters II Piglet)"] =       2671006
        location_lookup["F10 100 Acre Wood Field Scene Rabbit (Characters II Rabbit)"] =       2671007
        location_lookup["F10 100 Acre Wood Field Scene Roo (Characters II Roo)"] =             2671008
        location_lookup["F10 100 Acre Wood Field Scene Tigger (Characters II Tigger)"] =       2671009
        location_lookup["F10 100 Acre Wood Post Floor (Characters II Vexen)"] =                2671010
        location_lookup["F10 100 Acre Wood Post Floor (Characters II Winnie the Pooh)"] =      2671011
        location_lookup["F10 100 Acre Wood Post Floor (Item Cards Mega-Ether)"] =              2671012
        location_lookup["F10 100 Acre Wood Post Floor (Story 100 Acre Wood)"] =                2671013
        location_lookup["F10 100 Acre Wood Field Scene Roo (Item Cards Elixir)"] =             2671014
        location_lookup["F11 Twilight Town Post Floor (Item Cards Mega-Potion)"] =             2671101
        location_lookup["F11 Twilight Town Post Floor (Story Twilight Town)"] =                2671102
        location_lookup["F12 Destiny Islands Post Floor (Attack Cards Oathkeeper)"] =          2671201
        location_lookup["F12 Destiny Islands Post Floor (Characters I Selphie)"] =             2671202
        location_lookup["F12 Destiny Islands Post Floor (Characters I Tidus)"] =               2671203
        location_lookup["F12 Destiny Islands Post Floor (Characters I Wakka)"] =               2671204
        location_lookup["F12 Destiny Islands Post Floor (Characters I Riku Replica)"] =        2671205
        location_lookup["F12 Destiny Islands Post Floor (Characters I Namine)"] =              2671206
        location_lookup["F12 Destiny Islands Post Floor (Story Destiny Islands)"] =            2671207
        location_lookup["F12 Destiny Islands Post Floor (Story Sora's Tale IV)"] =             2671208
        location_lookup["F12 Destiny Islands Room of Truth (The Heartless Darkside)"] =        2671209
        location_lookup["F12 Destiny Islands Post Floor (Attack Cards Oblivion)"] =            2671210
        location_lookup["F12 Destiny Islands Room of Rewards (Item Cards Megalixir)"] =        2671211
        location_lookup["F13 Castle Oblivion Event (Characters I Marluxia)"] =                 2671301
        location_lookup["F13 Castle Oblivion Post Floor (Story Castle Oblivion)"] =            2671302
        location_lookup["F13 Castle Oblivion Post Marluxia (Attack Cards Diamond Dust)"] =     2671303
        location_lookup["F13 Castle Oblivion Post Marluxia (Attack Cards One-Winged Angel)"] = 2671304
        location_lookup["Heartless Air Pirate"] =                                              2671401
        location_lookup["Heartless Air Soldier"] =                                             2671402
        location_lookup["Heartless Aquatank"] =                                                2671403
        location_lookup["Heartless Bandit"] =                                                  2671404
        location_lookup["Heartless Barrel Spider"] =                                           2671405
        location_lookup["Heartless Black Fungus"] =                                            2671406
        location_lookup["Heartless Blue Rhapsody"] =                                           2671407
        location_lookup["Heartless Bouncywild"] =                                              2671408
        location_lookup["Heartless Creeper Plant"] =                                           2671409
        location_lookup["Heartless Crescendo"] =                                               2671410
        location_lookup["Heartless Darkball"] =                                                2671411
        location_lookup["Heartless Defender"] =                                                2671412
        location_lookup["Heartless Fat Bandit"] =                                              2671413
        location_lookup["Heartless Gargoyle"] =                                                2671414
        location_lookup["Heartless Green Requiem"] =                                           2671415
        location_lookup["Heartless Large Body"] =                                              2671416
        location_lookup["Heartless Neoshadow"] =                                               2671417
        location_lookup["Heartless Pirate"] =                                                  2671418
        location_lookup["Heartless Powerwild"] =                                               2671419
        location_lookup["Heartless Red Nocturne"] =                                            2671420
        location_lookup["Heartless Screwdiver"] =                                              2671421
        location_lookup["Heartless Sea Neon"] =                                                2671422
        location_lookup["Heartless Search Ghost"] =                                            2671423
        location_lookup["Heartless Shadow"] =                                                  2671424
        location_lookup["Heartless Soldier"] =                                                 2671425
        location_lookup["Heartless Tornado Step"] =                                            2671426
        location_lookup["Heartless White Mushroom"] =                                          2671427
        location_lookup["Heartless Wight Knight"] =                                            2671428
        location_lookup["Heartless Wizard"] =                                                  2671429
        location_lookup["Heartless Wyvern"] =                                                  2671430
        location_lookup["Heartless Yellow Opera"] =                                            2671431
    return location_lookup
end

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
    item_ids["Wonderland"]                       = 2663002
    item_ids["Olympus Coliseum"]                 = 2663003
    item_ids["Monstro"]                          = 2663004
    item_ids["Agrabah"]                          = 2663005
    item_ids["Halloween Town"]                   = 2663006
    item_ids["Atlantica"]                        = 2663007
    item_ids["Neverland"]                        = 2663008
    item_ids["Hollow Bastion"]                   = 2663009
    item_ids["100 Acre Wood"]                    = 2663010
    item_ids["Twilight Town"]                    = 2663011
    item_ids["Destiny Islands"]                  = 2663012
    item_ids["Castle Oblivion"]                  = 2663013
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

journal_byte_location_ids = define_journal_byte_location_ids()
card_order = define_card_order()
enemy_card_order = define_enemy_card_order()
location_lookup = define_location_lookup()
item_ids = define_item_ids()

base_address = 0x7FF698380000
frame_count = 1


function get_journal_array()
    journal_byte_pointer_offset = 0x00879408
    journal_byte_value_offset = 0x64
    journal_byte_pointer = GetPointerA(base_address+journal_byte_pointer_offset, 0x0)
    return ReadArrayA(journal_byte_pointer + journal_byte_value_offset, #journal_byte_location_ids)
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

function get_current_floor()
    return ReadByte(base_address + 0x878044, true)
end

function get_time_played()
    time_played_pointer_offset = 0x008778E0
    time_played_offset_1 = 0x8
    time_played_offset_2 = 0x300
    time_played_pointer_1 = GetPointerA(base_address+time_played_pointer_offset, 0x0)
    time_played_pointer_2 = GetPointerA(time_played_pointer_1+time_played_offset_1, 0x0)
    time_played = ReadInt(time_played_pointer_2 + time_played_offset_2, 0x0, true)
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

function set_gold_map_cards(gold_map_cards_array)
    gold_map_cards_pointer_offset = 0x00876FF0
    gold_map_cards_value_offset = 0x2
    gold_map_cards_pointer = GetPointerA(base_address+gold_map_cards_pointer_offset, 0x0)
    WriteArrayA(gold_map_cards_pointer+gold_map_cards_value_offset, gold_map_cards_array)
end

function set_cards(card_array)
    cards_pointer_offset = 0x008793F8
    card_value_offset = -0xD74
    cards_pointer = GetPointerA(base_address+cards_pointer_offset, 0x0)
    WriteArrayA(cards_pointer+card_value_offset, card_array)
end

function set_enemy_cards(enemy_card_array)
    enemy_cards_pointer_offset = 0x008793F8
    enemy_cards_value_offset = -0x914
    enemy_cards_pointer = GetPointerA(base_address+enemy_cards_pointer_offset, 0x0)
    WriteArrayA(enemy_cards_pointer+enemy_cards_value_offset, enemy_card_array)
end

function set_friends(friends_array)
    friend_byte_pointer_offset = 0x00879408
    friend_byte_value_offset = 0x64 + #journal_byte_location_ids
    friend_byte_pointer = GetPointerA(base_address+friend_byte_pointer_offset, 0x0)
    WriteArrayA(friend_byte_pointer + friend_byte_value_offset, friends_array)
end

function set_world_assignment(world_assignment_array)
    world_assignment_pointer_offset = 0x00879398
    world_assignment_value_offset = 0x48
    world_assignment_pointer = GetPointerA(base_address+world_assignment_pointer_offset, 0x0)
    WriteArrayA(world_assignment_pointer+world_assignment_value_offset, world_assignment_array)
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

function set_starting_deck()
    add_card("Kingdom Key", 8)
    add_card("Kingdom Key", 7)
    add_card("Kingdom Key", 6)
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

function receive_items()
    card_array = get_empty_card_array()
    enemy_card_array = get_empty_enemy_card_array()
    world_assignment_array = get_empty_world_assignment_array()
    gold_map_cards_array = get_empty_gold_map_cards_array()
    friends_array = get_empty_friends_array()
    current_floor = get_current_floor()
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
                    card_array = add_enemy_card(card_array, received_item_name:sub(12))
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