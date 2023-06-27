from ...stardew_rule import Count, StardewRule, True_
from ...mods.mod_data import ModNames
from ... import options


def has_skull_cavern_elevator_to_floor(self, floor: int) -> StardewRule:
    if (self.options[options.TheMinesElevatorsProgression] ==
            options.TheMinesElevatorsProgression.option_progressive or
            self.options[options.TheMinesElevatorsProgression] ==
            options.TheMinesElevatorsProgression.option_progressive_from_previous_floor) and \
            ModNames.skull_cavern_elevator in self.options[options.Mods]:
        return self.received("Progressive Skull Cavern Elevator", count=int(floor / 25))
    return True_()
