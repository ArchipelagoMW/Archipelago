from typing import TYPE_CHECKING
from worlds.generic.Rules import set_rule, CollectionRule
from . import RuleUtils

if TYPE_CHECKING:
    from . import MinitWorld
else:
    MinitWorld = object


class MinitRules:
    world: MinitWorld
    player: int
    darkrooms: int
    region_rules: dict[str, CollectionRule]

    location_rules: dict[str, CollectionRule]

    def __init__(self, world: MinitWorld) -> None:
        self.world = world
        self.player = world.player
        self.darkrooms = self.world.options.darkrooms

        self.region_rules = {
            "Menu -> Dog House": lambda state:
                True,
            "Dog House -> Island Shack": lambda state:
                (state.has_all({
                    "has_sword",
                    "ItemBoat",
                    "boatguy watered",
                    "ItemGlove",
                    }, self.player)),
                # obscure: you can swim from treasure island
                # - by baiting the shark
            "Dog House -> Desert RV": lambda state:
                (state.has("has_sword", self.player) and
                    (RuleUtils.has_darkroom(self.player, state, 2, self.darkrooms)
                     or state.has("ItemGlove", self.player)))
                or state.has("ItemSwim", self.player),
            "Dog House -> Hotel Room": lambda state:
                (state.has("has_sword", self.player)
                 and state.has("ItemGlove", self.player))
                or state.has("ItemSwim", self.player),
            "Island Shack -> Basement": lambda state:
                state.has("has_sword", self.player)
                and state.has("ItemBasement", self.player),
            "Desert RV -> Factory Main": lambda state:
                state.has("has_sword", self.player)
                and (state.has("ItemGrinder", self.player)
                     or state.has_all({
                        "ItemSwim", # damage boost
                        "ItemCoffee"
                        }, self.player)),
            "Hotel Room -> Underground Tent": lambda state:
                state.has("has_sword", self.player)
                and RuleUtils.has_darkroom(self.player, state, 3, self.darkrooms)
                and state.has("ItemGrinder", self.player),
            "Hotel Room -> Factory Main": lambda state:
                (RuleUtils.has_darkroom(self.player, state, 2, self.darkrooms)
                    and state.has("ItemSwim", self.player)
                )
                or (
                    state.has("has_sword", self.player) # obscure: shoes instead of sword (Precise movement to squeeze through the destroyables)
                    and state.has("ItemPressPass", self.player)
                    and (state.has("bombs exploded", self.player)
                         or state.has("ItemSwim", self.player) # damage boost
                        )
                ),
            "Factory Main -> Boss Fight": lambda state:
                RuleUtils.has_darkroom(self.player, state, 2, self.darkrooms)
                and RuleUtils.has_megasword(self.player, state),
            "Factory Main -> Hotel Room": lambda state:
                self.factory_to_hotel_backtrack(state),
        }

        self.location_rules = {

            # Dog House
            "Dog House - ItemCoffee": lambda state:
                state.has("has_sword", self.player),
            "Dog House - ItemFlashLight": lambda state:
                ((
                  state.has("has_sword", self.player)
                  or state.has("ItemSwim", self.player))
                 and state.has("ItemKey", self.player)),
                # obscure: you can swim behind the lighthouse
                # - and pick up the item
            "Dog House - ItemKey": lambda state:
                state.has("has_sword", self.player) and RuleUtils.can_passBoxes(self.player, state),
                # can swim past the plants,
                # but need to clear the plants by the boxes
            "Dog House - ItemWateringCan": lambda state:
                state.has("has_sword", self.player),
            "Dog house - ItemBoat": lambda state:
                state.has("has_sword", self.player) and state.has("ItemGlove", self.player),
            "Dog House - ItemBasement": lambda state:
                state.has("has_sword", self.player) and state.has("ItemGlove", self.player)
                and (state.has_all({
                        "ItemBoat",
                        "boatguy watered",
                        "ItemGlove",
                        }, self.player)),
                # obscure: you can swim from treasure island
                # - by baiting the shark
            "Dog House - ItemPressPass": lambda state:
                (
                    (RuleUtils.can_passBoxes(self.player, state)
                        and ((state.has("has_sword", self.player)
                              and state.has("ItemThrow", self.player))
                             or state.has("ItemSwim", self.player))) # damage boost
                    or (state.has("has_sword", self.player)
                        and state.can_reach("Hotel Room", player=self.player)
                        and (state.has_all({
                                "ItemGrinder",
                                "ItemGlove"
                                }, self.player)))),
                # obscure: you can, with clean movement and damage tanks,
                # - swim from the factory bridge to press pass house
                # - without any other items
            "Dog House - House Pot Coin": lambda state:
                state.has("has_sword", self.player),
            "Dog House - Sewer Island Coin": lambda state:
                state.has("has_sword", self.player) and RuleUtils.has_darkroom(self.player, state, 3, self.darkrooms)
                and RuleUtils.can_openChest(self.player, state),
            "Dog House - Sewer Coin": lambda state:
                state.has("has_sword", self.player) and RuleUtils.has_darkroom(self.player, state, 3, self.darkrooms)
                and RuleUtils.can_openChest(self.player, state)
                and state.has("ItemSwim", self.player),
            "Dog House - Land is Great Coin": lambda state:
                RuleUtils.can_openChest(self.player, state)
                and ((
                        state.has("has_sword", self.player)
                        and state.has("ItemCoffee", self.player))
                     or state.has("ItemSwim", self.player)),
            "Dog House - Hidden Snake Coin": lambda state:
                (state.has("has_sword", self.player) or state.has("ItemSwim", self.player))
                and RuleUtils.has_darkroom(self.player, state, 2, self.darkrooms) and RuleUtils.can_openChest(self.player, state),
            "Dog House - Waterfall Coin": lambda state:
                RuleUtils.can_openChest(self.player, state)
                and state.has("ItemSwim", self.player),
            "Dog House - Treasure Island Coin": lambda state:
                RuleUtils.can_openChest(self.player, state)
                and state.has("ItemSwim", self.player),
            "Dog House - Plant Heart": lambda state:
                state.has("ItemWateringCan", self.player),
            "Dog House - Bull Heart": lambda state:
                state.has("has_sword", self.player)
                and (state.can_reach("Desert RV", player=self.player)
                     or RuleUtils.has_darkroom(self.player, state, 2, self.darkrooms)),
            "Dog House - Boat Tentacle": lambda state:
                state.has("has_sword", self.player)
                and state.has_all({
                    "ItemBoat",
                    "boatguy watered",
                    "ItemGlove",
                    }, self.player),
            "Dog House - Treasure Island Tentacle": lambda state:
                state.has("has_sword", self.player) and state.has("ItemSwim", self.player),
            "Dog House - Sword Toss Tentacle": lambda state:
                state.has("has_sword", self.player)
                and state.has_all({
                    "ItemCoffee",
                    "ItemThrow",
                    "ItemGlove",
                    }, self.player),
            "Dog House - Sewer Tentacle": lambda state:
                state.has("has_sword", self.player) and RuleUtils.has_darkroom(self.player, state, 3, self.darkrooms)
                and state.has("ItemSwim", self.player),
            "Dog House - Dolphin Heart": lambda state:
                state.has("ItemWateringCan", self.player),
                # Non Vanilla Location: water the dolphin NPC
                # -  south of the watering can location

            # Desert RV
            "Desert RV - ItemThrow": lambda state:
                state.has("has_sword", self.player),
            "Desert RV - ItemShoes": lambda state:
                state.has("Coin", self.player, 7),
            "Desert RV - ItemGlove": lambda state:
                (state.has("has_sword", self.player)
                    and state.has("ItemGlove", self.player))
                or state.has_any({
                    "ItemWateringCan",
                    "ItemSwim",
                    }, self.player),
            "Desert RV - ItemTurboInk": lambda state:
                RuleUtils.has_darkroom(self.player, state, 2, self.darkrooms) and state.has("Tentacle", self.player, 8),
            "Desert RV - Temple Coin": lambda state:
                state.has("has_sword", self.player) and RuleUtils.has_darkroom(self.player, state, 2, self.darkrooms)
                and ((
                        state.can_reach("Hotel Room", player=self.player)
                        and state.has_all({
                            "teleporter switch1",
                            "teleporter switch4",
                            "teleporter switch6",
                            "ItemBasement",
                            }, self.player))
                     ),
                # item region implies desert rv access, can teleport implies
                # - island shack access, existing implies dog house access,
                # - only need to check hotel room access
            "Desert RV - Fire Bat Coin": lambda state:
                RuleUtils.has_darkroom(self.player, state, 1, self.darkrooms) and RuleUtils.can_openChest(self.player, state)
                and state.has("ItemWateringCan", self.player),
            "Desert RV - Truck Supplies Coin": lambda state:
                state.has("has_sword", self.player) and RuleUtils.can_openChest(self.player, state),
            "Desert RV - Broken Truck": lambda state:
                RuleUtils.can_openChest(self.player, state),
            "Desert RV - Quicksand Coin": lambda state:
                state.has("has_sword", self.player) and RuleUtils.has_darkroom(self.player, state, 2, self.darkrooms),
                # vanilla does require sword because the wateringcan drops
                # - while drowing in quicksand
            "Desert RV - Dumpster": lambda state:
                state.has("has_sword", self.player),
            "Desert RV - Temple Heart": lambda state:
                RuleUtils.has_darkroom(self.player, state, 3, self.darkrooms)
                and state.has("ItemShoes", self.player),
            "Desert RV - Shop Heart": lambda state:
                state.has("ItemBasement", self.player)
                and state.has("Coin", self.player, 19),
            "Desert RV - Octopus Tentacle": lambda state:
                state.has("has_sword", self.player) and RuleUtils.has_darkroom(self.player, state, 2, self.darkrooms)
                and state.has("ItemSwim", self.player),
            "Desert RV - Beach Tentacle": lambda state:
                state.has("has_sword", self.player),
                # redundant rules as swim gets us to the right region anyways
                # or (self.region_DogHouse(state)
                #     and state.has("has_sword", self.player)
                #     and state.has("ItemSwim", self.player)),

            # Hotel Room
            "Hotel Room - ItemSwim": lambda state:
                state.has_all({
                    "swimmer saved",
                    "hostage saved",
                    "wallet saved",
                    "ninja saved",
                    "bridge saved",
                    "hidden saved",
                    }, self.player),
            "Hotel Room - ItemGrinder": lambda state:
                RuleUtils.has_darkroom(self.player, state, 2, self.darkrooms)
                and state.has_all({
                    "ItemSwim",
                    "ItemCoffee"
                    }, self.player),
            "Hotel Room - Shrub Arena Coin": lambda state:
                state.has("has_sword", self.player),
            "Hotel Room - Miner's Chest Coin": lambda state:
                state.has("has_sword", self.player) and RuleUtils.has_darkroom(self.player, state, 3, self.darkrooms)
                and RuleUtils.can_openChest(self.player, state)
                and state.has("ItemGrinder", self.player),
            "Factory Main - Inside Truck": lambda state:
                True,
            "Hotel Room - Queue": lambda state:
                self.factory_to_hotel_backtrack(state)
                or state.has_any({"ItemSwim", "bridge on", "bombs exploded"}, self.player), # swim only uses damage boost
            "Hotel Room - Hotel Backroom Coin": lambda state:
                RuleUtils.can_passBoxes(self.player, state) and state.has("has_sword", self.player),
                # can be done without sword due to a bug
            "Factory Main - Drill Coin": lambda state:
                state.has("has_sword", self.player)
                and state.has("drill smacked", self.player),
            "Hotel Room - Crow Heart": lambda state:
                state.has("has_sword", self.player)
                and RuleUtils.can_passBoxes(self.player, state)
                and state.has("ItemGlove", self.player),
            "Hotel Room - Dog Heart": lambda state:
                state.has("has_sword", self.player) and state.has("ItemGlove", self.player)
                and (state.has_any({
                        "ItemSwim",
                        "ItemShoes"
                        }, self.player)
                     or state.has_all({
                            "teleporter switch1",
                            "teleporter switch4",
                            "teleporter switch6",
                            "ItemBasement",
                            }, self.player)),
                # obscure: with good movemnt can do this in 50s
                # -  with just sword glove, adding teleport/swim/shoes
                # - to give more wiggle room outside obscure logic
                # this logic changes if i rando the bone,
                # - don't think i will though

            # Island Shack
            "Island Shack - Teleporter Tentacle": lambda state:
                state.has("has_sword", self.player)
                and (state.has("ItemCoffee", self.player))
                and state.has_all({
                        "ItemBasement",
                        "ItemSwim",
                        }, self.player),
                # obscure: attacking in coyote frames from the right teleporter
                # - lets you do this with just sword/swim

            # Underground Tent
            "Underground Tent - ItemTrophy": lambda state:
                state.has("ItemSwim", self.player),

            # Factory Main
            "Factory Main - ItemMegaSword": lambda state:
                state.has("has_sword", self.player)
                and RuleUtils.has_darkroom(self.player, state, 1, self.darkrooms)
                and state.has_all({
                    "ItemWateringCan",
                    "left machine",
                    "right machine",
                    "generator smashed",
                    }, self.player),
            "Factory Main - Cooler Tentacle": lambda state:
                state.has("has_sword", self.player),

            # events
            "generator smashed": lambda state:
                state.has("has_sword", self.player),
            "drill smacked": lambda state:
                state.has("generator smashed", self.player)
                and state.has("has_sword", self.player),
            "swimmer saved": lambda state:
                True,
            "hostage saved": lambda state:
                state.has("has_sword", self.player),
            "wallet saved": lambda state:
                state.has("has_sword", self.player)
                and state.has_all({
                    "ItemCoffee",
                    "ItemGlove"
                    }, self.player),
            "ninja saved": lambda state:
                state.has("has_sword", self.player) and state.has("ItemGlove", self.player),
            "bridge on": lambda state:
                state.has("has_sword", self.player)
                and (
                     state.has("ItemSwim", self.player) # damage boost
                     or state.has("bombs exploded", self.player)
                     or self.factory_to_hotel_backtrack(state)
                ),
            "bridge saved": lambda state:
                state.has("bridge on", self.player),
            "hidden saved": lambda state:
                RuleUtils.can_passBoxes(self.player, state),
            "teleporter switch1": lambda state:
                state.has("has_sword", self.player),
            "teleporter switch4": lambda state:
                state.has("has_sword", self.player)
                and state.has_any({
                    "ItemSwim",
                    "ItemCoffee"
                    }, self.player),
            "teleporter switch6": lambda state:
                state.has("has_sword", self.player)
                and state.has_any({
                    "ItemSwim",
                    "ItemCoffee"
                    }, self.player),
            "boatguy watered": lambda state:
                state.has("ItemWateringCan", self.player),
            "left machine": lambda state:
                RuleUtils.has_darkroom(self.player, state, 1, self.darkrooms)
                and state.has_all({
                    "ItemCoffee",
                    "ItemSwim"
                    }, self.player),
            "right machine": lambda state:
                state.has("has_sword", self.player),
            "bombs exploded": lambda state:
                state.has("has_sword", self.player)
                and state.has("ItemThrow", self.player)
                and RuleUtils.has_darkroom(self.player, state, 2, self.darkrooms),
        }

        obscure = {
            "Dog House -> Island Shack": lambda state:
                state.has("ItemSwim", self.player)
                or (state.has_all({
                    "has_sword",
                    "ItemBoat",
                    "boatguy watered",
                    "ItemGlove",
                    }, self.player)),
                # obscure: you can swim from treasure island
                # - by baiting the shark
            "Hotel Room -> Factory Main": lambda state:
                RuleUtils.has_darkroom(self.player, state, 2, self.darkrooms)
                and state.has("ItemSwim", self.player)
                or (
                    (state.has("has_sword", self.player) or state.has("ItemShoes", self.player))
                    and state.has("ItemPressPass", self.player)
                    and (state.has("bombs exploded", self.player)
                         or state.has("ItemSwim", self.player) # damage boost
                        )
                ),
                # obscure: you can squeeze through the destroyables with shoes and precise movement
            "Dog House - ItemFlashLight": lambda state:
                state.has("ItemSwim", self.player)
                or state.has("has_sword", self.player)
                and state.has("ItemKey", self.player),
                # obscure: you can swim behind the lighthouse
                # - and pick up the item
            "Dog House - ItemBasement": lambda state:
                state.has("has_sword", self.player) and state.has("ItemGlove", self.player)
                and ((state.has("ItemSwim", self.player))
                     or state.has_all({
                        "ItemBoat",
                        "boatguy watered",
                        "ItemGlove",
                        }, self.player)),
                # obscure: you can swim from treasure island
                # - by baiting the shark
            "Hotel Room - Dog Heart": lambda state:
                state.has("has_sword", self.player) and state.has("ItemGlove", self.player),
                # obscure: with good movemnt can do this in 50s
                # -  with just sword glove, adding teleport/swim/shoes
                # - to give more wiggle room outside obscure logic
                # this logic changes if i rando the bone,
                # - don't think i will though

            "Island Shack - Teleporter Tentacle": lambda state:
                state.has("has_sword", self.player)
                and state.has_all({
                        "ItemBasement",
                        "ItemSwim",
                        }, self.player),
                # obscure: attacking in coyote frames from the right teleporter
                # - lets you do this with just sword/swim


            # assume other logic is off and they can get replaced later
            "Desert RV - Temple Coin": lambda state:
                state.has("has_sword", self.player) and RuleUtils.has_darkroom(self.player, state, 2, self.darkrooms)
                and ((
                        state.can_reach("Hotel Room", player=self.player)
                        and state.has_all({
                            "teleporter switch1",
                            "teleporter switch4",
                            "teleporter switch6",
                            "ItemBasement",
                            }, self.player))
                     or (state.has("ItemSwim", self.player)
                         # sword+darkroom+swim should cover the hotel -> temple route
                         )
                     ),
                # item region implies desert rv access, can teleport implies
                # - island shack access, existing implies dog house access,
                # - only need to check hotel room access
            "Dog House - ItemPressPass": lambda state:
                (
                    (RuleUtils.can_passBoxes(self.player, state)
                        and ((state.has("has_sword", self.player)
                              and state.has("ItemThrow", self.player))
                             or state.has("ItemSwim", self.player))) # damage boost
                    or (state.has("has_sword", self.player)
                        and state.can_reach("Hotel Room", player=self.player)
                        and (state.has_all({
                                "ItemGrinder",
                                "ItemGlove"
                                }, self.player)))),
                # obscure: you can, with clean movement and damage tanks,
                # - swim from the factory bridge to press pass house
                # - without any other items
        }

        damage_boost_obscure = {
            "Dog House - ItemPressPass": lambda state:
                RuleUtils.can_passBoxes(self.player, state)
                and (
                    state.has("has_sword", self.player)
                    and state.has("ItemThrow", self.player)
                    or state.has("ItemSwim", self.player)
                )
                or state.has_all({"has_sword", "ItemGrinder", "ItemGlove"}, self.player) # Tile movement from dog house: L U U U R (Glove used at 3 crab and before press house. Grinder used at box going toward press house.)
                or RuleUtils.total_hearts(self.player, state, 4)
                and state.has("ItemSwim", self.player)
                and state.has("has_sword", self.player) # dog house: L L U R U R U (sword to cut grass to enter toxic river on way to press house)
                or RuleUtils.total_hearts(self.player, state, 7)
                and state.has("ItemSwim", self.player), # Hotel Access is required but implied by having Swim
                # obscure: you can, with clean movement and damage tanks,
                # - swim from the factory bridge to press pass house
                # - without any other items
        }

        # darkroom: = {
        #     "Dog House -> Desert RV": lambda state: True or False,
        #     "Hotel Room -> Underground Tent": lambda state: True or False,
        #     "Hotel Room -> Factory Main": lambda state: True or False,
        #     "Factory Main -> Boss Fight": lambda state: True or False,
        #     "Dog House - Sewer Island Coin": lambda state: True or False,
        #     "Dog House - Sewer Coin": lambda state: True or False,
        #     "Dog House - Hidden Snake Coin": lambda state: True or False,
        #     "Dog House - Bull Heart": lambda state: True or False,
        #     "Dog House - Sewer Tentacle": lambda state: True or False,
        #     "Desert RV - ItemTurboInk": lambda state: True or False,
        #     "Desert RV - Fire Bat Coin": lambda state: True or False,
        #     "Desert RV - Quicksand Coin": lambda state: True or False,
        #     "Desert RV - Temple Heart": lambda state: True or False,
        #     "Desert RV - Octopus Tentacle": lambda state: True or False,
        #     "Hotel Room - ItemGrinder": lambda state: True or False,
        #     "Hotel Room - Miner's Chest Coin": lambda state: True or False,
        #     "Factory Main - ItemMegaSword": lambda state: True or False,
        #     "bridge on": lambda state: True or False,
        #     "left machine": lambda state: True or False,
        # }

        # darkroom_obscure: = {
        #     "Desert RV - Temple Coin": lambda state, obscure=self.world.options.obscure: True or False,
        # }

        def apply_rules(optional_rules):
            for key, rule in optional_rules.items():
                if key in self.region_rules:
                    self.region_rules[key] = rule
                else:
                    self.location_rules[key] = rule

        if self.world.options.obscure:
            apply_rules(obscure)

            if self.world.options.obscure and self.world.options.damage_boosts:
                apply_rules(damage_boost_obscure)

        # if self.world.options.dark_room:
        #     apply_rules(darkroom)

        #     if self.world.options.obscure and self.world.options.dark_room:
        #         apply_rules(darkroom_obscure)

    def factory_to_hotel_backtrack(self, state) -> bool:
        return (state.can_reach("Factory Main", player=self.player)
                and state.has("has_sword", self.player)
                and state.has("ItemPressPass", self.player))

    def set_Minit_rules(self) -> None:
        multiworld = self.world.multiworld
        # if option: change relevant rules

        for region in multiworld.get_regions(self.player):
            for entrance in region.entrances:
                if entrance.name in self.region_rules:
                    set_rule(entrance, self.region_rules[entrance.name])
            for location in region.locations:
                if location.name in self.location_rules:
                    set_rule(location, self.location_rules[location.name])
