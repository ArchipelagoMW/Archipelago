from worlds._bizhawk.client import BizHawkClient
from NetUtils import NetworkItem
from typing import List, Optional
import worlds._bizhawk as bizhawk

from worlds._bizhawk.context import BizHawkClientContext

EXPECTED_ROM_NAME= "DRAGON WARRIOR"

class DragonWarriorClient(BizHawkClient):
    game = "Dragon Warrior"
    system = "NES"
    patch_suffix = ".apdw"
    item_queue: List[NetworkItem] = []
    rom: Optional[bytes] = None

    def __init__(self) -> None:
        super().__init__()

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        from CommonClient import logger

        try:
            # Check ROM name/patch version
            rom_name_bytes = (
                await bizhawk.read(ctx.bizhawk_ctx, [(0x1FFE0, 16, "PRG ROM")])
            )[0]

            rom_name = bytes([byte for byte in rom_name_bytes if byte != 0]).decode(
                "ascii"
            )
            if not rom_name.startswith(EXPECTED_ROM_NAME):
                logger.info(
                    "ERROR: Rom is not valid!"
                )
                return False
        except UnicodeDecodeError:
            return False
        except bizhawk.RequestFailedError:
            return False  # Should verify on the next pass

        ctx.game = self.game
        ctx.items_handling = 0b111

        return True