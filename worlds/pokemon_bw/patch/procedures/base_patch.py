import io
from typing import NamedTuple, TYPE_CHECKING
from zipfile import ZipFile

from ...ndspy.rom import NintendoDSRom
from ...ndspy.narc import NARC
import pkgutil

from .. import otpp

if TYPE_CHECKING:
    from ...rom import PokemonBWPatch


class PatchProcedure(NamedTuple):
    otpp_patches: list[int, bytes]
    narc: NARC
    narc_filename: str


def patch(rom: NintendoDSRom, world_package: str, bw_patch_instance: "PokemonBWPatch", files_dump: ZipFile) -> None:
    from ...data import version

    pad = rom.pad088[:0x15] + bytes(version.rom()) + bw_patch_instance.player_name.encode()
    rom.pad088 = pad + bytes(0x38 - len(pad))

    # open patch files zip and create dict of patch procedures
    base_otpp_zip = pkgutil.get_data(world_package, "patch/base_otpp.zip")
    buffer = io.BytesIO(base_otpp_zip)
    procedures: dict[str, list[tuple[int, bytes]]] = {}
    with ZipFile(buffer, "r") as opened_zip:
        # go through all patch files
        for zip_info in opened_zip.filelist:
            filename = zip_info.filename
            # only data/a files are handled for now
            if "data" in filename:
                if not zip_info.is_dir():
                    # get strings and indexes
                    filename_path_list = filename.split("/")
                    narc_filename = "/".join(filename_path_list[1:-1])  # remove "data" and in-narc index
                    narc_index = int(filename_path_list[-1])
                    # add procedure to dict
                    if narc_filename not in procedures:
                        procedures[narc_filename] = [(narc_index, opened_zip.read(filename))]
                    else:
                        procedures[narc_filename].append((narc_index, opened_zip.read(filename)))
            else:
                raise Exception(f"Base patch file not in data subfolder: {filename}")
    # apply patches to each narc
    for narc_filename, proc_list in procedures.items():
        # load correct narc
        source_narc = NARC(rom.getFileByName(narc_filename))
        # apply each patch to corresponding file inside narc
        for proc in proc_list:
            source_narc.files[proc[0]] = otpp.patch(source_narc.files[proc[0]], proc[1])
        # write patched narc to rom
        rom.setFileByName(narc_filename, source_narc.save())
