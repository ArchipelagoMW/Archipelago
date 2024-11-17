from typing import Union, Optional, Callable
from BaseClasses import CollectionState, Req
from BaseRules import AllReq, AnyReq, req_to_rule, complex_reqs_to_rule, RULE_ALWAYS_FALSE, RULE_ALWAYS_TRUE
from .Options import TimespinnerOptions
from .PreCalculatedWeights import PreCalculatedWeights


class TimespinnerLogic:
    player: int

    flag_unchained_keys: bool
    flag_eye_spy: bool
    flag_specific_keycards: bool
    pyramid_keys_unlock: Optional[str]
    present_keys_unlock: Optional[str]
    past_keys_unlock: Optional[str]
    time_keys_unlock: Optional[str]

    def __init__(self, player: int, options: Optional[TimespinnerOptions], 
                 precalculated_weights: Optional[PreCalculatedWeights]):
        self.player = player

        self.flag_specific_keycards = bool(options and options.specific_keycards)
        self.flag_eye_spy = bool(options and options.eye_spy)
        self.flag_unchained_keys = bool(options and options.unchained_keys)

        if precalculated_weights:
            if self.flag_unchained_keys:
                self.pyramid_keys_unlock = None
                self.present_keys_unlock = precalculated_weights.present_key_unlock
                self.past_keys_unlock = precalculated_weights.past_key_unlock
                self.time_keys_unlock = precalculated_weights.time_key_unlock
            else:
                self.pyramid_keys_unlock = precalculated_weights.pyramid_keys_unlock
                self.present_keys_unlock = None
                self.past_keys_unlock = None
                self.time_keys_unlock = None

        self.timestop_req = AnyReq([Req("Timespinner Wheel"), Req("Succubus Hairpin"),
                                    Req("Lightwall"), Req("Celestial Sash")])
        self.doublejump_req = AnyReq([Req("Succubus Hairpin"), Req("Lightwall"), Req("Celestial Sash")])
        self.upwarddash_req = AnyReq([Req("Lightwall"), Req("Celestial Sash")])
        self.fastjump_on_npc_req = AllReq([Req("Timespinner Wheel"), Req("Talaria Attachment")])
        self.multiple_small_jumps_of_npc_req = AnyReq([Req("Timespinner Wheel"), self.upwarddash_req])
        self.forwarddash_doublejump_req = AnyReq([self.upwarddash_req,
                                                  AllReq([Req("Talaria Attachment"), self.doublejump_req])])
        self.doublejump_of_npc_req = AnyReq([self.upwarddash_req,
                                             AllReq([Req("Timespinner Wheel"), self.doublejump_req])])
        
        self.fire_req = AnyReq([Req("Fire Orb"), Req("Infernal Flames"), Req("Pyro Ring"), Req("Djinn Inferno")])
        self.pink_req = AnyReq([Req("Plasma Orb"), Req("Plasma Geyser"), Req("Royal Ring")])
        
        self.keycard_A_req = Req("Security Keycard A")
        if self.flag_specific_keycards:
            self.keycard_B_req = Req("Security Keycard B")
            self.keycard_C_req = Req("Security Keycard C")
            self.keycard_D_req = Req("Security Keycard D")
        else:
            self.keycard_B_req = AnyReq([Req("Security Keycard B"), self.keycard_A_req])
            self.keycard_C_req = AnyReq([Req("Security Keycard C"), self.keycard_B_req])
            self.keycard_D_req = AnyReq([Req("Security Keycard D"), self.keycard_C_req])

        if self.flag_eye_spy:
            self.break_walls_req = Req("Oculus Ring")
        else:
            self.break_walls_req = None

        self.all_3_bosses_req = AllReq([Req("Killed Maw"), Req("Killed Twins"), Req("Killed Aelana")])
        if self.flag_unchained_keys:
            self.teleport_req = None
        else:
            self.teleport_req = Req("Twin Pyramid Key")

        # Other useful reqs
        self.wheel_and_spindle_req = AllReq([Req("Timespinner Wheel"), Req("Timespinner Spindle")])
        self.all_timespinner_pieces_req = AllReq([self.wheel_and_spindle_req, Req("Timespinner Gear 1"),
                                           Req("Timespinner Gear 2"), Req("Timespinner Gear 3")])

        # Build rules
        self.has_timestop = complex_reqs_to_rule(player, self.timestop_req)
        self.has_doublejump = complex_reqs_to_rule(player, self.doublejump_req)
        self.has_forwarddash_doublejump = complex_reqs_to_rule(player, self.forwarddash_doublejump_req)
        self.has_doublejump_of_npc = complex_reqs_to_rule(player, self.doublejump_of_npc_req)
        self.has_fastjump_on_npc = complex_reqs_to_rule(player, self.fastjump_on_npc_req)
        self.has_multiple_small_jumps_of_npc = complex_reqs_to_rule(player, self.multiple_small_jumps_of_npc_req)
        self.has_upwarddash = complex_reqs_to_rule(player, self.upwarddash_req)
        self.has_fire = complex_reqs_to_rule(player, self.fire_req)
        self.has_pink = complex_reqs_to_rule(player, self.pink_req)
        self.has_keycard_A = complex_reqs_to_rule(player, self.keycard_A_req)
        self.has_keycard_B = complex_reqs_to_rule(player, self.keycard_B_req)
        self.has_keycard_C = complex_reqs_to_rule(player, self.keycard_C_req)
        self.has_keycard_D = complex_reqs_to_rule(player, self.keycard_D_req)
        self.can_break_walls = complex_reqs_to_rule(player, self.break_walls_req)
        self.can_kill_all_3_bosses = complex_reqs_to_rule(player, self.all_3_bosses_req)
        self.has_teleport = complex_reqs_to_rule(player, self.teleport_req)

    def make_rule_can_teleport_to(self, era: str, gate: str) -> Callable[[CollectionState], bool]:
        if not self.flag_unchained_keys:
            return RULE_ALWAYS_TRUE if self.pyramid_keys_unlock == gate else RULE_ALWAYS_FALSE

        if era == "Present":
            if self.present_keys_unlock == gate:
                return req_to_rule(self.player, Req("Modern Warp Beacon"))
            return RULE_ALWAYS_FALSE
        elif era == "Past":
            if self.past_keys_unlock == gate:
                return req_to_rule(self.player, Req("Timeworn Warp Beacon"))
            return RULE_ALWAYS_FALSE
        elif era == "Time":
            if self.time_keys_unlock == gate:
                return req_to_rule(self.player, Req("Mysterious Warp Beacon"))
            return RULE_ALWAYS_FALSE
        else:
            raise Exception("Invalid Era: {}".format(era))

    def can_teleport_to(self, state: CollectionState, era: str, gate: str) -> bool:
        if not self.flag_unchained_keys:
            return self.pyramid_keys_unlock == gate

        if era == "Present":
            return self.present_keys_unlock == gate and state.has("Modern Warp Beacon", self.player)
        elif era == "Past":
            return self.past_keys_unlock == gate and state.has("Timeworn Warp Beacon", self.player)
        elif era == "Time":
            return self.time_keys_unlock == gate and state.has("Mysterious Warp Beacon", self.player)
        else:
            raise Exception("Invalid Era: {}".format(era))
