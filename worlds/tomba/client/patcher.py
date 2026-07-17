from CommonClient import logger

from .compiler import Compiler
from .retroarch import RetroArch
from ..constants import Addresses, BittingPlantFlowerState, SectionEventMask

FEATURE_PATCH = "worlds/tomba/client/src/interface.asm"
ADD_ITEM_PATCH = "worlds/tomba/client/src/add_item.asm"


class PatchException(Exception):
    pass


class Patcher:
    def __init__(self, playstation: RetroArch):
        self.playstation = playstation

        try:
            compiler = Compiler()
            # Patch a custom handler triggerred on game sprite updates
            self.interface_patch = compiler.compile(FEATURE_PATCH)

            # Hook to call the custom handler
            self.handler_hook = "542C0008"

            # Patch receive item method to create a list of found items in game instead
            self.add_item_patch = compiler.compile(ADD_ITEM_PATCH)
        except Exception as e:
            logger.critical(e)
            raise PatchException("Unable to initialize the patching interface")

    async def patch_game(self):
        """Patch a custom method to play SFX on demand"""
        logger.info("Patching custom methods...")

        add_item_patch = bytes.fromhex(self.add_item_patch)
        interface_patch = bytes.fromhex(self.interface_patch)
        interface_hook = bytes.fromhex(self.handler_hook)

        self.playstation.write_memory(Addresses.PATCH_ADD_ITEM, add_item_patch)
        self.playstation.write_memory(Addresses.PATCH_INTERFACE_HANDLER, interface_patch)
        self.playstation.write_memory(Addresses.PATCH_INTERFACE_HOOK, interface_hook)

        # Prevent missable location
        self.playstation.write_memory(Addresses.BITTING_PLANT_FLOWER_STATE, BittingPlantFlowerState.BLOOM.to_bytes())

        # Indicates that the game is patched
        self.playstation.write_memory(Addresses.IS_PATCHED, bytes.fromhex("01"))

        logger.info("Game patched")

    async def patch_save(self):
        """Pre-trigger some event to avoid glitches"""
        await self.playstation.set_flag(
            Addresses.SECTION_STATE + 4, SectionEventMask.SECTION_1_BITTING_FLOWER_BLUE_APPLE
        )

    async def is_patched(self) -> bool:
        return (await self.playstation.async_read_memory(Addresses.IS_PATCHED))[0] != 0

    async def is_save_patched(self) -> bool:
        return await self.playstation.get_flag(
            Addresses.SECTION_STATE + 4, SectionEventMask.SECTION_1_BITTING_FLOWER_BLUE_APPLE
        )
