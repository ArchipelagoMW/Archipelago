# entry point for the logic implementation

class Logic(object):
    @staticmethod
    def factory(implementation):
        if implementation == 'vanilla':
            from worlds.sm.variaRandomizer.graph.vanilla.graph_helpers import HelpersGraph
            from worlds.sm.variaRandomizer.graph.vanilla.graph_access import accessPoints
            from worlds.sm.variaRandomizer.graph.vanilla.graph_locations import locations
            from worlds.sm.variaRandomizer.graph.vanilla.graph_locations import LocationsHelper
            Logic.locations = locations
            Logic.accessPoints = accessPoints
            Logic.HelpersGraph = HelpersGraph
            Logic.patches = implementation
            Logic.LocationsHelper = LocationsHelper
        elif implementation == 'rotation':
            from worlds.sm.variaRandomizer.graph.rotation.graph_helpers import HelpersGraph
            from worlds.sm.variaRandomizer.graph.rotation.graph_access import accessPoints
            from worlds.sm.variaRandomizer.graph.rotation.graph_locations import locations
            from worlds.sm.variaRandomizer.graph.rotation.graph_locations import LocationsHelper
            Logic.locations = locations
            Logic.accessPoints = accessPoints
            Logic.HelpersGraph = HelpersGraph
            Logic.patches = implementation
            Logic.LocationsHelper = LocationsHelper
            Logic.implementation = implementation
