from . import overworld
from . import dungeon1
from . import dungeon2
from . import dungeon3
from . import dungeon4
from . import dungeon5
from . import dungeon6
from . import dungeon7
from . import dungeon8
from . import dungeonColor
from .requirements import AND, OR, COUNT, COUNTS, FOUND, RequirementsSettings
from .location import Location
from ..locations.items import *
from ..locations.keyLocation import KeyLocation
from ..worldSetup import WorldSetup
from .. import itempool
from .. import mapgen


class Logic:
    def __init__(self, configuration_options, *, world_setup):
        self.world_setup = world_setup
        r = RequirementsSettings(configuration_options)

        if configuration_options.overworld == "dungeondive":
            world = overworld.DungeonDiveOverworld(configuration_options, r)
        elif configuration_options.overworld == "random":
            world = mapgen.LogicGenerator(configuration_options, world_setup, r, world_setup.map)
        else:
            world = overworld.World(configuration_options, world_setup, r)

        if configuration_options.overworld == "nodungeons":
            world.updateIndoorLocation("d1", dungeon1.NoDungeon1(configuration_options, world_setup, r).entrance)
            world.updateIndoorLocation("d2", dungeon2.NoDungeon2(configuration_options, world_setup, r).entrance)
            world.updateIndoorLocation("d3", dungeon3.NoDungeon3(configuration_options, world_setup, r).entrance)
            world.updateIndoorLocation("d4", dungeon4.NoDungeon4(configuration_options, world_setup, r).entrance)
            world.updateIndoorLocation("d5", dungeon5.NoDungeon5(configuration_options, world_setup, r).entrance)
            world.updateIndoorLocation("d6", dungeon6.NoDungeon6(configuration_options, world_setup, r).entrance)
            world.updateIndoorLocation("d7", dungeon7.NoDungeon7(configuration_options, world_setup, r).entrance)
            world.updateIndoorLocation("d8", dungeon8.NoDungeon8(configuration_options, world_setup, r).entrance)
            world.updateIndoorLocation("d0", dungeonColor.NoDungeonColor(configuration_options, world_setup, r).entrance)
        elif configuration_options.overworld != "random":
            world.updateIndoorLocation("d1", dungeon1.Dungeon1(configuration_options, world_setup, r).entrance)
            world.updateIndoorLocation("d2", dungeon2.Dungeon2(configuration_options, world_setup, r).entrance)
            world.updateIndoorLocation("d3", dungeon3.Dungeon3(configuration_options, world_setup, r).entrance)
            world.updateIndoorLocation("d4", dungeon4.Dungeon4(configuration_options, world_setup, r).entrance)
            world.updateIndoorLocation("d5", dungeon5.Dungeon5(configuration_options, world_setup, r).entrance)
            world.updateIndoorLocation("d6", dungeon6.Dungeon6(configuration_options, world_setup, r).entrance)
            world.updateIndoorLocation("d7", dungeon7.Dungeon7(configuration_options, world_setup, r).entrance)
            world.updateIndoorLocation("d8", dungeon8.Dungeon8(configuration_options, world_setup, r).entrance)
            world.updateIndoorLocation("d0", dungeonColor.DungeonColor(configuration_options, world_setup, r).entrance)

        if configuration_options.overworld != "random":
            for k in world.overworld_entrance.keys():
                assert k in world_setup.entrance_mapping, k
            for k in world_setup.entrance_mapping.keys():
                assert k in world.overworld_entrance, k

            for entrance, indoor in world_setup.entrance_mapping.items():
                exterior = world.overworld_entrance[entrance]
                if world.indoor_location[indoor] is not None:
                    exterior.location.connect(world.indoor_location[indoor], exterior.requirement)
                    if exterior.enterIsSet():
                        exterior.location.connect(world.indoor_location[indoor], exterior.one_way_enter_requirement, one_way=True)
                    if exterior.exitIsSet():
                        world.indoor_location[indoor].connect(exterior.location, exterior.one_way_exit_requirement, one_way=True)

        egg_trigger = AND(OCARINA, SONG1)
        if configuration_options.logic == 'glitched' or configuration_options.logic == 'hell':
            egg_trigger = OR(AND(OCARINA, SONG1), BOMB)

        if world_setup.goal == "seashells":
            world.nightmare.connect(world.egg, COUNT(SEASHELL, 20))
        elif world_setup.goal in ("raft", "bingo", "bingo-full"):
            world.nightmare.connect(world.egg, egg_trigger)
        else:
            goal = int(world_setup.goal)
            if goal < 0:
                world.nightmare.connect(world.egg, None)
            elif goal == 0:
                world.nightmare.connect(world.egg, egg_trigger)
            elif goal == 8:
                world.nightmare.connect(world.egg, AND(egg_trigger, INSTRUMENT1, INSTRUMENT2, INSTRUMENT3, INSTRUMENT4, INSTRUMENT5, INSTRUMENT6, INSTRUMENT7, INSTRUMENT8))
            else:
                world.nightmare.connect(world.egg, AND(egg_trigger, COUNTS([INSTRUMENT1, INSTRUMENT2, INSTRUMENT3, INSTRUMENT4, INSTRUMENT5, INSTRUMENT6, INSTRUMENT7, INSTRUMENT8], goal)))

        # if configuration_options.dungeon_items == 'keysy':
        #     for n in range(9):
        #         for count in range(9):
        #             world.start.add(KeyLocation("KEY%d" % (n + 1)))
        #         world.start.add(KeyLocation("NIGHTMARE_KEY%d" % (n + 1)))

        self.world = world
        self.start = world.start
        self.windfish = world.windfish
        self.location_list = []
        self.iteminfo_list = []

        self.__location_set = set()
        self.__recursiveFindAll(self.start)
        del self.__location_set

        for ii in self.iteminfo_list:
            ii.configure(configuration_options)

    def dumpFlatRequirements(self):
        def __rec(location, req):
            if hasattr(location, "flat_requirements"):
                new_flat_requirements = requirements.mergeFlat(location.flat_requirements, requirements.flatten(req))
                if new_flat_requirements == location.flat_requirements:
                    return
                location.flat_requirements = new_flat_requirements
            else:
                location.flat_requirements = requirements.flatten(req)
            for connection, requirement in location.simple_connections:
                __rec(connection, AND(req, requirement) if req else requirement)
            for connection, requirement in location.gated_connections:
                __rec(connection, AND(req, requirement) if req else requirement)
        __rec(self.start, None)
        for ii in self.iteminfo_list:
            print(ii)
            for fr in ii._location.flat_requirements:
                print("    " + ", ".join(sorted(map(str, fr))))

    def __recursiveFindAll(self, location):
        if location in self.__location_set:
            return
        self.location_list.append(location)
        self.__location_set.add(location)
        for ii in location.items:
            self.iteminfo_list.append(ii)
        for connection, requirement in location.simple_connections:
            self.__recursiveFindAll(connection)
        for connection, requirement in location.gated_connections:
            self.__recursiveFindAll(connection)
