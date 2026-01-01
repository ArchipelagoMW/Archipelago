from BaseClasses import CollectionState
from typing import TYPE_CHECKING

from .Options import StageLogic, BowserDoor, ObjectVis

if TYPE_CHECKING:
    from . import YoshisIslandWorld


class YoshiLogic:
    player: int
    game_logic: str
    midring_start: bool
    clouds_always_visible: bool
    consumable_logic: bool
    luigi_pieces: int

    def __init__(self, world: "YoshisIslandWorld") -> None:
        self.player = world.player
        self.boss_order = world.boss_order
        self.luigi_pieces = world.options.luigi_pieces_required.value

        if world.options.stage_logic == StageLogic.option_strict:
            self.game_logic = "Easy"
        elif world.options.stage_logic == StageLogic.option_loose:
            self.game_logic = "Normal"
        else:
            self.game_logic = "Hard"

        self.midring_start = not world.options.shuffle_midrings
        self.consumable_logic = not world.options.item_logic

        self.clouds_always_visible =  world.options.hidden_object_visibility >= ObjectVis.option_clouds_only

        self.bowser_door = world.options.bowser_door_mode.value
        if self.bowser_door == BowserDoor.option_door_4:
            self.bowser_door = BowserDoor.option_door_3

    def has_midring(self, state: CollectionState) -> bool:
        return self.midring_start or state.has("Middle Ring", self.player)

    def reconstitute_luigi(self, state: CollectionState) -> bool:
        return state.has("Piece of Luigi", self.player, self.luigi_pieces)

    def bandit_bonus(self, state: CollectionState) -> bool:
        return state.has("Bandit Consumables", self.player) or state.has("Bandit Watermelons", self.player)

    def item_bonus(self, state: CollectionState) -> bool:
        return state.has("Bonus Consumables", self.player)

    def combat_item(self, state: CollectionState) -> bool:
        if not self.consumable_logic:
            return False
        else:
            if self.game_logic == "Easy":
                return self.item_bonus(state)
            else:
                return self.bandit_bonus(state) or self.item_bonus(state)

    def melon_item(self, state: CollectionState) -> bool:
        if not self.consumable_logic:
            return False
        else:
            if self.game_logic == "Easy":
                return self.item_bonus(state)
            else:
                return state.has("Bandit Watermelons", self.player) or self.item_bonus(state)

    def default_vis(self, state: CollectionState) -> bool:
        if self.clouds_always_visible:
            return True
        else:
            return False

    def cansee_clouds(self, state: CollectionState) -> bool:
        if self.game_logic != "Easy":
            return True
        else:
            return self.default_vis(state) or state.has("Secret Lens", self.player) or self.combat_item(state)

    def bowserdoor_1(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({"Egg Plant", "! Switch"}, self.player) and state.has("Egg Capacity Upgrade", self.player, 2)
        elif self.game_logic == "Normal":
            return state.has("Egg Plant", self.player) and state.has("Egg Capacity Upgrade", self.player, 1)
        else:
            return state.has("Egg Plant", self.player)

    def bowserdoor_2(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return ((state.has("Egg Capacity Upgrade", self.player, 3) and state.has("Egg Plant", self.player)) or self.combat_item(state)) and state.has("Key", self.player)
        elif self.game_logic == "Normal":
            return ((state.has("Egg Capacity Upgrade", self.player, 2) and state.has("Egg Plant", self.player)) or self.combat_item(state)) and state.has("Key", self.player)
        else:
            return ((state.has("Egg Capacity Upgrade", self.player, 1) and state.has("Egg Plant", self.player)) or self.combat_item(state)) and state.has("Key", self.player)

    def bowserdoor_3(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def bowserdoor_4(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _68Route(self, state: CollectionState) -> bool:
        if self.bowser_door == 0:
            return True
        elif self.bowser_door == 1:
            return self.bowserdoor_1(state)
        elif self.bowser_door == 2:
            return self.bowserdoor_2(state)
        elif self.bowser_door == 3:
            return True
        elif self.bowser_door == 4:
            return True
        elif self.bowser_door == 5:
            return self.bowserdoor_1(state) and self.bowserdoor_2(state) and self.bowserdoor_3(state)

    def _68CollectibleRoute(self, state: CollectionState) -> bool:
        if self.bowser_door == 0:
            return True
        elif self.bowser_door == 1:
            return self.bowserdoor_1(state)
        elif self.bowser_door == 2:
            return self.bowserdoor_2(state)
        elif self.bowser_door == 3:
            return True
        elif self.bowser_door == 4:
            return True
        elif self.bowser_door == 5:
            return self.bowserdoor_1(state)


##############################################################################
    def _13Game(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has("Key", self.player)
        elif self.game_logic == "Normal":
            return state.has("Key", self.player)
        else:
            return state.has("Key", self.player)
##############################################################################
    def _14Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({"Spring Ball", "Key"}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({"Spring Ball", "Key"}, self.player)
        else:
            return state.has_all({"Spring Ball", "Key"}, self.player)

    def _14Boss(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has("Egg Plant", self.player)
        elif self.game_logic == "Normal":
            return state.has("Egg Plant", self.player)
        else:
            return (state.has("Egg Capacity Upgrade", self.player, 5) or state.has("Egg Plant", self.player))

    def _14CanFightBoss(self, state: CollectionState) -> bool:
        if state.can_reach(self.boss_order[0], "Location", self.player):
            return True
##############################################################################
    def _17Game(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has("Key", self.player)
        elif self.game_logic == "Normal":
            return state.has("Key", self.player)
        else:
            return state.has("Key", self.player)
##############################################################################
    def _18Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({"Key", "Arrow Wheel"}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({"Key", "Arrow Wheel"}, self.player)
        else:
            return state.has_all({"Key", "Arrow Wheel"}, self.player)

    def _18Boss(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _18CanFightBoss(self, state: CollectionState) -> bool:
        if state.can_reach(self.boss_order[1], "Location", self.player):
            return True
##############################################################################
    def _21Game(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({"Poochy", "Large Spring Ball", "Key"}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({"Poochy", "Large Spring Ball", "Key"}, self.player)
        else:
            return state.has_all({"Poochy", "Large Spring Ball", "Key"}, self.player)
##############################################################################
    def _23Game(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({"Mole Tank Morph", "Key"}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({"Mole Tank Morph", "Key"}, self.player)
        else:
            return state.has_all({"Mole Tank Morph", "Key"}, self.player)
##############################################################################
    def _24Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({"! Switch", "Key", "Dashed Stairs"}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({"! Switch", "Dashed Stairs"}, self.player)
        else:
            return state.has("! Switch", self.player)

    def _24Boss(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _24CanFightBoss(self, state: CollectionState) -> bool:
        if state.can_reach(self.boss_order[2], "Location", self.player):
            return True
##############################################################################
    def _26Game(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({"Large Spring Ball", "Key"}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({"Large Spring Ball", "Key"}, self.player)
        else:
            return state.has_all({"Large Spring Ball", "Key"}, self.player)
##############################################################################
    def _27Game(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has("Key", self.player)
        elif self.game_logic == "Normal":
            return state.has("Key", self.player)
        else:
            return state.has("Key", self.player)
##############################################################################
    def _28Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({"Arrow Wheel", "Key"}, self.player) and (state.has("Egg Capacity Upgrade", self.player, 1))
        elif self.game_logic == "Normal":
            return state.has_all({"Arrow Wheel", "Key"}, self.player)
        else:
            return state.has_all({"Arrow Wheel", "Key"}, self.player)

    def _28Boss(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _28CanFightBoss(self, state: CollectionState) -> bool:
        if state.can_reach(self.boss_order[3], "Location", self.player):
            return True
##############################################################################
    def _32Game(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({"Dashed Stairs", "Spring Ball", "Key"}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({"Dashed Stairs", "Key"}, self.player)
        else:
            return state.has_all({"Dashed Stairs", "Key"}, self.player)
##############################################################################
    def _34Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has("Dashed Platform", self.player)
        elif self.game_logic == "Normal":
            return (state.has("Dashed Platform", self.player) or self.has_midring(state))
        else:
            return True

    def _34Boss(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has("Giant Eggs", self.player)
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _34CanFightBoss(self, state: CollectionState) -> bool:
        if state.can_reach(self.boss_order[4], "Location", self.player):
            return True
##############################################################################
    def _37Game(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({"Key", "Large Spring Ball"}, self.player)
        elif self.game_logic == "Normal":
            return state.has("Key", self.player)
        else:
            return state.has("Key", self.player)
##############################################################################
    def _38Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return (state.has("Egg Capacity Upgrade", self.player, 3) or self.combat_item(state))
        elif self.game_logic == "Normal":
            return (state.has("Egg Capacity Upgrade", self.player, 1) or self.combat_item(state))
        else:
            return True

    def _38Boss(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _38CanFightBoss(self, state: CollectionState) -> bool:
        if state.can_reach(self.boss_order[5], "Location", self.player):
            return True
##############################################################################
    def _42Game(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({"Large Spring Ball", "Key"}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({"Large Spring Ball", "Key"}, self.player)
        else:
            return state.has("Key", self.player)
##############################################################################
    def _44Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({"Dashed Stairs", "Vanishing Arrow Wheel", "Arrow Wheel", "Bucket", "Key"}, self.player) and (state.has("Egg Capacity Upgrade", self.player, 1) or self.combat_item(state))
        elif self.game_logic == "Normal":
            return state.has_all({"Dashed Stairs", "Vanishing Arrow Wheel", "Arrow Wheel", "Bucket", "Key"}, self.player)
        else:
            return state.has_all({"Dashed Stairs", "Vanishing Arrow Wheel", "Arrow Wheel", "Bucket", "Key"}, self.player)

    def _44Boss(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _44CanFightBoss(self, state: CollectionState) -> bool:
        if state.can_reach(self.boss_order[6], "Location", self.player):
            return True
########################################################################################################

    def _46Game(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({"Key", "Large Spring Ball"}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({"Key", "Large Spring Ball"}, self.player)
        else:
            return state.has_all({"Key", "Large Spring Ball"}, self.player)

    def _47Game(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({"Key", "Large Spring Ball"}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({"Key", "Large Spring Ball"}, self.player)
        else:
            return state.has_all({"Key", "Large Spring Ball"}, self.player)
##############################################################################
    def _48Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return (state.has_all({"Dashed Stairs", "Vanishing Arrow Wheel", "Key", "Large Spring Ball"}, self.player))
        elif self.game_logic == "Normal":
            return (state.has_all({"Dashed Stairs", "Vanishing Arrow Wheel", "Key", "Large Spring Ball"}, self.player))
        else:
            return (state.has_all({"Key", "Large Spring Ball"}, self.player))

    def _48Boss(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return (state.has("Egg Capacity Upgrade", self.player, 3))
        elif self.game_logic == "Normal":
            return (state.has("Egg Capacity Upgrade", self.player, 2))
        else:
            return (state.has("Egg Capacity Upgrade", self.player, 1))

    def _48CanFightBoss(self, state: CollectionState) -> bool:
        if state.can_reach(self.boss_order[7], "Location", self.player):
            return True
######################################################################################################################
    def _51Game(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has("Key", self.player)
        elif self.game_logic == "Normal":
            return state.has("Key", self.player)
        else:
            return state.has("Key", self.player)
##############################################################################
    def _54Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return (state.has_all({"Dashed Stairs", "Platform Ghost", "Dashed Platform"}, self.player))
        elif self.game_logic == "Normal":
            return (state.has_all({"Dashed Stairs", "Platform Ghost", "Dashed Platform"}, self.player))
        else:
            return (state.has_all({"Dashed Stairs", "Platform Ghost"}, self.player))

    def _54Boss(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return (state.has("Egg Capacity Upgrade", self.player, 2) and state.has("Egg Plant", self.player))
        elif self.game_logic == "Normal":
            return ((state.has("Egg Capacity Upgrade", self.player, 1) and state.has("Egg Plant", self.player)) or (state.has("Egg Capacity Upgrade", self.player, 5) and self.has_midring(state)))
        else:
            return ((state.has("Egg Plant", self.player)) or (state.has("Egg Capacity Upgrade", self.player, 3) and self.has_midring(state)))

    def _54CanFightBoss(self, state: CollectionState) -> bool:
        if state.can_reach(self.boss_order[8], "Location", self.player):
            return True
###################################################################################################
    def _58Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({"Arrow Wheel", "Large Spring Ball"}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({"Arrow Wheel", "Large Spring Ball"}, self.player)
        else:
            return state.has_all({"Arrow Wheel", "Large Spring Ball"}, self.player)

    def _58Boss(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _58CanFightBoss(self, state: CollectionState) -> bool:
        if state.can_reach(self.boss_order[9], "Location", self.player):
            return True
##############################################################################
    def _61Game(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({"Dashed Platform", "Key", "Beanstalk"}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({"Dashed Platform", "Key", "Beanstalk"}, self.player)
        else:
            return state.has("Key", self.player)
##############################################################################
    def _64Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({"Spring Ball", "Large Spring Ball", "Egg Plant", "Key"}, self.player) and (state.has("Egg Capacity Upgrade", self.player, 3) or self.combat_item(state))
        elif self.game_logic == "Normal":
            return state.has_all({"Large Spring Ball", "Egg Plant", "Key"}, self.player) and (state.has("Egg Capacity Upgrade", self.player, 2) or self.combat_item(state))
        else:
            return state.has_all({"Egg Plant", "Key"}, self.player) and (state.has("Egg Capacity Upgrade", self.player, 1) or self.combat_item(state))

    def _64Boss(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has("Egg Plant", self.player)
        elif self.game_logic == "Normal":
            return state.has("Egg Plant", self.player)
        else:
            return True

    def _64CanFightBoss(self, state: CollectionState) -> bool:
        if state.can_reach(self.boss_order[10], "Location", self.player):
            return True
##############################################################################
    def _67Game(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has("Key", self.player)
        elif self.game_logic == "Normal":
            return state.has("Key", self.player)
        else:
            return state.has("Key", self.player)
##############################################################################
    def _68Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({"Helicopter Morph", "Egg Plant", "Giant Eggs"}, self.player) and self._68Route(state)
        elif self.game_logic == "Normal":
            return state.has_all({"Helicopter Morph", "Egg Plant", "Giant Eggs"}, self.player) and self._68Route(state)
        else:
            return state.has_all({"Helicopter Morph", "Giant Eggs"}, self.player) and self._68Route(state)
