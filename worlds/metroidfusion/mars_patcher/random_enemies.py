import random

from .constants.game_data import spriteset_count, spriteset_ptrs
from .mf.constants.enemies import ENEMY_TYPES, EnemyType
from .mf.constants.game_data import sprite_vram_sizes
from .rom import Rom


def randomize_enemies(rom: Rom) -> None:
    # Setup enemy types dictionary
    enemy_types = {k: v[1] for k, v in ENEMY_TYPES.items()}

    # Get graphics info for each enemy
    size_addr = sprite_vram_sizes(rom)
    gfx_rows = {}
    for en_id in enemy_types:
        size = rom.read_32(size_addr + (en_id - 0x10) * 4)
        gfx_rows[en_id] = size // 0x800

    # Get replacement pools
    replacements: dict[EnemyType, list[int]] = {t: [] for t in EnemyType}
    for en_id, en_type in enemy_types.items():
        replacements[en_type].append(en_id)
        if en_type == EnemyType.CRAWLING:
            replacements[EnemyType.GROUND].append(en_id)
            replacements[EnemyType.CEILING].append(en_id)
            replacements[EnemyType.GROUND_CEILING].append(en_id)
            replacements[EnemyType.WALL].append(en_id)
        elif en_type == EnemyType.GROUND_CEILING:
            replacements[EnemyType.GROUND].append(en_id)
            replacements[EnemyType.CEILING].append(en_id)
        # Ground, Ceiling, Wall, and Flying cannot replace others

    # Randomize spritesets
    ss_ptrs = spriteset_ptrs(rom)
    for i in range(spriteset_count(rom)):
        spriteset_addr = rom.read_ptr(ss_ptrs + i * 4)
        used_gfx_rows: dict[int, int] = {}
        spriteset = get_spriteset(rom, spriteset_addr)
        for j, (en_id, gfx_row) in enumerate(spriteset):
            # Skip enemies that aren't randomized
            if en_id not in enemy_types:
                continue

            # Check if sprite shares graphics with one that's never randomized
            if any(
                en_id != other_id and gfx_row == other_row and other_id not in enemy_types
                for other_id, other_row in spriteset
            ):
                continue

            # Check if sprite shares graphics with one that's already randomized
            addr = spriteset_addr + (j * 2)
            if gfx_row in used_gfx_rows:
                new_id = used_gfx_rows[gfx_row]
                rom.write_8(addr, new_id)
                continue

            # Choose randomly and assign
            en_type = enemy_types[en_id]
            row_count = gfx_rows[en_id]
            candidates = replacements[en_type]
            random.shuffle(candidates)
            for new_id in candidates:
                new_row_count = gfx_rows[new_id]
                # New enemy must use same or fewer graphics rows
                if new_row_count <= row_count:
                    rom.write_8(addr, new_id)
                    used_gfx_rows[gfx_row] = new_id
                    break


def get_spriteset(rom: Rom, addr: int) -> list[tuple[int, int]]:
    """Returns a list of (sprite ID, graphics row) tuples in the spriteset
    at the provided address."""
    spriteset: list[tuple[int, int]] = []
    for _ in range(0xF):
        en_id = rom.read_8(addr)
        if en_id == 0:
            break
        gfx_row = rom.read_8(addr + 1)
        spriteset.append((en_id, gfx_row))
        addr += 2
    return spriteset
