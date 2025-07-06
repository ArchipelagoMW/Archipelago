# Pokémon Gen 3 Adjuster for Pokémon Emerald

1) [Introduction](#introduction)
2) [Quickstart](#quickstart)
3) [Sprite Pack](#sprite-pack)
    1) [Extracting Resources from the ROM](#extracting-resources-from-the-rom)
    2) [Pokémon Folder Specifications](#pokemon-folder-specifications)
        1) [Pokémon Folder Sprites](#pokemon-folder-sprites)
        2) [Pokémon Folder Exceptions](#pokemon-folder-exceptions)
    3) [Player Folder Specifications](#player-folder-specifications)
        1) [Player Folder Palettes](#player-folder-palettes)
        2) [Player Folder Sprites](#player-folder-sprites)
        3) [Player Folder Sprite Size Override](#player-folder-sprite-size-override)
4) [Pokémon Data Edition](#pokemon-data-edition)
5) [Applying the Sprite Pack](#applying-the-sprite-pack)

## Introduction

The Pokémon Gen 3 Adjuster allows anyone to apply a sprite pack to Pokémon Emerald, Pokémon Firered and Pokémon
Leafgreen, in order to personnalize runs made in Archipelago with these games.

While its main goal is to apply said sprite packs to an AP-patched version of said ROMs, the tool also allows the
patching of vanilla ROMs.

## Quickstart

If you want to quickly get into using the adjuster, you can create a sprite pack by
[extracting resources from the ROM](#extracting-resources-from-the-rom).

Once you have said pack, modify the sprites in it at your leisure, but feel free to check the specifications for each
folder if you encounter any problem.

Once a ROM (or AP patch) and a sprite pack is given, you just need to [apply the sprite pack](#applying-the-sprite-pack)
and run your adjusted ROM in your emulator of choice, and you're good to go!

## Sprite Pack

A sprite pack is a folder containing folders with specific names for the various objects you want to replace. Here
is an example of a valid sprite pack, who replaces some resources from the Pokémon Latios and the Player Brendan:

```
Sprite Pack/
    Brendan/
        battle_back.png
        battle_front.png
    Latios/
        front_anim.png
        back.png
```

<u>Note:</u> If sprites contain several frames, then said frames must be vertical: a `64x64px` sprite with `2`
frames will require a `64x128px` sprite.

<u>**Warning:**</u> All sprites used in sprite packs must be <u>Indexed PNG</u> files. Some pixel editing
programs such as <u>Aseprite</u> allow you to make those easily instead of standard PNG files.

Different types of folder exists: mainly Pokémon folders, and Player folders.

### Extracting Resources from the ROM

The Pokémon Gen 3 Adjuster allows you to extract resources from any object handled by the adjuster. In order to
extract a resource, a ROM or .apemerald patch must be given.

Once a valid ROM or patch is given, a new module will appear within the adjuster named `Sprite Extractor`. In it,
you can either select one specific object to extract the resources of using the field given in it, or you can
extract all resources from the ROM with one button press.

Once you press any of the `Extract` buttons, you must select a folder in which either all resources from the
currently selected object will be extracted, or in which a complete sprite pack will be extracted.

<u>Note:</u> If you try to extract resources in a folder that doesn't exist, the adjuster will create said folders
first.

### Pokémon Folder Specifications

Pokémon folder names correspond to the name of the 386 Pokémon available within Generation 3 of Pokémon, with some
extras and exceptions. Here is a list of them:

- Nidoran♂ => Nidoran Male
- Nidoran♀ => Nidoran Female
- Unown => Unown A
- All letter shapes of Unown have been added as Unown B, Unown C... Unown Z
- Unown ! => Unown Exclamation Mark
- Unown ? => Unown Question Mark
- The Egg folder has been added

#### Pokémon Folder Sprites

Generally, Pokémon folders will handle these sprites:

- `front_anim.png`: This sprite replaces the animation used when displaying the enemy's Pokémon sprite in battle,
and the Pokémon sprite used when looking at a Pokémon's status in your team menu
    - Required sprite size: `64x64px` sprite with `2` frames (`64x128px`)
    - Required palette size: `16` colors max
- `sfront_anim.png`: Shiny variant of the animation used when displaying the enemy's Pokémon sprite in battle, and
the Pokémon sprite used when looking at a Pokémon's status in your team menu
    - Same requirements as `front_anim.png`
    - Make sure that the sprite's pixel data matches the one from `front_anim.png`, as only the sprite's palette
    is used by the adjuster
- `back.png`: This sprite replaces the sprite used when displaying your Pokémon sprite in battle
    - Required sprite size: `64x64px` sprite
    - Required palette size: `16` colors max
- `sback.png`: Shiny variant of the sprite used when displaying your Pokémon sprite in battle
    - Optional if `sfront_anim.png` is given
    - Same requirements as `back.png`
    - Make sure that the sprite's pixel data matches the one from `back.png`, as only the sprite's palette
    is used by the adjuster
- `icon-X.png`: Icon used for the Pokémon in the team menu
    - Required sprite size: `32x32px` sprite with `2` frames (`32x64px`)
    - X must be a value between 0 and 2: This number will choose which icon palette to use
    - Icon palettes: [Palette 0](./icon_palette_0.pal), [Palette 1](./icon_palette_1.pal),
    [Palette 2](./icon_palette_2.pal)
    - Alternatively, `Venusaur` uses Palette 1, `Charizard` uses Palette 0, and `Blastoise` uses Palette 2. You can
    extract those objects to get icon sprites with the right palettes.
- `footprint.png`: Pokémon's footprint in the Pokédex
    - Required sprite size: `16x16px` sprite
    - Required palette: Exactly 2 colors: black (0, 0, 0) and white (255, 255, 255)

#### Pokémon Folder Exceptions

While most Pokémon follow the rules above, some of them have different requirements:

- Castform:
    - `front_anim.png` & `sfront_anim.png`:
        - Required sprite size: `64x64px` sprite with `4` frames (`64x256px`)
        - Required palette size: Exactly `64` colors
        - Each frame uses colors from its 16-color palette: Frame 1 uses colors 1-16 from the palette, Frame 2
        uses colors 17-32 from the palette, etc...
    - `back.png` & `sback.png`:
        - Required sprite size: `64x64px` sprite with `4` frames (`64x256px`)
        - Required palette size: Exactly `64` colors
        - Each frame uses colors from its 16-color palette: Frame 1 uses colors 1-16 from the palette, Frame 2
        uses colors 17-32 from the palette, etc...
- Deoxys:
    - `back.png` & `sback.png`:
        - Required sprite size: `64x64px` sprite with `2` frames (`64x128px`)
        - First frame for the Normal Deoxys form, second frame for the Speed Deoxys form
    - `icon-X.png`:
        - Required sprite size: `32x32` sprite with `4` frames (`32x128px`)
        - First two frames for the Normal Deoxys form, last two frames for the Speed Deoxys form
- All Unowns:
    - `front_anim.png` & `back.png`:
        - Palette: Only Unown A's palette is used for all Unowns, so the existing colors of the palette must be
        kept. Extract Unown A's sprites to get its palette, and only edit the pink colors in it
    - `sfront_anim.png` & `sback.png`:
        - Palette: Only Unown A's shiny palette is used for all Unowns, so the existing colors of the palette must
        be kept. Extract Unown A's sprites to get its shiny palette, and only edit the pink colors in it
    - `footprint.png`:
        - Only Unown A's footprint is used for all Unowns, thus this sprite doesn't exist within the ROM, and will
        be ignored by the adjuster
- Egg:
    - `hatch_anim.png`:
        - Required sprite size: `32x32px` sprite with `4` frames + `8x8px` sprite with `4` frames (`32x136px`)
        - Required palette size: `16` colors max
        - Extract the Egg sprite from the ROM to see this sprite's shape. It contains 4 frames for the hatching
        animation, and 4 frames for eggshells shards flying around after hatching

### Player Folder Specifications

Player folder names correspond to the name of the male and female players within Emerald: `Brendan` for the male
trainer, and `May` for the female trainer.

These sprites are separated in two categories: battle sprites and overworld sprites. The sprites' palettes must be
the same between battle sprites, and between overworld sprites, unless stated otherwise.

#### Player Folder Palettes

The palettes used for overworld sprites has some restrictions, as elements other than the player uses said palette:
- The arrow displayed when next to an exit from a sub-area (cave, dungeon) uses the color #10 from the palette,
- The exclamation mark displayed above trainers when they notice you before battling uses colors #15 and #16 from
the palette,
- The Pokémon you surf on in the overworld uses color #6 for its light shade, color #7 for its medium shade, and
color #16 for its dark shade,
- The Pokémon you fly on in the overworld uses color #6 for its light shade, color #7 for its medium shade, and
color #16 for its dark shade,

For this reason, color #15 of the player's overworld palette must be white (255, 255, 255), and color #16 must be
black (0, 0, 0).

#### Player Folder Sprites

- `battle_back.png`: `Battle` sprite. This sprite replaces the animation used when the player is throwing a ball,
whether it's at the beginning of a battle, or in the Safari Zone
    - Required sprite size: `64x64px` sprite with `4` OR `5` frames (`64x256px` OR `64x320px`)
    - Required palette size: Exactly `16` colors
    - If `4` frames are given, the player will use the `Emerald-style` ball throwing animation, and if `5` frames
    are given, the player will use the `Firered/Leafgreen-style` ball thowing animation
    - `Emerald-style` ball throwing animation: The last frame is the idle frame, the rest is the animation
    - `Firered/Leafgreen-style` ball throwing animation: The first frame is the idle frame, the rest is the
    animation
- `battle_front.png`: `Battle` sprite. This sprite replaces the sprite used when fighting your rival, at the
beginning and end of a battle, and the sprite used in the Trainer card.
    - Required sprite size: `64x64px` sprite
    - Required palette size: Exactly `16` colors
- `walking_running.png`: `Overworld` sprite. This sprite replaces the walking and running animations of the player
in the overworld.
    - Required sprite size: `16x32px` sprite with `18` frames (`16x576px`)
    - Required palette size: Exactly `16` colors, see [Player Folder Palettes](#player-folder-palettes)
- `reflection.png`: `Overworld` sprite. This sprite's palette is shown whenever the player stands in front of clear
water, in their reflection.
    - Required sprite size: `16x32px` sprite with `18` frames (`16x576px`)
    - Required palette size: Exactly `16` colors
    - The palette must be a faded version of the overworld palette, to look like a reflection of the player in the
    water
- `acro_bike.png`: `Overworld` sprite. This sprite replaces the Acro Bike animations of the player in the overworld.
    - Required sprite size: `32x32px` sprite with `27` frames (`32x864px`)
    - Required palette size: Exactly `16` colors, see [Player Folder Palettes](#player-folder-palettes)
- `mach_bike.png`: `Overworld` sprite. This sprite replaces the Mach Bike animations of the player in the overworld.
    - Required sprite size: `32x32px` sprite with `9` frames (`32x288px`)
    - Required palette size: Exactly `16` colors, see [Player Folder Palettes](#player-folder-palettes)
- `surfing.png`: `Overworld` sprite. This sprite replaces the surfing animations of the player in the overworld.
    - Required sprite size: `32x32px` sprite with `12` frames (`32x384px`)
    - Required palette size: Exactly `16` colors, see [Player Folder Palettes](#player-folder-palettes)
- `field_move.png`: `Overworld` sprite. This sprite replaces the animation used when the player uses an HM move in
the overworld such as Cut, Rock Smash or Strength.
    - Required sprite size: `32x32px` sprite with `5` frames (`32x160px`)
    - Required palette size: Exactly `16` colors, see [Player Folder Palettes](#player-folder-palettes)
- `underwater.png`: `Overworld` sprite. This sprite replaces the animation used when the player is swimming on a
Pokémon's back underwater.
    - Required sprite size: `32x32px` sprite with `9` frames (`32x288px`)
    - Required palette size: Exactly `16` colors. Since this palette is shared among both players, the existing
    colors of the palette must be kept. Extract the player's sprites to get its palette, and only edit colors #2
    to #5, and colors #11 to #16
- `fishing.png`: `Overworld` sprite. This sprite replaces the animation used when the player is fishing.
    - Required sprite size: `32x32px` sprite with `12` frames (`32x384px`)
    - Required palette size: Exactly `16` colors, see [Player Folder Palettes](#player-folder-palettes)
- `watering.png`: `Overworld` sprite. This sprite replaces the animation used when the player is watering berries.
    - Required sprite size: `32x32px` sprite with `9` frames (`32x288px`)
    - Required palette size: Exactly `16` colors, see [Player Folder Palettes](#player-folder-palettes)
- `decorating.png`: `Overworld` sprite. This sprite replaces the sprite used when the player is decorating their
secret base.
    - Required sprite size: `16x32px` sprite
    - Required palette size: Exactly `16` colors, see [Player Folder Palettes](#player-folder-palettes)

#### Player Folder Sprite Size Override

All overworld sprites frames can have a different size if you wish for your sprite to be bigger or smaller. In
order to change a sprite's size, you must add `-XxY` at the end of their file name, with `X` the width of the
sprite, and `Y` the height of the sprite.

Currently, only three overworld sprite sizes are allowed: `16x16px`, `16x32px` and `32x32px`.

For example, if you want the frames of the sprite `walking_running.png` to have a size of `32x32px`, then the
sprite must be named `walking_running-32x32.png`, and its size must be `32x576px`.

## Pokémon Data Edition

Once a sprite pack has been loaded into the adjuster, a `Sprite Preview` module will be added to it. It allows you
to preview the various sprites within the sprite pack, as well as their palette.

If a valid ROM or AP patch have been given, then the `Pokémon Data Editor` module will appear. This module allows
you to edit some data related to the Pokémon in the current sprite pack.

Here is a list of the values and their specifications:

- HP: The Pokémon's base HP. Must be a number between 1 and 255.
- Attack: The Pokémon's base attack. Must be a number between 1 and 255.
- Defense: The Pokémon's base defense. Must be a number between 1 and 255.
- Sp. Attack: The Pokémon's base special attack. Must be a number between 1 and 255.
- Sp. Defense: The Pokémon's base special defense. Must be a number between 1 and 255.
- Speed: The Pokémon's base speed. Must be a number between 1 and 255.
- Type 1: The Pokémon's first type. Select a value within the given list.
- Type 2: The Pokémon's second type. Select a value within the given list. Make it match the first type if you want
the Pokémon to only have one type.
- Ability 1: The Pokémon's first ability. Select a value within the given list.
- Ability 2: The Pokémon's second ability. Select a value within the given list. Make it match the first ability if
you want the Pokémon to only have one ability.
- Gender Ratio: The Pokémon's gender ratio. Select a value within the given list.
- Forbid Flip: Dictates whether the Pokémon's sprite can be flipped or not when looking at the Pokémon's status
screen in your team. The sprite can't be flipped if the option is ticked, otherwise it can be flipped.
- Move Pool: The Pokémon's level up learnset. Each line must contain a move. Each move must be written in the
format `<move>: <level>`, with `<move>` a known Pokémon move from this generation, and `<level>` a number between 1
and 100.

<u>**Warning:**</u> Some of these values may overwrite randomization options selected in Archipelago: if the
Pokémon's base stats or level up move pool have been randomized, the adjuster will replace the randomized values
with its values.

Hovering over a field's name will tell you more details about what kind of value it needs. Additionally, if the value's
text is red, blue or in bold, it will tell you exactly why.

Saving any changes for the Pokémon's data will create a file named `data.txt` in the Pokémon's folder. The contents of
the file should not be modified manually.

## Applying the Sprite Pack

Once both a ROM (or AP patch) and a sprite pack have been passed to the adjuster, you can press the `Adjust ROM`
button and a new ROM will be made from the patch application, whih is usable as-is.

In order to use this ROM instead of the standard AP-patched ROM with Archipelago, once BizHawk or any other
emulator is running, you should open the ROM made from the adjuster instead of the original one. Normally, the ROM
made by the adjuster should have the same name as the ROM or AP patch you passed to it, with `-adjusted` added at
the end of its name.
