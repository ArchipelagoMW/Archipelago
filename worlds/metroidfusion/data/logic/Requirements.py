from typing import TYPE_CHECKING

from .Requirement import Requirement
if TYPE_CHECKING:
    from ... import MetroidFusionOptions

level_1_e_tanks = 3
level_2_e_tanks = 5
level_3_e_tanks = 7
level_4_e_tanks = 10

#region Individual Item Requirements
class HasMorph(Requirement):
    name = "Has Morph Ball"
    items_needed = ["Morph Ball"]

class HasVaria(Requirement):
    name = "Has Varia Suit"
    items_needed = ["Varia Suit"]

class HasGravity(Requirement):
    name = "Has Gravity Suit"
    items_needed = ["Gravity Suit"]

class HasHiJump(Requirement):
    name = "Has Hi-Jump"
    items_needed = ["Hi-Jump"]

class HasSpaceJump(Requirement):
    name = "Has Space Jump"
    items_needed = ["Space Jump"]

class HasSpeedBooster(Requirement):
    name = "Has Speed Booster"
    items_needed = ["Speed Booster"]

class HasScrewAttack(Requirement):
    name = "Has Screw Attack"
    items_needed = ["Screw Attack"]

class HasMissile(Requirement):
    name = "Has Missile Data"
    items_needed = ["Missile Data"]

class HasChargeBeam(Requirement):
    name = "Has Charge Beam"
    items_needed = ["Charge Beam"]

class HasWaveBeam(Requirement):
    name = "Has Wave Beam"
    items_needed = ["Wave Beam"]

#endregion

#region Combined Item Requirements
class CanJumpHigh(Requirement):
    name = "Can Jump High"
    other_requirements = [
        Requirement(["Hi-Jump"], []),
        Requirement(["Space Jump"], [])
    ]

class CanLavaDive(Requirement):
    name = "Can Lava Dive"
    items_needed = ["Varia Suit", "Gravity Suit"]

class CanBomb(Requirement):
    name = "Can Bomb"
    items_needed = ["Morph Ball", "Bomb Data"]

class CanPowerBomb(Requirement):
    name = "Can Power Bomb"
    items_needed = ["Morph Ball", "Power Bomb Data"]

class CanBombOrPowerBomb(Requirement):
    name = "Can Bomb or Power Bomb"
    other_requirements = [CanBomb, CanPowerBomb]

class CanPowerBombAndJumpHigh(Requirement):
    name = "Can Power Bomb and Jump High"
    items_needed = ["Morph Ball", "Power Bomb Data"]
    other_requirements = [CanJumpHigh]

class CanBallJump(Requirement):
    name = "Can Ball Jump"
    items_needed = ["Morph Ball"]
    other_requirements = [
        Requirement(["Bomb Data"], []),
        Requirement(["Hi-Jump"], [])
    ]

class CanBallJumpAndBomb(Requirement):
    name = "Can Ball Jump and Bomb"
    other_requirements = [
        Requirement(["Morph Ball", "Bomb Data"], []),
        Requirement(["Hi-Jump"], [CanPowerBomb])
    ]

class CanScrewAttackAndSpaceJump(Requirement):
    name = "Can Screw Attack and Space Jump"
    items_needed = ["Screw Attack", "Space Jump"]

class CanJumpHighUnderwater(Requirement):
    name = "Can Jump High underwater"
    items_needed = ["Gravity Suit"]
    other_requirements = [CanJumpHigh]

class CanSpeedBoosterUnderwater(Requirement):
    name = "Can Speed Booster Underwater"
    items_needed = ["Gravity Suit", "Speed Booster"]

class CanScrewAttackUnderwater(Requirement):
    items_needed = ["Gravity Suit", "Screw Attack"]

class CanFreezeEnemies(Requirement):
    name = "Can Freeze Enemies"
    other_requirements = [
        Requirement(["Ice Missile"], [HasMissile]),
        Requirement(["Diffusion Missile"], [HasMissile]),
        Requirement(["Ice Beam"], [])
    ]

class CanActivatePillar(Requirement):
    name = "Can Activate Pillar"
    other_requirements = [CanBombOrPowerBomb, HasWaveBeam]

class CanDiffusionMissile(Requirement):
    name = "Can Diffusion Missile"
    items_needed = ["Missile Data", "Diffusion Missile"]

class CanDestroyBombBlocks(Requirement):
    name = "Can Destroy Bomb Blocks"
    other_requirements = [CanBombOrPowerBomb, HasScrewAttack]

class CanChargedWaveShot(Requirement):
    name = "Can Charged Wave Shot"
    items_needed = ["Charge Beam", "Wave Beam"]

#endregion

#region Optional Requirements

class CanDoBeginnerShinespark(Requirement):
    name = "Can Do Beginner Shinespark"
    items_needed = ["Speed Booster"]

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return options.ShinesparkTrickDifficulty.value >= options.ShinesparkTrickDifficulty.option_beginner

class CanDoAdvancedShinespark(Requirement):
    name = "Can Do Advanced Shinespark"
    items_needed = ["Speed Booster"]

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return options.ShinesparkTrickDifficulty >= options.ShinesparkTrickDifficulty.option_advanced

class CanDoSimpleWallJump(Requirement):
    name = "Can Do Simple Wall Jump"
    items_needed = ["Wall Jump Boots"]

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return options.WallJumpTrickDifficulty >= options.WallJumpTrickDifficulty.option_beginner

class CanDoSimpleWallJumpWithHiJump(Requirement):
    name = "Can Do Simple Wall Jump with Hi-Jump"
    items_needed = ["Hi-Jump"]

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return options.WallJumpTrickDifficulty >= options.WallJumpTrickDifficulty.option_beginner

class CanDoSimpleWallJumpWithScrewAttack(Requirement):
    name = "Can Do Simple Wall Jump with Screw Attack"
    items_needed = ["Screw Attack"]

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return options.WallJumpTrickDifficulty >= options.WallJumpTrickDifficulty.option_beginner

class CanDoSimpleWallJumpWithHiJumpAndScrewAttack(Requirement):
    name = "Can Do Simple Wall Jump with Hi-Jump and Screw Attack"
    items_needed = ["Hi-Jump", "Screw Attack"]

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return options.WallJumpTrickDifficulty >= options.WallJumpTrickDifficulty.option_beginner

class CanDoSimpleWallJumpAndFreezeEnemies(Requirement):
    name = "Can Do Simple Wall Jump and Freeze Enemies"
    other_requirements = [CanFreezeEnemies]

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return options.WallJumpTrickDifficulty >= options.WallJumpTrickDifficulty.option_beginner

class CanDoAdvancedWallJump(Requirement):
    name = "Can Do Advanced Wall Jump"
    items_needed = ["Wall Jump Boots"]

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return options.WallJumpTrickDifficulty >= options.WallJumpTrickDifficulty.option_advanced

class CanDoAdvancedWallJumpWithHiJump(Requirement):
    name = "Can Do Advanced Wall Jump with Hi-Jump"
    items_needed = ["Hi-Jump"]

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return options.WallJumpTrickDifficulty >= options.WallJumpTrickDifficulty.option_advanced

class CanDoAdvancedWallJumpWithScrewAttack(Requirement):
    name = "Can Do Advanced Wall Jump with Screw Attack"
    items_needed = ["Screw Attack"]

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return options.WallJumpTrickDifficulty >= options.WallJumpTrickDifficulty.option_advanced

class CanDoAdvancedCombat(Requirement):
    name = "Can Do Advanced Combat"
    items_needed = ["Nothing"]

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return options.CombatDifficulty >= options.CombatDifficulty.option_advanced

class CanDoExpertCombat(Requirement):
    name = "Can Do Expert Combat"
    items_needed = ["Nothing"]

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return options.CombatDifficulty >= options.CombatDifficulty.option_expert

class CanFightBossOnAdvanced(Requirement):
    name = "Can Fight Boss on Advanced"
    items_needed = ["Missile Data", "Charge Beam"]
    energy_tanks_needed = level_1_e_tanks

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return options.CombatDifficulty >= options.CombatDifficulty.option_advanced

class CanFightLategameBossOnAdvanced(Requirement):
    name = "Can Fight Lategame Boss on Advanced"
    items_needed = ["Missile Data", "Charge Beam", "Super Missile"]
    energy_tanks_needed = level_2_e_tanks

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return options.CombatDifficulty >= options.CombatDifficulty.option_advanced

class CanFightBossOnExpert(Requirement):
    name = "Can Fight Boss on Expert"
    items_needed = ["Missile Data", "Charge Beam"]

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return options.CombatDifficulty >= options.CombatDifficulty.option_expert

class SectorHubLevel1KeycardRequirement(Requirement):
    name = "Sector Hub Level 1 Keycard Requirement"
    items_needed = ["Level 1 Keycard"]
    energy_tanks_needed = level_1_e_tanks

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions"):
        if options.GameMode == options.GameMode.option_custom:
            return not options.OpenSectorElevators
        else:
            return options.GameMode == options.GameMode.option_vanilla


class SectorHubLevel1And2KeycardRequirement(Requirement):
    name = "Sector Hub Level 1 and 2 Keycard Requirement"
    items_needed = ["Level 1 Keycard", "Level 2 Keycard"]
    energy_tanks_needed = level_2_e_tanks

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions"):
        if options.GameMode == options.GameMode.option_custom:
            return not options.OpenSectorElevators
        else:
            return options.GameMode == options.GameMode.option_vanilla


# endregion

#region Keycard Requirements
class HasKeycard1(Requirement):
    name = "Has Keycard 1"
    energy_tanks_needed = level_1_e_tanks
    items_needed = ["Level 1 Keycard"]

class HasKeycard2(Requirement):
    name = "Has Keycard 2"
    energy_tanks_needed = level_2_e_tanks
    items_needed = ["Level 2 Keycard"]

class HasKeycard1And2(Requirement):
    name = "Has Keycard 1 and 2"
    energy_tanks_needed = level_2_e_tanks
    items_needed = ["Level 1 Keycard", "Level 2 Keycard"]

class HasKeycard3(Requirement):
    name = "Has Keycard 3"
    energy_tanks_needed = level_3_e_tanks
    items_needed = ["Level 3 Keycard"]

class HasKeycard4(Requirement):
    name = "Has Keycard 4"
    energy_tanks_needed = level_4_e_tanks
    items_needed = ["Level 4 Keycard"]

class Level1KeycardRequirement(Requirement):
    name = "Level 1 Keycard Requirement"
    def __init__(self, items_needed, other_requirements, energy_tanks_needed=3):
        super().__init__(items_needed, other_requirements, energy_tanks_needed)
        self.items_needed.append("Level 1 Keycard")

class Level2KeycardRequirement(Requirement):
    name = "Level 2 Keycard Requirement"
    def __init__(self, items_needed, other_requirements, energy_tanks_needed=5):
        super().__init__(items_needed, other_requirements, energy_tanks_needed)
        self.items_needed.append("Level 2 Keycard")

class Level1And2KeycardRequirement(Requirement):
    name = "Level 1 and 2 Keycard Requirement"
    def __init__(self, items_needed, other_requirements, energy_tanks_needed=5):
        super().__init__(items_needed, other_requirements, energy_tanks_needed)
        self.items_needed.append("Level 1 Keycard")
        self.items_needed.append("Level 2 Keycard")

class Level3KeycardRequirement(Requirement):
    name = "Level 3 Keycard Requirement"
    def __init__(self, items_needed, other_requirements, energy_tanks_needed=7):
        super().__init__(items_needed, other_requirements, energy_tanks_needed)
        self.items_needed.append("Level 3 Keycard")

class Level4KeycardRequirement(Requirement):
    name = "Level 4 Keycard Requirement"
    def __init__(self, items_needed, other_requirements, energy_tanks_needed=10):
        super().__init__(items_needed, other_requirements, energy_tanks_needed)
        self.items_needed.append("Level 4 Keycard")
#endregion

#region Enemy Requirements
class CanDefeatSmallGeron(Requirement):
    name = "Can Defeat Small Geron"
    other_requirements = [
        Requirement(["Missile Data"], []),
        CanPowerBomb,
        Requirement(["Screw Attack"], [])
    ]

class CanDefeatMediumGeron(Requirement):
    name = "Can Defeat Medium Geron"
    other_requirements = [
        Requirement(["Missile Data", "Super Missile"], []),
        CanPowerBomb,
        Requirement(["Screw Attack"], [])
    ]

class CanDefeatLargeGeron(Requirement):
    name = "Can Defeat Large Geron"
    other_requirements = [
        CanPowerBomb,
        Requirement(["Screw Attack"], [])
    ]

class CanBeatToughEnemy(Requirement):
    name = "Can Beat Tough Enemy"
    other_requirements = [HasChargeBeam, HasMissile]

class CanBeatToughEnemyAndJumpHigh(Requirement):
    name = "Can Beat Tough Enemy and Jump High"
    other_requirements = [
        Requirement(["Hi-Jump"], [CanBeatToughEnemy]),
        Requirement(["Space Jump"], [CanBeatToughEnemy])
    ]

class CanDefeatStabilizerOrToughEnemy(Requirement):
    name = "Can Defeat Stabilizer"
    other_requirements = [HasScrewAttack, HasMissile, HasChargeBeam, CanPowerBomb]

class CanDefeatThirdStabilizer(Requirement):
    name = "Can Defeat Third Stabilizer"
    other_requirements = [
        Requirement(["Screw Attack"], [
            HasSpaceJump,
            CanDoAdvancedWallJump,
            CanDoSimpleWallJumpWithHiJump
        ]),
        Requirement(["Charge Beam"], []),
        Requirement(["Missile Data"], []),
        CanPowerBomb
    ]

#endregion

#region Boss Requirements
class CanFightBeginnerBoss(Requirement):
    name = "Can Fight Beginner Boss"
    items_needed = ["Missile Data"]

class CanFightBoss(Requirement):
    name = "Can Fight Boss"
    energy_tanks_needed = level_1_e_tanks
    items_needed = ["Missile Data", "Charge Beam"]

class CanFightMidgameBoss(Requirement):
    name = "Can Fight Midgame Boss"
    energy_tanks_needed = level_2_e_tanks
    items_needed = ["Super Missile"]
    other_requirements = [CanFightBoss]

class CanFightLateGameBoss(Requirement):
    name = "Can Fight Lategame Boss"
    energy_tanks_needed = level_3_e_tanks
    items_needed = ["Plasma Beam", "Space Jump"]
    other_requirements = [CanFightMidgameBoss]

#endregion

#region Individual Location Requirements

#region Main Deck Individual Requirements
class CanReachAnimals(Requirement):
    name = "Can Reach Animals"
    items_needed = ["Speed Booster"]
    other_requirements = [
        Requirement(["Hi-Jump"], [CanFreezeEnemies]),
        HasSpaceJump
    ]

class CanReachGenesisSpeedway(Requirement):
    name = "Can Reach Genesis Speedway"
    items_needed = ["Morph Ball", "Power Bomb Data"]
    other_requirements = [
        Requirement(["Bomb Data"], [CanDoSimpleWallJump, CanJumpHigh]),
        HasHiJump
    ]

class CanCrossFromReactorToSector2(Requirement):
    name = "Can Cross from Reactor to Sector 2"
    items_needed = ["Space Jump", "Missile Data"]
    other_requirements = [CanBombOrPowerBomb]

class CanAccessYakuza(Requirement):
    name = "Can Access Yakuza"
    other_requirements = [
        Requirement(["Morph Ball", "Bomb Data"], [CanBeatToughEnemy]),
        Requirement(["Morph Ball", "Power Bomb Data"], [CanBeatToughEnemy]),
        Requirement(["Morph Ball", "Wave Beam"], [CanBeatToughEnemy]),
        Requirement(
            ["Morph Ball", "Missile Data", "Diffusion Missile"],
            [CanBeatToughEnemy]
        )
    ]
#endregion

#region Sector 1 Individual Requirements
class CanReachAnimorphs(Requirement):
    name = "Can Reach Animorphs"
    other_requirements = [
        # Wave or PB for the crab, Supers for the other two.
        Requirement(["Missile Data", "Super Missile"], [CanChargedWaveShot, CanPowerBomb]),
        # Wave or PB for the crab, Screw Attack for the other two
        Requirement(["Screw Attack"], [CanChargedWaveShot, CanPowerBomb]),
        # Technically don't need Supers with enough of other missiles but we don't have ammo requirements in logic yet.
    ]

class CanAccessWallJumpTutorialWithSpaceJump(Requirement):
    name = "Can Access Wall Jump Tutorial with Space Jump"
    items_needed = ["Space Jump"]
    other_requirements = [CanBallJump]

class CanAccessWallJumpTutorialWithWallJump(Requirement):
    name = "Can Access Wall Jump Tutorial with Wall Jump"
    other_requirements = [
        Requirement(["Morph Ball", "Hi-Jump"], [CanDoSimpleWallJump]),
        Requirement(["Morph Ball", "Bomb Data"], [CanDoSimpleWallJump]),
    ]
#endregion

#region Sector 2 Individual Requirements
class CanReachOasisStorage(Requirement):
    name = "Can Reach Oasis Storage"
    other_requirements = [
        CanPowerBomb,
        Requirement(["Hi-Jump"], [CanBombOrPowerBomb]),
        Requirement(["Morph Ball", "Screw Attack"], [CanJumpHighUnderwater])
    ]

class CanAccessZazabiSpeedway(Requirement):
    name = "Can Access Zazabi Speedway"
    items_needed = ["Space Jump", "Speed Booster", "Screw Attack"]
    other_requirements = [CanFightBoss]

class CanAccessWateringHole(Requirement):
    name = "Can Access Watering Hole"
    items_needed = ["Gravity Suit", "Speed Booster", "Morph Ball"]
    other_requirements = [
        # The first three are straightforward, but other crab killing methods are made much easier with a recharge.
        Requirement(["Charge Beam"], [CanBallJump]),
        Requirement(["Plasma Beam"], [CanBallJump]),
        Requirement(["Screw Attack"], [CanBallJump]),
        Requirement(["Missile Data", "Bomb Data"], [CanDoBeginnerShinespark]),
        Requirement(["Missile Data", "Hi-Jump"], [CanDoBeginnerShinespark]),
        Requirement(["Wide Beam", "Bomb Data"], [CanDoBeginnerShinespark]),
        Requirement(["Wide Beam", "Hi-Jump"], [CanDoBeginnerShinespark]),
        Requirement(["Wave Beam", "Bomb Data"], [CanDoBeginnerShinespark]),
        Requirement(["Wave Beam", "Hi-Jump"], [CanDoBeginnerShinespark]),
        Requirement(["Ice Beam", "Bomb Data"], [CanDoBeginnerShinespark]),
        Requirement(["Ice Beam", "Hi-Jump"], [CanDoBeginnerShinespark]),
        Requirement(["Power Bomb Data", "Bomb Data"], [CanDoBeginnerShinespark]),
        Requirement(["Power Bomb Data", "Hi-Jump"], [CanDoBeginnerShinespark]),
        Requirement([], [CanDoAdvancedShinespark]),
        Requirement([], [CanDoAdvancedCombat]),

    ]

class CanBacktrackToCultivationStation(Requirement):
    name = "Can Backtrack to Cultivation Station"
    other_requirements = [
        Requirement(["Hi-Jump"], [CanBombOrPowerBomb]),
        Requirement(["Space Jump"], [CanBombOrPowerBomb])
    ]
#endregion

#region Sector 3 Individual Requirements
class CanAscendBOXRoom(Requirement):
    name = "Can Ascend BOX Room"
    items_needed = ["Charge Beam", "Missile Data"]
    other_requirements = [CanJumpHigh, CanDoSimpleWallJump]

class CanNavigateLavaMaze(Requirement):
    name = "Can Navigate Lava Maze"
    items_needed = ["Morph Ball", "Power Bomb Data"]
    other_requirements = [CanLavaDive]

class CanAccessLevel2SecurityRoom(Requirement):
    name = "Can Access Level 2 Security Room"
    items_needed = ["Speed Booster"]
    other_requirements = [CanBallJumpAndBomb]

class CanAccessFieryStorage(Requirement):
    name = "Can Access Fiery Storage"
    items_needed = ["Varia Suit"]
    other_requirements = [
        CanBeatToughEnemy,
        CanLavaDive,
        CanDoBeginnerShinespark
    ]

class CanAccessFieryStorageUpper(Requirement):
    name = "Can Access Fiery Storage Upper"
    items_needed = ["Speed Booster"]
    other_requirements = [
        Requirement(["Morph Ball", "Bomb Data"],[CanActivatePillar, HasSpaceJump]),
        Requirement(["Morph Ball", "Power Bomb Data"], [CanActivatePillar, HasSpaceJump]),
        Requirement(["Screw Attack"], [CanActivatePillar, HasSpaceJump]),
    ]

class CanAccessGlassTubeItem(Requirement):
    name = "Can Access Glass Tube Item"
    other_requirements = [
        Requirement(["Hi-Jump"], [CanBomb]),
        CanPowerBomb,
        Requirement(["Screw Attack"], []),
    ]

class CanAccessGarbageChute(Requirement):
    name = "Can Access Garbage Chute"
    items_needed = ["Screw Attack", "Speed Booster"]
    other_requirements = [
        CanLavaDive
    ]

class CanAccessSector3LowerAlcove(Requirement):
    name = "Can Access Sector 3 Lower Alcove"
    items_needed = ["Morph Ball"]
    other_requirements = [
        CanBombOrPowerBomb,
        Requirement(["Screw Attack"], [CanActivatePillar, HasSpeedBooster, CanJumpHigh])
    ]
#endregion

#region Sector 4 Individual Requirements
class CanDrainAQA(Requirement):
    name = "Can Drain AQA"
    items_needed = ["Speed Booster", "Level 1 Keycard"]
    other_requirements = [CanBombOrPowerBomb]

class CanAscendCheddarBay(Requirement):
    name = "Can Ascend Cheddar Bay"
    items_needed = ["Missile Data"]
    other_requirements = [CanBombOrPowerBomb]

class CanAccessReservoirVault(Requirement):
    name = "Can Access Reservoir Vault"
    other_requirements = [
        Requirement(["Hi-Jump", "Morph Ball", "Bomb Data"], [CanDoSimpleWallJump]),
        Requirement(["Hi-Jump", "Morph Ball", "Power Bomb Data"], [CanDoSimpleWallJump]),
        Requirement(["Space Jump"], [CanBallJumpAndBomb])
    ]

class CanAccessSanctuaryCache(Requirement):
    name = "Can Access Sanctuary Cache"
    other_requirements = [
        Requirement(["Wave Beam", "Charge Beam"], [CanDoSimpleWallJump, HasSpaceJump]),
        Requirement(
            ["Wave Beam", "Missile Data", "Morph Ball"],
            [CanDoSimpleWallJump, HasSpaceJump]
        ),
        Requirement(
            ["Power Bomb Data", "Missile Data", "Morph Ball"],
            [CanDoSimpleWallJump, HasSpaceJump]
        ),
        Requirement(
            ["Power Bomb Data", "Charge Beam", "Morph Ball"],
            [CanDoSimpleWallJump, HasSpaceJump]
        ),
    ]

class CanCrossSector4RightWaterCorner(Requirement):
    name = "Can Cross Sector 4 Right Water Corner"
    items_needed = ["Missile Data", "Morph Ball", "Gravity Suit"]
    other_requirements = [
        CanFreezeEnemies,
        Requirement(["Space Jump"], []),
    ]

class CanCrossSector4LowerSecurityToRightWaterZone(Requirement):
    name = "Can Cross Sector 4 Lower Security to Right Water Zone"
    items_needed = ["Morph Ball", "Level 4 Keycard"]
    other_requirements = [
        Requirement(["Speed Booster"], [CanFreezeEnemies]),
        HasScrewAttack
    ]
    energy_tanks_needed = level_4_e_tanks
#endregion

#region Sector 5 Individual Requirements
class CanEscapeNightmareRoom(Requirement):
    name = "Can Escape Nightmare Room"
    items_needed = ["Gravity Suit", "Speed Booster"]
    other_requirements = [
        CanFightLateGameBoss, CanFightLategameBossOnAdvanced, CanFightBossOnExpert
    ]

class CanAccessRipperRoad(Requirement):
    name = "Can Access Ripper Road"
    items_needed = ["Morph Ball", "Hi-Jump"]
    other_requirements = [
        Requirement(["Bomb Data", "Screw Attack"], [CanFreezeEnemies]),
        Requirement(["Power Bomb Data"], [CanFreezeEnemies]),
    ]

class CanAccessRipperTreasure(Requirement):
    name = "Can Access Ripper Treasure"
    items_needed = ["Morph Ball", "Power Bomb Data"]
    other_requirements = [
        HasSpaceJump,
        Requirement(["Hi-Jump"], [CanFreezeEnemies]),
        Requirement(["Ice Beam"], [CanDoSimpleWallJump]),
        Requirement(["Missile Data", "Ice Missile"], [CanDoSimpleWallJump]),
        Requirement(["Missile Data", "Diffusion Missile"], [CanDoSimpleWallJump])
    ]
#endregion

#region Sector 6 Individual Requirements
#endregion

#endregion

#region Event Requirements
class CanDrainAQARequirement(Requirement):
    name = "Can Drain AQA Requirement"
    def __init__(self, items_needed, other_requirements, energy_tanks_needed=3):
        super().__init__(items_needed, other_requirements, energy_tanks_needed)
        self.items_needed.append("Pump Control Activated")
#endregion