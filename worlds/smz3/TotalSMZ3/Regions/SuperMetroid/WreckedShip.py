from ...Region import SMRegion, IReward, RewardType
from ...Config import Config, SMLogic
from ...Location import Location, LocationType
from ...Item import Progression

class WreckedShip(SMRegion, IReward):
    Name = "Wrecked Ship"
    Area = "Wrecked Ship"

    def __init__(self, world, config: Config):
        super().__init__(world, config)
        self.Weight = 4
        self.Reward = RewardType.Null
        self.Locations = [
            Location(self, 128, 0x8FC265, LocationType.Visible, "Missile (Wrecked Ship middle)", 
                lambda items: items.CanPassBombPassages()),
            Location(self, 129, 0x8FC2E9, LocationType.Chozo, "Reserve Tank, Wrecked Ship",
                lambda items: self.CanUnlockShip(items) and items.CardWreckedShipL1 and items.CanUsePowerBombs() and items.SpeedBooster and
                    (items.Grapple or items.SpaceJump or items.Varia and items.HasEnergyReserves(2) or items.HasEnergyReserves(3)) if self.Logic == SMLogic.Normal else \
                lambda items: self.CanUnlockShip(items) and items.CardWreckedShipL1 and items.CanUsePowerBombs() and items.SpeedBooster and
                    (items.Varia or items.HasEnergyReserves(2))),
            Location(self, 130, 0x8FC2EF, LocationType.Visible, "Missile (Gravity Suit)", 
                lambda items: self.CanUnlockShip(items) and items.CardWreckedShipL1 and
                    (items.Grapple or items.SpaceJump or items.Varia and items.HasEnergyReserves(2) or items.HasEnergyReserves(3)) if self.Logic == SMLogic.Normal else \
                lambda items: self.CanUnlockShip(items) and items.CardWreckedShipL1 and (items.Varia or items.HasEnergyReserves(1))),
            Location(self, 131, 0x8FC319, LocationType.Visible, "Missile (Wrecked Ship top)",
                lambda items: self.CanUnlockShip(items)),
            Location(self, 132, 0x8FC337, LocationType.Visible, "Energy Tank, Wrecked Ship",
                lambda items: self.CanUnlockShip(items) and
                    (items.HiJump or items.SpaceJump or items.SpeedBooster or items.Gravity) if self.Logic == SMLogic.Normal else \
                lambda items: self.CanUnlockShip(items) and (items.Morph and (items.Bombs or items.PowerBomb) or items.CanSpringBallJump() or
                    items.HiJump or items.SpaceJump or items.SpeedBooster or items.Gravity)),
            Location(self, 133, 0x8FC357, LocationType.Visible, "Super Missile (Wrecked Ship left)",
                lambda items: self.CanUnlockShip(items)),
            Location(self, 134, 0x8FC365, LocationType.Visible, "Right Super, Wrecked Ship",
                lambda items: self.CanUnlockShip(items)),
            Location(self, 135, 0x8FC36D, LocationType.Chozo, "Gravity Suit", 
                lambda items: self.CanUnlockShip(items) and items.CardWreckedShipL1 and
                    (items.Grapple or items.SpaceJump or items.Varia and items.HasEnergyReserves(2) or items.HasEnergyReserves(3)) if self.Logic == SMLogic.Normal else \
                lambda items: self.CanUnlockShip(items) and items.CardWreckedShipL1 and (items.Varia or items.HasEnergyReserves(1)))
            ]

    def CanUnlockShip(self, items:Progression):
        return items.CardWreckedShipBoss and items.CanPassBombPassages()

    def CanEnter(self, items:Progression):
        if self.Logic == SMLogic.Normal:
            return items.Super and (
                    # /* Over the Moat */
                    (items.CardCrateriaL2 if self.Config.Keysanity else items.CanUsePowerBombs()) and (
                        items.SpeedBooster or items.Grapple or items.SpaceJump or
                        items.Gravity and (items.CanIbj() or items.HiJump)
                    ) or
                    # /* Through Maridia -> Forgotten Highway */
                    items.CanUsePowerBombs() and items.Gravity or
                    # /* From Maridia portal -> Forgotten Highway */
                    items.CanAccessMaridiaPortal(self.world) and items.Gravity and (
                        items.CanDestroyBombWalls() and items.CardMaridiaL2 or
                        self.world.GetLocation("Space Jump").Available(items)))
        else:
            return items.Super and (
                    # /* Over the Moat */
                    (items.CardCrateriaL2 if self.Config.Keysanity else items.CanUsePowerBombs()) or
                    # /* Through Maridia -> Forgotten Highway */
                    items.CanUsePowerBombs() and (
                        items.Gravity or
                        # /* Climb Mt. Everest */
                        items.HiJump and (items.Ice or items.CanSpringBallJump()) and items.Grapple and items.CardMaridiaL1
                    ) or
                    # /* From Maridia portal -> Forgotten Highway */
                    items.CanAccessMaridiaPortal(self.world) and ( 
                        items.HiJump and items.CanPassBombPassages() and items.CardMaridiaL2 or
                        items.Gravity and (
                            items.CanDestroyBombWalls() and items.CardMaridiaL2 or
                            self.world.GetLocation("Space Jump").Available(items))))

    def CanComplete(self, items:Progression):
        return self.CanEnter(items) and self.CanUnlockShip(items)