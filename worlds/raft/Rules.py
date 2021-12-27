from ..generic.Rules import set_rule
from .Locations import location_table
from .Regions import regionMap
from ..AutoWorld import LogicMixin

# TODOs
# - Maybe put large island unlockables behind Receiver
# -- This will make getting them more consistent
# - Blueprint fuel pipe on Balboa didn't trigger Archipelago sendable ("Error finding ID for location Blueprint_Pipe_Fuel")
# -- Same with Blueprint_Fueltank
# -- All blueprints :(
# - Blueprint_Firework from doll after explosive barrel on Caravan Island doesn't disappear when picked up

class RaftLogic(LogicMixin):
    def can_smelt_items(self, player):
        return self.has("Smelter", player)

    def can_craft_bolt(self, player):
        return self.can_smelt_items(player) and self.has("Bolt", player)

    def can_craft_hinge(self, player):
        return self.can_smelt_items(player) and self.has("Hinge", player)

    def can_craft_battery(self, player):
        return self.can_smelt_items(player) and self.has("Battery", player)

    def can_craft_circuitBoard(self, player):
        return self.can_smelt_items(player) and self.has("Circuit board", player)

    def can_craft_reciever(self, player):
        return self.can_craft_circuitBoard(player) and self.can_craft_hinge(player) and self.has("Receiver", player)

    def can_craft_antenna(self, player):
        return self.can_craft_circuitBoard(player) and self.can_craft_bolt(player) and self.has("Antenna", player)

    def can_craft_plasticBottle(self, player):
        return self.can_smelt_items(player) and self.has("Empty bottle", player)

    def can_fire_bow(self, player):
        return self.has("Basic bow", player) and self.has("Stone arrow", player)

    def can_craft_shears(self, player):
        return self.can_smelt_items(player) and self.can_craft_hinge(player) and self.has("Shear", player)

    def can_craft_birdNest(self, player):
        return self.has("Birds nest", player)

    def can_craft_engine(self, player):
        return self.can_smelt_items(player) and self.can_craft_circuitBoard(player) and self.has("Engine", player)

    def can_craft_steeringWheel(self, player):
        return (self.can_smelt_items(player) and self.can_craft_bolt(player)
            and self.can_craft_hinge(player) and self.has("Steering Wheel", player))

    def can_craft_machete(self, player):
        return self.can_smelt_items(player) and self.can_craft_bolt(player) and self.has("Machete", player)

    def can_craft_ziplineTool(self, player):
        return self.can_craft_hinge(player) and self.can_craft_bolt(player) and self.has("Zipline tool", player)

    def can_get_dirt(self, player):
        return self.can_smelt_items(player) and self.can_craft_bolt(player) and self.has("Shovel", player)

    def can_craft_grassPlot(self, player):
        return self.can_get_dirt(player) and self.has("Grass plot", player)

    def can_craft_netLauncher(self, player):
        return self.can_smelt_items(player) and self.can_craft_bolt(player) and self.has("Net launcher", player)

    def can_craft_netCanister(self, player):
        return self.can_smelt_items(player) and self.has("Net canister", player)

    def can_capture_animals(self, player):
        return (self.can_craft_netLauncher(player) and self.can_craft_netCanister(player)
            and self.can_craft_grassPlot(player))

    def can_navigate(self, player): # Sail is added by default and not considered in Archipelago
        return self.can_craft_battery(player) and self.can_craft_reciever(player) and self.can_craft_antenna(player)

    def can_drive(self, player): # The player can go wherever they want with the engine
        return self.can_craft_engine(player) and self.can_craft_steeringWheel(player)

    def can_access_radio_tower(self, player):
        # Technically the player doesn't need things like the sail to reach the Radio Tower,
        # but paddling there is not very efficient or engaging gameplay.
        return self.can_navigate(player)

    def can_complete_radio_tower(self, player):
        return self.can_access_radio_tower(player)

    def can_access_vasagatan(self, player):
        return self.can_complete_radio_tower(player) and self.can_navigate(player) and self.has("Vasagatan Frequency", player)

    def can_complete_vasagatan(self, player):
        return self.can_access_vasagatan(player)

    def can_access_balboa_island(self, player):
        return self.can_complete_vasagatan(player) and self.can_drive(player) and self.has("Balboa Island Frequency", player)

    def can_complete_balboa_island(self, player):
        return self.can_access_balboa_island(player) and self.can_craft_machete(player) and self.can_fire_bow(player)

    def can_access_caravan_island(self, player):
        return self.can_complete_balboa_island(player) and self.can_drive(player) # Coordinates are given from Relay Station quest

    def can_complete_caravan_island(self, player):
        return self.can_access_caravan_island(player) and self.can_craft_ziplineTool(player)

    def can_access_tangaroa(self, player):
        return self.can_complete_caravan_island(player) and self.can_drive(player) and self.has("Tangaroa Frequency", player)

    def can_complete_tangaroa(self, player):
        return self.can_access_tangaroa(player)

def set_rules(world, player):
    # Map region to check to see if we can access it
    regionChecks = {
        "Raft": lambda state: True,
        "ResearchTable": lambda state: True,
        "RadioTower": lambda state: state.can_access_radio_tower(player), # All can_access functions have state as implicit parameter for function
        "Vasagatan": lambda state: state.can_access_vasagatan(player),
        "BalboaIsland": lambda state: state.can_access_balboa_island(player),
        "CaravanIsland": lambda state: state.can_access_caravan_island(player),
        "Tangaroa": lambda state: state.can_access_tangaroa(player)
    }
    itemChecks = {
        "Plank": lambda state: True,
        "Plastic": lambda state: True,
        "Clay": lambda state: True,
        "Stone": lambda state: True,
        "Rope": lambda state: True,
        "Nail": lambda state: True,
        "Scrap": lambda state: True,
        "SeaVine": lambda state: True,
        "Brick_Dry": lambda state: True,
        "Leather": lambda state: True, # Conflicting info on whetherwe need state.can_navigate(player) instead, personal testing indicates this is correct
        "Thatch": lambda state: True, # Palm Leaf
        "Placeable_GiantClam": lambda state: True,
        "Feather": lambda state: state.can_craft_birdNest(player), # Maybe add config for this since you technically don't need bird nest
        "MetalIngot": lambda state: state.can_smelt_items(player),
        "CopperIngot": lambda state: state.can_smelt_items(player),
        "VineGoo": lambda state: state.can_smelt_items(player),
        "ExplosivePowder": lambda state: state.can_smelt_items(player),
        "Glass": lambda state: state.can_smelt_items(player),
        "Bolt": lambda state: state.can_craft_bolt(player),
        "Hinge": lambda state: state.can_craft_hinge(player),
        "CircuitBoard": lambda state: state.can_craft_circuitBoard(player),
        "PlasticBottle_Empty": lambda state: state.can_craft_plasticBottle(player),
        "Shear": lambda state: state.can_craft_shears(player),
        "Wool": lambda state: state.can_capture_animals(player) and state.can_craft_shears(player),
        "HoneyComb": lambda state: state.can_access_balboa_island(player),
        "Jar_Bee": lambda state: state.can_access_balboa_island(player) and state.can_smelt_items(player),
        "Dirt": lambda state: state.can_get_dirt(player),
        "Egg": lambda state: state.can_capture_animals(player),
        # Specific items for story island location checks
        "Machete": lambda state: state.can_craft_machete(player),
        "BowAndArrow": lambda state: state.can_fire_bow(player),
        "Zipline tool": lambda state: state.can_craft_ziplineTool(player)
    }

    # Location rules
    for region in regionMap:
        if region != "Menu":
            for exitRegion in world.get_region(region, player).exits:
                set_rule(world.get_entrance(exitRegion.name, player), regionChecks[region])
     
    # Process locations
    for location in location_table:
        locFromWorld = world.get_location(location["name"], player)
        if "requiresAccessToItems" in location:
            def ruleLambda(state, location=location):
                canAccess = regionChecks[location["region"]](state)
                for item in location["requiresAccessToItems"]:
                    if not itemChecks[item](state):
                        canAccess = False
                        break
                return canAccess
            set_rule(locFromWorld, ruleLambda)
        else:
            set_rule(locFromWorld, regionChecks[location["region"]])

    # Victory location
    world.completion_condition[player] = lambda state: state.has('Victory', player)