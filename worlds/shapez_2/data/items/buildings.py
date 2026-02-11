from .. import ItemData
from ..classification import *

always: dict[str, ItemData] = {
    "Painter": ItemData(1, always_progression, "RemotePainter", ("PainterDefaultVariant", ), 0),
    "Pump": ItemData(2, always_progression, "RemotePump", ("PumpDefaultVariant", ), 0),
    "Pipe": ItemData(3, always_progression, "RemotePipe", ("PipeDefaultVariant", "Pipe1LayerVariant",
                                                           "Pipe2LayerVariant", "FluidPortSenderVariant",
                                                           "FluidPortReceiverVariant"), 0),
    "Color Mixer": ItemData(4, always_progression, "RemoteColorMixer", ("MixerDefaultVariant", ), 0),
    "Crystal Generator": ItemData(5, always_progression, "RemoteCrystalGenerator", ("CrystalGeneratorDefaultVariant", ), 0),
    "Trash": ItemData(6, always_useful, "RemoteTrash", ("TrashDefaultVariant", ), 0),
    "Label": ItemData(7, always_filler, "RemoteLabel", ("LabelDefaultVariant", ), 0),
    "Overflow Splitter": ItemData(8, always_useful, "RemoteOverflowSplitter", ("SplitterOverflowVariant", ), 0),
    "Wires": ItemData(9, always_useful, "RemoteWires", ("WireDefaultVariant", "WireBridgeVariant",
                                                        "WireTransmitterSenderVariant", "WireTransmitterReceiverVariant"), 0),
    "Signal Producer": ItemData(10, always_useful, "RemoteSignalProducer", ("ConstantSignalDefaultVariant", ), 0),
    "Belt Filter": ItemData(11, always_useful, "RemoteBeltFilter", ("BeltFilterDefaultVariant", ), 0),
    "Belt Reader": ItemData(12, always_useful, "RemoteBeltReader", ("BeltReaderDefaultVariant", ), 0),
    "Pipe Gate": ItemData(13, always_useful, "RemotePipeGate", ("PipeGateDefaultVariant", ), 0),
    "Display": ItemData(14, always_filler, "RemoteDisplay", ("DisplayDefaultVariant", ), 0),
    "Button": ItemData(15, always_useful, "RemoteButton", ("ButtonDefaultVariant", ), 0),
    "Logic Gates": ItemData(16, always_useful, "RemoteLogicGates",
                            ("LogicGateAndVariant", "LogicGateOrVariant", "LogicGateIfVariant",
                             "LogicGateXOrVariant", "LogicGateNotVariant", "LogicGateCompareVariant"), 0),
    "Simulated Buildings": ItemData(17, always_useful, "RemoteSimulatedBuildings",
                                    ("VirtualRotatorDefaultVariant", "VirtualAnalyzerDefaultVariant",
                                     "VirtualUnstackerDefaultVariant","VirtualStackerDefaultVariant",
                                     "VirtualHalfCutterDefaultVariant", "VirtualPainterDefaultVariant",
                                     "VirtualPinPusherDefaultVariant", "VirtualCrystalGeneratorDefaultVariant",
                                     "VirtualHalvesSwapperDefaultVariant"), 0),
    "Global Signal Transmitter": ItemData(18, always_useful, "RemoteGlobalSignalTransmission",
                                          ("ControlledSignalReceiverVariant", "ControlledSignalTransmitterVariant"), 0),
    "Operator Signal Receiver": ItemData(19, always_useful, "RemoteOperatorSignalReceiver", ("WireGlobalTransmitterReceiverVariant", ), 0),
    "Fluid Tank": ItemData(20, always_useful, "RemoteFluidTank", ("FluidStorageDefaultVariant", ), 0),
    "Stacker": ItemData(21, always_progression, "RemoteStacker", ("StackerStraightVariant", ), 0),
    "Stacker (Bent)": ItemData(22, always_progression, "RemoteStackerBent", ("StackerDefaultVariant", ), 0),
    "Rotator (CW)": ItemData(23, always_progression, "RemoteRotatorCW", ("RotatorOneQuadVariant", ), 0),
    "Rotator (CCW)": ItemData(24, always_progression, "RemoteRotatorCCW", ("RotatorOneQuadCCWVariant", ), 0),
    "Rotator (180)": ItemData(25, always_progression, "RemoteRotator180", ("RotatorHalfVariant", ), 0),
}

starting: dict[str, ItemData] = {
    "Conveyor Belt": ItemData(100, always_progression, "RemoteConveyorBelt",
                              ("BeltDefaultVariant", "BeltPortSenderVariant", "BeltPortReceiverVariant",
                               "Merger2To1Variant", "Merger3To1Variant", "MergerTShapeVariant", "Splitter1To2Variant",
                               "Splitter1To3Variant", "SplitterTShapeVariant", "Lift1LayerVariant",
                               "Lift2LayerVariant"), 0),
    "Extractor": ItemData(101, always_progression, "RemoteExtractor", ("ExtractorDefaultVariant", ), 0),
}

simple_processors: dict[str, ItemData] = {
    "Half Destroyer": ItemData(200, always_progression, "RemoteHalfDestroyer", ("CutterHalfVariant", ), 0),
    "Pin Pusher": ItemData(203, always_progression, "RemotePinPusher", ("PinPusherDefaultVariant", ), 0),
    "Cutter": ItemData(204, always_progression, "RemoteCutter", ("CutterDefaultVariant", ), 0),
    "Swapper": ItemData(205, always_progression, "RemoteSwapper", ("HalvesSwapperDefaultVariant", ), 0),
}

sandbox: dict[str, ItemData] = {
    "Sandbox Item Producer": ItemData(300, always_progression, "RemoteSandboxItemProducer", ("SandboxItemProducerDefaultVariant", ), 0),
    "Sandbox Fluid Producer": ItemData(301, always_progression, "RemoteSandboxFluidProducer", ("SandboxFluidProducerDefaultVariant", ), 0),
}
