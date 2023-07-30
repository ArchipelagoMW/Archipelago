# Undertale Randomizer Setup Guide

### Required Software

- Undertale from the [Steam page](https://store.steampowered.com/app/391540)
- Archipelago from the [Archipelago Releases Page](https://github.com/ArchipelagoMW/Archipelago/releases)
    - (select `Undertale Client` during installation.)

### First time setup

Start the Undertale client, and in the bottom text box, input `/auto_patch (Input your Undertale install directory here)` (It is usually located at `C:\Program Files\Steam\steamapps\Undertale`, but it can be different, you can more easily find the directory
by opening the Undertale directory through Steam), it will then make an Undertale folder that will be created in the
Archipelago install location. That contains the version of Undertale you will use for Archipelago. (You will need to
redo this step when updating Archipelago.)

**Linux Users**: This guide is mostly similar; however, when Undertale is installed on Steam, it defaults to a Linux
supported variant; this randomizer only supports the Windows version.  To fix this, right-click the game in Steam, go to
Properties -> Compatibility, and check "Force the use of a specific Steam Play compatibility tool".  This
downloads the Windows version instead.  If the play button is greyed out in Steam, be sure to go to
Settings -> Compatibility and toggle "Enable Steam Play for all other titles".

### Connect to the MultiServer

Make sure both Undertale and its client are running. (Undertale will ask for a saveslot, it can be 1 through 99, none 
of the slots will overwrite your vanilla save, although you may want to make a backup just in case.)

In the top text box of the client, type the 
`Ip Address` (or `Hostname`) and `Port` separated with a `:` symbol. (Ex. `archipelago.gg:38281`)

The client will then ask for the slot name, input that in the text box at the bottom of the client.

**Linux Users**: When you start the client, it is likely that the save data path is incorrect, and how the game
is played depends on where the save data folder is located.

*On Steam (via Proton)*: This assumes the game is in a Steam Library folder.  Right-click Undertale, go to Manage -> 
Browse Local Files.  Move back to the steamapps folder, open compatdata/391540 (391540 is the "magic number" for
Undertale in Steam and can be confirmed by visiting its store page and looking at the URL).  Save data from here is at
/pfx/drive_c/users/steamuser/AppData/Local/UNDERTALE.

*Through WINE directly*: This depends on the prefix used.  If it is default, then the save data is located at
/home/USERNAME/.wine/drive_c/users/USERNAME/AppData/Local/UNDERTALE.

Once the save data folder is located, run the /savepath command to redirect the client to the correct save data folder
before connecting.

### Play the game

When the console tells you that you have joined the room, you're all set. Congratulations on successfully joining a
multiworld game!

### PLEASE READ!

Please read this page in its entirety before asking questions! Most importantly, there is a list of 
gameplay differences at the bottom.
[Undertale Game Info Page](/games/Undertale/info/en)

### Where do I get a YAML file?

You can customize your settings by visiting the [Undertale Player Settings Page](/games/Undertale/player-settings)
