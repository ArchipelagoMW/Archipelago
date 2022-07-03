from BaseClasses import MultiWorld
from ..AutoWorld import LogicMixin
from .Options import is_option_enabled

class TimespinnerLogic(LogicMixin):
    def _timespinner_has_timestop(self, world: MultiWorld, player: int) -> bool:
        return self.has_any({'Timespinner Wheel', 'Succubus Hairpin', 'Lightwall', 'Celestial Sash'}, player)

    def _timespinner_has_doublejump(self, world: MultiWorld, player: int) -> bool:
        return self.has_any({'Succubus Hairpin', 'Lightwall', 'Celestial Sash'}, player)

    def _timespinner_has_forwarddash_doublejump(self, world: MultiWorld, player: int) -> bool:
        return self._timespinner_has_upwarddash(world, player) or (self.has('Talaria Attachment', player) and self._timespinner_has_doublejump(world, player))

    def _timespinner_has_doublejump_of_npc(self, world: MultiWorld, player: int) -> bool:
        return self._timespinner_has_upwarddash(world, player) or (self.has('Timespinner Wheel', player) and self._timespinner_has_doublejump(world, player))

    def _timespinner_has_fastjump_on_npc(self, world: MultiWorld, player: int) -> bool:
        return self.has_all({'Timespinner Wheel', 'Talaria Attachment'}, player)

    def _timespinner_has_multiple_small_jumps_of_npc(self, world: MultiWorld, player: int) -> bool:
        return self.has('Timespinner Wheel', player) or self._timespinner_has_upwarddash(world, player)

    def _timespinner_has_upwarddash(self, world: MultiWorld, player: int) -> bool:
        return self.has_any({'Lightwall', 'Celestial Sash'}, player)
    
    def _timespinner_has_fire(self, world: MultiWorld, player: int) -> bool:
        return self.has_any({'Fire Orb', 'Infernal Flames', 'Pyro Ring', 'Djinn Inferno'}, player)

    def _timespinner_has_pink(self, world: MultiWorld, player: int) -> bool:
        return self.has_any({'Plasma Orb', 'Plasma Geyser', 'Royal Ring'}, player)

    def _timespinner_has_keycard_A(self, world: MultiWorld, player: int) -> bool:
        return self.has('Security Keycard A', player)

    def _timespinner_has_keycard_B(self, world: MultiWorld, player: int) -> bool:
        if is_option_enabled(world, player, "SpecificKeycards"):
            return self.has('Security Keycard B', player)
        else:
            return self.has_any({'Security Keycard A', 'Security Keycard B'}, player)

    def _timespinner_has_keycard_C(self, world: MultiWorld, player: int) -> bool:
        if is_option_enabled(world, player, "SpecificKeycards"):
            return self.has('Security Keycard C', player)
        else:
            return self.has_any({'Security Keycard A', 'Security Keycard B', 'Security Keycard C'}, player)

    def _timespinner_has_keycard_D(self, world: MultiWorld, player: int) -> bool:
        if is_option_enabled(world, player, "SpecificKeycards"):
            return self.has('Security Keycard D', player)
        else:
            return self.has_any({'Security Keycard A', 'Security Keycard B', 'Security Keycard C', 'Security Keycard D'}, player)

    def _timespinner_can_break_walls(self, world: MultiWorld, player: int) -> bool:
        if is_option_enabled(world, player, "EyeSpy"):
            return self.has('Oculus Ring', player)
        else:
            return True

    def _timespinner_can_kill_all_3_bosses(self, world: MultiWorld, player: int) -> bool:
        return self.has_all({'Killed Maw', 'Killed Twins', 'Killed Aelana'}, player)