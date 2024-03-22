# Slay the Spire Setup Guide

## Required Software

For Steam-based installation, subscribe to the following mods:

- [ModTheSpire](https://steamcommunity.com/sharedfiles/filedetails/?id=1605060445)
- [BaseMod](https://steamcommunity.com/workshop/filedetails/?id=1605833019)
- [Archipelago Multiworld Randomizer](https://steamcommunity.com/sharedfiles/filedetails/?id=2596397288)
- (optional) [Downfall](https://steamcommunity.com/sharedfiles/filedetails/?id=1610056683)
- (required for downfall) [StSLib](https://steamcommunity.com/workshop/filedetails/?id=1609158507)

For GOG or Xbox PC Game Pass installation:

1. Download the official Steam Console Client [SteamCMD](https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip).
2. Unpack that .zip file into some folder and double-click on `steamcmd.exe`.
3. The client will now update itself. When it's ready type `login anonymous`. Now you are ready to download the actual
    mods.
4. Run the following commands to download the required mod files:
  - Mod the Spire: `workshop_download_item 646570 1605060445`
  - BaseMod: `workshop_download_item 646570 1605833019`
  - ArchipelagoMW: `workshop_download_item 646570 2596397288`
  - (optional) Downfall: `workshop_download_item 646570 1610056683`
  - (required for Downfall) StSLib: `workshop_download_item 646570 1609158507`
5. Open your Slay the Spire installation directory. By default on GOG this is `C:\GOG Games\Slay the Spire`, on PC Game
    Pass this is `C:\XboxGames\Slay The Spire\Content`.
6. In the folder where you unzipped SteamCMD there will now be a `steamapps` folder. Copy ModTheSpire.jar from
    `steamapps\workshop\content\646570\1605060445\ModTheSpire.jar` to your Slay The Spire installation directory.
7. Create a folder named `mods` inside the Slay the Spire installation directory. Each folder inside
    `steamapps\workshop\content\646570` will have a single .jar file. Copy each of them except ModTheSpire.jar into the
    `mods` folder you made.
8. Now open Notepad. Paste in the following text: `jre\bin\java.exe -jar ModTheSpire.jar`. Go to "File -> Save as" and
    save it into your Slay the Spire installation directory with the name `"start.bat"`. Make sure to include the quotes
    in the file name!

## Configuring your YAML file

### What is a YAML file and why do I need one?

Your YAML file contains a set of configuration options which provide the generator with information about how it should
generate your game. Each player of a multiworld will provide their own YAML file. This setup allows each player to enjoy
an experience customized for their taste, and different players in the same multiworld can all have different options.

### Where do I get a YAML file?

you can customize your options by visiting
the [Slay the Spire Options Page](/games/Slay%20the%20Spire/player-options).

### Connect to the MultiServer

For Steam-based installations, if you are subscribed to ModTheSpire, when you launch the game, you should have the
option to launch the game with mods.

For GOG or Xbox PC Game Pass intallations, launch the game by double-clicking the `start.bat` file you created earlier
which will give you the option to launch the game with mods.

On the mod loader screen, ensure you only have the following mods enabled and then start the game:

- BaseMod
- Archipelago Multiworld Randomizer

If playing with Downfall, also make sure the following are enabled:

- Downfall
- StSLib

Once you are in-game, you will be able to click the **Archipelago** menu option and enter the ip and port (separated by
a colon) in the hostname field and enter your player slot name in the Slot Name field. Then click connect, and now you
are ready to climb the spire!
