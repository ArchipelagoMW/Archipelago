# Slay the Spire Setup Guide

## Required Software

For steam-based installation, subscribe to the following mods:

- ModTheSpire from the [Slay the Spire Workshop](https://steamcommunity.com/sharedfiles/filedetails/?id=1605060445)
- BaseMod from the [Slay the Spire Workshop](https://steamcommunity.com/workshop/filedetails/?id=1605833019)
- Archipelago Multiworld Randomizer Mod from
  the [Slay the Spire Workshop](https://steamcommunity.com/sharedfiles/filedetails/?id=2596397288)

- For Xbox PC Game Pass installation:
  1. Download the official Steam Console Client [SteamCMD](https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip)
  2. Unpack that .zip file into some folder, right click steamcmd.exe and choose "Run as administrator".
  3. The client will now update itself. When it's ready type `login anonymous`. Now you are ready to download the actual
      mods.
  4. Mod the Spire: Type `workshop_download_item 646570 1605060445` in the SteamCMD window and hit Enter.
  5. BaseMod: Type `workshop_download_item 646570 1605833019` in the SteamCMD window and hit Enter.
  6. Archipelago Mod: Type `workshop_download_item 646570 2596397288` in the SteamCMD window and hit Enter.
  7. Open your Slay the Spire installation directory. By default this is `C:\XboxGames\Slay The Spire\Content`.
  8. In the folder where you unzipped SteamCMD there will now be a `steamapps` folder. Copy the ModTheSpire.jar from
      `steamapps\workshop\content\646570\1605060445\ModTheSpire.jar` to your Slay The Spire installation
      directory.
  9. Create a folder named `mods` inside the Slay The Spire installation directory. Copy
    "steamapps\workshop\content\646570\1605833019\BaseMod.jar" and
    "steamapps\workshop\content\646570\2596397288\ArchipelagoMW-0.1.11.jar" into that `mods` folder. Note that the
    version number of ArchipelagoMW may be different.

## Configuring your YAML file

### What is a YAML file and why do I need one?

Your YAML file contains a set of configuration options which provide the generator with information about how it should
generate your game. Each player of a multiworld will provide their own YAML file. This setup allows each player to enjoy
an experience customized for their taste, and different players in the same multiworld can all have different options.

### Where do I get a YAML file?

you can customize your settings by visiting
the [Slay the Spire Settings Page](/games/Slay%20the%20Spire/player-settings).

### Connect to the MultiServer

For Steam-based installations, if you are subscribed to ModTheSpire, when you launch the game, you should have the
option to launch the game with mods. On the mod loader screen, ensure you only have the following mods enabled and then
start the game:

- BaseMod
- Archipelago Multiworld Randomizer

For Xbox PC Game Pass installations, open the Slay The Spire installation directory, double-click on ModTheSpire.jar,
check both "Archipelago Multi-World" and "BaseMod" on the left and then click Play.

Once you are in-game, you will be able to click the **Archipelago** menu option and enter the ip and port (separated by
a colon) in the hostname field and enter your player slot name in the Slot Name field. Then click connect, and now you
are ready to climb the spire!
