from settings import get_settings
from worlds.Files import APProcedurePatch, APTokenMixin, APPatchExtension


def get_base_rom_as_bytes() -> bytes:
    with open(get_settings().sonic_rush_options.rom_file, "rb") as infile:
        base_rom_bytes = bytes(infile.read())
    return base_rom_bytes


class SonicRushPathExtension(APPatchExtension):
    game = "Sonic Rush"


class SonicRushProcedurePatch(APProcedurePatch, APTokenMixin):
    # settings for what the end file is going to look like
    game = "Sonic Rush"
    hash = "2d7e5a3d40c4d74062599e0a573cc447"
    patch_file_ending = ".aprush"
    result_file_ending = ".nds"
    procedure = [
        ("apply_bsdiff4", ["base_patch.bsdiff4"]),
        ("apply_tokens", ["token_data.bin"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_as_bytes()


def write_tokens(patch: SonicRushProcedurePatch) -> None:
    patch.write_file("token_data.bin", patch.get_token_binary())
