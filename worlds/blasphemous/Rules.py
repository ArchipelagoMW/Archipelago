from typing import Dict, List, Tuple, Any, Callable, TYPE_CHECKING, Mapping
from BaseClasses import CollectionState
from worlds.generic.Rules import CollectionRule

if TYPE_CHECKING:
    from . import BlasphemousWorld
else:
    BlasphemousWorld = object


# Depending on a player's options, some logic can either always be True, or always be False.
# When combining rules together in load_rule(), optimizations can be made by checking whether a rule being combined is
# _always or _never.
def _always(state: CollectionState):
    return True


def _never(state: CollectionState):
    return False


def _bool_rule(b) -> CollectionRule:
    """Small helper to return the appropriate rule function for a rule that can be pre-calculated"""
    if b:
        return _always
    else:
        return _never


# Player strengths required to logically beat bosses.
# Mapping is an immutable type, so type hints should warn if attempts are made to modify it.
BOSS_STRENGTHS: Mapping[str, float] = {
    "warden": -0.10,
    "ten-piedad": 0.05,
    "charred-visage": 0.20,
    "tres-angustias": 0.15,
    "esdras": 0.25,
    "melquiades": 0.25,
    "exposito": 0.30,
    "quirce": 0.35,
    "crisanta": 0.50,
    "isidora": 0.70,
    "sierpes": 0.70,
    "amanecida": 0.60,
    "laudes": 0.60,
    "perpetua": -0.05,
    "legionary": 0.20
}


class BlasRules:
    player: int
    world: BlasphemousWorld
    string_rules: Dict[str, Callable[[CollectionState], bool]]

    upwarp_skips_allowed: bool
    mourning_skip_allowed: bool
    enemy_skips_allowed: bool
    obscure_skips_allowed: bool
    precise_skips_allowed: bool
    can_enemy_bounce: bool

    # Player strengths required to logically beat bosses, adjusted by the player's difficulty option.
    boss_strengths: Mapping[str, float]

    can_enemy_upslash: CollectionRule
    can_air_stall: CollectionRule
    can_dawn_jump: CollectionRule
    can_dive_laser: CollectionRule
    can_survive_poison_1: CollectionRule
    can_survive_poison_2: CollectionRule
    can_survive_poison_3: CollectionRule

    def __init__(self, world: "BlasphemousWorld") -> None:
        self.player = world.player
        self.world = world
        self.multiworld = world.multiworld
        self.indirect_conditions: List[Tuple[str, str]] = []

        difficulty = world.options.difficulty.value

        # Rules that can be fully or partially pre-calculated based on world.options.

        # Special Skips
        self.upwarp_skips_allowed = difficulty >= 2
        self.mourning_skip_allowed = difficulty >= 2
        self.enemy_skips_allowed = difficulty >= 2 and not world.options.enemy_randomizer.value
        self.obscure_skips_allowed = difficulty >= 2
        self.precise_skips_allowed = difficulty >= 2

        if difficulty >= 2:
            # Beating bosses ends up in logic earlier.
            self.boss_strengths = {boss: strength - 0.1 for boss, strength in BOSS_STRENGTHS.items()}
        elif difficulty >= 1:
            self.boss_strengths = BOSS_STRENGTHS
        else:
            # Beating bosses ends up in logic later.
            self.boss_strengths = {boss: strength + 0.1 for boss, strength in BOSS_STRENGTHS.items()}

        # Enemy tech
        if self.enemy_skips_allowed:
            self.can_enemy_bounce = True
            self.can_enemy_upslash = lambda state: self.combo(state) >= 2
        else:
            self.can_enemy_bounce = False
            self.can_enemy_upslash = _never

        # Movement tech
        if difficulty >= 1:
            self.can_air_stall = self.ranged
            self.can_dawn_jump = lambda state: self.dawn_heart(state) and self.dash(state)
        else:
            self.can_air_stall = _never
            self.can_dawn_jump = _never

        # Breakable tech
        if difficulty >= 2:
            self.can_dive_laser = lambda state: self.dive(state) >= 3
        else:
            self.can_dive_laser = _never

        # Lung tech
        if difficulty >= 2:
            self.can_survive_poison_1 = _always
            self.can_survive_poison_2 = lambda state: self.lung(state) or self.tiento(state)
            self.can_survive_poison_3 = lambda state: self.lung(state) or (self.tiento(state)
                                                                           and self.total_fervour(state) >= 120)
        elif difficulty >= 1:
            self.can_survive_poison_1 = lambda state: self.lung(state) or self.tiento(state)
            self.can_survive_poison_2 = lambda state: self.lung(state) or self.tiento(state)
            self.can_survive_poison_3 = self.lung
        else:
            self.can_survive_poison_1 = self.lung
            self.can_survive_poison_2 = self.lung
            self.can_survive_poison_3 = self.lung


        # BrandenEK/Blasphemous.Randomizer/ItemRando/BlasphemousInventory.cs
        self.string_rules: dict[str, CollectionRule] = {
            # Visibility flags
            "DoubleJump": _bool_rule(self.world.options.purified_hand.value),
            "NormalLogic": _bool_rule(self.world.options.difficulty.value >= 1),
            "NormalLogicAndDoubleJump": _bool_rule(self.world.options.difficulty.value >= 1
                                                   and bool(self.world.options.purified_hand.value)),
            "HardLogic": _bool_rule(self.world.options.difficulty.value >= 2),
            "HardLogicAndDoubleJump": _bool_rule(self.world.options.difficulty.value >= 2
                                                 and bool(self.world.options.purified_hand.value)),
            "EnemySkips": _bool_rule(self.enemy_skips_allowed),
            "EnemySkipsAndDoubleJump": _bool_rule(self.enemy_skips_allowed and self.world.options.purified_hand.value),

            # Relics
            "blood": self.blood,
            # skip "root"
            "linen": self.linen,
            "nail": self.nail,
            "shroud": self.shroud,
            # skip "lung"

            # Keys
            "bronzeKey": self.bronze_key,
            "silverKey": self.silver_key,
            "goldKey": self.gold_key,
            "peaksKey": self.peaks_key,
            "elderKey": self.elder_key,
            "woodKey": self.wood_key,

            # Collections
            "cherubs20": lambda state: self.cherubs(state) >= 20,
            "cherubs38": lambda state: self.cherubs(state) >= 38,

            "bones4": lambda state: self.bones(state, 4),
            "bones8": lambda state: self.bones(state, 8),
            "bones12": lambda state: self.bones(state, 12),
            "bones16": lambda state: self.bones(state, 16),
            "bones20": lambda state: self.bones(state, 20),
            "bones24": lambda state: self.bones(state, 24),
            "bones28": lambda state: self.bones(state, 28),
            "bones30": lambda state: self.bones(state, 30),
            "bones32": lambda state: self.bones(state, 32),
            "bones36": lambda state: self.bones(state, 36),
            "bones40": lambda state: self.bones(state, 40),
            "bones44": lambda state: self.bones(state, 44),

            "tears0": _always,

            # Special items
            "dash": self.dash,
            "wallClimb": self.wall_climb,
            # skip "airImpulse"
            "boots": self.boots,
            "doubleJump": self.double_jump,

            # Speed boosts
            "wheel": self.wheel,
            # skip "dawnHeart"

            # Health boosts
            # skip "flasks"
            # skip "quicksilver"

            # Puzzles
            "redWax1": lambda state: self.red_wax(state) >= 1,
            "redWax3": lambda state: self.red_wax(state) >= 3,
            "blueWax1": lambda state: self.blue_wax(state) >= 1,
            "blueWax3": lambda state: self.blue_wax(state) >= 3,
            "chalice": self.chalice,

            # Cherubs
            "debla": self.debla,
            "lorquiana": self.lorquiana,
            "zarabanda": self.zarabanda,
            "taranto": self.taranto,
            "verdiales": self.verdiales,
            "cante": self.cante,
            "cantina": self.cantina,

            "aubade": self.aubade,
            "tirana": self.tirana,

            "ruby": self.ruby,
            "tiento": self.tiento,
            # skip "anyPrayer"
            "pillar": self.pillar,

            # Stats
            # skip "healthLevel"
            # skip "fervourLevel"
            # skip "swordLevel"

            # Skills
            # skip "combo"
            # skip "charged"
            # skip "ranged"
            # skip "dive"
            # skip "lunge"
            "chargeBeam": self.charge_beam,
            "rangedAttack": self.ranged,

            # Main quest
            "holyWounds3": lambda state: self.holy_wounds(state, 3),
            "masks1": lambda state: self.masks(state, 1),
            "masks2": lambda state: self.masks(state, 2),
            "masks3": lambda state: self.masks(state, 3),
            "guiltBead": self.guilt_bead,

            # LOTL quest
            "cloth": self.cloth,
            "hand": self.hand,
            "hatchedEgg": self.hatched_egg,

            # Tirso quest
            "herbs1": lambda state: self.herbs(state, 1),
            "herbs2": lambda state: self.herbs(state, 2),
            "herbs3": lambda state: self.herbs(state, 3),
            "herbs4": lambda state: self.herbs(state, 4),
            "herbs5": lambda state: self.herbs(state, 5),
            "herbs6": lambda state: self.herbs(state, 6),

            # Tentudia quest
            "tentudiaRemains1": lambda state: self.tentudia_remains(state, 1),
            "tentudiaRemains2": lambda state: self.tentudia_remains(state, 2),
            "tentudiaRemains3": lambda state: self.tentudia_remains(state, 3),

            # Gemino quest
            "emptyThimble": self.empty_thimble,
            "fullThimble": self.full_thimble,
            "driedFlowers": self.dried_flowers,

            # Altasgracias quest
            "ceremonyItems3": lambda state: self.ceremony_items(state, 3),
            "egg": self.egg,

            # Redento quest
            # skip "limestones", not actually used
            # skip "knots", not actually used

            # Cleofas quest
            "marksOfRefuge3": lambda state: self.marks_of_refuge(state, 3),
            "cord": self.cord,

            # Crisanta quest
            "scapular": self.scapular,
            "trueHeart": self.true_heart,
            "traitorEyes2": lambda state: self.traitor_eyes(state, 2),

            # Jibrael quest
            "bell": self.bell,
            "verses4": lambda state: self.verses(state) >= 4,

            # Movement tech
            "canAirStall": self.can_air_stall,
            "canDawnJump": self.can_dawn_jump,
            "canWaterJump": self.can_water_jump,

            # Breakable tech
            "canBreakHoles": self.can_break_holes,
            "canDiveLaser": self.can_dive_laser,

            # Root tech
            "canWalkOnRoot": self.can_walk_on_root,
            "canClimbOnRoot": self.can_climb_on_root,

            # Lung tech
            "canSurvivePoison1": self.can_survive_poison_1,
            "canSurvivePoison2": self.can_survive_poison_2,
            "canSurvivePoison3": self.can_survive_poison_3,

            # Enemy tech
            "canEnemyBounce": _bool_rule(self.can_enemy_bounce),
            "canEnemyUpslash": self.can_enemy_upslash,

            # Reaching rooms
            "guiltRooms1": lambda state: self.guilt_rooms(state, 1),
            "guiltRooms2": lambda state: self.guilt_rooms(state, 2),
            "guiltRooms3": lambda state: self.guilt_rooms(state, 3),
            "guiltRooms4": lambda state: self.guilt_rooms(state, 4),
            "guiltRooms5": lambda state: self.guilt_rooms(state, 5),
            "guiltRooms6": lambda state: self.guilt_rooms(state, 6),
            "guiltRooms7": lambda state: self.guilt_rooms(state, 7),

            "swordRooms1": lambda state: self.sword_rooms(state, 1),
            "swordRooms2": lambda state: self.sword_rooms(state, 2),
            "swordRooms3": lambda state: self.sword_rooms(state, 3),
            "swordRooms4": lambda state: self.sword_rooms(state, 4),
            "swordRooms5": lambda state: self.sword_rooms(state, 5),
            "swordRooms6": lambda state: self.sword_rooms(state, 6),
            "swordRooms7": lambda state: self.sword_rooms(state, 7),

            "redentoRooms2": lambda state: self.redento_rooms(state, 2),
            "redentoRooms3": lambda state: self.redento_rooms(state, 3),
            "redentoRooms4": lambda state: self.redento_rooms(state, 4),
            "redentoRooms5": lambda state: self.redento_rooms(state, 5),

            "miriamRooms5": self.all_miriam_rooms,

            "amanecidaRooms1": lambda state: self.amanecida_rooms(state) >= 1,
            "amanecidaRooms2": lambda state: self.amanecida_rooms(state) >= 2,
            "amanecidaRooms3": lambda state: self.amanecida_rooms(state) >= 3,
            "amanecidaRooms4": lambda state: self.amanecida_rooms(state) >= 4,

            "chaliceRooms3": lambda state: self.chalice_rooms(state) >= 3,

            # Crossing gaps
            "canCrossGap1": self.can_cross_gap_1,
            "canCrossGap2": self.can_cross_gap_2,
            "canCrossGap3": self.can_cross_gap_3,
            "canCrossGap4": self.can_cross_gap_4,
            "canCrossGap5": self.can_cross_gap_5,
            "canCrossGap6": self.can_cross_gap_6,
            "canCrossGap7": self.can_cross_gap_7,
            "canCrossGap8": self.can_cross_gap_8,
            "canCrossGap9": self.can_cross_gap_9,
            "canCrossGap10": self.can_cross_gap_10,
            "canCrossGap11": self.can_cross_gap_11,

            # Events in different scenes
            "openedDCGateW": self.opened_dc_gate_w,
            "openedDCGateE": self.opened_dc_gate_e,
            "openedDCLadder": self.opened_dc_ladder,
            "openedWOTWCave": self.opened_wotw_cave,
            "rodeGotPElevator": self.rode_gotp_elevator,
            "openedConventLadder": self.opened_convent_ladder,
            "brokeJondoBellW": self.broke_jondo_bell_w,
            "brokeJondoBellE": self.broke_jondo_bell_e,
            "openedMoMLadder": self.opened_mom_ladder,
            "openedTSCGate": self.opened_tsc_gate,
            "openedARLadder": self.opened_ar_ladder,
            "brokeBotTCStatue": self.broke_bottc_statue,
            "openedWotHPGate": self.opened_wothp_gate,
            "openedBotSSLadder": self.opened_botss_ladder,

            # Special skips
            "upwarpSkipsAllowed": _bool_rule(self.upwarp_skips_allowed),
            "mourningSkipAllowed": _bool_rule(self.mourning_skip_allowed),
            "enemySkipsAllowed": _bool_rule(self.enemy_skips_allowed),
            "obscureSkipsAllowed": _bool_rule(self.obscure_skips_allowed),
            "preciseSkipsAllowed": _bool_rule(self.precise_skips_allowed),

            # Bosses
            "canBeatBrotherhoodBoss": self.can_beat_brotherhood_boss,
            "canBeatMercyBoss": self.can_beat_mercy_boss,
            "canBeatConventBoss": self.can_beat_convent_boss,
            "canBeatGrievanceBoss": self.can_beat_grievance_boss,
            "canBeatBridgeBoss": self.can_beat_bridge_boss,
            "canBeatMothersBoss": self.can_beat_mothers_boss,
            "canBeatCanvasesBoss": self.can_beat_canvases_boss,
            "canBeatPrisonBoss": self.can_beat_prison_boss,
            "canBeatRooftopsBoss": self.can_beat_rooftops_boss,
            "canBeatOssuaryBoss": self.can_beat_ossuary_boss,
            "canBeatMourningBoss": self.can_beat_mourning_boss,
            "canBeatGraveyardBoss": self.can_beat_graveyard_boss,
            "canBeatJondoBoss": self.can_beat_jondo_boss,
            "canBeatPatioBoss": self.can_beat_patio_boss,
            "canBeatWallBoss": self.can_beat_wall_boss,
            "canBeatHallBoss": self.can_beat_hall_boss,
            "canBeatPerpetua": self.can_beat_perpetua,
            "canBeatLegionary": self.can_beat_legionary
        }

        boss_strength_indirect_regions: List[str] = [
            # flasks
            "D01Z05S05[SW]",
            "D02Z02S04[W]",
            "D03Z02S08[W]",
            "D03Z03S04[SW]",
            "D04Z02S13[W]",
            "D05Z01S08[NW]",
            "D20Z01S07[NE]",
            # quicksilver
            "D01Z05S01[W]"
        ]

        guilt_indirect_regions: List[str] = [
            "D01Z04S01[NE]",
            "D02Z02S11[W]",
            "D03Z03S02[NE]",
            "D04Z02S02[SE]",
            "D05Z01S05[NE]",
            "D09Z01S05[W]",
            "D17Z01S04[W]"
        ]

        sword_indirect_regions: List[str] = [
            "D01Z02S07[E]",
            "D01Z02S02[SW]",
            "D20Z01S04[E]",
            "D01Z05S23[W]",
            "D02Z03S02[NE]",
            "D04Z02S21[NE]",
            "D05Z01S21[NW]",
            "D06Z01S15[NE]",
            "D17Z01S07[SW]"
        ]

        redento_indirect_regions: List[str] = [
            "D03Z01S04[E]",
            "D03Z02S10[N]",
            "D17Z01S05[S]",
            "D17BZ02S01[FrontR]",
            "D01Z03S04[E]",
            "D08Z01S01[W]",
            "D04Z01S03[E]",
            "D04Z02S01[W]",
            "D06Z01S18[-Cherubs]",
            "D04Z02S08[E]",
            "D04BZ02S01[Redento]",
            "D17Z01S07[NW]"
        ]

        miriam_indirect_regions: List[str] = [
            "D02Z03S07[NWW]",
            "D03Z03S07[NW]",
            "D04Z04S01[E]",
            "D05Z01S06[W]",
            "D06Z01S17[E]"
        ]

        chalice_indirect_regions: List[str] = [
            "D03Z01S02[E]",
            "D01Z05S02[W]",
            "D20Z01S03[N]",
            "D05Z01S11[SE]",
            "D05Z02S02[NW]",
            "D09Z01S09[E]",
            "D09Z01S10[W]",
            "D09Z01S08[SE]",
            "D09Z01S02[SW]"
        ]

        self.indirect_regions: Dict[str, List[str]] = {
            "openedDCGateW":          ["D20Z01S04[E]",
                                       "D01Z05S23[W]"],
            "openedDCGateE":          ["D01Z05S10[SE]",
                                       "D01Z04S09[W]"],
            "openedDCLadder":         ["D01Z05S25[NE]",
                                       "D01Z05S02[S]"],
            "openedWOTWCave":         ["D02Z01S01[SW]",
                                       "D02Z01S08[E]",
                                       "D02Z01S02[]"],
            "rodeGotPElevator":       ["D02Z03S14[E]",
                                       "D02Z02S13[W]",
                                       "D02Z02S06[E]",
                                       "D02Z02S12[W]",
                                       "D02Z02S08[W]"],
            "openedConventLadder":    ["D02Z03S02[N]",
                                       "D02Z03S15[E]",
                                       "D02Z03S19[E]",
                                       "D02Z03S10[W]",
                                       "D02Z03S22[W]"],
            "brokeJondoBellW":        ["D03Z02S08[N]",
                                       "D03Z02S12[E]",
                                       "D03Z02S10[S]",
                                       "D03Z02S10[-Cherubs]"],
            "brokeJondoBellE":        ["D03Z02S04[NE]",
                                       "D03Z02S11[W]",
                                       "D03Z02S03[E]"],
            "openedMoMLadder":        ["D04Z02S11[E]",
                                       "D04Z02S09[W]",
                                       "D06Z01S23[S]",
                                       "D04Z02S04[N]"],
            "openedTSCGate":          ["D05Z02S06[SE]",
                                       "D05Z01S21[-Cherubs]"],
            "openedARLadder":         ["D06Z01S22[Sword]",
                                       "D06Z01S20[W]",
                                       "D04Z02S06[N]",
                                       "D06Z01S01[-Cherubs]"],
            "brokeBotTCStatue":       ["D08Z03S03[W]",
                                       "D08Z02S03[W]"],
            "openedWotHPGate":        ["D09Z01S13[E]",
                                       "D09Z01S03[W]",
                                       "D09Z01S08[W]"],
            "openedBotSSLadder":      ["D17Z01S05[S]",
                                       "D17BZ02S01[FrontR]"],
            "canBeatBrotherhoodBoss": [*boss_strength_indirect_regions,
                                       "D17Z01S05[E]",
                                       "D17Z01S03[W]"],
            "canBeatMercyBoss":       [*boss_strength_indirect_regions,
                                       "D01Z04S19[E]",
                                       "D01Z04S12[W]"],
            "canBeatConventBoss":     [*boss_strength_indirect_regions,
                                       "D02Z03S09[E]",
                                       "D02Z03S21[W]"],
            "canBeatGrievanceBoss":   [*boss_strength_indirect_regions,
                                       "D03Z03S11[E]",
                                       "D03Z03S16[W]"],
            "canBeatBridgeBoss":      [*boss_strength_indirect_regions,
                                       "D01Z03S06[E]",
                                       "D08Z02S01[W]"],
            "canBeatMothersBoss":     [*boss_strength_indirect_regions,
                                       "D04Z02S15[E]",
                                       "D04Z02S21[W]"],
            "canBeatCanvasesBoss":    [*boss_strength_indirect_regions,
                                       "D05Z02S06[NE]",
                                       "D05Z01S21[SW]"],
            "canBeatPrisonBoss":      [*boss_strength_indirect_regions,
                                       "D09Z01S05[SE]",
                                       "D09Z01S08[S]"],
            "canBeatRooftopsBoss":    [*boss_strength_indirect_regions,
                                       "D06Z01S19[E]",
                                       "D07Z01S01[W]"],
            "canBeatOssuaryBoss":     [*boss_strength_indirect_regions,
                                       "D01BZ06S01[E]"],
            "canBeatMourningBoss":    [*boss_strength_indirect_regions,
                                       "D20Z02S07[W]"],
            "canBeatGraveyardBoss":   [*boss_strength_indirect_regions,
                                       "D01Z06S01[Santos]",
                                       "D02Z03S18[NW]",
                                       "D02Z02S03[NE]"],
            "canBeatJondoBoss":       [*boss_strength_indirect_regions,
                                       "D01Z06S01[Santos]",
                                       "D20Z01S06[NE]",
                                       "D20Z01S04[W]",
                                       "D03Z01S04[E]",
                                       "D03Z02S10[N]"],
            "canBeatPatioBoss":       [*boss_strength_indirect_regions,
                                       "D01Z06S01[Santos]",
                                       "D06Z01S02[W]",
                                       "D04Z01S03[E]",
                                       "D04Z01S01[W]",
                                       "D06Z01S18[-Cherubs]"],
            "canBeatWallBoss":        [*boss_strength_indirect_regions,
                                       "D01Z06S01[Santos]",
                                       "D09Z01S09[Cell24]",
                                       "D09Z01S11[E]",
                                       "D06Z01S13[W]"],
            "canBeatHallBoss":        [*boss_strength_indirect_regions,
                                       "D08Z01S02[NE]",
                                       "D08Z03S02[NW]"],
            "canBeatPerpetua":        boss_strength_indirect_regions,
            "canBeatLegionary":       boss_strength_indirect_regions,
            "guiltRooms1":            guilt_indirect_regions,
            "guiltRooms2":            guilt_indirect_regions,
            "guiltRooms3":            guilt_indirect_regions,
            "guiltRooms4":            guilt_indirect_regions,
            "guiltRooms5":            guilt_indirect_regions,
            "guiltRooms6":            guilt_indirect_regions,
            "guiltRooms7":            guilt_indirect_regions,
            "swordRooms1":            sword_indirect_regions,
            "swordRooms2":            sword_indirect_regions,
            "swordRooms3":            sword_indirect_regions,
            "swordRooms4":            sword_indirect_regions,
            "swordRooms5":            sword_indirect_regions,
            "swordRooms6":            sword_indirect_regions,
            "swordRooms7":            sword_indirect_regions,
            "redentoRooms2":          redento_indirect_regions,
            "redentoRooms3":          redento_indirect_regions,
            "redentoRooms4":          redento_indirect_regions,
            "redentoRooms5":          redento_indirect_regions,
            "miriamRooms5":           miriam_indirect_regions,
            "chaliceRooms3":          chalice_indirect_regions
        }

        self.indirect_regions["amanecidaRooms1"] = [*self.indirect_regions["canBeatGraveyardBoss"],
                                                    *self.indirect_regions["canBeatJondoBoss"],
                                                    *self.indirect_regions["canBeatPatioBoss"],
                                                    *self.indirect_regions["canBeatWallBoss"]]
        self.indirect_regions["amanecidaRooms2"] = [*self.indirect_regions["canBeatGraveyardBoss"],
                                                    *self.indirect_regions["canBeatJondoBoss"],
                                                    *self.indirect_regions["canBeatPatioBoss"],
                                                    *self.indirect_regions["canBeatWallBoss"]]
        self.indirect_regions["amanecidaRooms3"] = [*self.indirect_regions["canBeatGraveyardBoss"],
                                                    *self.indirect_regions["canBeatJondoBoss"],
                                                    *self.indirect_regions["canBeatPatioBoss"],
                                                    *self.indirect_regions["canBeatWallBoss"]]
        self.indirect_regions["amanecidaRooms4"] = [*self.indirect_regions["canBeatGraveyardBoss"],
                                                    *self.indirect_regions["canBeatJondoBoss"],
                                                    *self.indirect_regions["canBeatPatioBoss"],
                                                    *self.indirect_regions["canBeatWallBoss"]]


    def req_is_region(self, string: str) -> bool:
        return (string[0] == "D" and string[3] == "Z" and string[6] == "S")\
            or (string[0] == "D" and string[3] == "B" and string[4] == "Z" and string[7] == "S")

    def load_rule(self, obj_is_region: bool, name: str, obj: Dict[str, Any]) -> Callable[[CollectionState], bool]:
        clauses = []
        clauses_are_impossible_if_empty = False
        rule_indirect_conditions = []
        for clause in obj["logic"]:
            reqs = []
            clause_indirect_conditions = []
            clause_is_impossible = False
            for req in clause["item_requirements"]:
                if self.req_is_region(req):
                    if obj_is_region:
                        # add to indirect conditions if object and requirement are doors
                        clause_indirect_conditions.append((req, f"{name} -> {obj['target']}"))
                    reqs.append(lambda state, req=req: state.can_reach_region(req, self.player))
                else:
                    string_rule = self.string_rules[req]
                    if string_rule is _never:
                        # This clause is not possible with the options this player has chosen.
                        clause_is_impossible = True
                        break
                    elif string_rule is _always:
                        # Don't need to add a rule that is always True with the options this player has chosen.
                        # Continue to the next requirement.
                        continue
                    if obj_is_region and req in self.indirect_regions:
                        # add to indirect conditions if object is door and requirement has list of regions
                        for region in self.indirect_regions[req]:
                            clause_indirect_conditions.append((region, f"{name} -> {obj['target']}"))
                    reqs.append(self.string_rules[req])
            if clause_is_impossible:
                # At least one clause was impossible, so if all clauses were impossible, the entire rule is impossible.
                clauses_are_impossible_if_empty = True
                # Continue to the next clause.
                continue
            rule_indirect_conditions.extend(clause_indirect_conditions)

            # Combine the requirements if there are multiple.
            # Requirements are AND-ed together.
            if len(reqs) == 1:
                clauses.append(reqs[0])
            else:
                def req_func(state, reqs=reqs):
                    for req in reqs:
                        if not req(state):
                            return False
                    return True
                clauses.append(req_func)

        # Combine the clauses if there are multiple.
        # Clauses are OR-ed together.
        if not clauses:
            # There is no need to register the indirect conditions if it turns out the rule is impossible or always
            # possible.
            rule_indirect_conditions.clear()
            if clauses_are_impossible_if_empty:
                to_return = _never
            else:
                to_return = _always
        elif len(clauses) == 1:
            to_return = clauses[0]
        else:
            def clause_func(state, clauses=clauses):
                for clause in clauses:
                    if clause(state):
                        return True
                return False
            to_return = clause_func
        # Update the list of indirect conditions to add.
        self.indirect_conditions.extend(rule_indirect_conditions)
        return to_return

    # Relics
    def blood(self, state: CollectionState) -> bool:
        return state.has("Blood Perpetuated in Sand", self.player)
    
    def root(self, state: CollectionState) -> bool:
        return state.has("Three Gnarled Tongues", self.player)

    def linen(self, state: CollectionState) -> bool:
        return state.has("Linen of Golden Thread", self.player)
    
    def nail(self, state: CollectionState) -> bool:
        return state.has("Nail Uprooted from Dirt", self.player)
    
    def shroud(self, state: CollectionState) -> bool:
        return state.has("Shroud of Dreamt Sins", self.player)

    def lung(self, state: CollectionState) -> bool:
        return state.has("Silvered Lung of Dolphos", self.player)
    
    # Keys
    def bronze_key(self, state: CollectionState) -> bool:
        return state.has("Key of the Secular", self.player)
    
    def silver_key(self, state: CollectionState) -> bool:
        return state.has("Key of the Scribe", self.player)
    
    def gold_key(self, state: CollectionState) -> bool:
        return state.has("Key of the Inquisitor", self.player)

    def peaks_key(self, state: CollectionState) -> bool:
        return state.has("Key of the High Peaks", self.player)
    
    def elder_key(self, state: CollectionState) -> bool:
        return state.has("Key to the Chamber of the Eldest Brother", self.player)
    
    def wood_key(self, state: CollectionState) -> bool:
        return state.has("Key Grown from Twisted Wood", self.player)
    
    # Collections
    def cherubs(self, state: CollectionState) -> int:
        return state.count("Child of Moonlight", self.player)
    
    def bones(self, state: CollectionState, count: int) -> bool:
        # Count of unique items in the "bones" item group that have been collected into state.
        # BlasphemousWorld.collect/remove adjust the count when items in the group are collected/removed.
        return state.has("bones", self.player, count)
    
    # def tears():

    # Special items
    def dash(self, state: CollectionState) -> bool:
        return state.has("Dash Ability", self.player)

    def wall_climb(self, state: CollectionState) -> bool:
        return state.has("Wall Climb Ability", self.player)
    
    #def air_impulse():

    def boots(self, state: CollectionState) -> bool:
        return state.has("Boots of Pleading", self.player)
    
    def double_jump(self, state: CollectionState) -> bool:
        return state.has("Purified Hand of the Nun", self.player)

    # Speed boosts
    def wheel(self, state: CollectionState) -> bool:
        return state.has("The Young Mason's Wheel", self.player)

    def dawn_heart(self, state: CollectionState) -> bool:
        return state.has("Brilliant Heart of Dawn", self.player)

    # Health boosts
    def flasks(self, state: CollectionState) -> int:
        doors = (
            "D01Z05S05[SW]",
            "D02Z02S04[W]",
            "D03Z02S08[W]",
            "D03Z03S04[SW]",
            "D04Z02S13[W]",
            "D05Z01S08[NW]",
            "D20Z01S07[NE]"
        )
        for door in doors:
            if state.can_reach_region(door, self.player):
                return state.count("Empty Bile Vessel", self.player)
        return 0
    
    def quicksilver(self, state: CollectionState) -> int:
        return state.count("Quicksilver", self.player) if state.can_reach_region("D01Z05S01[W]", self.player) else 0
    
    # Puzzles
    def red_wax(self, state: CollectionState) -> int:
        return state.count("Bead of Red Wax", self.player)

    def blue_wax(self, state: CollectionState) -> int:
        return state.count("Bead of Blue Wax", self.player)
    
    def chalice(self, state: CollectionState) -> bool:
        return state.has("Chalice of Inverted Verses", self.player)
    
    # Cherubs
    def debla(self, state: CollectionState) -> bool:
        return state.has("Debla of the Lights", self.player)
    
    def lorquiana(self, state: CollectionState) -> bool:
        return state.has("Lorquiana", self.player)
    
    def zarabanda(self, state: CollectionState) -> bool:
        return state.has("Zarabanda of the Safe Haven", self.player)
    
    def taranto(self, state: CollectionState) -> bool:
        return state.has("Taranto to my Sister", self.player)
    
    def verdiales(self, state: CollectionState) -> bool:
        return state.has("Verdiales of the Forsaken Hamlet", self.player)
    
    def cante(self, state: CollectionState) -> bool:
        return state.has("Cante Jondo of the Three Sisters", self.player)
    
    def cantina(self, state: CollectionState) -> bool:
        return state.has("Cantina of the Blue Rose", self.player)

    def aubade(self, state: CollectionState) -> bool:
        return (
            state.has("Aubade of the Nameless Guardian", self.player)
            and self.total_fervour(state) >= 90
        )
    
    def tirana(self, state: CollectionState) -> bool:
        return (
            state.has("Tirana of the Celestial Bastion", self.player)
            and self.total_fervour(state) >= 90
        )

    def ruby(self, state: CollectionState) -> bool:
        return state.has("Cloistered Ruby", self.player)
    
    def tiento(self, state: CollectionState) -> bool:
        return state.has("Tiento to my Sister", self.player)
    
    def any_small_prayer(self, state: CollectionState) -> bool:
        return (
            self.debla(state)
            or self.lorquiana(state)
            or self.zarabanda(state)
            or self.taranto(state)
            or self.verdiales(state)
            or self.cante(state)
            or self.cantina(state)
            or self.tiento(state)
            or state.has_any((
                "Campanillero to the Sons of the Aurora",
                "Mirabras of the Return to Port",
                "Romance to the Crimson Mist",
                "Saeta Dolorosa",
                "Seguiriya to your Eyes like Stars",
                "Verdiales of the Forsaken Hamlet",
                "Zambra to the Resplendent Crown"
            ), self.player)
        )
    
    def pillar(self, state: CollectionState) -> bool:
        return (
            self.debla(state)
            or self.taranto(state)
            or self.ruby(state)
        )
    
    def can_use_any_prayer(self, state: CollectionState) -> bool:
        return (
            self.any_small_prayer(state)
            or self.tirana(state)
            or self.aubade(state)
        )

    # Stats
    def total_fervour(self, state: CollectionState) -> int:
        return (
            60
            + (20 * min(6, state.count("Fervour Upgrade", self.player)))
            + (10 * min(3, state.count("Bead of Blue Wax", self.player)))
        )

    # Skills
    def combo(self, state: CollectionState) -> int:
        return state.count("Combo Skill", self.player)

    def charged(self, state: CollectionState) -> int:
        return state.count("Charged Skill", self.player)

    def ranged(self, state: CollectionState) -> bool:
        return state.has("Ranged Skill", self.player)
    
    def dive(self, state: CollectionState) -> int:
        return state.count("Dive Skill", self.player)
    
    def lunge(self, state: CollectionState) -> int:
        return state.count("Lunge Skill", self.player)
    
    def charge_beam(self, state: CollectionState) -> bool:
        return self.charged(state) >= 3
    
    # Main quest
    def holy_wounds(self, state: CollectionState, count: int) -> bool:
        # Count of unique items in the "wounds" item group that have been collected into state.
        # BlasphemousWorld.collect/remove adjust the count when items in the group are collected/removed.
        return state.has("wounds", self.player, count)
    
    def masks(self, state: CollectionState, count: int) -> bool:
        # Count of unique items in the "masks" item group that have been collected into state.
        # BlasphemousWorld.collect/remove adjust the count when items in the group are collected/removed.
        return state.has("masks", self.player, count)
    
    def guilt_bead(self, state: CollectionState) -> bool:
        return state.has("Weight of True Guilt", self.player)
    
    # LOTL quest
    def cloth(self, state: CollectionState) -> bool:
        return state.has("Linen Cloth", self.player)
    
    def hand(self, state: CollectionState) -> bool:
        return state.has("Severed Hand", self.player)

    def hatched_egg(self, state: CollectionState) -> bool:
        return state.has("Hatched Egg of Deformity", self.player)
    
    # Tirso quest
    def herbs(self, state: CollectionState, count: int) -> bool:
        # Count of unique items in the "tirso" item group that have been collected into state.
        # BlasphemousWorld.collect/remove adjust the count when items in the group are collected/removed.
        return state.has("tirso", self.player, count)
    
    # Tentudia quest
    def tentudia_remains(self, state: CollectionState, count: int) -> bool:
        # Count of unique items in the "tentudia" item group that have been collected into state.
        # BlasphemousWorld.collect/remove adjust the count when items in the group are collected/removed.
        return state.has("tentudia", self.player, count)
    
    # Gemino quest
    def empty_thimble(self, state: CollectionState) -> bool:
        return state.has("Empty Golden Thimble", self.player)
    
    def full_thimble(self, state: CollectionState) -> bool:
        return state.has("Golden Thimble Filled with Burning Oil", self.player)
    
    def dried_flowers(self, state: CollectionState) -> bool:
        return state.has("Dried Flowers bathed in Tears", self.player)
    
    # Altasgracias quest
    def ceremony_items(self, state: CollectionState, count: int) -> bool:
        # Count of unique items in the "egg" item group that have been collected into state.
        # BlasphemousWorld.collect/remove adjust the count when items in the group are collected/removed.
        return state.has("egg", self.player, count)
    
    def egg(self, state: CollectionState) -> bool:
        return state.has("Egg of Deformity", self.player)
    
    # Redento quest
    def limestones(self, state: CollectionState, count: int) -> bool:
        # Count of unique items in the "toe" item group that have been collected into state.
        # BlasphemousWorld.collect/remove adjust the count when items in the group are collected/removed.
        return state.has("toe", self.player, count)
    
    def knots(self, state: CollectionState) -> int:
        return state.count("Knot of Rosary Rope", self.player) if state.can_reach_region("D17Z01S07[NW]", self.player)\
            else 0
    
    # Cleofas quest
    def marks_of_refuge(self, state: CollectionState, count: int) -> bool:
        # Count of unique items in the "marks" item group that have been collected into state.
        # BlasphemousWorld.collect/remove adjust the count when items in the group are collected/removed.
        return state.has("marks", self.player, count)
    
    def cord(self, state: CollectionState) -> bool:
        return state.has("Cord of the True Burying", self.player)
    
    # Crisanta quest
    def scapular(self, state: CollectionState) -> bool:
        return state.has("Incomplete Scapular", self.player)
    
    def true_heart(self, state: CollectionState) -> bool:
        return state.has("Apodictic Heart of Mea Culpa", self.player)
    
    def traitor_eyes(self, state: CollectionState, count: int) -> bool:
        # Count of unique items in the "eye" item group that have been collected into state.
        # BlasphemousWorld.collect/remove adjust the count when items in the group are collected/removed.
        return state.has("eye", self.player, count)
    
    # Jibrael quest
    def bell(self, state: CollectionState) -> bool:
        return state.has("Petrified Bell", self.player)
    
    def verses(self, state: CollectionState) -> int:
        return state.count("Verses Spun from Gold", self.player)
    
    # Movement tech
    def can_water_jump(self, state: CollectionState) -> bool:
        return (
            self.nail(state)
            or self.double_jump(state)
        )
    
    # Breakable tech
    def can_break_holes(self, state: CollectionState) -> bool:
        return (
            self.charged(state) > 0
            or self.dive(state) > 0
            or self.lunge(state) >= 3 and self.dash(state)
            or self.can_use_any_prayer(state)
        )
    
    # Root tech
    def can_walk_on_root(self, state: CollectionState) -> bool:
        return self.root(state)
    
    def can_climb_on_root(self, state: CollectionState) -> bool:
        return (
            self.root(state)
            and self.wall_climb(state)
        )
    
    # Crossing gaps
    def can_cross_gap_1(self, state: CollectionState) -> bool:
        return (
            self.double_jump(state)
            or self.can_dawn_jump(state)
            or self.wheel(state)
            or self.can_air_stall(state)
        )
    
    def can_cross_gap_2(self, state: CollectionState) -> bool:
        return (
            self.double_jump(state)
            or self.can_dawn_jump(state)
            or self.wheel(state)
        )
    
    def can_cross_gap_3(self, state: CollectionState) -> bool:
        return (
            self.double_jump(state)
            or self.can_dawn_jump(state)
            or self.wheel(state)
            and self.can_air_stall(state)
        )
    
    def can_cross_gap_4(self, state: CollectionState) -> bool:
        return (
            self.double_jump(state)
            or self.can_dawn_jump(state)
        )
    
    def can_cross_gap_5(self, state: CollectionState) -> bool:
        return (
            self.double_jump(state)
            or self.can_dawn_jump(state)
            and self.can_air_stall(state)
        )
    
    def can_cross_gap_6(self, state: CollectionState) -> bool:
        return self.double_jump(state)

    def can_cross_gap_7(self, state: CollectionState) -> bool:
        return (
            self.double_jump(state)
            and (
                self.can_dawn_jump(state)
                or self.wheel(state)
                or self.can_air_stall(state)
            )
        )
    
    def can_cross_gap_8(self, state: CollectionState) -> bool:
        return (
            self.double_jump(state)
            and (
                self.can_dawn_jump(state)
                or self.wheel(state)
            )
        )
    
    def can_cross_gap_9(self, state: CollectionState) -> bool:
        return (
            self.double_jump(state)
            and (
                self.can_dawn_jump(state)
                or self.wheel(state)
                and self.can_air_stall(state)
            )
        )
    
    def can_cross_gap_10(self, state: CollectionState) -> bool:
        return (
            self.double_jump(state)
            and self.can_dawn_jump(state)
        )
    
    def can_cross_gap_11(self, state: CollectionState) -> bool:
        return (
            self.double_jump(state)
            and self.can_dawn_jump(state)
            and self.can_air_stall(state)
        )

    # Events that trigger in different scenes
    def opened_dc_gate_w(self, state: CollectionState) -> bool:
        return (
            state.can_reach_region("D20Z01S04[E]", self.player)
            or state.can_reach_region("D01Z05S23[W]", self.player)
        )
    
    def opened_dc_gate_e(self, state: CollectionState) -> bool:
        return (
            state.can_reach_region("D01Z05S10[SE]", self.player)
            or state.can_reach_region("D01Z04S09[W]", self.player)
        )
    
    def opened_dc_ladder(self, state: CollectionState) -> bool:
        return (
            state.can_reach_region("D01Z05S25[NE]", self.player)
            or state.can_reach_region("D01Z05S02[S]", self.player)
        )
    
    def opened_wotw_cave(self, state: CollectionState) -> bool:
        return (
            state.can_reach_region("D02Z01S01[SW]", self.player)
            or self.wall_climb(state)
            and state.can_reach_region("D02Z01S08[E]", self.player)
            or state.can_reach_region("D02Z01S02[]", self.player)
        )
    
    def rode_gotp_elevator(self, state: CollectionState) -> bool:
        return (
            state.can_reach_region("D02Z03S14[E]", self.player)
            or state.can_reach_region("D02Z02S13[W]", self.player)
            or state.can_reach_region("D02Z02S06[E]", self.player)
            or state.can_reach_region("D02Z02S12[W]", self.player)
            or state.can_reach_region("D02Z02S08[W]", self.player)
        )
    
    def opened_convent_ladder(self, state: CollectionState) -> bool:
        return (
            state.can_reach_region("D02Z03S02[N]", self.player)
            or state.can_reach_region("D02Z03S15[E]", self.player)
            or state.can_reach_region("D02Z03S19[E]", self.player)
            or state.can_reach_region("D02Z03S10[W]", self.player)
            or state.can_reach_region("D02Z03S22[W]", self.player)
        )
    
    def broke_jondo_bell_w(self, state: CollectionState) -> bool:
        return (
            state.can_reach_region("D03Z02S08[N]", self.player)
            or state.can_reach_region("D03Z02S12[E]", self.player)
            and self.dash(state)
            or state.can_reach_region("D03Z02S10[S]", self.player)
            or state.can_reach_region("D03Z02S10[-Cherubs]", self.player)
        )
    
    def broke_jondo_bell_e(self, state: CollectionState) -> bool:
        return (
            state.can_reach_region("D03Z02S04[NE]", self.player)
            or state.can_reach_region("D03Z02S11[W]", self.player)
            or state.can_reach_region("D03Z02S03[E]", self.player)
            and (
                self.can_cross_gap_5(state)
                or self.can_enemy_bounce
                and self.can_cross_gap_3(state)
            )
        )

    def opened_mom_ladder(self, state: CollectionState) -> bool:
        return (
            state.can_reach_region("D04Z02S11[E]", self.player)
            or state.can_reach_region("D04Z02S09[W]", self.player)
            or state.can_reach_region("D06Z01S23[S]", self.player)
            or state.can_reach_region("D04Z02S04[N]", self.player)
        )
    
    def opened_tsc_gate(self, state: CollectionState) -> bool:
        return (
            state.can_reach_region("D05Z02S06[SE]", self.player)
            or state.can_reach_region("D05Z01S21[-Cherubs]", self.player)
        )
    
    def opened_ar_ladder(self, state: CollectionState) -> bool:
        return (
            state.can_reach_region("D06Z01S22[Sword]", self.player)
            or state.can_reach_region("D06Z01S20[W]", self.player)
            or state.can_reach_region("D04Z02S06[N]", self.player)
            or state.can_reach_region("D06Z01S01[-Cherubs]", self.player)
        )
    
    def broke_bottc_statue(self, state: CollectionState) -> bool:
        return (
            state.can_reach_region("D08Z03S03[W]", self.player)
            or state.can_reach_region("D08Z02S03[W]", self.player)
        )
    
    def opened_wothp_gate(self, state: CollectionState) -> bool:
        return (
            state.can_reach_region("D09Z01S13[E]", self.player)
            or state.can_reach_region("D09Z01S03[W]", self.player)
            or state.can_reach_region("D09Z01S08[W]", self.player)
        )
    
    def opened_botss_ladder(self, state: CollectionState) -> bool:
        return (
            state.can_reach_region("D17Z01S05[S]", self.player)
            or state.can_reach_region("D17BZ02S01[FrontR]", self.player)
        )
    
    # Bosses
    def can_beat_brotherhood_boss(self, state: CollectionState) -> bool:
        return (
            self.has_boss_strength(state, "warden")
            and (
                state.can_reach_region("D17Z01S05[E]", self.player)
                or state.can_reach_region("D17Z01S03[W]", self.player)
            )
        )

    def can_beat_mercy_boss(self, state: CollectionState) -> bool:
        return (
            self.has_boss_strength(state, "ten-piedad")
            and (
                state.can_reach_region("D01Z04S19[E]", self.player)
                or state.can_reach_region("D01Z04S12[W]", self.player)
            )
        )
    
    def can_beat_convent_boss(self, state: CollectionState) -> bool:
        return (
            self.has_boss_strength(state, "charred-visage")
            and (
                state.can_reach_region("D02Z03S09[E]", self.player)
                or state.can_reach_region("D02Z03S21[W]", self.player)
            )
        )
    
    def can_beat_grievance_boss(self, state: CollectionState) -> bool:
        return (
            self.has_boss_strength(state, "tres-angustias")
            and (
                self.wall_climb(state)
                or self.double_jump(state)
            ) and (
                state.can_reach_region("D03Z03S11[E]", self.player)
                or state.can_reach_region("D03Z03S16[W]", self.player)
            )
        )
    
    def can_beat_bridge_boss(self, state: CollectionState) -> bool:
        return (
            self.has_boss_strength(state, "esdras")
            and (
                state.can_reach_region("D01Z03S06[E]", self.player)
                or state.can_reach_region("D08Z02S01[W]", self.player)
            )
        )
    
    def can_beat_mothers_boss(self, state: CollectionState) -> bool:
        return (
            self.has_boss_strength(state, "melquiades")
            and (
                state.can_reach_region("D04Z02S15[E]", self.player)
                or state.can_reach_region("D04Z02S21[W]", self.player)
            )
        )
    
    def can_beat_canvases_boss(self, state: CollectionState) -> bool:
        return (
            self.has_boss_strength(state, "exposito")
            and (
                state.can_reach_region("D05Z02S06[NE]", self.player)
                or state.can_reach_region("D05Z01S21[SW]", self.player)
            )
        )
    
    def can_beat_prison_boss(self, state: CollectionState) -> bool:
        return (
            self.has_boss_strength(state, "quirce")
            and (
                state.can_reach_region("D09Z01S05[SE]", self.player)
                or state.can_reach_region("D09Z01S08[S]", self.player)
            )
        )
    
    def can_beat_rooftops_boss(self, state: CollectionState) -> bool:
        return (
            self.has_boss_strength(state, "crisanta")
            and (
                state.can_reach_region("D06Z01S19[E]", self.player)
                or state.can_reach_region("D07Z01S01[W]", self.player)
            )
        )
    
    def can_beat_ossuary_boss(self, state: CollectionState) -> bool:
        return (
            self.has_boss_strength(state, "isidora")
            and state.can_reach_region("D01BZ06S01[E]", self.player)
        )
    
    def can_beat_mourning_boss(self, state: CollectionState) -> bool:
        return (
            self.has_boss_strength(state, "sierpes")
            and state.can_reach_region("D20Z02S07[W]", self.player)
        )
    
    def can_beat_graveyard_boss(self, state: CollectionState, player_strength: float | None = None) -> bool:
        return (
            self.has_boss_strength(state, "amanecida", player_strength)
            and self.wall_climb(state)
            and state.can_reach_region("D01Z06S01[Santos]", self.player)
            and state.can_reach_region("D02Z03S18[NW]", self.player)
            and state.can_reach_region("D02Z02S03[NE]", self.player)
        )
    
    def can_beat_jondo_boss(self, state: CollectionState, player_strength: float | None = None) -> bool:
        return (
            self.has_boss_strength(state, "amanecida", player_strength)
            and state.can_reach_region("D01Z06S01[Santos]", self.player)
            and (
                state.can_reach_region("D20Z01S06[NE]", self.player)
                or state.can_reach_region("D20Z01S04[W]", self.player)
            )
            and (
                state.can_reach_region("D03Z01S04[E]", self.player)
                or state.can_reach_region("D03Z02S10[N]", self.player)
            )
        )
    
    def can_beat_patio_boss(self, state: CollectionState, player_strength: float | None = None) -> bool:
        return (
            self.has_boss_strength(state, "amanecida", player_strength)
            and state.can_reach_region("D01Z06S01[Santos]", self.player)
            and state.can_reach_region("D06Z01S02[W]", self.player)
            and (
                state.can_reach_region("D04Z01S03[E]", self.player)
                or state.can_reach_region("D04Z01S01[W]", self.player)
                or state.can_reach_region("D06Z01S18[-Cherubs]", self.player)
            )
        )
    
    def can_beat_wall_boss(self, state: CollectionState, player_strength: float | None = None) -> bool:
        return (
            self.has_boss_strength(state, "amanecida", player_strength)
            and state.can_reach_region("D01Z06S01[Santos]", self.player)
            and state.can_reach_region("D09Z01S09[Cell24]", self.player)
            and (
                state.can_reach_region("D09Z01S11[E]", self.player)
                or state.can_reach_region("D06Z01S13[W]", self.player)
            )
        )
    
    def can_beat_hall_boss(self, state: CollectionState) -> bool:
        return (
            self.has_boss_strength(state, "laudes")
            and (
                state.can_reach_region("D08Z01S02[NE]", self.player)
                or state.can_reach_region("D08Z03S02[NW]", self.player)
            )
        )
    
    def can_beat_perpetua(self, state: CollectionState) -> bool:
        return self.has_boss_strength(state, "perpetua")
    
    def can_beat_legionary(self, state: CollectionState) -> bool:
        return self.has_boss_strength(state, "legionary")

    def get_player_strength(self, state: CollectionState) -> float:
        life: int = state.count("Life Upgrade", self.player)
        sword: int = state.count("Mea Culpa Upgrade", self.player)
        fervour: int = state.count("Fervour Upgrade", self.player)
        flasks: int = self.flasks(state)
        quicksilver: int = self.quicksilver(state)

        player_strength: float = (
            min(6, life) * 0.25 / 6
            + min(7, sword) * 0.25 / 7
            + min(6, fervour) * 0.20 / 6
            + min(8, flasks) * 0.15 / 8
            + min(5, quicksilver) * 0.15 / 5
        )
        return player_strength

    def has_boss_strength(self, state: CollectionState, boss: str, player_strength: float | None = None) -> bool:
        if player_strength is None:
            return self.get_player_strength(state) >= self.boss_strengths[boss]
        else:
            return player_strength >= self.boss_strengths[boss]

    def guilt_rooms(self, state: CollectionState, count: int) -> bool:
        doors = (
            "D01Z04S01[NE]",
            "D02Z02S11[W]",
            "D03Z03S02[NE]",
            "D04Z02S02[SE]",
            "D05Z01S05[NE]",
            "D09Z01S05[W]",
            "D17Z01S04[W]",
        )

        total: int = 0
        for door in doors:
            total += state.can_reach_region(door, self.player)
            if total >= count:
                return True
        return False
    
    def sword_rooms(self, state: CollectionState, count: int) -> bool:
        doors = (
            ("D01Z02S07[E]", "D01Z02S02[SW]"),
            ("D20Z01S04[E]", "D01Z05S23[W]"),
            ("D02Z03S02[NE]",),
            ("D04Z02S21[NE]",),
            ("D05Z01S21[NW]",),
            ("D06Z01S15[NE]",),
            ("D17Z01S07[SW]",)
        )

        total: int = 0
        for subdoors in doors:
            for door in subdoors:
                if state.can_reach_region(door, self.player):
                    total += 1
                    break
            if total >= count:
                return True

        return False

    def redento_rooms(self, state: CollectionState, count: int) -> bool:
        if not (
                state.can_reach_region("D03Z01S04[E]", self.player)
                or state.can_reach_region("D03Z02S10[N]", self.player)
        ):
            # Realistically, count should never be zero or negative.
            return count < 1

        if count == 1:
            return True

        if not (
                state.can_reach_region("D17Z01S05[S]", self.player)
                or state.can_reach_region("D17BZ02S01[FrontR]", self.player)
        ):
            return False

        if count == 2:
            return True

        if not (state.can_reach_region("D01Z03S04[E]", self.player)
                or state.can_reach_region("D08Z01S01[W]", self.player)):
            return False

        if count == 3:
            return True

        if not (state.can_reach_region("D04Z01S03[E]", self.player)
                or state.can_reach_region("D04Z02S01[W]", self.player)
                or state.can_reach_region("D06Z01S18[-Cherubs]", self.player)):
            return False

        if count == 4:
            return True

        if not (
                self.knots(state) >= 1
                and self.limestones(state, 3)
                and (state.can_reach_region("D04Z02S08[E]", self.player)
                     or state.can_reach_region("D04BZ02S01[Redento]", self.player))
        ):
            return False

        return count == 5

    def all_miriam_rooms(self, state: CollectionState) -> bool:
        doors = (
            "D02Z03S07[NWW]",
            "D03Z03S07[NW]",
            "D04Z04S01[E]",
            "D05Z01S06[W]",
            "D06Z01S17[E]"
        )

        for door in doors:
            if not state.can_reach_region(door, self.player):
                return False
        return True
    
    def amanecida_rooms(self, state: CollectionState) -> int:
        player_strength = self.get_player_strength(state)
        total: int = 0
        if self.can_beat_graveyard_boss(state, player_strength):
            total += 1
        if self.can_beat_jondo_boss(state, player_strength):
            total += 1
        if self.can_beat_patio_boss(state, player_strength):
            total += 1
        if self.can_beat_wall_boss(state, player_strength):
            total += 1

        return total
    
    def chalice_rooms(self, state: CollectionState) -> int:
        doors = (
            ("D03Z01S02[E]", "D01Z05S02[W]", "D20Z01S03[N]"),
            ("D05Z01S11[SE]", "D05Z02S02[NW]"),
            ("D09Z01S09[E]", "D09Z01S10[W]", "D09Z01S08[SE]", "D09Z01S02[SW]")
        )

        total: int = 0
        for subdoors in doors:
            for door in subdoors:
                if state.can_reach_region(door, self.player):
                    total += 1
                    break

        return total
