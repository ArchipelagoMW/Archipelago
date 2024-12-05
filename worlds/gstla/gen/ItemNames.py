# This file was generated using jinja2 from a template. If this file needs
# to be changed, either change the template, or the code leveraging the template.
from typing import Dict
from enum import Enum
class ItemName(str, Enum):
    # Consumable
    Empty = "Empty"
    Herb = "Herb"
    Nut = "Nut"
    Vial = "Vial"
    Potion = "Potion"
    Psy_Crystal = "Psy Crystal"
    Antidote = "Antidote"
    Elixir = "Elixir"
    Water_of_Life = "Water of Life"
    Mist_Potion = "Mist Potion"
    Power_Bread = "Power Bread"
    Cookie = "Cookie"
    Apple = "Apple"
    Hard_Nut = "Hard Nut"
    Mint = "Mint"
    Lucky_Pepper = "Lucky Pepper"
    Smoke_Bomb = "Smoke Bomb"
    Sleep_Bomb = "Sleep Bomb"
    Lucky_Medal = "Lucky Medal"
    Bone = "Bone"
    Corn = "Corn"
    Sacred_Feather = "Sacred Feather"
    Oil_Drop = "Oil Drop"
    Weasels_Claw = "Weasel's Claw"
    Bramble_Seed = "Bramble Seed"
    Crystal_Powder = "Crystal Powder"
    Black_Crystal = "Black Crystal"
    Red_Key = "Red Key"
    Blue_Key = "Blue Key"
    Tear_Stone = "Tear Stone"
    Star_Dust = "Star Dust"
    Sylph_Feather = "Sylph Feather"
    Dragon_Skin = "Dragon Skin"
    Salamander_Tail = "Salamander Tail"
    Golem_Core = "Golem Core"
    Mythril_Silver = "Mythril Silver"
    Dark_Matter = "Dark Matter"
    Orihalcon = "Orihalcon"
    Right_Prong = "Right Prong"
    Left_Prong = "Left Prong"
    Center_Prong = "Center Prong"
    Healing_Fungus = "Healing Fungus"
    Laughing_Fungus = "Laughing Fungus"
    Dancing_Idol = "Dancing Idol"
    Pretty_Stone = "Pretty Stone"
    Red_Cloth = "Red Cloth"
    Milk = "Milk"
    Lil_Turtle = "Li'l Turtle"
    Aquarius_Stone = "Aquarius Stone"
    Sea_Gods_Tear = "Sea God's Tear"
    Ruin_Key = "Ruin Key"
    Magma_Ball = "Magma Ball"
    Coins_3 = "Coins 3"
    Coins_12 = "Coins 12"
    Coins_15 = "Coins 15"
    Coins_315 = "Coins 315"
    Coins_32 = "Coins 32"
    Coins_123 = "Coins 123"
    Coins_777 = "Coins 777"
    Coins_82 = "Coins 82"
    Coins_666 = "Coins 666"
    Coins_18 = "Coins 18"
    Coins_16 = "Coins 16"
    Coins_182 = "Coins 182"
    Coins_210 = "Coins 210"
    Coins_365 = "Coins 365"
    Coins_166 = "Coins 166"
    Coins_161 = "Coins 161"
    Coins_911 = "Coins 911"
    Coins_306 = "Coins 306"
    Coins_383 = "Coins 383"
    # Weapon
    Long_Sword = "Long Sword"
    Broad_Sword = "Broad Sword"
    Claymore = "Claymore"
    Great_Sword = "Great Sword"
    Shamshir = "Shamshir"
    Silver_Blade = "Silver Blade"
    Fire_Brand = "Fire Brand"
    Arctic_Blade = "Arctic Blade"
    Gaia_Blade = "Gaia Blade"
    Sol_Blade = "Sol Blade"
    Muramasa = "Muramasa"
    Machete = "Machete"
    Short_Sword = "Short Sword"
    Hunters_Sword = "Hunter's Sword"
    Battle_Rapier = "Battle Rapier"
    Master_Rapier = "Master Rapier"
    Ninja_Blade = "Ninja Blade"
    Swift_Sword = "Swift Sword"
    Elven_Rapier = "Elven Rapier"
    Assassin_Blade = "Assassin Blade"
    Mystery_Blade = "Mystery Blade"
    Kikuichimonji = "Kikuichimonji"
    Masamune = "Masamune"
    Bandits_Sword = "Bandit's Sword"
    Battle_Axe = "Battle Axe"
    Broad_Axe = "Broad Axe"
    Great_Axe = "Great Axe"
    Dragon_Axe = "Dragon Axe"
    Giant_Axe = "Giant Axe"
    Vulcan_Axe = "Vulcan Axe"
    Burning_Axe = "Burning Axe"
    Demon_Axe = "Demon Axe"
    Mace = "Mace"
    Heavy_Mace = "Heavy Mace"
    Battle_Mace = "Battle Mace"
    War_Mace = "War Mace"
    Righteous_Mace = "Righteous Mace"
    Grievous_Mace = "Grievous Mace"
    Blessed_Mace = "Blessed Mace"
    Wicked_Mace = "Wicked Mace"
    Wooden_Stick = "Wooden Stick"
    Magic_Rod = "Magic Rod"
    Witchs_Wand = "Witch's Wand"
    Blessed_Ankh = "Blessed Ankh"
    Psynergy_Rod = "Psynergy Rod"
    Frost_Wand = "Frost Wand"
    Angelic_Ankh = "Angelic Ankh"
    Demonic_Staff = "Demonic Staff"
    Crystal_Rod = "Crystal Rod"
    Zodiac_Wand = "Zodiac Wand"
    Shamans_Rod = "Shaman's Rod"
    Huge_Sword = "Huge Sword"
    Mythril_Blade = "Mythril Blade"
    Levatine = "Levatine"
    Darksword = "Darksword"
    Excalibur = "Excalibur"
    Robbers_Blade = "Robber's Blade"
    Soul_Brand = "Soul Brand"
    Storm_Brand = "Storm Brand"
    Hestia_Blade = "Hestia Blade"
    Lightning_Sword = "Lightning Sword"
    Rune_Blade = "Rune Blade"
    Cloud_Brand = "Cloud Brand"
    Sylph_Rapier = "Sylph Rapier"
    Burning_Sword = "Burning Sword"
    Pirates_Sword = "Pirate's Sword"
    Corsairs_Edge = "Corsair's Edge"
    Pirates_Sabre = "Pirate's Sabre"
    Hypnos_Sword = "Hypnos' Sword"
    Mist_Sabre = "Mist Sabre"
    Phaetons_Blade = "Phaeton's Blade"
    Tisiphone_Edge = "Tisiphone Edge"
    Apollos_Axe = "Apollo's Axe"
    Gaias_Axe = "Gaia's Axe"
    Stellar_Axe = "Stellar Axe"
    Captains_Axe = "Captain's Axe"
    Viking_Axe = "Viking Axe"
    Disk_Axe = "Disk Axe"
    Themis_Axe = "Themis' Axe"
    Mighty_Axe = "Mighty Axe"
    Tartarus_Axe = "Tartarus Axe"
    Comet_Mace = "Comet Mace"
    Tungsten_Mace = "Tungsten Mace"
    Demon_Mace = "Demon Mace"
    Hagbone_Mace = "Hagbone Mace"
    Blow_Mace = "Blow Mace"
    Rising_Mace = "Rising Mace"
    Thanatos_Mace = "Thanatos Mace"
    Cloud_Wand = "Cloud Wand"
    Salamander_Rod = "Salamander Rod"
    Nebula_Wand = "Nebula Wand"
    Dracomace = "Dracomace"
    Glower_Staff = "Glower Staff"
    Goblins_Rod = "Goblin's Rod"
    Meditation_Rod = "Meditation Rod"
    Firemans_Pole = "Fireman's Pole"
    Atropos_Rod = "Atropos' Rod"
    Lachesis_Rule = "Lachesis' Rule"
    Clothos_Distaff = "Clotho's Distaff"
    Staff_of_Anubis = "Staff of Anubis"
    Rusty_Sword_RobbersBlade = "Rusty Sword - Robber's Blade"
    Rusty_Sword_SoulBrand = "Rusty Sword - Soul Brand"
    Rusty_Sword_CorsairsEdge = "Rusty Sword - Corsair's Edge"
    Rusty_Sword_PiratesSabre = "Rusty Sword - Pirate's Sabre"
    Rusty_Axe_CaptainsAxe = "Rusty Axe - Captain's Axe"
    Rusty_Axe_VikingAxe = "Rusty Axe - Viking Axe"
    Rusty_Mace_DemonMace = "Rusty Mace - Demon Mace"
    Rusty_Mace_HagboneMace = "Rusty Mace - Hagbone Mace"
    Rusty_Staff_Dracomace = "Rusty Staff - Dracomace"
    Rusty_Staff_GlowerStaff = "Rusty Staff - Glower Staff"
    Rusty_Staff_GoblinsRod = "Rusty Staff - Goblin's Rod"
    # Armor
    Leather_Armor = "Leather Armor"
    Psynergy_Armor = "Psynergy Armor"
    Chain_Mail = "Chain Mail"
    Armored_Shell = "Armored Shell"
    Plate_Mail = "Plate Mail"
    Steel_Armor = "Steel Armor"
    Spirit_Armor = "Spirit Armor"
    Dragon_Scales = "Dragon Scales"
    Demon_Mail = "Demon Mail"
    Asuras_Armor = "Asura's Armor"
    Spiked_Armor = "Spiked Armor"
    Cotton_Shirt = "Cotton Shirt"
    Travel_Vest = "Travel Vest"
    Fur_Coat = "Fur Coat"
    Adepts_Clothes = "Adept's Clothes"
    Elven_Shirt = "Elven Shirt"
    Silver_Vest = "Silver Vest"
    Water_Jacket = "Water Jacket"
    Storm_Gear = "Storm Gear"
    Kimono = "Kimono"
    Ninja_Garb = "Ninja Garb"
    OnePiece_Dress = "OnePiece Dress"
    Travel_Robe = "Travel Robe"
    Silk_Robe = "Silk Robe"
    China_Dress = "China Dress"
    Jerkin = "Jerkin"
    Cocktail_Dress = "Cocktail Dress"
    Blessed_Robe = "Blessed Robe"
    Magical_Cassock = "Magical Cassock"
    Mysterious_Robe = "Mysterious Robe"
    Feathered_Robe = "Feathered Robe"
    Oracles_Robe = "Oracle's Robe"
    Planet_Armor = "Planet Armor"
    Dragon_Mail = "Dragon Mail"
    Chronos_Mail = "Chronos Mail"
    Stealth_Armor = "Stealth Armor"
    Xylion_Armor = "Xylion Armor"
    Ixion_Mail = "Ixion Mail"
    Phantasmal_Mail = "Phantasmal Mail"
    Erebus_Armor = "Erebus Armor"
    Valkyrie_Mail = "Valkyrie Mail"
    Faery_Vest = "Faery Vest"
    Mythril_Clothes = "Mythril Clothes"
    Full_Metal_Vest = "Full Metal Vest"
    Wild_Coat = "Wild Coat"
    Floral_Dress = "Floral Dress"
    Festival_Coat = "Festival Coat"
    Erinyes_Tunic = "Erinyes Tunic"
    Tritons_Ward = "Triton's Ward"
    Dragon_Robe = "Dragon Robe"
    Ardagh_Robe = "Ardagh Robe"
    Muni_Robe = "Muni Robe"
    Aeolian_Cassock = "Aeolian Cassock"
    Iris_Robe = "Iris Robe"
    # Shield
    Wooden_Shield = "Wooden Shield"
    Bronze_Shield = "Bronze Shield"
    Iron_Shield = "Iron Shield"
    Knights_Shield = "Knight's Shield"
    Mirrored_Shield = "Mirrored Shield"
    Dragon_Shield_GS = "Dragon Shield GS"
    Earth_Shield = "Earth Shield"
    Padded_Gloves = "Padded Gloves"
    Leather_Gloves = "Leather Gloves"
    Gauntlets = "Gauntlets"
    Vambrace = "Vambrace"
    War_Gloves = "War Gloves"
    Spirit_Gloves_GS = "Spirit Gloves GS"
    Battle_Gloves = "Battle Gloves"
    Aura_Gloves = "Aura Gloves"
    Leather_Armlet = "Leather Armlet"
    Armlet = "Armlet"
    Heavy_Armlet = "Heavy Armlet"
    Silver_Armlet = "Silver Armlet"
    Spirit_Armlet = "Spirit Armlet"
    Virtuous_Armlet = "Virtuous Armlet"
    Guardian_Armlet = "Guardian Armlet"
    Luna_Shield = "Luna Shield"
    Dragon_Shield = "Dragon Shield"
    Flame_Shield = "Flame Shield"
    Terra_Shield = "Terra Shield"
    Cosmos_Shield = "Cosmos Shield"
    Fujin_Shield = "Fujin Shield"
    Aegis_Shield = "Aegis Shield"
    Aerial_Gloves = "Aerial Gloves"
    Titan_Gloves = "Titan Gloves"
    Big_Bang_Gloves = "Big Bang Gloves"
    Crafted_Gloves = "Crafted Gloves"
    Riot_Gloves = "Riot Gloves"
    Spirit_Gloves = "Spirit Gloves"
    Clear_Bracelet = "Clear Bracelet"
    Mythril_Armlet = "Mythril Armlet"
    Bone_Armlet = "Bone Armlet"
    Jesters_Armlet = "Jester's Armlet"
    Ledas_Bracelet = "Leda's Bracelet"
    # Helm
    Open_Helm = "Open Helm"
    Bronze_Helm = "Bronze Helm"
    Iron_Helm = "Iron Helm"
    Steel_Helm = "Steel Helm"
    Silver_Helm = "Silver Helm"
    Knights_Helm = "Knight's Helm"
    Warriors_Helm = "Warrior's Helm"
    Adepts_Helm = "Adept's Helm"
    Leather_Cap = "Leather Cap"
    Wooden_Cap = "Wooden Cap"
    Mail_Cap = "Mail Cap"
    Jeweled_Crown = "Jeweled Crown"
    Ninja_Hood = "Ninja Hood"
    Lucky_Cap = "Lucky Cap"
    Thunder_Crown = "Thunder Crown"
    Prophets_Hat = "Prophet's Hat"
    Lure_Cap = "Lure Cap"
    Circlet = "Circlet"
    Silver_Circlet = "Silver Circlet"
    Guardian_Circlet = "Guardian Circlet"
    Platinum_Circlet = "Platinum Circlet"
    Mythril_Circlet = "Mythril Circlet"
    Glittering_Tiara = "Glittering Tiara"
    Dragon_Helm = "Dragon Helm"
    Mythril_Helm = "Mythril Helm"
    Fear_Helm = "Fear Helm"
    Millenium_Helm = "Millenium Helm"
    Viking_Helm = "Viking Helm"
    Gloria_Helm = "Gloria Helm"
    Minerva_Helm = "Minerva Helm"
    Floating_Hat = "Floating Hat"
    Nurses_Cap = "Nurse's Cap"
    Thorn_Crown = "Thorn Crown"
    Otafuku_Mask = "Otafuku Mask"
    Hiotoko_Mask = "Hiotoko Mask"
    Crown_of_Glory = "Crown of Glory"
    Alastors_Hood = "Alastor's Hood"
    Pure_Circlet = "Pure Circlet"
    Astral_Circlet = "Astral Circlet"
    Psychic_Circlet = "Psychic Circlet"
    Demon_Circlet = "Demon Circlet"
    Clarity_Circlet = "Clarity Circlet"
    Brilliant_Circlet = "Brilliant Circlet"
    Berserker_Band = "Berserker Band"
    # Boots
    Hyper_Boots = "Hyper Boots"
    Quick_Boots = "Quick Boots"
    Fur_Boots = "Fur Boots"
    Turtle_Boots = "Turtle Boots"
    Leather_Boots = "Leather Boots"
    Dragon_Boots = "Dragon Boots"
    Safety_Boots = "Safety Boots"
    Knights_Greave = "Knight's Greave"
    Silver_Greave = "Silver Greave"
    Ninja_Sandals = "Ninja Sandals"
    Golden_Boots = "Golden Boots"
    # PsyenergyItem
    Lash_Pebble = "Lash Pebble"
    Pound_Cube = "Pound Cube"
    Orb_of_Force = "Orb of Force"
    Douse_Drop = "Douse Drop"
    Frost_Jewel = "Frost Jewel"
    Lifting_Gem = "Lifting Gem"
    Halt_Gem = "Halt Gem"
    Cloak_Ball = "Cloak Ball"
    Carry_Stone = "Carry Stone"
    Catch_Beads = "Catch Beads"
    Tremor_Bit = "Tremor Bit"
    Scoop_Gem = "Scoop Gem"
    Cyclone_Chip = "Cyclone Chip"
    Burst_Brooch = "Burst Brooch"
    Grindstone = "Grindstone"
    Hover_Jade = "Hover Jade"
    Teleport_Lapis = "Teleport Lapis"
    # Trident
    Trident = "Trident"
    # Ring
    Adept_Ring = "Adept Ring"
    War_Ring = "War Ring"
    Sleep_Ring = "Sleep Ring"
    Healing_Ring = "Healing Ring"
    Unicorn_Ring = "Unicorn Ring"
    Fairy_Ring = "Fairy Ring"
    Clerics_Ring = "Cleric's Ring"
    Spirit_Ring = "Spirit Ring"
    Stardust_Ring = "Stardust Ring"
    Aroma_Ring = "Aroma Ring"
    Rainbow_Ring = "Rainbow Ring"
    Soul_Ring = "Soul Ring"
    Guardian_Ring = "Guardian Ring"
    Golden_Ring = "Golden Ring"
    # Shirt
    Mythril_Shirt = "Mythril Shirt"
    Silk_Shirt = "Silk Shirt"
    Running_Shirt = "Running Shirt"
    Divine_Camisole = "Divine Camisole"
    Herbed_Shirt = "Herbed Shirt"
    Golden_Shirt = "Golden Shirt"
    Casual_Shirt = "Casual Shirt"
    # Class
    Mysterious_Card = "Mysterious Card"
    Trainers_Whip = "Trainer's Whip"
    Tomegathericon = "Tomegathericon"
    # KeyItem
    Mars_Star = "Mars Star"
    # Mimic
    Milquetoast_Mimic = "Milquetoast Mimic"
    Clumsy_Mimic = "Clumsy Mimic"
    Mimic = "Mimic"
    Journeyman_Mimic = "Journeyman Mimic"
    Advanced_Mimic = "Advanced Mimic"
    Sacred_Mimic = "Sacred Mimic"
    Royal_Mimic = "Royal Mimic"
    Imperial_Mimic = "Imperial Mimic"
    Divine_Mimic = "Divine Mimic"
    

    #Summons
    Venus="Venus"
    Mercury="Mercury"
    Mars="Mars"
    Jupiter="Jupiter"
    Ramses="Ramses"
    Nereid="Nereid"
    Kirin="Kirin"
    Atalanta="Atalanta"
    Cybele="Cybele"
    Neptune="Neptune"
    Tiamat="Tiamat"
    Procne="Procne"
    Judgment="Judgment"
    Boreas="Boreas"
    Meteor="Meteor"
    Thor="Thor"
    Zagan="Zagan"
    Megaera="Megaera"
    Flora="Flora"
    Moloch="Moloch"
    Ulysses="Ulysses"
    Haures="Haures"
    Eclipse="Eclipse"
    Coatlique="Coatlique"
    Daedalus="Daedalus"
    Azul="Azul"
    Catastrophe="Catastrophe"
    Charon="Charon"
    Iris="Iris"
    

    # Psyenergy
    Growth = "Growth"
    Whirlwind = "Whirlwind"
    Parch = "Parch"
    Sand = "Sand"
    Mind_Read = "Mind Read"
    Reveal = "Reveal"
    Blaze = "Blaze"
    # Djinn
    Flint = "Flint"
    Granite = "Granite"
    Quartz = "Quartz"
    Vine = "Vine"
    Sap = "Sap"
    Ground = "Ground"
    Bane = "Bane"
    Echo = "Echo"
    Iron = "Iron"
    Steel = "Steel"
    Mud = "Mud"
    Flower = "Flower"
    Meld = "Meld"
    Petra = "Petra"
    Salt = "Salt"
    Geode = "Geode"
    Mold = "Mold"
    Crystal = "Crystal"
    Fizz = "Fizz"
    Sleet = "Sleet"
    Mist = "Mist"
    Spritz = "Spritz"
    Hail = "Hail"
    Tonic = "Tonic"
    Dew = "Dew"
    Fog = "Fog"
    Sour = "Sour"
    Spring = "Spring"
    Shade = "Shade"
    Chill = "Chill"
    Steam = "Steam"
    Rime = "Rime"
    Gel = "Gel"
    Eddy = "Eddy"
    Balm = "Balm"
    Serac = "Serac"
    Forge = "Forge"
    Fever = "Fever"
    Corona = "Corona"
    Scorch = "Scorch"
    Ember = "Ember"
    Flash = "Flash"
    Torch = "Torch"
    Cannon = "Cannon"
    Spark = "Spark"
    Kindle = "Kindle"
    Char = "Char"
    Coal = "Coal"
    Reflux = "Reflux"
    Core = "Core"
    Tinder = "Tinder"
    Shine = "Shine"
    Fury = "Fury"
    Fugue = "Fugue"
    Gust = "Gust"
    Breeze = "Breeze"
    Zephyr = "Zephyr"
    Smog = "Smog"
    Kite = "Kite"
    Squall = "Squall"
    Luff = "Luff"
    Breath = "Breath"
    Blitz = "Blitz"
    Ether = "Ether"
    Waft = "Waft"
    Haze = "Haze"
    Wheeze = "Wheeze"
    Aroma = "Aroma"
    Whorl = "Whorl"
    Gasp = "Gasp"
    Lull = "Lull"
    Gale = "Gale"
    # Events
    Victory = "Victory"
    Briggs_defeated = "Briggs defeated"
    Briggs_escaped = "Briggs escaped"
    Gabomba_Statue_Completed = "Gabomba Statue Completed"
    Serpent_defeated = "Serpent defeated"
    Poseidon_defeated = "Poseidon defeated"
    Aqua_Hydra_defeated = "Aqua Hydra defeated"
    Moapa_defeated = "Moapa defeated"
    Jupiter_Beacon_Lit = "Jupiter Beacon Lit"
    Flame_Dragons_defeated = "Flame Dragons - defeated"
    Ship = "Ship"
    Wings_of_Anemos = "Wings of Anemos"
    

    # Characters
    Isaac = "Isaac"
    Garet = "Garet"
    Ivan = "Ivan"
    Mia = "Mia"
    Jenna = "Jenna"
    Sheba = "Sheba"
    Piers = "Piers"
    

item_id_by_name: Dict[ItemName, int] = {
    "???": 0,
    "Milquetoast Mimic": 2561,
    "Clumsy Mimic": 2562,
    "Mimic": 2563,
    "Journeyman Mimic": 2564,
    "Advanced Mimic": 2565,
    "Sacred Mimic": 2566,
    "Royal Mimic": 2567,
    "Imperial Mimic": 2568,
    "Divine Mimic": 2569,
    "Empty": 0,
    "Long Sword": 1,
    "Broad Sword": 2,
    "Claymore": 3,
    "Great Sword": 4,
    "Shamshir": 5,
    "Silver Blade": 6,
    "Fire Brand": 7,
    "Arctic Blade": 8,
    "Gaia Blade": 9,
    "Sol Blade": 10,
    "Muramasa": 11,
    "Machete": 15,
    "Short Sword": 16,
    "Hunter's Sword": 17,
    "Battle Rapier": 18,
    "Master Rapier": 19,
    "Ninja Blade": 20,
    "Swift Sword": 21,
    "Elven Rapier": 22,
    "Assassin Blade": 23,
    "Mystery Blade": 24,
    "Kikuichimonji": 25,
    "Masamune": 26,
    "Bandit's Sword": 27,
    "Battle Axe": 31,
    "Broad Axe": 32,
    "Great Axe": 33,
    "Dragon Axe": 34,
    "Giant Axe": 35,
    "Vulcan Axe": 36,
    "Burning Axe": 37,
    "Demon Axe": 38,
    "Mace": 43,
    "Heavy Mace": 44,
    "Battle Mace": 45,
    "War Mace": 46,
    "Righteous Mace": 47,
    "Grievous Mace": 48,
    "Blessed Mace": 49,
    "Wicked Mace": 50,
    "Wooden Stick": 55,
    "Magic Rod": 56,
    "Witch's Wand": 57,
    "Blessed Ankh": 58,
    "Psynergy Rod": 59,
    "Frost Wand": 60,
    "Angelic Ankh": 61,
    "Demonic Staff": 62,
    "Crystal Rod": 63,
    "Zodiac Wand": 64,
    "Shaman's Rod": 65,
    "Leather Armor": 75,
    "Psynergy Armor": 76,
    "Chain Mail": 77,
    "Armored Shell": 78,
    "Plate Mail": 79,
    "Steel Armor": 80,
    "Spirit Armor": 81,
    "Dragon Scales": 82,
    "Demon Mail": 83,
    "Asura's Armor": 84,
    "Spiked Armor": 85,
    "Cotton Shirt": 89,
    "Travel Vest": 90,
    "Fur Coat": 91,
    "Adept's Clothes": 92,
    "Elven Shirt": 93,
    "Silver Vest": 94,
    "Water Jacket": 95,
    "Storm Gear": 96,
    "Kimono": 97,
    "Ninja Garb": 98,
    "OnePiece Dress": 103,
    "Travel Robe": 104,
    "Silk Robe": 105,
    "China Dress": 106,
    "Jerkin": 107,
    "Cocktail Dress": 108,
    "Blessed Robe": 109,
    "Magical Cassock": 110,
    "Mysterious Robe": 111,
    "Feathered Robe": 112,
    "Oracle's Robe": 113,
    "Wooden Shield": 118,
    "Bronze Shield": 119,
    "Iron Shield": 120,
    "Knight's Shield": 121,
    "Mirrored Shield": 122,
    "Dragon Shield GS": 123,
    "Earth Shield": 124,
    "Padded Gloves": 127,
    "Leather Gloves": 128,
    "Gauntlets": 129,
    "Vambrace": 130,
    "War Gloves": 131,
    "Spirit Gloves GS": 132,
    "Battle Gloves": 133,
    "Aura Gloves": 134,
    "Leather Armlet": 136,
    "Armlet": 137,
    "Heavy Armlet": 138,
    "Silver Armlet": 139,
    "Spirit Armlet": 140,
    "Virtuous Armlet": 141,
    "Guardian Armlet": 142,
    "Open Helm": 145,
    "Bronze Helm": 146,
    "Iron Helm": 147,
    "Steel Helm": 148,
    "Silver Helm": 149,
    "Knight's Helm": 150,
    "Warrior's Helm": 151,
    "Adept's Helm": 152,
    "Leather Cap": 156,
    "Wooden Cap": 157,
    "Mail Cap": 158,
    "Jeweled Crown": 159,
    "Ninja Hood": 160,
    "Lucky Cap": 161,
    "Thunder Crown": 162,
    "Prophet's Hat": 163,
    "Lure Cap": 164,
    "Circlet": 166,
    "Silver Circlet": 167,
    "Guardian Circlet": 168,
    "Platinum Circlet": 169,
    "Mythril Circlet": 170,
    "Glittering Tiara": 171,
    "Herb": 180,
    "Nut": 181,
    "Vial": 182,
    "Potion": 183,
    "Psy Crystal": 186,
    "Antidote": 187,
    "Elixir": 188,
    "Water of Life": 189,
    "Mist Potion": 190,
    "Power Bread": 191,
    "Cookie": 192,
    "Apple": 193,
    "Hard Nut": 194,
    "Mint": 195,
    "Lucky Pepper": 196,
    "Lash Pebble": 3717,
    "Pound Cube": 3718,
    "Orb of Force": 3726,
    "Douse Drop": 3617,
    "Frost Jewel": 3608,
    "Lifting Gem": 3727,
    "Halt Gem": 3729,
    "Cloak Ball": 3730,
    "Carry Stone": 3731,
    "Catch Beads": 3732,
    "Tremor Bit": 3719,
    "Scoop Gem": 3720,
    "Cyclone Chip": 3721,
    "Burst Brooch": 3735,
    "Grindstone": 3736,
    "Hover Jade": 3737,
    "Teleport Lapis": 3740,
    "Mars Star": 222,
    "Smoke Bomb": 226,
    "Sleep Bomb": 227,
    "Lucky Medal": 229,
    "Bone": 231,
    "Corn": 233,
    "Sacred Feather": 236,
    "Oil Drop": 238,
    "Weasel's Claw": 239,
    "Bramble Seed": 240,
    "Crystal Powder": 241,
    "Black Crystal": 242,
    "Red Key": 243,
    "Blue Key": 244,
    "Mythril Shirt": 250,
    "Silk Shirt": 251,
    "Running Shirt": 252,
    "Hyper Boots": 256,
    "Quick Boots": 257,
    "Fur Boots": 258,
    "Turtle Boots": 259,
    "Adept Ring": 262,
    "War Ring": 263,
    "Sleep Ring": 264,
    "Healing Ring": 265,
    "Unicorn Ring": 266,
    "Fairy Ring": 267,
    "Cleric's Ring": 268,
    "Huge Sword": 272,
    "Mythril Blade": 273,
    "Levatine": 274,
    "Darksword": 275,
    "Excalibur": 276,
    "Robber's Blade": 277,
    "Soul Brand": 278,
    "Storm Brand": 279,
    "Hestia Blade": 280,
    "Lightning Sword": 281,
    "Rune Blade": 282,
    "Cloud Brand": 283,
    "Sylph Rapier": 285,
    "Burning Sword": 286,
    "Pirate's Sword": 287,
    "Corsair's Edge": 288,
    "Pirate's Sabre": 289,
    "Hypnos' Sword": 290,
    "Mist Sabre": 291,
    "Phaeton's Blade": 292,
    "Tisiphone Edge": 293,
    "Apollo's Axe": 295,
    "Gaia's Axe": 296,
    "Stellar Axe": 297,
    "Captain's Axe": 298,
    "Viking Axe": 299,
    "Disk Axe": 300,
    "Themis' Axe": 301,
    "Mighty Axe": 302,
    "Tartarus Axe": 303,
    "Comet Mace": 305,
    "Tungsten Mace": 306,
    "Demon Mace": 307,
    "Hagbone Mace": 308,
    "Blow Mace": 309,
    "Rising Mace": 310,
    "Thanatos Mace": 311,
    "Cloud Wand": 313,
    "Salamander Rod": 314,
    "Nebula Wand": 315,
    "Dracomace": 316,
    "Glower Staff": 317,
    "Goblin's Rod": 318,
    "Meditation Rod": 319,
    "Fireman's Pole": 320,
    "Atropos' Rod": 321,
    "Lachesis' Rule": 322,
    "Clotho's Distaff": 323,
    "Staff of Anubis": 324,
    "Trident": 326,
    "Planet Armor": 328,
    "Dragon Mail": 329,
    "Chronos Mail": 330,
    "Stealth Armor": 331,
    "Xylion Armor": 332,
    "Ixion Mail": 333,
    "Phantasmal Mail": 334,
    "Erebus Armor": 335,
    "Valkyrie Mail": 336,
    "Faery Vest": 338,
    "Mythril Clothes": 339,
    "Full Metal Vest": 340,
    "Wild Coat": 341,
    "Floral Dress": 342,
    "Festival Coat": 343,
    "Erinyes Tunic": 344,
    "Triton's Ward": 345,
    "Dragon Robe": 347,
    "Ardagh Robe": 348,
    "Muni Robe": 349,
    "Aeolian Cassock": 350,
    "Iris Robe": 351,
    "Luna Shield": 353,
    "Dragon Shield": 354,
    "Flame Shield": 355,
    "Terra Shield": 356,
    "Cosmos Shield": 357,
    "Fujin Shield": 358,
    "Aegis Shield": 359,
    "Aerial Gloves": 361,
    "Titan Gloves": 362,
    "Big Bang Gloves": 363,
    "Crafted Gloves": 364,
    "Riot Gloves": 365,
    "Spirit Gloves": 366,
    "Clear Bracelet": 368,
    "Mythril Armlet": 369,
    "Bone Armlet": 370,
    "Jester's Armlet": 371,
    "Leda's Bracelet": 372,
    "Dragon Helm": 374,
    "Mythril Helm": 375,
    "Fear Helm": 376,
    "Millenium Helm": 377,
    "Viking Helm": 378,
    "Gloria Helm": 379,
    "Minerva Helm": 380,
    "Floating Hat": 382,
    "Nurse's Cap": 383,
    "Thorn Crown": 384,
    "Otafuku Mask": 385,
    "Hiotoko Mask": 386,
    "Crown of Glory": 387,
    "Alastor's Hood": 388,
    "Pure Circlet": 390,
    "Astral Circlet": 391,
    "Psychic Circlet": 392,
    "Demon Circlet": 393,
    "Clarity Circlet": 394,
    "Brilliant Circlet": 395,
    "Berserker Band": 396,
    "Divine Camisole": 398,
    "Herbed Shirt": 399,
    "Golden Shirt": 400,
    "Casual Shirt": 401,
    "Leather Boots": 402,
    "Dragon Boots": 403,
    "Safety Boots": 404,
    "Knight's Greave": 405,
    "Silver Greave": 406,
    "Ninja Sandals": 407,
    "Golden Boots": 408,
    "Spirit Ring": 409,
    "Stardust Ring": 410,
    "Aroma Ring": 411,
    "Rainbow Ring": 412,
    "Soul Ring": 413,
    "Guardian Ring": 414,
    "Golden Ring": 415,
    "Rusty Sword - Robber's Blade": 417,
    "Rusty Sword - Soul Brand": 418,
    "Rusty Sword - Corsair's Edge": 419,
    "Rusty Sword - Pirate's Sabre": 420,
    "Rusty Axe - Captain's Axe": 421,
    "Rusty Axe - Viking Axe": 422,
    "Rusty Mace - Demon Mace": 423,
    "Rusty Mace - Hagbone Mace": 424,
    "Rusty Staff - Dracomace": 425,
    "Rusty Staff - Glower Staff": 426,
    "Rusty Staff - Goblin's Rod": 427,
    "Tear Stone": 429,
    "Star Dust": 430,
    "Sylph Feather": 431,
    "Dragon Skin": 432,
    "Salamander Tail": 433,
    "Golem Core": 434,
    "Mythril Silver": 435,
    "Dark Matter": 436,
    "Orihalcon": 437,
    "Right Prong": 439,
    "Left Prong": 440,
    "Center Prong": 441,
    "Mysterious Card": 443,
    "Trainer's Whip": 444,
    "Tomegathericon": 445,
    "Healing Fungus": 448,
    "Laughing Fungus": 449,
    "Dancing Idol": 451,
    "Pretty Stone": 452,
    "Red Cloth": 453,
    "Milk": 454,
    "Li'l Turtle": 455,
    "Aquarius Stone": 456,
    "Sea God's Tear": 458,
    "Ruin Key": 459,
    "Magma Ball": 460,
    "Coins 3": 32771,
    "Coins 12": 32780,
    "Coins 15": 32783,
    "Coins 315": 33083,
    "Coins 32": 32800,
    "Coins 123": 32891,
    "Coins 777": 33545,
    "Coins 82": 32850,
    "Coins 666": 33434,
    "Coins 18": 32786,
    "Coins 16": 32784,
    "Coins 182": 32950,
    "Coins 210": 32978,
    "Coins 365": 33133,
    "Coins 166": 32934,
    "Coins 161": 32929,
    "Coins 911": 33679,
    "Coins 306": 33074,
    "Coins 383": 33151,
    "Venus": 3840,
    "Mercury": 3841,
    "Mars": 3842,
    "Jupiter": 3843,
    "Ramses": 3844,
    "Nereid": 3845,
    "Kirin": 3846,
    "Atalanta": 3847,
    "Cybele": 3848,
    "Neptune": 3849,
    "Tiamat": 3850,
    "Procne": 3851,
    "Judgment": 3852,
    "Boreas": 3853,
    "Meteor": 3854,
    "Thor": 3855,
    "Zagan": 3856,
    "Megaera": 3857,
    "Flora": 3858,
    "Moloch": 3859,
    "Ulysses": 3860,
    "Haures": 3861,
    "Eclipse": 3862,
    "Coatlique": 3863,
    "Daedalus": 3864,
    "Azul": 3865,
    "Catastrophe": 3866,
    "Charon": 3867,
    "Iris": 3868,
    "Victory": 5001,
    "Briggs defeated": 5002,
    "Briggs escaped": 5003,
    "Gabomba Statue Completed": 5004,
    "Serpent defeated": 5005,
    "Poseidon defeated": 5006,
    "Aqua Hydra defeated": 5007,
    "Moapa defeated": 5008,
    "Jupiter Beacon Lit": 5009,
    "Flame Dragons - defeated": 5010,
    "Ship": 5011,
    "Wings of Anemos": 5012,
    "Flint": 16384000,
    "Granite": 16384002,
    "Quartz": 16384004,
    "Vine": 16384006,
    "Sap": 16384008,
    "Ground": 16384010,
    "Bane": 16384012,
    "Echo": 16384014,
    "Iron": 16384016,
    "Steel": 16384018,
    "Mud": 16384020,
    "Flower": 16384022,
    "Meld": 16384024,
    "Petra": 16384026,
    "Salt": 16384028,
    "Geode": 16384030,
    "Mold": 16384032,
    "Crystal": 16384034,
    "Fizz": 16384036,
    "Sleet": 16384038,
    "Mist": 16384040,
    "Spritz": 16384042,
    "Hail": 16384044,
    "Tonic": 16384046,
    "Dew": 16384048,
    "Fog": 16384050,
    "Sour": 16384052,
    "Spring": 16384054,
    "Shade": 16384056,
    "Chill": 16384058,
    "Steam": 16384060,
    "Rime": 16384062,
    "Gel": 16384064,
    "Eddy": 16384066,
    "Balm": 16384068,
    "Serac": 16384070,
    "Forge": 16384072,
    "Fever": 16384074,
    "Corona": 16384076,
    "Scorch": 16384078,
    "Ember": 16384080,
    "Flash": 16384082,
    "Torch": 16384084,
    "Cannon": 16384086,
    "Spark": 16384088,
    "Kindle": 16384090,
    "Char": 16384092,
    "Coal": 16384094,
    "Reflux": 16384096,
    "Core": 16384098,
    "Tinder": 16384100,
    "Shine": 16384102,
    "Fury": 16384104,
    "Fugue": 16384106,
    "Gust": 16384108,
    "Breeze": 16384110,
    "Zephyr": 16384112,
    "Smog": 16384114,
    "Kite": 16384116,
    "Squall": 16384118,
    "Luff": 16384120,
    "Breath": 16384122,
    "Blitz": 16384124,
    "Ether": 16384126,
    "Waft": 16384128,
    "Haze": 16384130,
    "Wheeze": 16384132,
    "Aroma": 16384134,
    "Whorl": 16384136,
    "Gasp": 16384138,
    "Lull": 16384140,
    "Gale": 16384142,
    "Growth": 3596,
    "Whirlwind": 3662,
    "Parch": 3722,
    "Sand": 3723,
    "Mind Read": 3725,
    "Reveal": 3728,
    "Blaze": 3738,
    "Isaac": 3328,
    "Garet": 3329,
    "Ivan": 3330,
    "Mia": 3331,
    "Jenna": 3333,
    "Sheba": 3334,
    "Piers": 3335,
    
}

name_by_item_id: Dict[int, ItemName] = {
    2561: "Milquetoast Mimic",
    2562: "Clumsy Mimic",
    2563: "Mimic",
    2564: "Journeyman Mimic",
    2565: "Advanced Mimic",
    2566: "Sacred Mimic",
    2567: "Royal Mimic",
    2568: "Imperial Mimic",
    2569: "Divine Mimic",
    0: "Empty",
    1: "Long Sword",
    2: "Broad Sword",
    3: "Claymore",
    4: "Great Sword",
    5: "Shamshir",
    6: "Silver Blade",
    7: "Fire Brand",
    8: "Arctic Blade",
    9: "Gaia Blade",
    10: "Sol Blade",
    11: "Muramasa",
    15: "Machete",
    16: "Short Sword",
    17: "Hunter's Sword",
    18: "Battle Rapier",
    19: "Master Rapier",
    20: "Ninja Blade",
    21: "Swift Sword",
    22: "Elven Rapier",
    23: "Assassin Blade",
    24: "Mystery Blade",
    25: "Kikuichimonji",
    26: "Masamune",
    27: "Bandit's Sword",
    31: "Battle Axe",
    32: "Broad Axe",
    33: "Great Axe",
    34: "Dragon Axe",
    35: "Giant Axe",
    36: "Vulcan Axe",
    37: "Burning Axe",
    38: "Demon Axe",
    43: "Mace",
    44: "Heavy Mace",
    45: "Battle Mace",
    46: "War Mace",
    47: "Righteous Mace",
    48: "Grievous Mace",
    49: "Blessed Mace",
    50: "Wicked Mace",
    55: "Wooden Stick",
    56: "Magic Rod",
    57: "Witch's Wand",
    58: "Blessed Ankh",
    59: "Psynergy Rod",
    60: "Frost Wand",
    61: "Angelic Ankh",
    62: "Demonic Staff",
    63: "Crystal Rod",
    64: "Zodiac Wand",
    65: "Shaman's Rod",
    75: "Leather Armor",
    76: "Psynergy Armor",
    77: "Chain Mail",
    78: "Armored Shell",
    79: "Plate Mail",
    80: "Steel Armor",
    81: "Spirit Armor",
    82: "Dragon Scales",
    83: "Demon Mail",
    84: "Asura's Armor",
    85: "Spiked Armor",
    89: "Cotton Shirt",
    90: "Travel Vest",
    91: "Fur Coat",
    92: "Adept's Clothes",
    93: "Elven Shirt",
    94: "Silver Vest",
    95: "Water Jacket",
    96: "Storm Gear",
    97: "Kimono",
    98: "Ninja Garb",
    103: "OnePiece Dress",
    104: "Travel Robe",
    105: "Silk Robe",
    106: "China Dress",
    107: "Jerkin",
    108: "Cocktail Dress",
    109: "Blessed Robe",
    110: "Magical Cassock",
    111: "Mysterious Robe",
    112: "Feathered Robe",
    113: "Oracle's Robe",
    118: "Wooden Shield",
    119: "Bronze Shield",
    120: "Iron Shield",
    121: "Knight's Shield",
    122: "Mirrored Shield",
    123: "Dragon Shield GS",
    124: "Earth Shield",
    127: "Padded Gloves",
    128: "Leather Gloves",
    129: "Gauntlets",
    130: "Vambrace",
    131: "War Gloves",
    132: "Spirit Gloves GS",
    133: "Battle Gloves",
    134: "Aura Gloves",
    136: "Leather Armlet",
    137: "Armlet",
    138: "Heavy Armlet",
    139: "Silver Armlet",
    140: "Spirit Armlet",
    141: "Virtuous Armlet",
    142: "Guardian Armlet",
    145: "Open Helm",
    146: "Bronze Helm",
    147: "Iron Helm",
    148: "Steel Helm",
    149: "Silver Helm",
    150: "Knight's Helm",
    151: "Warrior's Helm",
    152: "Adept's Helm",
    156: "Leather Cap",
    157: "Wooden Cap",
    158: "Mail Cap",
    159: "Jeweled Crown",
    160: "Ninja Hood",
    161: "Lucky Cap",
    162: "Thunder Crown",
    163: "Prophet's Hat",
    164: "Lure Cap",
    166: "Circlet",
    167: "Silver Circlet",
    168: "Guardian Circlet",
    169: "Platinum Circlet",
    170: "Mythril Circlet",
    171: "Glittering Tiara",
    180: "Herb",
    181: "Nut",
    182: "Vial",
    183: "Potion",
    186: "Psy Crystal",
    187: "Antidote",
    188: "Elixir",
    189: "Water of Life",
    190: "Mist Potion",
    191: "Power Bread",
    192: "Cookie",
    193: "Apple",
    194: "Hard Nut",
    195: "Mint",
    196: "Lucky Pepper",
    3717: "Lash Pebble",
    3718: "Pound Cube",
    3726: "Orb of Force",
    3617: "Douse Drop",
    3608: "Frost Jewel",
    3727: "Lifting Gem",
    3729: "Halt Gem",
    3730: "Cloak Ball",
    3731: "Carry Stone",
    3732: "Catch Beads",
    3719: "Tremor Bit",
    3720: "Scoop Gem",
    3721: "Cyclone Chip",
    3735: "Burst Brooch",
    3736: "Grindstone",
    3737: "Hover Jade",
    3740: "Teleport Lapis",
    222: "Mars Star",
    226: "Smoke Bomb",
    227: "Sleep Bomb",
    229: "Lucky Medal",
    231: "Bone",
    233: "Corn",
    236: "Sacred Feather",
    238: "Oil Drop",
    239: "Weasel's Claw",
    240: "Bramble Seed",
    241: "Crystal Powder",
    242: "Black Crystal",
    243: "Red Key",
    244: "Blue Key",
    250: "Mythril Shirt",
    251: "Silk Shirt",
    252: "Running Shirt",
    256: "Hyper Boots",
    257: "Quick Boots",
    258: "Fur Boots",
    259: "Turtle Boots",
    262: "Adept Ring",
    263: "War Ring",
    264: "Sleep Ring",
    265: "Healing Ring",
    266: "Unicorn Ring",
    267: "Fairy Ring",
    268: "Cleric's Ring",
    272: "Huge Sword",
    273: "Mythril Blade",
    274: "Levatine",
    275: "Darksword",
    276: "Excalibur",
    277: "Robber's Blade",
    278: "Soul Brand",
    279: "Storm Brand",
    280: "Hestia Blade",
    281: "Lightning Sword",
    282: "Rune Blade",
    283: "Cloud Brand",
    285: "Sylph Rapier",
    286: "Burning Sword",
    287: "Pirate's Sword",
    288: "Corsair's Edge",
    289: "Pirate's Sabre",
    290: "Hypnos' Sword",
    291: "Mist Sabre",
    292: "Phaeton's Blade",
    293: "Tisiphone Edge",
    295: "Apollo's Axe",
    296: "Gaia's Axe",
    297: "Stellar Axe",
    298: "Captain's Axe",
    299: "Viking Axe",
    300: "Disk Axe",
    301: "Themis' Axe",
    302: "Mighty Axe",
    303: "Tartarus Axe",
    305: "Comet Mace",
    306: "Tungsten Mace",
    307: "Demon Mace",
    308: "Hagbone Mace",
    309: "Blow Mace",
    310: "Rising Mace",
    311: "Thanatos Mace",
    313: "Cloud Wand",
    314: "Salamander Rod",
    315: "Nebula Wand",
    316: "Dracomace",
    317: "Glower Staff",
    318: "Goblin's Rod",
    319: "Meditation Rod",
    320: "Fireman's Pole",
    321: "Atropos' Rod",
    322: "Lachesis' Rule",
    323: "Clotho's Distaff",
    324: "Staff of Anubis",
    326: "Trident",
    328: "Planet Armor",
    329: "Dragon Mail",
    330: "Chronos Mail",
    331: "Stealth Armor",
    332: "Xylion Armor",
    333: "Ixion Mail",
    334: "Phantasmal Mail",
    335: "Erebus Armor",
    336: "Valkyrie Mail",
    338: "Faery Vest",
    339: "Mythril Clothes",
    340: "Full Metal Vest",
    341: "Wild Coat",
    342: "Floral Dress",
    343: "Festival Coat",
    344: "Erinyes Tunic",
    345: "Triton's Ward",
    347: "Dragon Robe",
    348: "Ardagh Robe",
    349: "Muni Robe",
    350: "Aeolian Cassock",
    351: "Iris Robe",
    353: "Luna Shield",
    354: "Dragon Shield",
    355: "Flame Shield",
    356: "Terra Shield",
    357: "Cosmos Shield",
    358: "Fujin Shield",
    359: "Aegis Shield",
    361: "Aerial Gloves",
    362: "Titan Gloves",
    363: "Big Bang Gloves",
    364: "Crafted Gloves",
    365: "Riot Gloves",
    366: "Spirit Gloves",
    368: "Clear Bracelet",
    369: "Mythril Armlet",
    370: "Bone Armlet",
    371: "Jester's Armlet",
    372: "Leda's Bracelet",
    374: "Dragon Helm",
    375: "Mythril Helm",
    376: "Fear Helm",
    377: "Millenium Helm",
    378: "Viking Helm",
    379: "Gloria Helm",
    380: "Minerva Helm",
    382: "Floating Hat",
    383: "Nurse's Cap",
    384: "Thorn Crown",
    385: "Otafuku Mask",
    386: "Hiotoko Mask",
    387: "Crown of Glory",
    388: "Alastor's Hood",
    390: "Pure Circlet",
    391: "Astral Circlet",
    392: "Psychic Circlet",
    393: "Demon Circlet",
    394: "Clarity Circlet",
    395: "Brilliant Circlet",
    396: "Berserker Band",
    398: "Divine Camisole",
    399: "Herbed Shirt",
    400: "Golden Shirt",
    401: "Casual Shirt",
    402: "Leather Boots",
    403: "Dragon Boots",
    404: "Safety Boots",
    405: "Knight's Greave",
    406: "Silver Greave",
    407: "Ninja Sandals",
    408: "Golden Boots",
    409: "Spirit Ring",
    410: "Stardust Ring",
    411: "Aroma Ring",
    412: "Rainbow Ring",
    413: "Soul Ring",
    414: "Guardian Ring",
    415: "Golden Ring",
    417: "Rusty Sword - Robber's Blade",
    418: "Rusty Sword - Soul Brand",
    419: "Rusty Sword - Corsair's Edge",
    420: "Rusty Sword - Pirate's Sabre",
    421: "Rusty Axe - Captain's Axe",
    422: "Rusty Axe - Viking Axe",
    423: "Rusty Mace - Demon Mace",
    424: "Rusty Mace - Hagbone Mace",
    425: "Rusty Staff - Dracomace",
    426: "Rusty Staff - Glower Staff",
    427: "Rusty Staff - Goblin's Rod",
    429: "Tear Stone",
    430: "Star Dust",
    431: "Sylph Feather",
    432: "Dragon Skin",
    433: "Salamander Tail",
    434: "Golem Core",
    435: "Mythril Silver",
    436: "Dark Matter",
    437: "Orihalcon",
    439: "Right Prong",
    440: "Left Prong",
    441: "Center Prong",
    443: "Mysterious Card",
    444: "Trainer's Whip",
    445: "Tomegathericon",
    448: "Healing Fungus",
    449: "Laughing Fungus",
    451: "Dancing Idol",
    452: "Pretty Stone",
    453: "Red Cloth",
    454: "Milk",
    455: "Li'l Turtle",
    456: "Aquarius Stone",
    458: "Sea God's Tear",
    459: "Ruin Key",
    460: "Magma Ball",
    32771: "Coins 3",
    32780: "Coins 12",
    32783: "Coins 15",
    33083: "Coins 315",
    32800: "Coins 32",
    32891: "Coins 123",
    33545: "Coins 777",
    32850: "Coins 82",
    33434: "Coins 666",
    32786: "Coins 18",
    32784: "Coins 16",
    32950: "Coins 182",
    32978: "Coins 210",
    33133: "Coins 365",
    32934: "Coins 166",
    32929: "Coins 161",
    33679: "Coins 911",
    33074: "Coins 306",
    33151: "Coins 383",
    3840: "Venus",
    3841: "Mercury",
    3842: "Mars",
    3843: "Jupiter",
    3844: "Ramses",
    3845: "Nereid",
    3846: "Kirin",
    3847: "Atalanta",
    3848: "Cybele",
    3849: "Neptune",
    3850: "Tiamat",
    3851: "Procne",
    3852: "Judgment",
    3853: "Boreas",
    3854: "Meteor",
    3855: "Thor",
    3856: "Zagan",
    3857: "Megaera",
    3858: "Flora",
    3859: "Moloch",
    3860: "Ulysses",
    3861: "Haures",
    3862: "Eclipse",
    3863: "Coatlique",
    3864: "Daedalus",
    3865: "Azul",
    3866: "Catastrophe",
    3867: "Charon",
    3868: "Iris",
    5001: "Victory",
    5002: "Briggs defeated",
    5003: "Briggs escaped",
    5004: "Gabomba Statue Completed",
    5005: "Serpent defeated",
    5006: "Poseidon defeated",
    5007: "Aqua Hydra defeated",
    5008: "Moapa defeated",
    5009: "Jupiter Beacon Lit",
    5010: "Flame Dragons - defeated",
    5011: "Ship",
    5012: "Wings of Anemos",
    16384000: "Flint",
    16384002: "Granite",
    16384004: "Quartz",
    16384006: "Vine",
    16384008: "Sap",
    16384010: "Ground",
    16384012: "Bane",
    16384014: "Echo",
    16384016: "Iron",
    16384018: "Steel",
    16384020: "Mud",
    16384022: "Flower",
    16384024: "Meld",
    16384026: "Petra",
    16384028: "Salt",
    16384030: "Geode",
    16384032: "Mold",
    16384034: "Crystal",
    16384036: "Fizz",
    16384038: "Sleet",
    16384040: "Mist",
    16384042: "Spritz",
    16384044: "Hail",
    16384046: "Tonic",
    16384048: "Dew",
    16384050: "Fog",
    16384052: "Sour",
    16384054: "Spring",
    16384056: "Shade",
    16384058: "Chill",
    16384060: "Steam",
    16384062: "Rime",
    16384064: "Gel",
    16384066: "Eddy",
    16384068: "Balm",
    16384070: "Serac",
    16384072: "Forge",
    16384074: "Fever",
    16384076: "Corona",
    16384078: "Scorch",
    16384080: "Ember",
    16384082: "Flash",
    16384084: "Torch",
    16384086: "Cannon",
    16384088: "Spark",
    16384090: "Kindle",
    16384092: "Char",
    16384094: "Coal",
    16384096: "Reflux",
    16384098: "Core",
    16384100: "Tinder",
    16384102: "Shine",
    16384104: "Fury",
    16384106: "Fugue",
    16384108: "Gust",
    16384110: "Breeze",
    16384112: "Zephyr",
    16384114: "Smog",
    16384116: "Kite",
    16384118: "Squall",
    16384120: "Luff",
    16384122: "Breath",
    16384124: "Blitz",
    16384126: "Ether",
    16384128: "Waft",
    16384130: "Haze",
    16384132: "Wheeze",
    16384134: "Aroma",
    16384136: "Whorl",
    16384138: "Gasp",
    16384140: "Lull",
    16384142: "Gale",
    3596: "Growth",
    3662: "Whirlwind",
    3722: "Parch",
    3723: "Sand",
    3725: "Mind Read",
    3728: "Reveal",
    3738: "Blaze",
    3328: "Isaac",
    3329: "Garet",
    3330: "Ivan",
    3331: "Mia",
    3333: "Jenna",
    3334: "Sheba",
    3335: "Piers",
    
}

assert len(ItemName.__members__) + 1 == len(item_id_by_name), \
    "Members: %d, Dict: %d" % (len(ItemName.__members__), len(item_id_by_name))