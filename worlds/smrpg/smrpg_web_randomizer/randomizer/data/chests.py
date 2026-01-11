# Data module for chest data.

from ...randomizer.data import items
from ...randomizer.logic.utils import isclass_or_instance
from . import locations


# ******* Chest location classes

class Chest(locations.ItemLocation):
    """Subclass for treasure chest location."""
    ms_override = False


class NonCoinChest(Chest):
    """Subclass for chest that cannot contain coin items."""

    def item_allowed(self, item):
        """

        Args:
            item(randomizer.data.items.Item|type): Item to check.

        Returns:
            bool: True if the given item is allowed to be placed in this spot, False otherwise.

        """
        return super().item_allowed(item) and not isclass_or_instance(item, items.Coins)


class StarAllowedChest(Chest):
    """Subclass for chests that are in the same room as an invincibility star."""

    def item_allowed(self, item):
        """

        Args:
            item(randomizer.data.items.Item|type): Item to check.

        Returns:
            bool: True if the given item is allowed to be placed in this spot, False otherwise.

        """
        return super().item_allowed(item) or isclass_or_instance(item, items.InvincibilityStar)


class RoseTownGardenerChest(Chest):
    """Subclass for the Lazy Shell chests in Rose Town."""

    @staticmethod
    def can_access(inventory):
        return inventory.has_item(items.Seed) and inventory.has_item(items.Fertilizer)


class MolevilleMinesBackChest(Chest):
    """Subclass for the back chests in Moleville Mines requiring Bambino Bomb to access."""

    @staticmethod
    def can_access(inventory):
        return locations.can_access_mines_back(inventory)


class BowserDoorReward(Chest):
    """Subclass for Bowser door rewards because they can only be inventory items or you missed."""

    def item_allowed(self, item):
        """

        Args:
            item(randomizer.data.items.Item|type): Item to check.

        Returns:
            bool: True if the given item is allowed to be placed in this spot, False otherwise.

        """
        return super().item_allowed(item) and not isclass_or_instance(item, items.ChestReward)


# ******* NPC reward data classes

class Reward(locations.ItemLocation):
    """Subclass for NPC reward location."""

    def item_allowed(self, item):
        # NPC rewards cannot contain "You Missed!" or chest-only rewards.
        # FIXME: Non-KI NPC rewards don't work with progressive cards for now.  Remove this when fixed.
        return super().item_allowed(item) and not isclass_or_instance(item, (items.AltoCard, items.ChestReward))


class TreasureSellerReward(Reward):
    """Subclass for Moleville treasure seller NPC to check access.  Need to beat mines to unlock this."""

    @staticmethod
    def can_access(inventory):
        return locations.can_access_mines_back(inventory)


class BelomeTempleTreasure(Reward):
    """Subclass for Belome Temple rewards."""

    @staticmethod
    def can_access(inventory):
        return inventory.has_item(items.TempleKey)


# ****************************** Actual chest classes

# *** Mushroom Way

class MushroomWay1(Chest):
    area = locations.Area.MushroomWay
    addresses = [0x14b389]
    item = items.Coins5
    access = 1


class MushroomWay2(Chest):
    area = locations.Area.MushroomWay
    addresses = [0x14b38d]
    item = items.Coins8
    access = 1


class MushroomWay3(Chest):
    area = locations.Area.MushroomWay
    addresses = [0x14b3da]
    item = items.Flower
    access = 2


class MushroomWay4(Chest):
    area = locations.Area.MushroomWay
    addresses = [0x14b3de]
    item = items.RecoveryMushroom
    access = 1


class ToadRescue1(Reward):
    area = locations.Area.MushroomWay
    addresses = [0x1efedc]
    item = items.HoneySyrup
    access = 2


class ToadRescue2(Reward):
    area = locations.Area.MushroomWay
    addresses = [0x1efe1e]
    item = items.FlowerTab
    access = 2


class HammerBrosReward(Reward):
    area = locations.Area.MushroomWay
    addresses = [0x1e94c4]
    item = items.Hammer
    access = 3


# *** Mushroom Kingdom

class MushroomKingdomVault1(Chest):
    area = locations.Area.MushroomKingdom
    addresses = [0x148ad3]
    item = items.Coins10
    access = 1


class MushroomKingdomVault2(Chest):
    area = locations.Area.MushroomKingdom
    addresses = [0x148adf]
    item = items.RecoveryMushroom
    access = 1


class MushroomKingdomVault3(Chest):
    area = locations.Area.MushroomKingdom
    addresses = [0x148aeb]
    item = items.Flower
    access = 1


class WalletGuy1(Reward):
    area = locations.Area.MushroomKingdom
    addresses = [0x1e3765]
    item = items.FlowerTab
    missable = True
    access = 4


class WalletGuy2(Reward):
    area = locations.Area.MushroomKingdom
    addresses = [0x1e17de]
    item = items.FrogCoin
    missable = True
    access = 4


class MushroomKingdomStore(Reward):
    area = locations.Area.MushroomKingdom
    addresses = [0x1e65f8]
    item = items.PickMeUp
    access = 1


class PeachSurprise(Reward):
    area = locations.Area.MushroomKingdom
    addresses = [0x1e26b2]
    item = items.Mushroom
    access = 2


class InvasionFamily(Reward):
    area = locations.Area.MushroomKingdom
    addresses = [0x1e3a74, 0x1e39b9]
    item = items.FlowerTab
    missable = True
    access = 3


class InvasionGuestRoom(Reward):
    area = locations.Area.MushroomKingdom
    addresses = [0x1e3373]
    item = items.WakeUpPin
    missable = True
    access = 3


class InvasionGuard(Reward):
    area = locations.Area.MushroomKingdom
    addresses = [0x1e3514]
    item = items.FlowerTab
    missable = True
    access = 3


# *** Bandit's Way

class BanditsWay1(Chest):
    area = locations.Area.BanditsWay
    addresses = [0x14b535]
    item = items.KerokeroCola
    access = 1


class BanditsWay2(Chest):
    area = locations.Area.BanditsWay
    addresses = [0x1495ff]
    item = items.RecoveryMushroom
    access = 1


class BanditsWayStarChest(StarAllowedChest):
    area = locations.Area.BanditsWay
    addresses = [0x14964c]
    item = items.BanditsWayStar
    access = 1


class BanditsWayDogJump(StarAllowedChest):
    area = locations.Area.BanditsWay
    addresses = [0x149650]
    item = items.Flower
    access = 3


class BanditsWayCroco(Chest):
    area = locations.Area.BanditsWay
    addresses = [0x14b494]
    item = items.RecoveryMushroom
    access = 1


class Croco1Reward(Reward):
    area = locations.Area.BanditsWay
    addresses = [0x1e94f0]
    item = items.Wallet
    access = 3


# *** Kero Sewers

class KeroSewersPandoriteRoom(Chest):
    area = locations.Area.KeroSewers
    addresses = [0x149053]
    item = items.Flower
    access = 1


class KeroSewersStarChest(StarAllowedChest):
    area = locations.Area.KeroSewers
    addresses = [0x14901e]
    item = items.KeroSewersStar
    access = 1


class PandoriteReward(Reward):
    area = locations.Area.KeroSewers
    addresses = [0x1e950d]
    item = items.TrueformPin
    access = 3


# *** Midas River

class MidasRiverFirstTime(Reward):
    area = locations.Area.MidasRiver
    addresses = [0x205fd3]
    item = items.NokNokShell
    access = 3


# *** Tadpole Pond

class CricketPieReward(Reward):
    area = locations.Area.TadpolePond
    addresses = [0x1e6636]
    item = items.FroggieStick
    access = 3

    @staticmethod
    def can_access(inventory):
        return inventory.has_item(items.CricketPie)


class CricketJamReward(Reward):
    area = locations.Area.TadpolePond
    addresses = [0x1e6642]
    item = items.FrogCoin
    access = 3
    num_frog_coins = 10

    @staticmethod
    def can_access(inventory):
        return inventory.has_item(items.CricketJam)

    def get_patch(self):
        patch = super().get_patch()

        # If we're giving frog coins at this spot, write the number of frog coins to a special address.
        if isclass_or_instance(self.item, items.FrogCoin):
            patch.add_data(0x1e6650, self.num_frog_coins)
        # Otherwise extra bytes are needed to enable this spot to use the regular item granting subroutine.
        else:
            patch.add_data(0x1e6631, bytes([0x40, 0x66]))

        return patch


# *** Rose Way

class RoseWayPlatform(Chest):
    area = locations.Area.RoseWay
    addresses = [0x14973e]
    item = items.FrogCoin
    access = 2


# *** Rose Town

class RoseTownStore1(Chest):
    area = locations.Area.RoseTown
    addresses = [0x1499ad]
    item = items.Flower
    access = 1


class RoseTownStore2(Chest):
    area = locations.Area.RoseTown
    addresses = [0x1499b9]
    item = items.FrogCoin
    access = 1


class GardenerCloud1(RoseTownGardenerChest):
    area = locations.Area.RoseTownClouds
    addresses = [0x14de24]
    item = items.LazyShellArmor
    access = 4
    ms_override = True


class GardenerCloud2(RoseTownGardenerChest):
    area = locations.Area.RoseTownClouds
    addresses = [0x14de28]
    item = items.LazyShellWeapon
    access = 4
    ms_override = True


class RoseTownToad(Reward):
    area = locations.Area.RoseTown
    addresses = [0x1e6030]
    item = items.FlowerTab
    missable = True
    access = 3


class Gaz(Reward):
    area = locations.Area.RoseTown
    addresses = [0x1e61ff]
    item = items.FingerShot
    access = 3


# *** Forest Maze

class ForestMaze1(Chest):
    area = locations.Area.ForestMaze
    addresses = [0x14b75e]
    item = items.KerokeroCola
    access = 1


class ForestMaze2(Chest):
    area = locations.Area.ForestMaze
    addresses = [0x14b872]
    item = items.FrogCoin
    access = 1


class ForestMazeUnderground1(Chest):
    area = locations.Area.ForestMaze
    addresses = [0x14bb9d]
    item = items.KerokeroCola
    access = 1


class ForestMazeUnderground2(Chest):
    area = locations.Area.ForestMaze
    addresses = [0x14bba1]
    item = items.Flower
    access = 3


class ForestMazeUnderground3(Chest):
    area = locations.Area.ForestMaze
    addresses = [0x14bba5]
    item = items.YouMissed
    access = 2


class ForestMazeRedEssence(Chest):
    area = locations.Area.ForestMaze
    addresses = [0x14b841]
    item = items.RedEssence
    access = 2


# *** Pipe Vault

class PipeVaultSlide1(Chest):
    area = locations.Area.PipeVault
    addresses = [0x14a2b7]
    item = items.Flower
    access = 2


class PipeVaultSlide2(Chest):
    area = locations.Area.PipeVault
    addresses = [0x14a2c3]
    item = items.FrogCoin
    access = 2


class PipeVaultSlide3(Chest):
    area = locations.Area.PipeVault
    addresses = [0x14a2cf]
    item = items.FrogCoin
    access = 2


class PipeVaultNippers1(Chest):
    area = locations.Area.PipeVault
    addresses = [0x14a33e]
    item = items.Flower
    access = 2


class PipeVaultNippers2(Chest):
    area = locations.Area.PipeVault
    addresses = [0x14a34a]
    item = items.CoinsDoubleBig
    access = 2


class GoombaThumping1(Reward):
    area = locations.Area.PipeVault
    addresses = [0x1e3f9c]
    item = items.FlowerTab
    access = 3


class GoombaThumping2(Reward):
    area = locations.Area.PipeVault
    addresses = [0x1e3fae]
    item = items.FlowerJar
    access = 3


# *** Yo'ster Isle

class YosterIsleEntrance(Chest):
    area = locations.Area.YosterIsle
    addresses = [0x148b39]
    item = items.FrogCoin
    access = 3


# *** Moleville


class TreasureSeller1(TreasureSellerReward):
    area = locations.Area.Moleville
    addresses = [0x1f8ca5]
    item = items.LuckyJewel
    access = 4


class TreasureSeller2(TreasureSellerReward):
    area = locations.Area.Moleville
    addresses = [0x1f8cd1]
    item = items.MysteryEgg
    access = 4


class TreasureSeller3(TreasureSellerReward):
    area = locations.Area.Moleville
    addresses = [0x1f8cfd]
    item = items.FryingPan
    access = 4


# *** Moleville Mines

class MolevilleMinesStarChest(MolevilleMinesBackChest, StarAllowedChest):
    area = locations.Area.MolevilleMines
    addresses = [0x14c4af]
    item = items.MolevilleMinesStar
    access = 3


class MolevilleMinesCoins(MolevilleMinesBackChest):
    area = locations.Area.MolevilleMines
    addresses = [0x14c3c6]
    item = items.Coins150
    access = 3


class MolevilleMinesPunchinello1(MolevilleMinesBackChest):
    area = locations.Area.MolevilleMines
    addresses = [0x14c546]
    item = items.RecoveryMushroom
    access = 3


class MolevilleMinesPunchinello2(MolevilleMinesBackChest):
    area = locations.Area.MolevilleMines
    addresses = [0x14c552]
    item = items.Flower
    access = 3


class CrocoFlunkie1(Reward):
    area = locations.Area.MolevilleMines
    addresses = [0x202073]
    item = items.FlowerTab
    missable = True
    access = 3


class CrocoFlunkie2(Reward):
    area = locations.Area.MolevilleMines
    addresses = [0x2020cc]
    item = items.FlowerTab
    missable = True
    access = 3


class CrocoFlunkie3(Reward):
    area = locations.Area.MolevilleMines
    addresses = [0x202123]
    item = items.FlowerTab
    missable = True
    access = 3


# *** Booster Pass

class BoosterPass1(Chest):
    area = locations.Area.BoosterPass
    addresses = [0x149c62]
    item = items.Flower
    access = 2


class BoosterPass2(Chest):
    area = locations.Area.BoosterPass
    addresses = [0x149c6e]
    item = items.RockCandy
    access = 1


class BoosterPassSecret1(Chest):
    area = locations.Area.BoosterPass
    addresses = [0x14da32]
    item = items.FrogCoin
    access = 3


class BoosterPassSecret2(Chest):
    area = locations.Area.BoosterPass
    addresses = [0x14da36]
    item = items.Flower
    access = 3


class BoosterPassSecret3(Chest):
    area = locations.Area.BoosterPass
    addresses = [0x14da42]
    item = items.KerokeroCola
    access = 3


# *** Booster Tower

class BoosterTowerSpookum(Chest):
    area = locations.Area.BoosterTower
    addresses = [0x14b23e]
    item = items.FrogCoin
    access = 1


class BoosterTowerThwomp(Chest):
    area = locations.Area.BoosterTower
    addresses = [0x148c60]
    item = items.RecoveryMushroom
    access = 1


class BoosterTowerMasher(Reward):
    area = locations.Area.BoosterTower
    addresses = [0x1f9ce9]
    item = items.Masher
    access = 3


class BoosterTowerParachute(Chest):
    area = locations.Area.BoosterTower
    addresses = [0x148c2f]
    item = items.FrogCoin
    access = 1


class BoosterTowerZoomShoes(Chest):
    area = locations.Area.BoosterTower
    addresses = [0x148eac]
    item = items.ZoomShoes
    access = 3
    ms_override = True

    @staticmethod
    def can_access(inventory):
        return inventory.has_item(items.RoomKey)


class BoosterTowerTop1(NonCoinChest):
    area = locations.Area.BoosterTower
    addresses = [0x14b2d1]
    item = items.FrogCoin
    access = 2


class BoosterTowerTop2(Chest):
    area = locations.Area.BoosterTower
    addresses = [0x14b2e1]
    item = items.GoodieBag
    access = 2


class BoosterTowerTop3(Chest):
    area = locations.Area.BoosterTower
    addresses = [0x14b325]
    item = items.RecoveryMushroom
    access = 2


class BoosterTowerRailway(Reward):
    area = locations.Area.BoosterTower
    addresses = [0x1ee468]
    item = items.FlowerTab
    access = 2


class BoosterTowerChomp(Reward):
    area = locations.Area.BoosterTower
    addresses = [0x1ee27b]
    item = items.Chomp
    access = 3

    @staticmethod
    def can_access(inventory):
        return inventory.has_item(items.ElderKey)


class BoosterTowerCurtainGame(Reward):
    area = locations.Area.BoosterTower
    addresses = [0x1ef49b]
    item = items.Amulet
    access = 3
    missable = True  # Curtain minigame is not repeatable if failed.


# *** Marrymore

class MarrymoreInn(Chest):
    area = locations.Area.Marrymore
    addresses = [0x1485d7]
    item = items.FrogCoin
    access = 1


# *** Seaside Town

class SeasideTownRescue(Reward):
    area = locations.Area.SeasideTown
    addresses = [0x1ed6c7]
    item = items.FlowerBox
    access = 3

    @staticmethod
    def can_access(inventory):
        return inventory.has_item(items.ShedKey)


# *** Sea

class SeaStarChest(StarAllowedChest):
    area = locations.Area.Sea
    addresses = [0x14a458]
    item = items.SeaStar
    access = 1


class SeaSaveRoom1(Chest):
    area = locations.Area.Sea
    addresses = [0x14a40e]
    item = items.FrogCoin
    access = 1


class SeaSaveRoom2(Chest):
    area = locations.Area.Sea
    addresses = [0x14a412]
    item = items.Flower
    access = 1


class SeaSaveRoom3(Chest):
    area = locations.Area.Sea
    addresses = [0x14a416]
    item = items.RecoveryMushroom
    access = 1


class SeaSaveRoom4(Chest):
    area = locations.Area.Sea
    addresses = [0x14a42f]
    item = items.MaxMushroom
    access = 2


# *** Sunken Ship

class SunkenShipRatStairs(Chest):
    area = locations.Area.SunkenShip
    addresses = [0x14ac26]
    item = items.Coins100
    access = 1


class SunkenShipShop(Chest):
    area = locations.Area.SunkenShip
    addresses = [0x14ac70]
    item = items.Coins100
    access = 3


class SunkenShipCoins1(Chest):
    area = locations.Area.SunkenShip
    addresses = [0x14ad85]
    item = items.Coins100
    access = 3


class SunkenShipCoins2(Chest):
    area = locations.Area.SunkenShip
    addresses = [0x14ad89]
    item = items.Coins100
    access = 3


class SunkenShipCloneRoom(Chest):
    area = locations.Area.SunkenShip
    addresses = [0x14ae61]
    item = items.KerokeroCola
    access = 3


class SunkenShipFrogCoinRoom(Chest):
    area = locations.Area.SunkenShip
    addresses = [0x14aef5]
    item = items.FrogCoin
    access = 3


class SunkenShipHidonMushroom(Chest):
    area = locations.Area.SunkenShip
    addresses = [0x14af0e]
    item = items.RecoveryMushroom
    access = 3


class SunkenShipSafetyRing(Chest):
    area = locations.Area.SunkenShip
    addresses = [0x14af27]
    item = items.SafetyRing
    access = 3


class SunkenShipBandanaReds(Chest):
    area = locations.Area.SunkenShip
    addresses = [0x14895d]
    item = items.RecoveryMushroom
    access = 3


class SunkenShip3DMaze(Reward):
    area = locations.Area.SunkenShip
    addresses = [0x203b30]
    item = items.RoyalSyrup
    access = 3


class SunkenShipCannonballPuzzle(Reward):
    area = locations.Area.SunkenShip
    addresses = [0x203b57]
    item = items.Mushroom
    access = 2


class SunkenShipHidonReward(Reward):
    area = locations.Area.SunkenShip
    addresses = [0x1e979c]
    item = items.SafetyBadge
    access = 4


# *** Land's End

class LandsEndRedEssence(Chest):
    area = locations.Area.LandsEnd
    addresses = [0x14a4df]
    item = items.RedEssence
    access = 1


class LandsEndChowPit1(Chest):
    area = locations.Area.LandsEnd
    addresses = [0x14a51c]
    item = items.KerokeroCola
    access = 2


class LandsEndChowPit2(Chest):
    area = locations.Area.LandsEnd
    addresses = [0x14a528]
    item = items.FrogCoin
    access = 2


class LandsEndBeeRoom(Chest):
    area = locations.Area.LandsEnd
    addresses = [0x14a5a2]
    item = items.FrogCoin
    access = 2


class LandsEndSecret1(Chest):
    area = locations.Area.LandsEnd
    addresses = [0x14c1f4]
    item = items.FrogCoin
    access = 1


class LandsEndSecret2(Chest):
    area = locations.Area.LandsEnd
    addresses = [0x14c200]
    item = items.FrogCoin
    access = 1


class LandsEndShyAway(Chest):
    area = locations.Area.LandsEnd
    addresses = [0x14d932]
    item = items.RecoveryMushroom
    access = 1


class LandsEndStarChest1(StarAllowedChest):
    area = locations.Area.LandsEnd
    addresses = [0x14c069]
    item = items.LandsEndVolcanoStar
    access = 2


class LandsEndStarChest2(StarAllowedChest):
    area = locations.Area.LandsEnd
    addresses = [0x14c02c]
    item = items.LandsEndStar2
    access = 2


class LandsEndStarChest3(StarAllowedChest):
    area = locations.Area.LandsEnd
    addresses = [0x14c030]
    item = items.LandsEndStar3
    access = 3


class TroopaClimb(Reward):
    area = locations.Area.LandsEnd
    addresses = [0x1f5282]
    item = items.TroopaPin
    access = 3


# *** Belome Temple

class BelomeTempleFortuneTeller(Chest):
    area = locations.Area.BelomeTemple
    addresses = [0x14de81]
    item = items.Coins50
    access = 2


class BelomeTempleAfterFortune1(Chest):
    area = locations.Area.BelomeTemple
    addresses = [0x14df69]
    item = items.FrogCoin
    access = 2


class BelomeTempleAfterFortune2(Chest):
    area = locations.Area.BelomeTemple
    addresses = [0x14df6d]
    item = items.Coins150
    access = 2


class BelomeTempleAfterFortune3(Chest):
    area = locations.Area.BelomeTemple
    addresses = [0x14df79]
    item = items.FrogCoin
    access = 2


class BelomeTempleAfterFortune4(Chest):
    area = locations.Area.BelomeTemple
    addresses = [0x14df7d]
    item = items.FrogCoin
    access = 2


class BelomeTempleTreasure1(BelomeTempleTreasure):
    area = locations.Area.BelomeTemple
    addresses = [0x1f4fba]
    item = items.RoyalSyrup
    access = 3


class BelomeTempleTreasure2(BelomeTempleTreasure):
    area = locations.Area.BelomeTemple
    addresses = [0x1f4fc0]
    item = items.MaxMushroom
    access = 3


class BelomeTempleTreasure3(BelomeTempleTreasure):
    area = locations.Area.BelomeTemple
    addresses = [0x1f4fc6]
    item = items.FireBomb
    access = 3


# *** Monstro Town

class MonstroTownEntrance(Chest):
    area = locations.Area.MonstroTown
    addresses = [0x14c10d]
    item = items.FrogCoin
    access = 1


class JinxDojoReward(Reward):
    area = locations.Area.MonstroTown
    addresses = [0x1e982a]
    item = items.JinxBelt
    access = 4


class CulexReward(Reward):
    area = locations.Area.MonstroTown
    addresses = [0x1e98bf]
    item = items.QuartzCharm
    access = 4

    @staticmethod
    def can_access(inventory):
        return inventory.has_item(items.ShinyStone)


class SuperJumps30(Reward):
    area = locations.Area.MonstroTown
    addresses = [0x1f6b41, 0x1f6b6a]
    item = items.AttackScarf
    access = 4


class SuperJumps100(Reward):
    area = locations.Area.MonstroTown
    addresses = [0x1f6b8f]
    item = items.SuperSuit
    access = 4


class ThreeMustyFears(Reward):
    area = locations.Area.MonstroTown
    addresses = [0x1f7160]
    item = items.GhostMedal
    access = 4

    @staticmethod
    def can_access(inventory):
        return (inventory.has_item(items.BigBooFlag) and inventory.has_item(items.GreaperFlag) and
                inventory.has_item(items.DryBonesFlag))


# *** Bean Valley

class BeanValley1(Chest):
    area = locations.Area.BeanValley
    addresses = [0x14bde3]
    item = items.Flower
    access = 2


class BeanValley2(Chest):
    area = locations.Area.BeanValley
    addresses = [0x14bdef]
    item = items.FrogCoin
    access = 1


class BeanValleyBoxBoyRoom(NonCoinChest):
    area = locations.Area.BeanValley
    addresses = [0x14cc58]
    item = items.RedEssence
    access = 2


class BeanValleySlotRoom(NonCoinChest):
    area = locations.Area.BeanValley
    addresses = [0x14cf7e]
    item = items.KerokeroCola
    access = 2


class BeanValleyPiranhaPlants(Chest):
    area = locations.Area.BeanValley
    addresses = [0x14bdb6]
    item = items.FrogCoin
    access = 2


class BeanValleyBeanstalk(NonCoinChest):
    area = locations.Area.BeanValley
    addresses = [0x14d444]
    item = items.Flower
    access = 3


class BeanValleyCloud1(Chest):
    area = locations.Area.BeanValley
    addresses = [0x14d2f1]
    item = items.FrogCoin
    access = 3


class BeanValleyCloud2(NonCoinChest):
    area = locations.Area.BeanValley
    addresses = [0x14d2fd]
    item = items.RareScarf
    access = 3


class BeanValleyFall1(Chest):
    area = locations.Area.BeanValley
    addresses = [0x14d316]
    item = items.Flower
    access = 3


class BeanValleyFall2(NonCoinChest):
    area = locations.Area.BeanValley
    addresses = [0x14d322]
    item = items.Flower
    access = 3


# *** Nimbus Land

class NimbusLandShop(NonCoinChest):
    area = locations.Area.NimbusLand
    addresses = [0x14ce25]
    item = items.FrogCoin
    access = 1


class NimbusLandInn(Reward):
    area = locations.Area.NimbusLand
    addresses = [0x1e122c]
    item = items.RedEssence
    access = 3

    def item_allowed(self, item):
        """FIXME: This spot grants the same item twice, it must be one-time consumables only until item code fixed."""
        return super().item_allowed(item) and item.consumable and not item.reuseable


class NimbusCastleBeforeBirdo1(Chest):
    area = locations.Area.NimbusLand
    addresses = [0x14a088]
    item = items.Flower
    missable = True
    access = 1


class NimbusCastleBeforeBirdo2(Chest):
    area = locations.Area.NimbusLand
    addresses = [0x14eda7]
    item = items.FrogCoin
    access = 4


class NimbusCastleOutOfBounds1(NonCoinChest):
    area = locations.Area.NimbusLand
    addresses = [0x14db97]
    item = items.FrogCoin
    access = 2


class NimbusCastleOutOfBounds2(Chest):
    area = locations.Area.NimbusLand
    addresses = [0x14dba3]
    item = items.FrogCoin
    access = 2


class NimbusCastleSingleGoldBird(Chest):
    area = locations.Area.NimbusLand
    addresses = [0x149f47]
    item = items.RecoveryMushroom
    access = 1


class NimbusCastleStarChest(StarAllowedChest):
    area = locations.Area.NimbusLand
    addresses = [0x14a1a3]
    item = items.NimbusLandStar
    missable = True
    access = 4

    @staticmethod
    def can_access(inventory):
        return locations.can_clear_nimbus_castle(inventory)


class NimbusCastleStarAfterValentina(Chest):
    area = locations.Area.NimbusLand
    addresses = [0x14a1af]
    item = items.Flower
    access = 4

    @staticmethod
    def can_access(inventory):
        return locations.can_clear_nimbus_castle(inventory)


class DodoReward(Reward):
    area = locations.Area.NimbusLand
    addresses = [0x20936a]
    item = items.Feather
    access = 3


class NimbusLandPrisoners(Reward):
    area = locations.Area.NimbusLand
    addresses = [0x20a9c5]
    item = items.FlowerJar
    missable = True
    access = 3


class NimbusLandSignalRing(Reward):
    area = locations.Area.NimbusLand
    addresses = [0x20a456]
    item = items.SignalRing
    access = 4

    @staticmethod
    def can_access(inventory):
        return locations.can_clear_nimbus_castle(inventory)


class NimbusLandCellar(Reward):
    area = locations.Area.NimbusLand
    addresses = [0x1ea732]
    item = items.FlowerJar
    access = 4

    @staticmethod
    def can_access(inventory):
        return locations.can_clear_nimbus_castle(inventory)


# *** Barrel Volcano

class BarrelVolcanoSecret1(Chest):
    area = locations.Area.BarrelVolcano
    addresses = [0x14d048]
    item = items.Flower
    access = 2


class BarrelVolcanoSecret2(Chest):
    area = locations.Area.BarrelVolcano
    addresses = [0x14d04c]
    item = items.Flower
    access = 2


class BarrelVolcanoBeforeStar1(Chest):
    area = locations.Area.BarrelVolcano
    addresses = [0x14d595]
    item = items.Flower
    access = 1


class BarrelVolcanoBeforeStar2(Chest):
    area = locations.Area.BarrelVolcano
    addresses = [0x14d5a1]
    item = items.Coins100
    access = 1


class BarrelVolcanoStarRoom(StarAllowedChest):
    area = locations.Area.BarrelVolcano
    addresses = [0x14d5ce]
    item = items.LandsEndVolcanoStar
    access = 1


class BarrelVolcanoSaveRoom1(Chest):
    area = locations.Area.BarrelVolcano
    addresses = [0x14d203]
    item = items.Flower
    access = 2


class BarrelVolcanoSaveRoom2(Chest):
    area = locations.Area.BarrelVolcano
    addresses = [0x14d207]
    item = items.FrogCoin
    access = 2


class BarrelVolcanoHinnopio(Chest):
    area = locations.Area.BarrelVolcano
    addresses = [0x14d220]
    item = items.Coins100
    access = 2


# *** Bowser's Keep

class BowsersKeepDarkRoom(Chest):
    area = locations.Area.BowsersKeep
    addresses = [0x14e3b1]
    item = items.RecoveryMushroom
    access = 1


class BowsersKeepCrocoShop1(Chest):
    area = locations.Area.BowsersKeep
    addresses = [0x14e37f]
    item = items.Coins150
    access = 1


class BowsersKeepCrocoShop2(Chest):
    area = locations.Area.BowsersKeep
    addresses = [0x14e38b]
    item = items.RecoveryMushroom
    access = 1
    not_depletable = True


class BowsersKeepInvisibleBridge1(Chest):
    area = locations.Area.BowsersKeep
    addresses = [0x14c9b3]
    item = items.FrightBomb
    access = 2


class BowsersKeepInvisibleBridge2(Chest):
    area = locations.Area.BowsersKeep
    addresses = [0x14c9b7]
    item = items.RoyalSyrup
    access = 2


class BowsersKeepInvisibleBridge3(Chest):
    area = locations.Area.BowsersKeep
    addresses = [0x14c9bb]
    item = items.IceBomb
    access = 2


class BowsersKeepInvisibleBridge4(Chest):
    area = locations.Area.BowsersKeep
    addresses = [0x14c9bf]
    item = items.RockCandy
    access = 2


class BowsersKeepMovingPlatforms1(Chest):
    area = locations.Area.BowsersKeep
    addresses = [0x14e536]
    item = items.Flower
    access = 3


class BowsersKeepMovingPlatforms2(Chest):
    area = locations.Area.BowsersKeep
    addresses = [0x14e542]
    item = items.RedEssence
    access = 3


class BowsersKeepMovingPlatforms3(Chest):
    area = locations.Area.BowsersKeep
    addresses = [0x14e546]
    item = items.MaxMushroom
    access = 3


class BowsersKeepMovingPlatforms4(Chest):
    area = locations.Area.BowsersKeep
    addresses = [0x14e54a]
    item = items.FireBomb
    access = 3


class BowsersKeepElevatorPlatforms(Chest):
    area = locations.Area.BowsersKeep
    addresses = [0x14c97a]
    item = items.KerokeroCola
    access = 2


class BowsersKeepCannonballRoom1(Chest):
    area = locations.Area.BowsersKeep
    addresses = [0x14e4b1]
    item = items.Flower
    access = 2


class BowsersKeepCannonballRoom2(Chest):
    area = locations.Area.BowsersKeep
    addresses = [0x14e4b5]
    item = items.Flower
    access = 2


class BowsersKeepCannonballRoom3(Chest):
    area = locations.Area.BowsersKeep
    addresses = [0x14e4c1]
    item = items.PickMeUp
    access = 2


class BowsersKeepCannonballRoom4(Chest):
    area = locations.Area.BowsersKeep
    addresses = [0x14e4c5]
    item = items.RockCandy
    access = 2


class BowsersKeepCannonballRoom5(Chest):
    area = locations.Area.BowsersKeep
    addresses = [0x14e4c9]
    item = items.MaxMushroom
    access = 2


class BowsersKeepRotatingPlatforms1(Chest):
    area = locations.Area.BowsersKeep
    addresses = [0x14e3ff]
    item = items.Flower
    access = 2


class BowsersKeepRotatingPlatforms2(Chest):
    area = locations.Area.BowsersKeep
    addresses = [0x14e403]
    item = items.Flower
    access = 3


class BowsersKeepRotatingPlatforms3(Chest):
    area = locations.Area.BowsersKeep
    addresses = [0x14e40f]
    item = items.FireBomb
    access = 3


class BowsersKeepRotatingPlatforms4(Chest):
    area = locations.Area.BowsersKeep
    addresses = [0x14e413]
    item = items.RoyalSyrup
    access = 2


class BowsersKeepRotatingPlatforms5(Chest):
    area = locations.Area.BowsersKeep
    addresses = [0x14e417]
    item = items.PickMeUp
    access = 3


class BowsersKeepRotatingPlatforms6(Chest):
    area = locations.Area.BowsersKeep
    addresses = [0x14e41b]
    item = items.KerokeroCola
    access = 2


class BowsersKeepDoorReward1(BowserDoorReward):
    area = locations.Area.BowsersKeep
    addresses = [0x204bfc]
    item = items.SonicCymbal
    access = 4


class BowsersKeepDoorReward2(BowserDoorReward):
    area = locations.Area.BowsersKeep
    addresses = [0x204c02]
    item = items.SuperSlap
    access = 4


class BowsersKeepDoorReward3(BowserDoorReward):
    area = locations.Area.BowsersKeep
    addresses = [0x204c08]
    item = items.DrillClaw
    access = 4


class BowsersKeepDoorReward4(BowserDoorReward):
    area = locations.Area.BowsersKeep
    addresses = [0x204c0e]
    item = items.StarGun
    access = 4


class BowsersKeepDoorReward5(BowserDoorReward):
    area = locations.Area.BowsersKeep
    addresses = [0x204c14]
    item = items.RockCandy
    access = 4


class BowsersKeepDoorReward6(BowserDoorReward):
    area = locations.Area.BowsersKeep
    addresses = [0x204c1a]
    item = items.RockCandy
    access = 4


# *** Factory

class FactorySaveRoom(Chest):
    area = locations.Area.Factory
    addresses = [0x14bafa]
    item = items.RecoveryMushroom
    access = 4


class FactoryBoltPlatforms(Chest):
    area = locations.Area.Factory
    addresses = [0x14bb6c]
    item = items.UltraHammer
    access = 4


class FactoryFallingAxems(Chest):
    area = locations.Area.Factory
    addresses = [0x14e0c8]
    item = items.RecoveryMushroom
    access = 4


class FactoryTreasurePit1(Chest):
    area = locations.Area.Factory
    addresses = [0x14e2c4]
    item = items.RecoveryMushroom
    access = 4


class FactoryTreasurePit2(NonCoinChest):
    area = locations.Area.Factory
    addresses = [0x14e2cc]
    item = items.Flower
    access = 4


class FactoryConveyorPlatforms1(Chest):
    area = locations.Area.Factory
    addresses = [0x14e9cb]
    item = items.RoyalSyrup
    access = 4


class FactoryConveyorPlatforms2(Chest):
    area = locations.Area.Factory
    addresses = [0x14e9cf]
    item = items.MaxMushroom
    access = 4


class FactoryBehindSnakes1(Chest):
    area = locations.Area.Factory
    addresses = [0x14e2c8]
    item = items.RecoveryMushroom
    access = 4


class FactoryBehindSnakes2(Chest):
    area = locations.Area.Factory
    addresses = [0x14e2d0]
    item = items.Flower
    access = 4


class FactoryToadGift(Reward):
    area = locations.Area.Factory
    addresses = [0x1ff7ed]
    item = items.RockCandy
    access = 4


# ********************* Default objects for world

def get_default_chests(world):
    """Get default vanilla chest and reward list for the world.

    Args:
        world (randomizer.logic.main.GameWorld):

    Returns:
        list[ItemLocation]: List of default chest objects.
    """
    return [
        # Chests
        MushroomWay1(world),
        MushroomWay2(world),
        MushroomWay3(world),
        MushroomWay4(world),
        MushroomKingdomVault1(world),
        MushroomKingdomVault2(world),
        MushroomKingdomVault3(world),
        BanditsWay1(world),
        BanditsWay2(world),
        BanditsWayStarChest(world),
        BanditsWayDogJump(world),
        BanditsWayCroco(world),
        KeroSewersPandoriteRoom(world),
        KeroSewersStarChest(world),
        RoseWayPlatform(world),
        RoseTownStore1(world),
        RoseTownStore2(world),
        GardenerCloud1(world),
        GardenerCloud2(world),
        ForestMaze1(world),
        ForestMaze2(world),
        ForestMazeUnderground1(world),
        ForestMazeUnderground2(world),
        ForestMazeUnderground3(world),
        ForestMazeRedEssence(world),
        PipeVaultSlide1(world),
        PipeVaultSlide2(world),
        PipeVaultSlide3(world),
        PipeVaultNippers1(world),
        PipeVaultNippers2(world),
        YosterIsleEntrance(world),
        MolevilleMinesStarChest(world),
        MolevilleMinesCoins(world),
        MolevilleMinesPunchinello1(world),
        MolevilleMinesPunchinello2(world),
        BoosterPass1(world),
        BoosterPass2(world),
        BoosterPassSecret1(world),
        BoosterPassSecret2(world),
        BoosterPassSecret3(world),
        BoosterTowerSpookum(world),
        BoosterTowerThwomp(world),
        BoosterTowerMasher(world),
        BoosterTowerParachute(world),
        BoosterTowerZoomShoes(world),
        BoosterTowerTop1(world),
        BoosterTowerTop2(world),
        BoosterTowerTop3(world),
        MarrymoreInn(world),
        SeaStarChest(world),
        SeaSaveRoom1(world),
        SeaSaveRoom2(world),
        SeaSaveRoom3(world),
        SeaSaveRoom4(world),
        SunkenShipRatStairs(world),
        SunkenShipShop(world),
        SunkenShipCoins1(world),
        SunkenShipCoins2(world),
        SunkenShipCloneRoom(world),
        SunkenShipFrogCoinRoom(world),
        SunkenShipHidonMushroom(world),
        SunkenShipSafetyRing(world),
        SunkenShipBandanaReds(world),
        LandsEndRedEssence(world),
        LandsEndChowPit1(world),
        LandsEndChowPit2(world),
        LandsEndBeeRoom(world),
        LandsEndSecret1(world),
        LandsEndSecret2(world),
        LandsEndShyAway(world),
        LandsEndStarChest1(world),
        LandsEndStarChest2(world),
        LandsEndStarChest3(world),
        BelomeTempleFortuneTeller(world),
        BelomeTempleAfterFortune1(world),
        BelomeTempleAfterFortune2(world),
        BelomeTempleAfterFortune3(world),
        BelomeTempleAfterFortune4(world),
        MonstroTownEntrance(world),
        BeanValley1(world),
        BeanValley2(world),
        BeanValleyBoxBoyRoom(world),
        BeanValleySlotRoom(world),
        BeanValleyPiranhaPlants(world),
        BeanValleyBeanstalk(world),
        BeanValleyCloud1(world),
        BeanValleyCloud2(world),
        BeanValleyFall1(world),
        BeanValleyFall2(world),
        NimbusLandShop(world),
        NimbusCastleBeforeBirdo1(world),
        NimbusCastleBeforeBirdo2(world),
        NimbusCastleOutOfBounds1(world),
        NimbusCastleOutOfBounds2(world),
        NimbusCastleSingleGoldBird(world),
        NimbusCastleStarChest(world),
        NimbusCastleStarAfterValentina(world),
        BarrelVolcanoSecret1(world),
        BarrelVolcanoSecret2(world),
        BarrelVolcanoBeforeStar1(world),
        BarrelVolcanoBeforeStar2(world),
        BarrelVolcanoStarRoom(world),
        BarrelVolcanoSaveRoom1(world),
        BarrelVolcanoSaveRoom2(world),
        BarrelVolcanoHinnopio(world),
        BowsersKeepDarkRoom(world),
        BowsersKeepCrocoShop1(world),
        BowsersKeepCrocoShop2(world),
        BowsersKeepInvisibleBridge1(world),
        BowsersKeepInvisibleBridge2(world),
        BowsersKeepInvisibleBridge3(world),
        BowsersKeepInvisibleBridge4(world),
        BowsersKeepMovingPlatforms1(world),
        BowsersKeepMovingPlatforms2(world),
        BowsersKeepMovingPlatforms3(world),
        BowsersKeepMovingPlatforms4(world),
        BowsersKeepElevatorPlatforms(world),
        BowsersKeepCannonballRoom1(world),
        BowsersKeepCannonballRoom2(world),
        BowsersKeepCannonballRoom3(world),
        BowsersKeepCannonballRoom4(world),
        BowsersKeepCannonballRoom5(world),
        BowsersKeepRotatingPlatforms1(world),
        BowsersKeepRotatingPlatforms2(world),
        BowsersKeepRotatingPlatforms3(world),
        BowsersKeepRotatingPlatforms4(world),
        BowsersKeepRotatingPlatforms5(world),
        BowsersKeepRotatingPlatforms6(world),
        BowsersKeepDoorReward1(world),
        BowsersKeepDoorReward2(world),
        BowsersKeepDoorReward3(world),
        BowsersKeepDoorReward4(world),
        BowsersKeepDoorReward5(world),
        BowsersKeepDoorReward6(world),
        FactorySaveRoom(world),
        FactoryBoltPlatforms(world),
        FactoryFallingAxems(world),
        FactoryTreasurePit1(world),
        FactoryTreasurePit2(world),
        FactoryConveyorPlatforms1(world),
        FactoryConveyorPlatforms2(world),
        FactoryBehindSnakes1(world),
        FactoryBehindSnakes2(world),

        # NPC rewards
        ToadRescue1(world),
        ToadRescue2(world),
        HammerBrosReward(world),
        WalletGuy1(world),
        WalletGuy2(world),
        MushroomKingdomStore(world),
        PeachSurprise(world),
        InvasionFamily(world),
        InvasionGuestRoom(world),
        InvasionGuard(world),
        Croco1Reward(world),
        PandoriteReward(world),
        MidasRiverFirstTime(world),
        RoseTownToad(world),
        Gaz(world),
        TreasureSeller1(world),
        TreasureSeller2(world),
        TreasureSeller3(world),
        CrocoFlunkie1(world),
        CrocoFlunkie2(world),
        CrocoFlunkie3(world),
        BoosterTowerRailway(world),
        BoosterTowerChomp(world),
        BoosterTowerCurtainGame(world),
        SeasideTownRescue(world),
        SunkenShip3DMaze(world),
        SunkenShipCannonballPuzzle(world),
        SunkenShipHidonReward(world),
        BelomeTempleTreasure1(world),
        BelomeTempleTreasure2(world),
        BelomeTempleTreasure3(world),
        JinxDojoReward(world),
        CulexReward(world),
        SuperJumps30(world),
        SuperJumps100(world),
        ThreeMustyFears(world),
        TroopaClimb(world),
        DodoReward(world),
        NimbusLandInn(world),
        NimbusLandPrisoners(world),
        NimbusLandSignalRing(world),
        NimbusLandCellar(world),
        FactoryToadGift(world),
        GoombaThumping1(world),
        GoombaThumping2(world),
        CricketPieReward(world),
        CricketJamReward(world),
    ]
