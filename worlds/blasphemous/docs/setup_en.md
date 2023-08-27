# Blasphemous Multiworld Setup Guide

## Useful Links

Required:
- Blasphemous: [Steam](https://store.steampowered.com/app/774361/Blasphemous/)
    - The GOG version of Blasphemous will also work.
- Blasphemous Mod Installer: [GitHub](https://github.com/BrandenEK/Blasphemous-Mod-Installer)
- Blasphemous Modding API: [GitHub](https://github.com/BrandenEK/Blasphemous-Modding-API)
- Blasphemous Randomizer: [GitHub](https://github.com/BrandenEK/Blasphemous-Randomizer)
- Blasphemous Multiworld: [GitHub](https://github.com/BrandenEK/Blasphemous-Multiworld)

Optional:
- In-game map tracker: [GitHub](https://github.com/BrandenEK/Blasphemous-Rando-Map)
- Quick Prie Dieu warp mod: [GitHub](https://github.com/BadMagic100/Blasphemous-PrieWarp)
- Boots of Pleading mod: [GitHub](https://github.com/BrandenEK/Blasphemous-Boots-of-Pleading)
- Double Jump mod: [GitHub](https://github.com/BrandenEK/Blasphemous-Double-Jump)
- PopTracker pack: [GitHub](https://github.com/sassyvania/Blasphemous-Randomizer-Maptracker) 

## Mod Installer (Recommended)

1. Download the [Mod Installer](https://github.com/BrandenEK/Blasphemous-Mod-Installer),
and point it to your install directory for Blasphemous.

2. Install the `Modding API`, `Randomizer`, and `Multiworld` mods. Optionally, you can also install the
`Rando Map`, `PrieWarp`, `Boots of Pleading`, and `Double Jump` mods, and set up the PopTracker pack if desired.

3. Start Blasphemous. To verfy that the mods are working, look for a version number for both
the Randomizer and Multiworld on the title screen.

## Manual Installation

1. Download the [Modding API](https://github.com/BrandenEK/Blasphemous-Modding-API/releases), and follow
the [installation instructions](https://github.com/BrandenEK/Blasphemous-Modding-API#installation) on the GitHub page.

2. After the Modding API has been installed, download the 
[Randomizer](https://github.com/BrandenEK/Blasphemous-Randomizer/releases) and 
[Multiworld](https://github.com/BrandenEK/Blasphemous-Multiworld/releases) archives, and extract the contents of both
into the `Modding` folder. Then, add any desired additional mods.

3. Start Blasphemous. To verfy that the mods are working, look for a version number for both
the Randomizer and Multiworld on the title screen.

## Connecting

To connect to an Archipelago server, open the in-game console by pressing backslash `\` and use
the command `multiworld connect [address:port] [name] [password]`. 
The port and password are both optional - if no port is provided then the default port of 38281 is used.
**Make sure to connect to the server before attempting to start a new save file.**