from ..generic.Rules import set_rule
from .Locations import location_table
from .Regions import regionMap
from ..AutoWorld import LogicMixin

class RaftLogic(LogicMixin):
    def raft_paddleboard_mode_enabled(self, player):
        return bool(self.multiworld.worlds[player].options.paddleboard_mode)
    
    def raft_big_islands_available(self, player):
        return bool(self.multiworld.worlds[player].options.big_island_early_crafting) or self.raft_can_access_radio_tower(player)

    def raft_can_smelt_items(self, player):
        return self.has("Smelter", player)

    def raft_can_craft_bolt(self, player):
        return self.raft_can_smelt_items(player) and self.has("Bolt", player)

    def raft_can_craft_hinge(self, player):
        return self.raft_can_smelt_items(player) and self.has("Hinge", player)

    def raft_can_craft_battery(self, player):
        return self.raft_can_smelt_items(player) and self.has("Battery", player)

    def raft_can_craft_circuitBoard(self, player):
        return self.raft_can_smelt_items(player) and self.has("Circuit board", player)
    
    def raft_can_craft_shovel(self, player):
        return self.raft_can_smelt_items(player) and self.has("Shovel", player) and self.raft_can_craft_bolt(player)

    def raft_can_craft_reciever(self, player):
        return self.raft_can_craft_circuitBoard(player) and self.raft_can_craft_hinge(player) and self.has("Receiver", player)

    def raft_can_craft_antenna(self, player):
        return self.raft_can_craft_circuitBoard(player) and self.raft_can_craft_bolt(player) and self.has("Antenna", player)
    
    def raft_can_find_titanium(self, player):
        return (self.has("Metal detector", player) and self.raft_can_craft_battery(player)
            and self.raft_can_craft_shovel(player))

    def raft_can_craft_plasticBottle(self, player):
        return self.raft_can_smelt_items(player) and self.has("Empty bottle", player)

    def raft_can_fire_bow(self, player):
        return self.has("Basic bow", player) and self.has("Stone arrow", player)

    def raft_can_craft_shears(self, player):
        return self.raft_can_smelt_items(player) and self.raft_can_craft_hinge(player) and self.has("Shear", player)

    def raft_can_craft_birdNest(self, player):
        return self.has("Birds nest", player)

    def raft_can_craft_engine(self, player):
        return self.raft_can_smelt_items(player) and self.raft_can_craft_circuitBoard(player) and self.has("Engine", player)

    def raft_can_craft_steeringWheel(self, player):
        return (self.raft_can_smelt_items(player) and self.raft_can_craft_bolt(player)
            and self.raft_can_craft_hinge(player) and self.has("Steering Wheel", player))

    def raft_can_craft_machete(self, player):
        return self.raft_can_smelt_items(player) and self.raft_can_craft_bolt(player) and self.has("Machete", player)

    def raft_can_craft_ziplineTool(self, player):
        return self.raft_can_craft_hinge(player) and self.raft_can_craft_bolt(player) and self.has("Zipline tool", player)

    def raft_can_get_dirt(self, player):
        return self.raft_can_craft_shovel(player) and self.raft_big_islands_available(player)

    def raft_can_craft_grassPlot(self, player):
        return self.raft_can_get_dirt(player) and self.has("Grass plot", player)

    def raft_can_craft_netLauncher(self, player):
        return self.raft_can_smelt_items(player) and self.raft_can_craft_bolt(player) and self.has("Net launcher", player)

    def raft_can_craft_netCanister(self, player):
        return self.raft_can_smelt_items(player) and self.has("Net canister", player)

    def raft_can_capture_animals(self, player):
        return (self.raft_can_craft_netLauncher(player) and self.raft_can_craft_netCanister(player)
            and self.raft_can_craft_grassPlot(player))

    def raft_can_navigate(self, player): # Sail is added by default and not considered in Archipelago
        return self.raft_can_craft_battery(player) and self.raft_can_craft_reciever(player) and self.raft_can_craft_antenna(player)

    def raft_can_drive(self, player): # The player can go wherever they want with the engine
        return (self.raft_can_craft_engine(player) and self.raft_can_craft_steeringWheel(player)) or self.raft_paddleboard_mode_enabled(player)

    def raft_can_access_radio_tower(self, player):
        return self.raft_can_navigate(player)

    def raft_can_complete_radio_tower(self, player):
        return self.raft_can_access_radio_tower(player)

    def raft_can_access_vasagatan(self, player):
        return self.raft_can_navigate(player) and self.has("Vasagatan Frequency", player)

    def raft_can_complete_vasagatan(self, player):
        return self.raft_can_access_vasagatan(player)

    def raft_can_access_balboa_island(self, player):
        return self.raft_can_navigate(player) and self.raft_can_drive(player) and self.has("Balboa Island Frequency", player)

    def raft_can_complete_balboa_island(self, player):
        return self.raft_can_access_balboa_island(player) and self.raft_can_craft_machete(player)

    def raft_can_access_caravan_island(self, player):
        return self.raft_can_navigate(player) and self.raft_can_drive(player) and self.has("Caravan Island Frequency", player)

    def raft_can_complete_caravan_island(self, player):
        return self.raft_can_access_caravan_island(player) and self.raft_can_craft_ziplineTool(player)

    def raft_can_access_tangaroa(self, player):
        return self.raft_can_navigate(player) and self.raft_can_drive(player) and self.has("Tangaroa Frequency", player)

    def raft_can_complete_tangaroa(self, player):
        return self.raft_can_access_tangaroa(player) and self.raft_can_craft_ziplineTool(player)

    def raft_can_access_varuna_point(self, player):
        return self.raft_can_navigate(player) and self.raft_can_drive(player) and self.has("Varuna Point Frequency", player)

    def raft_can_complete_varuna_point(self, player):
        return self.raft_can_access_varuna_point(player) and self.raft_can_craft_ziplineTool(player)

    def raft_can_access_temperance(self, player):
        return self.raft_can_navigate(player) and self.raft_can_drive(player) and self.has("Temperance Frequency", player)

    def raft_can_complete_temperance(self, player):
        return self.raft_can_access_temperance(player) # No zipline required on Temperance

    def raft_can_access_utopia(self, player):
        return (self.raft_can_navigate(player) and self.raft_can_drive(player)
            # Access checks are to prevent frequencies for other
            # islands from appearing in Utopia
            and self.raft_can_access_radio_tower(player)
            and self.raft_can_access_vasagatan(player)
            and self.raft_can_access_balboa_island(player)
            and self.raft_can_access_caravan_island(player)
            and self.raft_can_access_tangaroa(player)
            and self.raft_can_access_varuna_point(player)
            and self.raft_can_access_temperance(player)
            and self.has("Utopia Frequency", player)
            and self.raft_can_craft_shovel(player)) # Shovels are available but we don't want to softlock players

    def raft_can_complete_utopia(self, player):
        return self.raft_can_access_utopia(player) and self.raft_can_craft_ziplineTool(player)

def set_rules(world, player):
    regionChecks = {
        "Raft": lambda state: True,
        "ResearchTable": lambda state: True,
        "RadioTower": lambda state: state.raft_can_access_radio_tower(player), # All can_access functions have state as implicit parameter for function
        "Vasagatan": lambda state: state.raft_can_access_vasagatan(player),
        "BalboaIsland": lambda state: state.raft_can_access_balboa_island(player),
        "CaravanIsland": lambda state: state.raft_can_access_caravan_island(player),
        "Tangaroa": lambda state: state.raft_can_access_tangaroa(player),
        "Varuna Point": lambda state: state.raft_can_access_varuna_point(player),
        "Temperance": lambda state: state.raft_can_access_temperance(player),
        "Utopia": lambda state: state.raft_can_complete_temperance(player) and state.raft_can_access_utopia(player)
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
        "Thatch": lambda state: True, # Palm Leaf
        "Placeable_GiantClam": lambda state: True,
        "Leather": lambda state: state.raft_big_islands_available(player),
        "Feather": lambda state: state.raft_big_islands_available(player) or state.raft_can_craft_birdNest(player),
        "MetalIngot": lambda state: state.raft_can_smelt_items(player),
        "CopperIngot": lambda state: state.raft_can_smelt_items(player),
        "VineGoo": lambda state: state.raft_can_smelt_items(player),
        "ExplosivePowder": lambda state: state.raft_big_islands_available(player) and state.raft_can_smelt_items(player),
        "Glass": lambda state: state.raft_can_smelt_items(player),
        "Bolt": lambda state: state.raft_can_craft_bolt(player),
        "Hinge": lambda state: state.raft_can_craft_hinge(player),
        "CircuitBoard": lambda state: state.raft_can_craft_circuitBoard(player),
        "PlasticBottle_Empty": lambda state: state.raft_can_craft_plasticBottle(player),
        "Wool": lambda state: state.raft_can_capture_animals(player) and state.raft_can_craft_shears(player),
        "HoneyComb": lambda state: state.raft_can_access_balboa_island(player),
        "Jar_Bee": lambda state: state.raft_can_access_balboa_island(player) and state.raft_can_smelt_items(player),
        "Dirt": lambda state: state.raft_can_get_dirt(player),
        "Egg": lambda state: state.raft_can_capture_animals(player),
        "TitaniumIngot": lambda state: state.raft_can_smelt_items(player) and state.raft_can_find_titanium(player),
        # Specific items for story island location checks
        "Machete": lambda state: state.raft_can_craft_machete(player),
        "Zipline tool": lambda state: state.raft_can_craft_ziplineTool(player)
    }

    # Region access rules
    for region in regionMap:
        if region != "Menu":
            for exitRegion in world.get_region(region, player).exits:
                set_rule(world.get_entrance(exitRegion.name, player), regionChecks[region])

    # Location access rules
    for location in location_table:
        locFromWorld = world.get_location(location["name"], player)
        if "requiresAccessToItems" in location: # Specific item access required
            def fullLocationCheck(state, location=location):
                canAccess = regionChecks[location["region"]](state)
                for item in location["requiresAccessToItems"]:
                    if not itemChecks[item](state):
                        canAccess = False
                        break
                return canAccess
            set_rule(locFromWorld, fullLocationCheck)
        else: # Only region access required
            set_rule(locFromWorld, regionChecks[location["region"]])

    # Victory requirement
    world.completion_condition[player] = lambda state: state.has("Victory", player)