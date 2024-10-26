import math

from typing_extensions import TYPE_CHECKING

from worlds.generic.Rules import add_rule, add_item_rule
from typing import Set
from .Items import ItemType, all_items
from .gen.ItemNames import ItemName
from .gen.ItemData import summon_list, characters
from .Names.EntranceName import EntranceName
from .Locations import location_type_to_data
from .gen.LocationData import LocationType
from BaseClasses import MultiWorld
from .gen.LocationNames import LocationName, loc_names_by_id

if TYPE_CHECKING:
    from . import GSTLAWorld

def set_entrance_rules(world: 'GSTLAWorld'):
    multiworld = world.multiworld
    player = world.player
    add_rule(multiworld.get_entrance(EntranceName.DailaToShrineOfTheSeaGod, player),
             lambda state: state.has(ItemName.Lash_Pebble, player))

    add_rule(multiworld.get_entrance(EntranceName.DailaToKandoreanTemple, player),
             lambda state: state.has(ItemName.Whirlwind, player))

    add_rule(multiworld.get_entrance(EntranceName.MadraToMadraCatacombs, player),
             lambda state: state.has(ItemName.Reveal, player))

    add_rule(multiworld.get_entrance(EntranceName.YampiDesertFrontToYampiDesertBack, player),
             lambda state: state.has(ItemName.Scoop_Gem, player))

    add_rule(multiworld.get_entrance(EntranceName.YampiDesertBackToYampiDesertCave, player),
             lambda state: state.has(ItemName.Sand, player)  and state.has(ItemName.Teleport_Lapis, player) and state.has(ItemName.Burst_Brooch, player))

    add_rule(multiworld.get_entrance(EntranceName.AlhafraToAlhafraCave, player),
             lambda state: (state.has(ItemName.Briggs_defeated, player) and state.has(ItemName.Tremor_Bit, player)) or state.has(ItemName.Briggs_escaped, player))

    add_rule(multiworld.get_entrance(EntranceName.GarohToAirsRock, player),
             lambda state: state.has(ItemName.Whirlwind, player))

    add_rule(multiworld.get_entrance(EntranceName.GarohToYampiDesertBack, player),
             lambda state: state.has(ItemName.Sand, player))

    add_rule(multiworld.get_entrance(EntranceName.MadraToGondowanCliffs, player),
             lambda state: state.has(ItemName.Frost_Jewel, player) or state.has(ItemName.Scoop_Gem, player))

    add_rule(multiworld.get_entrance(EntranceName.GondowanCliffsToNaribwe, player),
             lambda state: state.has(ItemName.Briggs_defeated, player))

    add_rule(multiworld.get_entrance(EntranceName.KibomboMountainsToKibombo, player),
             lambda state: state.has(ItemName.Frost_Jewel, player) or state.has(ItemName.Lash_Pebble, player) and state.has(ItemName.Whirlwind, player))

    add_rule(multiworld.get_entrance(EntranceName.KibomboToGabombaStatue, player),
             lambda state: state.has(ItemName.Lash_Pebble, player) and state.has(ItemName.Scoop_Gem, player))

    add_rule(multiworld.get_entrance(EntranceName.GabombaStatueToGabombaCatacombs, player),
             lambda state: state.has(ItemName.Gabomba_Statue_Completed, player) and state.has(ItemName.Cyclone_Chip, player))

    add_rule(multiworld.get_entrance(EntranceName.MadraToEasternSea, player),
             lambda state: state.has(ItemName.Ship, player))

    add_rule(multiworld.get_entrance(EntranceName.SeaOfTimeIsletToIsletCave, player),
             lambda state: state.has(ItemName.Mind_Read, player) and state.has(ItemName.Lil_Turtle, player))

    add_rule(multiworld.get_entrance(EntranceName.SeaOfTimeToLemuria, player),
             lambda state: state.has(ItemName.Poseidon_defeated, player) or state.has(ItemName.Grindstone, player))

    add_rule(multiworld.get_entrance(EntranceName.TreasureIslandToTreasureIsland_Grindstone, player),
             lambda state: state.has(ItemName.Grindstone, player))

    add_rule(multiworld.get_entrance(EntranceName.TreasureIsland_GrindstoneToTreasureIsland_PostReunion, player),
             lambda state: state.has(ItemName.Lifting_Gem, player))

    add_rule(multiworld.get_entrance(EntranceName.AnkohlRuinsToAnkohlRuins_Sand, player),
             lambda state: state.has(ItemName.Sand, player))
    add_rule(multiworld.get_entrance(EntranceName.EasternSeaToAquaRock, player),
             lambda state: state.has(ItemName.Douse_Drop, player))

    add_rule(multiworld.get_entrance(EntranceName.TundariaTowerToTundariaTower_Parched, player),
             lambda state: state.has(ItemName.Parch, player))

    add_rule(multiworld.get_entrance(EntranceName.EasternSeaToWesternSea, player),
             lambda state: state.has(ItemName.Grindstone, player))

    add_rule(multiworld.get_entrance(EntranceName.WesternSeaToMagmaRock, player),
             lambda state: state.has(ItemName.Lifting_Gem, player))
    add_rule(multiworld.get_entrance(EntranceName.MagmaRockToMagmaRockInterior, player),
             lambda state: state.has(ItemName.Burst_Brooch, player) and state.has(ItemName.Growth, player) and state.has(ItemName.Lash_Pebble, player))

    add_rule(multiworld.get_entrance(EntranceName.ContigoToAnemosInnerSanctum, player),
             lambda state: state.has(ItemName.Teleport_Lapis, player) and state.count_group(ItemType.Djinn.name, player) >= 72)

    add_rule(multiworld.get_entrance(EntranceName.ContigoToJupiterLighthouse, player),
             lambda state: state.has(ItemName.Cyclone_Chip, player))

    add_rule(multiworld.get_entrance(EntranceName.ContigoToReunion, player),
             lambda state: state.has(ItemName.Jupiter_Beacon_Lit, player))

    add_rule(multiworld.get_entrance(EntranceName.ShamanVillageCaveToShamanVillage, player),
             lambda state: state.has(ItemName.Whirlwind, player))

    add_rule(multiworld.get_entrance(EntranceName.WesternSeaToProx, player),
             lambda state: state.has(ItemName.Magma_Ball, player))
    add_rule(multiworld.get_entrance(EntranceName.MarsLighthouseToMarsLighthouse_Activated, player),
            lambda state: state.has(ItemName.Flame_Dragons_defeated, player) and state.has(ItemName.Mythril_Bag_Mars, player))

def set_access_rules(world: 'GSTLAWorld'):
    multiworld = world.multiworld
    player = world.player
    #Character locations
    add_rule(multiworld.get_location(LocationName.Idejima_Mind_Read, player),
             lambda state: state.has(ItemName.Sheba, player))
    add_rule(multiworld.get_location(LocationName.Idejima_Whirlwind, player),
             lambda state: state.has(ItemName.Sheba, player))

    add_rule(multiworld.get_location(LocationName.Kibombo_Douse_Drop, player),
             lambda state: state.has(ItemName.Piers, player))
    add_rule(multiworld.get_location(LocationName.Kibombo_Frost_Jewel, player),
             lambda state: state.has(ItemName.Piers, player))
    
    
    add_rule(multiworld.get_location(LocationName.Contigo_Carry_Stone, player),
             lambda state: state.has(ItemName.Mia, player))
    add_rule(multiworld.get_location(LocationName.Contigo_Lifting_Gem, player),
             lambda state: state.has(ItemName.Ivan, player))
    add_rule(multiworld.get_location(LocationName.Contigo_Orb_of_Force, player),
             lambda state: state.has(ItemName.Garet, player))
    add_rule(multiworld.get_location(LocationName.Contigo_Catch_Beads, player),
             lambda state: state.has(ItemName.Isaac, player))
    
    #Character djinn
    if world.options.character_shuffle == 2:
        add_rule(multiworld.get_location(LocationName.Spring, player),
                lambda state: state.has(ItemName.Piers, player))
        add_rule(multiworld.get_location(LocationName.Shade, player),
                lambda state: state.has(ItemName.Piers, player))

        add_rule(multiworld.get_location(LocationName.Flint, player),
                lambda state: state.has(ItemName.Isaac, player))
        add_rule(multiworld.get_location(LocationName.Forge, player),
                lambda state: state.has(ItemName.Isaac, player))  
        add_rule(multiworld.get_location(LocationName.Gust, player),
                lambda state: state.has(ItemName.Isaac, player))
        add_rule(multiworld.get_location(LocationName.Granite, player),
                lambda state: state.has(ItemName.Isaac, player))
        add_rule(multiworld.get_location(LocationName.Fizz, player),
                lambda state: state.has(ItemName.Isaac, player))
        add_rule(multiworld.get_location(LocationName.Fever, player),
                lambda state: state.has(ItemName.Isaac, player))
        
        add_rule(multiworld.get_location(LocationName.Breeze, player),
                lambda state: state.has(ItemName.Garet, player))
        add_rule(multiworld.get_location(LocationName.Sleet, player),
                lambda state: state.has(ItemName.Garet, player))
        add_rule(multiworld.get_location(LocationName.Quartz, player),
                lambda state: state.has(ItemName.Garet, player))
        add_rule(multiworld.get_location(LocationName.Mist, player),
                lambda state: state.has(ItemName.Garet, player))
        add_rule(multiworld.get_location(LocationName.Corona, player),
                lambda state: state.has(ItemName.Garet, player))
        add_rule(multiworld.get_location(LocationName.Zephyr, player),
                lambda state: state.has(ItemName.Garet, player))
        
        add_rule(multiworld.get_location(LocationName.Vine, player),
                lambda state: state.has(ItemName.Ivan, player))
        add_rule(multiworld.get_location(LocationName.Spritz, player),
                lambda state: state.has(ItemName.Ivan, player))
        add_rule(multiworld.get_location(LocationName.Scorch, player),
                lambda state: state.has(ItemName.Ivan, player))
        add_rule(multiworld.get_location(LocationName.Smog, player),
                lambda state: state.has(ItemName.Ivan, player))
        add_rule(multiworld.get_location(LocationName.Sap, player),
                lambda state: state.has(ItemName.Ivan, player))
        add_rule(multiworld.get_location(LocationName.Hail, player),
                lambda state: state.has(ItemName.Ivan, player))
        

        add_rule(multiworld.get_location(LocationName.Ember, player),
                lambda state: state.has(ItemName.Mia, player))
        add_rule(multiworld.get_location(LocationName.Kite, player),
                lambda state: state.has(ItemName.Mia, player))
        add_rule(multiworld.get_location(LocationName.Ground, player),
                lambda state: state.has(ItemName.Mia, player))
        add_rule(multiworld.get_location(LocationName.Tonic, player),
                lambda state: state.has(ItemName.Mia, player))
        add_rule(multiworld.get_location(LocationName.Flash, player),
                lambda state: state.has(ItemName.Mia, player))
        add_rule(multiworld.get_location(LocationName.Squall, player),
                lambda state: state.has(ItemName.Mia, player))
    else:
        add_rule(multiworld.get_location(LocationName.Spring, player),
                lambda state: state.count_group(ItemType.Character.name, player) >= 2)
        add_rule(multiworld.get_location(LocationName.Shade, player),
                lambda state: state.count_group(ItemType.Character.name, player) >= 2)

        add_rule(multiworld.get_location(LocationName.Flint, player),
                lambda state: state.count_group(ItemType.Character.name, player) >= 3)
        add_rule(multiworld.get_location(LocationName.Forge, player),
                lambda state: state.count_group(ItemType.Character.name, player) >= 3)  
        add_rule(multiworld.get_location(LocationName.Gust, player),
                lambda state: state.count_group(ItemType.Character.name, player) >= 3)


        add_rule(multiworld.get_location(LocationName.Granite, player),
                lambda state: state.count_group(ItemType.Character.name, player) >= 4)
        add_rule(multiworld.get_location(LocationName.Fizz, player),
                lambda state: state.count_group(ItemType.Character.name, player) >= 4)
        add_rule(multiworld.get_location(LocationName.Fever, player),
                lambda state: state.count_group(ItemType.Character.name, player) >= 4)
        add_rule(multiworld.get_location(LocationName.Breeze, player),
                lambda state: state.count_group(ItemType.Character.name, player) >= 4)
        
        add_rule(multiworld.get_location(LocationName.Sleet, player),
                lambda state: state.count_group(ItemType.Character.name, player) >= 5)
        add_rule(multiworld.get_location(LocationName.Quartz, player),
                lambda state: state.count_group(ItemType.Character.name, player) >= 5)
        add_rule(multiworld.get_location(LocationName.Mist, player),
                lambda state: state.count_group(ItemType.Character.name, player) >= 5)
        add_rule(multiworld.get_location(LocationName.Corona, player),
                lambda state: state.count_group(ItemType.Character.name, player) >= 5)
        add_rule(multiworld.get_location(LocationName.Zephyr, player),
                lambda state: state.count_group(ItemType.Character.name, player) >= 5)
        
        add_rule(multiworld.get_location(LocationName.Vine, player),
                lambda state: state.count_group(ItemType.Character.name, player) >= 6)
        add_rule(multiworld.get_location(LocationName.Spritz, player),
                lambda state: state.count_group(ItemType.Character.name, player) >= 6)
        add_rule(multiworld.get_location(LocationName.Scorch, player),
                lambda state: state.count_group(ItemType.Character.name, player) >= 6)
        add_rule(multiworld.get_location(LocationName.Smog, player),
                lambda state: state.count_group(ItemType.Character.name, player) >= 6)
        add_rule(multiworld.get_location(LocationName.Sap, player),
                lambda state: state.count_group(ItemType.Character.name, player) >= 6)
        add_rule(multiworld.get_location(LocationName.Hail, player),
                lambda state: state.count_group(ItemType.Character.name, player) >= 6)
        

        add_rule(multiworld.get_location(LocationName.Ember, player),
                lambda state: state.count_group(ItemType.Character.name, player) >= 7)
        add_rule(multiworld.get_location(LocationName.Kite, player),
                lambda state: state.count_group(ItemType.Character.name, player) >= 7)
        add_rule(multiworld.get_location(LocationName.Ground, player),
                lambda state: state.count_group(ItemType.Character.name, player) >= 7)
        add_rule(multiworld.get_location(LocationName.Tonic, player),
                lambda state: state.count_group(ItemType.Character.name, player) >= 7)
        add_rule(multiworld.get_location(LocationName.Flash, player),
                lambda state: state.count_group(ItemType.Character.name, player) >= 7)
        add_rule(multiworld.get_location(LocationName.Squall, player),
                lambda state: state.count_group(ItemType.Character.name, player) >= 7)


    #Daila
    add_rule(multiworld.get_location(LocationName.Daila_Sea_Gods_Tear, player),
             lambda state: state.has(ItemName.Frost_Jewel, player))

    add_rule(multiworld.get_location(LocationName.Daila_Psy_Crystal, player),
             lambda state: state.has(ItemName.Scoop_Gem, player))

    #Kandorean Temple
    add_rule(multiworld.get_location(LocationName.Fog, player),
             lambda state: state.has(ItemName.Lash_Pebble, player))

    #Dehkan Platea
    add_rule(multiworld.get_location(LocationName.Cannon, player),
             lambda state: state.has(ItemName.Pound_Cube, player))

    add_rule(multiworld.get_location(LocationName.Dehkan_Plateau_Nut, player),
             lambda state: state.has(ItemName.Lash_Pebble, player))

    #Shrine of the Sea God
    add_rule(multiworld.get_location(LocationName.Shrine_of_the_Sea_God_Rusty_Staff, player),
             lambda state: state.has(ItemName.Frost_Jewel, player))

    add_rule(multiworld.get_location(LocationName.Shrine_of_the_Sea_God_Right_Prong, player),
             lambda state: state.has(ItemName.Frost_Jewel, player) and state.has(ItemName.Reveal, player))


    #Indra Cavern
    add_rule(multiworld.get_location(LocationName.Indra_Cavern_Zagan, player),
             lambda state: state.has(ItemName.Lash_Pebble, player))

    #Madra
    add_rule(multiworld.get_location(LocationName.Madra_Cyclone_Chip, player),
             lambda state: state.has(ItemName.Gabomba_Statue_Completed, player))

    add_rule(multiworld.get_location(LocationName.Char, player),
             lambda state: state.has(ItemName.Healing_Fungus, player))

    #Madra Catacombs
    add_rule(multiworld.get_location(LocationName.Madra_Catacombs_Ruin_Key, player),
             lambda state: state.has(ItemName.Tremor_Bit, player) and state.has(ItemName.Lash_Pebble, player) and state.has(ItemName.Frost_Jewel, player))

    add_rule(multiworld.get_location(LocationName.Madra_Catacombs_Mist_Potion, player),
             lambda state: state.has(ItemName.Lash_Pebble, player) and state.has(ItemName.Frost_Jewel, player))

    add_rule(multiworld.get_location(LocationName.Madra_Catacombs_Moloch, player),
             lambda state: state.has(ItemName.Ruin_Key, player))

    #Yampi Desert
    add_rule(multiworld.get_location(LocationName.Blitz, player),
             lambda state: state.has(ItemName.Pound_Cube, player))

    add_rule(multiworld.get_location(LocationName.Yampi_Desert_Guardian_Ring, player),
             lambda state: state.has(ItemName.Pound_Cube, player) or state.has(ItemName.Sand, player))

    add_rule(multiworld.get_location(LocationName.Yampi_Desert_Antidote, player),
             lambda state: state.has(ItemName.Pound_Cube, player) or state.has(ItemName.Sand, player))

    add_rule(multiworld.get_location(LocationName.Yampi_Desert_Scoop_Gem, player),
             lambda state: state.has(ItemName.Pound_Cube, player))

    #Yamp Desert Backside
    add_rule(multiworld.get_location(LocationName.Yampi_Desert_Lucky_Medal, player),
             lambda state: state.has(ItemName.Reveal, player))

    add_rule(multiworld.get_location(LocationName.Yampi_Desert_Trainers_Whip, player),
             lambda state: state.has(ItemName.Lash_Pebble, player) or state.has(ItemName.Sand, player))

    add_rule(multiworld.get_location(LocationName.Yampi_Desert_Trainers_Whip, player),
             lambda state: state.has(ItemName.Pound_Cube, player))

    add_rule(multiworld.get_location(LocationName.Yampi_Desert_315_coins, player),
             lambda state: state.has(ItemName.Scoop_Gem, player))

    add_rule(multiworld.get_location(LocationName.Yampi_Desert_Cave_Water_of_Life, player),
             lambda state: state.has(ItemName.Sand, player))

    #Yampi Desert Cave
    add_rule(multiworld.get_location(LocationName.Yampi_Desert_Cave_Mythril_Silver, player),
             lambda state: state.has(ItemName.Scoop_Gem, player))

    add_rule(multiworld.get_location(LocationName.Crystal, player),
             lambda state: state.has(ItemName.Scoop_Gem, player))

    #Alhafra
    add_rule(multiworld.get_location(LocationName.Alhafra_Psy_Crystal, player),
             lambda state: state.has(ItemName.Reveal, player))

    add_rule(multiworld.get_location(LocationName.Alhafra_Prison_Briggs, player),
             lambda state: state.has(ItemName.Briggs_defeated, player) and state.has(ItemName.Lash_Pebble, player) and state.has(ItemName.Burst_Brooch, player) and state.has(ItemName.Pound_Cube, player))

    #Alhafra Cave
    add_rule(multiworld.get_location(LocationName.Alhafran_Cave_123_coins, player),
             lambda state: state.has(ItemName.Lash_Pebble, player) and state.has(ItemName.Pound_Cube, player))

    add_rule(multiworld.get_location(LocationName.Alhafran_Cave_Ixion_Mail, player),
             lambda state: state.has(ItemName.Lash_Pebble, player) and state.has(ItemName.Pound_Cube, player))

    add_rule(multiworld.get_location(LocationName.Alhafran_Cave_Lucky_Medal, player),
             lambda state: state.has(ItemName.Lash_Pebble, player) and state.has(ItemName.Pound_Cube, player))

    add_rule(multiworld.get_location(LocationName.Alhafran_Cave_777_coins, player),
             lambda state: state.has(ItemName.Briggs_escaped, player) and state.has(ItemName.Frost_Jewel, player))

    add_rule(multiworld.get_location(LocationName.Alhafran_Cave_Potion, player),
             lambda state: state.has(ItemName.Briggs_escaped, player) and state.has(ItemName.Frost_Jewel, player))

    add_rule(multiworld.get_location(LocationName.Alhafran_Cave_Psy_Crystal, player),
             lambda state: state.has(ItemName.Briggs_escaped, player) and state.has(ItemName.Frost_Jewel, player))


    #Mikasalla
    add_rule(multiworld.get_location(LocationName.Spark, player),
             lambda state: state.has(ItemName.Scoop_Gem, player))


    #Osenia Cavern
    add_rule(multiworld.get_location(LocationName.Osenia_Cavern_Megaera, player),
             lambda state: state.has(ItemName.Scoop_Gem, player))


    #Garoh
    add_rule(multiworld.get_location(LocationName.Garoh_Hypnos_Sword, player),
             lambda state: state.has(ItemName.Reveal, player))

    add_rule(multiworld.get_location(LocationName.Ether, player),
             lambda state: state.has(ItemName.Reveal, player))


    #Airs Rock
    add_rule(multiworld.get_location(LocationName.Airs_Rock_Vial, player),
             lambda state: state.has(ItemName.Frost_Jewel, player))

    add_rule(multiworld.get_location(LocationName.Airs_Rock_Psy_Crystal, player),
             lambda state: state.has(ItemName.Reveal, player))

    #Gondowan Cliffs
    add_rule(multiworld.get_location(LocationName.Gondowan_Cliffs_Healing_Fungus, player),
             lambda state: state.has(ItemName.Frost_Jewel, player))

    #Naribwe
    add_rule(multiworld.get_location(LocationName.Naribwe_Thorn_Crown, player),
             lambda state: state.has(ItemName.Lash_Pebble, player))

    add_rule(multiworld.get_location(LocationName.Naribwe_Unicorn_Ring, player),
             lambda state: state.has(ItemName.Whirlwind, player) and state.has(ItemName.Reveal, player))

    #Kibombo Mountains
    add_rule(multiworld.get_location(LocationName.Kibombo_Mountains_Power_Bread, player),
             lambda state: state.has(ItemName.Lash_Pebble, player) or state.has(ItemName.Gabomba_Statue_Completed, player))

    add_rule(multiworld.get_location(LocationName.Kibombo_Mountains_Tear_Stone, player),
             lambda state: state.has(ItemName.Lash_Pebble, player) or state.has(ItemName.Gabomba_Statue_Completed, player))

    add_rule(multiworld.get_location(LocationName.Waft, player),
             lambda state: state.has(ItemName.Frost_Jewel, player) and state.has(ItemName.Growth, player))

    #Kibombo
    add_rule(multiworld.get_location(LocationName.Kibombo_Piers, player),
             lambda state: state.has(ItemName.Lash_Pebble, player))


    #Gabomba Statue
    add_rule(multiworld.get_location(LocationName.Gabomba_Statue, player),
             lambda state: state.has(ItemName.Pound_Cube, player))

    add_rule(multiworld.get_location(LocationName.Steel, player),
             lambda state: state.has(ItemName.Pound_Cube, player))

    add_rule(multiworld.get_location(LocationName.Gabomba_Statue_Black_Crystal, player),
             lambda state: state.has(ItemName.Gabomba_Statue_Completed, player))

    #Gabomba Catacombs
    add_rule(multiworld.get_location(LocationName.Gabomba_Catacombs_Tomegathericon, player),
             lambda state: state.has(ItemName.Reveal, player) and state.has(ItemName.Frost_Jewel, player))

    #Lemurian Ship
    if world.options.starter_ship > 0:
        add_rule(multiworld.get_location(LocationName.Lemurian_Ship_Engine_Room, player),
                        lambda state: state.has(ItemName.Aqua_Hydra_defeated, player))
        add_rule(multiworld.get_location(LocationName.Lemurian_Ship_Aqua_Hydra_fight, player), lambda state: state.has(ItemName.Black_Crystal, player))

    add_rule(multiworld.get_location(LocationName.Lemurian_Ship_Potion, player),
             lambda state: state.has(ItemName.Frost_Jewel, player) and (state.has(ItemName.Grindstone, player) or state.has(ItemName.Poseidon_defeated, player)))
    add_rule(multiworld.get_location(LocationName.Lemurian_Ship_Mist_Potion, player),
             lambda state: state.has(ItemName.Aqua_Hydra_defeated, player) and state.has(ItemName.Parch, player) and (state.has(ItemName.Grindstone, player) or state.has(ItemName.Poseidon_defeated, player)))
    add_rule(multiworld.get_location(LocationName.Lemurian_Ship_Aqua_Hydra_fight, player),
             lambda state: state.has(ItemName.Frost_Jewel, player))



    #East Tunderia Islet N/A

    #SouthEast Angara Islet
    add_rule(multiworld.get_location(LocationName.SE_Angara_Islet_Red_Cloth, player),
             lambda state: state.has(ItemName.Pretty_Stone, player) and state.has(ItemName.Frost_Jewel, player) and state.has(ItemName.Mind_Read, player))

    #North Osenia Islet
    add_rule(multiworld.get_location(LocationName.N_Osenia_Islet_Milk, player),
             lambda state: state.has(ItemName.Red_Cloth, player) and state.has(ItemName.Sand, player) and state.has(ItemName.Mind_Read, player))

    #West Indra Islet
    add_rule(multiworld.get_location(LocationName.W_Indra_Islet_Lil_Turtle, player),
             lambda state: state.has(ItemName.Milk, player) and state.has(ItemName.Mind_Read, player))

    #Sea of Time Islet N/A

    #Islet Cave
    add_rule(multiworld.get_location(LocationName.Serac, player),
             lambda state: state.has(ItemName.Teleport_Lapis, player) and state.has(ItemName.Tremor_Bit, player))


    #Apoji Islands
    add_rule(multiworld.get_location(LocationName.Apojii_Islands_Bramble_Seed, player),
             lambda state: state.has(ItemName.Cyclone_Chip, player))

    add_rule(multiworld.get_location(LocationName.Apojii_Islands_Mint, player),
             lambda state: state.has(ItemName.Cyclone_Chip, player))

    add_rule(multiworld.get_location(LocationName.Apojii_Islands_Herb, player),
             lambda state: state.has(ItemName.Cyclone_Chip, player))

    add_rule(multiworld.get_location(LocationName.Haze, player),
             lambda state: state.has(ItemName.Sand, player) and state.has(ItemName.Whirlwind, player))

    #Aqua Rock
    add_rule(multiworld.get_location(LocationName.Aqua_Rock_Parch, player),
             lambda state: state.has(ItemName.Aquarius_Stone, player) and (state.has(ItemName.Parch, player) or state.has(ItemName.Frost_Jewel, player)))

    add_rule(multiworld.get_location(LocationName.Aqua_Rock_Mimic, player),
             lambda state: state.has(ItemName.Parch, player) or state.has(ItemName.Frost_Jewel, player))

    add_rule(multiworld.get_location(LocationName.Aqua_Rock_Mist_Sabre, player),
             lambda state: state.has(ItemName.Frost_Jewel, player))

    add_rule(multiworld.get_location(LocationName.Aqua_Rock_Aquarius_Stone, player),
             lambda state: state.has(ItemName.Parch, player) or state.has(ItemName.Frost_Jewel, player))

    add_rule(multiworld.get_location(LocationName.Aqua_Rock_Lucky_Pepper, player),
             lambda state: state.has(ItemName.Parch, player) or state.has(ItemName.Frost_Jewel, player))

    add_rule(multiworld.get_location(LocationName.Aqua_Rock_Rusty_Sword, player),
             lambda state: state.has(ItemName.Parch, player))

    add_rule(multiworld.get_location(LocationName.Aqua_Rock_Crystal_Powder, player),
             lambda state: state.has(ItemName.Frost_Jewel, player))

    add_rule(multiworld.get_location(LocationName.Aqua_Rock_Vial, player),
             lambda state: state.has(ItemName.Frost_Jewel, player))

    add_rule(multiworld.get_location(LocationName.Aqua_Rock_Tear_Stone, player),
             lambda state: state.has(ItemName.Parch, player) or state.has(ItemName.Frost_Jewel, player))

    add_rule(multiworld.get_location(LocationName.Steam, player),
             lambda state: state.has(ItemName.Parch, player))

    #Izumo
    add_rule(multiworld.get_location(LocationName.Izumo_Ulysses, player),
             lambda state: state.has(ItemName.Reveal, player) and state.has(ItemName.Sand, player) and state.has(ItemName.Frost_Jewel, player) and state.has(ItemName.Pound_Cube, player) and state.has(ItemName.Parch, player))

    add_rule(multiworld.get_location(LocationName.Izumo_Antidote, player),
             lambda state: state.has(ItemName.Cyclone_Chip, player))

    add_rule(multiworld.get_location(LocationName.Izumo_Antidote_Two, player),
             lambda state: state.has(ItemName.Cyclone_Chip, player))

    add_rule(multiworld.get_location(LocationName.Izumo_Lucky_Medal, player),
             lambda state: state.has(ItemName.Cyclone_Chip, player))

    add_rule(multiworld.get_location(LocationName.Izumo_Phantasmal_Mail, player),
             lambda state: state.has(ItemName.Reveal, player) and state.has(ItemName.Sand, player) and state.has(ItemName.Frost_Jewel, player) and state.has(ItemName.Pound_Cube, player))

    add_rule(multiworld.get_location(LocationName.Coal, player),
             lambda state: state.has(ItemName.Dancing_Idol, player) and state.has(ItemName.Serpent_defeated, player))

    #Gaia Rock
    add_rule(multiworld.get_location(LocationName.Gaia_Rock_Sand, player),
             lambda state: state.has(ItemName.Serpent_defeated, player))

    add_rule(multiworld.get_location(LocationName.Gaia_Rock_Cloud_Brand, player),
             lambda state: state.has(ItemName.Sand, player) and state.has(ItemName.Serpent_defeated, player))

    add_rule(multiworld.get_location(LocationName.Gaia_Rock_Mimic, player),
             lambda state: state.has(ItemName.Growth, player))

    add_rule(multiworld.get_location(LocationName.Gaia_Rock_Rusty_Mace, player),
             lambda state: state.has(ItemName.Growth, player))

    add_rule(multiworld.get_location(LocationName.Gaia_Rock_Dancing_Idol, player),
             lambda state: state.has(ItemName.Reveal, player) and state.has(ItemName.Whirlwind, player))

    add_rule(multiworld.get_location(LocationName.Gaia_Rock_Apple, player),
             lambda state: state.has(ItemName.Whirlwind, player))

    add_rule(multiworld.get_location(LocationName.Gaia_Rock_Serpent_Fight, player),
             lambda state: state.has(ItemName.Cyclone_Chip, player) and state.has(ItemName.Dancing_Idol, player))


    #Tundaria Tower
    add_rule(multiworld.get_location(LocationName.Tundaria_Tower_Center_Prong, player),
             lambda state: state.has(ItemName.Burst_Brooch, player))

    add_rule(multiworld.get_location(LocationName.Tundaria_Tower_Burst_Brooch, player),
             lambda state: state.has(ItemName.Pound_Cube, player) and state.has(ItemName.Reveal, player))

    add_rule(multiworld.get_location(LocationName.Tundaria_Tower_Sylph_Feather, player),
             lambda state: state.has(ItemName.Burst_Brooch, player))

    add_rule(multiworld.get_location(LocationName.Tundaria_Tower_Lucky_Medal, player),
             lambda state: state.has(ItemName.Burst_Brooch, player))

    add_rule(multiworld.get_location(LocationName.Tundaria_Tower_Vial, player),
             lambda state: state.has(ItemName.Burst_Brooch, player))

    add_rule(multiworld.get_location(LocationName.Tundaria_Tower_Lightning_Sword, player),
             lambda state: state.has(ItemName.Burst_Brooch, player))

    add_rule(multiworld.get_location(LocationName.Tundaria_Tower_Hard_Nut, player),
             lambda state: state.has(ItemName.Pound_Cube, player))

    add_rule(multiworld.get_location(LocationName.Tundaria_Tower_Crystal_Powder, player),
             lambda state: state.has(ItemName.Pound_Cube, player))

    #Ankohl Ruins
    add_rule(multiworld.get_location(LocationName.Ankohl_Ruins_Left_Prong, player),
             lambda state: state.has(ItemName.Reveal, player))

    #Champa
    add_rule(multiworld.get_location(LocationName.Champa_Trident, player),
             lambda state: state.has(ItemName.Reveal, player) and state.has(ItemName.Briggs_escaped, player) and state.has(ItemName.Left_Prong, player)
                           and state.has(ItemName.Center_Prong, player) and state.has(ItemName.Right_Prong, player))

    add_rule(multiworld.get_location(LocationName.Champa_Viking_Helm, player),
             lambda state: state.has(ItemName.Reveal, player))

    #Yallam
    add_rule(multiworld.get_location(LocationName.Yallam_Nut, player),
             lambda state: state.has(ItemName.Cyclone_Chip, player))

    add_rule(multiworld.get_location(LocationName.Yallam_Antidote, player),
             lambda state: state.has(ItemName.Cyclone_Chip, player))

    add_rule(multiworld.get_location(LocationName.Yallam_Masamune, player),
             lambda state: state.has(ItemName.Cyclone_Chip, player) and state.has(ItemName.Orb_of_Force, player))

    #Taopo Swamp
    add_rule(multiworld.get_location(LocationName.Taopo_Swamp_Tear_Stone, player),
             lambda state: state.has(ItemName.Whirlwind, player) and state.has(ItemName.Scoop_Gem, player))

    add_rule(multiworld.get_location(LocationName.Taopo_Swamp_Tear_Stone_Two, player),
             lambda state: state.has(ItemName.Whirlwind, player) and state.has(ItemName.Scoop_Gem, player))

    add_rule(multiworld.get_location(LocationName.Taopo_Swamp_Vial, player),
             lambda state: state.has(ItemName.Whirlwind, player) and state.has(ItemName.Growth, player) and state.has(ItemName.Douse_Drop, player) and state.has(ItemName.Frost_Jewel, player))

    add_rule(multiworld.get_location(LocationName.Taopo_Swamp_Star_Dust, player),
             lambda state: state.has(ItemName.Whirlwind, player) and state.has(ItemName.Growth, player) and state.has(ItemName.Douse_Drop, player) and state.has(ItemName.Frost_Jewel, player) and state.has(ItemName.Tremor_Bit, player) and state.has(ItemName.Scoop_Gem, player))

    add_rule(multiworld.get_location(LocationName.Taopo_Swamp_Bramble_Seed, player),
             lambda state: state.has(ItemName.Whirlwind, player) and state.has(ItemName.Cyclone_Chip, player))


    #Sea Of Time
    add_rule(multiworld.get_location(LocationName.Sea_of_Time_Poseidon_fight, player),
             lambda state: state.has(ItemName.Trident, player))


    #Lemuria
    add_rule(multiworld.get_location(LocationName.Lemuria_Lucky_Medal, player),
             lambda state: state.has(ItemName.Scoop_Gem, player))

    add_rule(multiworld.get_location(LocationName.Lemuria_Rusty_Sword, player),
             lambda state: state.has(ItemName.Scoop_Gem, player))

    add_rule(multiworld.get_location(LocationName.Lemuria_Hard_Nut, player),
             lambda state: state.has(ItemName.Growth, player) and state.has(ItemName.Cyclone_Chip, player))

    add_rule(multiworld.get_location(LocationName.Lemuria_Bone, player),
             lambda state: state.has(ItemName.Scoop_Gem, player))

    add_rule(multiworld.get_location(LocationName.Lemuria_Star_Dust, player),
             lambda state: state.has(ItemName.Scoop_Gem, player))

    add_rule(multiworld.get_location(LocationName.Rime, player),
             lambda state: state.has(ItemName.Grindstone, player) and state.has(ItemName.Cyclone_Chip, player) and state.has(ItemName.Tremor_Bit, player))

    #Western Sea
    add_rule(multiworld.get_location(LocationName.Overworld_Rusty_Sword_Two, player),
             lambda state: state.has(ItemName.Jupiter_Beacon_Lit, player))

    #SW Atteka Islet
    add_rule(multiworld.get_location(LocationName.Luff, player),
             lambda state: state.has(ItemName.Lifting_Gem, player))

    #Hesperia Settlement
    add_rule(multiworld.get_location(LocationName.Hesperia_Settlement_166_coins, player),
             lambda state: state.has(ItemName.Growth, player))

    add_rule(multiworld.get_location(LocationName.Tinder, player),
             lambda state: state.has(ItemName.Growth, player))

    #Shaman Village Cave
    add_rule(multiworld.get_location(LocationName.Eddy, player),
             lambda state: state.has(ItemName.Whirlwind, player) and state.has(ItemName.Lifting_Gem, player) and state.has(ItemName.Frost_Jewel, player))

    #Shaman Village
    add_rule(multiworld.get_location(LocationName.Shaman_Village_Hover_Jade, player),
             lambda state: state.has(ItemName.Moapa_defeated, player))

    add_rule(multiworld.get_location(LocationName.Shaman_Village_Hard_Nut, player),
             lambda state: state.has(ItemName.Shamans_Rod, player))

    add_rule(multiworld.get_location(LocationName.Shaman_Village_Spirit_Gloves, player),
             lambda state: state.has(ItemName.Growth, player))

    add_rule(multiworld.get_location(LocationName.Shaman_Village_Weasels_Claw, player),
             lambda state: state.has(ItemName.Shamans_Rod, player))

    add_rule(multiworld.get_location(LocationName.Aroma, player),
             lambda state: state.has(ItemName.Moapa_defeated, player) and state.has(ItemName.Lash_Pebble, player))

    add_rule(multiworld.get_location(LocationName.Gasp, player),
             lambda state: state.has(ItemName.Shamans_Rod, player) and state.has(ItemName.Whirlwind, player) and state.has(ItemName.Hover_Jade, player) and state.has(ItemName.Lifting_Gem, player) and state.has(ItemName.Reveal, player))

    add_rule(multiworld.get_location(LocationName.Shaman_Village_Moapa_fight, player),
             lambda state: state.has(ItemName.Shamans_Rod, player))

    #Atteka Inlet
    add_rule(multiworld.get_location(LocationName.Geode, player),
             lambda state: state.has(ItemName.Cyclone_Chip, player) and state.has(ItemName.Lifting_Gem, player))

    #Contigo
    add_rule(multiworld.get_location(LocationName.Contigo_Dragon_Skin, player),
             lambda state: state.has(ItemName.Reveal, player))

    add_rule(multiworld.get_location(LocationName.Contigo_Bramble_Seed, player),
             lambda state: state.has(ItemName.Cyclone_Chip, player))

    add_rule(multiworld.get_location(LocationName.Salt, player),
             lambda state: state.has(ItemName.Scoop_Gem, player))

    add_rule(multiworld.get_location(LocationName.Shine, player),
             lambda state: state.has(ItemName.Orb_of_Force, player))


    #Jupiter Lighthouse
    add_rule(multiworld.get_location(LocationName.Jupiter_Lighthouse_Mimic, player),
             lambda state: state.has(ItemName.Hover_Jade, player) and state.has(ItemName.Red_Key, player))

    add_rule(multiworld.get_location(LocationName.Jupiter_Lighthouse_Erinyes_Tunic, player),
             lambda state: state.has(ItemName.Hover_Jade, player))

    add_rule(multiworld.get_location(LocationName.Jupiter_Lighthouse_Potion, player),
             lambda state: state.has(ItemName.Hover_Jade, player) and state.has(ItemName.Reveal, player))

    add_rule(multiworld.get_location(LocationName.Jupiter_Lighthouse_Psy_Crystal, player),
             lambda state: state.has(ItemName.Hover_Jade, player) and state.has(ItemName.Reveal, player))

    add_rule(multiworld.get_location(LocationName.Jupiter_Lighthouse_Meditation_Rod, player),
             lambda state: state.has(ItemName.Hover_Jade, player) and state.has(ItemName.Reveal, player))

    add_rule(multiworld.get_location(LocationName.Jupiter_Lighthouse_Red_Key, player),
             lambda state: state.has(ItemName.Hover_Jade, player) and state.has(ItemName.Reveal, player))

    add_rule(multiworld.get_location(LocationName.Jupiter_Lighthouse_Blue_Key, player),
             lambda state: state.has(ItemName.Hover_Jade, player) and state.has(ItemName.Red_Key, player))

    add_rule(multiworld.get_location(LocationName.Jupiter_Lighthouse_Mist_Potion, player),
             lambda state: state.has(ItemName.Hover_Jade, player) and state.has(ItemName.Red_Key, player))

    add_rule(multiworld.get_location(LocationName.Jupiter_Lighthouse_306_coins, player),
             lambda state: state.has(ItemName.Hover_Jade, player) and state.has(ItemName.Red_Key, player))

    add_rule(multiworld.get_location(LocationName.Jupiter_Lighthouse_Water_of_Life, player),
             lambda state: state.has(ItemName.Hover_Jade, player) and state.has(ItemName.Reveal, player) and state.has(ItemName.Pound_Cube, player) and state.has(ItemName.Blue_Key, player))

    add_rule(multiworld.get_location(LocationName.Jupiter_Lighthouse_Phaetons_Blade, player),
             lambda state: state.has(ItemName.Hover_Jade, player) and state.has(ItemName.Reveal, player) and state.has(ItemName.Pound_Cube, player) and state.has(ItemName.Blue_Key, player))

    add_rule(multiworld.get_location(LocationName.Whorl, player),
             lambda state: state.has(ItemName.Hover_Jade, player) and state.has(ItemName.Reveal, player) and state.has(ItemName.Pound_Cube, player) and state.has(ItemName.Blue_Key, player))

    add_rule(multiworld.get_location(LocationName.Jupiter_Lighthouse_Aeri_Agatio_and_Karst_fight, player),
             lambda state: state.has(ItemName.Hover_Jade, player) and state.has(ItemName.Reveal, player) and state.has(ItemName.Pound_Cube, player) and state.has(ItemName.Blue_Key, player) and state.has(ItemName.Red_Key, player))

    #Atteka Cavern
    add_rule(multiworld.get_location(LocationName.Atteka_Cavern_Coatlicue, player),
             lambda state: state.has(ItemName.Parch, player))


    #Gondowan Settlement
    add_rule(multiworld.get_location(LocationName.Gondowan_Settlement_Star_Dust, player),
             lambda state: state.has(ItemName.Cyclone_Chip, player))

    #Magma Rock
    add_rule(multiworld.get_location(LocationName.Magma_Rock_Oil_Drop, player),
             lambda state: state.has(ItemName.Burst_Brooch, player))

    add_rule(multiworld.get_location(LocationName.Magma_Rock_383_coins, player),
             lambda state: state.has(ItemName.Burst_Brooch, player) and state.has(ItemName.Growth, player))

    add_rule(multiworld.get_location(LocationName.Magma_Rock_Salamander_Tail, player),
             lambda state: state.has(ItemName.Burst_Brooch, player) and state.has(ItemName.Growth, player) and state.has(ItemName.Lash_Pebble, player))

    #Magma Rock Interior
    add_rule(multiworld.get_location(LocationName.Magma_Rock_Magma_Ball, player),
             lambda state: state.has(ItemName.Whirlwind, player) and state.has(ItemName.Blaze, player))

    add_rule(multiworld.get_location(LocationName.Magma_Rock_Blaze, player),
             lambda state: state.has(ItemName.Whirlwind, player))

    add_rule(multiworld.get_location(LocationName.Magma_Rock_Salamander_Tail_Two, player),
             lambda state: state.has(ItemName.Whirlwind, player))

    add_rule(multiworld.get_location(LocationName.Magma_Rock_Golem_Core, player),
             lambda state: state.has(ItemName.Whirlwind, player))

    #Loho
    add_rule(multiworld.get_location(LocationName.Loho_Mythril_Silver, player),
             lambda state: state.has(ItemName.Magma_Ball, player) and state.has(ItemName.Scoop_Gem, player))
    add_rule(multiworld.get_location(LocationName.Loho_Golem_Core, player),
             lambda state: state.has(ItemName.Magma_Ball, player) and state.has(ItemName.Scoop_Gem, player))
    add_rule(multiworld.get_location(LocationName.Loho_Golem_Core_Two, player),
             lambda state: state.has(ItemName.Magma_Ball, player) and state.has(ItemName.Scoop_Gem, player) and state.has(ItemName.Lifting_Gem, player))
    add_rule(multiworld.get_location(LocationName.Lull, player),
             lambda state: state.has(ItemName.Magma_Ball, player))

    #Angara Cavern
    add_rule(multiworld.get_location(LocationName.Angara_Cavern_Haures, player),
             lambda state: state.has(ItemName.Carry_Stone, player))

    #Kalt Island
    add_rule(multiworld.get_location(LocationName.Gel, player),
             lambda state: state.has(ItemName.Lash_Pebble, player))

    #Prox
    add_rule(multiworld.get_location(LocationName.Prox_Dark_Matter, player),
             lambda state: state.has(ItemName.Scoop_Gem, player) and state.has(ItemName.Lifting_Gem, player))

    add_rule(multiworld.get_location(LocationName.Mold, player),
             lambda state: state.has(ItemName.Scoop_Gem, player))

    #Mars Lighthouse
    add_rule(multiworld.get_location(LocationName.Mars_Lighthouse_Mimic, player),
             lambda state: state.has(ItemName.Pound_Cube, player))

    add_rule(multiworld.get_location(LocationName.Mars_Lighthouse_Teleport_Lapis, player),
             lambda state: state.has(ItemName.Pound_Cube, player) and state.has(ItemName.Burst_Brooch, player) and
                           (state.has(ItemName.Blaze, player) or state.has(ItemName.Teleport_Lapis, player)))

    add_rule(multiworld.get_location(LocationName.Mars_Lighthouse_Mars_Star, player),
             lambda state: state.has(ItemName.Pound_Cube, player) and state.has(ItemName.Burst_Brooch, player) and state.has(ItemName.Blaze, player))

    add_rule(multiworld.get_location(LocationName.Mars_Lighthouse_Mars_Star, player),
             lambda state: state.has(ItemName.Flame_Dragons_defeated, player))

    add_rule(multiworld.get_location(LocationName.Mars_Lighthouse_Orihalcon, player),
             lambda state: state.has(ItemName.Pound_Cube, player) and state.has(ItemName.Burst_Brooch, player) and state.has(ItemName.Blaze, player))

    add_rule(multiworld.get_location(LocationName.Mars_Lighthouse_Valkyrie_Mail, player),
             lambda state: state.has(ItemName.Pound_Cube, player) and state.has(ItemName.Burst_Brooch, player) and state.has(ItemName.Blaze, player) and
                           state.has(ItemName.Reveal, player) and state.has(ItemName.Teleport_Lapis, player))

    add_rule(multiworld.get_location(LocationName.Mars_Lighthouse_Sol_Blade, player),
             lambda state: state.has(ItemName.Pound_Cube, player) and state.has(ItemName.Burst_Brooch, player) and state.has(ItemName.Blaze, player) and
                           state.has(ItemName.Reveal, player) and state.has(ItemName.Teleport_Lapis, player))

    add_rule(multiworld.get_location(LocationName.Mars_Lighthouse_Flame_Dragons_fight, player),
             lambda state: state.has(ItemName.Teleport_Lapis, player) and state.has(ItemName.Pound_Cube, player) and
                           state.has(ItemName.Burst_Brooch, player) and state.has(ItemName.Blaze, player) and state.has(ItemName.Reveal, player))


    #Mars Lighthouse activated

    add_rule(multiworld.get_location(LocationName.Mars_Lighthouse_Psy_Crystal, player),
             lambda state: state.has(ItemName.Cyclone_Chip, player) and state.has(ItemName.Hover_Jade, player))

    add_rule(multiworld.get_location(LocationName.Mars_Lighthouse_Doom_Dragon_Fight, player),
             lambda state: state.has(ItemName.Cyclone_Chip, player) and state.has(ItemName.Hover_Jade, player) and
                           state.has(ItemName.Frost_Jewel, player) and state.has(ItemName.Carry_Stone, player) and state.has(ItemName.Sand, player))

    #djinn logic
    if world.options.djinn_logic > 0:
        djinn_percentage = world.options.djinn_logic / 100

        add_rule(multiworld.get_location(LocationName.Yampi_Desert_Scoop_Gem, player),
                 lambda state: state.count_group(ItemType.Djinn.name, player) >= math.ceil(3 * djinn_percentage))

        add_rule(multiworld.get_location(LocationName.Alhafra_Briggs, player),
                 lambda state: state.count_group(ItemType.Djinn.name, player) >= math.ceil(6 * djinn_percentage))

        add_rule(multiworld.get_location(LocationName.Lemurian_Ship_Aqua_Hydra_fight, player),
                 lambda state: state.count_group(ItemType.Djinn.name, player) >= math.ceil(10 * djinn_percentage))

        add_rule(multiworld.get_location(LocationName.Gaia_Rock_Serpent_Fight, player),
                 lambda state: (state.count_group(ItemType.Djinn.name, player) >= math.ceil(24 * djinn_percentage) or
                                (state.count_group(ItemType.Djinn.name, player) >= math.ceil(16 * djinn_percentage) and state.has(ItemName.Whirlwind, player))))

        add_rule(multiworld.get_location(LocationName.Champa_Trident, player),
                 lambda state: state.count_group(ItemType.Djinn.name, player) >= math.ceil(20 * djinn_percentage))

        add_rule(multiworld.get_location(LocationName.Sea_of_Time_Poseidon_fight, player),
                 lambda state: state.count_group(ItemType.Djinn.name, player) >= math.ceil(24 * djinn_percentage))

        add_rule(multiworld.get_location(LocationName.Shaman_Village_Moapa_fight, player),
                 lambda state: state.count_group(ItemType.Djinn.name, player) >= math.ceil(28 * djinn_percentage))

        add_rule(multiworld.get_location(LocationName.Mars_Lighthouse_Flame_Dragons_fight, player),
                 lambda state: state.count_group(ItemType.Djinn.name, player) >= math.ceil(48 * djinn_percentage))

        add_rule(multiworld.get_location(LocationName.Mars_Lighthouse_Doom_Dragon_Fight, player),
                 lambda state: state.count_group(ItemType.Djinn.name, player) >= math.ceil(56 * djinn_percentage))
    else:
        #Force whirldwind to be able to get all 4 light orbs to make serpent as weak as possible to beat it logically without djinn
        add_rule(multiworld.get_location(LocationName.Gaia_Rock_Serpent_Fight, player),
                 lambda state: state.has(ItemName.Whirlwind, player))

    #Optional Super Boss content
    if world.options.super_bosses > 0:
        add_rule(multiworld.get_location(LocationName.Yampi_Desert_Cave_Daedalus, player),
             lambda state: state.has(ItemName.Pound_Cube, player) and state.count_group(ItemType.Djinn, player) >= 64)

        add_rule(multiworld.get_location(LocationName.Islet_Cave_Catastrophe, player),
             lambda state: state.has(ItemName.Teleport_Lapis, player) and state.count_group(ItemType.Djinn, player) >= 64)

        #Treasure Isle
        add_rule(multiworld.get_location(LocationName.Treasure_Isle_Azul, player), lambda state: state.count_group(ItemType.Djinn, player) >= 64)


    if world.options.super_bosses > 1:
        #Anemos Inner Sanctum
        add_rule(multiworld.get_location(LocationName.Anemos_Inner_Sanctum_Iris, player),
             lambda state: state.has(ItemName.Lifting_Gem, player) and state.has(ItemName.Sand, player) and state.has(ItemName.Hover_Jade, player))

        add_rule(multiworld.get_location(LocationName.Anemos_Inner_Sanctum_Orihalcon, player),
             lambda state: state.has(ItemName.Lifting_Gem, player))


    #Hidden Items
    if world.options.hidden_items < 2:
        add_rule(multiworld.get_location(LocationName.Alhafra_Lucky_Medal, player),
                 lambda state: state.has(ItemName.Briggs_defeated, player))

        add_rule(multiworld.get_location(LocationName.Alhafran_Cave_Power_Bread, player),
                 lambda state: state.has(ItemName.Briggs_escaped, player))

        add_rule(multiworld.get_location(LocationName.Kibombo_Mountains_Smoke_Bomb, player),
                 lambda state: state.has(ItemName.Lash_Pebble, player) or
                               state.has(ItemName.Gabomba_Statue_Completed, player))

        add_rule(multiworld.get_location(LocationName.Kibombo_Lucky_Medal, player),
                 lambda state: state.has(ItemName.Gabomba_Statue_Completed, player))

        add_rule(multiworld.get_location(LocationName.Kibombo_Nut, player),
                 lambda state: state.has(ItemName.Gabomba_Statue_Completed, player))

        add_rule(multiworld.get_location(LocationName.Lemurian_Ship_Antidote, player),
                 lambda state: state.has(ItemName.Frost_Jewel, player) and (
                             state.has(ItemName.Grindstone, player) or state.has(ItemName.Poseidon_defeated, player)))

        add_rule(multiworld.get_location(LocationName.Lemurian_Ship_Oil_Drop, player),
                 lambda state: state.has(ItemName.Frost_Jewel, player) and (
                             state.has(ItemName.Grindstone, player) or state.has(ItemName.Poseidon_defeated, player)))

        add_rule(multiworld.get_location(LocationName.Shaman_Village_Elixir_Two, player),
                 lambda state: state.has(ItemName.Shamans_Rod, player) and state.has(ItemName.Hover_Jade,
                               player) and state.has(ItemName.Lifting_Gem, player) and state.has(ItemName.Whirlwind, player) and state.has(ItemName.Reveal, player))

        add_rule(multiworld.get_location(LocationName.Shaman_Village_Lucky_Medal, player),
                 lambda state: state.has(ItemName.Moapa_defeated, player))

        add_rule(multiworld.get_location(LocationName.Shaman_Village_Lucky_Pepper, player),
                 lambda state: state.has(ItemName.Moapa_defeated, player))

    if world.options.hidden_items == 0:
        for loc in location_type_to_data[LocationType.Hidden]:
            add_rule(multiworld.get_location(loc_names_by_id[loc.ap_id], player),
                 lambda state: state.has(ItemName.Reveal, player))





def set_item_rules(world: 'GSTLAWorld'):
    multiworld = world.multiworld
    player = world.player
    djinn: Set[str] = {item.name for item in all_items if item.type == ItemType.Djinn}

    for loc in location_type_to_data[LocationType.Djinn]:
        add_item_rule(multiworld.get_location(loc_names_by_id[loc.ap_id], player), lambda item: item.player == player and item.name in djinn)

    #TODO: This location is also not allowed to have a mimic
    add_item_rule(multiworld.get_location(LocationName.Airs_Rock_Reveal, player), lambda item: item.player != player or (item.player == player and item.name != ItemName.Empty))
    #TODO: This location is also not allowed to have a mimic
    add_item_rule(multiworld.get_location(LocationName.Aqua_Rock_Parch, player), lambda item: item.player != player or (item.player == player and item.name != ItemName.Empty))
    #TODO: This location is also not allowed to have a mimic
    add_item_rule(multiworld.get_location(LocationName.Magma_Rock_Magma_Ball, player), lambda item: item.player != player or (item.player == player and item.name != ItemName.Empty))
    #TODO: This location is also not allowed to have a mimic
    add_item_rule(multiworld.get_location(LocationName.Magma_Rock_Blaze, player), lambda item: item.player != player or (item.player == player and item.name != ItemName.Empty))
    #TODO: This location is also not allowed to have a mimic
    add_item_rule(multiworld.get_location(LocationName.Gaia_Rock_Sand, player), lambda item: item.player != player or (item.player == player and item.name != ItemName.Empty))
    #TODO: This location is also not allowed to have a mimic
    add_item_rule(multiworld.get_location(LocationName.Gaia_Rock_Dancing_Idol, player), lambda item: item.player != player or (item.player == player and item.name != ItemName.Empty))

    #TODO: This location is also not allowed to have a mimic
    add_item_rule(multiworld.get_location(LocationName.Dehkan_Plateau_Pound_Cube, player), lambda item: item.player != player or (item.player == player and item.name != ItemName.Empty))   
    #TODO: This location is also not allowed to have a mimic
    add_item_rule(multiworld.get_location(LocationName.Kandorean_Temple_Lash_Pebble, player), lambda item: item.player != player or (item.player == player and item.name != ItemName.Empty))
    #TODO: This location is also not allowed to have a mimic
    add_item_rule(multiworld.get_location(LocationName.Madra_Cyclone_Chip, player), lambda item: item.player != player or (item.player == player and item.name != ItemName.Empty))
    #TODO: This location is also not allowed to have a mimic
    add_item_rule(multiworld.get_location(LocationName.Shaman_Village_Hover_Jade, player), lambda item: item.player != player or (item.player == player and item.name != ItemName.Empty))
    #TODO: This location is also not allowed to have a mimic
    add_item_rule(multiworld.get_location(LocationName.Yampi_Desert_Scoop_Gem, player), lambda item: item.player != player or (item.player == player and item.name != ItemName.Empty))

    #TODO: This location is also not allowed to have a mimic
    add_item_rule(multiworld.get_location(LocationName.Champa_Trident, player), lambda item: item.player != player or (item.player == player and item.name != ItemName.Empty))

    character_names = [character.name for character in characters]
    summon_names = [summon.name for summon in summon_list]

    #TODO: This location is also not allowed to have a mimic
    add_item_rule(multiworld.get_location(LocationName.Contigo_Carry_Stone, player), lambda item: item.player != player or (item.player == player and item.name not in summon_names and item.name not in character_names))
    #TODO: This location is also not allowed to have a mimic
    add_item_rule(multiworld.get_location(LocationName.Contigo_Lifting_Gem, player), lambda item: item.player != player or (item.player == player and item.name not in summon_names and item.name not in character_names))
    #TODO: This location is also not allowed to have a mimic
    add_item_rule(multiworld.get_location(LocationName.Contigo_Orb_of_Force, player), lambda item: item.player != player or (item.player == player and item.name not in summon_names and item.name not in character_names))
    #TODO: This location is also not allowed to have a mimic
    add_item_rule(multiworld.get_location(LocationName.Contigo_Catch_Beads, player), lambda item: item.player != player or (item.player == player and item.name not in summon_names and item.name not in character_names))
    #TODO: This location only has no summon flag but it seems odd to me to allow mimics
    add_item_rule(multiworld.get_location(LocationName.Idejima_Shamans_Rod, player), lambda item: item.player != player or (item.player == player and item.name not in summon_names and item.name not in character_names))
    #TODO: This location only has no summon flag but it seems odd to me to allow mimics
    add_item_rule(multiworld.get_location(LocationName.Idejima_Growth, player), lambda item: item.player != player or (item.player == player and item.name not in summon_names and item.name not in character_names))
    #TODO: This location only has no summon flag but it seems odd to me to allow mimics
    add_item_rule(multiworld.get_location(LocationName.Idejima_Whirlwind, player), lambda item: item.player != player or (item.player == player and item.name not in summon_names and item.name not in character_names))
    #TODO: This location only has no summon flag but it seems odd to me to allow mimics
    add_item_rule(multiworld.get_location(LocationName.Idejima_Mind_Read, player), lambda item: item.player != player or (item.player == player and item.name not in summon_names and item.name not in character_names))
    #TODO: This location only has no summon flag but it seems odd to me to allow mimics
    add_item_rule(multiworld.get_location(LocationName.Kibombo_Douse_Drop, player), lambda item: item.player != player or (item.player == player and item.name not in summon_names and item.name not in character_names))
    #TODO: This location only has no summon flag but it seems odd to me to allow mimics
    add_item_rule(multiworld.get_location(LocationName.Kibombo_Frost_Jewel, player), lambda item: item.player != player or (item.player == player and item.name not in summon_names and item.name not in character_names))

    #TODO: This location is also not allowed to have a mimic
    add_item_rule(multiworld.get_location(LocationName.Contigo_Isaac, player), lambda item: item.player != player or (item.player == player and item.name != ItemName.Empty))
    #TODO: This location is also not allowed to have a mimic
    add_item_rule(multiworld.get_location(LocationName.Contigo_Garet, player), lambda item: item.player != player or (item.player == player and item.name != ItemName.Empty))
    #TODO: This location is also not allowed to have a mimic
    add_item_rule(multiworld.get_location(LocationName.Contigo_Ivan, player), lambda item: item.player != player or (item.player == player and item.name != ItemName.Empty))
    #TODO: This location is also not allowed to have a mimic
    add_item_rule(multiworld.get_location(LocationName.Contigo_Mia, player), lambda item: item.player != player or (item.player == player and item.name != ItemName.Empty))
    #TODO: This location is also not allowed to have a mimic
    add_item_rule(multiworld.get_location(LocationName.Idejima_Jenna, player), lambda item: item.player != player or (item.player == player and item.name != ItemName.Empty))
    #TODO: This location is also not allowed to have a mimic
    add_item_rule(multiworld.get_location(LocationName.Idejima_Sheba, player), lambda item: item.player != player or (item.player == player and item.name != ItemName.Empty))
    #TODO: This location is also not allowed to have a mimic
    add_item_rule(multiworld.get_location(LocationName.Kibombo_Piers, player), lambda item: item.player != player or (item.player == player and item.name != ItemName.Empty))


    #TODO: This location is also not allowed to have a mimic
    add_item_rule(multiworld.get_location(LocationName.Daila_Sea_Gods_Tear, player), lambda item: item.player != player or (item.player == player and item.name != ItemName.Empty))
    #TODO: This location is also not allowed to have a mimic
    add_item_rule(multiworld.get_location(LocationName.Gabomba_Catacombs_Tomegathericon, player), lambda item: item.player != player or (item.player == player and item.name != ItemName.Empty))
    #TODO: This location is also not allowed to have a mimic
    add_item_rule(multiworld.get_location(LocationName.Gabomba_Statue_Black_Crystal, player), lambda item: item.player != player or (item.player == player and item.name != ItemName.Empty))
    
    #TODO: This location is not allowed to have a mimic
    #add_item_rule(multiworld.get_location(LocationName.Lemurian_Ship_Mist_Potion, player), lambda item: item.player != player or (item.player == player and item.name != ItemName.Empty))

    #TODO: This location is also not allowed to have a mimic
    add_item_rule(multiworld.get_location(LocationName.Mars_Lighthouse_Mars_Star, player), lambda item: item.player != player or (item.player == player and item.name != ItemName.Empty))

    #TODO: This location is also not allowed to have a mimic
    add_item_rule(multiworld.get_location(LocationName.E_Tundaria_Islet_Pretty_Stone, player), lambda item: item.player != player or (item.player == player and item.name != ItemName.Empty))
    #TODO: This location is also not allowed to have a mimic
    add_item_rule(multiworld.get_location(LocationName.N_Osenia_Islet_Milk, player), lambda item: item.player != player or (item.player == player and item.name != ItemName.Empty))
    #TODO: This location is also not allowed to have a mimic
    add_item_rule(multiworld.get_location(LocationName.SE_Angara_Islet_Red_Cloth, player), lambda item: item.player != player or (item.player == player and item.name != ItemName.Empty))
    #TODO: This location is also not allowed to have a mimic
    add_item_rule(multiworld.get_location(LocationName.W_Indra_Islet_Lil_Turtle, player), lambda item: item.player != player or (item.player == player and item.name != ItemName.Empty))
