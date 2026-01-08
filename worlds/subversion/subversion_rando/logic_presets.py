from .trick import Trick
from .trick_data import Tricks


casual: frozenset[Trick] = frozenset()  # empty

medium = frozenset([
    Tricks.infinite_bomb_jump,
    Tricks.crouch_or_downgrab,
    Tricks.dark_easy,
    Tricks.dark_medium,
    Tricks.ggg,
    Tricks.gravity_jump,
    Tricks.hell_run_easy,
    Tricks.hell_run_medium,
    Tricks.wall_jump_precise,
    Tricks.morph_jump_3_tile_water,
    Tricks.morph_jump_4_tile,
    Tricks.movement_moderate,
    Tricks.short_charge_2,
    Tricks.wave_gate_glitch,
])

expert = frozenset(t for t in vars(Tricks).values() if isinstance(t, Trick))  # all

assert all(isinstance(t, Trick) for t in expert), f"{list(expert)}"


def custom_logic_str_from_tricks(tricks: frozenset[Trick]) -> str:
    bits = 0
    count = 0
    output = ""

    def add_byte() -> None:
        nonlocal output
        if bits < 0x10:
            output += "0"
        output += hex(bits)[2:]

    for t in vars(Tricks).values():
        if isinstance(t, Trick):
            count += 1
            bits <<= 1
            if t in tricks:
                bits |= 1
            if count % 8 == 0:
                add_byte()
                bits = 0
    # print(count)
    last_group_count = count % 8
    # print(f"{last_group_count=} {bin(bits)=}")
    if last_group_count:
        pad = 8 - last_group_count
        # print(f"{pad=}")
        bits <<= pad
        add_byte()

    return output


_mask_2_trick = {
    "800000000000": Tricks.infinite_bomb_jump,
    "400000000000": Tricks.sbj_underwater_no_hjb,
    "200000000000": Tricks.sbj_underwater_w_hjb,
    "100000000000": Tricks.sbj_no_hjb,
    "080000000000": Tricks.sbj_w_hjb,
    "040000000000": Tricks.sbj_wall,
    "020000000000": Tricks.uwu_2_tile,
    "010000000000": Tricks.uwu_2_tile_surface,
    "008000000000": Tricks.gravity_jump,
    "004000000000": Tricks.hell_run_hard,
    "002000000000": Tricks.hell_run_medium,
    "001000000000": Tricks.hell_run_easy,
    "000800000000": Tricks.movement_moderate,
    "000400000000": Tricks.movement_zoast,
    "000200000000": Tricks.wall_jump_delayed,
    "000100000000": Tricks.wall_jump_precise,
    "000080000000": Tricks.crumble_jump,
    "000040000000": Tricks.mockball_hard,
    "000020000000": Tricks.morphless_tunnel_crawl,
    "000010000000": Tricks.morph_jump_3_tile,
    "000008000000": Tricks.morph_jump_4_tile,
    "000004000000": Tricks.morph_jump_3_tile_up_1,
    "000002000000": Tricks.morph_jump_3_tile_water,
    "000001000000": Tricks.crouch_or_downgrab,
    "000000800000": Tricks.crouch_precise,
    "000000400000": Tricks.dark_easy,
    "000000200000": Tricks.dark_medium,
    "000000100000": Tricks.dark_hard,
    "000000080000": Tricks.freeze_hard,
    "000000040000": Tricks.wave_gate_glitch,
    "000000020000": Tricks.ggg,
    "000000010000": Tricks.clip_crouch,
    "000000008000": Tricks.short_charge_2,
    "000000004000": Tricks.short_charge_3,
    "000000002000": Tricks.short_charge_4,
    "000000001000": Tricks.xray_climb,
    "000000000800": Tricks.ice_clip,
    "000000000400": Tricks.moonfall_clip,
    "000000000200": Tricks.super_sink_easy,
    "000000000100": Tricks.super_sink_hard,
    "000000000080": Tricks.patience,
    "000000000040": Tricks.plasma_gate_glitch,
    "000000000020": Tricks.searing_gate_tricks,
    "000000000010": Tricks.spazer_into_lower_pirate_lab,
}
# table made with this code:
# for t in vars(Tricks).values():
#     if isinstance(t, Trick):
#         print(f'    "{custom_logic_str_from_tricks(frozenset([t]))}": Tricks.{trick_name_lookup[t]},')


def custom_logic_tricks_from_str(logic_str: str) -> frozenset[Trick]:
    """ raises ValueError if invalid logic string """
    tricks: list[Trick] = []

    expected_len = len(next(iter(_mask_2_trick.keys())))

    logic_str = logic_str.strip()[:expected_len]
    if len(logic_str) < expected_len:
        logic_str += "0" * (expected_len - len(logic_str))
    try:
        logic_int = int(logic_str, 16)
    except ValueError:
        raise ValueError("invalid logic string")

    for mask_str, t in _mask_2_trick.items():
        mask = int(mask_str, 16)
        if mask & logic_int:
            tricks.append(t)

    return frozenset(tricks)
