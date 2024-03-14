from ....Region import SMRegion
from ....Config import Config, SMLogic
from ....Location import Location, LocationType
from ....Item import Progression

class East(SMRegion):
    Name = "Norfair Upper East"
    Area = "Norfair Upper"

    def __init__(self, world, config: Config):
        super().__init__(world, config)
        self.Locations = [
            Location(self, 61, 0x8F8C3E, LocationType.Chozo, "Reserve Tank, Norfair", 
                lambda items: items.CardNorfairL2 and items.Morph and (
                    items.CanFly() or
                    items.Grapple and (items.SpeedBooster or items.CanPassBombPassages()) or
                    items.HiJump or items.Ice
                ) if self.Logic == SMLogic.Normal else \
                lambda items: items.CardNorfairL2 and items.Morph and items.Super),
            Location(self, 62, 0x8F8C44, LocationType.Hidden, "Missile (Norfair Reserve Tank)",
                lambda items: items.CardNorfairL2 and items.Morph and (
                    items.CanFly() or
                    items.Grapple and (items.SpeedBooster or items.CanPassBombPassages()) or
                    items.HiJump or items.Ice
                ) if self.Logic == SMLogic.Normal else \
                lambda items: items.CardNorfairL2 and items.Morph and items.Super),
            Location(self, 63, 0x8F8C52, LocationType.Visible, "Missile (bubble Norfair green door)",
                lambda items: items.CardNorfairL2 and (
                    items.CanFly() or
                    items.Grapple and items.Morph and (items.SpeedBooster or items.CanPassBombPassages()) or
                    items.HiJump or items.Ice
                ) if self.Logic == SMLogic.Normal else \
                lambda items: items.CardNorfairL2 and items.Super),
            Location(self, 64, 0x8F8C66, LocationType.Visible, "Missile (bubble Norfair)", 
                lambda items: items.CardNorfairL2),
            Location(self, 65, 0x8F8C74, LocationType.Hidden, "Missile (Speed Booster)",
                lambda items: items.CardNorfairL2 and (
                    items.CanFly() or
                    items.Morph and (items.SpeedBooster or items.CanPassBombPassages()) or
                    items.HiJump or items.Ice
                ) if self.Logic == SMLogic.Normal else \
                lambda items: items.CardNorfairL2 and items.Super),
            Location(self, 66, 0x8F8C82, LocationType.Chozo, "Speed Booster",
                lambda items: items.CardNorfairL2 and (
                    items.CanFly() or
                    items.Morph and (items.SpeedBooster or items.CanPassBombPassages()) or
                    items.HiJump or items.Ice
                ) if self.Logic == SMLogic.Normal else \
                lambda items: items.CardNorfairL2 and items.Super),
            Location(self, 67, 0x8F8CBC, LocationType.Visible, "Missile (Wave Beam)",
                lambda items: items.CardNorfairL2 and (
                    items.CanFly() or
                    items.Morph and (items.SpeedBooster or items.CanPassBombPassages()) or
                    items.HiJump or items.Ice
                ) or
                items.SpeedBooster and items.Wave and items.Morph and items.Super if self.Logic == SMLogic.Normal else \
                lambda items: items.CardNorfairL2 or items.Varia),
            Location(self, 68, 0x8F8CCA, LocationType.Chozo, "Wave Beam",
                lambda items: items.Morph and (
                    items.CardNorfairL2 and (
                        items.CanFly() or
                        items.Morph and (items.SpeedBooster or items.CanPassBombPassages()) or
                        items.HiJump or items.Ice
                    ) or
                    items.SpeedBooster and items.Wave and items.Morph and items.Super
                ) if self.Logic == SMLogic.Normal else \
                lambda items: items.CanOpenRedDoors() and (items.CardNorfairL2 or items.Varia) and
                    (items.Morph or items.Grapple or items.HiJump and items.Varia or items.SpaceJump))
            ]

    # // Todo: Super is not actually needed for Frog Speedway, but changing this will affect locations
    # // Todo: Ice Beam -> Croc Speedway is not considered
    def CanEnter(self, items:Progression):
        if self.Logic == SMLogic.Normal:
            return ((items.CanDestroyBombWalls() or items.SpeedBooster) and items.Super and items.Morph or
                    items.CanAccessNorfairUpperPortal()
                ) and items.Varia and items.Super and (
                    # /* Cathedral */
                    items.CanOpenRedDoors() and (items.CardNorfairL2 if self.Config.Keysanity else items.Super) and
                        (items.CanFly() or items.HiJump or items.SpeedBooster) or
                    # /* Frog Speedway */
                    items.SpeedBooster and (items.CardNorfairL2 or items.Wave) and items.CanUsePowerBombs()
                )
        else:
            return ((items.CanDestroyBombWalls() or items.SpeedBooster) and items.Super and items.Morph or
                    items.CanAccessNorfairUpperPortal()) and (
                items.CanHellRun()) and (
                    # /* Cathedral */
                    items.CanOpenRedDoors() and (items.CardNorfairL2 if self.Config.Keysanity else items.Super) and (
                        items.CanFly() or items.HiJump or items.SpeedBooster or
                        items.CanSpringBallJump() or items.Varia and items.Ice
                    ) or
                    # /* Frog Speedway */
                    items.SpeedBooster and (items.CardNorfairL2 or items.Missile or items.Super or items.Wave) and items.CanUsePowerBombs())
