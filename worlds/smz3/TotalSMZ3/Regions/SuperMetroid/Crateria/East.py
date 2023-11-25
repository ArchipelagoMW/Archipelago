from ....Region import SMRegion
from ....Config import Config, SMLogic
from ....Location import Location, LocationType
from ....Item import Progression

class East(SMRegion):
    Name = "Crateria East"
    Area = "Crateria"

    def __init__(self, world, config: Config):
        super().__init__(world, config)
        self.Locations = [
            Location(self, 1, 0x8F81E8, LocationType.Visible, "Missile (outside Wrecked Ship bottom)",
                lambda items: items.Morph and (
                    items.SpeedBooster or items.Grapple or items.SpaceJump or
                    items.Gravity and (items.CanIbj() or items.HiJump) or
                    self.world.CanEnter("Wrecked Ship", items)) if self.Logic == SMLogic.Normal else \
                lambda items: items.Morph),
            Location(self, 2, 0x8F81EE, LocationType.Hidden, "Missile (outside Wrecked Ship top)",
                lambda items: self.world.CanEnter("Wrecked Ship", items) and items.CardWreckedShipBoss and items.CanPassBombPassages()),
            Location(self, 3, 0x8F81F4, LocationType.Visible, "Missile (outside Wrecked Ship middle)",
                lambda items: self.world.CanEnter("Wrecked Ship", items) and items.CardWreckedShipBoss and items.CanPassBombPassages()),
            Location(self, 4, 0x8F8248, LocationType.Visible, "Missile (Crateria moat)",
                lambda items: True)
            ]

    def CanEnter(self, items:Progression):
        if self.Logic == SMLogic.Normal:
                # /* Ship -> Moat */
            return (items.CardCrateriaL2 if self.Config.Keysanity else items.CanUsePowerBombs()) and items.Super or (
                # /* UN Portal -> Red Tower -> Moat
                items.CardCrateriaL2 if self.Config.Keysanity else items.CanUsePowerBombs()) and items.CanAccessNorfairUpperPortal() and (
                    items.Ice or items.HiJump or items.SpaceJump) or (
                # /*Through Maridia From Portal*/
                items.CanAccessMaridiaPortal(self.world)) and items.Gravity and items.Super and (
                    # /* Oasis -> Forgotten Highway */
                    items.CardMaridiaL2 and items.CanDestroyBombWalls() or (
                    # /* Draygon -> Cactus Alley -> Forgotten Highway */
                    self.world.GetLocation("Space Jump").Available(items))) or (
                # /*Through Maridia from Pipe*/
                items.CanUsePowerBombs()) and items.Super and items.Gravity
        else:
                # /* Ship -> Moat */
            return (items.CardCrateriaL2 if self.Config.Keysanity else  items.CanUsePowerBombs()) and items.Super or (
                # /* UN Portal -> Red Tower -> Moat */
                items.CardCrateriaL2  if self.Config.Keysanity else  items.CanUsePowerBombs()) and items.CanAccessNorfairUpperPortal() and (
                    items.Ice or items.HiJump or items.CanFly() or items.CanSpringBallJump()) or (
                # /*Through Maridia From Portal*/
                items.CanAccessMaridiaPortal(self.world)) and (
                    # /* Oasis -> Forgotten Highway */
                    items.CardMaridiaL2 and items.Super and (
                        items.HiJump and items.CanPassBombPassages() or
                        items.Gravity and items.CanDestroyBombWalls()
                    ) or
                    # /* Draygon -> Cactus Alley -> Forgotten Highway */
                    items.Gravity and self.world.GetLocation("Space Jump").Available(items)) or (
                # /*Through Maridia from Pipe*/
                items.CanUsePowerBombs()) and items.Super and (items.Gravity or items.HiJump and (items.Ice or items.CanSpringBallJump()) 
                                                            and items.Grapple and items.CardMaridiaL1)
