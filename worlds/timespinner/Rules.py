from worlds.timespinner.Options import is_option_enabled
from BaseClasses import MultiWorld
from ..AutoWorld import LogicMixin
from ..generic.Rules import set_rule
from .Options import is_option_enabled

class TimespinnerLogic(LogicMixin):
    def _timespinner_has_timestop(self, world: MultiWorld, player: int) -> bool:
        return self.has_any(['Timespinner Wheel', 'Succubus Hairpin', 'Lightwall', 'Celestial Sash'], player)

    def _timespinner_has_doublejump(self, world: MultiWorld, player: int) -> bool:
        return self.has_any(['Succubus Hairpin', 'Lightwall', 'Celestial Sash'], player)

    def _timespinner_has_forwarddash_doublejump(self, world: MultiWorld, player: int) -> bool:
        return self.has('Celestial Sash', player) or (self._timespinner_has_doublejump(world, player) and self.has('Talaria Attachment', player))

    def _timespinner_has_doublejump_of_npc(self, world: MultiWorld, player: int) -> bool:
        return self.has('Celestial Sash', player) or (self._timespinner_has_doublejump(world, player) and self.has('Timespinner Wheel', player))

    def _timespinner_has_upwarddash(self, world: MultiWorld, player: int) -> bool:
        return self.has_any(['Lightwall', 'Celestial Sash'], player)
    
    def _timespinner_has_fire(self, world: MultiWorld, player: int) -> bool:
        return self.has_any(['Fire Orb', 'Infernal Flames', 'Pyro Ring', 'Djinn Inferno'], player)

    def _timespinner_has_keycard_A(self, world: MultiWorld, player: int) -> bool:
        return self.has('Security Keycard A', player)

    def _timespinner_has_keycard_B(self, world: MultiWorld, player: int) -> bool:
        if is_option_enabled(world, player, "SpecificKeycards"):
            return self.has('Security Keycard B', player)
        else:
            return self.has_any(['Security Keycard A', 'Security Keycard B'], player)

    def _timespinner_has_keycard_C(self, world: MultiWorld, player: int) -> bool:
        if is_option_enabled(world, player, "SpecificKeycards"):
            return self.has('Security Keycard C', player)
        else:
            return self.has_any(['Security Keycard A', 'Security Keycard B', 'Security Keycard C'], player)

    def _timespinner_has_keycard_D(self, world: MultiWorld, player: int) -> bool:
        if is_option_enabled(world, player, "SpecificKeycards"):
            return self.has('Security Keycard D', player)
        else:
            return self.has_any(['Security Keycard A', 'Security Keycard B', 'Security Keycard C', 'Security Keycard D'], player)

    def _timespinner_can_kill_all_3_bosses(self, world: MultiWorld, player: int) -> bool:
        #return self.has_all(['Kill Maw', 'Kill Twins', 'Kill Aelana']) TODO convert to events
        hasAccessToMaw = self.can_reach('Caves of Banishment (Maw)', 'Region', player) and self.has('Gas Mask', player)
        hasAccessToTwins = self.can_reach('Caste Keep', 'Region', player) and self._timespinner_has_timestop(world, player)
        hasAccessToAelana = self.can_reach('Royal towers (upper)', 'Region', player)

        return hasAccessToMaw and hasAccessToTwins and hasAccessToAelana

    #def _timespinner_is_option_enabled(self, world: MultiWorld, player: int, name: str) -> bool:
    #    option = getattr(world, name, None)
    #
    #    if option == None:
    #        return False
    #
    #    return int(option[player].value) > 0


def set_rules(world: MultiWorld, player: int):
    world.completion_condition[player] = lambda state: state.can_reach('Ancient Pyramid (left)', 'Region', player)

    pass
    # Act 1 Card Draws
    #set_rule(world.get_location("Card Draw 1", player), lambda state: True)
    #set_rule(world.get_location("Card Draw 2", player), lambda state: True)
    #set_rule(world.get_location("Card Draw 3", player), lambda state: True)
    #set_rule(world.get_location("Card Draw 4", player), lambda state: state._timespinner_has_relics(player, 1))
    #set_rule(world.get_location("Card Draw 5", player), lambda state: state._timespinner_has_relics(player, 1))

    # Act 1 Relics
    #set_rule(world.get_location("Relic 1", player), lambda state: True)
    #set_rule(world.get_location("Relic 2", player), lambda state: True)
    #set_rule(world.get_location("Relic 3", player), lambda state: True)

    # Act 1 Boss Event
    #set_rule(world.get_location("Act 1 Boss", player), lambda state: True and state._timespinner_has_relics(player, 2))

    # Act 1 Boss Rewards
    #set_rule(world.get_location("Rare Card Draw 1", player), lambda state: state.has("Beat Act 1 Boss", player))
    #set_rule(world.get_location("Boss Relic 1", player), lambda state: state.has("Beat Act 1 Boss", player))

    # Act 2 Card Draws
    #set_rule(world.get_location("Card Draw 6", player), lambda state: state.has("Beat Act 1 Boss", player))
    #set_rule(world.get_location("Card Draw 7", player), lambda state: state.has("Beat Act 1 Boss", player))
    #set_rule(world.get_location("Card Draw 8", player), lambda state: state.has("Beat Act 1 Boss", player) and True and state._timespinner_has_relics(player, 3))
    #set_rule(world.get_location("Card Draw 9", player), lambda state: state.has("Beat Act 1 Boss", player) and True and state._timespinner_has_relics(player, 4))
    #set_rule(world.get_location("Card Draw 10", player), lambda state: state.has("Beat Act 1 Boss", player) and True and state._timespinner_has_relics(player, 4))

    # Act 2 Relics
    #set_rule(world.get_location("Relic 4", player), lambda state: state.has("Beat Act 1 Boss", player) and True and state._timespinner_has_relics(player, 2))
    #set_rule(world.get_location("Relic 5", player), lambda state: state.has("Beat Act 1 Boss", player) and True and state._timespinner_has_relics(player, 2))
    #set_rule(world.get_location("Relic 6", player), lambda state: state.has("Beat Act 1 Boss", player) and True and state._timespinner_has_relics(player, 3))

    # Act 2 Boss Event
    #set_rule(world.get_location("Act 2 Boss", player), lambda state: state.has("Beat Act 1 Boss", player) and True and state._timespinner_has_relics(player, 4) and state.has("Boss Relic", player))

    # Act 2 Boss Rewards
    #set_rule(world.get_location("Rare Card Draw 2", player), lambda state: state.has("Beat Act 2 Boss", player))
    #set_rule(world.get_location("Boss Relic 2", player), lambda state: state.has("Beat Act 2 Boss", player))

    # Act 3 Card Draws
    #set_rule(world.get_location("Card Draw 11", player), lambda state: state.has("Beat Act 2 Boss", player))
    #set_rule(world.get_location("Card Draw 12", player), lambda state: state.has("Beat Act 2 Boss", player))
    #set_rule(world.get_location("Card Draw 13", player), lambda state: state.has("Beat Act 2 Boss", player) and state._timespinner_has_relics(player, 4))
    #set_rule(world.get_location("Card Draw 14", player), lambda state: state.has("Beat Act 2 Boss", player) and state._timespinner_has_relics(player, 4))
    #set_rule(world.get_location("Card Draw 15", player), lambda state: state.has("Beat Act 2 Boss", player) and state._timespinner_has_relics(player, 4))

    # Act 3 Relics
    #set_rule(world.get_location("Relic 7", player), lambda state: state.has("Beat Act 2 Boss", player) and state._timespinner_has_relics(player, 4))
    #set_rule(world.get_location("Relic 8", player), lambda state: state.has("Beat Act 2 Boss", player) and state._timespinner_has_relics(player, 5))
    #set_rule(world.get_location("Relic 9", player), lambda state: state.has("Beat Act 2 Boss", player) and state._timespinner_has_relics(player, 5))
    #set_rule(world.get_location("Relic 10", player), lambda state: state.has("Beat Act 2 Boss", player) and state._timespinner_has_relics(player, 5))

    # Act 3 Boss Event
    #set_rule(world.get_location("Act 3 Boss", player), lambda state: state.has("Beat Act 2 Boss", player) and state._timespinner_has_relics(player, 7) and state.has("Boss Relic", player, 2))

    # Act 3 Boss Rewards
    #set_rule(world.get_location("Rare Card Draw 3", player), lambda state: state.has("Beat Act 3 Boss", player))
    #set_rule(world.get_location("Boss Relic 3", player), lambda state: state.has("Beat Act 3 Boss", player))

    #set_rule(world.get_location("Heart Room", player), lambda state: state.has("Beat Act 3 Boss", player))


present_teleportation_gates = {
    "GateKittyBoss",
    "GateLeftLibrary",
    "GateMilitairyGate",
    "GateSealedCaves",
    "GateSealedSirensCave",
    "GateLakeDesolation"
}

past_teleportation_gates = {
    "GateLakeSirineRight",
    "GateAccessToPast",
    "GateCastleRamparts",
    "GateCastleKeep",
    "GateRoyalTowers",
    "GateMaw",
    "GateCavesOfBanishment"
}
