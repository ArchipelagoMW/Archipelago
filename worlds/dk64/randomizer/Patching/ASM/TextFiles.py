"""Write ASM data for the calling of text file elements."""

from randomizer.Patching.Patcher import LocalROM
from randomizer.Patching.Library.ASM import *
from randomizer.Patching.Library.Assets import CompTextFiles, ItemPreview


def writeNewTextFiles(ROM_COPY: LocalROM, offset_dict: dict):
    """Write the new file indexes and text indexes for the new save files."""
    writeFunction(ROM_COPY, 0x8070DE08, Overlay.Static, "getTextData", offset_dict)  # Text file arg translation
    # Seal Preview
    writeValue(ROM_COPY, 0x806C265A, Overlay.Static, CompTextFiles.PreviewsFlavor, offset_dict)
    writeValue(ROM_COPY, 0x806C2666, Overlay.Static, ItemPreview.Seal, offset_dict)
    writeValue(ROM_COPY, 0x806C273E, Overlay.Static, CompTextFiles.PreviewsFlavor, offset_dict)
    writeValue(ROM_COPY, 0x806C275A, Overlay.Static, ItemPreview.Seal, offset_dict)
    # Owl Race
    writeValue(ROM_COPY, 0x806C56E6, Overlay.Static, CompTextFiles.PreviewsFlavor, offset_dict)
    writeValue(ROM_COPY, 0x806C5768, Overlay.Static, 0x24060000 | ItemPreview.OwlRace, offset_dict, 4)
    # Vulture
    writeValue(ROM_COPY, 0x806C50F2, Overlay.Static, CompTextFiles.PreviewsFlavor, offset_dict)
    writeValue(ROM_COPY, 0x806C50F4, Overlay.Static, 0x24060000 | ItemPreview.VultureFreedom, offset_dict, 4)
    # Mermaid
    writeValue(ROM_COPY, 0x806C3E96, Overlay.Static, CompTextFiles.PreviewsFlavor, offset_dict)
    writeValue(ROM_COPY, 0x806C3E9E, Overlay.Static, ItemPreview.MermaidReward, offset_dict)
    writeValue(ROM_COPY, 0x806C3DBE, Overlay.Static, CompTextFiles.PreviewsFlavor, offset_dict)
    writeValue(ROM_COPY, 0x806C3DC6, Overlay.Static, ItemPreview.MermaidMissing, offset_dict)
    writeValue(ROM_COPY, 0x806C3D06, Overlay.Static, CompTextFiles.PreviewsFlavor, offset_dict)
    writeValue(ROM_COPY, 0x806C3D0C, Overlay.Static, 0x24060000 | ItemPreview.MermaidIntro, offset_dict, 4)
    # Llama
    writeValue(ROM_COPY, 0x806C213E, Overlay.Static, CompTextFiles.PreviewsFlavor, offset_dict)
    writeValue(ROM_COPY, 0x806C2142, Overlay.Static, ItemPreview.LlamaTalk, offset_dict)
    # Apple
    writeValue(ROM_COPY, 0x806BF6A6, Overlay.Static, CompTextFiles.PreviewsFlavor, offset_dict)
    writeValue(ROM_COPY, 0x806BF6AE, Overlay.Static, ItemPreview.AppleReward, offset_dict)
    writeValue(ROM_COPY, 0x806BF4B2, Overlay.Static, CompTextFiles.PreviewsFlavor, offset_dict)
    writeValue(ROM_COPY, 0x806BF4BA, Overlay.Static, ItemPreview.ApplePickUp, offset_dict)
    writeValue(ROM_COPY, 0x806BF442, Overlay.Static, CompTextFiles.PreviewsFlavor, offset_dict)
    writeValue(ROM_COPY, 0x806BF448, Overlay.Static, 0x24060000 | ItemPreview.AppleIntro, offset_dict, 4)
    # Rabbit
    writeValue(ROM_COPY, 0x806BED7A, Overlay.Static, CompTextFiles.PreviewsFlavor, offset_dict)
    writeValue(ROM_COPY, 0x806BED7E, Overlay.Static, ItemPreview.RabbitFirstRaceReward, offset_dict)
    writeValue(ROM_COPY, 0x806BED8E, Overlay.Static, CompTextFiles.PreviewsFlavor, offset_dict)
    writeValue(ROM_COPY, 0x806BED96, Overlay.Static, ItemPreview.RabbitFinalRaceReward, offset_dict)
    writeValue(ROM_COPY, 0x806BEA66, Overlay.Static, CompTextFiles.PreviewsFlavor, offset_dict)
    writeValue(ROM_COPY, 0x806BEA6E, Overlay.Static, ItemPreview.RabbitFinalRaceIntro, offset_dict)
    # Wrinkly
    writeValue(ROM_COPY, 0x8069E186, Overlay.Static, CompTextFiles.Wrinkly, offset_dict)
