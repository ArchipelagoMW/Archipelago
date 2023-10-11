from ...logic.received_logic import ReceivedLogic
from ...options import ElevatorProgression, Mods
from ...stardew_rule import StardewRule, True_
from ...mods.mod_data import ModNames


class ModElevatorLogic:
    player: int
    elevator_option: ElevatorProgression
    mods: Mods
    received: ReceivedLogic

    def __init__(self, player: int, elevator_option: ElevatorProgression, mods: Mods, received: ReceivedLogic):
        self.player = player
        self.elevator_option = elevator_option
        self.mods = mods
        self.received = received

    def has_skull_cavern_elevator_to_floor(self, floor: int) -> StardewRule:
        if self.elevator_option != ElevatorProgression.option_vanilla and ModNames.skull_cavern_elevator in self.mods:
            return self.received("Progressive Skull Cavern Elevator", floor // 25)
        return True_()
