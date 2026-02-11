from typing import Union

import settings
from .data.Constants import ROM_HASH, AGES_ROM_HASH


class OracleOfSeasonsSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Oracle of Seasons US ROM"""
        copy_to = "Legend of Zelda, The - Oracle of Seasons (USA).gbc"
        description = "OoS ROM File"
        md5s = [ROM_HASH]

    class AgesRomFile(settings.UserFilePath):
        """File name of the Oracle of Ages US ROM (only needed for cross items)"""
        copy_to = "Legend of Zelda, The - Oracle of Ages (USA).gbc"
        description = "OoA ROM File"
        md5s = [AGES_ROM_HASH]

    class OoSCharacterSprite(str):
        """
        The name of the sprite file to use (from "data/sprites/oos_ooa/").
        Putting "link" as a value uses the default game sprite.
        Putting "random" as a value randomly picks a sprite from your sprites directory for each generated ROM.
        If you want some weighted result, you can arrange the options like in your option yaml.
        """

    class OoSCharacterPalette(str):
        """
        The color palette used for character sprite throughout the game.
        Valid values are: "green", "red", "blue", "orange", and "random"
        If you want some weighted result, you can arrange the options like in your option yaml.
        If you want a color weight to only apply to a specific sprite, you can write color|sprite: weight.
        For example, red|link: 1 would add red in the possible palettes with a weight of 1 only if link is the selected sprite
        """

    class OoSRevealDiggingSpots(str):
        """
        If enabled, hidden digging spots in Subrosia are revealed as diggable tiles.
        """

    class OoSHeartBeepInterval(str):
        """
        A factor applied to the infamous heart beep sound interval.
        Valid values are: "vanilla", "half", "quarter", "disabled"
        """

    class OoSRemoveMusic(str):
        """
        If true, no music will be played in the game while sound effects remain untouched
        """

    rom_file: RomFile = RomFile(RomFile.copy_to)
    ages_rom_file: AgesRomFile = AgesRomFile(AgesRomFile.copy_to)
    rom_start: bool = True
    character_sprite: Union[OoSCharacterSprite, str] = "link"
    character_palette: Union[OoSCharacterPalette, str] = "green"
    reveal_hidden_subrosia_digging_spots: Union[OoSRevealDiggingSpots, bool] = True
    heart_beep_interval: Union[OoSHeartBeepInterval, str] = "vanilla"
    remove_music: Union[OoSRemoveMusic, bool] = False