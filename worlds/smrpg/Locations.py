from typing import Dict, List

from BaseClasses import Location
from enum import Enum, auto


class SMRPGRegions(Enum):
    marios_pad = auto()
    mushroom_way = auto()
    mushroom_kingdom = auto()
    bandits_way = auto()
    kero_sewers = auto()
    midas_river = auto()
    tadpole_pond = auto()
    rose_way = auto()
    rose_town = auto()
    forest_maze = auto()
    pipe_vault = auto()
    yoster_isle = auto()
    moleville = auto()
    moleville_mines_back = auto()
    booster_pass = auto()
    booster_tower = auto()
    booster_hill = auto()
    marrymore = auto()
    star_hill = auto()
    seaside_town = auto()
    sea = auto()
    sunken_ship = auto()
    sunken_ship_back = auto()
    lands_end = auto()
    belome_temple = auto()
    monstro_town = auto()
    bean_valley = auto()
    nimbus_land = auto()
    nimbus_castle_front = auto()
    nimbus_castle_middle = auto()
    nimbus_castle_back = auto()
    barrel_volcano = auto()
    bowsers_keep = auto()
    factory = auto()


class LocationData():
    name = ""
    star_piece_eligible = False
    region = None
    id = 0
    rando_name = ""

    def __init__(self, name: str, star_piece_eligible: bool, region: SMRPGRegions, id: int, rando_name: str):
        self.name = name
        self.star_piece_eligible = star_piece_eligible
        self.region = region
        self.id = id
        # The internal name used by the randomizer.
        self.rando_name = rando_name


bosses_data = [
    ("Boss - Hammer Bros Spot", SMRPGRegions.mushroom_way, "HammerBros"),
    ("Boss - Croco 1 Spot", SMRPGRegions.bandits_way, "Croco1(Boss)"),
    ("Boss - Mack Spot", SMRPGRegions.mushroom_kingdom, "Mack"),
    ("Boss - Pandorite Spot", SMRPGRegions.kero_sewers, "Pandorite"),
    ("Boss - Belome 1 Spot", SMRPGRegions.kero_sewers, "Belome1"),
    ("Boss - Bowyer Spot", SMRPGRegions.forest_maze, "Bowyer"),
    ("Boss - Croco 2 Spot", SMRPGRegions.moleville, "Croco2(Boss)"),
    ("Boss - Punchinello Spot", SMRPGRegions.moleville_mines_back, "Punchinello"),
    ("Boss - Booster Spot", SMRPGRegions.booster_tower, "Booster"),
    ("Boss - Knife Guy and Crate Guy Spot", SMRPGRegions.booster_tower, "ClownBros"),
    ("Boss - Bundt Spot", SMRPGRegions.marrymore, "Bundt"),
    ("Event - Star Hill Spot", SMRPGRegions.star_hill, "StarHill"),
    ("Boss - King Calamari Spot", SMRPGRegions.sunken_ship, "KingCalamari"),
    ("Boss - Hidon Spot", SMRPGRegions.sunken_ship_back, "Hidon"),
    ("Boss - Johnny Spot", SMRPGRegions.sunken_ship_back, "Johnny"),
    ("Boss - Yaridovich Spot", SMRPGRegions.seaside_town, "Yaridovich"),
    ("Boss - Belome 2 Spot", SMRPGRegions.belome_temple, "Belome2"),
    ("Boss - Jagger Spot", SMRPGRegions.monstro_town, "Jagger"),
    # ("Jinx 1", SMRPGRegions.monstro_town),
    # ("Jinx 2", SMRPGRegions.monstro_town),
    ("Boss - Jinx 3 Spot", SMRPGRegions.monstro_town, "Jinx3(Boss)"),
    ("Boss - Culex Spot", SMRPGRegions.monstro_town, "Culex"),
    ("Boss - Box Boy Spot", SMRPGRegions.bean_valley, "BoxBoy"),
    ("Boss - Mega Smilax Spot", SMRPGRegions.bean_valley, "MegaSmilax"),
    ("Boss - Dodo Spot", SMRPGRegions.nimbus_castle_front, "Dodo"),
    ("Boss - Birdo Spot", SMRPGRegions.nimbus_castle_middle, "Birdo(Boss)"),
    ("Boss - Valentina Spot", SMRPGRegions.nimbus_castle_back, "Valentina"),
    ("Boss - Czar Dragon Spot", SMRPGRegions.barrel_volcano, "CzarDragon"),
    ("Boss - Axem Rangers Spot", SMRPGRegions.barrel_volcano, "AxemRangers"),
    ("Boss - Magikoopa Spot", SMRPGRegions.bowsers_keep, "Magikoopa"),
    ("Boss - Boomer Spot", SMRPGRegions.bowsers_keep, "Boomer"),
    ("Boss - Exor Spot", SMRPGRegions.bowsers_keep, "Exor"),
    ("Boss - Countdown Spot", SMRPGRegions.factory, "Countdown"),
    ("Boss - Cloaker and Domino Spot", SMRPGRegions.factory, "CloakerDomino"),
    ("Boss - Clerk Spot", SMRPGRegions.factory, "Clerk"),
    ("Boss - Manager Spot", SMRPGRegions.factory, "Manager"),
    ("Boss - Director Spot", SMRPGRegions.factory, "Director"),
    ("Boss - Gunyolk Spot", SMRPGRegions.factory, "Gunyolk"),
    ("Boss - Smithy Spot", SMRPGRegions.factory, "Smithy"),
]

bad_boss_data = [
    ("Boss - Box Boy Spot", SMRPGRegions.bean_valley, "BoxBoy"),
    ("Boss - Croco 1 Spot", SMRPGRegions.bandits_way, "Croco1(Boss)"),
    ("Boss - Croco 2 Spot", SMRPGRegions.moleville, "Croco2(Boss)"),
    ("Event - Star Hill Spot", SMRPGRegions.star_hill, "StarHill"),
    ("Boss - Belome 2 Spot", SMRPGRegions.belome_temple, "Belome2"),
    ("Boss - Booster Spot", SMRPGRegions.booster_tower, "Booster"),
    ("Boss - Birdo Spot", SMRPGRegions.nimbus_castle_middle, "Birdo(Boss)"),
    ("Boss - Valentina Spot", SMRPGRegions.nimbus_castle_back, "Valentina"),
]

key_items_data = [
    ("Key Item - Mario's Bed (Dry Bones Flag)", SMRPGRegions.marios_pad, "MariosBed"),
    ("Key Item - Croco 1 (Rare Frog Coin)", SMRPGRegions.bandits_way, "Croco1"),
    ("Key Item - Rare Frog Coin Reward (Cricket Pie)", SMRPGRegions.mushroom_kingdom, "RareFrogCoinReward"),
    ("Key Item - Melody Bay Song 1 (Alto Card)", SMRPGRegions.tadpole_pond, "MelodyBaySong1"),
    ("Key Item - Melody Bay Song 2 (Tenor Card)", SMRPGRegions.tadpole_pond, "MelodyBaySong2"),
    ("Key Item - Melody Bay Song 3 (Soprano Card)", SMRPGRegions.tadpole_pond, "MelodyBaySong3"),
    ("Key Item - Rose Town Sign (Greaper Flag)", SMRPGRegions.rose_town, "RoseTownSign"),
    ("Key Item - Yo'ster Isle Goal (Big Boo Flag)", SMRPGRegions.yoster_isle, "YosterIsleGoal"),
    ("Key Item - Croco 2 (Bambino Bomb)", SMRPGRegions.moleville, "Croco2"),
    ("Key Item - Booster Tower Genealogy Hall (Elder Key)", SMRPGRegions.booster_tower, "BoosterTowerAncestors"),
    ("Key Item - Booster Tower Checkerboard Room (Room Key)", SMRPGRegions.booster_tower, "BoosterTowerCheckerboard"),
    ("Key Item - Knife Guy (Bright Card)", SMRPGRegions.booster_tower, "KnifeGuy"),
    ("Key Item - Seaside Town Key (Shed Key)", SMRPGRegions.seaside_town, "SeasideTownKey"),
    ("Key Item - Monstro Town Key (Temple Key)", SMRPGRegions.monstro_town, "MonstroTownKey"),
    ("Key Item - Kero Sewers Key Chest (Cricket Jam)", SMRPGRegions.lands_end, "CricketJamChest"),
    ("Key Item - Smilax (Seed)", SMRPGRegions.bean_valley, "Seed"),
    ("Key Item - Nimbus Land Guard (Castle Key 1)", SMRPGRegions.nimbus_castle_front, "NimbusLandCastleKey"),
    ("Key Item - Birdo (Castle Key 2)", SMRPGRegions.nimbus_castle_middle, "Birdo"),
    ("Key Item - Shy Away (Fertilizer)", SMRPGRegions.nimbus_castle_back, "Fertilizer"),
]

chests_data = [
    ("Chest - Mushroom Way 1", SMRPGRegions.mushroom_way, "MushroomWay1"),
    ("Chest - Mushroom Way 2", SMRPGRegions.mushroom_way, "MushroomWay2"),
    ("Chest - Mushroom Way 3", SMRPGRegions.mushroom_way, "MushroomWay3"),
    ("Chest - Mushroom Way 4", SMRPGRegions.mushroom_way, "MushroomWay4"),
    ("Chest - Mushroom Kingdom Vault 1", SMRPGRegions.mushroom_kingdom, "MushroomKingdomVault1"),
    ("Chest - Mushroom Kingdom Vault 2", SMRPGRegions.mushroom_kingdom, "MushroomKingdomVault2"),
    ("Chest - Mushroom Kingdom Vault 3", SMRPGRegions.mushroom_kingdom, "MushroomKingdomVault3"),
    ("Chest - Bandit's Way Flower Jump", SMRPGRegions.bandits_way, "BanditsWay1"),
    ("Chest - Bandit's Way Guard Dog", SMRPGRegions.bandits_way, "BanditsWay2"),
    ("Chest - Bandit's Way Invincibility Star", SMRPGRegions.bandits_way, "BanditsWayStarChest"),
    ("Chest - Bandit's Way Dog Jump", SMRPGRegions.bandits_way, "BanditsWayDogJump"),
    ("Chest - Bandit's Way Croco Room", SMRPGRegions.bandits_way, "BanditsWayCroco"),
    ("Chest - Kero Sewers Pandorite Room", SMRPGRegions.kero_sewers, "KeroSewersPandoriteRoom"),
    ("Chest - Kero Sewers Invincibility Star", SMRPGRegions.kero_sewers, "KeroSewersStarChest"),
    ("Chest - Rose Way Platform Jump", SMRPGRegions.rose_way, "RoseWayPlatform"),
    ("Chest - Rose Town Store 1", SMRPGRegions.rose_town, "RoseTownStore1"),
    ("Chest - Rose Town Store 2", SMRPGRegions.rose_town, "RoseTownStore2"),
    ("Chest - Lazy Shell 1", SMRPGRegions.rose_town, "GardenerCloud1"),
    ("Chest - Lazy Shell 2", SMRPGRegions.rose_town, "GardenerCloud2"),
    ("Chest - Forest Maze 1", SMRPGRegions.forest_maze, "ForestMaze1"),
    ("Chest - Forest Maze 2", SMRPGRegions.forest_maze, "ForestMaze2"),
    ("Chest - Forest Maze Underground 1", SMRPGRegions.forest_maze, "ForestMazeUnderground1"),
    ("Chest - Forest Maze Underground 2", SMRPGRegions.forest_maze, "ForestMazeUnderground2"),
    ("Chest - Forest Maze Underground 3", SMRPGRegions.forest_maze, "ForestMazeUnderground3"),
    ("Chest - Forest Maze Red Essence", SMRPGRegions.forest_maze, "ForestMazeRedEssence"),
    ("Chest - Pipe Vault Slide 1", SMRPGRegions.pipe_vault, "PipeVaultSlide1"),
    ("Chest - Pipe Vault Slide 2", SMRPGRegions.pipe_vault, "PipeVaultSlide2"),
    ("Chest - Pipe Vault Slide 3", SMRPGRegions.pipe_vault, "PipeVaultSlide3"),
    ("Chest - Pipe Vault Nippers 1", SMRPGRegions.pipe_vault, "PipeVaultNippers1"),
    ("Chest - Pipe Vault Nippers 2", SMRPGRegions.pipe_vault, "PipeVaultNippers2"),
    ("Chest - Yo'ster Isle", SMRPGRegions.yoster_isle, "YosterIsleEntrance"),
    ("Chest - Moleville Mines Invincibility Star", SMRPGRegions.moleville_mines_back, "MolevilleMinesStarChest"),
    ("Chest - Moleville Mines Coins", SMRPGRegions.moleville_mines_back, "MolevilleMinesCoins"),
    ("Chest - Moleville Mines Punchinello 1", SMRPGRegions.moleville_mines_back, "MolevilleMinesPunchinello1"),
    ("Chest - Moleville Mines Punchinello 2", SMRPGRegions.moleville_mines_back, "MolevilleMinesPunchinello2"),
    ("Chest - Booster Pass 1", SMRPGRegions.booster_pass, "BoosterPass1"),
    ("Chest - Booster Pass 2", SMRPGRegions.booster_pass, "BoosterPass2"),
    ("Chest - Booster Pass Secret 1", SMRPGRegions.booster_pass, "BoosterPassSecret1"),
    ("Chest - Booster Pass Secret 2", SMRPGRegions.booster_pass, "BoosterPassSecret2"),
    ("Chest - Booster Pass Secret 3", SMRPGRegions.booster_pass, "BoosterPassSecret3"),
    ("Chest - Booster Tower Spookum", SMRPGRegions.booster_tower, "BoosterTowerSpookum"),
    ("Chest - Booster Tower Thwomp", SMRPGRegions.booster_tower, "BoosterTowerThwomp"),
    ("Chest - Booster Tower Masher", SMRPGRegions.booster_tower, "BoosterTowerMasher"),
    ("Chest - Booster Tower Parachute", SMRPGRegions.booster_tower, "BoosterTowerParachute"),
    ("Chest - Booster Tower Zoom Shoes", SMRPGRegions.booster_tower, "BoosterTowerZoomShoes"),
    ("Chest - Booster Tower Top 1", SMRPGRegions.booster_tower, "BoosterTowerTop1"),
    ("Chest - Booster Tower Top 2", SMRPGRegions.booster_tower, "BoosterTowerTop2"),
    ("Chest - Booster Tower Top 3", SMRPGRegions.booster_tower, "BoosterTowerTop3"),
    ("Chest - Marrymore Inn Second Floor", SMRPGRegions.marrymore, "MarrymoreInn"),
    ("Chest - Sea Invincibility Star", SMRPGRegions.sea, "SeaStarChest"),
    ("Chest - Sea Save Room 1", SMRPGRegions.sea, "SeaSaveRoom1"),
    ("Chest - Sea Save Room 2", SMRPGRegions.sea, "SeaSaveRoom2"),
    ("Chest - Sea Save Room 3", SMRPGRegions.sea, "SeaSaveRoom3"),
    ("Chest - Sea Save Room 4", SMRPGRegions.sea, "SeaSaveRoom4"),
    ("Chest - Sunken Ship Rat Stairs", SMRPGRegions.sunken_ship, "SunkenShipRatStairs"),
    ("Chest - Sunken Ship Shop", SMRPGRegions.sunken_ship, "SunkenShipShop"),
    ("Chest - Sunken Ship Coins 1", SMRPGRegions.sunken_ship, "SunkenShipCoins1"),
    ("Chest - Sunken Ship Coins 2", SMRPGRegions.sunken_ship, "SunkenShipCoins2"),
    ("Chest - Sunken Ship Clone Room", SMRPGRegions.sunken_ship_back, "SunkenShipCloneRoom"),
    ("Chest - Sunken Ship Frog Coin Room", SMRPGRegions.sunken_ship_back, "SunkenShipFrogCoinRoom"),
    ("Chest - Sunken Ship Hidon Mushroom", SMRPGRegions.sunken_ship_back, "SunkenShipHidonMushroom"),
    ("Chest - Sunken Ship Safety Ring", SMRPGRegions.sunken_ship_back, "SunkenShipSafetyRing"),
    ("Chest - Sunken Ship Bandana Reds", SMRPGRegions.sunken_ship_back, "SunkenShipBandanaReds"),
    ("Chest - Land's End Red Essence", SMRPGRegions.lands_end, "LandsEndRedEssence"),
    ("Chest - Land's End Chow Pit 1", SMRPGRegions.lands_end, "LandsEndChowPit1"),
    ("Chest - Land's End Chow Pit 2", SMRPGRegions.lands_end, "LandsEndChowPit2"),
    ("Chest - Land's End Bee Room", SMRPGRegions.lands_end, "LandsEndBeeRoom"),
    ("Chest - Land's End Secret 1", SMRPGRegions.lands_end, "LandsEndSecret1"),
    ("Chest - Land's End Secret 2", SMRPGRegions.lands_end, "LandsEndSecret2"),
    ("Chest - Land's End Shy Away", SMRPGRegions.lands_end, "LandsEndShyAway"),
    ("Chest - Land's End Invincibility Star 1", SMRPGRegions.lands_end, "LandsEndStarChest1"),
    ("Chest - Land's End Invincibility Star 2", SMRPGRegions.lands_end, "LandsEndStarChest2"),
    ("Chest - Land's End Invincibility Star 3", SMRPGRegions.lands_end, "LandsEndStarChest3"),
    ("Chest - Belome Temple Fortune Teller", SMRPGRegions.belome_temple, "BelomeTempleFortuneTeller"),
    ("Chest - Belome Temple After Fortune 1", SMRPGRegions.belome_temple, "BelomeTempleAfterFortune1"),
    ("Chest - Belome Temple After Fortune 2", SMRPGRegions.belome_temple, "BelomeTempleAfterFortune2"),
    ("Chest - Belome Temple After Fortune 3", SMRPGRegions.belome_temple, "BelomeTempleAfterFortune3"),
    ("Chest - Belome Temple After Fortune 4", SMRPGRegions.belome_temple, "BelomeTempleAfterFortune4"),
    ("Chest - Monstro Town Entrance", SMRPGRegions.monstro_town, "MonstroTownEntrance"),
    ("Chest - Bean Valley 1", SMRPGRegions.bean_valley, "BeanValley1"),
    ("Chest - Bean Valley 2", SMRPGRegions.bean_valley, "BeanValley2"),
    ("Chest - Bean Valley Box Boy Room", SMRPGRegions.bean_valley, "BeanValleyBoxBoyRoom"),
    ("Chest - Bean Valley Slot Room", SMRPGRegions.bean_valley, "BeanValleySlotRoom"),
    ("Chest - Bean Valley Piranha Plants", SMRPGRegions.bean_valley, "BeanValleyPiranhaPlants"),
    ("Chest - Bean Valley Beanstalk", SMRPGRegions.bean_valley, "BeanValleyBeanstalk"),
    ("Chest - Bean Valley Cloud 1", SMRPGRegions.bean_valley, "BeanValleyCloud1"),
    ("Chest - Bean Valley Cloud 2", SMRPGRegions.bean_valley, "BeanValleyCloud2"),
    ("Chest - Bean Valley Fall 1", SMRPGRegions.bean_valley, "BeanValleyFall1"),
    ("Chest - Bean Valley Fall 2", SMRPGRegions.bean_valley, "BeanValleyFall2"),
    ("Chest - Nimbus Land Shop", SMRPGRegions.nimbus_land, "NimbusLandShop"),
    ("Chest - Nimbus Castle Before Birdo 1", SMRPGRegions.nimbus_castle_front, "NimbusCastleBeforeBirdo1"),
    ("Chest - Nimbus Castle Before Birdo 2", SMRPGRegions.nimbus_castle_front, "NimbusCastleBeforeBirdo2"),
    ("Chest - Nimbus Castle Out Of Bounds 1", SMRPGRegions.nimbus_castle_back, "NimbusCastleOutOfBounds1"),
    ("Chest - Nimbus Castle Out Of Bounds 2", SMRPGRegions.nimbus_castle_back, "NimbusCastleOutOfBounds2"),
    ("Chest - Nimbus Castle Single Gold Bird", SMRPGRegions.nimbus_castle_back, "NimbusCastleSingleGoldBird"),
    ("Chest - Nimbus Castle Invincibility Star", SMRPGRegions.nimbus_castle_back, "NimbusCastleStarChest"),
    ("Chest - Nimbus Castle Star After Valentina", SMRPGRegions.nimbus_castle_back, "NimbusCastleStarAfterValentina"),
    ("Chest - Barrel Volcano Secret 1", SMRPGRegions.barrel_volcano, "BarrelVolcanoSecret1"),
    ("Chest - Barrel Volcano Secret 2", SMRPGRegions.barrel_volcano, "BarrelVolcanoSecret2"),
    ("Chest - Barrel Volcano Before Star 1", SMRPGRegions.barrel_volcano, "BarrelVolcanoBeforeStar1"),
    ("Chest - Barrel Volcano Before Star 2", SMRPGRegions.barrel_volcano, "BarrelVolcanoBeforeStar2"),
    ("Chest - Barrel Volcano Invincibility Star", SMRPGRegions.barrel_volcano, "BarrelVolcanoStarRoom"),
    ("Chest - Barrel Volcano Save Room 1", SMRPGRegions.barrel_volcano, "BarrelVolcanoSaveRoom1"),
    ("Chest - Barrel Volcano Save Room 2", SMRPGRegions.barrel_volcano, "BarrelVolcanoSaveRoom2"),
    ("Chest - Barrel Volcano Hinopio", SMRPGRegions.barrel_volcano, "BarrelVolcanoHinnopio"),
    ("Chest - Bowser's Keep Dark Room", SMRPGRegions.bowsers_keep, "BowsersKeepDarkRoom"),
    ("Chest - Bowser's Keep Croco Shop 1", SMRPGRegions.bowsers_keep, "BowsersKeepCrocoShop1"),
    ("Chest - Bowser's Keep Croco Shop 2", SMRPGRegions.bowsers_keep, "BowsersKeepCrocoShop2"),
    ("Chest - Bowser's Keep Invisible Bridge 1", SMRPGRegions.bowsers_keep, "BowsersKeepInvisibleBridge1"),
    ("Chest - Bowser's Keep Invisible Bridge 2", SMRPGRegions.bowsers_keep, "BowsersKeepInvisibleBridge2"),
    ("Chest - Bowser's Keep Invisible Bridge 3", SMRPGRegions.bowsers_keep, "BowsersKeepInvisibleBridge3"),
    ("Chest - Bowser's Keep Invisible Bridge 4", SMRPGRegions.bowsers_keep, "BowsersKeepInvisibleBridge4"),
    ("Chest - Bowser's Keep Moving Platforms 1", SMRPGRegions.bowsers_keep, "BowsersKeepMovingPlatforms1"),
    ("Chest - Bowser's Keep Moving Platforms 2", SMRPGRegions.bowsers_keep, "BowsersKeepMovingPlatforms2"),
    ("Chest - Bowser's Keep Moving Platforms 3", SMRPGRegions.bowsers_keep, "BowsersKeepMovingPlatforms3"),
    ("Chest - Bowser's Keep Moving Platforms 4", SMRPGRegions.bowsers_keep, "BowsersKeepMovingPlatforms4"),
    ("Chest - Bowser's Keep Elevator Platforms", SMRPGRegions.bowsers_keep, "BowsersKeepElevatorPlatforms"),
    ("Chest - Bowser's Keep Cannonball Room 1", SMRPGRegions.bowsers_keep, "BowsersKeepCannonballRoom1"),
    ("Chest - Bowser's Keep Cannonball Room 2", SMRPGRegions.bowsers_keep, "BowsersKeepCannonballRoom2"),
    ("Chest - Bowser's Keep Cannonball Room 3", SMRPGRegions.bowsers_keep, "BowsersKeepCannonballRoom3"),
    ("Chest - Bowser's Keep Cannonball Room 4", SMRPGRegions.bowsers_keep, "BowsersKeepCannonballRoom4"),
    ("Chest - Bowser's Keep Cannonball Room 5", SMRPGRegions.bowsers_keep, "BowsersKeepCannonballRoom5"),
    ("Chest - Bowser's Keep Rotating Platforms 1", SMRPGRegions.bowsers_keep, "BowsersKeepRotatingPlatforms1"),
    ("Chest - Bowser's Keep Rotating Platforms 2", SMRPGRegions.bowsers_keep, "BowsersKeepRotatingPlatforms2"),
    ("Chest - Bowser's Keep Rotating Platforms 3", SMRPGRegions.bowsers_keep, "BowsersKeepRotatingPlatforms3"),
    ("Chest - Bowser's Keep Rotating Platforms 4", SMRPGRegions.bowsers_keep, "BowsersKeepRotatingPlatforms4"),
    ("Chest - Bowser's Keep Rotating Platforms 5", SMRPGRegions.bowsers_keep, "BowsersKeepRotatingPlatforms5"),
    ("Chest - Bowser's Keep Rotating Platforms 6", SMRPGRegions.bowsers_keep, "BowsersKeepRotatingPlatforms6"),
    ("Chest - Bowser's Keep Door Reward 1", SMRPGRegions.bowsers_keep, "BowsersKeepDoorReward1"),
    ("Chest - Bowser's Keep Door Reward 2", SMRPGRegions.bowsers_keep, "BowsersKeepDoorReward2"),
    ("Chest - Bowser's Keep Door Reward 3", SMRPGRegions.bowsers_keep, "BowsersKeepDoorReward3"),
    ("Chest - Bowser's Keep Door Reward 4", SMRPGRegions.bowsers_keep, "BowsersKeepDoorReward4"),
    ("Chest - Bowser's Keep Door Reward 5", SMRPGRegions.bowsers_keep, "BowsersKeepDoorReward5"),
    ("Chest - Bowser's Keep Door Reward 6", SMRPGRegions.bowsers_keep, "BowsersKeepDoorReward6"),
    ("Chest - Factory Save Room", SMRPGRegions.factory, "FactorySaveRoom"),
    ("Chest - Factory Bolt Platforms", SMRPGRegions.factory, "FactoryBoltPlatforms"),
    ("Chest - Factory Falling Axems", SMRPGRegions.factory, "FactoryFallingAxems"),
    ("Chest - Factory Treasure Pit 1", SMRPGRegions.factory, "FactoryTreasurePit1"),
    ("Chest - Factory Treasure Pit 2", SMRPGRegions.factory, "FactoryTreasurePit2"),
    ("Chest - Factory Conveyor Platforms 1", SMRPGRegions.factory, "FactoryConveyorPlatforms1"),
    ("Chest - Factory Conveyor Platforms 2", SMRPGRegions.factory, "FactoryConveyorPlatforms2"),
    ("Chest - Factory Behind Snakes 1", SMRPGRegions.factory, "FactoryBehindSnakes1"),
    ("Chest - Factory Behind Snakes 2", SMRPGRegions.factory, "FactoryBehindSnakes2"),
]

events_data = [
    ("Event - Toad Rescue 1", SMRPGRegions.mushroom_way, "ToadRescue1"),
    ("Event - Toad Rescue 2", SMRPGRegions.mushroom_way, "ToadRescue2"),
    ("Event - Hammer Bros Reward", SMRPGRegions.mushroom_way, "HammerBrosReward"),
    ("Event - Wallet Guy 1", SMRPGRegions.mushroom_kingdom, "WalletGuy1"),
    ("Event - Wallet Guy 2", SMRPGRegions.mushroom_kingdom, "WalletGuy2"),
    ("Event - Mushroom Kingdom Store", SMRPGRegions.mushroom_kingdom, "MushroomKingdomStore"),
    ("Event - Peach Surprise", SMRPGRegions.mushroom_kingdom, "PeachSurprise"),
    ("Event - Invasion Family", SMRPGRegions.mushroom_kingdom, "InvasionFamily"),
    ("Event - Invasion Guest Room", SMRPGRegions.mushroom_kingdom, "InvasionGuestRoom"),
    ("Event - Invasion Guard", SMRPGRegions.mushroom_kingdom, "InvasionGuard"),
    ("Event - Croco 1 Reward", SMRPGRegions.bandits_way, "Croco1Reward"),
    ("Event - Pandorite Reward", SMRPGRegions.kero_sewers, "PandoriteReward"),
    ("Event - Midas River First Time", SMRPGRegions.midas_river, "MidasRiverFirstTime"),
    ("Event - Rose Town Toad", SMRPGRegions.rose_town, "RoseTownToad"),
    ("Event - Gaz", SMRPGRegions.rose_town, "Gaz"),
    ("Event - Treasure Seller 1", SMRPGRegions.moleville, "TreasureSeller1"),
    ("Event - Treasure Seller 2", SMRPGRegions.moleville, "TreasureSeller2"),
    ("Event - Treasure Seller 3", SMRPGRegions.moleville, "TreasureSeller3"),
    ("Event - Croco Flunkie 1", SMRPGRegions.moleville, "CrocoFlunkie1"),
    ("Event - Croco Flunkie 2", SMRPGRegions.moleville, "CrocoFlunkie2"),
    ("Event - Croco Flunkie 3", SMRPGRegions.moleville, "CrocoFlunkie3"),
    ("Event - Booster Tower Railway", SMRPGRegions.booster_tower, "BoosterTowerRailway"),
    ("Event - Booster Tower Chomp", SMRPGRegions.booster_tower, "BoosterTowerChomp"),
    ("Event - Booster Tower Curtain Game", SMRPGRegions.booster_tower, "BoosterTowerCurtainGame"),
    ("Event - Seaside Town Rescue", SMRPGRegions.seaside_town, "SeasideTownRescue"),
    ("Event - Sunken Ship 3D Maze", SMRPGRegions.sunken_ship, "SunkenShip3DMaze"),
    ("Event - Sunken Ship Cannonball Puzzle", SMRPGRegions.sunken_ship, "SunkenShipCannonballPuzzle"),
    ("Event - Sunken Ship Hidon Reward", SMRPGRegions.sunken_ship_back, "SunkenShipHidonReward"),
    ("Event - Belome Temple Treasure 1", SMRPGRegions.belome_temple, "BelomeTempleTreasure1"),
    ("Event - Belome Temple Treasure 2", SMRPGRegions.belome_temple, "BelomeTempleTreasure2"),
    ("Event - Belome Temple Treasure 3", SMRPGRegions.belome_temple, "BelomeTempleTreasure3"),
    ("Event - Jinx Dojo Reward", SMRPGRegions.monstro_town, "JinxDojoReward"),
    ("Event - Culex Reward", SMRPGRegions.monstro_town, "CulexReward"),
    ("Event - Super Jumps 30", SMRPGRegions.monstro_town, "SuperJumps30"),
    ("Event - Super Jumps 100", SMRPGRegions.monstro_town, "SuperJumps100"),
    ("Event - Three Musty Fears", SMRPGRegions.monstro_town, "ThreeMustyFears"),
    ("Event - Troopa Climb", SMRPGRegions.lands_end, "TroopaClimb"),
    ("Event - Dodo Reward", SMRPGRegions.nimbus_castle_front, "DodoReward"),
    ("Event - Nimbus Land Inn", SMRPGRegions.nimbus_land, "NimbusLandInn"),
    ("Event - Nimbus Land Prisoners", SMRPGRegions.nimbus_castle_front, "NimbusLandPrisoners"),
    ("Event - Nimbus Land Signal Ring", SMRPGRegions.nimbus_castle_back, "NimbusLandSignalRing"),
    ("Event - Nimbus Land Cellar", SMRPGRegions.nimbus_castle_back, "NimbusLandCellar"),
    ("Event - Factory Toad Gift", SMRPGRegions.factory, "FactoryToadGift"),
    ("Event - Goomba Thumping 1", SMRPGRegions.pipe_vault, "GoombaThumping1"),
    ("Event - Goomba Thumping 2", SMRPGRegions.pipe_vault, "GoombaThumping2"),
    ("Event - Cricket Pie Reward", SMRPGRegions.tadpole_pond, "CricketPieReward"),
    ("Event - Cricket Jam Reward", SMRPGRegions.tadpole_pond, "CricketJamReward"),
]

locations_data = [*bosses_data, *key_items_data, *chests_data, *events_data]

star_piece_locations = [*bosses_data]
force_defeated_locations = [*bad_boss_data]

location_to_remove = None
for location in star_piece_locations:
    if location[0] == "Boss - Smithy Spot":
        location_to_remove = location
star_piece_locations.remove(location_to_remove)

additional_bambino_locks: List[str] = [
    "Event - Treasure Seller 1", "Event - Treasure Seller 2", "Event - Treasure Seller 3",
    "Key Item - Melody Bay Song 2", "Key Item - Melody Bay Song 3", "Boss - Culex Spot", "Event - Culex Reward"
]

missable_locations = [
    "Event - Wallet Guy 1", "Event - Wallet Guy 2", "Event - Invasion Guard", "Event - Invasion Family",
    "Event - Invasion Guest Room","Event - Rose Town Toad", "Event - Croco Flunkie 1", "Event - Croco Flunkie 2",
    "Event - Croco Flunkie 3", "Event - Booster Tower Curtain Game", "Event - Nimbus Castle Before Birdo 1",
    "Event - Nimbus Land Star Chest", "Event - Nimbus Land Prisoners"
]

no_key_locations = [*missable_locations]

no_reward_locations = [*[event[0] for event in events_data], *[key[0] for key in key_items_data]]

no_coin_locations = [
    "Chest - Bean Valley Beanstalk", "Chest - Bean Valley Box Boy Room",
    "Chest - Bean Valley Cloud 2, Chest - Bean Valley Fall 2", "Chest - Bean Valley Slot Room",
    "Chest - Booster Tower Top 1", "Chest - Factory Treasure Pit 2",
    "Chest - Nimbus Castle Out Of Bounds 1", "Chest - Nimbus Land Shop"
]

star_allowed_locations = [
    "Chest - Bandit's Way Invincibility Star", "Chest - Barrel Volcano Invincibility Star",
    "Chest - Kero Sewers Invincibility Star", "Chest - Land's End Invincibility Star 1",
    "Chest - Land's End Invincibility Star 2", "Chest - Land's End Invincibility Star 3",
    "Chest - Moleville Mines Invincibility Star", "Chest - Nimbus Castle Invincibility Star",
    "Chest - Sea Invincibility Star"
]

world_one_regions = [
    SMRPGRegions.marios_pad, SMRPGRegions.mushroom_way, SMRPGRegions.mushroom_kingdom, SMRPGRegions.bandits_way
]

world_two_regions = [
    SMRPGRegions.kero_sewers, SMRPGRegions.midas_river, SMRPGRegions.tadpole_pond, SMRPGRegions.rose_way,
    SMRPGRegions.rose_town, SMRPGRegions.forest_maze, SMRPGRegions.pipe_vault, SMRPGRegions.yoster_isle
]

world_three_regions = [
    SMRPGRegions.moleville, SMRPGRegions.moleville_mines_back, SMRPGRegions.booster_pass, SMRPGRegions.booster_tower,
    SMRPGRegions.booster_hill, SMRPGRegions.marrymore
]

world_four_regions = [
    SMRPGRegions.star_hill, SMRPGRegions.seaside_town, SMRPGRegions.sea,
    SMRPGRegions.sunken_ship, SMRPGRegions.sunken_ship_back
]

world_five_regions = [
    SMRPGRegions.lands_end, SMRPGRegions.monstro_town, SMRPGRegions.belome_temple, SMRPGRegions.bean_valley
]

world_six_regions = [
    SMRPGRegions.nimbus_land, SMRPGRegions.nimbus_castle_front, SMRPGRegions.nimbus_castle_middle,
    SMRPGRegions.nimbus_castle_back, SMRPGRegions.barrel_volcano
]

world_seven_regions = [
    SMRPGRegions.bowsers_keep, SMRPGRegions.factory
]

key_item_locations = {
    "Temple Key": [
        "Event - Belome Temple Treasure 1",
        "Event - Belome Temple Treasure 2",
        "Event - Belome Temple Treasure 3"
    ],
    "Rare Frog Coin": ["Key Item - Rare Frog Coin Reward (Cricket Pie)"],
    "Cricket Pie": ["Event - Cricket Pie Reward"],
    "Room Key": ["Chest - Booster Tower Zoom Shoes"],
    "Elder Key": ["Event - Booster Tower Chomp"],
    "Shed Key": ["Event - Seaside Town Rescue"],
    "Big Boo Flag": ["Event - Three Musty Fears"],
    "Dry Bones Flag": ["Event - Three Musty Fears"],
    "Greaper Flag": ["Event - Three Musty Fears"],
    "Seed": ["Chest - Lazy Shell 1", "Chest - Lazy Shell 2"],
    "Fertilizer": ["Chest - Lazy Shell 1", "Chest - Lazy Shell 2"],
}

keep_bosses = [
    "Boss - Magikoopa Spot", "Boss - Boomer Spot", "Boss - Exor Spot"
]

factory_bosses = [
    "Boss - Countdown Spot", "Boss - Cloaker and Domino Spot", "Boss - Clerk Spot",
    "Boss - Manager Spot", "Boss - Director Spot", "Boss - Gunyolk Spot"
]

culex_locations = ["Boss - Culex Spot", "Event - Culex Reward"]

super_jump_locations = ["Event - Super Jumps 30", "Event - Super Jumps 100"]

bowsers_keep_doors = [
    "Chest - Bowser's Keep Door Reward 1", "Chest - Bowser's Keep Door Reward 2", "Chest - Bowser's Keep Door Reward 3",
    "Chest - Bowser's Keep Door Reward 4", "Chest - Bowser's Keep Door Reward 5", "Chest - Bowser's Keep Door Reward 6"
]

location_table: Dict[str, LocationData] = dict()
for index, value in enumerate(locations_data):
    star_piece_eligible = value[0] in star_piece_locations
    location = LocationData(
        value[0],
        star_piece_eligible,
        value[1],
        index,
        value[2])
    location_table[location.name] = location
