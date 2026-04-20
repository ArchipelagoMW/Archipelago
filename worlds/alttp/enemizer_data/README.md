These files are vendored from the upstream Enemizer compiled release that was already present locally in
`/home/alchav/PycharmProjects/Archipelago/EnemizerCLI`.

Source details:

- Upstream project: `Ijwu/Enemizer`
- Release family: `7.1`
- Library version from `EnemizerCLI/EnemizerCLI.Core.deps.json`: `EnemizerLibrary/7.1.0`

Vendored artifacts:

- `enemizerBasePatch.json`
- `exported_symbols.txt`

Archipelago-authored companion metadata:

- `default_dungeon_room_enemies.json`
- `enemy_room_metadata.json`
- `enemy_sprite_requirements.json`
- `overworld_enemy_metadata.json`
- `pot_shuffle.json`
- `room_names.json`

Purpose:

- `enemizerBasePatch.json` contains the generated base patch Enemizer applies before feature-specific randomization.
- `default_dungeon_room_enemies.json` contains the default dungeon enemy placements, key flags, and coordinates used by
  ALTTP room-combat logic when enemy shuffle is off. This copy exists so logic and unit tests do not need access to a
  local base ROM.
- `exported_symbols.txt` contains the assembled symbol map consumed by Enemizer's runtime code for ROM addresses.

These copies exist so Archipelago can transition away from depending on an external Enemizer executable and release
bundle layout.
