These modules are vendored/generated from the upstream Enemizer compiled release and source that were already present
locally in `/home/alchav/PycharmProjects/Archipelago/EnemizerCLI` and `/home/alchav/PycharmProjects/Archipelago/Enemizer`.

Source details:

- Upstream project: `Ijwu/Enemizer`
- Release family: `7.1`
- Library version from `EnemizerCLI/EnemizerCLI.Core.deps.json`: `EnemizerLibrary/7.1.0`

Vendored data modules:

- `base_patch_data.py`
- `symbols.py`
- `dungeon_sprite_addresses.py`

Archipelago-authored companion data modules:

- `default_dungeon_room_enemies.py`
- `enemy_room_metadata.py`
- `enemy_sprite_requirements.py`
- `overworld_enemy_metadata.py`
- `pot_shuffle_data.py`
- `room_names.py`

Purpose:

- `base_patch_data.py` contains the generated base patch Enemizer applies before feature-specific randomization.
- `default_dungeon_room_enemies.py` contains the default dungeon enemy placements, key flags, and coordinates used by
  ALTTP room-combat logic when enemy shuffle is off. This copy exists so logic and unit tests do not need access to a
  local base ROM.
- `symbols.py` contains the assembled symbol map consumed by Enemizer's runtime code for ROM addresses.
- `dungeon_sprite_addresses.py` contains dungeon sprite slot metadata derived from Enemizer's source tables and keyed-enemy address list.
- `enemy_room_metadata.py` and `overworld_enemy_metadata.py` contain room and area grouping/randomization constraints.
- `enemy_sprite_requirements.py` contains the sprite metadata used by the native enemy shuffle implementation.
- `pot_shuffle_data.py` contains the native pot shuffle room/item source data.
- `room_names.py` contains the named room lookup table used by ALTTP room-combat logic.
