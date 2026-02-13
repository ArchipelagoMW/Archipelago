from .auto_generated_types import MarsschemamfCreditstextItem
from .constants.credits_lines import (
    FUSION_STAFF_LINES,
    MARS_CREDITS,
    RDV_CREDITS,
)
from ..credits import CreditsWriter, CreditsLine
from ..rom import Rom

CREDITS_ADDR = 0x74B0B0
CREDITS_LEN = 0x2B98


def write_credits(rom: Rom, data: list[MarsschemamfCreditstextItem]) -> None:
    writer = CreditsWriter(rom, CREDITS_ADDR)
    # Write MARS credits
    lines = [CreditsLine(*line) for line in MARS_CREDITS]
    writer.write_lines(lines)
    # Write RDV credits
    lines = [CreditsLine(*line) for line in RDV_CREDITS]
    writer.write_lines(lines)
    # Write custom credits
    lines = [CreditsLine.from_json(d) for d in data]
    writer.write_lines(lines)
    # Write fusion staff credits
    lines = [CreditsLine(*line) for line in FUSION_STAFF_LINES]
    writer.write_lines(lines)
    # Verify that credits don't exceed existing space
    if writer.addr > CREDITS_ADDR + CREDITS_LEN:
        raise ValueError("Credits exceeded existing space")
