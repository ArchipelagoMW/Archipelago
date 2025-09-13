from enum import Enum
from typing import List

from .Patch import DropPrize
from .Region import RewardType
from .Config import OpenTower, GanonVulnerable, OpenTourian

class Medallion(Enum):
    Bombos = 0
    Ether = 1
    Quake = 2

class DropPrizeRecord:
    Packs: List[DropPrize]
    TreePulls: List[DropPrize]
    CrabContinous: DropPrize
    CrabFinal: DropPrize
    Stun: DropPrize
    Fish: DropPrize
    
    def __init__(self, Packs, TreePulls, CrabContinous, CrabFinal, Stun, Fish):
        self.Packs = Packs
        self.TreePulls = TreePulls
        self.CrabContinous = CrabContinous
        self.CrabFinal = CrabFinal
        self.Stun = Stun
        self.Fish = Fish

class WorldState:
    Rewards: List[RewardType]
    Medallions: List[Medallion]

    TowerCrystals: int
    GanonCrystals: int
    TourianBossTokens: int

    DropPrizes: DropPrizeRecord

    def __init__(self, config, rnd):
        self.Rewards = self.DistributeRewards(rnd)
        self.Medallions = self.GenerateMedallions(rnd)
        self.TowerCrystals = rnd.randint(0, 7) if config.OpenTower == OpenTower.Random else config.OpenTower.value
        self.GanonCrystals = rnd.randint(0, 7) if config.GanonVulnerable == GanonVulnerable.Random else config.GanonVulnerable.value
        self.TourianBossTokens = rnd.randint(0, 4) if config.OpenTourian == OpenTourian.Random else config.OpenTourian.value
        self.DropPrizes = self.ShuffleDropPrizes(rnd)

    @staticmethod
    def Generate(config, rnd):
        return WorldState(config, rnd)

    BaseRewards =   [
                        RewardType.PendantGreen, RewardType.PendantNonGreen, RewardType.PendantNonGreen, RewardType.CrystalRed, RewardType.CrystalRed,
                        RewardType.CrystalBlue, RewardType.CrystalBlue, RewardType.CrystalBlue, RewardType.CrystalBlue, RewardType.CrystalBlue,
                        RewardType.AnyBossToken, RewardType.AnyBossToken, RewardType.AnyBossToken, RewardType.AnyBossToken,
                    ]

    BossTokens =    [
                        RewardType.BossTokenKraid, RewardType.BossTokenPhantoon, RewardType.BossTokenDraygon, RewardType.BossTokenRidley
                    ]

    @staticmethod
    def DistributeRewards(rnd):
        #// Assign four rewards for SM using a "loot table", randomized result
        gen = WorldState.Distribution().Generate(lambda dist: dist.Hit(rnd.randrange(dist.Sum)))
        smRewards = [next(gen) for x in range(4)]
        
        #// Exclude the SM rewards to get the Z3 lineup
        z3Rewards = WorldState.BaseRewards[:]
        for reward in smRewards:
            z3Rewards.remove(reward)

        rnd.shuffle(z3Rewards)
        #// Replace "any token" with random specific tokens
        rewards = z3Rewards + smRewards
        tokens = WorldState.BossTokens[:]
        rnd.shuffle(tokens)
        rewards = [tokens.pop() if reward == RewardType.AnyBossToken else reward for reward in rewards]

        return rewards


    class Distribution:
        factor = 3

        def __init__(self, distribution = None, boss = None, blue = None, red = None, pend = None, green = None):
            self.Boss = 4 * self.factor
            self.Blue = 5 * self.factor
            self.Red = 2 * self.factor
            self.Pend = 2
            self.Green = 1

            if (distribution is not None): 
                self.Boss = distribution.Boss
                self.Blue = distribution.Blue
                self.Red = distribution.Red
                self.Pend = distribution.Pend
                self.Green = distribution.Green
            if (boss is not None): 
                self.Boss = boss
            if (blue is not None): 
                self.Blue = blue
            if (red is not None): 
                self.Red = red
            if (pend is not None): 
                self.Pend = pend
            if (green is not None): 
                self.Green = green
        
        @property
        def Sum(self):
            return self.Boss + self.Blue + self.Red + self.Pend + self.Green

        def Hit(self, p):
            p -= self.Boss
            if (p < 0): return (RewardType.AnyBossToken, WorldState.Distribution(self, boss = self.Boss - WorldState.Distribution.factor))
            p -= self.Blue
            if (p < 0): return (RewardType.CrystalBlue, WorldState.Distribution(self, blue = self.Blue - WorldState.Distribution.factor))
            p -= self.Red
            if (p < 0): return (RewardType.CrystalRed, WorldState.Distribution(self, red = self.Red - WorldState.Distribution.factor))
            p -= self.Pend
            if (p < 0): return (RewardType.PendantNonGreen, WorldState.Distribution(self, pend = self.Pend - 1))
            return (RewardType.PendantGreen, WorldState.Distribution(self, green = self.Green - 1))

        def Generate(self, func):
            result = None
            while (True):
                (result, newSelf) = func(self)
                self.Boss = newSelf.Boss
                self.Blue = newSelf.Blue
                self.Red = newSelf.Red
                self.Pend = newSelf.Pend
                self.Green = newSelf.Green
                yield result

    @staticmethod
    def GenerateMedallions(rnd):
        return  [
                    Medallion(rnd.randrange(3)),
                    Medallion(rnd.randrange(3)),
                ]

    BaseDropPrizes = [
                        DropPrize.Heart, DropPrize.Heart, DropPrize.Heart, DropPrize.Heart, DropPrize.Green, DropPrize.Heart, DropPrize.Heart, DropPrize.Green,         #// pack 1
                        DropPrize.Blue, DropPrize.Green, DropPrize.Blue, DropPrize.Red, DropPrize.Blue, DropPrize.Green, DropPrize.Blue, DropPrize.Blue,                #// pack 2
                        DropPrize.FullMagic, DropPrize.Magic, DropPrize.Magic, DropPrize.Blue, DropPrize.FullMagic, DropPrize.Magic, DropPrize.Heart, DropPrize.Magic,  #// pack 3
                        DropPrize.Bomb1, DropPrize.Bomb1, DropPrize.Bomb1, DropPrize.Bomb4, DropPrize.Bomb1, DropPrize.Bomb1, DropPrize.Bomb8, DropPrize.Bomb1,        #// pack 4
                        DropPrize.Arrow5, DropPrize.Heart, DropPrize.Arrow5, DropPrize.Arrow10, DropPrize.Arrow5, DropPrize.Heart, DropPrize.Arrow5, DropPrize.Arrow10,#// pack 5
                        DropPrize.Magic, DropPrize.Green, DropPrize.Heart, DropPrize.Arrow5, DropPrize.Magic, DropPrize.Bomb1, DropPrize.Green, DropPrize.Heart,       #// pack 6
                        DropPrize.Heart, DropPrize.Fairy, DropPrize.FullMagic, DropPrize.Red, DropPrize.Bomb8, DropPrize.Heart, DropPrize.Red, DropPrize.Arrow10,      #// pack 7
                        DropPrize.Green, DropPrize.Blue, DropPrize.Red,#// from pull trees
                        DropPrize.Green, DropPrize.Red,#// from prize crab
                        DropPrize.Green, #// stunned prize
                        DropPrize.Red,#// saved fish prize
                    ]

    @staticmethod
    def ShuffleDropPrizes(rnd):
        nrPackDrops = 8 * 7
        nrTreePullDrops = 3

        prizes = WorldState.BaseDropPrizes[:]
        rnd.shuffle(prizes)

        (packs, prizes) = (prizes[:nrPackDrops], prizes[nrPackDrops:])
        (treePulls, prizes) = (prizes[:nrTreePullDrops], prizes[nrTreePullDrops:])
        (crabContinous, crabFinalDrop, prizes) = (prizes[0], prizes[1], prizes[2:])
        (stun, prizes) = (prizes[0], prizes[1:])
        fish = prizes[0]
        return DropPrizeRecord(packs, treePulls, crabContinous, crabFinalDrop, stun, fish)

    @staticmethod
    def SplitOff(source, count):
        return (source[:count], source[count:])