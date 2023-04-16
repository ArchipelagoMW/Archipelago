from ....Region import SMRegion, IReward, RewardType
from ....Config import Config, SMLogic
from ....Location import Location, LocationType
from ....Item import Progression

class Inner(SMRegion, IReward):
    Name = "Maridia Inner"
    Area = "Maridia"

    def __init__(self, world, config: Config):
        super().__init__(world, config)
        self.Reward = RewardType.Null
        self.Locations = [
            Location(self, 140, 0x8FC4AF, LocationType.Visible, "Super Missile (yellow Maridia)",
                lambda items: items.CardMaridiaL1 and items.CanPassBombPassages() and self.CanReachAqueduct(items) and
                    (items.Gravity or items.Ice or items.HiJump and items.SpringBall)),
            Location(self, 141, 0x8FC4B5, LocationType.Visible, "Missile (yellow Maridia super missile)",
                lambda items: items.CardMaridiaL1 and items.CanPassBombPassages() and
                    (items.Gravity or items.Ice or items.HiJump and items.SpringBall)),
            Location(self, 142, 0x8FC533, LocationType.Visible, "Missile (yellow Maridia false wall)",
                lambda items: items.CardMaridiaL1 and items.CanPassBombPassages() and
                    (items.Gravity or items.Ice or items.HiJump and items.SpringBall)),
            Location(self, 143, 0x8FC559, LocationType.Chozo, "Plasma Beam",
                lambda items: self.CanDefeatDraygon(items) and (items.ScrewAttack or items.Plasma) and (items.HiJump or items.CanFly()) if self.Logic == SMLogic.Normal else \
                lambda items: self.CanDefeatDraygon(items) and
                    (items.Charge and items.HasEnergyReserves(3) or items.ScrewAttack or items.Plasma or items.SpeedBooster) and
                    (items.HiJump or items.CanSpringBallJump() or items.CanFly() or items.SpeedBooster)),
            Location(self, 144, 0x8FC5DD, LocationType.Visible, "Missile (left Maridia sand pit room)",
                lambda items: self.CanReachAqueduct(items) and items.Super and items.CanPassBombPassages() if self.Logic == SMLogic.Normal else \
                lambda items: self.CanReachAqueduct(items) and items.Super and
                    (items.Gravity or items.HiJump and (items.SpaceJump or items.CanSpringBallJump()))),
            Location(self, 145, 0x8FC5E3, LocationType.Chozo, "Reserve Tank, Maridia",
                lambda items: self.CanReachAqueduct(items) and items.Super and items.CanPassBombPassages() if self.Logic == SMLogic.Normal else \
                lambda items: self.CanReachAqueduct(items) and items.Super and
                    (items.Gravity or items.HiJump and (items.SpaceJump or items.CanSpringBallJump()))),
            Location(self, 146, 0x8FC5EB, LocationType.Visible, "Missile (right Maridia sand pit room)",
                lambda items: self.CanReachAqueduct(items) and items.Super) if self.Logic == SMLogic.Normal else \
                lambda items: self.CanReachAqueduct(items) and items.Super and (items.HiJump or items.Gravity),
            Location(self, 147, 0x8FC5F1, LocationType.Visible, "Power Bomb (right Maridia sand pit room)",
                lambda items: self.CanReachAqueduct(items) and items.Super) if self.Logic == SMLogic.Normal else \
                lambda items: self.CanReachAqueduct(items) and items.Super and (items.Gravity or items.HiJump and items.CanSpringBallJump()),
            Location(self, 148, 0x8FC603, LocationType.Visible, "Missile (pink Maridia)", 
                lambda items: self.CanReachAqueduct(items) and items.SpeedBooster if self.Logic == SMLogic.Normal else \
                lambda items: self.CanReachAqueduct(items) and items.Gravity),
            Location(self, 149, 0x8FC609, LocationType.Visible, "Super Missile (pink Maridia)",
                lambda items: self.CanReachAqueduct(items) and items.SpeedBooster if self.Logic == SMLogic.Normal else \
                lambda items: self.CanReachAqueduct(items) and items.Gravity),
            Location(self, 150, 0x8FC6E5, LocationType.Chozo, "Spring Ball",
                lambda items: items.Super and items.Grapple and items.CanUsePowerBombs() and (items.SpaceJump or items.HiJump) if self.Logic == SMLogic.Normal else \
                lambda items: items.Super and items.Grapple and items.CanUsePowerBombs() and (
                    items.Gravity and (items.CanFly() or items.HiJump) or
                    items.Ice and items.HiJump and items.CanSpringBallJump() and items.SpaceJump)),
            Location(self, 151, 0x8FC74D, LocationType.Hidden, "Missile (Draygon)",
                lambda items: 
                    items.CardMaridiaL1 and items.CardMaridiaL2 and self.CanDefeatBotwoon(items) or
                    items.CanAccessMaridiaPortal(self.world) if self.Logic == SMLogic.Normal else \
                lambda items: (
                        items.CardMaridiaL1 and items.CardMaridiaL2 and self.CanDefeatBotwoon(items) or
                        items.CanAccessMaridiaPortal(self.world)
                    ) and items.Gravity),
            Location(self, 152, 0x8FC755, LocationType.Visible, "Energy Tank, Botwoon",
                lambda items: 
                    items.CardMaridiaL1 and items.CardMaridiaL2 and self.CanDefeatBotwoon(items) or
                    items.CanAccessMaridiaPortal(self.world) and items.CardMaridiaL2),
            Location(self, 154, 0x8FC7A7, LocationType.Chozo, "Space Jump",
                lambda items: self.CanDefeatDraygon(items))
            ]

    def CanReachAqueduct(self, items: Progression):
        if self.Logic == SMLogic.Normal:
            return items.CardMaridiaL1 and (items.CanFly() or items.SpeedBooster or items.Grapple) \
                    or items.CardMaridiaL2 and items.CanAccessMaridiaPortal(self.world)
        else:
            return items.CardMaridiaL1 and (items.Gravity or items.HiJump and (items.Ice or items.CanSpringBallJump()) and items.Grapple) \
                    or items.CardMaridiaL2 and items.CanAccessMaridiaPortal(self.world)

    def CanDefeatDraygon(self, items: Progression):
        if self.Logic == SMLogic.Normal:
            return (items.CardMaridiaL1 and items.CardMaridiaL2 and self.CanDefeatBotwoon(items) or
                    items.CanAccessMaridiaPortal(self.world)
                ) and items.CardMaridiaBoss and items.Gravity and (items.SpeedBooster and items.HiJump or items.CanFly())
        else:
            return (items.CardMaridiaL1 and items.CardMaridiaL2 and self.CanDefeatBotwoon(items) or
                    items.CanAccessMaridiaPortal(self.world)
                ) and items.CardMaridiaBoss and items.Gravity


    def CanDefeatBotwoon(self, items: Progression):
        if self.Logic == SMLogic.Normal:
            return items.SpeedBooster or items.CanAccessMaridiaPortal(self.world)
        else:
            return items.Ice or items.SpeedBooster and items.Gravity or items.CanAccessMaridiaPortal(self.world)


    def CanEnter(self, items: Progression):
        if self.Logic == SMLogic.Normal:
            return items.Gravity and (
                self.world.CanEnter("Norfair Upper West", items) and items.Super and items.CanUsePowerBombs() and
                    (items.CanFly() or items.SpeedBooster or items.Grapple) or
                items.CanAccessMaridiaPortal(self.world))
        else:
            return items.Super and self.world.CanEnter("Norfair Upper West", items) and items.CanUsePowerBombs() and (
                    items.Gravity or items.HiJump and (items.Ice or items.CanSpringBallJump()) and items.Grapple) or \
                items.CanAccessMaridiaPortal(self.world)

    def CanComplete(self, items: Progression):
        return self.GetLocation("Space Jump").Available(items)
