from ....Region import SMRegion
from ....Config import Config, SMLogic
from ....Location import Location, LocationType
from ....Item import Progression

class Outer(SMRegion):
    Name = "Maridia Outer"
    Area = "Maridia"

    def __init__(self, world, config: Config):
        super().__init__(world, config)
        self.Locations = [
            Location(self, 136, 0x8FC437, LocationType.Visible, "Missile (green Maridia shinespark)",
                lambda items: items.SpeedBooster if self.Logic == SMLogic.Normal else \
                lambda items: items.Gravity and items.SpeedBooster),
            Location(self, 137, 0x8FC43D, LocationType.Visible, "Super Missile (green Maridia)"),
            Location(self, 138, 0x8FC47D, LocationType.Visible, "Energy Tank, Mama turtle", 
                lambda items: items.CanOpenRedDoors() and (items.CanFly() or items.SpeedBooster or items.Grapple) if self.Logic == SMLogic.Normal else \
                lambda items: items.CanOpenRedDoors() and (
                    items.CanFly() or items.SpeedBooster or items.Grapple or
                    items.CanSpringBallJump() and (items.Gravity or items.HiJump))),
            Location(self, 139, 0x8FC483, LocationType.Hidden, "Missile (green Maridia tatori)",
                lambda items: items.CanOpenRedDoors())
            ]

    def CanEnter(self, items:Progression):
        if self.Logic == SMLogic.Normal:
            return items.Gravity and (
                    self.world.CanEnter("Norfair Upper West", items) and items.CanUsePowerBombs() or
                    items.CanAccessMaridiaPortal(self.world) and items.CardMaridiaL1 and items.CardMaridiaL2 and (items.CanPassBombPassages() or items.ScrewAttack))
        else:
            return self.world.CanEnter("Norfair Upper West", items) and items.CanUsePowerBombs() and (
                    items.Gravity or items.HiJump and (items.CanSpringBallJump() or items.Ice)) or (
                items.CanAccessMaridiaPortal(self.world)) and items.CardMaridiaL1 and items.CardMaridiaL2 and (
                    items.CanPassBombPassages() or
                    items.Gravity and items.ScrewAttack or
                    items.Super and (items.Gravity or items.HiJump and (items.CanSpringBallJump() or items.Ice)))