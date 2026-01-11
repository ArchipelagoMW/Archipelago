import zipfile
import orjson
from typing import TYPE_CHECKING
from zipfile import ZipFile

from ...ndspy.rom import NintendoDSRom
from ...ndspy.code import saveOverlayTable

if TYPE_CHECKING:
    from ...rom import PokemonBWPatch


overlay_offset = 0x02187f20
# offsets[grass=0/surfing=1/fishing=2][slot_num] = [0x..., 0x...]
# only slot sums for 0...10 or 0...3
offsets: list[list[list[int]]] = [
    [
        [0x021a9e06],
        [0x021a9e10, 0x021a9e18],
        [0x021a9e1c, 0x021a9e24],
        [0x021a9e28, 0x021a9e30],
        [0x021a9e34, 0x021a9e3c],
        [0x021a9e40, 0x021a9e48],
        [0x021a9e4c, 0x021a9e54],
        [0x021a9e58, 0x021a9e60],
        [0x021a9e64, 0x021a9e6c],
        [0x021a9e70],
        [0x021a9e78],
    ], [
        [0x021a9e8a],
        [0x021a9e94, 0x021a9e9c],
        [0x021a9ea0, 0x021a9ea8],
        [0x021a9eac],
    ], [
        [0x021a9ebe],
        [0x021a9ec6],
        [0x021a9ece],
        [0x021a9ed6],
    ],
]


def write_patch(bw_patch_instance: "PokemonBWPatch", opened_zipfile: zipfile.ZipFile) -> None:
    rates = bw_patch_instance.world.options.modify_encounter_rates.custom_rates
    if rates is not None:
        opened_zipfile.writestr("encounter_rates.json", orjson.dumps({
            "choice": "custom",
            "rates": rates
        }))
    else:
        opened_zipfile.writestr("encounter_rates.json", orjson.dumps({
            "choice": bw_patch_instance.world.options.modify_encounter_rates.current_key,
            "rates": []
        }))


def patch(rom: NintendoDSRom, world_package: str, bw_patch_instance: "PokemonBWPatch", files_dump: ZipFile) -> None:
    from ...data.locations.encounters.rates import tables

    rates_json: dict[str, str | list[list[int]]] = orjson.loads(bw_patch_instance.get_file("encounter_rates.json"))
    if rates_json["choice"] == "custom":
        rates: list[list[int]] = rates_json["rates"]
    else:
        rates: tuple[list[int], ...] = tables[rates_json["choice"]]
    rates_sum: list[list[int]] = [[rates[0][0]], [rates[1][0]], [rates[2][0]]]
    for slot in range(1, 11):
        rates_sum[0].append(rates[0][slot] + rates_sum[0][-1])
    for slot in range(1, 4):
        rates_sum[1].append(rates[1][slot] + rates_sum[1][-1])
    for slot in range(1, 4):
        rates_sum[2].append(rates[2][slot] + rates_sum[2][-1])

    overlay_table = rom.loadArm9Overlays()
    ov21 = overlay_table[21]
    data = ov21.data if isinstance(ov21.data, bytearray) else bytearray(ov21.data)
    for method in range(3):
        for slot in range(len(offsets[method])):
            for i in range(len(offsets[method][slot])):
                data[offsets[method][slot][i] - overlay_offset] = rates_sum[method][slot]
    data[0x021a9e7b - overlay_offset] = 0xd2  # changing that one bne opcode to bcs
    ov21.data = data
    rom.files[ov21.fileID] = ov21.save(compress=True)
    files_dump.writestr("ov21", rom.files[ov21.fileID])
    rom.arm9OverlayTable = saveOverlayTable(overlay_table)
