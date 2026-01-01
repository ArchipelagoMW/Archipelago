from ....Region import SMRegion
from ....Config import Config, SMLogic
from ....Location import Location, LocationType
from ....Item import Progression

class Crocomire(SMRegion):
    Name = "Norfair Upper Crocomire"
    Area = "Norfair Upper"

    def __init__(self, world, config: Config):
        super().__init__(world, config)
        self.Locations = [
            Location(self, 52, 0x8F8BA4, LocationType.Visible, "Energy Tank, Crocomire",
                lambda items: self.CanAccessCrocomire(items) and (items.HasEnergyReserves(1) or items.SpaceJump or items.Grapple) if self.Logic == SMLogic.Normal else \
                lambda items: self.CanAccessCrocomire(items)),
            Location(self, 54, 0x8F8BC0, LocationType.Visible, "Missile (above Crocomire)", 
                lambda items: items.CanFly() or items.Grapple or items.HiJump and items.SpeedBooster if self.Logic == SMLogic.Normal else \
                lambda items: (items.CanFly() or items.Grapple or items.HiJump and
                    (items.SpeedBooster or items.CanSpringBallJump() or items.Varia and items.Ice)) and items.CanHellRun()),
            Location(self, 57, 0x8F8C04, LocationType.Visible, "Power Bomb (Crocomire)",
                lambda items: self.CanAccessCrocomire(items) and (items.CanFly() or items.HiJump or items.Grapple) if self.Logic == SMLogic.Normal else \
                lambda items: self.CanAccessCrocomire(items)),
            Location(self, 58, 0x8F8C14, LocationType.Visible, "Missile (below Crocomire)", 
                lambda items: self.CanAccessCrocomire(items) and items.Morph),
            Location(self, 59, 0x8F8C2A, LocationType.Visible, "Missile (Grappling Beam)", 
                lambda items: self.CanAccessCrocomire(items) and items.Morph and (items.CanFly() or items.SpeedBooster and items.CanUsePowerBombs()) if self.Logic == SMLogic.Normal else \
                lambda items: self.CanAccessCrocomire(items) and (items.SpeedBooster or items.Morph and (items.CanFly() or items.Grapple))),
            Location(self, 60, 0x8F8C36, LocationType.Chozo, "Grappling Beam", 
                lambda items: self.CanAccessCrocomire(items) and items.Morph and (items.CanFly() or items.SpeedBooster and items.CanUsePowerBombs()) if self.Logic == SMLogic.Normal else \
                lambda items: self.CanAccessCrocomire(items) and (items.SpaceJump or items.Morph or items.Grapple or
                    items.HiJump and items.SpeedBooster))
        ]

    def CanAccessCrocomire(self, items:Progression):
        return items.CardNorfairBoss if self.Config.Keysanity else items.Super

    def CanEnter(self, items:Progression):
        if self.Logic == SMLogic.Normal:
            return ((items.CanDestroyBombWalls() or items.SpeedBooster) and items.Super and items.Morph or items.CanAccessNorfairUpperPortal()) and (
                items.Varia) and (
                    # /* Ice Beam -> Croc Speedway */
                    (items.CardNorfairL1 if self.Config.Keysanity else items.Super) and items.CanUsePowerBombs() and items.SpeedBooster or
                    # /* Frog Speedway */
                    items.SpeedBooster and items.Wave or
                    # /* Cathedral -> through the floor or Vulcano */
                    items.CanOpenRedDoors() and (items.CardNorfairL2 if self.Config.Keysanity else items.Super) and
                        (items.CanFly() or items.HiJump or items.SpeedBooster) and
                        (items.CanPassBombPassages() or items.Gravity and items.Morph) and items.Wave) or (
                    # /* Reverse Lava Dive */
                    items.Varia) and items.CanAccessNorfairLowerPortal() and items.ScrewAttack and items.SpaceJump and items.Super and (
                    items.Gravity) and items.Wave and (items.CardNorfairL2 or items.Morph)
        else:
            return ((items.CanDestroyBombWalls() or items.SpeedBooster) and items.Super and items.Morph or items.CanAccessNorfairUpperPortal()) and (
                    # /* Ice Beam -> Croc Speedway */
                    (items.CardNorfairL1 if self.Config.Keysanity else items.Super) and items.CanUsePowerBombs() and
                        items.SpeedBooster and (items.HasEnergyReserves(3) or items.Varia) or
                    # /* Frog Speedway */
                    items.SpeedBooster and (items.HasEnergyReserves(2) or items.Varia) and
                        (items.Missile or items.Super or items.Wave) or ( # /* Blue Gate */
                    # /* Cathedral -> through the floor or Vulcano */
                    items.CanHellRun()) and items.CanOpenRedDoors() and (items.CardNorfairL2 if self.Config.Keysanity else items.Super) and
                        (items.CanFly() or items.HiJump or items.SpeedBooster or items.CanSpringBallJump() or items.Varia and items.Ice) and
                        (items.CanPassBombPassages() or items.Varia and items.Morph) and
                        (items.Missile or items.Super or items.Wave) # /* Blue Gate */
                    ) or (
                    # /* Reverse Lava Dive */
                    items.Varia and items.CanAccessNorfairLowerPortal()) and items.ScrewAttack and items.SpaceJump and items.Super and (
                    items.HasEnergyReserves(2)) and (items.CardNorfairL2 or items.Morph)
