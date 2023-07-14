from ....Region import SMRegion, IReward, RewardType
from ....Config import Config, SMLogic
from ....Location import Location, LocationType
from ....Item import Progression

class East(SMRegion, IReward):
    Name = "Norfair Lower East"
    Area = "Norfair Lower"

    def __init__(self, world, config: Config):
        super().__init__(world, config)
        self.Reward = RewardType.Null
        self.Locations = [
            Location(self, 74, 0x8F8FCA, LocationType.Visible, "Missile (lower Norfair above fire flea room)",
                lambda items: self.CanExit(items)),
            Location(self, 75, 0x8F8FD2, LocationType.Visible, "Power Bomb (lower Norfair above fire flea room)",
                lambda items: self.CanExit(items)) if self.Logic == SMLogic.Normal else \
                lambda items: self.CanExit(items) and items.CanPassBombPassages(),
            Location(self, 76, 0x8F90C0, LocationType.Visible, "Power Bomb (Power Bombs of shame)",
                lambda items: self.CanExit(items) and items.CanUsePowerBombs()),
            Location(self, 77, 0x8F9100, LocationType.Visible, "Missile (lower Norfair near Wave Beam)",
                lambda items: self.CanExit(items)) if self.Logic == SMLogic.Normal else \
                lambda items: self.CanExit(items) and items.Morph and items.CanDestroyBombWalls(),
            Location(self, 78, 0x8F9108, LocationType.Hidden, "Energy Tank, Ridley",
                lambda items: self.CanExit(items) and items.CardLowerNorfairBoss and items.CanUsePowerBombs() and items.Super),
            Location(self, 80, 0x8F9184, LocationType.Visible, "Energy Tank, Firefleas",
                lambda items: self.CanExit(items))
            ]

    def CanExit(self, items:Progression):
        if self.Logic == SMLogic.Normal:
                # /*Bubble Mountain*/
            return items.Morph and (items.CardNorfairL2 or (
                # /* Volcano Room and Blue Gate */
                items.Gravity) and items.Wave and (
                # /*Spikey Acid Snakes and Croc Escape*/
                items.Grapple or items.SpaceJump))
        else:
            # /*Vanilla LN Escape*/
            return (items.Morph and (items.CardNorfairL2 or # /*Bubble Mountain*/ 
                                        (items.Missile or items.Super or items.Wave) and # /* Blue Gate */
                                    (items.SpeedBooster or items.CanFly() or items.Grapple or items.HiJump and 
                                    (items.CanSpringBallJump() or items.Ice))) or # /*Frog Speedway or Croc Escape*/
                # /*Reverse Amphitheater*/
                    items.HasEnergyReserves(5))

    def CanEnter(self, items:Progression):
        if self.Logic == SMLogic.Normal:
            return items.Varia and items.CardLowerNorfairL1 and (
                    self.world.CanEnter("Norfair Upper East", items) and items.CanUsePowerBombs() and items.SpaceJump and items.Gravity or
                    items.CanAccessNorfairLowerPortal() and items.CanDestroyBombWalls() and items.Super and items.CanUsePowerBombs() and items.CanFly())
        else:
            return items.Varia and items.CardLowerNorfairL1 and (
                    self.world.CanEnter("Norfair Upper East", items) and items.CanUsePowerBombs() and (items.HiJump or items.Gravity) or
                    items.CanAccessNorfairLowerPortal() and items.CanDestroyBombWalls() and items.Super and (items.CanFly() or items.CanSpringBallJump() or items.SpeedBooster)) and (
                items.CanFly() or items.HiJump or items.CanSpringBallJump() or items.Ice and items.Charge) and (
                items.CanPassBombPassages() or items.ScrewAttack and items.SpaceJump)                     

    def CanComplete(self, items:Progression):
        return self.GetLocation("Energy Tank, Ridley").Available(items)