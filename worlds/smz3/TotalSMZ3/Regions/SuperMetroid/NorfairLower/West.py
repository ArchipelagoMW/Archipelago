from ....Region import SMRegion
from ....Config import Config, SMLogic
from ....Location import Location, LocationType
from ....Item import Progression

class West(SMRegion):
    Name = "Norfair Lower West"
    Area = "Norfair Lower"

    def __init__(self, world, config: Config):
        super().__init__(world, config)
        self.Locations = [
            Location(self, 70, 0x8F8E6E, LocationType.Visible, "Missile (Gold Torizo)",
                lambda items: items.CanUsePowerBombs() and items.SpaceJump and items.Super if self.Logic == SMLogic.Normal else \
                lambda items: items.CanUsePowerBombs() and items.SpaceJump and items.Varia and (
                    items.HiJump or items.Gravity or
                    items.CanAccessNorfairLowerPortal() and (items.CanFly() or items.CanSpringBallJump() or items.SpeedBooster) and items.Super)),
            Location(self, 71, 0x8F8E74, LocationType.Hidden, "Super Missile (Gold Torizo)",
                lambda items: items.CanDestroyBombWalls() and (items.Super or items.Charge) and
                    (items.CanAccessNorfairLowerPortal() or items.CanUsePowerBombs() and items.SpaceJump) if self.Logic == SMLogic.Normal else \
                lambda items: items.CanDestroyBombWalls() and items.Varia and (items.Super or items.Charge)),
            Location(self, 79, 0x8F9110, LocationType.Chozo, "Screw Attack",
                lambda items: items.CanDestroyBombWalls() and (items.CanAccessNorfairLowerPortal() or items.CanUsePowerBombs() and items.SpaceJump) if self.Logic == SMLogic.Normal else \
                lambda items: items.CanDestroyBombWalls() and (items.CanAccessNorfairLowerPortal() or items.Varia)),
            Location(self, 73, 0x8F8F30, LocationType.Visible, "Missile (Mickey Mouse room)", 
                lambda items: items.Morph and items.Super and items.CanFly() and items.CanUsePowerBombs() and (
                    # /*Exit to Upper Norfair*/
                    (items.CardLowerNorfairL1 or 
                    # /*Vanilla or Reverse Lava Dive*/
                    items.Gravity) and 
                    # /*Bubble Mountain*/
                    items.CardNorfairL2 or
                    # /* Volcano Room and Blue Gate */
                    items.Gravity and items.Wave and 
                    # /*Spikey Acid Snakes and Croc Escape*/
                    (items.Grapple or items.SpaceJump) or
                    # /*Exit via GT fight and Portal*/
                    items.CanUsePowerBombs() and items.SpaceJump and (items.Super or items.Charge)) if self.Logic == SMLogic.Normal else \
                lambda items:
                        items.Varia and items.Morph and items.Super and 
                        #/* Climb worst room (from LN East CanEnter) */
                        (items.CanFly() or items.HiJump or items.CanSpringBallJump() or items.Ice and items.Charge) and
                        (items.CanPassBombPassages() or items.ScrewAttack and items.SpaceJump) and (
                        #/* Exit to Upper Norfair */
                        items.CardNorfairL2 or items.SpeedBooster or items.CanFly() or items.Grapple or
                        items.HiJump and (items.CanSpringBallJump() or items.Ice) or
                        #/* Portal (with GGG) */
                        items.CanUsePowerBombs()
                        ))
            ]

    # // Todo: account for Croc Speedway once Norfair Upper East also do so, otherwise it would be inconsistent to do so here
    def CanEnter(self, items:Progression):
        if self.Logic == SMLogic.Normal:
            return items.Varia and (
                    self.world.CanEnter("Norfair Upper East", items) and items.CanUsePowerBombs() and items.SpaceJump and items.Gravity and (
                        # /* Trivial case, Bubble Mountain access */
                        items.CardNorfairL2 or
                        # /* Frog Speedway -> UN Farming Room gate */
                        items.SpeedBooster and items.Wave
                    ) or
                    items.CanAccessNorfairLowerPortal() and items.CanDestroyBombWalls()
                )
        else:
            return self.world.CanEnter("Norfair Upper East", items) and items.CanUsePowerBombs() and items.Varia and (items.HiJump or items.Gravity) and (
                    # /* Trivial case, Bubble Mountain access */
                    items.CardNorfairL2 or
                    # /* Frog Speedway -> UN Farming Room gate */
                    items.SpeedBooster and (items.Missile or items.Super or items.Wave) # /* Blue Gate */
                ) or items.CanAccessNorfairLowerPortal() and items.CanDestroyBombWalls()