from typing import TYPE_CHECKING
from worlds.generic.Rules import set_rule, CollectionRule
from . import RuleUtils

if TYPE_CHECKING:
    from . import MinitWorld
else:
    MinitWorld = object


class ER_MinitRules:
    world: MinitWorld
    player: int
    darkrooms: int
    region_rules: dict[str, CollectionRule]

    location_rules: dict[str, CollectionRule]

    helpers: dict[str, CollectionRule]

    def __init__(self, world: MinitWorld) -> None:
        self.world = world
        self.player = world.player
        self.darkrooms = self.world.options.darkrooms

        self.helpers = {
            "swim": lambda state: state.has("ItemSwim", self.player),
            "darkroom1": lambda state: RuleUtils.has_darkroom(self.player, state, 1, self.darkrooms),
            "darkroom2": lambda state: RuleUtils.has_darkroom(self.player, state, 2, self.darkrooms),
            "darkroom3": lambda state: RuleUtils.has_darkroom(self.player, state, 3, self.darkrooms),
            "sword": lambda state: state.has("has_sword", self.player),
            "wateringcan": lambda state: state.has("ItemWateringCan", self.player),
            "presspass": lambda state: state.has("ItemPressPass", self.player),
            "basement": lambda state: state.has("ItemBasement", self.player),
            "tree": lambda state: state.has("has_sword", self.player) and state.has("ItemGlove", self.player),
            "chest": lambda state: RuleUtils.can_openChest(self.player, state),
            "box": lambda state: RuleUtils.can_passBoxes(self.player, state),
            "teleport": lambda state: state.has_all({"teleporter switch1", "teleporter switch4", "teleporter switch6",}, self.player),
            }

        self.region_rules = {
            # "Menu -> sword main": lambda state: True,
            "factory machine catwalk -> Boss Fight": lambda state:
                self.helpers["darkroom2"](state) and RuleUtils.has_megasword(self.player, state),
            "Boss Fight -> factory machine catwalk": lambda state: False,
            "factory machine generator -> Boss Fight": lambda state:
                self.helpers["darkroom2"](state) and RuleUtils.has_megasword(self.player, state),
            "Boss Fight -> factory machine generator": lambda state: False,
            "2crab tree exit <-> 2crab tile": lambda state: 
                self.helpers["tree"](state)
                or self.helpers["swim"](state),
            "boat tile -> Overworld island shack": lambda state: 
                state.has_all({
                    "ItemBoat",
                    "boatguy watered",
                    "ItemGlove",
                    }, self.player),
            "Overworld island shack -> boat tile": lambda state: False,
            # "coffee shop outside <-> coffee shop inside": lambda state: True,
            "quicksand left tree <-> quicksand main":  self.helpers["tree"],
                # technically an option to not have glove and water boatguy but
                # that adds weird issues so i'll just leave it as out of logic
            "quicksand right tree <-> quicksand main":  self.helpers["tree"],
            "factory drill <-> quicksand main": lambda state: state.has("drill smacked", self.player),
            "boattree box <-> boattree main":  self.helpers["box"],
            "camera river south -> camera river north": lambda state:
                self.helpers["sword"](state) and state.has("ItemThrow", self.player),
            "camera river north -> camera river south": self.helpers["sword"],
                # obscure: requires nothing
            "camera house tree <-> camera house outside":  self.helpers["tree"],
            # "camera house outside <-> camera house inside": lambda state: True,
            "3crab trees <-> 3crab main":  self.helpers["tree"],
            "throwcheck tile -> throwcheck box": lambda state:
                self.helpers["sword"](state)
                and state.has("ItemGrinder", self.player),
                # TODO: this currently allows for throw check to be in logic without being possible. It might make sense to make going this way out of logic to fix that.
            "throwcheck box -> throwcheck tile":  self.helpers["box"],
                # could be a oneway with coffee but i'll think about that later
            "arena tree north <-> arena tile":  self.helpers["tree"],
            "arena tree west <-> arena tile":  self.helpers["tree"],
            "bridge left <-> bridge right": lambda state:
                state.has("bridge on", self.player),  # need to confirm this works
            "factory loading lower main <-> factory loading lower shortcut": lambda state:
                self.helpers["sword"](state)
                and state.has("ItemGrinder", self.player),
                # damage boosting out of logic
            "mine entrance pipe <-> mine entrance bombs": lambda state:
                self.helpers["darkroom3"](state)
                and state.has("bombs exploded", self.player),
            "mine main -> mine main box": lambda state:
                self.helpers["sword"](state)
                and state.has("ItemGrinder", self.player),
            "mine main box -> mine main":  self.helpers["box"],
            "sewer main right north <-> sewer main":  self.helpers["darkroom2"],
            "sewer main left <-> sewer main": lambda state:
                self.helpers["darkroom2"](state)
                and self.helpers["swim"](state),
            "sewer bat arena -> sewer bat gate": lambda state:
                self.helpers["sword"](state)
                and self.helpers["darkroom3"](state),
                # this needs to be a one-way as the bats respawn
            "sewer bat gate -> sewer bat arena": lambda state: False,
            "grinder south": lambda state:
                self.helpers["darkroom1"](state)
                and self.helpers["swim"](state),
            "grinder east": lambda state:
                self.helpers["darkroom1"](state)  # maybe 2
                and self.helpers["swim"](state),
            "factory machine generator <-> factory machine catwalk": lambda state:
                state.has("generator smashed", self.player),
            "miner chest pipe entrance <-> miner chest tile": lambda state:
                self.helpers["darkroom3"](state)
                and self.helpers["swim"](state),
                # TODO: Better damage boosting logic
                # This is the only instance of allowed damage boosting. The reason for this is because this path is only possible through damage boosting and is a path that is required to be taken, through damage boosting, in vanilla.
                # Anyway, it's possible for this to cause logic problems if it needs to be passed through multiple times in one run.
                # For example, if you needed to pass through here to get to the set of 3 crabs and then needed to travel back through here before you could claim the coffee location, it may be impossible due to the damage taken

            # unrandomized doors
            "lighthouse inside <-> lighthouse": lambda state: 
                state.has("ItemKey", self.player),
            "lighthouse lookout -> lighthouse": lambda state: False,
            "lighthouse -> lighthouse lookout": lambda state: False,
                # obscure: you can swim and grab it from beneath
            # "lighthouse inside -> lighthouse lookout": lambda state: True,
            "lighthouse lookout -> lighthouse inside": lambda state: False,
            "coffee shop pot stairs <-> sewer main":  self.helpers["darkroom2"],  # maybe 3
            # "dog house inside <-> dog house west": lambda state: True,
            # "glove outside <-> glove inside": lambda state: True,
            "boattree main <-> waterfall cave":  self.helpers["swim"],
            # "hotel outside <-> hotel reception": lambda state: True,
            # "hotel outside <-> hotel backroom": lambda state: True,
            # "hotel reception <-> hotel room": lambda state: True,
            # "mine entrance right <-> mine entrance pipe": lambda state: True,
            # "factory loading upper <-> factory snakehall": lambda state: True,
            # "shoe shop inside <-> shoe shop outside": lambda state: True,
            # "desert RV main <-> RV house": lambda state: True,
            "Overworld treasure island <-> Overworld island shack": lambda state: False,
                # obscure: you can swim accross
            "island house -> Overworld island shack": lambda state: True,
            "Overworld island shack -> island house": self.helpers["sword"],
            "island house -> island teleporter": lambda state:
                self.helpers["basement"](state) and self.helpers["darkroom1"](state),
            "island teleporter -> island house": self.helpers["darkroom1"],
            "island teleporter east":  self.helpers["darkroom1"],
            # "tent room main <-> underground house": lambda state: True,
            # "factory mega entrance <-> factory central": lambda state: True,
            "factory mega entrance <-> megasword upper": lambda state:
                state.has("generator smashed", self.player) and self.helpers["darkroom1"](state),
            "factory central south <-> factory central": lambda state:
                state.has("generator smashed", self.player),
            "dog house basement <-> hotel room": lambda state: 
                self.helpers["teleport"](state)
                and state.can_reach("hotel room", player=self.player),
            "dog house basement <-> shoe shop downstairs": lambda state: 
                self.helpers["teleport"](state)
                and state.can_reach("shoe shop downstairs", player=self.player),
            "temple coin test north": lambda state: 
                state.can_reach("dog house inside", player=self.player)
                and state.can_reach("RV house", player=self.player)
                and state.can_reach("hotel room", player=self.player)
                and state.can_reach("island house", player=self.player)
                and self.helpers["darkroom3"](state),
            "temple coin test south": lambda state: 
                state.can_reach("dog house inside", player=self.player)
                and state.can_reach("RV house", player=self.player)
                and state.can_reach("hotel room", player=self.player)
                and state.can_reach("island house", player=self.player)
                and self.helpers["darkroom3"](state),

            # # only swims
            "lighthouse water upper west":  self.helpers["swim"],
            "lighthouse water upper north":  self.helpers["swim"],
            "lighthouse water upper east":  self.helpers["swim"],
            "lighthouse water lower west":  self.helpers["swim"],
            "lighthouse water lower south":  self.helpers["swim"],
            "lighthouse water lower east":  self.helpers["swim"],
            "boat water south":  self.helpers["swim"],
            "boat water east":  self.helpers["swim"],
            "boat water north":  self.helpers["swim"],
            "boat water west":  self.helpers["swim"],
            "sword east <-> sword water":  self.helpers["swim"],
            "2crab land north river":  self.helpers["swim"],
            "2crab water east":  self.helpers["swim"],
            "2crab water south":  self.helpers["swim"],
            "2crab water west":  self.helpers["swim"],
            "dolphin water east":  self.helpers["swim"],
            "dolphin water south":  self.helpers["swim"],
            "dolphin water west":  self.helpers["swim"],
            "desert beach water south":  self.helpers["swim"],
            "desert beach water west":  self.helpers["swim"],
            "coffee shop water north":  self.helpers["swim"],
            "coffee shop water west":  self.helpers["swim"],
            "coffee shop water south":  self.helpers["swim"],
            "coffee shop upper beach -> coffee shop outside": self.helpers["swim"],
            "coffee shop outside -> coffee shop upper beach": lambda state: 
                self.helpers["swim"](state)
                or state.has("ItemCoffee", self.player)
                and self.helpers["sword"](state),
                # obscure: coffee without sword

            "above lighthouse water north":  self.helpers["swim"],
            "above lighthouse water east upper":  self.helpers["swim"],
            "above lighthouse water east lower":  self.helpers["swim"],
            "above lighthouse water south":  self.helpers["swim"],
            "above lighthouse water west":  self.helpers["swim"],

            "dog house west <-> dog house east":  self.helpers["swim"],
            "dog house river north":  self.helpers["swim"],
            "dog house river south":  self.helpers["swim"],

            "boattree river south":  self.helpers["swim"],
            "3crab north water north":  self.helpers["swim"],
            "3crab north water west":  self.helpers["swim"],
            "3crab south water west":  self.helpers["swim"],
            "3crab south water south":  self.helpers["swim"],
            "sewer island water north":  self.helpers["swim"],
            "sewer island water south":  self.helpers["swim"],
            "sewer island water west":  self.helpers["swim"],
            "throwcheck water south":  self.helpers["swim"],
            "throwcheck water west":  self.helpers["swim"],
            "Overworld wet06": self.helpers["swim"],
            "bridge switch left <-> bridge switch right":  lambda state: False, # damage boosting is out of logic

            # # toxic waters

            "sewer island tile -> toxic waters": lambda state: 
                self.helpers["swim"](state)
                and self.helpers["sword"](state),
            "toxic waters -> sewer island tile": lambda state: False,
            "camera river south -> camera river wet": self.helpers["swim"],
            "camera river wet -> camera river south": lambda state: False,
            "mine entrance left -> toxic waters": self.helpers["swim"],
            "toxic waters -> mine entrance left": lambda state: False,
            "bridge left -> toxic waters": self.helpers["swim"],
            "toxic waters -> bridge left": lambda state: False,
            "bridge switch left -> toxic waters": self.helpers["swim"],
            "toxic waters -> bridge switch left": lambda state: False,

            # This logic is here so that the generic entrance randomizer doesn't crash randomizing toxic water connections with eachother when they aren't logically useful.
            # This logic says that you can enter the toxic waters, but you cannot exit, making it useless for logic.


            "temple octopus north": lambda state:
                self.helpers["swim"](state)
                and self.helpers["darkroom3"](state),

            # # darkroom only
            "submarine east":  self.helpers["darkroom1"],
            "submarine west":  self.helpers["darkroom1"],
            "teleporter maze west":  self.helpers["darkroom1"], # not doing it's job, but it feels unnecessary anyway: It's still in logic to come from the west without flashlight for some reason
            "mine main north":  self.helpers["darkroom1"],
            "mine main west upper": self.helpers["darkroom1"], # so that regions don't have to be added to enforce darkroom rules on mine main north and mine main west lower
            "mine main west lower":  self.helpers["darkroom1"],
            "mine main box": self.helpers["darkroom1"], # so that regions don't have to be added to enforce darkroom rules on mine main north and mine main west lower
            "factory switch test west":  self.helpers["darkroom1"],
            "factory switch test south":  self.helpers["darkroom1"],
            "dog house basement <-> island teleporter":  lambda state: 
                self.helpers["teleport"](state)
                and state.can_reach("island teleporter", player=self.player)
                and self.helpers["darkroom1"],

            "snake east <-> boattree east":  self.helpers["darkroom2"],
            "snake east <-> boattree main":  self.helpers["darkroom2"],
            "snake east path":  self.helpers["darkroom2"],
            "sewer island <-> sewer upper":  self.helpers["darkroom2"],
            "temple outside <-> temple main":  self.helpers["darkroom2"],
            "mine entrance left <-> mine entrance path":  self.helpers["darkroom2"],
            "tent room pipe I right":  self.helpers["darkroom2"],
            "tent room pipe I left":  self.helpers["darkroom2"],
            "tent room main right":  self.helpers["darkroom2"], # changed from 1 to 2 since you'd always travel across
            "tent room main left":  self.helpers["darkroom2"],

            "tent room pipe O":  self.helpers["darkroom3"],
            "temple octopus main": self.helpers["darkroom3"],
            "miner chest pipe L south":  self.helpers["darkroom3"],
            "miner chest pipe L west":  self.helpers["darkroom3"],
            "trophy pipe hall right":  self.helpers["darkroom3"],
            "trophy pipe hall left":  self.helpers["darkroom3"],
            "trophy maze lower main north right":  self.helpers["darkroom3"],
            "trophy maze lower main north left":  self.helpers["darkroom3"],
            "trophy maze lower main east right":  self.helpers["darkroom3"], # east upper
            "trophy maze lower main east left":  self.helpers["darkroom3"], # east lower
            "trophy maze lower hall left":  self.helpers["darkroom3"],
            "trophy maze lower hall right":  self.helpers["darkroom3"],
            "trophy maze upper main right":  self.helpers["darkroom3"],
            "trophy maze upper main left":  self.helpers["darkroom3"],
            "trophy maze upper hall south":  self.helpers["darkroom3"],
            "trophy maze upper hall west":  self.helpers["darkroom3"],

            # # sword
            "sword east <-> sword west": self.helpers["sword"],
            "dolphin bushes":  self.helpers["sword"],
            "dog house bushes <-> dog house west":  self.helpers["sword"],
            "coffee shop outside -> coffee shop pot stairs":  self.helpers["sword"],
                # obscure: shoes
            "coffee shop pot stairs -> coffee shop outside": lambda state: True,
            "plant bushes <-> plant tile":  self.helpers["sword"],
            "shoe shop shortcut <-> shoe shop outside":  self.helpers["sword"],
            "factory cooler west <-> factory cooler tile":  self.helpers["sword"],
                # obscure: shoes
            "temple main north <-> temple main": self.helpers["sword"],

            # TODO: fix logical issues with not being able to carry a sword and a watering can at the same time
            "temple main east <-> temple main":  self.helpers["wateringcan"],
            "temple firebat test east": lambda state:
                self.helpers["wateringcan"](state)
                and self.helpers["darkroom2"](state),
            "temple firebat test west": lambda state:
                self.helpers["wateringcan"](state)
                and self.helpers["darkroom2"](state),
            # TODO: fix logical issues with not being able to carry a sword and a watering can at the same time

            "dog house inside -> dog house basement":  self.helpers["basement"],
            "dog house basement -> dog house inside": lambda state: True,
            "shoe shop inside -> shoe shop downstairs":  self.helpers["basement"],
            "shoe shop downstairs -> shoe shop inside": lambda state: True,

            "factory reception east <-> factory reception tile":  self.helpers["presspass"],
        }

        self.location_rules = {
            # Dog House
            "Dog House - ItemCoffee": lambda state:
                self.helpers["sword"](state)
                and state.can_reach("2crab tile", player=self.player)
                and state.can_reach("3crab main", player=self.player),
            # "Dog House - ItemFlashLight": lambda state: True,
            "Dog House - ItemKey": lambda state:
                self.helpers["sword"](state) and self.helpers["box"](state),
                # need to clear the plants by the boxes even with coffee
            # "Dog House - ItemWateringCan": lambda state: True,
            "Dog house - ItemBoat":  self.helpers["tree"],
            "Dog House - ItemBasement": self.helpers["tree"],
            # "Dog House - ItemPressPass": lambda state: True,
            "Dog House - House Pot Coin":  self.helpers["sword"],
            "Dog House - Sewer Island Coin":  self.helpers["chest"],
            "Dog House - Sewer Coin": lambda state:
                self.helpers["chest"](state)
                and self.helpers["darkroom2"](state)
                and self.helpers["swim"](state),
            "Dog House - Land is Great Coin":  self.helpers["chest"],
            "Dog House - Hidden Snake Coin": lambda state:
                self.helpers["chest"](state) and self.helpers["darkroom3"](state),
            "Dog House - Waterfall Coin": lambda state:
                self.helpers["chest"](state) and self.helpers["darkroom1"](state),
            "Dog House - Treasure Island Coin": lambda state:
                self.helpers["chest"](state)
                and self.helpers["swim"](state),
            "Dog House - Plant Heart":  self.helpers["wateringcan"],
            "Dog House - Bull Heart":  self.helpers["sword"],
            "Dog House - Boat Tentacle": lambda state:
                self.helpers["sword"](state)
                and state.has_all({
                    "ItemBoat",
                    "boatguy watered",
                    "ItemGlove",
                    }, self.player),
            "Dog House - Treasure Island Tentacle": lambda state:
                self.helpers["sword"](state) and self.helpers["swim"](state),
            "Dog House - Sword Toss Tentacle": lambda state:
                self.helpers["sword"](state)
                and state.has_all({"ItemCoffee", "ItemThrow"}, self.player),
            "Dog House - Sewer Tentacle": lambda state:
                self.helpers["sword"](state) and self.helpers["darkroom3"](state)
                and self.helpers["swim"](state),

            # Desert RV
            "Desert RV - ItemThrow":  self.helpers["sword"],
            "Desert RV - ItemShoes": lambda state:
                state.has("Coin", self.player, 7),
            "Desert RV - ItemGlove":  self.helpers["darkroom1"],
            "Desert RV - ItemTurboInk": lambda state:
                self.helpers["darkroom3"](state) and state.has("Tentacle", self.player, 8),
            "Desert RV - Temple Coin": lambda state:
                self.helpers["sword"](state) and self.helpers["darkroom2"](state),
                # this may change if i connect the other temple puzzles
            "Desert RV - Fire Bat Coin": lambda state:
                self.helpers["chest"](state) and self.helpers["darkroom2"](state),
                # this may change if i connect the other temple puzzles
            "Desert RV - Truck Supplies Coin": self.helpers["sword"],
            "Desert RV - Broken Truck":  self.helpers["chest"],
            "Desert RV - Quicksand Coin": lambda state:
                self.helpers["sword"](state) and self.helpers["darkroom2"](state),
                # vanilla does require sword because the wateringcan
                # drops while drowning in quicksand
            "Desert RV - Dumpster":  self.helpers["sword"],
            "Desert RV - Temple Heart": lambda state:
                self.helpers["darkroom3"](state)
                and state.has("ItemShoes", self.player),
            "Desert RV - Shop Heart": lambda state:
                state.has("Coin", self.player, 19),
            "Desert RV - Octopus Tentacle": lambda state:
                self.helpers["sword"](state)
                and self.helpers["darkroom3"](state)
                and self.helpers["swim"](state),
            "Desert RV - Beach Tentacle":  self.helpers["sword"],

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
                # praying i can make this work
            "Hotel Room - ItemGrinder": lambda state:
                self.helpers["darkroom2"](state)
                and state.has_all({"ItemSwim", "ItemCoffee"}, self.player),
            "Hotel Room - Shrub Arena Coin":  self.helpers["sword"],
            "Hotel Room - Miner's Chest Coin": lambda state:
                self.helpers["chest"](state) and self.helpers["darkroom3"](state),
            # "Factory Main - Inside Truck": lambda state:  True,
            # "Hotel Room - Queue": lambda state: True,
            "Hotel Room - Hotel Backroom Coin": lambda state:
                self.helpers["sword"](state) and self.helpers["box"](state),
                # sword is not actually necessary due to non-vanilla behaviors with the stuff that gets put into the pot.
            "Factory Main - Drill Coin":  self.helpers["sword"],
            "Hotel Room - Crow Heart":  self.helpers["box"],
            "Hotel Room - Dog Heart": lambda state: state.can_reach("dog house inside", player=self.player),
            "Factory Main - Cooler Tentacle":  self.helpers["sword"],

            # Island Shack
            "Island Shack - Teleporter Tentacle": lambda state:
                self.helpers["sword"](state)
                and self.helpers["darkroom1"](state)
                and state.has("ItemCoffee", self.player)
                and self.helpers["swim"](state),
                # obscure: Coffee not required

            # Underground Tent
            "Underground Tent - ItemTrophy":  self.helpers["darkroom1"],
            "Dog House - Dolphin Heart":  self.helpers["wateringcan"], # TODO: fix logical issues with not being able to carry a sword and a watering can at the same time

            # Undefined
            "Factory Main - ItemMegaSword": lambda state:
                self.helpers["sword"](state)
                and state.has_all({
                    "ItemWateringCan",
                    "left machine",
                    "right machine",
                    }, self.player),

            # events
            "generator smashed":  self.helpers["sword"],
            "drill smacked":  self.helpers["sword"],
            # "swimmer saved": lambda state:
            #     True,
            "hostage saved":  self.helpers["sword"],
            "wallet saved": lambda state:
                state.has("ItemCoffee", self.player),
            "ninja saved":  self.helpers["tree"],
            "bridge on":  self.helpers["sword"],
            "bridge saved": lambda state:
                state.has("bridge on", self.player),
            "hidden saved":  self.helpers["box"],
            "teleporter switch1": lambda state:
                self.helpers["sword"](state) and self.helpers["darkroom3"](state),
            "teleporter switch4": lambda state: 
                self.helpers["sword"](state)
                and (state.has("ItemCoffee", self.player)
                    or self.helpers["swim"](state)),
            "teleporter switch6": lambda state: 
                self.helpers["sword"](state)
                and (state.has("ItemCoffee", self.player)
                    or self.helpers["swim"](state)),
            "boatguy watered":  self.helpers["wateringcan"], # TODO: fix logical issues with not being able to carry a sword and a watering can at the same time
            "left machine": lambda state:
                self.helpers["darkroom1"](state)
                and state.has_all({"ItemSwim", "ItemCoffee"}, self.player),
            "right machine": lambda state:
                self.helpers["darkroom1"](state)
                and self.helpers["sword"](state),
            "bombs exploded": lambda state:
                self.helpers["sword"](state)
                and state.has("ItemThrow", self.player)
                and self.helpers["darkroom3"](state),
        }

        obscure = {
            # Flashlight from Below
            "lighthouse -> lighthouse lookout": self.helpers["swim"],

            # Shoes to skip breaking the pot
            "coffee shop outside -> coffee shop pot stairs": lambda state: 
                self.helpers["sword"](state)
                or state.has("ItemShoes", self.player),
            
            # Coffee shop to upper beach without breaking pot
            "coffee shop outside -> coffee shop upper beach": lambda state: 
                state.has("ItemCoffee", self.player)
                or self.helpers["swim"](state),
            
            # Push archers into poison river
            "camera river north -> camera river south": lambda state: True,

            # Bait the sharks
            "Overworld treasure island <-> Overworld island shack": self.helpers["swim"],

            # Glitch through with precision
            "factory cooler west <-> factory cooler tile": lambda state: 
                self.helpers["sword"](state)
                or state.has("ItemShoes", self.player),

            # Island Shack
            "Island Shack - Teleporter Tentacle": lambda state:
                self.helpers["sword"](state)
                and self.helpers["darkroom1"](state)
                and self.helpers["swim"](state),
            

        }

        def apply_rules(optional_rules):
            for key, rule in optional_rules.items():
                if key in self.region_rules:
                    self.region_rules[key] = rule
                else:
                    self.location_rules[key] = rule

        if self.world.options.obscure:
            apply_rules(obscure)

    def rev(self, e_name: str) -> (str, str):
        e_list = e_name.split(" -> ")
        if len(e_list) == 2:
            return f"{e_list[1]} <-> {e_list[0]}", f"{e_list[0]} <-> {e_list[1]}"
        else:
            return "", ""

    def set_Minit_rules(self) -> None:
        multiworld = self.world.multiworld
        for region in multiworld.get_regions(self.player):
            for entrance in region.exits:
                if entrance.name in self.region_rules:
                    set_rule(entrance, self.region_rules[entrance.name])
                else:
                    left_name, right_name = self.rev(entrance.name)
                    if left_name in self.region_rules:
                        set_rule(
                            entrance,
                            self.region_rules[left_name]
                            )
                    elif right_name in self.region_rules:
                        set_rule(
                            entrance,
                            self.region_rules[right_name]
                            )
            for location in region.locations:
                if location.name in self.location_rules:
                    set_rule(location, self.location_rules[location.name])
