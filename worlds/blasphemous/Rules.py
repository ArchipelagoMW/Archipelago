from typing import Dict, List, Tuple, Any, Callable, TYPE_CHECKING
from BaseClasses import CollectionState

if TYPE_CHECKING:
    from . import BlasphemousWorld
else:
    BlasphemousWorld = object


class BlasRules:
    player: int
    world: BlasphemousWorld
    string_rules: Dict[str, Callable[[CollectionState], bool]]

    def __init__(self, world: "BlasphemousWorld") -> None:
        self.player = world.player
        self.world = world
        self.multiworld = world.multiworld
        self.indirect_conditions: List[Tuple[str, str]] = []

        # BrandenEK/Blasphemous.Randomizer/ItemRando/BlasphemousInventory.cs
        self.string_rules = {
            # Visibility flags
            "DoubleJump": lambda state: bool(self.world.options.purified_hand),
            "NormalLogic": lambda state: self.world.options.difficulty >= 1,
            "NormalLogicAndDoubleJump": lambda state: self.world.options.difficulty >= 1 \
                and bool(self.world.options.purified_hand),
            "HardLogic": lambda state: self.world.options.difficulty >= 2,
            "HardLogicAndDoubleJump": lambda state: self.world.options.difficulty >= 2 \
                and bool(self.world.options.purified_hand),
            "EnemySkips": self.enemy_skips_allowed,
            "EnemySkipsAndDoubleJump": lambda state: self.enemy_skips_allowed(state) \
                and bool(self.world.options.purified_hand),

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

            "bones4": lambda state: self.bones(state) >= 4,
            "bones8": lambda state: self.bones(state) >= 8,
            "bones12": lambda state: self.bones(state) >= 12,
            "bones16": lambda state: self.bones(state) >= 16,
            "bones20": lambda state: self.bones(state) >= 20,
            "bones24": lambda state: self.bones(state) >= 24,
            "bones28": lambda state: self.bones(state) >= 28,
            "bones30": lambda state: self.bones(state) >= 30,
            "bones32": lambda state: self.bones(state) >= 32,
            "bones36": lambda state: self.bones(state) >= 36,
            "bones40": lambda state: self.bones(state) >= 40,
            "bones44": lambda state: self.bones(state) >= 44,

            "tears0": lambda state: True,

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
            "rangedAttack": lambda state: self.ranged(state) > 0,

            # Main quest
            "holyWounds3": lambda state: self.holy_wounds(state) >= 3,
            "masks1": lambda state: self.masks(state) >= 1,
            "masks2": lambda state: self.masks(state) >= 2,
            "masks3": lambda state: self.masks(state) >= 3,
            "guiltBead": self.guilt_bead,

            # LOTL quest
            "cloth": self.cloth,
            "hand": self.hand,
            "hatchedEgg": self.hatched_egg,

            # Tirso quest
            "herbs1": lambda state: self.herbs(state) >= 1,
            "herbs2": lambda state: self.herbs(state) >= 2,
            "herbs3": lambda state: self.herbs(state) >= 3,
            "herbs4": lambda state: self.herbs(state) >= 4,
            "herbs5": lambda state: self.herbs(state) >= 5,
            "herbs6": lambda state: self.herbs(state) >= 6,

            # Tentudia quest
            "tentudiaRemains1": lambda state: self.tentudia_remains(state) >= 1,
            "tentudiaRemains2": lambda state: self.tentudia_remains(state) >= 2,
            "tentudiaRemains3": lambda state: self.tentudia_remains(state) >= 3,

            # Gemino quest
            "emptyThimble": self.empty_thimble,
            "fullThimble": self.full_thimble,
            "driedFlowers": self.dried_flowers,

            # Altasgracias quest
            "ceremonyItems3": lambda state: self.ceremony_items(state) >= 3,
            "egg": self.egg,

            # Redento quest
            # skip "limestones", not actually used
            # skip "knots", not actually used

            # Cleofas quest
            "marksOfRefuge3": lambda state: self.marks_of_refuge(state) >= 3,
            "cord": self.cord,

            # Crisanta quest
            "scapular": self.scapular,
            "trueHeart": self.true_heart,
            "traitorEyes2": lambda state: self.traitor_eyes(state) >= 2,

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
            "canEnemyBounce": self.can_enemy_bounce,
            "canEnemyUpslash": self.can_enemy_upslash,

            # Reaching rooms
            "guiltRooms1": lambda state: self.guilt_rooms(state) >= 1,
            "guiltRooms2": lambda state: self.guilt_rooms(state) >= 2,
            "guiltRooms3": lambda state: self.guilt_rooms(state) >= 3,
            "guiltRooms4": lambda state: self.guilt_rooms(state) >= 4,
            "guiltRooms5": lambda state: self.guilt_rooms(state) >= 5,
            "guiltRooms6": lambda state: self.guilt_rooms(state) >= 6,
            "guiltRooms7": lambda state: self.guilt_rooms(state) >= 7,

            "swordRooms1": lambda state: self.sword_rooms(state) >= 1,
            "swordRooms2": lambda state: self.sword_rooms(state) >= 2,
            "swordRooms3": lambda state: self.sword_rooms(state) >= 3,
            "swordRooms4": lambda state: self.sword_rooms(state) >= 4,
            "swordRooms5": lambda state: self.sword_rooms(state) >= 5,
            "swordRooms6": lambda state: self.sword_rooms(state) >= 6,
            "swordRooms7": lambda state: self.sword_rooms(state) >= 7,

            "redentoRooms2": lambda state: self.redento_rooms(state) >= 2,
            "redentoRooms3": lambda state: self.redento_rooms(state) >= 3,
            "redentoRooms4": lambda state: self.redento_rooms(state) >= 4,
            "redentoRooms5": lambda state: self.redento_rooms(state) >= 5,

            "miriamRooms5": lambda state: self.miriam_rooms(state) >= 5,

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
            "upwarpSkipsAllowed": self.upwarp_skips_allowed,
            "mourningSkipAllowed": self.mourning_skip_allowed,
            "enemySkipsAllowed": self.enemy_skips_allowed,
            "obscureSkipsAllowed": self.obscure_skips_allowed,
            "preciseSkipsAllowed": self.precise_skips_allowed,

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
        for clause in obj["logic"]:
            reqs = []
            for req in clause["item_requirements"]:
                if self.req_is_region(req):
                    if obj_is_region:
                        # add to indirect conditions if object and requirement are doors
                        self.indirect_conditions.append((req, f"{name} -> {obj['target']}"))
                    reqs.append(lambda state, req=req: state.can_reach_region(req, self.player))
                else:
                    if obj_is_region and req in self.indirect_regions:
                        # add to indirect conditions if object is door and requirement has list of regions
                        for region in self.indirect_regions[req]:
                            self.indirect_conditions.append((region, f"{name} -> {obj['target']}"))
                    reqs.append(self.string_rules[req])
            if len(reqs) == 1:
                clauses.append(reqs[0])
            else:
                clauses.append(lambda state, reqs=reqs: all(req(state) for req in reqs))
        if not clauses:
            return lambda state: True
        elif len(clauses) == 1:
            return clauses[0]
        else:
            return lambda state: any(clause(state) for clause in clauses)

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
    
    def bones(self, state: CollectionState) -> int:
        return state.count_group_unique("bones", self.player)
    
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
        doors = {
            "D01Z05S05[SW]",
            "D02Z02S04[W]",
            "D03Z02S08[W]",
            "D03Z03S04[SW]",
            "D04Z02S13[W]",
            "D05Z01S08[NW]",
            "D20Z01S07[NE]"
        }

        return state.count("Empty Bile Vessel", self.player) \
            if sum(state.can_reach_region(door, self.player) for door in doors) >= 1 else 0
    
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
            or state.has_any({
                "Campanillero to the Sons of the Aurora",
                "Mirabras of the Return to Port",
                "Romance to the Crimson Mist",
                "Saeta Dolorosa",
                "Seguiriya to your Eyes like Stars",
                "Verdiales of the Forsaken Hamlet",
                "Zambra to the Resplendent Crown"
            }, self.player)
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

    def ranged(self, state: CollectionState) -> int:
        return state.count("Ranged Skill", self.player)
    
    def dive(self, state: CollectionState) -> int:
        return state.count("Dive Skill", self.player)
    
    def lunge(self, state: CollectionState) -> int:
        return state.count("Lunge Skill", self.player)
    
    def charge_beam(self, state: CollectionState) -> bool:
        return self.charged(state) >= 3
    
    # Main quest
    def holy_wounds(self, state: CollectionState) -> int:
        return state.count_group_unique("wounds", self.player)
    
    def masks(self, state: CollectionState) -> int:
        return state.count_group_unique("masks", self.player)
    
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
    def herbs(self, state: CollectionState) -> int:
        return state.count_group_unique("tirso", self.player)
    
    # Tentudia quest
    def tentudia_remains(self, state: CollectionState) -> int:
        return state.count_group_unique("tentudia", self.player)
    
    # Gemino quest
    def empty_thimble(self, state: CollectionState) -> bool:
        return state.has("Empty Golden Thimble", self.player)
    
    def full_thimble(self, state: CollectionState) -> bool:
        return state.has("Golden Thimble Filled with Burning Oil", self.player)
    
    def dried_flowers(self, state: CollectionState) -> bool:
        return state.has("Dried Flowers bathed in Tears", self.player)
    
    # Altasgracias quest
    def ceremony_items(self, state: CollectionState) -> int:
        return state.count_group_unique("egg", self.player)
    
    def egg(self, state: CollectionState) -> bool:
        return state.has("Egg of Deformity", self.player)
    
    # Redento quest
    def limestones(self, state: CollectionState) -> int:
        return state.count_group_unique("toe", self.player)
    
    def knots(self, state: CollectionState) -> int:
        return state.count("Knot of Rosary Rope", self.player) if state.can_reach_region("D17Z01S07[NW]", self.player)\
            else 0
    
    # Cleofas quest
    def marks_of_refuge(self, state: CollectionState) -> int:
        return state.count_group_unique("marks", self.player)
    
    def cord(self, state: CollectionState) -> bool:
        return state.has("Cord of the True Burying", self.player)
    
    # Crisanta quest
    def scapular(self, state: CollectionState) -> bool:
        return state.has("Incomplete Scapular", self.player)
    
    def true_heart(self, state: CollectionState) -> bool:
        return state.has("Apodictic Heart of Mea Culpa", self.player)
    
    def traitor_eyes(self, state: CollectionState) -> int:
        return state.count_group_unique("eye", self.player)
    
    # Jibrael quest
    def bell(self, state: CollectionState) -> bool:
        return state.has("Petrified Bell", self.player)
    
    def verses(self, state: CollectionState) -> int:
        return state.count("Verses Spun from Gold", self.player)
    
    # Movement tech
    def can_air_stall(self, state: CollectionState) -> bool:
        return (
            self.ranged(state) > 0
            and self.world.options.difficulty >= 1
        )
    
    def can_dawn_jump(self, state: CollectionState) -> bool:
        return (
            self.dawn_heart(state)
            and self.dash(state)
            and self.world.options.difficulty >= 1
        )
    
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
    
    def can_dive_laser(self, state: CollectionState) -> bool:
        return (
            self.dive(state) >= 3
            and self.world.options.difficulty >= 2
        )
    
    # Root tech
    def can_walk_on_root(self, state: CollectionState) -> bool:
        return self.root(state)
    
    def can_climb_on_root(self, state: CollectionState) -> bool:
        return (
            self.root(state)
            and self.wall_climb(state)
        )
    
    # Lung tech
    def can_survive_poison_1(self, state: CollectionState) -> bool:
        return (
            self.lung(state)
            or self.world.options.difficulty >= 1
            and self.tiento(state)
            or self.world.options.difficulty >= 2
        )
    
    def can_survive_poison_2(self, state: CollectionState) -> bool:
        return (
            self.lung(state)
            or self.world.options.difficulty >= 1
            and self.tiento(state)
        )
    
    def can_survive_poison_3(self, state: CollectionState) -> bool:
        return (
            self.lung(state)
            or self.world.options.difficulty >= 2
            and self.tiento(state)
            and self.total_fervour(state) >= 120
        )
    
    # Enemy tech
    def can_enemy_bounce(self, state: CollectionState) -> bool:
        return self.enemy_skips_allowed(state)
    
    def can_enemy_upslash(self, state: CollectionState) -> bool:
        return (
            self.combo(state) >= 2
            and self.enemy_skips_allowed(state)
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
                or self.can_enemy_bounce(state)
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
    
    # Special skips
    def upwarp_skips_allowed(self, state: CollectionState) -> bool:
        return self.world.options.difficulty >= 2
    
    def mourning_skip_allowed(self, state: CollectionState) -> bool:
        return self.world.options.difficulty >= 2
    
    def enemy_skips_allowed(self, state: CollectionState) -> bool:
        return (
            self.world.options.difficulty >= 2
            and not self.world.options.enemy_randomizer
        )
    
    def obscure_skips_allowed(self, state: CollectionState) -> bool:
        return self.world.options.difficulty >= 2
    
    def precise_skips_allowed(self, state: CollectionState) -> bool:
        return self.world.options.difficulty >= 2
    
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
    
    def can_beat_graveyard_boss(self, state: CollectionState) -> bool:
        return (
            self.has_boss_strength(state, "amanecida")
            and self.wall_climb(state)
            and state.can_reach_region("D01Z06S01[Santos]", self.player)
            and state.can_reach_region("D02Z03S18[NW]", self.player)
            and state.can_reach_region("D02Z02S03[NE]", self.player)
        )
    
    def can_beat_jondo_boss(self, state: CollectionState) -> bool:
        return (
            self.has_boss_strength(state, "amanecida")
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
    
    def can_beat_patio_boss(self, state: CollectionState) -> bool:
        return (
            self.has_boss_strength(state, "amanecida")
            and state.can_reach_region("D01Z06S01[Santos]", self.player)
            and state.can_reach_region("D06Z01S02[W]", self.player)
            and (
                state.can_reach_region("D04Z01S03[E]", self.player)
                or state.can_reach_region("D04Z01S01[W]", self.player)
                or state.can_reach_region("D06Z01S18[-Cherubs]", self.player)
            )
        )
    
    def can_beat_wall_boss(self, state: CollectionState) -> bool:
        return (
            self.has_boss_strength(state, "amanecida")
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


    def has_boss_strength(self, state: CollectionState, boss: str) -> bool:
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

        bosses: Dict[str, float] = {
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
        boss_strength: float = bosses[boss]
        return player_strength >= (boss_strength - 0.10 if self.world.options.difficulty >= 2 else 
                                   (boss_strength if self.world.options.difficulty >= 1 else boss_strength + 0.10))

    def guilt_rooms(self, state: CollectionState) -> int:
        doors = [
            "D01Z04S01[NE]",
            "D02Z02S11[W]",
            "D03Z03S02[NE]",
            "D04Z02S02[SE]",
            "D05Z01S05[NE]",
            "D09Z01S05[W]",
            "D17Z01S04[W]",
        ]

        return sum(state.can_reach_region(door, self.player) for door in doors)
    
    def sword_rooms(self, state: CollectionState) -> int:
        doors = [
            ["D01Z02S07[E]", "D01Z02S02[SW]"],
            ["D20Z01S04[E]", "D01Z05S23[W]"],
            ["D02Z03S02[NE]"],
            ["D04Z02S21[NE]"],
            ["D05Z01S21[NW]"],
            ["D06Z01S15[NE]"],
            ["D17Z01S07[SW]"]
        ]

        total: int = 0
        for subdoors in doors:
            for door in subdoors:
                if state.can_reach_region(door, self.player):
                    total += 1
                    break

        return total

    def redento_rooms(self, state: CollectionState) -> int:
        if (
            state.can_reach_region("D03Z01S04[E]", self.player)
            or state.can_reach_region("D03Z02S10[N]", self.player)
        ):
            if (
                state.can_reach_region("D17Z01S05[S]", self.player)
                or state.can_reach_region("D17BZ02S01[FrontR]", self.player)
            ):
                if (
                    state.can_reach_region("D01Z03S04[E]", self.player)
                    or state.can_reach_region("D08Z01S01[W]", self.player)
                ):
                    if (
                        state.can_reach_region("D04Z01S03[E]", self.player)
                        or state.can_reach_region("D04Z02S01[W]", self.player)
                        or state.can_reach_region("D06Z01S18[-Cherubs]", self.player)
                    ):
                        if (
                            self.knots(state) >= 1
                            and self.limestones(state) >= 3
                            and (
                                state.can_reach_region("D04Z02S08[E]", self.player)
                                or state.can_reach_region("D04BZ02S01[Redento]", self.player)
                            )
                        ):
                            return 5
                        return 4
                    return 3
                return 2
            return 1
        return 0
    
    def miriam_rooms(self, state: CollectionState) -> int:
        doors = [
            "D02Z03S07[NWW]",
            "D03Z03S07[NW]",
            "D04Z04S01[E]",
            "D05Z01S06[W]",
            "D06Z01S17[E]"
        ]

        return sum(state.can_reach_region(door, self.player) for door in doors)
    
    def amanecida_rooms(self, state: CollectionState) -> int:
        total: int = 0
        if self.can_beat_graveyard_boss(state):
            total += 1
        if self.can_beat_jondo_boss(state):
            total += 1
        if self.can_beat_patio_boss(state):
            total += 1
        if self.can_beat_wall_boss(state):
            total += 1

        return total
    
    def chalice_rooms(self, state: CollectionState) -> int:
        doors = [
            ["D03Z01S02[E]", "D01Z05S02[W]", "D20Z01S03[N]"],
            ["D05Z01S11[SE]", "D05Z02S02[NW]"],
            ["D09Z01S09[E]", "D09Z01S10[W]", "D09Z01S08[SE]", "D09Z01S02[SW]"]
        ]

        total: int = 0
        for subdoors in doors:
            for door in subdoors:
                if state.can_reach_region(door, self.player):
                    total += 1
                    break

        return total
