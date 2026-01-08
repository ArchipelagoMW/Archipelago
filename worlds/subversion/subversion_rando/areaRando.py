from collections import defaultdict, deque
import random
from typing import Optional

from .area_rando_types import AreaDoor, DoorPairs
from .connection_data import area_doors_unpackable
from .romWriter import RomWriter

# RandomizeAreas shuffles the locations and checks that the ship connects to daphne properly
# updateAreaLogic is like a logic updater for area doors connecting to other area doors
# -this is done before the item locations are updated

# second version uses
# [0]the door pointer this door needs to send with
# [1]the data that is needed to go to this door


(
    CraterR, SunkenNestL, RuinedConcourseBL, RuinedConcourseTR, CausewayR,
    SporeFieldTR, SporeFieldBR, OceanShoreR, EleToTurbidPassageR, PileAnchorL,
    ExcavationSiteL, WestCorridorR, FoyerR, ConstructionSiteL, AlluringCenoteR,
    FieldAccessL, TransferStationR, CellarR, SubbasementFissureL,
    WestTerminalAccessL, MezzanineConcourseL, VulnarCanyonL, CanyonPassageR,
    ElevatorToCondenserL, LoadingDockSecurityAreaL, ElevatorToWellspringL,
    NorakBrookL, NorakPerimeterTR, NorakPerimeterBL, VulnarDepthsElevatorEL,
    VulnarDepthsElevatorER, HiveBurrowL, SequesteredInfernoL,
    CollapsedPassageR, MagmaPumpL, ReservoirMaintenanceTunnelR, IntakePumpR,
    ThermalReservoir1R, GeneratorAccessTunnelL, ElevatorToMagmaLakeR,
    MagmaPumpAccessR, FieryGalleryL, RagingPitL, HollowChamberR, PlacidPoolR,
    SporousNookL, RockyRidgeTrailL, TramToSuziIslandR
) = area_doors_unpackable


def escape_path(door_pairs: DoorPairs) -> Optional[list[str]]:
    adj: dict[str, dict[str, bool]] = {
        door_a.name: {
            door_b.name: True
            for door_b in area_doors_unpackable
            if door_a.area_name == door_b.area_name
        }
        for door_a in area_doors_unpackable
    }

    def disconnect_all(door: AreaDoor) -> None:
        adj[door.name] = {}
        for dests in adj.values():
            dests[door.name] = False

    # sky elevators don't work during escape, so no condenser
    disconnect_all(ElevatorToCondenserL)

    # ship is separated
    disconnect_all(SunkenNestL)
    disconnect_all(CraterR)

    # casual logic can't go through hive burrow
    disconnect_all(HiveBurrowL)
    # TODO: make it so Hive Burrow is allowed in expert logic?

    # west terminal up elevator is disabled (down elevator is ok)
    adj[WestTerminalAccessL.name] = {}

    # if enter norak brook from left, can't go anywhere
    adj[NorakBrookL.name] = {}

    # from Mezzanine Concourse, can only go west
    adj[MezzanineConcourseL.name] = {WestTerminalAccessL.name: True}

    # TODO: check: If you enter Vulnar Canyon through VulnarCanyonL during escape, can you go out CanyonPassageR?
    adj[VulnarCanyonL.name][CanyonPassageR.name] = False  # delete this line if you can

    # add all area connections
    for door_a, door_b in door_pairs.connections():
        adj[door_a.name][door_b.name] = True
        adj[door_b.name][door_a.name] = True

    # pprint(adj)

    sources: dict[str, Optional[str]] = {
        RockyRidgeTrailL.name: None
    }
    visited: dict[str, bool] = defaultdict(bool)
    bfs_queue: deque[str] = deque([RockyRidgeTrailL.name])

    while len(bfs_queue):
        current = bfs_queue.popleft()
        if not visited[current]:
            visited[current] = True
            if current == CraterR.name or current == SunkenNestL.name:
                break
            for neighbor in adj[current]:
                if adj[current][neighbor]:
                    if neighbor not in sources:
                        sources[neighbor] = current
                    bfs_queue.append(neighbor)

    if CraterR.name in sources:
        reverse_path = [CraterR.name]
    elif SunkenNestL.name in sources:
        reverse_path = [SunkenNestL.name]
    else:
        return None

    while reverse_path[-1] != RockyRidgeTrailL.name:
        source = sources[reverse_path[-1]]
        assert source, f"sources didn't lead back to daphne: {sources}"
        reverse_path.append(source)

    return list(reversed(reverse_path))


def RandomizeAreas(force_normal_early: bool, seed: Optional[int] = None) -> DoorPairs:
    """
    force_normal_early forces SunkenNestL to connect to OceanShoreR
    This is necessary for casual major/minor.
    """
    # Each location holds
    # [0]the data of its door
    # [1]the data of the vanilla door that goes here
    # [2]the area
    # [3]the name of the door
    # [4]region

    if not (seed is None):
        random.seed(seed)

    Connections: list[tuple[AreaDoor, AreaDoor]] = []
    areaAttempts = 0
    connected = False
    while not connected:
        areaAttempts += 1
        if areaAttempts > 1000:
            raise TimeoutError("> 1000 attempts for subversion area rando")
        if seed is None:
            print("**********Trying to get a good escape attempt:", areaAttempts)

        OpenNodesR = [CraterR,
                      RuinedConcourseTR,
                      CausewayR,
                      SporeFieldTR,
                      SporeFieldBR]
        OpenNodesL = [SunkenNestL,
                      RuinedConcourseBL]
        VisitedAreas = ['Early']
        Connections = []

        RightSideDoorsList = [OceanShoreR,
                              EleToTurbidPassageR,
                              WestCorridorR,
                              FoyerR,
                              AlluringCenoteR,
                              TransferStationR,
                              CellarR,
                              CanyonPassageR,
                              NorakPerimeterTR,
                              VulnarDepthsElevatorER,
                              CollapsedPassageR,
                              ReservoirMaintenanceTunnelR,
                              IntakePumpR,
                              ThermalReservoir1R,
                              ElevatorToMagmaLakeR,
                              MagmaPumpAccessR,
                              HollowChamberR,
                              PlacidPoolR,
                              TramToSuziIslandR]

        LeftSideDoorsList = [PileAnchorL,
                             ExcavationSiteL,
                             ConstructionSiteL,
                             FieldAccessL,
                             SubbasementFissureL,
                             WestTerminalAccessL,
                             MezzanineConcourseL,
                             VulnarCanyonL,
                             ElevatorToCondenserL,
                             LoadingDockSecurityAreaL,
                             ElevatorToWellspringL,
                             NorakBrookL,
                             NorakPerimeterBL,
                             VulnarDepthsElevatorEL,
                             HiveBurrowL,
                             SequesteredInfernoL,
                             MagmaPumpL,
                             GeneratorAccessTunnelL,
                             FieryGalleryL,
                             RagingPitL,
                             SporousNookL,
                             RockyRidgeTrailL]
        # for h in RightSideDoorsList :
        #     print(h[2],h[3])

        # for h in LeftSideDoorsList :
        #     print(h[2],h[3])

        if force_normal_early:
            Connections.append((SunkenNestL, OceanShoreR))
            OpenNodesL.remove(SunkenNestL)
            RightSideDoorsList.remove(OceanShoreR)

            VisitedAreas = VisitedAreas+[OceanShoreR.area_name]
            for doorSearch in RightSideDoorsList:
                if doorSearch.area_name in VisitedAreas:
                    OpenNodesR += [doorSearch]
            for doorClean in OpenNodesR:
                if doorClean in RightSideDoorsList:
                    RightSideDoorsList.remove(doorClean)

        while RightSideDoorsList != [] or LeftSideDoorsList != []:
            # print("Lengths : OpenNodesL",len(OpenNodesL)," and OpenNodesR",len(OpenNodesR))
            CombinedDoorsList = RightSideDoorsList + LeftSideDoorsList
            # This case is for making sure all areas make it into the map
            # Then all other connections happen later
            randomIndex = 0
            if len(CombinedDoorsList) > 1:
                randomIndex = random.randint(0, len(CombinedDoorsList)-1)
            selectedDoor = CombinedDoorsList[randomIndex]
            if (selectedDoor in RightSideDoorsList) and OpenNodesL != []:
                # It is a right door and there are open Left nodes to connect to
                # if it fails, the loop will try again with no change
                RightSideDoorsList.remove(selectedDoor)
                # Choose a random Left node to connect to
                randomNode = random.choice(OpenNodesL)
                Connections.append((selectedDoor, randomNode))
                # for DEBUG
                # print('RightSideDoorsList')
                # print('pairing',selectedDoor[2],selectedDoor[3],"--",OpenNodesL[randomNode][2],OpenNodesL[randomNode][3])
                OpenNodesL.remove(randomNode)
                # Now add the area to the visitedareas
                # and all nodes from that area
                VisitedAreas = VisitedAreas+[selectedDoor.area_name]
                for doorSearch in RightSideDoorsList:
                    if doorSearch.area_name in VisitedAreas:
                        OpenNodesR += [doorSearch]
                for doorClean in OpenNodesR:
                    if doorClean in RightSideDoorsList:
                        RightSideDoorsList.remove(doorClean)
            elif (selectedDoor in LeftSideDoorsList) and OpenNodesR != []:
                # It is a left door and there are open right nodes to connect to
                # if it fails, the loop will try again with no change
                LeftSideDoorsList.remove(selectedDoor)
                # Choose a random Right node to connect to
                randomNode = random.choice(OpenNodesR)
                Connections.append((selectedDoor, randomNode))
                # for DEBUG
                # print('LeftSideDoorsList')
                # print('pairing',selectedDoor[2],selectedDoor[3],"--",OpenNodesR[randomNode][2],OpenNodesR[randomNode][3])
                OpenNodesR.remove(randomNode)
                # Now add the area to the visitedareas
                # and all nodes from that area
                VisitedAreas = VisitedAreas + [selectedDoor.area_name]  # add the area string
                for doorSearch in LeftSideDoorsList:
                    if doorSearch.area_name in VisitedAreas:
                        OpenNodesL += [doorSearch]
                for doorClean in OpenNodesL:
                    if doorClean in LeftSideDoorsList:
                        LeftSideDoorsList.remove(doorClean)
                # print(len(VisitedAreas),"areas visited")
                # print(VisitedAreas)
        # print("Before connecting OpenNodes")
        # print("Lengths: OpenNodesL",len(OpenNodesL)," and OpenNodesR",len(OpenNodesR))

        # This section is when all areas have been placed and we just need
        # To connect nodes from OpenNodesL and OpenNodesR

        # print("While connecting OpenNodes:")
        while OpenNodesL != [] and OpenNodesR != []:
            # Should only need to keep track of one since they should match 1:1
            randomL = 0
            if len(OpenNodesL) > 1:
                randomL = random.randint(0, len(OpenNodesL) - 1)
            chosenNodeL = OpenNodesL[randomL]
            randomR = 0
            if len(OpenNodesR) > 1:
                randomR = random.randint(0, len(OpenNodesR) - 1)
            chosenNodeR = OpenNodesR[randomR]
            Connections.append((chosenNodeL, chosenNodeR))
            OpenNodesL.remove(chosenNodeL)
            OpenNodesR.remove(chosenNodeR)
            # print("    Lengths: OpenNodesL",len(OpenNodesL)," and OpenNodesR",len(OpenNodesR))
        # print("LeftoverL  ",OpenNodesL)
        # print("LeftoverR  ",OpenNodesR)
        # print(len(Connections), "Connections created:")
        # for item in Connections :
            # print(item[0][2], item[0][3], " << >> ", item[1][2], item[1][3])

        # check for valid escape
        if escape_path(DoorPairs(Connections)):
            connected = True

    return DoorPairs(Connections)


def write_area_doors(door_pairs: DoorPairs, romWriter: RomWriter) -> None:

    # Now I need to read the OG Subversion rom for 12 bytes at address:Node1[1]
    # and write it into the 12 bytes at Node2[0]
    # Also read the OG Subversion Rom for 12 bytes at address:Node2[1]
    # and write it into the 12 bytes at Node1[0]
    # Tada, area rando
    # But I need to do all the reading before I do any writing so that
    # I am getting the pure original Subversion data

    # do a round of reading the door data for each node
    # for pair in Connections :
    #     for node in pair :
    #         addressSending=int(node[0],16)
    #         addressReceiving=int(node[1],16)
    #         rom.seek(addressSending)
    #         sendingBytes=rom.read(12)
    #         node.append(sendingBytes) #this becomes node[3]
    #         rom.seek(addressReceiving)
    #         receivingBytes=rom.read(12)
    #         node.append(receivingBytes)    #this becomes node[4]
    for pair in door_pairs.connections():
        node1 = pair[0]
        node2 = pair[1]
        romWriter.connect_doors(node1, node2)

    # Area rando done?

    # coloring some doors to be flashing
    colorDoorsR = [
        '3fff70',  # CraterR
        '3fffa8',  # CraterR
        '3fe37c',  # FoyerR
        '3ff15e',  # TransitConcourseR
        '3ff1f8',  # TransitConcourseR
        '3fe668',  # NorakPerimeterBR
        '3fe66e',  # NorakPerimeterTR
        '3ff23e',  # CellarR
        '3ff258',  # CellarR
    ]

    colorDoorsL = [
        '3ffec4',  # SunkenNestL
        '3fe352',  # VulnarCanyonL
        '3fe35a',  # VulnarCanyonL
        '3fe686',  # NorakPerimeterBL
        '3ffa2c',  # WestTerminalAccessL
    ]

    for doorlocid in colorDoorsR:
        romWriter.writeBytes(int(doorlocid, 16)+0, b"\x42")  # gray type door
        romWriter.writeBytes(int(doorlocid, 16)+5, b"\x98")  # animals subtype
    for doorlocid in colorDoorsL:
        romWriter.writeBytes(int(doorlocid, 16)+0, b"\x48")  # gray type door
        romWriter.writeBytes(int(doorlocid, 16)+5, b"\x98")  # animals subtype
