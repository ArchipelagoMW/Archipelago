from enum import Enum
from logging import exception
from typing import Any, Callable, List, Sequence
import random
import typing
from BaseClasses import Location
from .Item import Item, ItemType, lookup_id_to_name
from .Location import LocationType
from .Region import IReward, RewardType, SMRegion, Z3Region
from .Regions.Zelda.EasternPalace import EasternPalace
from .Regions.Zelda.DesertPalace import DesertPalace
from .Regions.Zelda.TowerOfHera import TowerOfHera
from .Regions.Zelda.PalaceOfDarkness import PalaceOfDarkness
from .Regions.Zelda.SwampPalace import SwampPalace
from .Regions.Zelda.SkullWoods import SkullWoods
from .Regions.Zelda.ThievesTown import ThievesTown
from .Regions.Zelda.IcePalace import IcePalace
from .Regions.Zelda.MiseryMire import MiseryMire
from .Regions.Zelda.TurtleRock import TurtleRock
from .Regions.Zelda.GanonsTower import GanonsTower
from .Regions.SuperMetroid.Brinstar.Kraid import Kraid
from .Regions.SuperMetroid.WreckedShip import WreckedShip
from .Regions.SuperMetroid.Maridia.Inner import Inner
from .Regions.SuperMetroid.NorfairLower.East import East
from .Text.StringTable import StringTable

from .World import World
from .Config import Config, OpenTourian, Goal
from .Text.Texts import Texts
from .Text.Dialog import Dialog

class KeycardPlaque:
    Level1 = 0xe0
    Level2 = 0xe1
    Boss = 0xe2
    Null = 0x00  
    Zero = 0xe3
    One = 0xe4
    Two = 0xe5
    Three = 0xe6
    Four = 0xe7

class KeycardDoors:
    Left = 0xd414
    Right = 0xd41a
    Up = 0xd420
    Down = 0xd426
    BossLeft = 0xc842
    BossRight = 0xc848


class KeycardEvents:
    CrateriaLevel1 = 0x0000
    CrateriaLevel2 = 0x0100
    CrateriaBoss = 0x0200
    BrinstarLevel1 = 0x0300
    BrinstarLevel2 = 0x0400
    BrinstarBoss = 0x0500
    NorfairLevel1 = 0x0600
    NorfairLevel2 = 0x0700
    NorfairBoss = 0x0800
    MaridiaLevel1 = 0x0900
    MaridiaLevel2 = 0x0a00
    MaridiaBoss = 0x0b00
    WreckedShipLevel1 = 0x0c00
    WreckedShipBoss = 0x0d00
    LowerNorfairLevel1 = 0x0e00
    LowerNorfairBoss = 0x0f00

class DropPrize(Enum):
    Heart = 0xD8
    Green = 0xD9
    Blue = 0xDA
    Red = 0xDB
    Bomb1 = 0xDC
    Bomb4 = 0xDD
    Bomb8 = 0xDE
    Magic = 0xDF
    FullMagic = 0xE0
    Arrow5 = 0xE1
    Arrow10 = 0xE2
    Fairy = 0xE3

class Patch:
    Major = 11
    Minor = 3
    Patch = 1
    allWorlds: List[World]
    myWorld: World
    seedGuid: str
    seed: int
    rnd: random.Random
    patches: Sequence[Any]
    stringTable: StringTable
    silversWorldID: int

    def __init__(self, myWorld: World, allWorlds: List[World], seedGuid: str, seed: int, rnd: random.Random, playerNames: List[str], silversWorldID: int):
        self.myWorld = myWorld
        self.allWorlds = allWorlds
        self.seedGuid = seedGuid
        self.seed = seed
        self.rnd = rnd
        self.playerNames = playerNames
        self.playerIDToNames = {id:name for name, id in playerNames.items()}
        self.silversWorldID = silversWorldID

    def Create(self, config: Config):
        self.stringTable = StringTable()
        self.patches = []
        self.title = ""

        self.WriteMedallions()
        self.WriteRewards()
        self.WriteDungeonMusic(config.Keysanity)

        self.WriteDiggingGameRng()

        self.WritePrizeShuffle(self.myWorld.WorldState.DropPrizes)

        self.WriteRemoveEquipmentFromUncle( self.myWorld.GetLocation("Link's Uncle").APLocation.item.item if 
                                            self.myWorld.GetLocation("Link's Uncle").APLocation.item.game == "SMZ3" else
                                            Item(ItemType.Something))

        self.WriteGanonInvicible(config.Goal)
        self.WritePreOpenPyramid(config.Goal)
        self.WriteCrystalsNeeded(self.myWorld.TowerCrystals, self.myWorld.GanonCrystals, config.Goal)
        self.WriteBossesNeeded(self.myWorld.TourianBossTokens)
        self.WriteRngBlock()

        self.WriteSaveAndQuitFromBossRoom()
        self.WriteWorldOnAgahnimDeath()

        self.WriteTexts(config)

        self.WriteSMLocations([loc for region in self.myWorld.Regions for loc in region.Locations if isinstance(region, SMRegion)])
        self.WriteZ3Locations([loc for region in self.myWorld.Regions for loc in region.Locations if isinstance(region, Z3Region)])

        self.WriteStringTable()

        self.WriteSMKeyCardDoors()
        self.WriteZ3KeysanityFlags()

        self.WritePlayerNames()
        self.WriteSeedData()
        self.WriteGameTitle()
        self.WriteCommonFlags()

        return {patch[0]:patch[1] for patch in self.patches}
    
    def WriteMedallions(self):
        from .WorldState import Medallion
        turtleRock = next(region for region in self.myWorld.Regions if isinstance(region, TurtleRock))
        miseryMire = next(region for region in self.myWorld.Regions if isinstance(region, MiseryMire))

        turtleRockAddresses = [0x308023, 0xD020, 0xD0FF, 0xD1DE ]
        miseryMireAddresses = [ 0x308022, 0xCFF2, 0xD0D1, 0xD1B0 ]

        if turtleRock.Medallion == Medallion.Bombos:
            turtleRockValues = [0x00, 0x51, 0x10, 0x00]
        elif turtleRock.Medallion == Medallion.Ether:
            turtleRockValues = [0x01, 0x51, 0x18, 0x00]
        elif turtleRock.Medallion == Medallion.Quake:
            turtleRockValues = [0x02, 0x14, 0xEF, 0xC4]
        else:
            raise exception(f"Tried using {turtleRock.Medallion} in place of Turtle Rock medallion")

        if miseryMire.Medallion == Medallion.Bombos:
            miseryMireValues = [0x00, 0x51, 0x00, 0x00]
        elif miseryMire.Medallion == Medallion.Ether:
            miseryMireValues = [0x01, 0x13, 0x9F, 0xF1]
        elif miseryMire.Medallion == Medallion.Quake:
            miseryMireValues = [0x02, 0x51, 0x08, 0x00]
        else:
            raise exception(f"Tried using {miseryMire.Medallion} in place of Misery Mire medallion")

        self.patches += [(Snes(addr), [value]) for addr, value in zip(turtleRockAddresses, turtleRockValues)]
        self.patches += [(Snes(addr), [value]) for addr, value in zip(miseryMireAddresses, miseryMireValues)]

    def WriteRewards(self):
        crystalsBlue = [ 1, 2, 3, 4, 7 ]
        self.rnd.shuffle(crystalsBlue)
        crystalsRed = [ 5, 6 ]
        self.rnd.shuffle(crystalsRed)
        crystalRewards = crystalsBlue + crystalsRed

        pendantsGreen = [ 1 ]
        pendantsBlueRed = [ 2, 3 ]
        self.rnd.shuffle(pendantsBlueRed)
        pendantRewards = pendantsGreen + pendantsBlueRed

        bossTokens = [ 1, 2, 3, 4 ]

        regions = [region for region in self.myWorld.Regions if isinstance(region, IReward)]
        crystalRegions = [region for region in regions if region.Reward == RewardType.CrystalBlue] +  [region for region in regions if region.Reward == RewardType.CrystalRed]
        pendantRegions = [region for region in regions if region.Reward == RewardType.PendantGreen] +  [region for region in regions if region.Reward == RewardType.PendantNonGreen]
        bossRegions =   [region for region in regions if region.Reward == RewardType.BossTokenKraid] + \
                        [region for region in regions if region.Reward == RewardType.BossTokenPhantoon] + \
                        [region for region in regions if region.Reward == RewardType.BossTokenDraygon] + \
                        [region for region in regions if region.Reward == RewardType.BossTokenRidley]

        self.patches += self.RewardPatches(crystalRegions, crystalRewards, self.CrystalValues)
        self.patches += self.RewardPatches(pendantRegions, pendantRewards, self.PendantValues)
        self.patches += self.RewardPatches(bossRegions, bossTokens, self.BossTokenValues)

    def RewardPatches(self, regions: List[IReward], rewards: List[int], rewardValues: Callable):
        addresses = [self.RewardAddresses(region) for region in regions]
        values = [rewardValues(reward) for reward in rewards]
        associations = zip(addresses, values)
        return [(Snes(i), [b]) for association in associations for i,b in zip(association[0], association[1])]

    def RewardAddresses(self, region: IReward):
        regionType = {
                    EasternPalace : [ 0x2A09D, 0xABEF8, 0xABEF9, 0x308052, 0x30807C, 0x1C6FE, 0x30D100],
                    DesertPalace : [ 0x2A09E, 0xABF1C, 0xABF1D, 0x308053, 0x308078, 0x1C6FF, 0x30D101 ],
                    TowerOfHera : [ 0x2A0A5, 0xABF0A, 0xABF0B, 0x30805A, 0x30807A, 0x1C706, 0x30D102 ],
                    PalaceOfDarkness : [ 0x2A0A1, 0xABF00, 0xABF01, 0x308056, 0x30807D, 0x1C702, 0x30D103 ],
                    SwampPalace : [ 0x2A0A0, 0xABF6C, 0xABF6D, 0x308055, 0x308071, 0x1C701, 0x30D104 ],
                    SkullWoods : [ 0x2A0A3, 0xABF12, 0xABF13, 0x308058, 0x30807B, 0x1C704, 0x30D105 ],
                    ThievesTown : [ 0x2A0A6, 0xABF36, 0xABF37, 0x30805B, 0x308077, 0x1C707, 0x30D106 ],
                    IcePalace : [ 0x2A0A4, 0xABF5A, 0xABF5B, 0x308059, 0x308073, 0x1C705, 0x30D107 ],
                    MiseryMire : [ 0x2A0A2, 0xABF48, 0xABF49, 0x308057, 0x308075, 0x1C703, 0x30D108 ],
                    TurtleRock : [ 0x2A0A7, 0xABF24, 0xABF25, 0x30805C, 0x308079, 0x1C708, 0x30D109 ],
                    Kraid : [ 0xF26002, 0xF26004, 0xF26005, 0xF26000, 0xF26006, 0xF26007, 0x82FD36 ],
                    WreckedShip : [ 0xF2600A, 0xF2600C, 0xF2600D, 0xF26008, 0xF2600E, 0xF2600F, 0x82FE26 ],
                    Inner : [ 0xF26012, 0xF26014, 0xF26015, 0xF26010, 0xF26016, 0xF26017, 0x82FE76 ],
                    East : [ 0xF2601A, 0xF2601C, 0xF2601D, 0xF26018, 0xF2601E, 0xF2601F, 0x82FDD6 ]
                    }

        result = regionType.get(type(region), None)
        if result is None:
            raise exception(f"Region {region} should not be a dungeon reward region")
        else:
            return result

    def CrystalValues(self, crystal: int):
        crystalMap = {
                1 : [ 0x02, 0x34, 0x64, 0x40, 0x7F, 0x06, 0x10 ],
                2 : [ 0x10, 0x34, 0x64, 0x40, 0x79, 0x06, 0x10 ],
                3 : [ 0x40, 0x34, 0x64, 0x40, 0x6C, 0x06, 0x10 ],
                4 : [ 0x20, 0x34, 0x64, 0x40, 0x6D, 0x06, 0x10 ],
                5 : [ 0x04, 0x32, 0x64, 0x40, 0x6E, 0x06, 0x11 ],
                6 : [ 0x01, 0x32, 0x64, 0x40, 0x6F, 0x06, 0x11 ],
                7 : [ 0x08, 0x34, 0x64, 0x40, 0x7C, 0x06, 0x10 ],
                }
        result = crystalMap.get(crystal, None)
        if result is None:
            raise exception(f"Tried using {crystal} as a crystal number")
        else:
            return result

    def PendantValues(self, pendant: int):
        pendantMap = {
                        1 : [ 0x04, 0x38, 0x62, 0x00, 0x69, 0x01, 0x12 ],
                        2 : [ 0x01, 0x32, 0x60, 0x00, 0x69, 0x03, 0x14 ],
                        3 : [ 0x02, 0x34, 0x60, 0x00, 0x69, 0x02, 0x13 ]
                    }
        result = pendantMap.get(pendant, None)
        if result is None:
            raise exception(f"Tried using {pendant} as a pendant number")
        else:
            return result

    def BossTokenValues(self, token: int):
        tokenMap = {
                        1 : [ 0x01, 0x38, 0x40, 0x80, 0x69, 0x80, 0x15 ],
                        2 : [ 0x02, 0x34, 0x42, 0x80, 0x69, 0x81, 0x16 ],
                        3 : [ 0x04, 0x34, 0x44, 0x80, 0x69, 0x82, 0x17 ],
                        4 : [ 0x08, 0x32, 0x46, 0x80, 0x69, 0x83, 0x18 ]
                    }
        result = tokenMap.get(token, None)
        if result is None:
            raise exception(f"Tried using {token} as a boss token number")
        else:
            return result
    
    def WriteSMLocations(self, locations: List[Location]):
        def GetSMItemPLM(location:Location):
            itemMap = {
                    ItemType.ETank : 0xEED7,
                    ItemType.Missile : 0xEEDB,
                    ItemType.Super : 0xEEDF,
                    ItemType.PowerBomb : 0xEEE3,
                    ItemType.Bombs : 0xEEE7,
                    ItemType.Charge : 0xEEEB,
                    ItemType.Ice : 0xEEEF,
                    ItemType.HiJump : 0xEEF3,
                    ItemType.SpeedBooster : 0xEEF7,
                    ItemType.Wave : 0xEEFB,
                    ItemType.Spazer : 0xEEFF,
                    ItemType.SpringBall : 0xEF03,
                    ItemType.Varia : 0xEF07,
                    ItemType.Plasma : 0xEF13,
                    ItemType.Grapple : 0xEF17,
                    ItemType.Morph : 0xEF23,
                    ItemType.ReserveTank : 0xEF27,
                    ItemType.Gravity : 0xEF0B,
                    ItemType.XRay : 0xEF0F,
                    ItemType.SpaceJump : 0xEF1B,
                    ItemType.ScrewAttack : 0xEF1F
                    }
            plmId = 0xEFE0 if self.myWorld.Config.Multiworld else \
                                itemMap.get(location.APLocation.item.item.Type, 0xEFE0)
            if (plmId == 0xEFE0):
                plmId += 4 if location.Type == LocationType.Chozo else 8 if location.Type == LocationType.Hidden else 0
            else:
                plmId += 0x54 if location.Type == LocationType.Chozo else 0xA8 if location.Type == LocationType.Hidden else 0
            return plmId

        for location in locations:
            if (self.myWorld.Config.Multiworld):
                self.patches.append((Snes(location.Address), getWordArray(GetSMItemPLM(location))))
                self.patches.append(self.ItemTablePatch(location, self.GetZ3ItemId(location)))
            else:
                plmId = GetSMItemPLM(location)
                self.patches.append((Snes(location.Address), getWordArray(plmId)))
                if (plmId >= 0xEFE0):
                    self.patches.append((Snes(location.Address + 5), [self.GetZ3ItemId(location)]))

    def WriteZ3Locations(self, locations: List[Location]):
        for location in locations:
            if (location.Type == LocationType.HeraStandingKey):
                self.patches.append((Snes(0x9E3BB), [0xEB]))
            elif (location.Type in [LocationType.Pedestal, LocationType.Ether, LocationType.Bombos]):
                text = Texts.ItemTextbox(location.APLocation.item.item if location.APLocation.item.game == "SMZ3" else Item(ItemType.Something))
                if (location.Type == LocationType.Pedestal):
                    self.stringTable.SetPedestalText(text)
                elif (location.Type == LocationType.Ether):
                    self.stringTable.SetEtherText(text)
                elif (location.Type == LocationType.Bombos):
                    self.stringTable.SetBombosText(text)

            if (self.myWorld.Config.Multiworld):
                self.patches.append((Snes(location.Address), [(location.Id - 256)]))
                self.patches.append(self.ItemTablePatch(location, self.GetZ3ItemId(location)))
            else:
                self.patches.append((Snes(location.Address), [self.GetZ3ItemId(location)]))

    def GetZ3ItemId(self, location: Location):
        if (location.APLocation.item.game == "SMZ3"):
            item = location.APLocation.item.item
            itemDungeon = None
            if item.IsKey():
                itemDungeon = ItemType.Key
            elif item.IsBigKey(): 
                itemDungeon = ItemType.BigKey
            elif item.IsMap():
                itemDungeon = ItemType.Map
            elif item.IsCompass():
                itemDungeon = ItemType.Compass

            value = item.Type if location.Type == LocationType.NotInDungeon or \
                not (item.IsDungeonItem() and location.Region.IsRegionItem(item) and item.World == self.myWorld) else itemDungeon
            
            return value.value
        elif (location.APLocation.item.game == "A Link to the Past"):
            if location.APLocation.item.code + 84000 in lookup_id_to_name:
                ALTTPBottleContentCodeToSMZ3ItemCode = {
                    ItemType.RedContent.value: ItemType.BottleWithRedPotion.value,
                    ItemType.GreenContent.value: ItemType.BottleWithGreenPotion.value,
                    ItemType.BlueContent.value: ItemType.BottleWithBluePotion.value,
                    ItemType.BeeContent.value: ItemType.BottleWithBee.value,
                }
                return ALTTPBottleContentCodeToSMZ3ItemCode.get(location.APLocation.item.code, location.APLocation.item.code)
            else:
                return ItemType.Something.value
        elif (location.APLocation.item.game == "Super Metroid"):
            SMNameToSMZ3Code = {
                "Energy Tank": ItemType.ETank, "Missile": ItemType.Missile, "Super Missile": ItemType.Super,
                "Power Bomb": ItemType.PowerBomb, "Bomb": ItemType.Bombs, "Charge Beam": ItemType.Charge,
                "Ice Beam": ItemType.Ice, "Hi-Jump Boots": ItemType.HiJump, "Speed Booster": ItemType.SpeedBooster,
                "Wave Beam": ItemType.Wave, "Spazer": ItemType.Spazer, "Spring Ball": ItemType.SpringBall,
                "Varia Suit": ItemType.Varia, "Plasma Beam": ItemType.Plasma, "Grappling Beam": ItemType.Grapple,
                "Morph Ball": ItemType.Morph, "Reserve Tank": ItemType.ReserveTank, "Gravity Suit": ItemType.Gravity,
                "X-Ray Scope": ItemType.XRay, "Space Jump": ItemType.SpaceJump, "Screw Attack": ItemType.ScrewAttack,
                "Nothing": ItemType.Something, "No Energy": ItemType.Something, "Generic": ItemType.Something
            }
            return SMNameToSMZ3Code.get(location.APLocation.item.name, ItemType.Something).value
        else:
            return ItemType.Something.value

    def ItemTablePatch(self, location: Location, itemId: int):
        itemtype = 0 if location.APLocation.item.player == location.Region.world.Id else 1
        owner = location.APLocation.item.player if location.APLocation.item.player < 256 else 0
        return (0x386000 + (location.Id * 8), getWordArray(itemtype) + getWordArray(itemId) + getWordArray(owner))

    def WriteDungeonMusic(self, keysanity: bool):
        if (not keysanity):
            regions = [region for region in self.myWorld.Regions if isinstance(region, Z3Region) and isinstance(region, IReward) and 
                                                                    region.Reward != None and region.Reward != RewardType.Agahnim]
            pendantRegions = [region for region in regions if region.Reward in [RewardType.PendantGreen, RewardType.PendantNonGreen]]
            crystalRegions = [region for region in regions if region.Reward in [RewardType.CrystalBlue, RewardType.CrystalRed]]
            music = [0x11 if (region.Reward == RewardType.PendantGreen or region.Reward == RewardType.PendantNonGreen) else 0x16 for region in regions]
            self.patches += self.MusicPatches(regions, music)

    #IEnumerable<byte> RandomDungeonMusic() {
    #    while (true) yield return rnd.Next(2) == 0 ? (byte)0x11 : (byte)0x16;
    #}

    def MusicPatches(self, regions: List[IReward], music: List[int]):
        addresses = [self.MusicAddresses(region) for region in regions]
        associations = zip(addresses, music)
        return [(Snes(i), [association[1]]) for association in associations for i in association[0]]

    def MusicAddresses(self, region: IReward):
        regionMap = {
                        EasternPalace : [ 0x2D59A ],
                        DesertPalace : [ 0x2D59B, 0x2D59C, 0x2D59D, 0x2D59E ],
                        TowerOfHera : [ 0x2D5C5, 0x2907A, 0x28B8C ],
                        PalaceOfDarkness : [ 0x2D5B8 ],
                        SwampPalace : [ 0x2D5B7 ],
                        SkullWoods : [ 0x2D5BA, 0x2D5BB, 0x2D5BC, 0x2D5BD, 0x2D608, 0x2D609, 0x2D60A, 0x2D60B ],
                        ThievesTown : [ 0x2D5C6 ],
                        IcePalace : [ 0x2D5BF ],
                        MiseryMire : [ 0x2D5B9 ],
                        TurtleRock : [ 0x2D5C7, 0x2D5A7, 0x2D5AA, 0x2D5AB ],
                    }
        result = regionMap.get(type(region), None)
        if result is None:
            raise exception(f"Region {region} should not be a dungeon music region")
        else:
            return result

    def WritePrizeShuffle(self, dropPrizes):
        self.patches.append((Snes(0x6FA78), [e.value for e in dropPrizes.Packs]))
        self.patches.append((Snes(0x1DFBD4), [e.value for e in dropPrizes.TreePulls]))
        self.patches.append((Snes(0x6A9C8), [dropPrizes.CrabContinous.value]))
        self.patches.append((Snes(0x6A9C4), [dropPrizes.CrabFinal.value]))
        self.patches.append((Snes(0x6F993), [dropPrizes.Stun.value]))
        self.patches.append((Snes(0x1D82CC), [dropPrizes.Fish.value]))

        self.patches += self.EnemyPrizePackDistribution()

        #/* Pack drop chance */
        #/* Normal difficulty is 50%. 0 => 100%, 1 => 50%, 3 => 25% */
        nrPacks = 7
        probability = 1
        self.patches.append((Snes(0x6FA62), [probability] * nrPacks))

    def EnemyPrizePackDistribution(self):
        (prizePacks, duplicatePacks) = self.EnemyPrizePacks()

        n = sum(len(x[1]) for x in prizePacks)
        randomization = self.PrizePackRandomization(n, 1)
        patches = []
        for prizepack in prizePacks:
            (packs, randomization) = SplitOff(randomization, len(prizepack[1]))
            patches.append((prizepack[0], [(b | p) for b,p in zip(prizepack[1], packs)]))

        duplicates = [(d[1], p[1])
                        for d in duplicatePacks
                        for p in patches
                        if p[0] == d[0]]
        patches += duplicates

        return [(Snes(x[0]), x[1]) for x in patches]

    #/* Guarantees at least s of each prize pack, over a total of n packs.
    #* In each iteration, from the product n * m, use the guaranteed number
    #* at k, where k is the "row" (integer division by m), when k falls
    #* within the list boundary. Otherwise use the "column" (modulo by m)
    #* as the random element.
    #*/
    def PrizePackRandomization(self, n: int, s: int):
        m = 7
        g = list(range(0, m)) * s

        def randomization(n: int):
            result = []
            n = m * n
            while (n > 0):
                r = self.rnd.randrange(0, n)
                k = r // m
                result.append(g[k] if k < len(g) else r % m)
                if (k < len(g)): del g[k]
                n -= m
            return result

        return [(x + 1) for x in randomization(n)]

    #/* Todo: Deadrock turns into $8F Blob when powdered, but those "onion blobs" always drop prize pack 1. */
    def EnemyPrizePacks(self):
        offset = 0xDB632
        patches = [
            #/* sprite_prep */
            (0x6888D, [ 0x00 ]), #// Keese DW
            (0x688A8, [ 0x00 ]), #// Rope
            (0x68967, [ 0x00, 0x00 ]), #// Crow/Dacto
            (0x69125, [ 0x00, 0x00 ]), #// Red/Blue Hardhat Bettle
            #/* sprite properties */
            (offset+0x01, [ 0x90 ]), #// Vulture
            (offset+0x08, [ 0x00 ]), #// Octorok (One Way)
            (offset+0x0A, [ 0x00 ]), #// Octorok (Four Way)
            (offset+0x0D, [ 0x80, 0x90 ]), #// Buzzblob, Snapdragon
            (offset+0x11, [ 0x90, 0x90, 0x00 ]), #// Hinox, Moblin, Mini Helmasaur
            (offset+0x18, [ 0x90, 0x90 ]), #// Mini Moldorm, Poe/Hyu
            (offset+0x20, [ 0x00 ]), #// Sluggula
            (offset+0x22, [ 0x80, 0x00, 0x00 ]), #// Ropa, Red Bari, Blue Bari
            #// Blue Soldier/Tarus, Green Soldier, Red Spear Soldier
            #// Blue Assault Soldier, Red Assault Spear Soldier/Tarus
            #// Blue Archer, Green Archer
            #// Red Javelin Soldier, Red Bush Javelin Soldier
            #// Red Bomb Soldiers, Green Soldier Recruits,
            #// Geldman, Toppo
            (offset+0x41, [ 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x10, 0x90, 0x90, 0x80 ]),
            (offset+0x4F, [ 0x80 ]), #// Popo 2
            (offset+0x51, [ 0x80 ]), #// Armos
            (offset+0x55, [ 0x00, 0x00 ]), #// Ku, Zora
            (offset+0x58, [ 0x90 ]), #// Crab
            (offset+0x64, [ 0x80 ]), #// Devalant (Shooter)
            (offset+0x6A, [ 0x90, 0x90 ]), #// Ball N' Chain Trooper, Cannon Soldier
            (offset+0x6D, [ 0x80, 0x80 ]), #// Rat/Buzz, (Stal)Rope
            (offset+0x71, [ 0x80 ]), #// Leever
            (offset+0x7C, [ 0x90 ]), #// Initially Floating Stal
            (offset+0x81, [ 0xC0 ]), #// Hover
            #// Green Eyegore/Mimic, Red Eyegore/Mimic
            #// Detached Stalfos Body, Kodongo
            (offset+0x83, [ 0x10, 0x10, 0x10, 0x00 ]),
            (offset+0x8B, [ 0x10 ]), #// Gibdo
            (offset+0x8E, [ 0x00, 0x00 ]), #// Terrorpin, Blob
            (offset+0x91, [ 0x10 ]), #// Stalfos Knight
            (offset+0x99, [ 0x10 ]), #// Pengator
            (offset+0x9B, [ 0x10 ]), #// Wizzrobe
            #// Blue Zazak, Red Zazak, Stalfos
            #// Green Zirro, Blue Zirro, Pikit
            (offset+0xA5, [ 0x10, 0x10, 0x10, 0x80, 0x80, 0x80 ]),
            (offset+0xC7, [ 0x10 ]), #// Hokku-Bokku
            (offset+0xC9, [ 0x10 ]), #// Tektite
            (offset+0xD0, [ 0x10 ]), #// Lynel
            (offset+0xD3, [ 0x00 ]), #// Stal
            ]
        duplicates = [
            #/* Popo2 -> Popo. Popo is not used in vanilla Z3, but we duplicate from Popo2 just to be sure */
            (offset + 0x4F, offset + 0x4E),
        ]
        return (patches, duplicates)

    def WriteTexts(self, config: Config):
        regions = [region for region in self.myWorld.Regions if isinstance(region, IReward)]
        greenPendantDungeon = [region for region in regions if region.Reward == RewardType.PendantGreen][0]
        redCrystalDungeons = [region for region in regions if region.Reward == RewardType.CrystalRed]

        sahasrahla = Texts.SahasrahlaReveal(greenPendantDungeon)
        self.stringTable.SetSahasrahlaRevealText(sahasrahla)

        bombShop = Texts.BombShopReveal(redCrystalDungeons)
        self.stringTable.SetBombShopRevealText(bombShop)

        blind = Texts.Blind(self.rnd)
        self.stringTable.SetBlindText(blind)

        tavernMan = Texts.TavernMan(self.rnd)
        self.stringTable.SetTavernManText(tavernMan)

        ganon = Texts.GanonFirstPhase(self.rnd)
        self.stringTable.SetGanonFirstPhaseText(ganon)

        silversLocation = [loc for world in self.allWorlds for loc in world.Locations if loc.ItemIs(ItemType.SilverArrows, self.myWorld)]
        if len(silversLocation) == 0:      
            silvers = Texts.GanonThirdPhaseMulti(None, self.myWorld, self.silversWorldID, self.playerIDToNames[self.silversWorldID])
        else:
            silvers = Texts.GanonThirdPhaseMulti(silversLocation[0].Region, self.myWorld) if config.Multiworld else \
                        Texts.GanonThirdPhaseSingle(silversLocation[0].Region)
        self.stringTable.SetGanonThirdPhaseText(silvers)

        triforceRoom = Texts.TriforceRoom(self.rnd)
        self.stringTable.SetTriforceRoomText(triforceRoom)

    def WriteStringTable(self):
        #// Todo: v12, base table in asm, use move instructions in seed patch
        self.patches.append((Snes(0x1C8000), self.stringTable.GetPaddedBytes()))

    def WritePlayerNames(self):
        self.patches += [(0x385000 + (0 * 16), self.PlayerNameBytes("Archipelago"))]
        self.patches += [(0x385000 + (id * 16), self.PlayerNameBytes(name)) for name, id in self.playerNames.items() if id < 256]

    def PlayerNameBytes(self, name: str):
        name = (name[:16] if len(name) > 16 else name).center(16)
        return bytearray(name, 'utf8') 

    def WriteSeedData(self):
        configField1 =                                                                           \
            ((1 if self.myWorld.Config.Race else 0) << 15) |                                     \
            ((1 if self.myWorld.Config.Keysanity else 0) << 13) |                                \
            ((1 if self.myWorld.Config.Multiworld else 0) << 12) |                               \
            (self.myWorld.Config.Z3Logic.value << 10) |                                          \
            (self.myWorld.Config.SMLogic.value << 8) |                                           \
            (Patch.Major << 4) |                                                                 \
            (Patch.Minor << 0)

        configField2 =                                                                           \
            ((1 if self.myWorld.Config.SwordLocation else 0) << 14) |                            \
            ((1 if self.myWorld.Config.MorphLocation else 0) << 12) |                            \
            ((1 if self.myWorld.Config.Goal else 0) << 8)     

        self.patches.append((Snes(0x80FF50), getWordArray(self.myWorld.Id)))
        self.patches.append((Snes(0x80FF52), getWordArray(configField1)))
        self.patches.append((Snes(0x80FF54), getDoubleWordArray(self.seed)))
        self.patches.append((Snes(0x80FF58), getWordArray(configField2)))
        #/* Reserve the rest of the space for future use */
        self.patches.append((Snes(0x80FF5A), [0x00] * 6))
        self.patches.append((Snes(0x80FF60), bytearray(self.seedGuid, 'utf8')))
        self.patches.append((Snes(0x80FF80), bytearray(self.myWorld.Guid, 'utf8')))

    def WriteCommonFlags(self):
        #/* Common Combo Configuration flags at [asm]/config.asm */
        if (self.myWorld.Config.Multiworld):
            self.patches.append((Snes(0xF47000), getWordArray(0x0001)))
        if (self.myWorld.Config.Keysanity):
            self.patches.append((Snes(0xF47006), getWordArray(0x0001)))

    def WriteGameTitle(self):
        z3Glitch =  "N" if self.myWorld.Config.Z3Logic == Config.Z3Logic.Nmg else \
                    "O" if self.myWorld.Config.Z3Logic == Config.Z3Logic.Owg else \
                    "C"
        smGlitch =  "N" if self.myWorld.Config.SMLogic == Config.SMLogic.Normal else \
                    "H" if self.myWorld.Config.SMLogic == Config.SMLogic.Hard else \
                    "X"

        from Utils import __version__
        self.title = f"ZSM{Patch.Major}{Patch.Minor}{Patch.Patch}{__version__.replace('.', '')[0:3]}{z3Glitch}{smGlitch}{self.myWorld.Id}{self.seed:08x}".ljust(21)[:21]
        self.patches.append((Snes(0x00FFC0), bytearray(self.title, 'utf8')))
        self.patches.append((Snes(0x80FFC0), bytearray(self.title, 'utf8')))
    
    def WriteZ3KeysanityFlags(self):
        if (self.myWorld.Config.Keysanity):
            self.patches.append((Snes(0x40003B), [ 1 ])) #// MapMode #$00 = Always On (default) - #$01 = Require Map Item
            self.patches.append((Snes(0x400045), [ 0x0f ])) #// display ----dcba a: Small Keys, b: Big Key, c: Map, d: Compass
            self.patches.append((Snes(0x40016A), [ 0x01 ])) #// FreeItemText: db #$01 ; #00 = Off (default) - #$01 = On

    def WriteSMKeyCardDoors(self):
        plaquePlm = 0xd410
        plmTablePos = 0xf800

        if ( self.myWorld.Config.Keysanity):
            doorList = [
                            #// RoomId  Door Facing              yyxx  Keycard Event Type                   Plaque type               yyxx, Address (if 0 a dynamic PLM is created)
                            #// Crateria
                            [ 0x91F8, KeycardDoors.Right,      0x2601, KeycardEvents.CrateriaLevel1,        KeycardPlaque.Level1,   0x2400, 0x0000 ], #// Crateria - Landing Site - Door to gauntlet
                            [ 0x91F8, KeycardDoors.Left,       0x168E, KeycardEvents.CrateriaLevel1,        KeycardPlaque.Level1,   0x148F, 0x801E ], #// Crateria - Landing Site - Door to landing site PB
                            [ 0x948C, KeycardDoors.Left,       0x062E, KeycardEvents.CrateriaLevel2,        KeycardPlaque.Level2,   0x042F, 0x8222 ], #// Crateria - Before Moat - Door to moat (overwrite PB door)
                            [ 0x99BD, KeycardDoors.Left,       0x660E, KeycardEvents.CrateriaBoss,          KeycardPlaque.Boss,     0x640F, 0x8470 ], #// Crateria - Before G4 - Door to G4
                            [ 0x9879, KeycardDoors.Left,       0x062E, KeycardEvents.CrateriaBoss,          KeycardPlaque.Boss,     0x042F, 0x8420 ], #// Crateria - Before BT - Door to Bomb Torizo
                            
                            #// Brinstar
                            [ 0x9F11, KeycardDoors.Left,       0x060E, KeycardEvents.BrinstarLevel1,        KeycardPlaque.Level1,   0x040F, 0x8784 ], #// Brinstar - Blue Brinstar - Door to ceiling e-tank room

                            [ 0x9AD9, KeycardDoors.Right,      0xA601, KeycardEvents.BrinstarLevel2,        KeycardPlaque.Level2,   0xA400, 0x0000 ], #// Brinstar - Green Brinstar - Door to etecoon area                
                            [ 0x9D9C, KeycardDoors.Down,       0x0336, KeycardEvents.BrinstarBoss,          KeycardPlaque.Boss,     0x0234, 0x863A ], #// Brinstar - Pink Brinstar - Door to spore spawn                
                            [ 0xA130, KeycardDoors.Left,       0x161E, KeycardEvents.BrinstarLevel2,        KeycardPlaque.Level2,   0x141F, 0x881C ], #// Brinstar - Pink Brinstar - Door to wave gate e-tank
                            [ 0xA0A4, KeycardDoors.Left,       0x062E, KeycardEvents.BrinstarLevel2,        KeycardPlaque.Level2,   0x042F, 0x0000 ], #// Brinstar - Pink Brinstar - Door to spore spawn super

                            [ 0xA56B, KeycardDoors.Left,       0x161E, KeycardEvents.BrinstarBoss,          KeycardPlaque.Boss,     0x141F, 0x8A1A ], #// Brinstar - Before Kraid - Door to Kraid

                            #// Upper Norfair
                            [ 0xA7DE, KeycardDoors.Right,      0x3601, KeycardEvents.NorfairLevel1,         KeycardPlaque.Level1,   0x3400, 0x8B00 ], #// Norfair - Business Centre - Door towards Ice
                            [ 0xA923, KeycardDoors.Right,      0x0601, KeycardEvents.NorfairLevel1,         KeycardPlaque.Level1,   0x0400, 0x0000 ], #// Norfair - Pre-Crocomire - Door towards Ice

                            [ 0xA788, KeycardDoors.Left,       0x162E, KeycardEvents.NorfairLevel2,         KeycardPlaque.Level2,   0x142F, 0x8AEA ], #// Norfair - Lava Missile Room - Door towards Bubble Mountain
                            [ 0xAF72, KeycardDoors.Left,       0x061E, KeycardEvents.NorfairLevel2,         KeycardPlaque.Level2,   0x041F, 0x0000 ], #// Norfair - After frog speedway - Door to Bubble Mountain
                            [ 0xAEDF, KeycardDoors.Down,       0x0206, KeycardEvents.NorfairLevel2,         KeycardPlaque.Level2,   0x0204, 0x0000 ], #// Norfair - Below bubble mountain - Door to Bubble Mountain
                            [ 0xAD5E, KeycardDoors.Right,      0x0601, KeycardEvents.NorfairLevel2,         KeycardPlaque.Level2,   0x0400, 0x0000 ], #// Norfair - LN Escape - Door to Bubble Mountain
                            
                            [ 0xA923, KeycardDoors.Up,         0x2DC6, KeycardEvents.NorfairBoss,           KeycardPlaque.Boss,     0x2EC4, 0x8B96 ], #// Norfair - Pre-Crocomire - Door to Crocomire

                            #// Lower Norfair
                            [ 0xB4AD, KeycardDoors.Left,       0x160E, KeycardEvents.LowerNorfairLevel1,    KeycardPlaque.Level1,   0x140F, 0x0000 ], #// Lower Norfair - WRITG - Door to Amphitheatre
                            [ 0xAD5E, KeycardDoors.Left,       0x065E, KeycardEvents.LowerNorfairLevel1,    KeycardPlaque.Level1,   0x045F, 0x0000 ], #// Lower Norfair - Exit - Door to "Reverse LN Entry"
                            [ 0xB37A, KeycardDoors.Right,      0x0601, KeycardEvents.LowerNorfairBoss,      KeycardPlaque.Boss,     0x0400, 0x8EA6 ], #// Lower Norfair - Pre-Ridley - Door to Ridley

                            #// Maridia
                            [ 0xD0B9, KeycardDoors.Left,       0x065E, KeycardEvents.MaridiaLevel1,         KeycardPlaque.Level1,   0x045F, 0x0000 ], #// Maridia - Mt. Everest - Door to Pink Maridia
                            [ 0xD5A7, KeycardDoors.Right,      0x1601, KeycardEvents.MaridiaLevel1,         KeycardPlaque.Level1,   0x1400, 0x0000 ], #// Maridia - Aqueduct - Door towards Beach

                            [ 0xD617, KeycardDoors.Left,       0x063E, KeycardEvents.MaridiaLevel2,         KeycardPlaque.Level2,   0x043F, 0x0000 ], #// Maridia - Pre-Botwoon - Door to Botwoon
                            [ 0xD913, KeycardDoors.Right,      0x2601, KeycardEvents.MaridiaLevel2,         KeycardPlaque.Level2,   0x2400, 0x0000 ], #// Maridia - Pre-Colloseum - Door to post-botwoon

                            [ 0xD78F, KeycardDoors.Right,      0x2601, KeycardEvents.MaridiaBoss,           KeycardPlaque.Boss,     0x2400, 0xC73B ], #// Maridia - Precious Room - Door to Draygon

                            [ 0xDA2B, KeycardDoors.BossLeft,   0x164E, 0x00f0,                              KeycardPlaque.Null,     0x144F, 0x0000 ], #// Maridia - Change Cac Alley Door to Boss Door (prevents key breaking)

                            #// Wrecked Ship
                            [ 0x93FE, KeycardDoors.Left,       0x167E, KeycardEvents.WreckedShipLevel1,     KeycardPlaque.Level1,   0x147F, 0x0000 ], #// Wrecked Ship - Outside Wrecked Ship West - Door to Reserve Tank Check
                            [ 0x968F, KeycardDoors.Left,       0x060E, KeycardEvents.WreckedShipLevel1,     KeycardPlaque.Level1,   0x040F, 0x0000 ], #// Wrecked Ship - Outside Wrecked Ship West - Door to Bowling Alley
                            [ 0xCE40, KeycardDoors.Left,       0x060E, KeycardEvents.WreckedShipLevel1,     KeycardPlaque.Level1,   0x040F, 0x0000 ], #// Wrecked Ship - Gravity Suit - Door to Bowling Alley

                            [ 0xCC6F, KeycardDoors.Left,       0x064E, KeycardEvents.WreckedShipBoss,       KeycardPlaque.Boss,     0x044F, 0xC29D ], #// Wrecked Ship - Pre-Phantoon - Door to Phantoon   
            ]

            doorId = 0x0000
            for door in doorList:
                #/* When "Fast Ganon" is set, don't place the G4 Boss key door to enable faster games */
                if (door[0] == 0x99BD and self.myWorld.Config.Goal == Goal.FastGanonDefeatMotherBrain):
                    continue
                doorArgs = doorId | door[3] if door[4] != KeycardPlaque.Null else door[3]
                if (door[6] == 0):
                    #// Write dynamic door
                    doorData = []
                    for x in door[0:3]:
                        doorData += getWordArray(x)
                    doorData += getWordArray(doorArgs)
                    self.patches.append((Snes(0x8f0000 + plmTablePos), doorData))
                    plmTablePos += 0x08
                else:
                    #// Overwrite existing door
                    doorData = []
                    for x in door[1:3]:
                        doorData += getWordArray(x)
                    doorData += getWordArray(doorArgs)
                    self.patches.append((Snes(0x8f0000 + door[6]), doorData))
                    if((door[3] == KeycardEvents.BrinstarBoss and door[0] != 0x9D9C) or door[3] == KeycardEvents.LowerNorfairBoss or door[3] == KeycardEvents.MaridiaBoss or door[3] == KeycardEvents.WreckedShipBoss):
                        #// Overwrite the extra parts of the Gadora with a PLM that just deletes itself
                        self.patches.append((Snes(0x8f0000 + door[6] + 0x06), [ 0x2F, 0xB6, 0x00, 0x00, 0x00, 0x00, 0x2F, 0xB6, 0x00, 0x00, 0x00, 0x00 ]))

                #// Plaque data
                if (door[4] != KeycardPlaque.Null):
                    plaqueData = getWordArray(door[0]) + getWordArray(plaquePlm) + getWordArray(door[5]) + getWordArray(door[4])
                    self.patches.append((Snes(0x8f0000 + plmTablePos), plaqueData))
                    plmTablePos += 0x08
                doorId += 1

        #/* Write plaque showing SM bosses that needs to be killed */
        if (self.myWorld.Config.OpenTourian != OpenTourian.FourBosses):
            plaqueData = getWordArray(0xA5ED) + getWordArray(plaquePlm) + getWordArray(0x044F) + getWordArray(KeycardPlaque.Zero + self.myWorld.TourianBossTokens)
            self.patches.append((Snes(0x8f0000 + plmTablePos), plaqueData))
            plmTablePos += 0x08

        self.patches.append((Snes(0x8f0000 + plmTablePos), [ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ]))

    def WriteDiggingGameRng(self):
        digs = (self.rnd.randrange(30) + 1)
        self.patches.append((Snes(0x308020), [ digs ]))
        self.patches.append((Snes(0x1DFD95), [ digs ]))

    #// Removes Sword/Shield from Uncle by moving the tiles for
    #// sword/shield to his head and replaces them with his head.
    def WriteRemoveEquipmentFromUncle(self, item: Item):
        if (item.Type != ItemType.ProgressiveSword):
            self.patches += [
                    (Snes(0xDD263), [ 0x00, 0x00, 0xF6, 0xFF, 0x00, 0x0E ]),
                    (Snes(0xDD26B), [ 0x00, 0x00, 0xF6, 0xFF, 0x00, 0x0E ]),
                    (Snes(0xDD293), [ 0x00, 0x00, 0xF6, 0xFF, 0x00, 0x0E ]),
                    (Snes(0xDD29B), [ 0x00, 0x00, 0xF7, 0xFF, 0x00, 0x0E ]),
                    (Snes(0xDD2B3), [ 0x00, 0x00, 0xF6, 0xFF, 0x02, 0x0E ]),
                    (Snes(0xDD2BB), [ 0x00, 0x00, 0xF6, 0xFF, 0x02, 0x0E ]),
                    (Snes(0xDD2E3), [ 0x00, 0x00, 0xF7, 0xFF, 0x02, 0x0E ]),
                    (Snes(0xDD2EB), [ 0x00, 0x00, 0xF7, 0xFF, 0x02, 0x0E ]),
                    (Snes(0xDD31B), [ 0x00, 0x00, 0xE4, 0xFF, 0x08, 0x0E ]),
                    (Snes(0xDD323), [ 0x00, 0x00, 0xE4, 0xFF, 0x08, 0x0E ]),
                ]
        if (item.Type != ItemType.ProgressiveShield):
            self.patches += [
                    (Snes(0xDD253), [ 0x00, 0x00, 0xF6, 0xFF, 0x00, 0x0E ]),
                    (Snes(0xDD25B), [ 0x00, 0x00, 0xF6, 0xFF, 0x00, 0x0E ]),
                    (Snes(0xDD283), [ 0x00, 0x00, 0xF6, 0xFF, 0x00, 0x0E ]),
                    (Snes(0xDD28B), [ 0x00, 0x00, 0xF7, 0xFF, 0x00, 0x0E ]),
                    (Snes(0xDD2CB), [ 0x00, 0x00, 0xF6, 0xFF, 0x02, 0x0E ]),
                    (Snes(0xDD2FB), [ 0x00, 0x00, 0xF7, 0xFF, 0x02, 0x0E ]),
                    (Snes(0xDD313), [ 0x00, 0x00, 0xE4, 0xFF, 0x08, 0x0E ]),
                ]

    def WritePreOpenPyramid(self, goal: Goal):
        if (goal == Goal.FastGanonDefeatMotherBrain):
            self.patches.append((Snes(0x30808B), [0x01]))

    def WriteGanonInvicible(self, goal: Goal):
        #/* Defaults to $00 (never) at [asm]/z3/randomizer/tables.asm */
        valueMap =  {
                        Goal.DefeatBoth : 0x03,
                        Goal.FastGanonDefeatMotherBrain : 0x04,
                        Goal.AllDungeonsDefeatMotherBrain : 0x02
                    }
        value = valueMap.get(goal, None)
        if (value is None):
            raise exception(f"Unknown Ganon invincible value {goal}")
        else:
            self.patches.append((Snes(0x30803E), [value]))

    def WriteBossesNeeded(self, tourianBossTokens):
        self.patches.append((Snes(0xF47200), getWordArray(tourianBossTokens)))

    def WriteCrystalsNeeded(self, towerCrystals, ganonCrystals, goal: Goal):
        self.patches.append((Snes(0x30805E), [towerCrystals]))
        self.patches.append((Snes(0x30805F), [ganonCrystals]))

        self.stringTable.SetTowerRequirementText(f"You need {towerCrystals} crystals to enter Ganon's Tower.")
        if (goal == Goal.AllDungeonsDefeatMotherBrain):
            self.stringTable.SetGanonRequirementText(f"You need to complete all the dungeons and bosses to defeat Ganon.")
        else:
            self.stringTable.SetGanonRequirementText(f"You need {ganonCrystals} crystals to defeat Ganon.")

    def WriteRngBlock(self):
        #/* Repoint RNG Block */
        self.patches.append((0x420000, [self.rnd.randrange(0, 0x100) for x in range(0, 1024)]))

    def WriteSaveAndQuitFromBossRoom(self):
        #/* Defaults to $00 at [asm]/z3/randomizer/tables.asm */
        self.patches.append((Snes(0x308042), [ 0x01 ]))

    def WriteWorldOnAgahnimDeath(self):
        pass
        #/* Defaults to $01 at [asm]/z3/randomizer/tables.asm */
        #// Todo: Z3r major glitches disables this, reconsider extending or dropping with glitched logic later.
        #//patches.Add((Snes(0x3080A3), new byte[] { 0x01 }));

def Snes(addr: int):
    #/* Redirect hi bank $30 access into ExHiRom lo bank $40 */
    if (addr & 0xFF8000) == 0x308000:
        addr = 0x400000 | (addr & 0x7FFF)
    else: #/* General case, add ExHi offset for banks < $80, and collapse mirroring */
        addr = (0x400000 if addr < 0x800000 else 0)| (addr & 0x3FFFFF)
    if (addr > 0x600000):
        raise Exception(f"Unmapped pc address target ${addr:x}")
    return addr

def getWord(w):
    return (w & 0x00FF, (w & 0xFF00) >> 8)

def getWordArray(w):
    return [w & 0x00FF, (w & 0xFF00) >> 8]

def getDoubleWordArray(w):
    return [w & 0x000000FF, (w & 0x0000FF00) >> 8, (w & 0x00FF0000) >> 16, (w & 0xFF000000) >> 24]

"""
    byte[] UintBytes(int value) => BitConverter.GetBytes((uint)value);

    byte[] UshortBytes(int value) => BitConverter.GetBytes((ushort)value);

    byte[] AsAscii(string text) => Encoding.ASCII.GetBytes(text);

}

}
"""
def SplitOff(source: List[Any], count: int):
    head = source[:count]
    tail = source[count:]
    return (head, tail)
