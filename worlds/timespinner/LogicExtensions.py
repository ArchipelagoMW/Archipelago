from typing import Union, Optional
from BaseClasses import CollectionState
from .Options import TimespinnerOptions
from .PreCalculatedWeights import PreCalculatedWeights


class TimespinnerLogic:
    player: int

    flag_unchained_keys: bool
    flag_eye_spy: bool
    flag_specific_keycards: bool
    flag_prism_break: bool
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
        self.flag_prism_break = bool(options and options.prism_break)

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

    def has_timestop(self, state: CollectionState) -> bool:
        return state.has_any({'Timespinner Wheel', 'Succubus Hairpin', 'Lightwall', 'Celestial Sash'}, self.player)

    def has_doublejump(self, state: CollectionState) -> bool:
        return state.has_any({'Succubus Hairpin', 'Lightwall', 'Celestial Sash'}, self.player)

    def has_forwarddash_doublejump(self, state: CollectionState) -> bool:
        return self.has_upwarddash(state) \
            or (state.has('Talaria Attachment', self.player) and self.has_doublejump(state))

    def has_doublejump_of_npc(self, state: CollectionState) -> bool:
        return self.has_upwarddash(state) \
            or (state.has('Timespinner Wheel', self.player) and self.has_doublejump(state))

    def has_fastjump_on_npc(self, state: CollectionState) -> bool:
        return state.has_all({'Timespinner Wheel', 'Talaria Attachment'}, self.player)

    def has_multiple_small_jumps_of_npc(self, state: CollectionState) -> bool:
        return state.has('Timespinner Wheel', self.player) or self.has_upwarddash(state)

    def has_upwarddash(self, state: CollectionState) -> bool:
        return state.has_any({'Lightwall', 'Celestial Sash'}, self.player)
    
    def has_fire(self, state: CollectionState) -> bool:
        return state.has_any({'Fire Orb', 'Infernal Flames', 'Pyro Ring', 'Djinn Inferno'}, self.player)

    def has_pink(self, state: CollectionState) -> bool:
        return state.has_any({'Plasma Orb', 'Plasma Geyser', 'Royal Ring'}, self.player)

    def has_keycard_A(self, state: CollectionState) -> bool:
        return state.has('Security Keycard A', self.player)

    def has_keycard_B(self, state: CollectionState) -> bool:
        if self.flag_specific_keycards:
            return state.has('Security Keycard B', self.player)
        else:
            return state.has_any({'Security Keycard A', 'Security Keycard B'}, self.player)

    def has_keycard_C(self, state: CollectionState) -> bool:
        if self.flag_specific_keycards:
            return state.has('Security Keycard C', self.player)
        else:
            return state.has_any({'Security Keycard A', 'Security Keycard B', 'Security Keycard C'}, self.player)

    def has_keycard_D(self, state: CollectionState) -> bool:
        if self.flag_specific_keycards:
            return state.has('Security Keycard D', self.player)
        else:
            return state.has_any({'Security Keycard A', 'Security Keycard B', 'Security Keycard C', 'Security Keycard D'}, self.player)

    def can_break_walls(self, state: CollectionState) -> bool:
        if self.flag_eye_spy:
            return state.has('Oculus Ring', self.player)
        else:
            return True

    def can_kill_all_3_bosses(self, state: CollectionState) -> bool:
        if self.flag_prism_break:
            return state.has_all({'Laser Access M', 'Laser Access I', 'Laser Access A'}, self.player)
        return state.has_all({'Killed Maw', 'Killed Twins', 'Killed Aelana'}, self.player)

    def has_teleport(self, state: CollectionState) -> bool:
        return self.flag_unchained_keys or state.has('Twin Pyramid Key', self.player)

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
            raise Exception("Invallid Era: {}".format(era))
