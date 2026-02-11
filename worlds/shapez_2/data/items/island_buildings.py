from .. import ItemData
from ..classification import *

always: dict[str, ItemData] = {
    "Space Pipe": ItemData(1003, always_progression, "RemoteSpacePipe", ("SpacePipesGroup", ), 1),
    "Rails": ItemData(1006, always_useful, "RemoteRails", ("TrainLaunchersGroup", "TrainCatchersGroup",
                                                           "RailLiftUp1X1X2Group", "RailLiftDown1X1X2Group",
                                                           "RailLiftUp1X1X3Group", "RailLiftDown1X1X3Group"), 1),
    "Shape (Un)loader": ItemData(1007, always_useful, "RemoteShapeUnLoader", ("TrainShapeLoadersGroup", "TrainShapeUnloadersGroup"), 1),
    "Shape Wagon": ItemData(1008, always_useful, "RemoteShapeWagon", ("ShapeCargoFactoriesGroup", ), 1),
    "Red Trains": ItemData(1009, always_useful, "RemoteRedTrains", ("RedTrainProducerGroup", "RedRailGroup", ), 1),
    "1x3 Foundation": ItemData(1010, always_progression_skip_balancing, "Remote1x3Foundation", ("FoundationGroup_1x3", ), 1),
    "1x4 Foundation": ItemData(1011, always_progression_skip_balancing, "Remote1x4Foundation", ("FoundationGroup_1x4", ), 1),
    "3-Blocks L Foundation": ItemData(1012, always_progression_skip_balancing, "Remote3BlocksLFoundation", ("FoundationGroup_L3", ), 1),
    "4-Blocks L Foundation": ItemData(1013, always_progression_skip_balancing, "Remote4BlocksLFoundation", ("FoundationGroup_L4", ), 1),
    "T Foundation": ItemData(1014, always_progression_skip_balancing, "RemoteTFoundation", ("FoundationGroup_T4", ), 1),
    "S Foundation": ItemData(1015, always_progression_skip_balancing, "RemoteSFoundation", ("FoundationGroup_S4", ), 1),
    "Cross Foundation": ItemData(1016, always_progression_skip_balancing, "RemoteCrossFoundation", ("FoundationGroup_C5", ), 1),
    "2x2 Foundation": ItemData(1017, always_progression_skip_balancing, "Remote2x2Foundation", ("FoundationGroup_2x2", ), 1),
    "2x3 Foundation": ItemData(1018, always_progression_skip_balancing, "Remote2x3Foundation", ("FoundationGroup_2x3", ), 1),
    "2x4 Foundation": ItemData(1019, always_progression_skip_balancing, "Remote2x4Foundation", ("FoundationGroup_2x4", ), 1),
    "3x3 Foundation": ItemData(1020, always_progression_skip_balancing, "Remote3x3Foundation", ("FoundationGroup_3x3", ), 1),
    "Green Trains": ItemData(1021, always_useful, "RemoteGreenTrains", ("GreenRailGroup", "GreenTrainProducerGroup", ), 1),
    "Blue Trains": ItemData(1022, always_useful, "RemoteBlueTrains", ("BlueRailGroup", "BlueTrainProducerGroup", ), 1),
    "Cyan Trains": ItemData(1023, always_useful, "RemoteCyanTrains", ("CyanRailGroup", "CyanTrainProducerGroup", ), 1),
    "Magenta Trains": ItemData(1024, always_useful, "RemoteMagentaTrains", ("MagentaTrainProducerGroup", "MagentaRailGroup"), 1),
    "Yellow Trains": ItemData(1025, always_useful, "RemoteYellowTrains", ("YellowTrainProducerGroup", "YellowRailGroup", ), 1),
    "White Trains": ItemData(1026, always_useful, "RemoteWhiteTrains", ("WhiteTrainProducerGroup", "WhiteRailGroup", ), 1),
    "Fluid (Un)loader": ItemData(1027, always_useful, "RemoteFluidUnLoader", ("TrainFluidLoadersGroup", "TrainFluidUnloadersGroup"), 1),
    "Fluid Wagon": ItemData(1028, always_useful, "RemoteFluidWagon", ("FluidCargoFactoriesGroup", ), 1),
    "Shape Wagon Transfer": ItemData(1029, always_useful, "RemoteShapeWagonTransfer", ("TrainShapeTransferGroup", ), 1),
    "Fluid Wagon Transfer": ItemData(1030, always_useful, "RemoteFluidWagonTransfer", ("TrainFluidTransferGroup", ), 1),
    "Train Quick Stop": ItemData(1031, always_useful, "RemoteTrainQuickStop", ("TrainQuickStationsGroup", ), 1),
    "Train Wait Stop": ItemData(1032, always_useful, "RemoteTrainWaitStop", ("TrainWaitStationsGroup", ), 1),
    "Filler Wagon": ItemData(1033, always_filler, "RemoteFillerWagon", ("FillerCargoFactoriesGroup", ), 1),
    # Might make using roller coasters possible even without the supporter edition
    # "Roller Coaster": ItemData(000, always_filler, "RemoteRollerCoaster", (
    #     "TrainTwistersGroup", "TrainLoopsGroup", "RailLiftUp2X1X2Group", "RailLiftDown2X1X2Group",
    # ), 1),
}

starting: dict[str, ItemData] = {
    "Space Belt": ItemData(1100, always_progression, "RemoteSpaceBelt", ("SpaceBeltsGroup", ), 1),
    "1x1 Foundation": ItemData(1105, always_progression_skip_balancing, "Remote1x1Foundation", ("FoundationGroup_1x1", ), 1),
    "1x2 Foundation": ItemData(1106, always_progression_skip_balancing, "Remote1x2Foundation", ("FoundationGroup_1x2", ), 1),
}

miners: dict[str, ItemData] = {
    "Shape Miner": ItemData(1200, always_progression, "RemoteShapeMiner", ("ShapeMinerExtractorsGroup", ), 1),
    "Fluid Miner": ItemData(1201, always_progression, "RemoteFluidMiner", ("FluidMinerExtractorsGroup", ), 1),
    "Shape Miner Extension": ItemData(1202, always_useful, "RemoteShapeMinerExtension", ("ShapeMinerChainsGroup", ), 1),
    "Fluid Miner Extension": ItemData(1203, always_useful, "RemoteFluidMinerExtension", ("FluidMinerChainsGroup", ), 1),
    "Shape Miner + Extension": ItemData(1204, always_progression, "RemoteShapeMinerPlusExtension", ("ShapeMinerExtractorsGroup", "ShapeMinerChainsGroup"), 1),
    "Fluid Miner + Extension": ItemData(1205, always_progression, "RemoteFluidMinerPlusExtension", ("FluidMinerExtractorsGroup", "FluidMinerChainsGroup"), 1),
}
