import random
import logging
import os
import threading
import typing

from BaseClasses import Item, CollectionState, Tutorial
from .SubClasses import ALttPItem
from ..AutoWorld import World, WebWorld, LogicMixin
from .Options import alttp_options, smallkey_shuffle
from .Items import as_dict_item_table, item_name_groups, item_table, GetBeemizerItem
from .Regions import lookup_name_to_id, create_regions, mark_light_world_regions
from .Rules import set_rules
from .ItemPool import generate_itempool, difficulties
from .Shops import create_shops, ShopSlotFill
from .Dungeons import create_dungeons
from .Rom import LocalRom, patch_rom, patch_race_rom, patch_enemizer, apply_rom_settings, get_hash_string, \
    get_base_rom_path, LttPDeltaPatch
import Patch
from itertools import chain

from .InvertedRegions import create_inverted_regions, mark_dark_world_regions
from .EntranceShuffle import link_entrances, link_inverted_entrances, plando_connect

lttp_logger = logging.getLogger("A Link to the Past")


class ALTTPWeb(WebWorld):
    setup_en = Tutorial(
        "Multiworld Setup Tutorial",
        "A guide to setting up the Archipelago ALttP Software on your computer. This guide covers single-player, multiworld, and related software.",
        "English",
        "multiworld_en.md",
        "multiworld/en",
        ["Farrak Kilhn"]
    )

    setup_de = Tutorial(
        setup_en.tutorial_name,
        setup_en.description,
        "Deutsch",
        "multiworld_de.md",
        "multiworld/de",
        ["Fischfilet"]
    )

    setup_es = Tutorial(
        setup_en.tutorial_name,
        setup_en.description,
        "Español",
        "multiworld_es.md",
        "multiworld/es",
        ["Edos"]
    )

    setup_fr = Tutorial(
        setup_en.tutorial_name,
        setup_en.description,
        "Français",
        "multiworld_fr.md",
        "multiworld/fr",
        ["Coxla"]
    )

    msu = Tutorial(
        "MSU-1 Setup Tutorial",
        "A guide to setting up MSU-1, which allows for custom in-game music.",
        "English",
        "msu1_en.md",
        "msu1/en",
        ["Farrak Kilhn"]
    )

    msu_es = Tutorial(
        msu.tutorial_name,
        msu.description,
        "Español",
        "msu1_es.md",
        "msu1/en",
        ["Edos"]
    )

    msu_fr = Tutorial(
        msu.tutorial_name,
        msu.description,
        "Français",
        "msu1_fr.md",
        "msu1/fr",
        ["Coxla"]
    )

    plando = Tutorial(
        "Plando Tutorial",
        "A guide to creating Multiworld Plandos with LTTP",
        "English",
        "plando_en.md",
        "plando/en",
        ["Berserker"]
    )

    tutorials = [setup_en, setup_de, setup_es, setup_fr, msu, msu_es, msu_fr, plando]

    if typing.TYPE_CHECKING:
        from WebHostLib.tracker import PlayerTracker
    else:
        PlayerTracker = object

    def modify_tracker(self, tracker: PlayerTracker):
        tracker.template = 'zeldaKeysTracker.html'

        tracker.icons = {
            "Blue Shield": r"https://www.zeldadungeon.net/wiki/images/8/85/Fighters-Shield.png",
            "Red Shield": r"https://www.zeldadungeon.net/wiki/images/5/55/Fire-Shield.png",
            "Mirror Shield": r"https://www.zeldadungeon.net/wiki/images/8/84/Mirror-Shield.png",
            "Fighter Sword": r"https://oyster.ignimgs.com/mediawiki/apis.ign.com/the-legend-of-zelda-a-link-to-the-past/4/40/SFighterSword.png?width=1920",
            "Master Sword": r"https://oyster.ignimgs.com/mediawiki/apis.ign.com/the-legend-of-zelda-a-link-to-the-past/6/65/SMasterSword.png?width=1920",
            "Tempered Sword": r"https://oyster.ignimgs.com/mediawiki/apis.ign.com/the-legend-of-zelda-a-link-to-the-past/9/92/STemperedSword.png?width=1920",
            "Golden Sword": r"https://oyster.ignimgs.com/mediawiki/apis.ign.com/the-legend-of-zelda-a-link-to-the-past/2/28/SGoldenSword.png?width=1920",
            "Bow": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/b/bc/ALttP_Bow_%26_Arrows_Sprite.png?version=5f85a70e6366bf473544ef93b274f74c",
            "Silver Bow": r"https://oyster.ignimgs.com/mediawiki/apis.ign.com/the-legend-of-zelda-a-link-to-the-past/6/65/Bow.png?width=1920",
            "Green Mail": r"https://oyster.ignimgs.com/mediawiki/apis.ign.com/the-legend-of-zelda-a-link-to-the-past/c/c9/SGreenTunic.png?width=1920",
            "Blue Mail": r"https://oyster.ignimgs.com/mediawiki/apis.ign.com/the-legend-of-zelda-a-link-to-the-past/9/98/SBlueTunic.png?width=1920",
            "Red Mail": r"https://oyster.ignimgs.com/mediawiki/apis.ign.com/the-legend-of-zelda-a-link-to-the-past/7/74/SRedTunic.png?width=1920",
            "Power Glove": r"https://oyster.ignimgs.com/mediawiki/apis.ign.com/the-legend-of-zelda-a-link-to-the-past/f/f5/SPowerGlove.png?width=1920",
            "Titan Mitts": r"https://oyster.ignimgs.com/mediawiki/apis.ign.com/the-legend-of-zelda-a-link-to-the-past/c/c1/STitanMitt.png?width=1920",
            "Progressive Sword": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/c/cc/ALttP_Master_Sword_Sprite.png?version=55869db2a20e157cd3b5c8f556097725",
            "Pegasus Boots": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/e/ed/ALttP_Pegasus_Shoes_Sprite.png?version=405f42f97240c9dcd2b71ffc4bebc7f9",
            "Progressive Glove": r"https://oyster.ignimgs.com/mediawiki/apis.ign.com/the-legend-of-zelda-a-link-to-the-past/c/c1/STitanMitt.png?width=1920",
            "Flippers": r"https://oyster.ignimgs.com/mediawiki/apis.ign.com/the-legend-of-zelda-a-link-to-the-past/4/4c/ZoraFlippers.png?width=1920",
            "Moon Pearl": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/6/63/ALttP_Moon_Pearl_Sprite.png?version=d601542d5abcc3e006ee163254bea77e",
            "Progressive Bow": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/b/bc/ALttP_Bow_%26_Arrows_Sprite.png?version=cfb7648b3714cccc80e2b17b2adf00ed",
            "Blue Boomerang": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/c/c3/ALttP_Boomerang_Sprite.png?version=96127d163759395eb510b81a556d500e",
            "Red Boomerang": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/b/b9/ALttP_Magical_Boomerang_Sprite.png?version=47cddce7a07bc3e4c2c10727b491f400",
            "Hookshot": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/2/24/Hookshot.png?version=c90bc8e07a52e8090377bd6ef854c18b",
            "Mushroom": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/3/35/ALttP_Mushroom_Sprite.png?version=1f1acb30d71bd96b60a3491e54bbfe59",
            "Magic Powder": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/e/e5/ALttP_Magic_Powder_Sprite.png?version=c24e38effbd4f80496d35830ce8ff4ec",
            "Fire Rod": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/d/d6/FireRod.png?version=6eabc9f24d25697e2c4cd43ddc8207c0",
            "Ice Rod": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/d/d7/ALttP_Ice_Rod_Sprite.png?version=1f944148223d91cfc6a615c92286c3bc",
            "Bombos": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/8/8c/ALttP_Bombos_Medallion_Sprite.png?version=f4d6aba47fb69375e090178f0fc33b26",
            "Ether": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/3/3c/Ether.png?version=34027651a5565fcc5a83189178ab17b5",
            "Quake": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/5/56/ALttP_Quake_Medallion_Sprite.png?version=efd64d451b1831bd59f7b7d6b61b5879",
            "Lamp": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/6/63/ALttP_Lantern_Sprite.png?version=e76eaa1ec509c9a5efb2916698d5a4ce",
            "Hammer": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/d/d1/ALttP_Hammer_Sprite.png?version=e0adec227193818dcaedf587eba34500",
            "Shovel": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/c/c4/ALttP_Shovel_Sprite.png?version=e73d1ce0115c2c70eaca15b014bd6f05",
            "Flute": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/d/db/Flute.png?version=ec4982b31c56da2c0c010905c5c60390",
            "Bug Catching Net": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/5/54/Bug-CatchingNet.png?version=4d40e0ee015b687ff75b333b968d8be6",
            "Book of Mudora": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/2/22/ALttP_Book_of_Mudora_Sprite.png?version=11e4632bba54f6b9bf921df06ac93744",
            "Bottle": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/e/ef/ALttP_Magic_Bottle_Sprite.png?version=fd98ab04db775270cbe79fce0235777b",
            "Cane of Somaria": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/e/e1/ALttP_Cane_of_Somaria_Sprite.png?version=8cc1900dfd887890badffc903bb87943",
            "Cane of Byrna": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/b/bc/ALttP_Cane_of_Byrna_Sprite.png?version=758b607c8cbe2cf1900d42a0b3d0fb54",
            "Cape": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/1/1c/ALttP_Magic_Cape_Sprite.png?version=6b77f0d609aab0c751307fc124736832",
            "Magic Mirror": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/e/e5/ALttP_Magic_Mirror_Sprite.png?version=e035dbc9cbe2a3bd44aa6d047762b0cc",
            "Triforce": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/4/4e/TriforceALttPTitle.png?version=dc398e1293177581c16303e4f9d12a48",
            "Small Key": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/f/f1/ALttP_Small_Key_Sprite.png?version=4f35d92842f0de39d969181eea03774e",
            "Big Key": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/3/33/ALttP_Big_Key_Sprite.png?version=136dfa418ba76c8b4e270f466fc12f4d",
            "Chest": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/7/73/ALttP_Treasure_Chest_Sprite.png?version=5f530ecd98dcb22251e146e8049c0dda",
            "Light World": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/e/e7/ALttP_Soldier_Green_Sprite.png?version=d650d417934cd707a47e496489c268a6",
            "Dark World": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/9/94/ALttP_Moblin_Sprite.png?version=ebf50e33f4657c377d1606bcc0886ddc",
            "Hyrule Castle": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/d/d3/ALttP_Ball_and_Chain_Trooper_Sprite.png?version=1768a87c06d29cc8e7ddd80b9fa516be",
            "Agahnims Tower": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/1/1e/ALttP_Agahnim_Sprite.png?version=365956e61b0c2191eae4eddbe591dab5",
            "Desert Palace": r"https://www.zeldadungeon.net/wiki/images/2/25/Lanmola-ALTTP-Sprite.png",
            "Eastern Palace": r"https://www.zeldadungeon.net/wiki/images/d/dc/RedArmosKnight.png",
            "Tower of Hera": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/3/3c/ALttP_Moldorm_Sprite.png?version=c588257bdc2543468e008a6b30f262a7",
            "Palace of Darkness": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/e/ed/ALttP_Helmasaur_King_Sprite.png?version=ab8a4a1cfd91d4fc43466c56cba30022",
            "Swamp Palace": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/7/73/ALttP_Arrghus_Sprite.png?version=b098be3122e53f751b74f4a5ef9184b5",
            "Skull Woods": r"https://alttp-wiki.net/images/6/6a/Mothula.png",
            "Thieves Town": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/8/86/ALttP_Blind_the_Thief_Sprite.png?version=3833021bfcd112be54e7390679047222",
            "Ice Palace": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/3/33/ALttP_Kholdstare_Sprite.png?version=e5a1b0e8b2298e550d85f90bf97045c0",
            "Misery Mire": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/8/85/ALttP_Vitreous_Sprite.png?version=92b2e9cb0aa63f831760f08041d8d8d8",
            "Turtle Rock": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/9/91/ALttP_Trinexx_Sprite.png?version=0cc867d513952aa03edd155597a0c0be",
            "Ganons Tower": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/b/b9/ALttP_Ganon_Sprite.png?version=956f51f054954dfff53c1a9d4f929c74"
        }

        tracker.regions = {
            'Light World': [
                'Lost Woods Hideout', 'Lumberjack Tree', 'Mushroom', 'Master Sword Pedestal', 'Bottle Merchant', 'Flute Spot',
                'Blind\'s Hideout - Top', 'Blind\'s Hideout - Left', 'Blind\'s Hideout - Right', 'Blind\'s Hideout - Far Left', 'Blind\'s Hideout - Far Right',
                'Link\'s House', 'Link\'s Uncle', 'Secret Passage',
                'King Zora', 'Zora\'s Ledge', 'Waterfall Fairy - Left', 'Waterfall Fairy - Right',
                'King\'s Tomb', 'Graveyard Cave', 'Bonk Rock Cave',
                'Sunken Treasure', 'Floodgate Chest', 'Hobo', 'Ice Rod Cave', 'Lake Hylia Island',
                'Kakariko Tavern', 'Chicken House', 'Sick Kid',
                'Blacksmith', 'Purple Chest', 'Magic Bat',
                'Aginah\'s Cave', 'Cave 45', 'Checkerboard Cave',
                'Sahasrahla\'s Hut - Left', 'Sahasrahla\'s Hut - Middle', 'Sahasrahla\'s Hut - Right', 'Sahasrahla',
                'Kakariko Well - Top', 'Kakariko Well - Left', 'Kakariko Well - Middle', 'Kakariko Well - Right', 'Kakariko Well - Bottom',
                'Mini Moldorm Cave - Far Left', 'Mini Moldorm Cave - Left', 'Mini Moldorm Cave - Right', 'Mini Moldorm Cave - Far Right', 'Mini Moldorm Cave - Generous Guy',
                'Library', 'Maze Race', 'Potion Shop', 'Desert Ledge',
                'Old Man', 'Spectacle Rock',
                'Paradox Cave Lower - Far Left', 'Paradox Cave Lower - Left', 'Paradox Cave Lower - Right', 'Paradox Cave Lower - Far Right', 'Paradox Cave Lower - Middle',
                'Paradox Cave Upper - Left', 'Paradox Cave Upper - Right',
                'Spiral Cave', 'Ether Tablet'
            ],
            'Dark World': [
                'Pyramid', 'Catfish', 'Pyramid Fairy - Left', 'Pyramid Fairy - Right',
                'Stumpy', 'Digging Game',
                'Bombos Tablet',
                'Hype Cave - Top', 'Hype Cave - Middle Right', 'Hype Cave - Middle Left', 'Hype Cave - Bottom', 'Hype Cave - Generous Guy',
                'Peg Cave', 'Brewery', 'C-Shaped House', 'Chest Game',
                'Bumper Cave Ledge',
                'Mire Shed - Left', 'Mire Shed - Right',
                'Superbunny Cave - Top', 'Superbunny Cave - Bottom',
                'Spike Cave', 'Floating Island', 'Mimic Cave',
                'Hookshot Cave - Top Right', 'Hookshot Cave - Top Left', 'Hookshot Cave - Bottom Right', 'Hookshot Cave - Bottom Left',

            ],
            'Desert Palace': [
                'Desert Palace - Big Chest', 'Desert Palace - Torch', 'Desert Palace - Map Chest',
                'Desert Palace - Compass Chest', 'Desert Palace - Big Key Chest',
                'Desert Palace - Boss'
            ],
            'Eastern Palace': [
                'Eastern Palace - Compass Chest', 'Eastern Palace - Big Chest', 'Eastern Palace - Cannonball Chest',
                'Eastern Palace - Big Key Chest', 'Eastern Palace - Map Chest', 'Eastern Palace - Boss'
            ],
            'Hyrule Castle': [
                'Hyrule Castle - Map Chest', 'Hyrule Castle - Boomerang Chest', 'Hyrule Castle - Zelda\'s Chest',
                'Sewers - Dark Cross', 'Sewers - Secret Room - Left', 'Sewers - Secret Room - Middle', 'Sewers - Secret Room - Right',
                'Sanctuary'
            ],
            'Agahnims Tower': [
                'Castle Tower - Room 03', 'Castle Tower - Dark Maze'
            ],
            'Tower of Hera': [
                'Tower of Hera - Basement Cage', 'Tower of Hera - Map Chest', 'Tower of Hera - Big Key Chest',
                'Tower of Hera - Compass Chest', 'Tower of Hera - Big Chest', 'Tower of Hera - Boss'
            ],
            'Swamp Palace': [
                'Swamp Palace - Entrance', 'Swamp Palace - Map Chest',
                'Swamp Palace - Big Chest', 'Swamp Palace - Compass Chest',
                'Swamp Palace - Big Key Chest', 'Swamp Palace - West Chest',
                'Swamp Palace - Flooded Room - Left', 'Swamp Palace - Flooded Room - Right',
                'Swamp Palace - Waterfall Room', 'Swamp Palace - Boss'
            ],
            'Thieves Town': [
                'Thieves\' Town - Big Key Chest', 'Thieves\' Town - Map Chest', 'Thieves\' Town - Compass Chest', 'Thieves\' Town - Ambush Chest',
                'Thieves\' Town - Attic', 'Thieves\' Town - Big Chest', 'Thieves\' Town - Blind\'s Cell', 'Thieves\' Town - Boss'
            ],
            'Skull Woods': [
                'Skull Woods - Map Chest', 'Skull Woods - Pinball Room',
                'Skull Woods - Compass Chest', 'Skull Woods - Pot Prison',
                'Skull Woods - Big Chest',
                'Skull Woods - Big Key Chest',
                'Skull Woods - Bridge Room', 'Skull Woods - Boss'
            ],
            'Ice Palace': [
                'Ice Palace - Compass Chest', 'Ice Palace - Freezor Chest', 'Ice Palace - Big Chest', 'Ice Palace - Iced T Room',
                'Ice Palace - Spike Room', 'Ice Palace - Big Key Chest', 'Ice Palace - Map Chest', 'Ice Palace - Boss'
            ],
            'Misery Mire': [
                'Misery Mire - Big Chest', 'Misery Mire - Map Chest', 'Misery Mire - Main Lobby', 'Misery Mire - Bridge Chest', 'Misery Mire - Spike Chest',
                'Misery Mire - Compass Chest', 'Misery Mire - Big Key Chest', 'Misery Mire - Boss'
            ],
            'Turtle Rock': [
                'Turtle Rock - Compass Chest', 'Turtle Rock - Roller Room - Left', 'Turtle Rock - Roller Room - Right',
                'Turtle Rock - Chain Chomps', 'Turtle Rock - Big Key Chest', 'Turtle Rock - Big Chest',
                'Turtle Rock - Crystaroller Room',
                'Turtle Rock - Eye Bridge - Bottom Left', 'Turtle Rock - Eye Bridge - Bottom Right', 'Turtle Rock - Eye Bridge - Top Left', 'Turtle Rock - Eye Bridge - Top Right',
                'Turtle Rock - Boss'
            ],
            'Palace of Darkness': [
                'Palace of Darkness - Shooter Room', 'Palace of Darkness - The Arena - Bridge', 'Palace of Darkness - Stalfos Basement',
                'Palace of Darkness - Big Key Chest',
                'Palace of Darkness - The Arena - Ledge', 'Palace of Darkness - Map Chest',
                'Palace of Darkness - Compass Chest', 'Palace of Darkness - Dark Basement - Left', 'Palace of Darkness - Dark Basement - Right',
                'Palace of Darkness - Dark Maze - Top', 'Palace of Darkness - Dark Maze - Bottom', 'Palace of Darkness - Big Chest',
                'Palace of Darkness - Harmless Hellway', 'Palace of Darkness - Boss'
            ],
            'Ganons Tower': [
                'Ganons Tower - Bob\'s Torch', 'Ganons Tower - Hope Room - Left', 'Ganons Tower - Hope Room - Right',
                'Ganons Tower - Tile Room',
                'Ganons Tower - Compass Room - Top Left', 'Ganons Tower - Compass Room - Top Right', 'Ganons Tower - Compass Room - Bottom Left', 'Ganons Tower - Compass Room - Bottom Right',
                'Ganons Tower - DMs Room - Top Left', 'Ganons Tower - DMs Room - Top Right', 'Ganons Tower - DMs Room - Bottom Left', 'Ganons Tower - DMs Room - Bottom Right',
                'Ganons Tower - Map Chest', 'Ganons Tower - Firesnake Room',
                'Ganons Tower - Randomizer Room - Top Left', 'Ganons Tower - Randomizer Room - Top Right', 'Ganons Tower - Randomizer Room - Bottom Left', 'Ganons Tower - Randomizer Room - Bottom Right',
                'Ganons Tower - Bob\'s Chest',
                'Ganons Tower - Big Chest', 'Ganons Tower - Big Key Room - Left', 'Ganons Tower - Big Key Room - Right', 'Ganons Tower - Big Key Chest',
            ]
        }

        tracker.progressive_items = [
            'Progressive Sword',
            'Progressive Shield',
            'Progressive Mail',
            'Progressive Bow',
            'Progressive Boomerang',
            'Hookshot',
            'Magic Powder',
            'Mushroom',
            'Bottle',
            'Lamp',
            'Progressive Glove',
            'Flippers',
            'Moon Pearl',
            'Bombos',
            'Ether',
            'Quake',
            'Fire Rod',
            'Ice Rod',
            'Hammer',
            'Book of Mudora',
            'Shovel',
            'Flute',
            'Bug Catching Net',
            'Cane of Somaria',
            'Cane of Byrna',
            'Cape',
            'Magic Mirror',
            'Small Key',
            'Big Key'
        ]

        tracker.progressive_names = {
            'Progressive Bow': ['Bow', 'Silver Arrows', 'Silver Bow', 'Progressive Bow (Alt)'],
            'Bottle': ['Bottle (Red Potion)', 'Bottle (Green Potion)', 'Bottle (Blue Potion)', 'Bottle (Fairy)', 'Bottle (Bee)', 'Bottle (Good Bee)'],
            'Progressive Sword': ['Fighter Sword', 'Master Sword', 'Tempered Sword', 'Golden Sword'],
            'Progressive Glove': ['Power Glove', 'Titans Mitts'],
            'Progressive Shield': ['Blue Shield', 'Red Shield', 'Mirror Shield'],
            'Progressive Boomerang': ['Red Boomerang', 'Blue Boomerang'],
            'Progressive Mail': ['Green Mail', 'Blue Mail', 'Red Mail'],
            'Small Key': [f'Small Key ({region})' for region in tracker.regions.keys() if region not in {'Light World', 'Dark World'}],
            'Big Key': [f'Big Key ({region})' for region in tracker.regions.keys() if region not in {'Light World', 'Dark World'}],
        }

        tracker.region_keys = {
            region: [f'Small Key ({region})', f'Big Key ({region})'] for region in tracker.regions.keys() if region not in {'Light World', 'Dark World'}
        }


class ALTTPWorld(World):
    """
    The Legend of Zelda: A Link to the Past is an action/adventure game. Take on the role of
    Link, a boy who is destined to save the land of Hyrule. Delve through three palaces and nine
    dungeons on your quest to rescue the descendents of the seven wise men and defeat the evil
    Ganon!
    """
    game: str = "A Link to the Past"
    options = alttp_options
    topology_present = True
    item_name_groups = item_name_groups
    hint_blacklist = {"Triforce"}

    item_name_to_id = {name: data.item_code for name, data in item_table.items() if type(data.item_code) == int}
    location_name_to_id = lookup_name_to_id

    data_version = 8
    remote_items: bool = False
    remote_start_inventory: bool = False
    required_client_version = (0, 3, 2)
    web = ALTTPWeb()

    set_rules = set_rules

    create_items = generate_itempool

    def __init__(self, *args, **kwargs):
        self.dungeon_local_item_names = set()
        self.dungeon_specific_item_names = set()
        self.rom_name_available_event = threading.Event()
        self.has_progressive_bows = False
        super(ALTTPWorld, self).__init__(*args, **kwargs)

    @classmethod
    def stage_assert_generate(cls, world):
        rom_file = get_base_rom_path()
        if not os.path.exists(rom_file):
            raise FileNotFoundError(rom_file)

    def generate_early(self):
        player = self.player
        world = self.world

        # system for sharing ER layouts
        self.er_seed = str(world.random.randint(0, 2 ** 64))

        if "-" in world.shuffle[player]:
            shuffle, seed = world.shuffle[player].split("-", 1)
            world.shuffle[player] = shuffle
            if shuffle == "vanilla":
                self.er_seed = "vanilla"
            elif seed.startswith("group-") or world.is_race:
                self.er_seed = get_same_seed(world, (
                    shuffle, seed, world.retro[player], world.mode[player], world.logic[player]))
            else:  # not a race or group seed, use set seed as is.
                self.er_seed = seed
        elif world.shuffle[player] == "vanilla":
            self.er_seed = "vanilla"
        for dungeon_item in ["smallkey_shuffle", "bigkey_shuffle", "compass_shuffle", "map_shuffle"]:
            option = getattr(world, dungeon_item)[player]
            if option == "own_world":
                world.local_items[player].value |= self.item_name_groups[option.item_name_group]
            elif option == "different_world":
                world.non_local_items[player].value |= self.item_name_groups[option.item_name_group]
            elif option.in_dungeon:
                self.dungeon_local_item_names |= self.item_name_groups[option.item_name_group]
                if option == "original_dungeon":
                    self.dungeon_specific_item_names |= self.item_name_groups[option.item_name_group]

        world.difficulty_requirements[player] = difficulties[world.difficulty[player]]

    def create_regions(self):
        player = self.player
        world = self.world
        if world.open_pyramid[player] == 'goal':
            world.open_pyramid[player] = world.goal[player] in {'crystals', 'ganontriforcehunt',
                                                                'localganontriforcehunt', 'ganonpedestal'}
        elif world.open_pyramid[player] == 'auto':
            world.open_pyramid[player] = world.goal[player] in {'crystals', 'ganontriforcehunt',
                                                                'localganontriforcehunt', 'ganonpedestal'} and \
                                         (world.shuffle[player] in {'vanilla', 'dungeonssimple', 'dungeonsfull',
                                                                    'dungeonscrossed'} or not world.shuffle_ganon)
        else:
            world.open_pyramid[player] = {'on': True, 'off': False, 'yes': True, 'no': False}.get(
                world.open_pyramid[player], 'auto')

        world.triforce_pieces_available[player] = max(world.triforce_pieces_available[player],
                                                      world.triforce_pieces_required[player])

        if world.mode[player] != 'inverted':
            create_regions(world, player)
        else:
            create_inverted_regions(world, player)
        create_shops(world, player)
        create_dungeons(world, player)

        if world.logic[player] not in ["noglitches", "minorglitches"] and world.shuffle[player] in \
                {"vanilla", "dungeonssimple", "dungeonsfull", "simple", "restricted", "full"}:
            world.fix_fake_world[player] = False

        # seeded entrance shuffle
        old_random = world.random
        world.random = random.Random(self.er_seed)

        if world.mode[player] != 'inverted':
            link_entrances(world, player)
            mark_light_world_regions(world, player)
        else:
            link_inverted_entrances(world, player)
            mark_dark_world_regions(world, player)

        world.random = old_random
        plando_connect(world, player)

    def collect_item(self, state: CollectionState, item: Item, remove=False):
        item_name = item.name
        if item_name.startswith('Progressive '):
            if remove:
                if 'Sword' in item_name:
                    if state.has('Golden Sword', item.player):
                        return 'Golden Sword'
                    elif state.has('Tempered Sword', item.player):
                        return 'Tempered Sword'
                    elif state.has('Master Sword', item.player):
                        return 'Master Sword'
                    elif state.has('Fighter Sword', item.player):
                        return 'Fighter Sword'
                    else:
                        return None
                elif 'Glove' in item.name:
                    if state.has('Titans Mitts', item.player):
                        return 'Titans Mitts'
                    elif state.has('Power Glove', item.player):
                        return 'Power Glove'
                    else:
                        return None
                elif 'Shield' in item_name:
                    if state.has('Mirror Shield', item.player):
                        return 'Mirror Shield'
                    elif state.has('Red Shield', item.player):
                        return 'Red Shield'
                    elif state.has('Blue Shield', item.player):
                        return 'Blue Shield'
                    else:
                        return None
                elif 'Bow' in item_name:
                    if state.has('Silver Bow', item.player):
                        return 'Silver Bow'
                    elif state.has('Bow', item.player):
                        return 'Bow'
                    else:
                        return None
            else:
                if 'Sword' in item_name:
                    if state.has('Golden Sword', item.player):
                        pass
                    elif state.has('Tempered Sword', item.player) and self.world.difficulty_requirements[
                        item.player].progressive_sword_limit >= 4:
                        return 'Golden Sword'
                    elif state.has('Master Sword', item.player) and self.world.difficulty_requirements[
                        item.player].progressive_sword_limit >= 3:
                        return 'Tempered Sword'
                    elif state.has('Fighter Sword', item.player) and self.world.difficulty_requirements[item.player].progressive_sword_limit >= 2:
                        return 'Master Sword'
                    elif self.world.difficulty_requirements[item.player].progressive_sword_limit >= 1:
                        return 'Fighter Sword'
                elif 'Glove' in item_name:
                    if state.has('Titans Mitts', item.player):
                        return
                    elif state.has('Power Glove', item.player):
                        return 'Titans Mitts'
                    else:
                        return 'Power Glove'
                elif 'Shield' in item_name:
                    if state.has('Mirror Shield', item.player):
                        return
                    elif state.has('Red Shield', item.player) and self.world.difficulty_requirements[item.player].progressive_shield_limit >= 3:
                        return 'Mirror Shield'
                    elif state.has('Blue Shield', item.player) and self.world.difficulty_requirements[item.player].progressive_shield_limit >= 2:
                        return 'Red Shield'
                    elif self.world.difficulty_requirements[item.player].progressive_shield_limit >= 1:
                        return 'Blue Shield'
                elif 'Bow' in item_name:
                    if state.has('Silver Bow', item.player):
                        return
                    elif state.has('Bow', item.player) and (self.world.difficulty_requirements[item.player].progressive_bow_limit >= 2
                        or self.world.logic[item.player] == 'noglitches'
                        or self.world.swordless[item.player]): # modes where silver bow is always required for ganon
                        return 'Silver Bow'
                    elif self.world.difficulty_requirements[item.player].progressive_bow_limit >= 1:
                        return 'Bow'
        elif item.advancement:
            return item_name

    def pre_fill(self):
        from Fill import fill_restrictive, FillError
        attempts = 5
        world = self.world
        player = self.player
        all_state = world.get_all_state(use_cache=True)
        crystals = [self.create_item(name) for name in ['Red Pendant', 'Blue Pendant', 'Green Pendant', 'Crystal 1', 'Crystal 2', 'Crystal 3', 'Crystal 4', 'Crystal 7', 'Crystal 5', 'Crystal 6']]
        crystal_locations = [world.get_location('Turtle Rock - Prize', player),
                             world.get_location('Eastern Palace - Prize', player),
                             world.get_location('Desert Palace - Prize', player),
                             world.get_location('Tower of Hera - Prize', player),
                             world.get_location('Palace of Darkness - Prize', player),
                             world.get_location('Thieves\' Town - Prize', player),
                             world.get_location('Skull Woods - Prize', player),
                             world.get_location('Swamp Palace - Prize', player),
                             world.get_location('Ice Palace - Prize', player),
                             world.get_location('Misery Mire - Prize', player)]
        placed_prizes = {loc.item.name for loc in crystal_locations if loc.item}
        unplaced_prizes = [crystal for crystal in crystals if crystal.name not in placed_prizes]
        empty_crystal_locations = [loc for loc in crystal_locations if not loc.item]
        for attempt in range(attempts):
            try:
                prizepool = unplaced_prizes.copy()
                prize_locs = empty_crystal_locations.copy()
                world.random.shuffle(prize_locs)
                fill_restrictive(world, all_state, prize_locs, prizepool, True, lock=True)
            except FillError as e:
                lttp_logger.exception("Failed to place dungeon prizes (%s). Will retry %s more times", e,
                                                attempts - attempt)
                for location in empty_crystal_locations:
                    location.item = None
                continue
            break
        else:
            raise FillError('Unable to place dungeon prizes')

    @classmethod
    def stage_pre_fill(cls, world):
        from .Dungeons import fill_dungeons_restrictive
        fill_dungeons_restrictive(world)

    @classmethod
    def stage_post_fill(cls, world):
        ShopSlotFill(world)

    def generate_output(self, output_directory: str):
        world = self.world
        player = self.player
        try:
            use_enemizer = (world.boss_shuffle[player] != 'none' or world.enemy_shuffle[player]
                            or world.enemy_health[player] != 'default' or world.enemy_damage[player] != 'default'
                            or world.pot_shuffle[player] or world.bush_shuffle[player]
                            or world.killable_thieves[player])

            rom = LocalRom(get_base_rom_path())

            patch_rom(world, rom, player, use_enemizer)

            if use_enemizer:
                patch_enemizer(world, player, rom, world.enemizer, output_directory)

            if world.is_race:
                patch_race_rom(rom, world, player)

            world.spoiler.hashes[player] = get_hash_string(rom.hash)

            palettes_options = {
                'dungeon': world.uw_palettes[player],
                'overworld': world.ow_palettes[player],
                'hud': world.hud_palettes[player],
                'sword': world.sword_palettes[player],
                'shield': world.shield_palettes[player],
                'link': world.link_palettes[player]
            }
            palettes_options = {key: option.current_key for key, option in palettes_options.items()}

            apply_rom_settings(rom, world.heartbeep[player].current_key,
                               world.heartcolor[player].current_key,
                               world.quickswap[player],
                               world.menuspeed[player].current_key,
                               world.music[player],
                               world.sprite[player],
                               palettes_options, world, player, True,
                               reduceflashing=world.reduceflashing[player] or world.is_race,
                               triforcehud=world.triforcehud[player].current_key,
                               deathlink=world.death_link[player],
                               allowcollect=world.allow_collect[player])

            outfilepname = f'_P{player}'
            outfilepname += f"_{world.get_file_safe_player_name(player).replace(' ', '_')}" \
                if world.player_name[player] != 'Player%d' % player else ''

            rompath = os.path.join(output_directory, f'AP_{world.seed_name}{outfilepname}.sfc')
            rom.write_to_file(rompath)
            patch = LttPDeltaPatch(os.path.splitext(rompath)[0]+LttPDeltaPatch.patch_file_ending, player=player,
                                   player_name=world.player_name[player], patched_path=rompath)
            patch.write()
            os.unlink(rompath)
            self.rom_name = rom.name
        except:
            raise
        finally:
            self.rom_name_available_event.set() # make sure threading continues and errors are collected

    def modify_multidata(self, multidata: dict):
        import base64
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.world.player_name[self.player]]

    def create_item(self, name: str) -> Item:
        return ALttPItem(name, self.player, **as_dict_item_table[name])

    @classmethod
    def stage_fill_hook(cls, world, progitempool, nonexcludeditempool, localrestitempool, nonlocalrestitempool,
                        restitempool, fill_locations):
        trash_counts = {}
        standard_keyshuffle_players = set()
        for player in world.get_game_players("A Link to the Past"):
            if world.mode[player] == 'standard' and world.smallkey_shuffle[player] \
                    and world.smallkey_shuffle[player] != smallkey_shuffle.option_universal and \
                    world.smallkey_shuffle[player] != smallkey_shuffle.option_own_dungeons:
                standard_keyshuffle_players.add(player)
            if not world.ganonstower_vanilla[player] or \
                    world.logic[player] in {'owglitches', 'hybridglitches', "nologic"}:
                pass
            elif 'triforcehunt' in world.goal[player] and ('local' in world.goal[player] or world.players == 1):
                trash_counts[player] = world.random.randint(world.crystals_needed_for_gt[player] * 2,
                                                            world.crystals_needed_for_gt[player] * 4)
            else:
                trash_counts[player] = world.random.randint(0, world.crystals_needed_for_gt[player] * 2)

        # Make sure the escape small key is placed first in standard with key shuffle to prevent running out of spots
        # TODO: this might be worthwhile to introduce as generic option for various games and then optimize it
        if standard_keyshuffle_players:
            viable = {}
            for location in world.get_locations():
                if location.player in standard_keyshuffle_players \
                        and location.item is None \
                        and location.can_reach(world.state):
                    viable.setdefault(location.player, []).append(location)

            for player in standard_keyshuffle_players:
                loc = world.random.choice(viable[player])
                key = world.create_item("Small Key (Hyrule Castle)", player)
                loc.place_locked_item(key)
                fill_locations.remove(loc)
            world.random.shuffle(fill_locations)
            # TODO: investigate not creating the key in the first place
            progitempool[:] = [item for item in progitempool if
                               item.player not in standard_keyshuffle_players or
                               item.name != "Small Key (Hyrule Castle)"]

        if trash_counts:
            locations_mapping = {player: [] for player in trash_counts}
            for location in fill_locations:
                if 'Ganons Tower' in location.name and location.player in locations_mapping:
                    locations_mapping[location.player].append(location)

            for player, trash_count in trash_counts.items():
                gtower_locations = locations_mapping[player]
                world.random.shuffle(gtower_locations)
                localrest = localrestitempool[player]
                if localrest:
                    gt_item_pool = restitempool + localrest
                    world.random.shuffle(gt_item_pool)
                else:
                    gt_item_pool = restitempool.copy()

                while gtower_locations and gt_item_pool and trash_count > 0:
                    spot_to_fill = gtower_locations.pop()
                    item_to_place = gt_item_pool.pop()
                    if item_to_place in localrest:
                        localrest.remove(item_to_place)
                    else:
                        restitempool.remove(item_to_place)
                    world.push_item(spot_to_fill, item_to_place, False)
                    fill_locations.remove(spot_to_fill)  # very slow, unfortunately
                    trash_count -= 1

    def get_filler_item_name(self) -> str:
        if self.world.goal[self.player] == "icerodhunt":
            item = "Nothing"
        else:
            item = self.world.random.choice(chain(difficulties[self.world.difficulty[self.player]].extras[0:5]))
        return GetBeemizerItem(self.world, self.player, item)

    def get_pre_fill_items(self):
        res = []
        if self.dungeon_local_item_names:
            for (name, player), dungeon in self.world.dungeons.items():
                if player == self.player:
                    for item in dungeon.all_items:
                        if item.name in self.dungeon_local_item_names:
                            res.append(item)
        return res


def get_same_seed(world, seed_def: tuple) -> str:
    seeds: typing.Dict[tuple, str] = getattr(world, "__named_seeds", {})
    if seed_def in seeds:
        return seeds[seed_def]
    seeds[seed_def] = str(world.random.randint(0, 2 ** 64))
    world.__named_seeds = seeds
    return seeds[seed_def]


class ALttPLogic(LogicMixin):
    def _lttp_has_key(self, item, player, count: int = 1):
        if self.world.logic[player] == 'nologic':
            return True
        if self.world.smallkey_shuffle[player] == smallkey_shuffle.option_universal:
            return self.can_buy_unlimited('Small Key (Universal)', player)
        return self.prog_items[item, player] >= count
