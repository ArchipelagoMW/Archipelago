# Blasphemous Multiworld Setup Guide

## Useful Links

- Blasphemous: [Steam](https://store.steampowered.com/app/774361/Blasphemous/)
    - The GOG version of Blasphemous will also work.
- Blasphemous Mod Installer: [GitHub](https://github.com/BrandenEK/Blasphemous-Mod-Installer)
- Blasphemous Modding API: [GitHub](https://github.com/BrandenEK/Blasphemous-Modding-API)
- Blasphemous Randomizer: [GitHub](https://github.com/BrandenEK/Blasphemous-Randomizer)
- Blasphemous Multiworld: [GitHub](https://github.com/BrandenEK/Blasphemous-Multiworld)
- (*Optional*) PopTracker Pack: [GitHub](https://github.com/sassyvania/Blasphemous-Randomizer-Maptracker) 

## Mod Installer (Recommended)

1. Download the [Mod Installer](https://github.com/BrandenEK/Blasphemous-Mod-Installer) and point it to your install directory for Blasphemous.

2. Install the `Modding API`, `Randomizer`, and `Multiworld` mods. If you have the options enabled, then install the `Boots of Pleading` and `Double Jump` mods as well.

3. Start Blasphemous. To verfy that the mods are working, look for a version number for both the Randomizer and Multiworld on the title screen.

4. (*Optional*) Set up PopTracker by adding the Blasphemous pack. In game, open the console by pressing backslash `\` and type `randomizer autotracker on` to automatically connect the game to PopTracker.

## Manual Installation

1. Download the [Modding API](https://github.com/BrandenEK/Blasphemous-Modding-API/releases), and follow the [installation instructions](https://github.com/BrandenEK/Blasphemous-Modding-API#installation) on the GitHub page.

2. After the Modding API has been installed, download the [Randomizer](https://github.com/BrandenEK/Blasphemous-Randomizer/releases) and [Multiworld](https://github.com/BrandenEK/Blasphemous-Multiworld/releases) archives, and extract the contents of both into the `Modding` folder.

3. Start Blasphemous. To verfy that the mods are working, look for a version number for both the Randomizer and Multiworld on the title screen.

4. (*Optional*) Set up PopTracker by adding the Blasphemous pack. In game, open the console by pressing backslash `\` and type `randomizer autotracker on` to automatically connect the game to PopTracker.

## Connecting

To connect to an Archipelago server, open the in-game console by pressing backslash `\` and use the command `multiworld connect [address:port] [name] [password]`. The port and password are both optional - if no port is provided then the default port of 38281 is used.
**Make sure to connect to the server before attempting to start a new save file.**