from typing import Union, Optional
from BaseClasses import MultiWorld, CollectionState
from .Options import get_option_value

class YoshiLogic:
    player: int
    game_logic: tuple
    midring_start: bool
    clouds_always_visible: bool
    consumable_logic: bool
    luigi_pieces: int


    def __init__(self, world: MultiWorld, player: int, boss_order: Optional[list], luigi_pieces: int):
        self.player = player
        self.boss_order = boss_order
        self.luigi_pieces = luigi_pieces

        
        if get_option_value(world, player, "stage_logic") == 0:
            self.game_logic = "Easy"
        elif get_option_value(world, player, "stage_logic") == 1:
            self.game_logic = "Normal"
        else:
            self.game_logic = "Hard"

        if get_option_value(world, player, "shuffle_midrings") == 0:
            self.midring_start = True
        else:
            self.midring_start = False

        if get_option_value(world, player, "item_logic") == 0:
            self.consumable_logic = False
        else:
            self.consumable_logic = True

        if get_option_value(world, player, "hidden_object_visibility") >= 2:
            self.clouds_always_visible = True
        else:
            self.clouds_always_visible = False

        if get_option_value(world, player, "bowser_door_mode") == 0:
            self.bowser_door = 0
        elif get_option_value(world, player, "bowser_door_mode") == 1:
            self.bowser_door = 1
        elif get_option_value(world, player, "bowser_door_mode") == 2:
            self.bowser_door = 2
        elif get_option_value(world, player, "bowser_door_mode") == 5:
            self.bowser_door = 5
        else:
            self.bowser_door = 3

    def has_midring(self, state: CollectionState) -> bool:
        if self.midring_start == True:
            return True
        else:
            return state.has('Middle Ring', self.player)

    def ReconstituteLuigi(self, state: CollectionState) -> bool:
        return state.has('Piece of Luigi', self.player, self.luigi_pieces)

    def bandit_bonus(self, state: CollectionState) -> bool:
        return (state.has('Seed Spitting Contest', self.player) or state.has('Touch Fuzzy Get Dizzy: Gather Coins', self.player) or state.has("Lakitu's Wall: Gather Coins", self.player) or state.has('Ride Like The Wind: Gather Coins', self.player))

    def item_bonus(self, state: CollectionState) -> bool:
        return state.has_any({'Flip Cards', 'Drawing Lots', 'Match Cards'}, self.player)

    def combat_item(self, state: CollectionState) -> bool:
        if self.consumable_logic == False:
            return False
        else:
            if self.game_logic == "Easy":
                return self.item_bonus(state)
            else:
                return self.bandit_bonus(state) or self.item_bonus(state)

    def melon_item(self, state: CollectionState) -> bool:
        if self.consumable_logic == False:
            return False
        else:
            if self.game_logic == "Easy":
                return self.item_bonus(state)
            else:
                return state.has('Seed Spitting Contest', self.player) or self.item_bonus(state)

    def default_vis(self, state: CollectionState) -> bool:
        if self.clouds_always_visible == True:
            return True
        else:
            return False

    def cansee_clouds(self, state: CollectionState) -> bool:
        if self.game_logic != "Easy":
            return True
        else:
            return (self.default_vis(state) or state.has('Secret Lens', self.player) or self.combat_item(state))

    def bowserdoor_1(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Egg Plant', '! Switch'}, self.player) and state.has('Egg Capacity Upgrade', self.player, 2)
        elif self.game_logic == "Normal":
            return state.has_all({'Egg Plant'}, self.player) and state.has('Egg Capacity Upgrade', self.player, 1)
        else:
            return state.has_all({'Egg Plant'}, self.player)

    def bowserdoor_2(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return ((state.has('Egg Capacity Upgrade', self.player, 3) and state.has('Egg Plant', self.player)) or self.combat_item(state)) and state.has_all({'Key'}, self.player)
        elif self.game_logic == "Normal":
            return ((state.has('Egg Capacity Upgrade', self.player, 2) and state.has('Egg Plant', self.player)) or self.combat_item(state)) and state.has_all({'Key'}, self.player)
        else:
            return ((state.has('Egg Capacity Upgrade', self.player, 1) and state.has('Egg Plant', self.player)) or self.combat_item(state)) and state.has_all({'Key'}, self.player)

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
            return self.bowserdoor_3(state)
        elif self.bowser_door == 5:
            return self.bowserdoor_1(state) and self.bowserdoor_2(state) and self.bowserdoor_3(state)

    ############################################################
    def _11Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Dashed Stairs', 'Beanstalk'}, self.player)
        elif self.game_logic == "Normal":
            return state.has('Dashed Stairs', self.player)
        else:
            return True

    def _11Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Dashed Stairs', 'Beanstalk'}, self.player)
        elif self.game_logic == "Normal":
            return state.has('Dashed Stairs', self.player)
        else:
            return True

    def _11Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Tulip', 'Beanstalk', 'Dashed Stairs'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Tulip'}, self.player)
        else:
            return True

    def _11Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Beanstalk'}, self.player)
        elif self.game_logic == "Normal":
            return True
        else:
            return True
##################
    def _12Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Large Spring Ball', 'Helicopter Morph'}, self.player)
        elif self.game_logic == "Normal":
            return state.has('Helicopter Morph', self.player)
        else:
            return True

    def _12Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Large Spring Ball', 'Helicopter Morph'}, self.player)
        elif self.game_logic == "Normal":
            return state.has('Helicopter Morph', self.player)
        else:
            return True

    def _12Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Large Spring Ball'}, self.player) and self.has_midring(state)
        elif self.game_logic == "Normal":
            return self.has_midring(state)
        else:
            return True

    def _12Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Large Spring Ball'}, self.player)
        elif self.game_logic == "Normal":
            return True
        else:
            return True
###############################
    def _13Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _13Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _13Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _13Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _13Game(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Key'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Key'}, self.player)
        else:
            return state.has_all({'Key'}, self.player)
############################################
    def _14Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Spring Ball'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Spring Ball'}, self.player)
        else:
            return state.has_all({'Spring Ball'}, self.player)

    def _14Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Spring Ball', 'Key'}, self.player) and (state.has('Egg Capacity Upgrade', self.player, 3) or self.combat_item(state))
        elif self.game_logic == "Normal":
            return state.has_all({'Spring Ball', 'Key'}, self.player) and (state.has('Egg Capacity Upgrade', self.player, 3) or self.combat_item(state))
        else:
            return state.has_all({'Spring Ball', 'Key'}, self.player) and (state.has('Egg Capacity Upgrade', self.player, 3) or self.combat_item(state))

    def _14Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Spring Ball'}, self.player) and (self.has_midring(state) or state.has('Key', self.player))
        elif self.game_logic == "Normal":
            return state.has_all({'Spring Ball'}, self.player)
        else:
            return state.has_all({'Spring Ball'}, self.player)

    def _14Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Spring Ball', 'Key'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Spring Ball', 'Key'}, self.player)
        else:
            return state.has_all({'Spring Ball', 'Key'}, self.player)

    def _14Boss(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Egg Plant'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Egg Plant'}, self.player)
        else:
            return (state.has('Egg Capacity Upgrade', self.player, 5) or state.has('Egg Plant', self.player))

    def _14CanFightBoss(self, state: CollectionState) -> bool:
        if state.can_reach(self.boss_order[0], 'Location', self.player):
            return True
######################################################
    def _15Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _15Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _15Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return self.has_midring(state) or self.cansee_clouds(state)
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _15Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True
##########################################################
    def _16Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Large Spring Ball', 'Flashing Eggs', 'Mole Tank Morph', '! Switch'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Large Spring Ball', 'Flashing Eggs', 'Mole Tank Morph', '! Switch'}, self.player)
        else:
            return state.has_all({'Large Spring Ball', 'Flashing Eggs', 'Mole Tank Morph', '! Switch'}, self.player)

    def _16Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Large Spring Ball'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Large Spring Ball'}, self.player)
        else:
            return True

    def _16Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return (self.has_midring(state) and state.has('Tulip', self.player) or self.has_midring(state) and state.has('Beanstalk', self.player)) and state.has('Large Spring Ball', self.player)
        elif self.game_logic == "Normal":
            return (self.has_midring(state) and state.has('Tulip', self.player) or self.has_midring(state) and state.has('Beanstalk', self.player) or (state.has('Tulip', self.player and state.has('Beanstalk', self.player)))) and state.has('Large Spring Ball', self.player)
        else:
            return True

    def _16Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Large Spring Ball', 'Beanstalk'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Large Spring Ball', 'Beanstalk'}, self.player)
        else:
            return state.has('Large Spring Ball', self.player)
#####################################################################
    def _17Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Flashing Eggs', 'Spring Ball', 'Chomp Rock', 'Beanstalk'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Flashing Eggs', 'Spring Ball', 'Chomp Rock', 'Beanstalk'}, self.player)
        else:
            return state.has_all({'Flashing Eggs', 'Spring Ball', 'Chomp Rock', 'Beanstalk'}, self.player)

    def _17Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _17Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return self.has_midring(state) or (self.cansee_clouds and state.has_all({'Spring Ball', 'Chomp Rock', 'Beanstalk'}, self.player))
        elif self.game_logic == "Normal":
            return self.has_midring(state) or (self.cansee_clouds and state.has_all({'Spring Ball', 'Chomp Rock', 'Beanstalk'}, self.player))
        else:
            return True

    def _17Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _17Game(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Key'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Key'}, self.player)
        else:
            return state.has_all({'Key'}, self.player)
###############################################################################
    def _18Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Platform Ghost'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Platform Ghost'}, self.player)
        else:
            return state.has_all({'Platform Ghost'}, self.player)

    def _18Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Platform Ghost'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Platform Ghost'}, self.player)
        else:
            return state.has_all({'Platform Ghost'}, self.player)

    def _18Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return self.has_midring(state) and (state.has('Platform Ghost', self.player) or state.has_all({'Arrow Wheel', 'Key'}, self.player))
        elif self.game_logic == "Normal":
            return self.has_midring(state) and (state.has('Platform Ghost', self.player) or state.has_all({'Arrow Wheel', 'Key'}, self.player))
        else:
            return True

    def _18Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Key', 'Arrow Wheel'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Key', 'Arrow Wheel'}, self.player)
        else:
            return state.has_all({'Key', 'Arrow Wheel'}, self.player)

    def _18Boss(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _18CanFightBoss(self, state: CollectionState) -> bool:
        if state.can_reach(self.boss_order[1], 'Location', self.player):
            return True
##################################################################################
    def _1ECoins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Poochy'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Poochy'}, self.player)
        else:
            return state.has_all({'Poochy'}, self.player)

    def _1EFlowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Poochy'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Poochy'}, self.player)
        else:
            return state.has_all({'Poochy'}, self.player)

    def _1EStars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has('Poochy', self.player)
        elif self.game_logic == "Normal":
            return state.has('Poochy', self.player)
        else:
            return state.has('Poochy', self.player)

    def _1EClear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has('Poochy', self.player)
        elif self.game_logic == "Normal":
            return state.has('Poochy', self.player)
        else:
            return state.has('Poochy', self.player)
###############################################################################
    def _21Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Poochy', 'Large Spring Ball', 'Spring Ball'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Poochy', 'Large Spring Ball', 'Spring Ball'}, self.player)
        else:
            return state.has_all({'Poochy', 'Large Spring Ball'}, self.player)

    def _21Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Super Star', 'Large Spring Ball'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Super Star', 'Large Spring Ball'}, self.player)
        else:
            return state.has_all({'Super Star', 'Large Spring Ball'}, self.player)

    def _21Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has('Large Spring Ball', self.player) and self.has_midring(state)
        elif self.game_logic == "Normal":
            return state.has('Large Spring Ball', self.player) and self.has_midring(state)
        else:
            return state.has('Large Spring Ball', self.player)

    def _21Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has('Large Spring Ball', self.player)
        elif self.game_logic == "Normal":
            return state.has('Large Spring Ball', self.player)
        else:
            return state.has('Large Spring Ball', self.player)

    def _21Game(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Poochy', 'Large Spring Ball', 'Key'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Poochy', 'Large Spring Ball', 'Key'}, self.player)
        else:
            return state.has_all({'Poochy', 'Large Spring Ball', 'Key'}, self.player)
#################################################################################
    def _22Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Beanstalk', 'Super Star', 'Egg Launcher', 'Large Spring Ball', 'Mole Tank Morph'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Beanstalk', 'Super Star', 'Large Spring Ball', 'Mole Tank Morph'}, self.player)
        else:
            return state.has_all({'Super Star', 'Large Spring Ball', 'Mole Tank Morph'}, self.player)

    def _22Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Beanstalk', 'Super Star', 'Egg Launcher', 'Large Spring Ball', 'Spring Ball'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Super Star', 'Large Spring Ball', 'Beanstalk', 'Spring Ball'}, self.player)
        else:
            return state.has_all({'Super Star', 'Large Spring Ball'}, self.player)

    def _22Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return (self.has_midring(state) and (state.has('Tulip', self.player))) and state.has_all({'Beanstalk', 'Super Star', 'Large Spring Ball', 'Egg Launcher'}, self.player)
        elif self.game_logic == "Normal":
            return (self.has_midring(state) or (state.has('Tulip', self.player))) and state.has_all({'Beanstalk', 'Super Star', 'Large Spring Ball'}, self.player)
        else:
            return True

    def _22Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Beanstalk', 'Super Star', 'Egg Launcher', 'Large Spring Ball'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Beanstalk', 'Super Star', 'Large Spring Ball'}, self.player)
        else:
            return state.has_all({'Super Star', 'Large Spring Ball'}, self.player)
#################################################################################
    def _23Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'! Switch'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'! Switch'}, self.player)
        else:
            return state.has_all({'! Switch'}, self.player)

    def _23Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_any({'Large Spring Ball', 'Super Star'}, self.player)
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _23Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _23Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_any({'Large Spring Ball', 'Super Star'}, self.player)
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _23Game(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Mole Tank Morph', 'Key'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Mole Tank Morph', 'Key'}, self.player)
        else:
            return state.has_all({'Mole Tank Morph', 'Key'}, self.player)
########################################################################################
    def _24Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'! Switch', 'Key', 'Dashed Stairs'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'! Switch', 'Key'}, self.player)
        else:
            return state.has_all({'! Switch', 'Key'}, self.player)

    def _24Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'! Switch', 'Key', 'Dashed Stairs'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'! Switch', 'Key'}, self.player)
        else:
            return state.has_all({'! Switch', 'Key'}, self.player)

    def _24Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'! Switch', 'Dashed Stairs'}, self.player) and self.has_midring(state)
        elif self.game_logic == "Normal":
            return state.has_all({'! Switch', 'Dashed Stairs'}, self.player)
        else:
            return state.has_all({'! Switch'}, self.player)

    def _24Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'! Switch', 'Key', 'Dashed Stairs'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'! Switch', 'Dashed Stairs'}, self.player)
        else:
            return state.has_all({'! Switch'}, self.player)

    def _24Boss(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _24CanFightBoss(self, state: CollectionState) -> bool:
        if state.can_reach(self.boss_order[2], 'Location', self.player):
            return True
###########################################################################################
    def _25Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Chomp Rock'}, self.player)
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _25Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Key', 'Train Morph', 'Chomp Rock'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Key', 'Train Morph'}, self.player)
        else:
            return state.has_all({'Key', 'Train Morph'}, self.player)

    def _25Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _25Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Chomp Rock'}, self.player)
        elif self.game_logic == "Normal":
            return True
        else:
            return True
##################################################################################
    def _26Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Large Spring Ball'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Large Spring Ball'}, self.player)
        else:
            return state.has_all({'Large Spring Ball'}, self.player)

    def _26Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Large Spring Ball', 'Egg Launcher'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Large Spring Ball', 'Egg Launcher'}, self.player)
        else:
            return state.has_all({'Large Spring Ball','Egg Launcher'}, self.player)

    def _26Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Large Spring Ball'}, self.player) and self.has_midring(state)
        elif self.game_logic == "Normal":
            return state.has_all({'Large Spring Ball'}, self.player)
        else:
            return True

    def _26Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Large Spring Ball'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Large Spring Ball'}, self.player)
        else:
            return state.has_all({'Large Spring Ball'}, self.player)

    def _26Game(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Large Spring Ball', 'Key'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Large Spring Ball', 'Key'}, self.player)
        else:
            return state.has_all({'Large Spring Ball', 'Key'}, self.player)
#########################################################################################
    def _27Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_any({'Dashed Platform', 'Giant Eggs'}, self.player) and state.has('Large Spring Ball', self.player)
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _27Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Large Spring Ball', '! Switch'}, self.player) and (self.combat_item(state) or state.has('Giant Eggs', self.player))
        elif self.game_logic == "Normal":
            return state.has_all({'Large Spring Ball', '! Switch'}, self.player) and (self.combat_item(state) or state.has('Giant Eggs', self.player))
        else:
            return state.has_all({'! Switch'}, self.player)

    def _27Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Giant Eggs'}, self.player) and self.has_midring(state)
        elif self.game_logic == "Normal":
            return state.has_all({'Giant Eggs'}, self.player) or self.has_midring(state)
        else:
            return state.has_all({'Giant Eggs'}, self.player) or self.has_midring(state)

    def _27Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Large Spring Ball', 'Car Morph'}, self.player)
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _27Game(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Key'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Key'}, self.player)
        else:
            return state.has_all({'Key'}, self.player)
##################################################################################################
    def _28Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_any({'Arrow Wheel', 'Key'}, self.player) and (state.has('Egg Capacity Upgrade', self.player, 1))
        elif self.game_logic == "Normal":
            return state.has_any({'Arrow Wheel', 'Key'}, self.player)
        else:
            return state.has_any({'Arrow Wheel', 'Key'}, self.player)

    def _28Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_any({'Arrow Wheel', 'Train Morph', 'Key'}, self.player) and (state.has('Egg Capacity Upgrade', self.player, 1))
        elif self.game_logic == "Normal":
            return state.has_any({'Arrow Wheel', 'Key', 'Train Morph'}, self.player)
        else:
            return state.has_any({'Arrow Wheel', 'Key', 'Train Morph'}, self.player)

    def _28Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Arrow Wheel', 'Key'}, self.player) and self.has_midring(state) and (state.has('Egg Capacity Upgrade', self.player, 1))
        elif self.game_logic == "Normal":
            return state.has_all({'Arrow Wheel'}, self.player) and (self.has_midring(state) or state.has('Key', self.player))
        else:
            return state.has_all({'Arrow Wheel'}, self.player)

    def _28Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_any({'Arrow Wheel', 'Key'}, self.player) and (state.has('Egg Capacity Upgrade', self.player, 1))
        elif self.game_logic == "Normal":
            return state.has_any({'Arrow Wheel', 'Key'}, self.player)
        else:
            return state.has_any({'Arrow Wheel', 'Key'}, self.player)

    def _28Boss(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _28CanFightBoss(self, state: CollectionState) -> bool:
        if state.can_reach(self.boss_order[3], 'Location', self.player):
            return True
######################################################################################################
    def _2ECoins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Large Spring Ball', '! Switch'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Large Spring Ball', '! Switch'}, self.player)
        else:
            return state.has_all({'Large Spring Ball', '! Switch'}, self.player)

    def _2EFlowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Large Spring Ball', '! Switch'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Large Spring Ball', '! Switch'}, self.player)
        else:
            return state.has_all({'Large Spring Ball', '! Switch'}, self.player)

    def _2EStars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _2EClear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Large Spring Ball', '! Switch'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Large Spring Ball', '! Switch'}, self.player)
        else:
            return state.has_all({'Large Spring Ball', '! Switch'}, self.player)
#####################################################################################################
    def _31Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _31Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _31Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return self.has_midring(state)
        elif self.game_logic == "Normal":
            return self.has_midring(state)
        else:
            return self.has_midring(state)

    def _31Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True
#############################################################################################
    def _32Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Dashed Stairs', 'Spring Ball'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Dashed Stairs'}, self.player)
        else:
            return state.has_all({'Dashed Stairs'}, self.player)

    def _32Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Dashed Stairs', 'Spring Ball'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Dashed Stairs'}, self.player)
        else:
            return state.has_all({'Dashed Stairs'}, self.player)

    def _32Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return self.has_midring(state) and state.has('Tulip', self.player)
        elif self.game_logic == "Normal":
            return self.has_midring(state) and state.has('Tulip', self.player)
        else:
            return self.has_midring(state) and state.has('Tulip', self.player)

    def _32Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Dashed Stairs', 'Spring Ball'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Dashed Stairs'}, self.player)
        else:
            return state.has_all({'Dashed Stairs'}, self.player)

    def _32Game(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Dashed Stairs', 'Spring Ball', 'Key'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Dashed Stairs', 'Key'}, self.player)
        else:
            return state.has_all({'Dashed Stairs', 'Key'}, self.player)
######################################################################################
    def _33Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Submarine Morph', 'Helicopter Morph'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Submarine Morph', 'Helicopter Morph'}, self.player)
        else:
            return state.has_all({'Submarine Morph', 'Helicopter Morph'}, self.player)

    def _33Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Submarine Morph', 'Helicopter Morph'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Submarine Morph', 'Helicopter Morph'}, self.player)
        else:
            return state.has_all({'Submarine Morph', 'Helicopter Morph'}, self.player)

    def _33Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return self.has_midring(state) or state.has_all({'Submarine Morph', 'Helicopter Morph'}, self.player)
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _33Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Submarine Morph', 'Helicopter Morph'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Submarine Morph', 'Helicopter Morph'}, self.player)
        else:
            return state.has_all({'Submarine Morph', 'Helicopter Morph'}, self.player)
##############################################################################################
    def _34Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Submarine Morph'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Submarine Morph'}, self.player)
        else:
            return state.has_all({'Submarine Morph'}, self.player)

    def _34Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return (state.has('Egg Capacity Upgrade', self.player, 5) or self.combat_item(state)) and (state.has('Dashed Platform', self.player))
        elif self.game_logic == "Normal":
            return (state.has('Egg Capacity Upgrade', self.player, 5) or self.combat_item(state)) and (state.has('Dashed Platform', self.player) or self.has_midring(state))
        else:
            return (state.has('Egg Capacity Upgrade', self.player, 5) or self.combat_item(state))

    def _34Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return self.has_midring(state)
        elif self.game_logic == "Normal":
            return self.has_midring(state)
        else:
            return True

    def _34Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has('Dashed Platform', self.player)
        elif self.game_logic == "Normal":
            return (state.has('Dashed Platform', self.player) or self.has_midring(state))
        else:
            return True

    def _34Boss(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Giant Eggs'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Giant Eggs'}, self.player)
        else:
            return state.has_all({'Giant Eggs'}, self.player)

    def _34CanFightBoss(self, state: CollectionState) -> bool:
        if state.can_reach(self.boss_order[4], 'Location', self.player):
            return True
#################################################################################################
    def _35Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _35Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Watermelon'}, self.player) or self.melon_item(state)
        elif self.game_logic == "Normal":
            return state.has_all({'Watermelon'}, self.player) or self.melon_item(state)
        else:
            return True

    def _35Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return ((self.has_midring(state) or state.has_all({'Tulip'}, self.player)) and self.cansee_clouds(state)) or self.has_midring(state) and state.has_all({'Tulip'}, self.player)
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _35Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True
###################################################################################################
    def _36Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Chomp Rock', 'Beanstalk', 'Mole Tank Morph', 'Large Spring Ball'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_any({'Dashed Stairs', 'Beanstalk'}, self.player) and state.has_all({'Mole Tank Morph', 'Large Spring Ball'}, self.player)
        else:
            return state.has('Mole Tank Morph', self.player)

    def _36Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Chomp Rock', 'Beanstalk', 'Mole Tank Morph', 'Large Spring Ball', '! Switch'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_any({'Dashed Stairs', 'Beanstalk'}, self.player) and state.has_all({'! Switch', 'Mole Tank Morph', 'Large Spring Ball'}, self.player)
        else:
            return state.has_all({'Mole Tank Morph', '! Switch'}, self.player)

    def _36Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Tulip', 'Large Spring Ball', 'Dashed Stairs', 'Chomp Rock', 'Beanstalk', 'Mole Tank Morph'}, self.player) and self.has_midring(state)
        elif self.game_logic == "Normal":
            return (state.has_any({'Dashed Stairs', 'Beanstalk'}, self.player) and state.has_all({'Mole Tank Morph', 'Large Spring Ball'}, self.player)) and (self.has_midring(state) or state.has('Tulip', self.player))
        else:
            return self.has_midring(state) or state.has('Tulip', self.player)

    def _36Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Chomp Rock', 'Large Spring Ball', 'Key'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Large Spring Ball', 'Key'}, self.player)
        else:
            return state.has_all({'Large Spring Ball', 'Key'}, self.player)
##################################################################################################
    def _37Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'! Switch', 'Submarine Morph', 'Large Spring Ball', 'Beanstalk'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'! Switch', 'Submarine Morph', 'Large Spring Ball', 'Beanstalk'}, self.player)
        else:
            return state.has_all({'! Switch', 'Submarine Morph'}, self.player)

    def _37Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Beanstalk', 'Large Spring Ball'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Beanstalk'}, self.player)
        else:
            return True

    def _37Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Large Spring Ball'}, self.player)
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _37Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Large Spring Ball'}, self.player)
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _37Game(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Key', 'Large Spring Ball'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Key'}, self.player)
        else:
            return state.has_all({'Key'}, self.player)
#######################################################################################################
    def _38Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return (state.has('Egg Capacity Upgrade', self.player, 3) or self.combat_item(state))
        elif self.game_logic == "Normal":
            return (state.has('Egg Capacity Upgrade', self.player, 1) or self.combat_item(state))
        else:
            return True

    def _38Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return (state.has('Egg Capacity Upgrade', self.player, 3) or self.combat_item(state))
        elif self.game_logic == "Normal":
            return (state.has('Egg Capacity Upgrade', self.player, 1) or self.combat_item(state))
        else:
            return True

    def _38Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return self.has_midring(state) and state.has('Tulip', self.player)
        elif self.game_logic == "Normal":
            return self.has_midring(state) and state.has('Tulip', self.player)
        else:
            return True

    def _38Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return (state.has('Egg Capacity Upgrade', self.player, 3) or self.combat_item(state))
        elif self.game_logic == "Normal":
            return (state.has('Egg Capacity Upgrade', self.player, 1) or self.combat_item(state))
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
        if state.can_reach(self.boss_order[5], 'Location', self.player):
            return True
########################################################################################################
    def _3ECoins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _3EFlowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _3EStars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _3EClear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True
#########################################################################################################
    def _41Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has('Super Star', self.player)
        elif self.game_logic == "Normal":
            return state.has('Super Star', self.player)
        else:
            return state.has('Super Star', self.player)

    def _41Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has('Super Star', self.player)
        elif self.game_logic == "Normal":
            return state.has('Super Star', self.player)
        else:
            return state.has('Super Star', self.player)

    def _41Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return self.has_midring(state) or (state.has('Tulip', self.player) and self.cansee_clouds(state))
        elif self.game_logic == "Normal":
            return self.has_midring(state) or state.has('Tulip', self.player)
        else:
            return True

    def _41Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has('Super Star', self.player)
        elif self.game_logic == "Normal":
            return state.has('Super Star', self.player)
        else:
            return state.has('Super Star', self.player)
#################################################################################################
    def _42Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Large Spring Ball', '! Switch', 'Egg Launcher'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Large Spring Ball', '! Switch', 'Egg Launcher'}, self.player)
        else:
            return state.has_all({'! Switch', 'Egg Launcher'}, self.player)

    def _42Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Large Spring Ball', 'Egg Launcher'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Large Spring Ball', 'Egg Launcher'}, self.player)
        else:
            return state.has_all({'Egg Launcher'}, self.player)

    def _42Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Large Spring Ball', 'Spring Ball'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Large Spring Ball'}, self.player)
        else:
            return True

    def _42Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Large Spring Ball'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Large Spring Ball'}, self.player)
        else:
            return True

    def _42Game(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Large Spring Ball', 'Key'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Large Spring Ball', 'Key'}, self.player)
        else:
            return state.has_all({'Key'}, self.player)
###################################################################################################
    def _43Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Helicopter Morph', '! Switch', 'Large Spring Ball'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Helicopter Morph', '! Switch', 'Large Spring Ball'}, self.player)
        else:
            return state.has_all({'Helicopter Morph', 'Large Spring Ball'}, self.player)

    def _43Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'! Switch', 'Large Spring Ball'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Large Spring Ball'}, self.player)
        else:
            return state.has_all({'Large Spring Ball'}, self.player)

    def _43Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return (self.has_midring(state) and state.has('Tulip', self.player)) and state.has('! Switch', self.player)
        elif self.game_logic == "Normal":
            return (self.has_midring(state) or state.has('Tulip', self.player)) and state.has('! Switch', self.player)
        else:
            return self.has_midring(state) or state.has('Tulip', self.player)

    def _43Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'! Switch'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'! Switch'}, self.player)
        else:
            return True
####################################################################################################
    def _44Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Dashed Stairs', 'Vanishing Arrow Wheel', 'Arrow Wheel', 'Bucket', 'Key'}, self.player) and (state.has('Egg Capacity Upgrade', self.player, 1) or self.combat_item(state))
        elif self.game_logic == "Normal":
            return state.has_all({'Dashed Stairs', 'Vanishing Arrow Wheel', 'Arrow Wheel', 'Bucket', 'Key'}, self.player)
        else:
            return state.has_all({'Dashed Stairs', 'Vanishing Arrow Wheel', 'Arrow Wheel', 'Bucket', 'Key'}, self.player)

    def _44Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Dashed Stairs', 'Vanishing Arrow Wheel', 'Arrow Wheel', 'Bucket'}, self.player) and (state.has('Egg Capacity Upgrade', self.player, 1) or self.combat_item(state))
        elif self.game_logic == "Normal":
            return state.has_all({'Dashed Stairs', 'Vanishing Arrow Wheel', 'Arrow Wheel', 'Bucket'}, self.player)
        else:
            return state.has_all({'Dashed Stairs', 'Vanishing Arrow Wheel', 'Arrow Wheel', 'Bucket'}, self.player)

    def _44Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Dashed Stairs'}, self.player) and (self.has_midring(state) or state.has('Vanishing Arrow Wheel', self.player) or self.cansee_clouds(state))
        elif self.game_logic == "Normal":
            return state.has_all({'Dashed Stairs'}, self.player)
        else:
            return state.has_all({'Dashed Stairs'}, self.player)

    def _44Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Dashed Stairs', 'Vanishing Arrow Wheel', 'Arrow Wheel', 'Bucket', 'Key'}, self.player) and (state.has('Egg Capacity Upgrade', self.player, 1) or self.combat_item(state))
        elif self.game_logic == "Normal":
            return state.has_all({'Dashed Stairs', 'Vanishing Arrow Wheel', 'Arrow Wheel', 'Bucket', 'Key'}, self.player)
        else:
            return state.has_all({'Dashed Stairs', 'Vanishing Arrow Wheel', 'Arrow Wheel', 'Bucket', 'Key'}, self.player)

    def _44Boss(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _44CanFightBoss(self, state: CollectionState) -> bool:
        if state.can_reach(self.boss_order[6], 'Location', self.player):
            return True
########################################################################################################
    def _45Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Large Spring Ball', 'Chomp Rock'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Large Spring Ball', 'Chomp Rock'}, self.player)
        else:
            return state.has_all({'Large Spring Ball'}, self.player)

    def _45Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Chomp Rock', '! Switch', 'Spring Ball', 'Dashed Platform'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Chomp Rock', '! Switch', 'Dashed Platform'}, self.player)
        else:
            return state.has_all({'Chomp Rock', '! Switch'}, self.player)

    def _45Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Chomp Rock', '! Switch', 'Spring Ball', 'Dashed Platform'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Chomp Rock', '! Switch', 'Dashed Platform'}, self.player)
        else:
            return state.has_all({'Chomp Rock', '! Switch'}, self.player)

    def _45Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True
############################################################################################################
    def _46Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_any({'Large Spring Ball', 'Spring Ball'}, self.player) and (state.has('Egg Plant', self.player) or self.combat_item(state))
        elif self.game_logic == "Normal":
            return state.has('Egg Plant', self.player) or self.combat_item(state)
        else:
            return True

    def _46Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_any({'Large Spring Ball', 'Spring Ball'}, self.player) and (state.has('Egg Plant', self.player) or self.combat_item(state))
        elif self.game_logic == "Normal":
            return state.has('Egg Plant', self.player) or self.combat_item(state)
        else:
            return True

    def _46Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return (self.has_midring(state) or (state.has_all({'Tulip'}, self.player) and self.cansee_clouds(state))) and (state.has('Egg Plant', self.player) or self.combat_item(state))
        elif self.game_logic == "Normal":
            return (self.has_midring(state) or (state.has_all({'Tulip'}, self.player) and self.cansee_clouds(state))) and (state.has('Egg Plant', self.player) or self.combat_item(state))
        else:
            return (self.has_midring(state) or (state.has_all({'Tulip'}, self.player) and self.cansee_clouds(state)))

    def _46Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has('Egg Plant', self.player) or self.combat_item(state)
        elif self.game_logic == "Normal":
            return state.has('Egg Plant', self.player) or self.combat_item(state)
        else:
            return True

    def _46Game(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Key', 'Large Spring Ball'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Key', 'Large Spring Ball'}, self.player)
        else:
            return state.has_all({'Key', 'Large Spring Ball'}, self.player)
##################################################################################################################
    def _47Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Large Spring Ball'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Large Spring Ball'}, self.player)
        else:
            return state.has_all({'Large Spring Ball'}, self.player)

    def _47Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Large Spring Ball'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Large Spring Ball'}, self.player)
        else:
            return state.has_all({'Large Spring Ball'}, self.player)

    def _47Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return (self.has_midring(state) and state.has('Helicopter Morph', self.player)) and state.has('Large Spring Ball', self.player)
        elif self.game_logic == "Normal":
            return (self.has_midring(state) or state.has('Helicopter Morph', self.player)) and state.has('Large Spring Ball', self.player)
        else:
            return (self.has_midring(state) or state.has('Helicopter Morph', self.player)) and state.has('Large Spring Ball', self.player)

    def _47Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Large Spring Ball'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Large Spring Ball'}, self.player)
        else:
            return state.has_all({'Large Spring Ball'}, self.player)

    def _47Game(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Key', 'Large Spring Ball'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Key', 'Large Spring Ball'}, self.player)
        else:
            return state.has_all({'Key', 'Large Spring Ball'}, self.player)
################################################################################################################
    def _48Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Dashed Stairs', 'Vanishing Arrow Wheel', 'Key'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Dashed Stairs', 'Vanishing Arrow Wheel', 'Key'}, self.player)
        else:
            return state.has_all({'Key', 'Dashed Stairs'}, self.player)

    def _48Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Dashed Stairs', 'Vanishing Arrow Wheel', 'Key'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Dashed Stairs', 'Vanishing Arrow Wheel', 'Key'}, self.player)
        else:
            return state.has_all({'Dashed Stairs', 'Key'}, self.player)

    def _48Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return self.has_midring(state) and (state.has_any({'Dashed Stairs', 'Vanishing Arrow Wheel'}, self.player))
        elif self.game_logic == "Normal":
            return self.has_midring(state) or (state.has_any({'Dashed Stairs', 'Vanishing Arrow Wheel'}, self.player))
        else:
            return True

    def _48Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return (state.has_all({'Dashed Stairs', 'Vanishing Arrow Wheel', 'Key', 'Large Spring Ball'}, self.player))
        elif self.game_logic == "Normal":
            return (state.has_all({'Dashed Stairs', 'Vanishing Arrow Wheel', 'Key', 'Large Spring Ball'}, self.player))
        else:
            return (state.has_all({'Key', 'Large Spring Ball'}, self.player))

    def _48Boss(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return (state.has('Egg Capacity Upgrade', self.player, 5))
        elif self.game_logic == "Normal":
            return (state.has('Egg Capacity Upgrade', self.player, 3))
        else:
            return (state.has('Egg Capacity Upgrade', self.player, 3))

    def _48CanFightBoss(self, state: CollectionState) -> bool:
        if state.can_reach(self.boss_order[7], 'Location', self.player):
            return True
##################################################################################################################
    def _4ECoins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Spring Ball', 'Large Spring Ball', 'Mole Tank Morph', 'Helicopter Morph', 'Flashing Eggs'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Spring Ball', 'Large Spring Ball', 'Mole Tank Morph', 'Helicopter Morph', 'Flashing Eggs'}, self.player)
        else:
            return state.has_all({'Spring Ball', 'Large Spring Ball', 'Mole Tank Morph', 'Helicopter Morph', 'Flashing Eggs'}, self.player)

    def _4EFlowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Spring Ball', 'Large Spring Ball', 'Mole Tank Morph', 'Helicopter Morph'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Spring Ball', 'Large Spring Ball', 'Mole Tank Morph', 'Helicopter Morph'}, self.player)
        else:
            return state.has_all({'Spring Ball', 'Large Spring Ball', 'Mole Tank Morph', 'Helicopter Morph'}, self.player)

    def _4EStars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Spring Ball', 'Large Spring Ball', 'Mole Tank Morph'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Spring Ball', 'Large Spring Ball', 'Mole Tank Morph'}, self.player)
        else:
            return state.has_all({'Spring Ball', 'Large Spring Ball', 'Mole Tank Morph'}, self.player)

    def _4EClear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Spring Ball', 'Large Spring Ball', 'Mole Tank Morph', 'Helicopter Morph'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Spring Ball', 'Large Spring Ball', 'Mole Tank Morph', 'Helicopter Morph'}, self.player)
        else:
            return state.has_all({'Spring Ball', 'Large Spring Ball', 'Mole Tank Morph', 'Helicopter Morph'}, self.player)
######################################################################################################################
    def _51Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Helicopter Morph', 'Dashed Stairs'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_any({'Dashed Stairs', 'Ice Melon'}, self.player) and (state.has('Egg Capacity Upgrade', self.player, 1) or self.combat_item(state) or state.has('Helicopter Morph', self.player))
        else:
            return True

    def _51Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _51Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return self.cansee_clouds(state) or ((self.has_midring(state) and state.has('Dashed Stairs', self.player)) or state.has('Tulip', self.player))
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _51Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _51Game(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Key'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Key'}, self.player)
        else:
            return state.has_all({'Key'}, self.player)
################################################################################################################
    def _52Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _52Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _52Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return self.has_midring(state) or state.has('Super Star', self.player)
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _52Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True
###########################################################################################################
    def _53Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return (state.has('Fire Melon', self.player) or self.melon_item(state)) and (state.has_all({'Bucket', 'Spring Ball', 'Super Star', 'Skis', 'Dashed Platform'}, self.player))
        elif self.game_logic == "Normal":
            return (state.has('Fire Melon', self.player) or self.melon_item(state)) and (state.has_all({'Spring Ball', 'Skis'}, self.player))  and (state.has('Super Star', self.player) or self.melon_item(state))
        else:
            return (state.has('Fire Melon', self.player) or self.melon_item(state)) and (state.has_all({'Spring Ball', 'Skis'}, self.player))  and (state.has('Super Star', self.player) or self.melon_item(state))

    def _53Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return (state.has('Fire Melon', self.player) or self.melon_item(state)) and state.has_all({'Spring Ball', 'Skis', 'Dashed Platform'}, self.player)
        elif self.game_logic == "Normal":
            return (state.has('Fire Melon', self.player) or self.melon_item(state)) and state.has_all({'Spring Ball', 'Skis'}, self.player)
        else:
            return (state.has('Fire Melon', self.player) or self.melon_item(state)) and state.has_all({'Spring Ball', 'Skis'}, self.player)

    def _53Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return (self.has_midring(state) and (state.has('Fire Melon', self.player) or self.melon_item(state))) and state.has('Spring Ball', self.player)
        elif self.game_logic == "Normal":
            return (self.has_midring(state) and (state.has('Fire Melon', self.player) or self.melon_item(state))) or (self.has_midring(state) and (state.has_all({'Tulip', 'Dashed Platform'}, self.player)))
        else:
            return (self.has_midring(state) and (state.has('Fire Melon', self.player) or self.melon_item(state))) or (self.has_midring(state) and (state.has_all({'Tulip', 'Dashed Platform'}, self.player)))

    def _53Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Spring Ball', 'Skis', 'Dashed Platform'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Spring Ball', 'Skis'}, self.player)
        else:
            return state.has_all({'Spring Ball', 'Skis'}, self.player)
##########################################################################################################
    def _54Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Dashed Stairs', 'Dashed Platform', 'Platform Ghost'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Dashed Stairs', 'Dashed Platform', 'Platform Ghost'}, self.player)
        else:
            return state.has_all({'Dashed Stairs', 'Dashed Platform', 'Platform Ghost'}, self.player)

    def _54Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Dashed Stairs', 'Platform Ghost', 'Dashed Platform'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Dashed Stairs', 'Platform Ghost', 'Dashed Platform'}, self.player)
        else:
            return state.has_all({'Dashed Stairs', 'Platform Ghost'}, self.player)

    def _54Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return ((state.has_all({'Dashed Stairs', 'Platform Ghost'}, self.player)) and self.has_midring(state)) or (self.cansee_clouds(state) and state.has('Dashed Stairs', self.player) and state.has('Dashed Platform', self.player))
        elif self.game_logic == "Normal":
            return ((state.has_all({'Dashed Stairs', 'Platform Ghost'}, self.player))) or (self.cansee_clouds(state) and state.has('Dashed Stairs', self.player))
        else:
            return True

    def _54Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return (state.has_all({'Dashed Stairs', 'Platform Ghost', 'Dashed Platform'}, self.player))
        elif self.game_logic == "Normal":
            return (state.has_all({'Dashed Stairs', 'Platform Ghost', 'Dashed Platform'}, self.player))
        else:
            return (state.has_all({'Dashed Stairs', 'Platform Ghost'}, self.player))

    def _54Boss(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return (state.has('Egg Capacity Upgrade', self.player, 2) and state.has('Egg Plant', self.player))
        elif self.game_logic == "Normal":
            return ((state.has('Egg Capacity Upgrade', self.player, 1) and state.has('Egg Plant', self.player)) or (state.has('Egg Capacity Upgrade', self.player, 5) and self.has_midring(state)))
        else:
            return ((state.has('Egg Plant', self.player)) or (state.has('Egg Capacity Upgrade', self.player, 3) and self.has_midring(state)))

    def _54CanFightBoss(self, state: CollectionState) -> bool:
        if state.can_reach(self.boss_order[8], 'Location', self.player):
            return True
###########################################################################################################
    def _55Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Helicopter Morph', '! Switch'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Helicopter Morph'}, self.player)
        else:
            return True

    def _55Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Helicopter Morph', '! Switch'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Helicopter Morph', '! Switch'}, self.player)
        else:
            return True

    def _55Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return self.has_midring(state)
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _55Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Helicopter Morph', '! Switch'}, self.player)
        elif self.game_logic == "Normal":
            return True
        else:
            return True
###########################################################################################################
    def _56Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _56Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _56Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return self.has_midring(state) or state.has('Tulip', self.player)
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _56Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True
#######################################################################################################
    def _57Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has('Egg Capacity Upgrade', self.player, 1) or self.combat_item(state)
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _57Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has('Egg Capacity Upgrade', self.player, 1) or self.combat_item(state)
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _57Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return self.has_midring(state)
        elif self.game_logic == "Normal":
            return self.has_midring(state)
        else:
            return self.has_midring(state)

    def _57Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True
###################################################################################################
    def _58Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Arrow Wheel', 'Train Morph'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Arrow Wheel', 'Train Morph'}, self.player)
        else:
            return state.has_all({'Arrow Wheel', 'Train Morph'}, self.player)

    def _58Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Arrow Wheel', 'Train Morph'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Arrow Wheel', 'Train Morph'}, self.player)
        else:
            return state.has_all({'Arrow Wheel', 'Train Morph'}, self.player)

    def _58Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return self.has_midring(state) and state.has('Arrow Wheel', self.player)
        elif self.game_logic == "Normal":
            return self.has_midring(state)
        else:
            return True

    def _58Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Arrow Wheel', 'Large Spring Ball'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Arrow Wheel', 'Large Spring Ball'}, self.player)
        else:
            return state.has_all({'Arrow Wheel', 'Large Spring Ball'}, self.player)

    def _58Boss(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _58CanFightBoss(self, state: CollectionState) -> bool:
        if state.can_reach(self.boss_order[9], 'Location', self.player):
            return True
##############################################################################################
    def _5ECoins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Key', 'Skis', 'Helicopter Morph', '! Switch'}, self.player) and self.has_midring(state)
        elif self.game_logic == "Normal":
            return state.has_all({'Key', 'Skis', 'Helicopter Morph', '! Switch'}, self.player) and self.has_midring(state)
        else:
            return state.has_all({'Key', 'Skis', 'Helicopter Morph'}, self.player)

    def _5EFlowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Key', 'Skis', 'Helicopter Morph', '! Switch'}, self.player) and self.has_midring(state)
        elif self.game_logic == "Normal":
            return state.has_all({'Key', 'Skis', 'Helicopter Morph', '! Switch'}, self.player) and self.has_midring(state)
        else:
            return state.has_all({'Key', 'Skis', 'Helicopter Morph', '! Switch'}, self.player)

    def _5EStars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'! Switch'}, self.player) and self.has_midring(state)
        elif self.game_logic == "Normal":
            return state.has_all({'! Switch'}, self.player) or self.has_midring(state)
        else:
            return state.has_all({'! Switch'}, self.player) or self.has_midring(state)

    def _5EClear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Key', 'Skis', '! Switch', 'Helicopter Morph'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Key', 'Skis', 'Helicopter Morph'}, self.player)
        else:
            return state.has_all({'Key', 'Skis', 'Helicopter Morph'}, self.player)
##################################################################################################
    def _61Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Dashed Platform', 'Large Spring Ball'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Large Spring Ball'}, self.player)
        else:
            return state.has_all({'Large Spring Ball'}, self.player)

    def _61Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Dashed Platform', 'Large Spring Ball'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Large Spring Ball'}, self.player)
        else:
            return state.has_all({'Large Spring Ball'}, self.player)

    def _61Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Dashed Platform'}, self.player) and self.has_midring(state)
        elif self.game_logic == "Normal":
            return self.has_midring(state)
        else:
            return self.has_midring(state)

    def _61Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Dashed Platform', 'Large Spring Ball'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Large Spring Ball'}, self.player)
        else:
            return state.has_all({'Large Spring Ball'}, self.player)

    def _61Game(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Dashed Platform', 'Key', 'Beanstalk'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Dashed Platform', 'Key', 'Beanstalk'}, self.player)
        else:
            return state.has_all({'Dashed Platform', 'Key', 'Beanstalk'}, self.player)
###################################################################################################
    def _62Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Super Star'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Super Star'}, self.player)
        else:
            return state.has_all({'Super Star'}, self.player)

    def _62Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Super Star'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Super Star'}, self.player)
        else:
            return state.has_all({'Super Star'}, self.player)

    def _62Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return self.cansee_clouds(state) or self.has_midring(state)
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _62Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Super Star'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Super Star'}, self.player)
        else:
            return state.has_all({'Super Star'}, self.player)
######################################################################################################
    def _63Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _63Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _63Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _63Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True
####################################################################################################
    def _64Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Spring Ball', 'Large Spring Ball', 'Egg Plant', 'Key'}, self.player) and (state.has('Egg Capacity Upgrade', self.player, 3) or self.combat_item(state))
        elif self.game_logic == "Normal":
            return state.has_all({'Large Spring Ball', 'Egg Plant', 'Key'}, self.player) and (state.has('Egg Capacity Upgrade', self.player, 2) or self.combat_item(state))
        else:
            return state.has_all({'Egg Plant', 'Key'}, self.player) and (state.has('Egg Capacity Upgrade', self.player, 1) or self.combat_item(state))

    def _64Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Spring Ball', 'Large Spring Ball', 'Egg Plant', 'Key'}, self.player) and (state.has('Egg Capacity Upgrade', self.player, 3) or self.combat_item(state))
        elif self.game_logic == "Normal":
            return state.has_all({'Large Spring Ball', 'Egg Plant', 'Key'}, self.player) and (state.has('Egg Capacity Upgrade', self.player, 2) or self.combat_item(state))
        else:
            return state.has_all({'Egg Plant', 'Key'}, self.player) and (state.has('Egg Capacity Upgrade', self.player, 1) or self.combat_item(state))

    def _64Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return self.has_midring(state) and state.has_all({'Spring Ball', 'Large Spring Ball', 'Egg Plant', 'Key'}, self.player)
        elif self.game_logic == "Normal":
            return self.has_midring(state) and state.has_all({'Spring Ball', 'Egg Plant', 'Key'}, self.player)
        else:
            return state.has('Egg Plant', self.player) and state.has('Key', self.player)

    def _64Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Spring Ball', 'Large Spring Ball', 'Egg Plant', 'Key'}, self.player) and (state.has('Egg Capacity Upgrade', self.player, 3) or self.combat_item(state))
        elif self.game_logic == "Normal":
            return state.has_all({'Large Spring Ball', 'Egg Plant', 'Key'}, self.player) and (state.has('Egg Capacity Upgrade', self.player, 2) or self.combat_item(state))
        else:
            return state.has_all({'Egg Plant', 'Key'}, self.player) and (state.has('Egg Capacity Upgrade', self.player, 1) or self.combat_item(state))

    def _64Boss(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Egg Plant'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Egg Plant'}, self.player)
        else:
            return True

    def _64CanFightBoss(self, state: CollectionState) -> bool:
        if state.can_reach(self.boss_order[10], 'Location', self.player):
            return True
###################################################################################################################
    def _65Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Chomp Rock'}, self.player) and (state.has('Egg Capacity Upgrade', self.player, 3) or self.combat_item(state))
        elif self.game_logic == "Normal":
            return state.has_all({'Chomp Rock'}, self.player) and (state.has('Egg Capacity Upgrade', self.player, 2) or self.combat_item(state))
        else:
            return state.has_all({'Chomp Rock'}, self.player)

    def _65Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Chomp Rock'}, self.player) and (state.has('Egg Capacity Upgrade', self.player, 3) or self.combat_item(state))
        elif self.game_logic == "Normal":
            return state.has_all({'Chomp Rock'}, self.player) and (state.has('Egg Capacity Upgrade', self.player, 2) or self.combat_item(state))
        else:
            return state.has_all({'Chomp Rock'}, self.player)

    def _65Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Chomp Rock'}, self.player) and (state.has('Egg Capacity Upgrade', self.player, 3) or self.combat_item(state)) and self.has_midring(state)
        elif self.game_logic == "Normal":
            return state.has_all({'Chomp Rock'}, self.player) and (state.has('Egg Capacity Upgrade', self.player, 2) or self.combat_item(state)) and self.has_midring(state)
        else:
            return state.has_all({'Chomp Rock'}, self.player) and self.has_midring(state)

    def _65Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True
#######################################################################################################################
    def _66Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Chomp Rock', 'Key', 'Large Spring Ball'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Chomp Rock', 'Key', 'Large Spring Ball'}, self.player)
        else:
            return state.has_all({'Key', 'Large Spring Ball'}, self.player) and (self.combat_item(state) or state.has('Chomp Rock', self.player))

    def _66Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Chomp Rock', 'Key', 'Large Spring Ball'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Chomp Rock', 'Key', 'Large Spring Ball'}, self.player)
        else:
            return state.has_all({'Key', 'Large Spring Ball'}, self.player) and (self.combat_item(state) or state.has('Chomp Rock', self.player))

    def _66Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Chomp Rock', 'Tulip', 'Key'}, self.player) or (self.has_midring(state) and state.has_all({'Key', 'Chomp Rock', 'Large Spring Ball'}, self.player))
        elif self.game_logic == "Normal":
            return state.has_all({'Chomp Rock', 'Tulip', 'Key'}, self.player) or (self.has_midring(state) and state.has_all({'Key', 'Chomp Rock', 'Large Spring Ball'}, self.player))
        else:
            return state.has_all({'Chomp Rock', 'Key'}, self.player)

    def _66Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Chomp Rock', 'Key', 'Large Spring Ball', 'Dashed Platform'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Chomp Rock', 'Key', 'Large Spring Ball', 'Dashed Platform'}, self.player)
        else:
            return state.has_all({'Key', 'Large Spring Ball', 'Dashed Platform'}, self.player) and (self.combat_item(state) or state.has('Chomp Rock', self.player))
###########################################################################################################################
    def _67Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return (state.has('Egg Capacity Upgrade', self.player, 1) or self.combat_item(state))
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _67Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Egg Plant'}, self.player)
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _67Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return self.has_midring(state)
        elif self.game_logic == "Normal":
            return self.has_midring(state)
        else:
            return self.has_midring(state)

    def _67Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return True
        elif self.game_logic == "Normal":
            return True
        else:
            return True

    def _67Game(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Key'}, self.player)
        elif self.game_logic == "Normal":
            return state.has_all({'Key'}, self.player)
        else:
            return state.has_all({'Key'}, self.player)
###########################################################################################################################
    def _68Coins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Helicopter Morph', 'Egg Plant'}, self.player) and self._68Route(state)
        elif self.game_logic == "Normal":
            return state.has_all({'Helicopter Morph', 'Egg Plant'}, self.player) and self._68Route(state)
        else:
            return state.has_all({'Helicopter Morph'}, self.player) and self._68Route(state)

    def _68Flowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Helicopter Morph', 'Egg Plant'}, self.player) and self._68Route(state)
        elif self.game_logic == "Normal":
            return state.has_all({'Helicopter Morph', 'Egg Plant'}, self.player) and self._68Route(state)
        else:
            return state.has_all({'Helicopter Morph'}, self.player) and self._68Route(state)

    def _68Stars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Helicopter Morph', 'Egg Plant'}, self.player) and self._68Route(state)
        elif self.game_logic == "Normal":
            return state.has_all({'Helicopter Morph', 'Egg Plant'}, self.player) and self._68Route(state)
        else:
            return state.has_all({'Helicopter Morph'}, self.player) and self._68Route(state)

    def _68Clear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return state.has_all({'Helicopter Morph', 'Egg Plant', 'Giant Eggs'}, self.player) and self._68Route(state)
        elif self.game_logic == "Normal":
            return state.has_all({'Helicopter Morph', 'Egg Plant', 'Giant Eggs'}, self.player) and self._68Route(state)
        else:
            return state.has_all({'Helicopter Morph', 'Giant Eggs'}, self.player) and self._68Route(state)
######################################################################################################################
    def _6ECoins(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return (state.has('Egg Capacity Upgrade', self.player, 2) or self.combat_item(state)) and state.has(('Large Spring Ball'), self.player)
        elif self.game_logic == "Normal":
            return (state.has('Egg Capacity Upgrade', self.player, 1) or self.combat_item(state)) and state.has(('Large Spring Ball'), self.player)
        else:
            return state.has(('Large Spring Ball'), self.player)

    def _6EFlowers(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return (state.has('Egg Capacity Upgrade', self.player, 2) or self.combat_item(state)) and state.has(('Large Spring Ball'), self.player)
        elif self.game_logic == "Normal":
            return (state.has('Egg Capacity Upgrade', self.player, 1) or self.combat_item(state)) and state.has(('Large Spring Ball'), self.player)
        else:
            return state.has(('Large Spring Ball'), self.player)

    def _6EStars(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return self.has_midring(state) and state.has(('Large Spring Ball'), self.player)
        elif self.game_logic == "Normal":
            return self.has_midring(state) or state.has(('Large Spring Ball'), self.player)
        else:
            return True

    def _6EClear(self, state: CollectionState) -> bool:
        if self.game_logic == "Easy":
            return (state.has('Egg Capacity Upgrade', self.player, 2) or self.combat_item(state)) and state.has(('Large Spring Ball'), self.player)
        elif self.game_logic == "Normal":
            return (state.has('Egg Capacity Upgrade', self.player, 1) or self.combat_item(state)) and state.has(('Large Spring Ball'), self.player)
        else:
            return state.has(('Large Spring Ball'), self.player)